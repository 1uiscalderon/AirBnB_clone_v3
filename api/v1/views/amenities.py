#!/usr/bin/python3
"""View for Amenity object
"""
from flask import request
from flask import abort
from flask.json import jsonify
from models import storage
from models.engine.file_storage import classes
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenitiesObjects(amenity_id=''):
    """Retrieve, Update, Delete and Create this object
    """
    if request.method == 'GET':
        if amenity_id is '':
            return jsonify(
                [amenity.to_dict() for amenity in
                 storage.all(classes['Amenity']).values()])
        else:
            amenity = storage.get(classes['Amenity'], amenity_id)
            if amenity:
                return amenity.to_dict()
            abort(404)
    elif request.method == 'DELETE':
        amenity = storage.get(classes['Amenity'], amenity_id)
        if amenity:
            storage.delete(amenity)
            storage.save()
            return {}
        abort(404)
    elif request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            if 'name' in data.keys():
                newAmenity = classes['Amenity'](**data)
                newAmenity.save()
                return newAmenity.to_dict(), 201
            abort(400, description='Missing name')
        abort(400, description='Not a JSON')
    elif request.method == 'PUT':
        amenity = storage.get(classes['Amenity'], amenity_id)
        if amenity:
            if request.is_json:
                data = request.get_json()
                for key, value in data.items():
                    if key in ['id', 'created_at', 'updated_at']:
                        continue
                    setattr(amenity, key, value)
                amenity.save()
                return amenity.to_dict(), 200
            abort(400, description='Not a JSON')
        abort(404)
