from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from myshare.config import Config
import os


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "users.login"
#Changing the default login message
login_manager.login_message = "Please login to view home page"
login_manager.login_message_category = "error"

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    from myshare.users.routes import users
    from myshare.link_posts.routes import link_posts
    from myshare.main.routes import main
    from myshare.errors.handlers import errors
    
    
    app.register_blueprint(users)
    app.register_blueprint(link_posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    
    return app