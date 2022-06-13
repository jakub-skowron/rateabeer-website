from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, url_for


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@login.unauthorized_handler
def unauthorized():
    return redirect(url_for("login"))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beer_name = db.Column(db.String(255))
    brewery_name = db.Column(db.String(255))
    beer_style = db.Column(db.String(255))
    beer_comment = db.Column(db.String(255))
    beer_rate = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    edition = db.Column(db.String(255), default='Unedited')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User (UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, unique=True)
    email = db.Column(db.String(255), index=True, unique=True)
    password_hash = db.Column(db.String(255))
    joined_at_date = db.Column(db.DateTime(), index=True, default=datetime.utcnow())
    posts = db.relationship("Post", backref = "author", lazy = "dynamic")

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

