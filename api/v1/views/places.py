#!/usr/bin/python3
""" handle all default RESTful API"""
from models.place import Place
from os import getenv
from flask import Flask, abort, jsonify, request, make_response
from models import storage
from api.v1.views import app_views

objs = storage.all('Place')


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_cityplace(city_id):
    """get places from cities
    """
    new_list = []
    if not storage.get('City', city_id):
        abort(404)
    for i in objs.values():
        if i.city_id == city_id:
            new_list.append(i.to_dict)
    return jsonify(new_list)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_places(place_id):
    """get a state
    """
    obj_place = 'Place.' + amenity_id
    if obj_state not in objs:
        abort(404)
    return jsonify(objs[obj_place].to_dict())


@app_views.route(
    '/places/<place_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_places(place_id):
    """delete a place
    """
    key_place = 'Place.' + place_id
    if key_place not in objs:
        abort(404)
    objs[key_place].delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/cities/<city_id/places>',
                 methods=['POST'], strict_slashes=False)
def post_places(city_id):
    """ POST a Place
    """
    cty = storage.get('City', city_id)
    if not cty:
        abort(404)
    if request.is_json:
        req_data = request.get_json()
        if user_id not in req_data:
            return(make_response(jsonify('Missing user_id'), 400))
        usr = storage.get('User', req_data['user_id'])
        if not usr:
            abort(404)
        if 'name' not in req_data:
            return(make_response(jsonify('Missing name'), 400))
        req_data['city_id'] = city_id
        new_obj = Place(**req_data)
        new_obj.save()
        return(jsonify(new_obj.to_dict()), 201)
    else:
        return(make_response(jsonify('Not a JSON'), 400))


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_places(place_id):
    """put place
    """
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    obj_place = 'Place.' + place_id
    if obj_place not in objs:
        abort(404)
    if request.is_json:
        req_data = request.get_json()
        obj_to_updt = storage.get('Place', place_id)
        for k1 in req_data:
            if k1 not in ignore:
                setattr(obj_to_updt, k1, req_data[k1])
        obj_to_updt.save()
        return(jsonify(obj_to_updt.to_dict()), 201)
    else:
        return(make_response(jsonify('Not a JSON'), 400))
    return jsonify(objs[obj_state].to_dict())
