"""
路由系统
"""
from flask_restful import Api

api = Api(prefix='/api/v1')

def init_api(app):
    api.init_app(app)

"""注册API路由系统"""
from apps.apis.indexapi import IndexApi

api.add_resource(IndexApi,'/index/',endpoint='index')

