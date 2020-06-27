from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager(app)

db = SQLAlchemy(app)
Base = declarative_base()
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
bootstrap = Bootstrap(app)

from app.models import auth
from app.forms import forms
from app.controllers import default
from app import urls

