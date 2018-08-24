import os
import glob
import json
from flask import render_template, request, url_for, flash, redirect
import traceback

from webscanner import app

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/subscribe/<plotId>')
# def newSubscription(plotId):
#     subscriberEmail = request.args.get('subscriberEmail')
#     # plotId = request.args.get('plot_id')
#     if not subscriberEmail:
#         flash('Please enter a valid e-mail to subscribe', 'error')
#     else:
#         try:
#             Db.insertSubscriber(subscriberEmail, plotId)
#             flash('{} was successfully subscribed to automatically receive fault detection reports for case {}'.format(subscriberEmail, plotId), 'success')
#         except sqlite3.IntegrityError:
#             flash('{} is already subscribed to fault {}'.format(subscriberEmail, plotId), 'error')
#         except:
#             flash('Failed to subscribe {}'.format(subscriberEmail), 'error')
#             print(traceback.format_exc())
#     return redirect(url_for('multiplotPanel', plotId=plotId))

@app.route('/scan')
def scanDo():
    return 'Scan command was sent'

# @app.route('/fdd')
# def fddDetails():
#     plotId = request.args.get('plot_id')
#     detectionType = request.args.get('detection_type')
#     antenna = request.args.get('antenna')
#     pol = None
#     if '_' in antenna:
#         pol = antenna.split('_')[1]
#         antenna = antenna.split('_')[0]
#         if 'P' in pol:
#             pol = pol[-1]

#     useTwoPols = Db.getIfTwoPolarizations(plotId, detectionType)
#     pathToFDDPlotClusterDist = 'plots/{}/fdd/{}/plot_distribution.png'.format(plotId, detectionType)
#     pathToFDDPlotClusterDistClusters = 'plots/{}/fdd/{}/plot_distribution_clusters.png'.format(plotId, detectionType)

#     pathToFDDPlotClusterAnt = []
#     pathToFDDPlotLinear = []

#     if useTwoPols:
#         if pol is not None:
#             pathToFDDPlotClusterAnt.append('plots/{}/fdd/{}/plot_distribution_{}_{}.png'.format(plotId, detectionType, antenna, pol))
#             pathToFDDPlotLinear.append('plots/{}/fdd/{}/plot_{}_{}.png'.format(plotId, detectionType, antenna, pol))
#         else:
#             for pol in [0, 1]:
#                 pathToFDDPlotClusterAnt.append('plots/{}/fdd/{}/plot_distribution_{}_{}.png'.format(plotId, detectionType, antenna, pol))
#                 pathToFDDPlotLinear.append('plots/{}/fdd/{}/plot_{}_{}.png'.format(plotId, detectionType, antenna, pol))
#     else:
#         pathToFDDPlotClusterAnt.append('plots/{}/fdd/{}/plot_distribution_{}.png'.format(plotId, detectionType, antenna))
#         pathToFDDPlotLinear.append('plots/{}/fdd/{}/plot_{}.png'.format(plotId, detectionType, antenna))

#     fddResults = Db.getResults(plotId, detectionType, antenna)
#     arrComments = []
#     for case in fddResults:
#         if case['polarization'] is not None and case['comments']:
#             arrComments.append('P{}: {}'.format(case['polarization'], case['comments'].replace('\n', '<br>')))
#         else:
#             if case['comments']:
#                 arrComments.append('{}'.format(case['comments'].replace('\n', '<br>')))

#     if detectionType in ['linear_regression', 'double_exponential', 'kalman_filters']:
#         # return '<br>'.join(['<img src="{}">'.format(url_for('static', filename=x)) for x in pathToFDDPlotLinear])
#         return render_template('fdd_details.html', images=pathToFDDPlotLinear, comments=arrComments)
#     elif detectionType == 'clustering_by_stats':
#         return render_template('fdd_details.html', images=pathToFDDPlotClusterAnt + [pathToFDDPlotClusterDistClusters], comments=arrComments)
#         # return '<img src="{}">'.format(url_for('static', filename=pathToFDDPlotClusterDist)) + \
#         #        '<br><img src="{}">'.format(url_for('static', filename=pathToFDDPlotClusterDistClusters)) + \
#         #        '<br>'.join(['<img src="{}">'.format(url_for('static', filename=x)) for x in pathToFDDPlotClusterAnt])

# @app.route('/plotter/<plotId>')
# def multiplotPanel(plotId):
#     data = Db.getMultiplotDataFromIdPlot(plotId)
#     availableDetectionTypes = Db.getAvailableDetectionType(plotId)

#     # faultCase = request.args.get('fault_case') #'ifp_7v_power'
#     detectionType = request.args.get('detection_type') #'linear_regression'
#     faultResult = request.args.get('detection_result')

#     if detectionType is None or detectionType == '-1' or faultResult is None or faultResult == '-1':
#         showFiltered = False
#     else:
#         showFiltered = True
#         filterList = []
#         fddResults = Db.getResults(plotId, detectionType)
#         for case in fddResults:
#             if case['detection_summary'] == faultResult:
#                 # if case['polarization'] is not None:
#                 if plotId == 'ifp_currents':
#                     filterList.append('{}_P{}'.format(case['antenna'], case['polarization']))
#                 else:
#                     filterList.append('{}'.format(case['antenna']))

#         # Remove repeated elements
#         filterList = set(filterList)

#     pathToPlots = '/plots/{}'.format(plotId)

#     # Translation dictionaries for cleaner human presentation
#     dictFaultResults = {
#                         '-1'             : 'No filter',
#                         'fault_detected' : 'Fault candidates',
#                         'no_fault'       : 'No fault',
#                         'inconclusive'   : 'Inconclusive'
#                        }

#     dictDetectionTypes = {
#                         '-1'                  : ' ',
#                         'kalman_filters'      : 'Kalman filters',
#                         'linear_regression'   : 'Linear regression',
#                         'clustering_by_stats' : 'Clustering by statistical descriptors',
#                         'double_exponential'  : 'Double exponential forecast'
#                        }

#     if os.path.exists(pathToPlots) and data is not None:
#         filteredFileList = []
#         if len(os.listdir(pathToPlots)) > 0:
#             files = [x for x in glob.glob(os.path.join(pathToPlots, '*.png'))]

#             if showFiltered:
#                 for fileName in files:
#                     for filterAnt in filterList:
#                         if filterAnt in fileName:
#                             filteredFileList.append(fileName)
#                 files = [(os.path.splitext(os.path.basename(x))[0], x[1:]) for x in filteredFileList]
#             else:
#                 files = [(os.path.splitext(os.path.basename(x))[0], x[1:]) for x in files]

#             return render_template('multiplot.html', files=sorted(files), plotId=plotId, metadata=data,
#                                    availableDetectionTypes=availableDetectionTypes, detectionType=detectionType,
#                                    faultResult=faultResult, dictFaultResults=dictFaultResults, dictDetectionTypes=dictDetectionTypes)
#         else:
#             return render_template('multiplot.html', files=[], metadata=data, dictFaultResults={}, dictDetectionTypes={})
#     return render_template('multiplot.html', files=[], metadata=data, dictFaultResults={}, dictDetectionTypes={})

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
