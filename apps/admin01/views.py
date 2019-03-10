from flask import url_for, request, abort, render_template, session
from flask_admin import Admin,BaseView,expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user,logout_user,login_user
from werkzeug.utils import redirect
from apps.extend import db
from flask_admin import AdminIndexView
from apps.news.models import News


class MyAdminIndexView(AdminIndexView):
    """后台用户登录"""
    @expose('/')
    def index(self):
        if session.get('authname',None) != 'zenglong':
            # return redirect(url_for('user.loginView'))
            return render_template('admin/authlogin.html')

        return super(MyAdminIndexView, self).index()


class CustomModelView(ModelView):
    """
    模型视图允许您添加一组专用管理页面，用于管理数据库中的任何模型。
    通过创建ModelView类的实例来执行此操作
    """
    # can_create = False
    # can_edit = False
    # can_delete = False
    # page_size = 50  # the number of entries to display on the list view
    # column_exclude_list = ['id', ]

    # 为了使搜索栏，或将其用于过滤，指定列名的列表
    # column_searchable_list = ['name', 'email']
    # column_filters = ['country']

"""
添加自己的视图
可以通过扩展BaseView类并定义自己的视图方法来添加一组独立视图（不依赖于任何特定模型） 。
例如，要添加显示来自第三方API的某些分析数据的页面
"""
from flask_admin import BaseView, expose
from apps.news.models import Hot,News,Tag

class AnalyticsView(BaseView):
    @expose('/')
    def index(self):
        tags = Tag.query.filter(Tag.is_delete==0).all()
        for tag in tags:
            news_count = News.query.filter(News.tid==tag.id).count()
            tag.news_count = news_count

        # 组织上下文模板
        context = {
            'tags':tags,
        }
        return self.render('admin/analytics_index.html',context=context)
