from flask_restful import Resource, marshal_with, fields, reqparse

from apps.apis.fields import result
from apps.news.models import Tag, News, NewsContentImg


class IndexApi(Resource):
    @marshal_with(result)
    def get(self):
        tags = Tag.query.limit(10).all()
        news = News.query.limit(10).all()
        img_url = NewsContentImg.query.limit(10).all()
        data = {
            'data': {
                'tags': tags,
                'news': news,
                'img_url': img_url,
            }
        }
        return data

    def post(self):
        pass
