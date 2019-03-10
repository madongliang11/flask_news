from apps import create_app
from apps.config import DEVELOP

"""
启动celery之前需要加载flask的app的配置，因此需要创建一个app对象给celery使用
"""
flask_app = create_app(DEVELOP)

from apps.extend import celery
