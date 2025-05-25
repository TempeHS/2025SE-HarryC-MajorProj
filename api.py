from flask import Flask
from flask import request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

import userManagement as dbHandler


api = Flask(__name__)
cors = CORS(api)
api.config["CORS_HEADERS"] = "Content-Type"
limiter = Limiter(
    get_remote_address,
    app=api,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)


@api.route("/", methods=["GET"])
@limiter.limit("3/second", override_defaults=False)
def get():
    return ("API Works"), 200


@api.route("/add_extension", methods=["POST"])
@limiter.limit("1/second", override_defaults=False)
def post():
    data = request.get_json()
    return data, 201

@api.route("/get_instagram", methods=["GET"])
@limiter.limit("1/second", override_defaults=False)
def get_instagram():
    data = request.get_json()
    if not data:
        return ("No data provided"), 400
    try:
        result = dbHandler.getInstagram(data)
        return result, 200
    except Exception as e:
        logging.error(f"Error: {e}")
        return ("Internal Server Error"), 500

if __name__ == "__main__":
    api.run(debug=True, host="0.0.0.0", port=3000)