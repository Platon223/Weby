from flask import render_template, request, make_response, redirect, Blueprint, jsonify
from flask_login import login_required, current_user, login_user
from app.blueprints.api.models import User
from app.extensions.db import db
from app.extensions.bcrypt import bcrypt

core = Blueprint('core', __name__, template_folder='templates')

@core.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('home/index.html', username=current_user.username)
    else:
        return render_template('home/index.html', username='Guest')

@core.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'GET':
        user_password = current_user.password
        return render_template('home/profile.html', username=current_user.username, password='***********', email=current_user.email, job=current_user.job, role='Admin' if current_user.password == b'$2b$12$Gqpi0DWr8rtrBZM13TWffei9YFD5GhPUMVg6na7KR3BYFrkAvkkMO' else 'User')
    elif request.method == 'POST':
        data = request.get_json()
        update = data.get('change')
        newValue = data.get('newValue')
        user = User.query.get(current_user.username)

        if update == 'username':
            user.username = newValue
        elif update == 'password':
            new_hashed_password = bcrypt.generate_password_hash(newValue)
            user.password = new_hashed_password
        elif update == 'email':
            user.email = newValue
        elif update == 'job':
            user.job = newValue

        db.session.commit()

        return redirect('/auth/login')
    
        
        





