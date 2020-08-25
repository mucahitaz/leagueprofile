import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'b77ece784e27cf7b42137c32fbee5ba4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///summoner.db'


db = SQLAlchemy(app)

from app import routes