# 第三方扩展插件的配置文件
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from flask_mail import Mail
from flask_celery import Celery
from flask_caching import Cache
import flask_whooshalchemyplus
from flask_admin import Admin
from flask_github import GitHub

"""初始化所有配置"""

# resources支持指定的特定路径
cors = CORS()
def init_cors(app):
    cors.init_app(app,resources={r"/api/*":{"origins":"*"}})


mail = Mail()
def init_mail(app):
    mail.init_app(app)

# github
github = GitHub()
def init_github(app):
    github.init_app(app)


login_manager = LoginManager()
def init_login(app):
    # 指定了未登录时跳转的页面
    login_manager.login_view = ''
    login_manager.init_app(app)

# flask全文搜索
def init_whoosh(app):
    flask_whooshalchemyplus.init_app(app)

"""
在使用工厂模式时
由于程序初始化的时候并不能创建出app对象，
所以celery启动的时候必须先在tasks中导入app对象才能完成初始化，
可能导致循环导入的错误；
"""
celery = Celery()
def init_celery(app):
    celery.init_app(app=app)

cache = Cache()
def init_cache(app):
    cache.init_app(app, config={
        # 默认的过期时间 单位秒
        'CACHE_DEFAULT_TIMEOUT': 60,
        # 缓存类型
        'CACHE_TYPE': 'redis',
        # IP地址
        'CACHE_REDIS_HOST': '127.0.0.1',
        # 端口
        'CACHE_REDIS_PORT': 6379,
        # 密码
        # 连接数据库的编号
        'CACHE_REDIS_DB': 1,
        # 缓存key的前缀
        'CACHE_KEY_PREFIX': 'view_'
    })



"""只做实例化和初始化的操作"""

# =========数据库配置 start=========

# 实例化(数据库操作核心对象,数据库迁移对象)
migrate=Migrate()
db=SQLAlchemy()
# 初始化数据库  (注册)
def init_db(app):
    # config_db(app)
    db.init_app(app=app)
    migrate.init_app(app=app,db=db)

# 配置数据库连接
# def config_db(app):
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/fl_restful'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
#     # 加这一句就不需要加commit
#     app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True

# =========数据库配置 end=========

def init_extend(app):
    init_db(app)
    init_cors(app)
    init_login(app)
    init_mail(app)
    # init_celery(app)
    init_cache(app)
    init_whoosh(app)
    init_github(app)

