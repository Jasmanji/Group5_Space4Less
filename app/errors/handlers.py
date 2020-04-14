# Contributed to by: Aure, Ariel

from flask import Blueprint, render_template

bp_errors = Blueprint('errors', __name__)

# reference: Error handler structure view and controller structure adapted from https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/ on 13/04/2020

# For bad request errors
@bp_errors.app_errorhandler(400)
def bad_request(error):
    return render_template('errors/400.html', title='Bad request'), 400

# For unauthorised errors
@bp_errors.app_errorhandler(401)
def unauthorized_to_access(error):
    return render_template('errors/401.html', title='Unauthorized to access'), 401

# For forbidden errors
@bp_errors.app_errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html', title='Forbidden'), 403

# For URI not found errors
@bp_errors.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', title='Page not found'), 404

# For prohibited method errors
@bp_errors.app_errorhandler(405)
def method_not_allowed(error):
    return render_template('errors/405.html', title='Method not allowed'), 405

# For conflict errors
@bp_errors.app_errorhandler(409)
def conflict(error):
    return render_template('errors/409.html', title='Conflict'), 409

# For removed page errors
@bp_errors.app_errorhandler(410)
def page_gone(error):
    return render_template('errors/410.html', title='Page gone'), 410

# For internal server errors
@bp_errors.app_errorhandler(500)
def server_side_error(error):
    return render_template('errors/500.html', title='Server side error'), 500
