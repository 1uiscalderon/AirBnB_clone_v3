#!/usr/bin/python3
"""[summary]
"""
from flask import request
from flask import abort
from flask.json import jsonify
from models import storage
from models.engine.file_storage import classes
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def placesObjects(city_id='', place_id=''):
    """[summary]
    """
    if request.method == 'GET':
        if city_id is not '':
            city = storage.get(classes['City'], city_id)
            if city:
                return jsonify([place.to_dict() for place in city.places])
            abort(404)
        elif place_id is not '':
            place = storage.get(classes['Place'], place_id)
            if place:
                return place.to_dict()
            abort(404)
    elif request.method == 'DELETE':
        place = storage.get(classes['Place'], place_id)
        if place:
            storage.delete(place)
            storage.save()
            return {}
        abort(404)
    elif request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            if 'name' not in data.keys():
                abort(400, description='Missing name')
            elif 'user_id' not in data.keys():
                abort(400, description='Missing user_id')
            elif storage.get(classes['City'], city_id) is None:
                abort(404)
            elif storage.get(classes['User'], data['user_id']) is None:
                abort(404)
            newPlace = classes['Place'](city_id=city_id, **data)
            newPlace.save()
            return newPlace.to_dict(), 201
        abort(400, description='Not a JSON')
    elif request.method == 'PUT':
        place = storage.get(classes['Place'], place_id)
        if place:
            if request.is_json:
                data = request.get_json()
                for key, value in data.items():
                    if key in ['id', 'created_at', 'updated_at', 'user_id',
                               'city_id']:
                        continue
                    setattr(place, key, value)
                place.save()
                return place.to_dict(), 200
            abort(400, description='Not a JSON')
        abort(404)
