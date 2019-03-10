import base64
from flask import Blueprint, render_template, request, redirect, url_for, session,make_response
from apps.news.models import Tag, News
from apps.user.models import *
from apps.extend import login_manager
from flask_login import login_user
from io import BytesIO


test = Blueprint('test',__name__,template_folder='templates')

@test.route("/")
def index():
    # 在首页加载的时候创建索引
    # flask_whooshalchemyplus.index_one_model(News)

    news = News.query.all()
    tags = Tag.query.all()
    user = User.query.filter(User.username == session.get('username')).first()
    # 组织上下文模板
    context = {
        'news':news,
        'tags':tags,
        'user': user
    }
    return render_template('index_test.html',**context)

@test.route("/search",methods = ['POST'])
def search():
    if not request.form['search']:
        return redirect(url_for('.index'))
    return redirect(url_for('.search_results', query=request.form['search']))


@test.route("/search_results/<query>")
def search_results(query):
    results = News.query.whoosh_search(query).all()
    print(results)
    return render_template('search_results.html', query=query, results=results)


@login_manager.user_loader
def _login_user(id):
    return User.query.get(id)


@test.route("/login",methods=['post','get'])
def loginView():
    if request.method=='POST':
        username=request.form.get('username')
        password = request.form.get('password')
        ver_code=request.form.get('code_text').upper()
        ver_img=session.get('img')
        user = User.query.filter(User.username==username).first()
        if user:
            if user.password==user.vertify_password(password):
                login_user(user)
                msg = {

                }
                return render_template('index_base.html')
            else:
                return render_template('error.html')


@test.route('/code')
def code():
    from apps.test_app.Verification_code import create_validate_code
    code_img, strs = create_validate_code()

    buf = BytesIO()
    code_img.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'

    session['img'] = strs.upper()

    return response


@test.route('/showupload/')
def uploadShowView():
    return render_template('upload.html')

@test.route('/upload')
def uploadView():
    # a = request.args.get('data')
    # image = a.split(',')[1]
    # print(f'b:{image}')
    # fh = open("heiqie.jpeg", "wb")
    # fh.write(base64.b64decode(image))
    # fh.close()
    image_str = request.args.get('data').split(',')[1]
    username = session.get('username')
    path = './apps/static/upload/img/' + username + '.png'
    with open(path, "wb") as file:
        file.write(base64.b64decode(image_str))
    return 'aaa'

@test.route('/sendemail')
def sendEmailView():
    username = 'zl'
    to_email = 'm18361480741@163.com'
    uid = 1
    from apps.celery_tasks import send_register_active_email
    send_register_active_email.apply_async(to_email=to_email, username=username, uid=uid)
    return 'success'

@test.route('/sendemail')
def activeEmailView():
    return 'success activeEmailView'


@test.route('/404')
def View404():
    return render_template('404.html')