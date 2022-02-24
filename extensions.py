from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vendingmachine.db'
app.config['SECRET_KEY'] = "itissecretkey"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
