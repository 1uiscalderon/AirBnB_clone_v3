#!/usr/bin/python3
"""
"""
from flask import request
from flask import abort
from flask.json import jsonify
from models import storage
from models.engine.file_storage import classes
from api.v1.views import app_views


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def statesObjects(state_id=''):
    """[summary]
    """
    if request.method == 'GET':
        if state_id is '':
            return jsonify(
                [object_.to_dict() for object_ in
                 storage.all(classes['State']).values()])
        else:
            object_ = storage.get(classes['State'], state_id)
            if object_:
                return object_.to_dict()
            abort(404)
    elif request.method == 'DELETE':
        object_ = storage.get(classes['State'], state_id)
        if object_:
            storage.delete(object_)
            storage.save()
            return {}
        abort(404)
    elif request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            if 'name' in data.keys():
                newState = classes['State'](**data)
                newState.save()
                return newState.to_dict(), 201
            abort(400, description='Missing name')
        abort(400, description='Not a JSON')
    elif request.method == 'PUT':
        object_ = storage.get(classes['State'], state_id)
        if object_:
            if request.is_json:
                data = request.get_json()
                for key, value in data.items():
                    if key in ['id', 'created_at', 'updated_at']:
                        continue
                    setattr(object_, key, value)
                object_.save()
                return object_.to_dict(), 200
            abort(400, description='Not a JSON')
        abort(404)
