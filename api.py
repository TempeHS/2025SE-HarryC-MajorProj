from flask import Flask
from flask import request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import jsonify, request
import logging
import blog_admin as admin_b
import testimonial_admin as admin_t
import userManagement as dbHandler

auth_key = "4L50v92nOgcDCYUM"
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


@api.route("/add_testimonial", methods=["POST"])
@limiter.limit("1/second", override_defaults=False)
def add_testimonial():
    if request.headers.get("Authorization") == auth_key:
        data = request.get_json()
        print(f"Received data: {data}")
        logging.debug(f"Received data: {data}")
        response = admin_t.add_testimonial(data)
        return response, 201 if response else 400
    else:
        return {"error": "Unauthorized"}, 401
    

@api.route("/get_testimonials", methods=["GET"])
@limiter.limit("1/second", override_defaults=False)
def get_testimonials():
    if request.headers.get("Authorization") == auth_key:
        testimonials = admin_t.get_testiominals()
        return testimonials, 200
    else:
        return {"error": "Unauthorized"}, 401
    
@api.route("/get_aboutme", methods=["GET"])
@limiter.limit("1/second", override_defaults=False)
def get_aboutme():
    if request.headers.get("Authorization") == auth_key:
        data = admin_b.get_aboutme()
        return data, 200
    else:
        return {"error": "Unauthorized"}, 401
    

@api.route("/post_blog", methods=["POST"])
@limiter.limit("1/second", override_defaults=False)
def post_blog():
    if request.headers.get("Authorization") == auth_key:
        data = request.get_json()
        response = admin_b.post_blog(data)
        print(response)
        return response, 200
    else:
        return {"error": "Unauthorized"}, 401

@api.route("/get_blog", methods=["GET"])
@limiter.limit("1/second", override_defaults=False)
def get_blog():
    if request.headers.get("Authorization") == auth_key:
        blog = admin_b.get_blogs()
        return blog, 200
    else:
        return {"error": "Unauthorized"}, 401


@api.route("/update_aboutme", methods=["POST"])
@limiter.limit("1/second", override_defaults=False)
def change_aboutme():
    if request.headers.get("Authorization") == auth_key:
        data = request.get_json()
        response = admin_b.update_aboutme(data)
        print(response)
        return response, 200
    else:
        return {"error": "Unauthorized"}, 401

@api.route("/delete_testimonial/<int:testimonial_id>", methods=["POST"])
@limiter.limit("1/second", override_defaults=False)
def delete_testimonial(testimonial_id):
    if request.headers.get("Authorization") == auth_key:
        response = admin_t.delete_testimonial(testimonial_id)
        return response, 200
    else:
        return {"error": "Unauthorized"}, 401

@api.route("/delete_blog/<int:blog_id>", methods=["POST"])
@limiter.limit("1/second", override_defaults=False)
def delete_blog(blog_id):
    if request.headers.get("Authorization") == auth_key:
        response = admin_b.delete_blog(blog_id)
        return response, 200
    else:
        return {"error": "Unauthorized"}, 401

if __name__ == "__main__":
    api.run(debug=True, host="0.0.0.0", port=3000)