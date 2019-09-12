#!/usr/bin/python3
""" handle all default RESTful API"""
from models.review import Review
from os import getenv
from flask import Flask, abort, jsonify, request
from models import storage
from api.v1.views import app_views

objs = storage.all('Review')


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review(place_id):
    """get review of one place
    """
    new_list = []
    for key, val in objs.items():
        if val.place_id == place_id:
            new_list.append(val.to_dict())
    if len(new_list) == 0:
        abort(404)
    return jsonify(new_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_reviews(review_id):
    """get an specify review
    """
    obj_place = 'Review.' + amenity_id
    if obj_state not in objs:
        abort(404)
    return jsonify(objs[obj_place].to_dict())


@app_views.route(
    '/reviews/<review_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_review(review_id):
    """delete a review
    """
    key_place = 'Review.' + place_id
    if key_place not in objs:
        abort(404)
    objs[key_place].delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """create a review of a place
    """
    if request.is_json:
        req_data = request.get_json()
        if 'user_id' not in req_data:
            abort(400, 'Missing user_id')
        elif 'text' not in req_data:
            abort(400, 'Missing text')

        for key, val in objs.items():
            if val.user_id == req_data[user_id]:
                req_data['place_id'] = val.place_id
                new_obj = Review(**req_data)
                new_obj.save()
                return(jsonify(new_obj.to_dict()), 201)
        abort(404)
    else:
        abort(400, 'Not a JSON')


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_places(review_id):
    """update review
    """
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    obj_place = 'Review.' + place_id
    if obj_place not in objs:
        abort(404)
    if request.is_json:
        req_data = request.get_json()
        obj_to_up = storage.get('Review', review_id)
        for k1 in req_data:
            if k1 not in ignore:
                setattr(obj_to_up, k1, req_data[k1])
        obj_to_up.save()
        return(jsonify(obj_to_up.to_dict()), 200)
    else:
        abort(400, 'Not a JSON')
