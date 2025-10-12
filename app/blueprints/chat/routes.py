from flask import render_template, jsonify, request, Blueprint, redirect, make_response
from flask_login import current_user, login_required
from app.blueprints.chat.models import Message
from app.blueprints.chat.models import Chat
from datetime import datetime
from app.extensions.db import db
import openai
import uuid
import json
from dotenv import load_dotenv
import os

load_dotenv()

ai_key = os.getenv('SECRET_API_KEY')

chat_bl = Blueprint('chat_bl', __name__, template_folder='templates')

@chat_bl.route('/<chat_id>', methods=['GET','POST'])
@login_required
def chat(chat_id):
    def ai_response(chat_id, user_message):
        history = Message.query.filter_by(chat_id=chat_id).order_by(Message.timestamp).all()
        messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]

        if history:

            for message in history:
                messages.append({'role': 'user' if message.sender == 'user' else 'bot', 'content': message.content})
                messages.append({'role': 'user', 'content': user_message})
        else:
            messages.append({'role': 'user', 'content': user_message})

        try:
            ai_res = openai.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=messages
            )

            return ai_res.choices[0].message.content
        except Exception as e:
            return f'error generating the response: {e}'
    
    if request.method == 'GET':
        chid = Chat.query.get(chat_id)
        if chid:
            messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.timestamp).all()
            messages_data_converted = [msg.to_dict() for msg in messages]
            

            chats = Chat.query.all()
            chats_data_converted = [cht.to_dict() for cht in chats]
            
            


            return render_template('chat/chat.html', chat_name=chid.name, messages=messages_data_converted, all_chats=chats_data_converted, api_key=ai_key)
        else:
            return redirect('/chat/dashboard')
    elif request.method == 'POST':


        data = request.get_json()
        message = data.get('message')

        if not message:
            return jsonify({'message': 'the message is empty, please fill out the message filed'})

        
        new_message = Message(id=str(uuid.uuid4()), sender='user', user_id=current_user.id, user_name=current_user.username, chat_id=chat_id, content=message)
        db.session.add(new_message)
        db.session.commit()

        res = ai_response(chat_id, message)

        new_message2 = Message(id=str(uuid.uuid4()), sender='ai', user_id=current_user.id, user_name=current_user.username, chat_id=chat_id, content=res)
        db.session.add(new_message2)
        db.session.commit()
        res_data = {'ai_res': res}

        http_res = make_response(res_data, 200)

        return http_res
    

@chat_bl.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'GET':
        return render_template('chat/dashboard.html', chats=Chat.query.all())
    elif request.method == 'POST':
        data = request.get_json()
        new_chat_name = data.get('name')
        new_chat_id = uuid.uuid4()

        new_chat = Chat(id=str(new_chat_id), name = new_chat_name, user_id = current_user.id, user_name = current_user.username)
        db.session.add(new_chat)
        db.session.commit()

        return redirect(f'/chat/{str(new_chat_id)}')




