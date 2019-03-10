from flask import Blueprint, render_template, request, redirect, url_for, session
from sqlalchemy import desc

from apps.user.models import User
from apps.collection.models import Collection
from apps.extend import db
from apps.news.models import Tag, News, NewsContentImg, Hot

news = Blueprint('news',__name__,template_folder='templates')

######主页#######
@news.route('/',methods=['get'])
def indexView():
    msg = request.args.get('msg')
    news = News.query.all()
    tags = Tag.query.all()
    hots = Hot.query.order_by(desc(Hot.count)).limit(7).all()
    for hot in hots:
        hotnews= News.query.filter_by(id=hot.nid).first()
        hot.new = hotnews

    try:
        del session['img_url']
    except:
        pass

    user = User.query.filter(User.username==session.get('username')).first()
    if user:
        img_url = user.img_url
        session['img_url'] = img_url
    # 组织上下文模板
    context = {
        'hots': hots,
        'news': news,
        'tags':tags,
        'msg': msg,
        'user':user
    }
    return render_template('index.html', **context)



######详情页#######
@news.route("/detail/",methods=['post','get'])
def detailView():
    message = request.args.get('message')
    id = request.args.get('nid')
    news = News.query.filter_by(id=id).first()
    user = User.query.filter_by(username=session.get('username')).first()
    bigimgs = NewsContentImg.query.filter_by(nid=id).first()
    collectnews = Collection.query.filter_by(nid=id).first()
    hotnews = Hot.query.filter_by(nid=id).first()
    if hotnews :
        hotnews.count += 1
    else:
        hotnews = Hot(nid=id,count=1)
    db.session.add(hotnews)
    db.session.commit()
    context = {
        'news': news,
        'bigimgs':bigimgs,
        'collectnews':collectnews,
        'user':user,
        'message':message,

    }
    return render_template('detail.html', **context)

######搜索页#######
@news.route("/search",methods = ['POST'])
def search():
    if not request.form['search']:
        return redirect(url_for('.index'))
    return redirect(url_for('.search_results', query=request.form['search']))


@news.route("/search_results/<query>")
def search_results(query):
    results = News.query.whoosh_search(query).all()
    print(results)
    return render_template('search_results.html', query=query, results=results)


######分类页#######
@news.route('/classify/',methods=['post','get'])
def classifyView():
    tid = request.args.get("tid")
    page = request.args.get("page",default=1,type=int)
    news = News.query.filter_by(tid=tid).paginate(page=page,per_page=5)
    context = {
        'pagination':news,
        'news':news.items,
        'tid':tid,
    }
    return render_template('classify.html',**context)

######今日热点######
@news.route('/todayhotnews/',methods=['post','get'])
def todayHotNews():
    news = News.query.order_by(desc(News.created_time)).limit(8)
    context = {
        'news': news,
    }
    return render_template('todayhotnews.html', **context)


# 赛选 多重赛选


# 富文本编辑
@news.route('/ckupload/',methods=['post','get'])
def ckUpload():
    return 'success'