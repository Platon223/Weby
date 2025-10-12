from flask import request, make_response, redirect, Blueprint, render_template
from flask_login import login_required, current_user
from app.main import db
from app.blueprints.api.models import User

api = Blueprint('api', __name__, template_folder='templates')

@api.route('/all_users')
@login_required
def all_users():
    if current_user.job == 'Admin':

        users = User.query.all()

        return render_template('admin/users.html', users=users)
    else:
        return render_template('error/401.html')