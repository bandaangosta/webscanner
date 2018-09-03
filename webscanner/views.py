import os
from flask import render_template, send_file, request
import yagmail
import traceback
import tempfile
import shutil
from subprocess import Popen, TimeoutExpired, PIPE
from webscanner import app

@app.route('/')
def index():
    return render_template('index.html', 
                           scanResolutionOptions = app.config.get('SCAN_RES_OPTIONS'), 
                           scanResolutionDefault = app.config.get('SCAN_RES_DEFAULT'),
                           scanModeOptions = app.config.get('SCAN_MODE_OPTIONS'),
                           scanModeDefault = app.config.get('SCAN_MODE_DEFAULT')
                          )

@app.route('/scan')
def scanDo():
    ''' Run scan command (bash script) and return console output for display to user '''

    resolution = request.args.get('resolution')       
    if resolution is None:
        return 'No scan resolution was defined'

    mode = request.args.get('mode')     
    if mode is None:
        return 'No scan mode was defined'
    
    if int(resolution) not in app.config.get('SCAN_RES_OPTIONS'):
        return 'Resolution is not a valid option'

    if mode not in app.config.get('SCAN_MODE_OPTIONS'):
        return 'Mode is not a valid option'

    try:
        args = ['scanDo', resolution, mode]
        proc = Popen(args, stdout=PIPE, stderr=PIPE)
        try:
            outs, errs = proc.communicate(timeout=30)
        except TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()     
            return 'Scan command timeout.\nOutput:\n{}'.format(outs.decode('utf-8')) + \
                   ('\nErrors:\n{}'.format(errs.decode('utf-8')) if errs else '')
        return 'Scan command finished. \nOutput:\n{}'.format(outs.decode('utf-8')) + \
               ('\nErrors:\n{}'.format(errs.decode('utf-8')) if errs else '')
    except FileNotFoundError:
        return 'Scan command failed: {} not found'.format(args[0]) 
    except:
        return 'Scan command failed'

@app.route('/clear')
def scanClear():
    ''' Run clear PDFs command (bash script) and return console output for display to user '''
    
    try:
        args = ['scanClear']
        proc = Popen(args, stdout=PIPE, stderr=PIPE)
        try:
            outs, errs = proc.communicate(timeout=30)
        except TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()     
            return 'Clear PDFs command timeout.\nOutput:\n{}'.format(outs.decode('utf-8')) + \
                   ('\nErrors:\n{}'.format(errs.decode('utf-8')) if errs else '')
        return 'Clear PDFs command finished.\nOutput:\n{}'.format(outs.decode('utf-8')) + \
               ('\nErrors:\n{}'.format(errs.decode('utf-8')) if errs else '')
    except FileNotFoundError:
        return 'Clear PDFs command failed: {} not found'.format(args[0]) 
    except:
        return 'Clear PDFs command failed'

@app.route('/save')
def scanSave():
    ''' Run save PDF command (bash script) and return console output for display to user '''
    
    try:
        args = ['scanSave']
        proc = Popen(args, stdout=PIPE, stderr=PIPE)
        try:
            outs, errs = proc.communicate(timeout=30)
        except TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()     
            return 'Merged PDF copy command timeout.\nOutput:\n{}\nErrors:\n{}'.format(outs.decode('utf-8'), errs.decode('utf-8'))
        return 'Merged PDF copy command finished. \nOutput:\n{}\nErrors:\n{}'.format(outs.decode('utf-8'), errs.decode('utf-8'))
    except FileNotFoundError:
        return 'Merged PDF copy command failed: {} not found'.format(args[0]) 
    except:
        return 'Merged PDF copy command failed'

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

    fileName = request.args.get('filename')     
    if fileName is None:
        return 'No file name was defined'
    
    if not os.path.exists(app.config.get('PDF_FILE_PATH')):
        return 'Scanned file was not found'
    
    # Create a copy of the scanned file with given name
    tmpdir = tempfile.gettempdir()
    shutil.copyfile(app.config.get('PDF_FILE_PATH'), os.path.join(tmpdir, fileName))

    try:
        yag = yagmail.SMTP(app.config['GMAIL_ACCOUNT'], oauth2_file=app.config['GMAIL_ACCOUNT_CREDENTIALS'])
        yag.send(to=recipient, 
                 subject='Scanned document', 
                 contents='Find scanned document attached. \n\nSent by WebScanner.', 
                 attachments=[os.path.join(tmpdir, fileName)])   
        return 'E-mail was sent'
    except:
        return 'Failed to send e-mail'

@app.route('/download')
def scanDownload():
    fileName = request.args.get('filename')     
    if fileName is None:
        return 'No file name was defined'

    # Define PDF_FILE_PATH in <instance folder>/settings.py
    if app.config.get('PDF_FILE_PATH') is not None and os.path.exists(app.config.get('PDF_FILE_PATH')):
        return send_file(app.config['PDF_FILE_PATH'],
                         attachment_filename=fileName,
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
