#!/usr/bin/python3
"""[summary]
"""
from api.v1.views import app_views
from models import storage
from models.engine.file_storage import classes


@app_views.route('/status')
def status():
    """Return the status of the page
    """
    return {'status': 'OK'}


@app_views.route('/stats')
def countdown():
    """Return the count for each Class
    """
    return {
        'amenities': storage.count(classes['Amenity']),
        'cities': storage.count(classes['City']),
        'places': storage.count(classes['Place']),
        'reviews': storage.count(classes['Review']),
        'states': storage.count(classes['State']),
        'users': storage.count(classes['User'])
    }
