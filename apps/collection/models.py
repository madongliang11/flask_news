import datetime
from apps.extend import db
from apps.user.models import User
from apps.news.models import News

IS_DELETE = [
    (0,'存在'),
    (1,'删除')
]

class Collection(db.Model):
    __tablename__ = "collections"
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer,db.ForeignKey(User.id))
    nid = db.Column(db.Integer,db.ForeignKey(News.id))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    is_delete = db.Column(db.Boolean,default=0)