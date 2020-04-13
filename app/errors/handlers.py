from flask import Blueprint, render_template

bp_errors = Blueprint('errors', __name__)

# reference:  https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/

@bp_errors.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', title='page not found'), 404


