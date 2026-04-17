from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
socketio = SocketIO(app, cors_allowed_origns="*")

@app.route('/home')
@app.route('/')
def index():
    return render_template('levon_wiki.html')

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000) 
