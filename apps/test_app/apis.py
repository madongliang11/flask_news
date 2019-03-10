from flask_restful import Resource, marshal_with, fields
import json

from apps.news.models import News, Tag, NewsContentImg

class Result:
    @staticmethod
    def get_result(data=None, status=200, msg='success'):
        return {
            'status': status,
            'msg': msg,
            'data': data
        }

    @staticmethod
    def get_result(status=404, msg='error'):
        return {
            'status': status,
            'msg': msg
        }

user_fields={
    'id':fields.Integer,
    'name':fields.String,
}

news_fields={
    'id':fields.Integer,
    'title':fields.String,
    'content':fields.String,
}

newscontentimg_fields={
    'img_url':fields.String,
}

result = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.Nested(news_fields)
}

class IndexApi(Resource):
    @marshal_with(result)
    def get(self):
        title_query=News.query.filter(News.is_delete==0).all()
        content_query=News.query.filter(News.is_delete==0).all()
        t_name_query=Tag.query.filter(Tag.is_delete==0).all()
        img_url_query=NewsContentImg.query.filter(NewsContentImg.is_delete==0).all()

        title=title_query.all()
        content=content_query.all()

        t_name=t_name_query.all()
        img_url=img_url_query.all()

        data = {
            'title': title,
            'content': content,
            't_name': t_name,
            'img_url': img_url,
        }

        return Result.get_result(data)