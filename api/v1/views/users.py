#!/usr/bin/python3
"""[summary]
"""
from flask import request
from flask import abort
from flask.json import jsonify
from models import storage
from models.engine.file_storage import classes
from api.v1.views import app_views


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def usersObjects(user_id=''):
    """[summary]
    """
    if request.method == 'GET':
        if user_id is '':
            return jsonify(
                [user.to_dict() for user in
                 storage.all(classes['User']).values()])
        else:
            user = storage.get(classes['User'], user_id)
            if user:
                return user.to_dict()
            abort(404)
    elif request.method == 'DELETE':
        user = storage.get(classes['User'], user_id)
        if user:
            storage.delete(user)
            storage.save()
            return {}
        abort(404)
    elif request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            if 'email' not in data.keys():
                abort(400, description='Missing email')
            elif 'password' not in data.keys():
                abort(400, description='Missing password')
            newUser = classes['User'](**data)
            newUser.save()
            return newUser.to_dict(), 201
        abort(400, description='Not a JSON')
    elif request.method == 'PUT':
        user = storage.get(classes['User'], user_id)
        if user:
            if request.is_json:
                data = request.get_json()
                for key, value in data.items():
                    if key in ['id', 'created_at', 'updated_at', 'email']:
                        continue
                    setattr(user, key, value)
                user.save()
                return user.to_dict(), 200
            abort(400, description='Not a JSON')
        abort(404)
