"""开发环境 部署的环境 测试环境"""
from datetime import timedelta

class Config:
    DEBUG = False
    SECRET_KEY = '24aa4d9f-9418-4500-aa51-8793db1b2670'
    # 用户session
    SESSION_TYPE = 'redis'
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    REMEMBER_COOKIE_NAME = 'session_id'
    # 邮箱
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USERNAME = 'az4565555@163.com'
    MAIL_PASSWORD = 'az4565555'

    # celery异步操作redis 配置
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/3'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/4'

    # github第三方配置
    GITHUB_CLIENT_ID = 'a05b1a2668bd705dddaa'
    GITHUB_CLIENT_SECRET = 'f7ed38ae7154fd8e9e914f8a6ec9bba3e787e895'

    # # redis缓存配置
    # # 默认的过期时间 单位秒
    # CACHE_DEFAULT_TIMEOUT= '60',
    # # 缓存类型
    # CACHE_TYPE= 'redis',
    # # IP地址
    # CACHE_REDIS_HOST= '127.0.0.1',
    # # 端口
    # CACHE_REDIS_PORT= '6379',
    # # 密码
    # # 连接数据库的编号
    # CACHE_REDIS_DB= ' 1',
    # # 缓存key的前缀
    # # CACHE_KEY_PREFIX= 'view_'



"""数据库配置"""
DATABASES_DEFAULT = 'default'
DATABASES_DEFAULT_ENGINE = 'mysql'
DATABASES_DEFAULT_DRIVER = 'pymysql'
DATABASES_DEFAULT_HOST = '192.168.1.107'
DATABASES_DEFAULT_PORT = '3306'
DATABASES_DEFAULT_CHARSET = 'utf8'


DATABASES = {
    'default': {
        'ENGINE': 'mysql',
        'NAME': 'wh_fl_news',
        'USER': 'zhougy',
        'PASSWORD': '123456',
        'PORT': '3306',
        'HOST': '192.168.1.107',
        'CHARSET': 'utf8',
        'DRIVER': 'pymysql'
    },
    'dev': {
        'ENGINE': 'mysql',
        'NAME': 'wh_1804_fl_news',
        'USER': 'root',
        'PASSWORD': '123456',
        'PORT': '3306',
        'HOST': '120.79.31.195',
        'CHARSET': 'utf8',
        'DRIVER': 'pymysql'
    },
    'pro': {
        'ENGINE': 'mysql',
        'NAME': 'wh_1804_fl_news',
        'USER': 'root',
        'PASSWORD': '123456',
        'PORT': '3306',
        'HOST': '120.79.31.195',
        'CHARSET': 'utf8',
        'DRIVER': 'pymysql'
    }
}

def get_db_uri(key):
    database_config = DATABASES.get(key) if key else DATABASES.get(DATABASES_DEFAULT)
    engine = database_config.get('ENGINE') or DATABASES_DEFAULT_ENGINE
    driver = database_config.get('DRIVER') or DATABASES_DEFAULT_DRIVER
    host = database_config.get('HOST') or DATABASES_DEFAULT_HOST
    port = database_config.get('PORT') or DATABASES_DEFAULT_PORT
    user = database_config.get('USER')
    name = database_config.get('NAME')
    password = database_config.get('PASSWORD')
    charset = database_config.get('CHARSET')
    return f'{engine}+{driver}://{user}:{password}@{host}:{port}/{name}?charset={charset}'

# 部署环境
class ProductConfig(Config):
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/fl_taopiao'
    SQLALCHEMY_DATABASE_URI = get_db_uri('default')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# 开发环境
class DevelopConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = get_db_uri('default')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

DEVELOP = 'dev'
PRODUCT = 'pro'
env = {
    'pro':DevelopConfig,
    'dev':ProductConfig
}


