from flask_script import Manager,Server
from flask_migrate import MigrateCommand
from apps import create_app
from apps.config import DEVELOP
from apps.extend import db

app = create_app(DEVELOP)

# Flask and Flask-SQLAlchemy initialization here

manage = Manager(app)
manage.add_command('run',Server(host='127.0.0.1',port=8000,use_debugger=True))
manage.add_command('db',MigrateCommand)

"""后台管理配置"""

from flask_admin import Admin
from apps.admin01.views import CustomModelView,AnalyticsView,MyAdminIndexView
from apps.news.models import Tag,NewsContentImg,News,Hot
from apps.user.models import User

admin = Admin(app,name='新闻网后台管理',template_mode='bootstrap3',index_view=MyAdminIndexView())
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# 模型视图
admin.add_view(CustomModelView(Tag,db.session,category='数据表'))
admin.add_view(CustomModelView(News,db.session,endpoint='News',category='数据表'))
admin.add_view(CustomModelView(NewsContentImg,db.session,category='数据表'))
admin.add_view(CustomModelView(Hot,db.session,category='数据表'))
admin.add_view(CustomModelView(User,db.session,endpoint='Users',category='数据表'))
# 独立视图
admin.add_view(AnalyticsView(name='Analytics', endpoint='analytics'))


if __name__ == '__main__':
    from apps.news.models import Tag, Hot, News, NewsContentImg
    from apps.user.models import User
    from apps.collection.models import Collection
    from apps.githubuser.models import Gituser
    manage.run()
