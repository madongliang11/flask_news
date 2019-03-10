from apps.extend import db


class Gituser(db.Model):
    __tablename__ = 'gituser'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    github_access_token = db.Column(db.String(200))

    def __init__(self, access_token):
        self.github_access_token = access_token
