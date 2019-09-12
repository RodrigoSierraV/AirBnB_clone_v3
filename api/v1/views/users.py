#!/usr/bin/python3
""" handle all default RESTful API"""
from models.user import User
from os import getenv
from flask import abort, jsonify, request, make_response
from models import storage
from api.v1.views import app_views

objs = storage.all('User')


@app_views.route('/users',
                 methods=['GET'], strict_slashes=False)
def get_users():
    """get all users
    """
    new_list = []
    new_list.append(objs.to_dict())
    if len(new_list) == 0:
        abort(404)
    return jsonify(new_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """get a user
    """
    user_obj = 'User.' + city_id
    if user_obj not in objs:
        abort(404)
    return jsonify(objs[user_obj].to_dict())


@app_views.route(
    '/users/<user_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_user(user_id):
    """delete a user
    """
    user_obj = 'City.' + city_id
    if key_city not in objs:
        abort(404)
    objs[user_obj].delete()
    storage.save()
    storage.close()
    return (jsonify({}), 200)


@app_views.route('/users',
                 methods=['POST'], strict_slashes=False)
def post_user():
    """create user
    """
    if request.is_json:
        req_data = request.get_json()
        if 'name' not in req_data:
            abort(400, 'Missing name')
        elif 'email' not in req_data:
            abort(400, 'Missing email')
        elif 'password' not in req_data:
            abort(400, 'Missing password')
        else:
            new_obj = City(**req_data)
            new_obj.save()
            return(jsonify(new_obj.to_dict()), 201)
        abort(404)
    else:
        abort(400, 'Not a JSON')


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """update user
    """
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    if request.is_json:
        req_data = request.get_json()
        obj_to_up = storage.get('User', user_id)
        if obj_to_up is not None:
            for k1, v1 in req_data.items():
                if k1 not in ignore_keys:
                    setattr(obj_to_up, k1, req_data[k1])
            obj_to_up.save()
            return(jsonify(obj_to_up.to_dict()), 200)
    else:
        return(abort(400, 'Not a JSON'))
