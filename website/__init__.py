
from flask import Flask, redirect, render_template, request, send_file, session, flash, jsonify, Response, url_for , Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null, true,desc
from flask_msearch import Search
from hashlib import *
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_login import *
import numpy as np
from flask_mail import Mail, Message, Attachment
from werkzeug.utils import secure_filename
import datetime
from requests import get
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy(session_options={"autoflush": False})
app = Flask(__name__)


ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.secret_key = 'hard-to-guess-key'
    app.config.update(dict(
        DEBUG = True,
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = 587,
        MAIL_USE_TLS = True,
        MAIL_USE_SSL = False,
        MAIL_USERNAME = os.environ.get('MAIL_USERNAME'),
        MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD'),
    ))
    mail = Mail(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///APP.db'
else:
    app.debug = False
    app.secret_key = os.environ.get('SECRET')
    app.secret_key = os.environ.get('reCAPTCHA')
    app.config['MAIL_SERVER']='smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USERNAME'] = os.environ.get('email')
    app.config['MAIL_PASSWORD'] = os.environ.get('email_pass')
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PIPENV_IGNORE_VIRTUALENVS']=True


def create_app():
    
    db.init_app(app)

    from .views import views
    from .employers import employers
    from .employees import employees

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(employees, url_prefix = '/')
    app.register_blueprint(employers, url_prefix = '/')

    from .models import Users_database,REQUESTS_database

    #create_database(app)

    search = Search(app)
    search.init_app(app)
    #search.create_index(update=True)
    MSEARCH_INDEX_NAME =  os.path.join(app.root_path,'msearch')
    MSEARCH_PRIMARY_KEY = 'id'
    MSEARCH_ENABLE = True

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view ="login"

    #create_mail_server(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Users_database.query.get(int(user_id))
    
    return app

def create_mail_server(app):
    mail = Mail(app)
    return mail

def create_database(app):
    db.create_all(app=app)
    print('Database created!')