import os
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('webscanner.default_settings')

## Default definitions. Override with local values preferably using instance folder
app.config['COMMAND_SCAN'] = 'scanDo'
app.config['COMMAND_CLEAR'] = 'scanClear'
app.config['COMMAND_SAVE'] = 'scanSave'
app.config['DEFAULT_FILE_NAME'] = 'scan.pdf'

# Path to "final" PDF file with appended pages after each COMMAND_SCAN is run. Must match definition in COMMAND_SCAN script.
app.config['PDF_FILE_PATH'] = None

# Gmail account and credentials to use to send "final" PDF file. See https://github.com/kootenpv/yagmail for details.
app.config['GMAIL_ACCOUNT'] = None
app.config['GMAIL_ACCOUNT_CREDENTIALS'] = None
app.config['DEFAULT_RECIPIENT'] = None

# Obtain available options for your scanner with scanimage -L
SCAN_MODE_OPTIONS = []
SCAN_MODE_DEFAULT = None
SCAN_RES_OPTIONS = []
SCAN_RES_DEFAULT = None

# Override previous definitions from variables in settings.py in instance folder
app.config.from_pyfile('settings.py', silent=True)

import webscanner.views
