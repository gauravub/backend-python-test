from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy

# configuration
DATABASE = '/tmp/alayatodo.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)


@app.before_request
def before_request():
    g.db = db


@app.teardown_request
def teardown_request(exception):
    setattr(g, 'db', None)



import alayatodo.views
import alayatodo.models