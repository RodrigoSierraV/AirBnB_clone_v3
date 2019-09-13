#!/usr/bin/python3
""" handle all default RESTful API"""
from models.state import State
from os import getenv
from flask import abort, jsonify, request, make_response
from models import storage
from api.v1.views import app_views

objs = storage.all('State')


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """get all states
    """
    new_list = []
    for key, val in objs.items():
        new_list.append(val.to_dict())
    return jsonify(new_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """get a state
    """
    obj_state = 'State.' + state_id
    if obj_state not in objs:
        abort(404)
    return jsonify(objs[obj_state].to_dict())


@app_views.route(
    '/states/<state_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_states(state_id):
    """delete a state
    """
    key_state = 'State.' + state_id
    if key_state not in objs:
        abort(404)
    storage.delete(objs[key_state])
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    """post states
    """
    if request.is_json:
        req_data = request.get_json()
        if 'name' not in req_data:
            return(make_response(jsonify('Missing name'), 400))
        new_obj = State(**request.get_json())
        new_obj.save()
        return(jsonify(new_obj.to_dict()), 201)
    else:
        return(make_response(jsonify('Not a JSON'), 400))


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_states(state_id):
    """put state
    """
    ignore_keys = ['id', 'created_at', 'updated_at']
    obj_state = 'State.' + state_id
    if obj_state not in objs:
        abort(404)
    if request.is_json:
        print("isjason")
        req_data = request.get_json()
        obj_to_updt = storage.get('State', state_id)
        if obj_to_updt is not None:
            for k1, v1 in req_data.items():
                if k1 not in ignore_keys:
                    setattr(obj_to_updt, k1, req_data[k1])
        obj_to_updt.save()
        return(jsonify(obj_to_updt.to_dict()), 200)
        else:
            abort(404)
    else:
        return(abort(400, 'Not a JSON'))
