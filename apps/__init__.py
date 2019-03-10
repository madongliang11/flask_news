import flask_whooshalchemyplus
from flask import Flask
from apps.config import env
from apps.extend import init_extend
from apps.news.models import News
from apps.urls import init_api

def create_app(env_name):
    app = Flask(__name__)
    app.debug = True
    app.config.from_object(env.get(env_name))

    init_extend(app)
    init_blue(app)
    init_api(app)

    return app

# 测试专用
from apps.test_app.views import test

from apps.news.views import news
from apps.collection.views import collection
from apps.user.views import user
from apps.githubuser.views import githubuser

def init_blue(app):
    # 测试专用
    app.register_blueprint(test)

    app.register_blueprint(news,url_prefix='/news')
    app.register_blueprint(collection,url_prefix='/collection')
    app.register_blueprint(user,url_prefix='/user')
    app.register_blueprint(githubuser,url_prefix='/githubuser')


