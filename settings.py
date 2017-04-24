# -*- coding: utf-8 -*-

import os

APP_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE = 'sqlite:///{}'.format(os.path.join(APP_DIR, 'app.db'))
DEBUG = True
SECRET_KEY = 'development'
WTF_CSRF_ENABLED = True
