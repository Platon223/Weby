from flask import render_template, request, Blueprint, make_response, redirect, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from app.blueprints.api.models import User
from app.extensions.bcrypt import bcrypt
import uuid
from app.extensions.db import db


auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.get(username)

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)

            return redirect('/home/')
        else:
            return jsonify({"message": "user not found"})


    return

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/signup.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        job = request.form.get('job')
        email = request.form.get('email')
        avatar = request.form.get('avatar')
        id = uuid.uuid4()
        hashed_password = bcrypt.generate_password_hash(password)

        if username and password and email and id:

            if avatar:
                pass

            user = User(username = username, password = hashed_password, email = email, id = str(id), job = job)

            db.session.add(user)
            db.session.commit()

            return redirect('/auth/login')
        else:
            return jsonify({"message": 'all fileds are required'})
        

@auth.route('/logout', methods=['POST'])
@login_required
def logout():

    logout_user()

    return redirect('/auth/login')