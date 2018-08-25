import os
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
# app.config.from_object('webscanner.default_settings')
# app.config.from_envvar('WEBSCANNER_SETTINGS', silent=True)
# app.config.from_envvar('settings.cfg', silent=True)
app.config.from_pyfile('settings.py', silent=True)

import webscanner.views
