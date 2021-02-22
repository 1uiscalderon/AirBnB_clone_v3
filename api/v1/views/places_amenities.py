#!/usr/bin/python3
"""[summary]
"""
from flask import request
from flask import abort
from flask.json import jsonify
from models import storage
from models import storage_t
from models.engine.file_storage import classes
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE', 'POST'])
def placeAmenityView(place_id='', amenity_id=''):
    """[summary]
    """
    if storage_t == 'db':
        if request.method == 'GET':
            place = storage.get(classes['Place'], place_id)
            if place:
                return jsonify(
                    [amenity.to_dict() for amenity in place.amenities])
            abort(404)
        elif request.method == 'DELETE':
            place = storage.get(classes['Place'], place_id)
            if place:
                amenity = storage.get(classes['Amenity'], amenity_id)
                if amenity and amenity in place.amenities:
                    place.amenities.remove(amenity)
                    place.save()
                    return {}
                abort(404)
            abort(404)
        elif request.method == 'POST':
            place = storage.get(classes['Place'], place_id)
            if place:
                amenity = storage.get(classes['Amenity'], amenity_id)
                if amenity:
                    try:
                        index = place.amenities.index(amenity)
                        return place.amenities[index].to_dict()
                    except Exception:
                        place.amenities.append(amenity)
                        place.save()
                        return amenity.to_dict(), 201
                abort(404)
            abort(404)
    else:
        if request.method == 'GET':
            place = storage.get(classes['Place'], place_id)
            if place:
                return jsonify(
                    [amenityID for amenityID in place.amenity_ids])
            abort(404)
        elif request.method == 'DELETE':
            place = storage.get(classes['Place'], place_id)
            if place:
                if storage.get(classes['Amenity'], amenity_id) and\
                   amenity_id in place.amenity_ids:
                    place.amenity_ids.remove(amenity_id)
                    storage.save()
                    return {}
                abort(404)
            abort(404)
        elif request.method == 'POST':
            place = storage.get(classes['Place'], place_id)
            if place:
                amenity = storage.get(classes['Amenity'], amenity_id)
                if amenity:
                    try:
                        index = place.amenity_ids.index(amenity_id)
                        return amenity_id
                    except Exception:
                        place.amenities = amenity
                        storage.save()
                        return amenity_id, 201
                abort(404)
            abort(404)
