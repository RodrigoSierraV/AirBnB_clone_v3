#!/usr/bin/python3
""" handle all default RESTful API"""
from models.city import City
from os import getenv
from flask import abort, jsonify, request, make_response
from models import storage
from api.v1.views import app_views

objs = storage.all('City')


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """get all cities of a state
    """
    new_list = []
    for key, val in objs.items():
        if val.state_id == state_id:
            new_list.append(val.to_dict())
    if len(new_list) == 0:
        abort(404)
    return jsonify(new_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """get a city
    """
    city_obj = 'City.' + city_id
    if city_obj not in objs:
        abort(404)
    return jsonify(objs[city_obj].to_dict())


@app_views.route(
    '/cities/<city_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_city(city_id):
    """delete a city
    """
    key_city = 'City.' + city_id
    if key_city not in objs:
        abort(404)
    objs[key_city].delete()
    storage.save()
    storage.close()
    return (jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """create city
    """
    if request.is_json:
        req_data = request.get_json()
        if 'name' not in req_data:
            abort(400, 'Missing name')

        for key, val in objs.items():
            if val.state_id == state_id:
                req_data['state_id'] = val.state_id
                new_obj = City(**req_data)
                new_obj.save()
                return(jsonify(new_obj.to_dict()), 201)
        abort(404)
    else:
        abort(400, 'Not a JSON')


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """update city
    """
    if request.is_json:
        req_data = request.get_json()
        obj_to_up = storage.get('City', city_id)
        if obj_to_up is not None:
            for k1, v1 in req_data.items():
                if k1 != 'id' and k1 != 'updated_at' and k1 != 'created_at':
                    setattr(obj_to_up, k1, req_data[k1])
            obj_to_up.save()
            return(jsonify(obj_to_up.to_dict()), 200)
    else:
        return(abort(400, 'Not a JSON'))
