#!/usr/bin/python3
"""return the status of your API"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.city import City
from models.review import Review
from models.user import User


classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status', strict_slashes=False)
def apistat():
    """Returns JSON with status of the API"""
    return jsonify(status='OK')


@app_views.route('/stats', strict_slashes=False)
def count():
    """retrieves the number of each objects by type"""

    dic = {}
    for key, value in classes.items():
        dic[key] = storage.count(value.__name__)
    return jsonify(dic)
