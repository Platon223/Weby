from flask import Flask, request, make_response, render_template, session
import json
from app.extensions.db import db
from flask_migrate import Migrate
from flask_login import LoginManager
from app.extensions.bcrypt import bcrypt
from app.blueprints.api.models import User
from app.extensions.admin import admin
from dotenv import load_dotenv
import os
import openai

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.secret_key = '6424SecureKey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./testdb.db'
    openai.api_key = os.getenv('SECRET_API_KEY')

    bcrypt.init_app(app)

    admin.init_app(app)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from app.blueprints.api.models import User


    @login_manager.user_loader
    def load_user(password):
        return User.query.get(password)
    
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return render_template('401.html')
    

    # import and register blueprints

    from app.blueprints.api.routes import api
    from app.blueprints.auth.routes import auth
    from app.blueprints.core.routes import core
    from app.blueprints.chat.routes import chat_bl

    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(core, url_prefix='/home')
    app.register_blueprint(chat_bl, url_prefix='/chat')



    migrate = Migrate(app, db)

    return app