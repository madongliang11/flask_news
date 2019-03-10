import datetime
from apps.extend import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

'''
choice
'''
IS_ACTIVE = [
    (0, '未激活'),
    (1, '激活')
]
IS_DELETE = [
    (0, '存在'),
    (1, '删除')
]


class User(db.Model,UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String(200))
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    is_active = db.Column(db.Boolean, default=0)
    flag = db.Column(db.String(100))
    is_delete = db.Column(db.Boolean, default=0)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    # 当主键不为id时必须重写该方法
    # def get_id(self):
    #     return self.uid

    # 获取私有属性 password = user.password
    @property
    def passwordHandle(self):
        return self.password

    # 设置私有属性 user.password = "1111111"
    @passwordHandle.setter
    def passwordHandle(self, password):
        # if re.findall('^[A-Z]{1}(\w){5,11}',password):
        if password:
            self.password = generate_password_hash(password=password)
        else:
            raise Exception('密码不符合规范')

    """
    删除私有属性 del user.password
    @password.deleter
    def password(self):
        del self._password_hash
    """

    def vertify_password(self, password):
        return check_password_hash(self.password, password=password)

class AuthUser(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    def __str__(self):
        return self.email