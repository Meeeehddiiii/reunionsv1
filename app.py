# app.py

from flask import Flask, render_template
from config import Config
from models import db
from routes import init_app

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
init_app(app)

@app.route('/')
def index():
    return render_template('index.html')  # Assurez-vous d'avoir un template 'index.html'

if __name__ == '__main__':
    app.run(debug=True)