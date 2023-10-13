from flask import *
from flask import Flask, request, jsonify, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'And blood black nothingness began to spin. A series of cells interlinked within cells interlinked within cells interlinked within one stem'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/perpus_calvin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
 
from models import *
from routes import *
