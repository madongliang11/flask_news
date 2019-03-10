import datetime
from jieba.analyse.analyzer import ChineseAnalyzer
from apps.extend import db

IS_DELETE = [
    (0,'存在'),
    (1,'删除')
]

class Cat(db.Model):
    __tablename__='cat'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    color=db.Column(db.String(20),nullable=False)

class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    t_name = db.Column(db.String(16), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    is_delete = db.Column(db.Integer, nullable=False)

class News(db.Model):
    __tablename__ = "news"
    __searchable__ = ['title', 'content']
    __analyzer__ = ChineseAnalyzer()

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tid = db.Column(db.Integer,db.ForeignKey(Tag.id), nullable=False)
    img_url = db.Column(db.String(300),nullable=True)
    created_time = db.Column(db.DateTime, default=datetime.datetime.now)
    is_delete = db.Column(db.Integer, default=0)
    img_finger=db.Column(db.String(300),nullable=True)

class NewsContentImg(db.Model):
    __tablename__ = "newscontentimgs"
    id = db.Column(db.Integer, primary_key=True)
    nid = db.Column(db.Integer,db.ForeignKey(News.id), nullable=False)
    img_url = db.Column(db.String(300),nullable=True)
    created_time = db.Column(db.DateTime, default=datetime.datetime.now)
    is_delete = db.Column(db.Integer, default=0)
    img_finger=db.Column(db.String(300),nullable=True)

class Hot(db.Model):
    __tablename__ = "hots"
    id = db.Column(db.Integer, primary_key=True)
    nid = db.Column(db.Integer,db.ForeignKey(News.id), nullable=False)
    count = db.Column(db.Integer, nullable=False)