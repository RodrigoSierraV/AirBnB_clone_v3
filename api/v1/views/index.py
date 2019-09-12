#!/usr/bin/python3
"""return the status of your API"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models import State
from models import Amenity
from models import Place
from models import City
from models import Review
from models import User

Classes = [State, Amenity, Place, City, Review, User]
@app_views.route('/status', strict_slashes=False)
def apistat():
    """Returns JSON with status of the API"""
    return jsonify(status='OK')

@app_views.route('/api/v1/stats', strict_slashes=False)
def count():
    """retrieves the number of each objects by type"""

    dic = {}
    for i in classes:
        dic[i.__name__] = storage.count(i.__name__)
    return dic
