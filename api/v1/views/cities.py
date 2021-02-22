#!/usr/bin/python3
"""View for City object
"""
from flask import request
from flask import abort
from flask.json import jsonify
from models import storage
from models.engine.file_storage import classes
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def citiesObjects(state_id='', city_id=''):
    """Retrieve, Update, Delete and Create this object
    """
    if request.method == 'GET':
        if state_id is not '':
            state = storage.get(classes['State'], state_id)
            if state:
                return jsonify([city.to_dict() for city in state.cities])
            abort(404)
        elif city_id is not '':
            city = storage.get(classes['City'], city_id)
            if city:
                return city.to_dict()
            abort(404)
    elif request.method == 'DELETE':
        city = storage.get(classes['City'], city_id)
        if city:
            storage.delete(city)
            storage.save()
            return {}
        abort(404)
    elif request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            if 'name' in data.keys():
                if storage.get(classes['State'], state_id):
                    newCity = classes['City'](state_id=state_id, **data)
                    newCity.save()
                    return newCity.to_dict(), 201
                abort(404)
            abort(400, description='Missing name')
        abort(400, description='Not a JSON')
    elif request.method == 'PUT':
        city = storage.get(classes['City'], city_id)
        if city:
            if request.is_json:
                data = request.get_json()
                for key, value in data.items():
                    if key in ['id', 'created_at', 'updated_at', 'state_id']:
                        continue
                    setattr(city, key, value)
                city.save()
                return city.to_dict(), 200
            abort(400, description='Not a JSON')
        abort(404)
