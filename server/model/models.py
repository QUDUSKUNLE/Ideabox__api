import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from configuration import app_config


app = Flask(__name__, template_folder='templates')
app_config(app)
db = SQLAlchemy(app)


class User(db.Model):
    """User model"""

    __tablename__ = 'user'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(120), unique=True)
    reset_password_link = db.Column(db.String)
    idea = db.relationship('Idea', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref='user', lazy='dynamic')
    subcomment = db.relationship('SubComment', backref='user', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())


class Idea(db.Model):
    """Idea model"""

    __tablename__ = 'idea'

    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String(200), unique=True)
    description = db.Column(db.String)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    category_id = db.Column(db.String, db.ForeignKey('category.id'))
    idea_status = db.Column(db.String, db.ForeignKey('tag.id'))
    comment = db.relationship('Comment', backref='idea', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())


class Category(db.Model):
    """"Idea category"""

    __tablename__ = 'category'

    id = db.Column(db.String, primary_key=True)
    category_type = db.Column(db.String)
    idea = db.relationship('Idea', backref='category', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())


class Comment(db.Model):
    """Comment table"""

    __tablename__ = 'comment'

    id = db.Column(db.String, primary_key=True)
    comment = db.Column(db.String)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    idea_id = db.Column(db.String, db.ForeignKey('idea.id'))
    sub_comment = db.relationship(
        'SubComment', backref='comment', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())


class SubComment(db.Model):
    """Sub comment table"""

    __tablename__ = 'subcomment'

    id = db.Column(db.String, primary_key=True)
    sub_comment = db.Column(db.String)
    comment_id = db.Column(db.String, db.ForeignKey('comment.id'))
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())


class Tag(db.Model):
    """Idea status"""

    __tablename__ = 'tag'

    id = db.Column(db.String, primary_key=True)
    idea_tag = db.Column(db.String(10))
    idea_status = db.relationship('Idea', backref='tag', lazy='dynamic')
