#!/usr/bin/python3
"""return the status of the API"""

import Blueprint from Flask

app_views = Blueprint(url_prefix='/api/v1')

from api.v1.views.index import *
