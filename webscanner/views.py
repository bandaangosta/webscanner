import os
import glob
import json
from flask import render_template, request, url_for, flash, redirect
import traceback
from subprocess import call,Popen

from webscanner import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan')
def scanDo():
    # Change call for Popen if you want a non-blocking process
    try:
	    Popen(['scanDo'])
	    return 'Scan command was sent'
    except:
	    return 'Scan command failed'

@app.route('/clear')
def scanClear():
    # Change call for Popen if you want a non-blocking process
    try:
	    Popen(['scanClear'])
	    return 'Clear PDFs command was sent'
    except:
	    return 'Clear PDFs failed'

@app.route('/save')
def scanSave():
    # Change call for Popen if you want a non-blocking process
    try:
	    Popen(['scanSave'])
	    return 'Merged PDF copy command was sent'
    except:
	    return 'Merged PDF copy failed'

@app.route('/email')
def scanEmail():
    return 'NOT IMPLEMENTED'

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page_not_found.html'), 404

@app.errorhandler(500)
def pageNotFound(error):
    return render_template('internal_server_error.html'), 500

# prevent cached responses
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
