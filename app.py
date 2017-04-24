# -*- coding: utf-8 -*-

import settings
from flask import Flask
from playhouse.flask_utils import FlaskDB
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect


app = Flask(__name__)
app.config.from_object(settings)


flask_db = FlaskDB(app)
database = flask_db.database

lm = LoginManager()
lm.init_app(app)

csrf = CsrfProtect()
csrf.init_app(app)
