import datetime
from flask import Blueprint, session, request, redirect, url_for,render_template
from sqlalchemy import and_

from apps.collection.models import Collection
from apps.extend import db
from apps.news.models import News

collection = Blueprint('collection', __name__,template_folder='templates')

'''收藏页'''


# 展示收藏
@collection.route('/show/',methods=['post','get'])
def showView():

    if request.method=='GET':
        uid=session.get('id')
        if uid:
            collection_news = Collection.query.filter( and_(Collection.uid==uid,Collection.is_delete==0)).all()
            for collection_new in collection_news:
                new=News.query.filter(News.id==collection_new.nid).first()
                collection_new.new = new
            #组织桑下文模板
            context = {
                'collection_news':collection_news
            }
            return render_template('collectview.html',**context)


# 添加到收藏
@collection.route('/add/',methods=['post','get'])
def addView():
    nid = request.args.get('nid')
    uid = request.args.get('uid')
    collectnews = Collection.query.filter_by(nid=nid,uid=uid).first()
    if collectnews:
        message = '您已经收藏了!~'
    else:
        collectnews =Collection(uid=uid, nid=nid,is_delete=0)
        message = '收藏成功!~'
    db.session.add(collectnews)
    db.session.commit()

    return redirect(url_for('news.detailView',nid=nid,uid=uid,message=message))
# 删除收藏
@collection.route('/delete/',methods=['post','get'])
def deleteView():
    nid = request.args.get('nid')
    uid = session.get('id')
    collectnews = Collection.query.filter_by(nid=nid,uid=uid).first()
    if collectnews:
        collectnews.is_delete = 1
        db.session.commit()
        message = '收藏成功!~'
    else:
        message = '您未收藏!~'

    return redirect(url_for('news.detailView',nid=nid,uid=uid,message=message))



# 收藏内容
@collection.route('/collect/',methods=['post','get'])
def collectionView():
    pass
