#!/usr/bin/python3
"""[summary]
"""
from flask import request
from flask import abort
from flask.json import jsonify
from models import storage
from models.engine.file_storage import classes
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def reviewObjects(place_id='', review_id=''):
    """[summary]
    """
    if request.method == 'GET':
        if place_id is not '':
            place = storage.get(classes['Place'], place_id)
            if place:
                return jsonify([place.to_dict() for place in place.reviews])
            abort(404)
        elif review_id is not '':
            review = storage.get(classes['Review'], review_id)
            if review:
                return review.to_dict()
            abort(404)
    elif request.method == 'DELETE':
        review = storage.get(classes['Review'], review_id)
        if review:
            storage.delete(review)
            storage.save()
            return {}
        abort(404)
    elif request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            if 'text' not in data.keys():
                abort(400, description='Missing text')
            elif 'user_id' not in data.keys():
                abort(400, description='Missing user_id')
            if storage.get(classes['Place'], place_id) and\
               storage.get(classes['User'], data['user_id']):
                newReview = classes['Review'](place_id=place_id, **data)
                newReview.save()
                return newReview.to_dict(), 201
            abort(404)
        abort(400, description='Not a JSON')
    elif request.method == 'PUT':
        review = storage.get(classes['Review'], review_id)
        if review:
            if request.is_json:
                data = request.get_json()
                for key, value in data.items():
                    if key in ['id', 'created_at', 'updated_at', 'user_id',
                               'place_id']:
                        continue
                    setattr(review, key, value)
                review.save()
                return review.to_dict(), 200
            abort(400, description='Not a JSON')
        abort(404)
