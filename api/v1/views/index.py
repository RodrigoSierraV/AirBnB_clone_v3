#!/usr/bin/python3
"""return the status of your API"""

from api.v1.views import app_views

@app_views.route('/status', strict_slashes=False)
def apistat():
    """Returns JSON with status of the API"""
    return jsonify({'status': 'OK'})
