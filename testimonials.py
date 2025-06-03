import bleach
import os
from flask import request
import sqlite3 as sql
from flask import jsonify

UPLOAD_FOLDER = "static/images/customer_profile_photos"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Add santiziation for the testimonial image
def sanitize_testimonial(request_form):
    customer_name = request_form.get("customer_name")
    customer_name = bleach.clean(customer_name)
    customer_testimonial = request_form.get("customer_testimonial")
    customer_testimonial = bleach.clean(customer_testimonial)
    formFile = request.files.get("formFile")
    if formFile and allowed_file(formFile.filename):
        filename = formFile.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        formFile.save(file_path)
        relative_path = os.path.join(UPLOAD_FOLDER, filename)
    else:
        relative_path = None  # Handle case where no valid file is provided
    data = {
        "customer_name": customer_name,
        "customer_testimonial": customer_testimonial,
        "formFile": relative_path
    }
    return data

def get_testiominals():
    con = sql.connect("databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM testimonials")
    migrate_data = [
        dict(
            id=row[0],
            customer_name=row[1],
            customer_testimonial=row[2],
            formFile=row[3]
        )
        for row in cur.fetchall()
    ]
    return jsonify(migrate_data)