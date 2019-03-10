import time
import base64

import flask_whooshalchemyplus
from flask import Blueprint, render_template, request, redirect, url_for,Flask, session,make_response
from apps.config import Config
from apps.news.models import Tag, Hot, News,NewsContentImg
from apps.user.models import *
from apps.extend import login_manager, mail,github
from flask_login import login_user, login_required
from io import BytesIO
from flask_mail import Message

from flask import jsonify

user = Blueprint('user', __name__,template_folder='templates')

'''用户中心'''


"""
Flask-Login要求程序实现一个回调函数，主要是获取存储到session中user对象
"""
@login_manager.user_loader
def load_user(id):
    """
    我们需要定义一个 LoginManager.user_loader 回调函数，
    它的作用是在用户登录并调用 login_user() 的时候, 根据 user_id 找到对应的 user, 如果没有找到，返回None,
    此时的 user_id 将会自动从 session 中移除, 若能找到 user ，则 user_id 会被继续保存
    :param id:
    :return:
    """
    return db.session.query(User).get(id)

# 登录
@user.route("/login",methods=['post','get'])
def loginView():
    if request.method=='POST':
        username=request.form.get('username')
        password = request.form.get('password')
        ver_code=request.form.get('code_text').upper()
        print(ver_code)
        ver_img=session.get('img')
        print(ver_img)
        if ver_img==ver_code:
            user = User.query.filter(User.username == username).first()
            if user:
                if user.vertify_password(password):
                    login_user(user)
                    session['username']=user.username
                    session['id']=user.id
                    session['img_url'] = user.img_url
                    return redirect(url_for('news.indexView'))
                else:
                    massage = '用户名或密码错误,请重新输入'
                    return redirect(url_for('news.indexView', msg=massage))
            else:
                massage='用户名或密码错误,请重新输入'
                return redirect(url_for('news.indexView',msg=massage))
        else:
            massage='验证码错误.请重新输入'
            return redirect(url_for('news.indexView',msg=massage))

@user.route('/ajax/',methods=['post'])
def ajaxHandle():
    username=request.values.get('name')
    user=User.query.filter(username==User.username).all()
    if user:
        return 'success'
    else:
        return ''

# 注册
@user.route('/register/',methods=['post','get'])
def registerView():

    # get方式返回注册页面
    if request.method == 'GET':
        return render_template('register.html')

    # post方式完成注册功能,并返回到首页
    elif request.method=='POST':

        # 获取数据
        username=request.form.get('username')
        password=request.form.get('password')
        email=request.form.get('email')
        phone=request.form.get('phone')
        user = User.query.filter(User.username == username).all()

        # 该用户未被注册,将信息保存,完成注册
        if not user:
            try:
                user = User()
                user.username = username
                user.email = email
                user.phone = phone
                # 将密码加密并保存
                user.passwordHandle=password
                db.session.add(user)
                db.session.commit()
            # 有错误,回滚
            except:
                db.session.rollback()
                return render_template('404.html')
        else:
            return render_template('register.html', msg='该用户名已被注册')
        # 注册成功,返回首页
        return redirect(url_for('news.indexView'))
    else:
        return render_template('404.html')



# 登出
@user.route('/logout/',methods=['post','get'])
def logoutView():
    del session['username']
    del session['id']
    return redirect(url_for('news.indexView'))

# 用户激活
@user.route('/activate/',methods=['post','get'])
def activateView():
    pass


#  发送邮件:密码修改前的验证
@user.route('/emailSend/',methods=['post','get'])
def emailSendView():

    # 先获取用户邮箱信息,用于验证
    if request.method=='GET':
        return render_template('/user_info_change/email_check.html')

    # 给用户发送邮件,完成验证
    elif request.method=='POST':
        email=request.form.get('email')
        user=User.query.filter(User.email==email).first()
        # 如果邮箱正确,发送邮件
        if user:
            try:
                msg = Message(subject="邮箱验证",
                              sender=Config.MAIL_USERNAME,
                              recipients=["13781041970@163.com"])

                context = {
                    'name': user.username,
                    'id': user.id
                }
                msg.html = render_template('/user_info_change/send_for_email_check.html', **context)
                mail.send(msg)
                return redirect(url_for('news.indexView'))
            except Exception as e:
                return redirect(url_for('test.View404'))
        else:
            return render_template('/user_info_change/email_check.html',msg='该邮箱未被注册')


@user.route('/passwordChange/',methods=['post','get'])
def passwordChangeView():
    if request.method=='GET':
        id=request.args.get('id')
        user=User.query.filter(User.id==id).first()
        return render_template('/user_info_change/passwordChange.html',username=user.username,id=id)
    elif request.method=='POST':
        id=request.form.get('id')
        password=request.form.get('password')
        user=User.query.filter(User.id==id).first()
        user.passwordHandle=password
        db.session.commit()
        login_user(user)
        session['username'] = user.username
        session['id'] = user.id
        return redirect(url_for('news.indexView'))
    else:
        return '404 错误的请求方式'

@user.route('/code')
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


# 管理后台用户登录
@user.route('/authlogin/',methods=['post'])
def authUserLogin():
    authname = request.form.get('authname')
    authpwd = request.form.get('authpwd')
    user = User.query.filter(User.username == 'zenglong').first()
    if authname == 'zenglong':
        if user.vertify_password(authpwd):
            login_user(user)
            session['authname'] = authname
            return redirect(url_for('admin.index'))
        else:
            context = {
                'msg' : '用户名或密码错误'
            }
            return render_template('admin/authlogin.html',**context)
    else:
        context = {
            'msg': '没有此用户'
        }
        return render_template('admin/authlogin.html',**context)

# 头像上传
@user.route('/showupload/')
def uploadShowView():
    return render_template('upload.html')

@user.route('/upload/')
def uploadView():
    image_str = request.args.get('data').split(',')[1]
    username = session.get('username')
    path = './apps/static/upload/img/' + username + '.png'
    with open(path, "wb") as file:
        file.write(base64.b64decode(image_str))

    user_img_url = '/static/upload/img/' + username + '.png'
    user = User.query.filter(User.username==username).first()
    user.img_url = user_img_url
    db.session.commit()

    # 如果用户更换头像,先清除session中的img_url
    if session.get('img_url',None):
        del session['img_url']

    return 'success'


# 用户中心
@user.route('/user_info/',methods=['post','get'])
def userInfoView():
    id=session.get('id')
    user=User.query.filter(User.id==id).first()
    tags = Tag.query.all()
    context={
        'user':user,
        'tags':tags
    }
    return render_template('user_info.html',**context)

