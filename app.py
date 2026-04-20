from flask import Flask, render_template

app = Flask(__name__)

@app.route('/home')
@app.route('/')
def index():
    return render_template('levon_wiki.html')




if __name__ == '__main__':
     app.run('0.0.0.0', debug=True)
     
