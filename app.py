import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'lkaeapetyan@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'lkaeapetyan@gmail.com'
app.config['MAIL_PASSWORD'] = 'pntc fshh ebyx hyvm'

socketio = SocketIO(app, cors_allowed_origns="*")
mail = Mail(app)


@app.route('/home')
@app.route('/')
def index():
    return render_template('levon_wiki.html')


@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    try:
        user_name = data.get('user_name', 'Guest')
        user_email = data.get('user_email')
        message = data.get('message')

        msg = Message(
            subject = f"New Chat Message from {user_name}",
            recipients = [app.config['MAIL_USERNAME']],
            body = f"Name: {user_name}\nEmail: {user_email}\n\nMessage: {message}",
            reply_to = user_email
        )
        mail.send(msg)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000) 
