from flask import Flask, request, make_response, render_template, session, jsonify, redirect
from flask_login import login_user, logout_user, current_user, login_required
import uuid

def config_routes(app, db, bcrypt):
    @app.route('/all_users')
    @login_required
    def api():

        if 'password' in session:

            current_user = User.query.get(session['password'])

            if current_user.job == 'Admin':
                all_users = User.query.all()

                return 'this is admin data'
            else:
                return jsonify({'message': 'restricted'}), 401
    
    @app.route('/')
    @login_required
    def home():
        return render_template('index.html', username = current_user.username)
        
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.get(username)

            print(user.password)

            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)

                return redirect('/')
            else:
                return jsonify({"message": "user not found"})


        return redirect('/')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'GET':
            return render_template('signup.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            job = request.form.get('job')
            email = request.form.get('email')
            id = uuid.uuid4()
            hashed_password = bcrypt.generate_password_hash(password)

            if username and password and email and id:

                user = User(username = username, password = hashed_password, email = email, id = str(id), job = job)

                db.session.add(user)
                db.session.commit()

                return redirect('/login')
            else:
                return jsonify({"message": 'all fileds are required'})
            
    @app.route('/logout', methods=['POST'])
    @login_required
    def logout():

        logout_user()

        return redirect('/login')
    
    @app.route('/profile', methods=['GET', 'UPDATE', 'DELETE'])
    @login_required
    def profile():
        user = current_user

        if request.method == 'GET':
            return render_template('profile.html', usr=user)
        elif request.method == 'UPDATE':
            change = request.get_json('change')

    @app.route('/chat', methods=['GET', 'POST'])
    @login_required
    def chat():
        return ''
    
    @app.route('/new_chat', methods=['POST'])
    @login_required
    def new_chat():
        return ''
    


        


    
