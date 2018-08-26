import os
import glob
import json
from flask import render_template, send_file, request
import yagmail
import traceback
from subprocess import call,Popen

from webscanner import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan')
def scanDo():
    # Use "Popen" if you want a non-blocking process; "call" for blocking
    try:
	    Popen(['scanDo'])
	    return 'Scan command was sent'
    except:
	    return 'Scan command failed'

@app.route('/clear')
def scanClear():
    # Use "Popen" if you want a non-blocking process; "call" for blocking
    try:
	    Popen(['scanClear'])
	    return 'Clear PDFs command was sent'
    except:
	    return 'Clear PDFs failed'

@app.route('/save')
def scanSave():
    # Use "Popen" if you want a non-blocking process; "call" for blocking
    try:
	    Popen(['scanSave'])
	    return 'Merged PDF copy command was sent'
    except:
	    return 'Merged PDF copy failed'

@app.route('/email')
def scanEmail():
	'''
	This function relies on yagmail library sending e-mail through a Gmail account using OAuth authentication. 
	See https://github.com/kootenpv/yagmail for details on how to setup the credentials. Define Gmail account and
	path to credentials file in <instance folder>/settings.py
	You can remove permissions to the account in: https://myaccount.google.com/permissions
	'''	
	if app.config.get('GMAIL_ACCOUNT') is None or app.config.get('GMAIL_ACCOUNT_CREDENTIALS') is None:
		return 'Gmail account not configured'
	
	recipient = request.args.get('email')		
	if recipient is None:
		return 'No e-mail recipient was defined'

	try:
		yag = yagmail.SMTP(app.config['GMAIL_ACCOUNT'], oauth2_file=app.config['GMAIL_ACCOUNT_CREDENTIALS'])
		yag.send(to=recipient, 
				 subject='Scanned document', 
				 contents='Find scanned document attached. \n\nSent by WebScanner.', 
				 attachments=[app.config.get('PDF_FILE_PATH')])   
		return 'E-mail was sent'
	except:
		return 'Failed to send e-mail'

@app.route('/download')
def scanDownload():
	# Define PDF_FILE_PATH in <instance folder>/settings.py
	if app.config.get('PDF_FILE_PATH') is not None and os.path.exists(app.config.get('PDF_FILE_PATH')):
	    return send_file(app.config['PDF_FILE_PATH'],
	                     attachment_filename="scan.pdf",
	                     mimetype='application/pdf',
	                     as_attachment=True)
	else:
	    return "There was an error downloading requested PDF file. File not found."	

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
