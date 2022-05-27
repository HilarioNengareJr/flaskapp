import timeago
from flask_login import UserMixin
from datetime import datetime
from appfiles import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


likes = db.Table('likes',
                 db.Column('post_id', db.Integer, db.ForeignKey('posts.pid')),
                 db.Column('user_id', db.Integer, db.ForeignKey('users.uid'))
                 )


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(35), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    def get_id(self):
        return (self.uid)

    def __repr__(self):
        return f"User('{self.username}', '{self.password}', '{self.image_file}')"


class Post(db.Model):
    __tablename__ = 'posts'
    pid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    media = db.Column(db.String(32), nullable=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    liked = db.relationship("User", secondary=likes)
    comments = db.relationship('Comment', backref='post', lazy=True)

    def __repr__(self):
        return f"Post('{self.content}', '{self.date_posted}')"


class Comment(db.Model):
    __tablename__ = 'comments'
    cid = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.pid'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Comment({self.post_id}, {self.user_id}, '{self.content}', '{self.date_posted}')"
