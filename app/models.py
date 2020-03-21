from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='static/images/social/profile.jpg')
    password = db.Column(db.String(60), nullable=True)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    posts = db.relationship('Post', backref='user', lazy=True)
    profile = db.relationship('UserProfile', backref='user', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.image_file}', '{self.member_since}')"

class UserProfile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), unique=True, nullable=True)
    birthday = db.Column(db.DateTime(), nullable=True)
    marital_status = db.Column(db.String(10), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    mobile_number = db.Column(db.String(20), nullable=True)
    twitter_id = db.Column(db.String(60), nullable=True)
    skype_id = db.Column(db.String(60), nullable=True)
    website = db.Column(db.String(60), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
            return f"UserProfile('{self.id}', '{self.full_name}', '{self.gender}', '{self.birthday}', '{self.mobile_number}')"


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.id}', '{self.title}', '{self.date_posted}', '{self.user_id}')"
