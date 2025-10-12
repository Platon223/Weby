from flask_admin import Admin, AdminIndexView
from app.extensions.db import db
from app.blueprints.api.models import User
from app.blueprints.chat.models import Message
from app.blueprints.chat.models import Chat
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import render_template

class AdminIndex(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.job == 'Admin'
    
    def inaccessible_callback(self, name, **kwargs):
        return render_template('401.html')

admin = Admin(index_view=AdminIndex())

class AdminUserView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.job == 'Admin'
    
    def inaccessible_callback(self, name, **kwargs):
        return render_template('401.html')

class AdminMessageView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.job == 'Admin'
    
    def inaccessible_callback(self, name, **kwargs):
        return render_template('401.html')
    
class AdminChatView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.job == 'Admin'
    
    def inaccessible_callback(self, name, **kwargs):
        return render_template('401.html')
    

admin.add_view(AdminUserView(User, db.session))
admin.add_view(AdminMessageView(Message, db.session))
admin.add_view(AdminChatView(Chat, db.session))