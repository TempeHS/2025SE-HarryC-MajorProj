from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify
from flask import session
import requests
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging
import userManagement as dbHandler
import twofa
from flask import send_file
from datetime import timedelta
from main import app

app_header = {"Authorization": "4L50v92nOgcDCYUM"}

def update_aboutme(data):
    url = "http://127.0.0.1:3000/update_aboutme"
    try:
        response = requests.post(url,json=data, headers=app_header)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        app.logger.critical(f"Failed to change about me: {e}")
        return False

def post_blog(data):
    url = "http://127.0.0.1:3000/post_blog"
    try:
        response = requests.post(url,json=data, headers=app_header)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        app.logger.critical(f"Failed to change about me: {e}")
        return False

def add_testimonial(data):
    post_url = "http://127.0.1:3000/add_testimonial"
    try:
        response = requests.post(post_url, json=data, headers=app_header)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        app.logger.critical(f"Failed to add testimonial: {e}")
        return False

def delete_testimonial(testimonial_id):
    delete_url = f"http://127.0.1:3000/delete_testimonial/{testimonial_id}"
    try:
        response = requests.post(delete_url, headers=app_header)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        app.logger.critical(f"Failed to delete testimonial: {e}")
        return False

def delete_blog(blog_id):
    delete_url = f"http://127.0.1:3000/delete_blog/{blog_id}"
    try:
        response = requests.post(delete_url, headers=app_header)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        app.logger.critical(f"Failed to delete blog: {e}")
        return False

def get_api_data(endpoint):
    url = f"http://127.0.0.1:3000/{endpoint}"
    data = []
    try:
        response = requests.get(url, headers=app_header)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        app.logger.critical(f"Failed to fetch {endpoint}: {e}")
        data = {"error": f"Failed to get data from {endpoint}"}
    return data