from flask import Flask, request, g, session, redirect, url_for, render_template, jsonify, flash, Blueprint
from sqlalchemy import and_, desc
from apps.extend import github, db
from apps.githubuser.models import Gituser
from apps.news.models import News, Hot, Tag

githubuser = Blueprint('githubuser', __name__,template_folder='templates')

@githubuser.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = Gituser.query.get(session['user_id'])

# 创建登录按钮
@githubuser.route('/')
def index():
    if g.user:
        is_login = True
        response = github.get('user')
        avatar = response['avatar_url']
        username = response['name']
        url = response['html_url']

        news = News.query.all()
        tags = Tag.query.all()
        hots = Hot.query.order_by(desc(Hot.count)).limit(7).all()
        for hot in hots:
            hotnews = News.query.filter_by(id=hot.nid).first()
            hot.new = hotnews

        # 组织上下文模板
        context = {
            'is_login' : is_login,
            'avatar' : avatar,
            'username' : username,
             'url' : url,
            'hots': hots,
            'news': news,
            'tags': tags,
        }
        return render_template('index.html',**context )

    # 如果未登录
    is_login = False
    context = {
        'is_login': is_login,
    }
    return render_template('gitindex.html',**context)

# 因为我们在进行授权时请求了repo权限，我们还可以对用户的仓库进行各类操作
@githubuser.route('/star/helloflask')
def star():
    github.put('user/starred/greyli/helloflask', headers={'Content-Length': '0'})
    flash('Star success.')
    return redirect(url_for('.index'))

# 因为我们需要在其他视图里调用GitHub资源，为了避免每次都获取和传入访问令牌，
# 我们可以使用github.access_token_getter装饰器创建一个统一的令牌获取函数：
# 当你在某处直接使用github.get()等方法而不传入访问令牌时，
# GitHub-Flask会通过你提供的这个回调函数来获取访问令牌。
@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user.github_access_token

# 获取access令牌（访问令牌）
@githubuser.route('/callback/github/')
@github.authorized_handler
def authorized(access_token):
    print(access_token)
    if access_token is None:
        flash('Login failed.')
        return redirect(url_for('.index'))

    # 创建新用户，保存访问令牌，登入用户等操作

    # 获取响应信息,github返回一个字典
    response = github.get('user', access_token=access_token)
    # 得到github用户名
    username = response['login']
    user = Gituser.query.filter_by(username=username).first()

    if user is None:
        # user = Gituser(username=username, github_access_token=access_token)
        user = Gituser(access_token)
        user.username = username
        user.github_access_token = access_token
        db.session.add(user)
    user.github_access_token = access_token  # update access token
    db.session.commit()
    flash('Login success.')
    # log the user in
    # if you use flask-login, just call login_user() here.
    session['user_id'] = user.id
    return redirect(url_for('.index'))

# 登入
@githubuser.route('/login')
def login():
    # print(session.get('user_id'))
    # 如果用户没有登录
    if session.get('user_id', None) is None:
        return github.authorize(scope='repo')
    # 如果用户已经登录
    flash('Already logged in.')
    return redirect(url_for('.index'))

# 登出
@githubuser.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Goodbye.')
    return redirect(url_for('.index'))

# 对应用户资料，返回的 JSON 数据
@githubuser.route('/user')
def get_user():
    return jsonify(github.get('user'))




'''
/user端点对应用户资料，返回的 JSON 数据如下所示：
{
 "avatar_url": "https://avatars3.githubusercontent.com/u/12967000?v=4", 
 "bio": null, 
 "blog": "greyli.com", 
 "company": "None", 
 "created_at": "2015-06-19T13:00:23Z", 
 "email": "withlihui@gmail.com", 
 "events_url": "https://api.github.com/users/greyli/events{/privacy}", 
 "followers": 132, 
 "followers_url": "https://api.github.com/users/greyli/followers", 
 "following": 8, 
 "following_url": "https://api.github.com/users/greyli/following{/other_user}", 
 "gists_url": "https://api.github.com/users/greyli/gists{/gist_id}", 
 "gravatar_id": "", 
 "hireable": true, 
 "html_url": "https://github.com/greyli", 
 "id": 12967000, 
 "location": "China", 
 "login": "greyli", 
 "name": "Grey Li", 
 "node_id": "MDQ6VXNlcjEyOTY3MDAw", 
 "organizations_url": "https://api.github.com/users/greyli/orgs", 
 "public_gists": 7, 
 "public_repos": 61, 
 "received_events_url": "https://api.github.com/users/greyli/received_events", 
 "repos_url": "https://api.github.com/users/greyli/repos", 
 "site_admin": false, 
 "starred_url": "https://api.github.com/users/greyli/starred{/owner}{/repo}", 
 "subscriptions_url": "https://api.github.com/users/greyli/subscriptions", 
 "type": "User", 
 "updated_at": "2018-06-24T02:05:38Z", 
 "url": "https://api.github.com/users/greyli"
}复制代码
'''