import eventlet
eventlet.monkey_patch()

import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = 'my_very_secret_key'
load_dotenv()

admin_password = os.getenv('ADMIN_PASSWORD')
users = {
    'admin': {
        'password': generate_password_hash(admin_password)
    }
}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'lkaeapetyan@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'lkaeapetyan@gmail.com'
app.config['MAIL_PASSWORD'] = 'pntc fshh ebyx hyvm'

socketio = SocketIO(app, cors_allowed_origins="*")
mail = Mail(app)
sent_emails = {}

class User(UserMixin):
   def __init__(self, id):
       self.id = id


@login_manager.user_loader
def load_user(user_id):
    if user_id not in users:
        return None
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_data = users.get(username)
        if user_data and check_password_hash(user_data['password'], password):
            user = User(username)
            login_user(user)
            login_user(user, remember=False)
            return redirect(url_for('admin'))
        else: 
            flash('Incorrect login or password')
    return render_template('login.html')


@app.route('/home')
@app.route('/')
def index():
    return render_template('levon_wiki.html')



@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@socketio.on('user_msg')
def handle_user_message(data):
    user_name = data.get('user_name', 'Guest')
    user_email = data.get('user_email', 'No email')
    message = data.get('message', '')
    sid = request.sid
    print(f"Message from {user_name}: {message}")
    emit('admin_receive', {
        'user_name': user_name,
        'message': message
    }, broadcast=True)

    if sid not in sent_emails:
        try:
           msg = Message(
               subject=f"New message in chat from: {user_name}",
               recipients=[app.config['MAIL_USERNAME']],
               body=f"User {user_name} ({user_email}) write you in chat.\n\n"
               f"Open admin panel",
       	       reply_to=user_email
       	   )
           mail.send(msg)
           sent_emails[sid] = True
        except Exception as e:
             print(f"Error: {e}")

@socketio.on('admin_reply')
def handle_admin_reply(data):
    emit('user_receive', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000) 
