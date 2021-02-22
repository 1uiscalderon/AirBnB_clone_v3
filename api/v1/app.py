#!/usr/bin/python3
"""Script that fetches data from the storage engine and runs the app
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r'/api/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def sessionClose(err):
    """Closes the session
    """
    storage.close()


@app.errorhandler(404)
def pageNotFound(err):
    """[summary]
    """
    return {
        'error': 'Not found'
    }, 404


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default='5000')
    app.run(host=host, port=port, threaded=True)
