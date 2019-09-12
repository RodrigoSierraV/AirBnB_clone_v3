#!/usr/bin/python3
""" handle all default RESTful API"""
from models.amenity import Amenity
from os import getenv
from flask import Flask, abort, jsonify, request, make_response
from models import storage
from api.v1.views import app_views

objs = storage.all('Amenity')


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenitiess():
    """get all states
    """
    new_list = []
    for key, val in objs.items():
        new_list.append(val.to_dict())
    return jsonify(new_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(amenity_id):
    """get a state
    """
    obj_state = 'Amenity.' + amenity_id
    if obj_state not in objs:
        abort(404)
    return jsonify(objs[obj_state].to_dict())


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_states(amenity_id):
    """delete a state
    """
    key_state = 'Amenity.' + amenity_id
    if key_state not in objs:
        abort(404)
    objs[key_state].delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_states():
    """post states
    """
    if request.is_json:
        req_data = request.get_json()
        if 'name' not in req_data:
            return(make_response(jsonify('Missing name'), 400))
        new_obj = Amenity(**request.get_json())
        new_obj.save()
        return(jsonify(new_obj.to_dict()), 201)
    else:
        return(make_response(jsonify('Not a JSON'), 400))


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_states(amenity_id):
    """put state
    """
    obj_state = 'Amenity.' + amenity_id
    if obj_state not in objs:
        abort(404)
    if request.is_json:
        req_data = request.get_json()
        obj_to_updt = storage.get('Amenity', amenity_id)
        for k1, v1 in req_data.items():
            if k1 != 'id' and k1 != 'updated_at' and k1 != 'created_at':
                setattr(obj_to_updt, k1, req_data[k1])

        obj_to_updt.save()
        return(jsonify(obj_to_updt.to_dict()), 201)
    else:
        return(make_response(jsonify('Not a JSON'), 400))
    return jsonify(objs[obj_state].to_dict())
