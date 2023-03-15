from myshare import db, login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin
import jwt
import time


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    links = db.relationship("Link", backref="author", lazy=True)
    
    def get_reset_token(self, expires_sec= int(time.time()) + 1800):
        payload = {'user_id': self.id, 'exp': expires_sec}
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token 
     
    @staticmethod
    def verify_reset_token(token): 
        try:
            # payload = {'user_id': self.id, 'exp': expires_sec}
            token_ = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = token_['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return f"User('{self.username}, {self.email}, {self.image_file}')"
    
class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    
    def __repr__(self):
        return f"Post('{self.title}, '{self.content}')"