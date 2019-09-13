#!/usr/bin/python3
"""create api
"""
from flask import Flask
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from flask import jsonify
import os
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
CORS(app, resources={"/*": {'origins': "0.0.0.0"}})


@app.teardown_appcontext
def close_context(self):
    """calls close method
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    return (jsonify(error='Not found'), 404)


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')),
            threaded=True)
