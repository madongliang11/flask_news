from flask_restful import fields

news_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    # 'tid': fields.Integer,
    # 'img_url': fields.String,
    # 'created_time': fields.String,
}

tags_fields = {
    # 'id': fields.Integer,
    't_name': fields.String,
    # 'create_time': fields.String,
}

img_fields={
    # 'id':fields.Integer,
    'img_url':fields.String
}

data_fields = {
    'tags': fields.List(fields.Nested(tags_fields)),
    'news': fields.List(fields.Nested(news_fields)),
    'img_url': fields.List(fields.Nested(img_fields)),
}

result = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.Nested(data_fields)
}