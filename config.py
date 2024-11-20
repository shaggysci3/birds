from flask import Flask
from flask_mail import Mail, Message
import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import MetaData
# from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Email settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  # Email address
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')  # Email password or app password
app.config['MAIL_DEFAULT_SENDER'] = ('Your App Name', 'matthewsandor01@gmail.com')

app.json.compact = False
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


migrate = Migrate(app, db)
db.init_app(app)
bcrypt = Bcrypt(app)
mail = Mail(app)