import bleach
import os
from flask import request
import sqlite3 as sql
from flask import jsonify

schema = {
    "type": "object",
    "ValidationLevel": "strict",
    "properties": {
        "customer_name": {
            "type": "string",
            "title": "Customer Name",
            "description": "Name of the customer giving the testimonial",
        },
        "customer_testimonial": {
            "type": "string",
            "title": "Customer Testimonial",
            "description": "The testimonial text provided by the customer",
        },
        "formFile": {
            "type": "string",
            "title": "Profile Picture",
            "description": "URL or path to the profile picture of the customer",
        },
        "id": {
            "type": "integer",
            "title": "ID",
            "description": "Unique identifier for the testimonial",
        },
    },
    "required": ["customer_name", "customer_testimonial", "formFile"],
    "additionalProperties": False,
}




UPLOAD_FOLDER = "static/images/profile_pictures"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS



def add_testimonial(data):
    if validate_json(data):
        con = sql.connect("databaseFiles/database.db")
        cur = con.cursor()
        cur.execute(
            "INSERT INTO testimonials (customer, customer_testimonial, profile_picture) VALUES (?, ?, ?)",
            (data["customer_name"], data["customer_testimonial"], data["formFile"]),
        )
        con.commit()
        con.close()
        return {"message": "Testimonial added successfully"}
    else:
        return {"error": "Invalid data format"}, 400


def update_testimonial(data):
    if validate_json(data):
        con = sql.connect("databaseFiles/database.db")
        cur = con.cursor()
        cur.execute(
            "UPDATE testimonials SET customer_testimonial = ?, profile_picture = ? WHERE customer = ? WHERE id = ?",
            (data["customer_testimonial"], data["formFile"], data["customer_name"], data["id"]),
        )
        con.commit()
        con.close()
        return {"message": "Testimonial updated successfully"}, 200
    else:
        return {"error": "Invalid data format"}, 400


def sanatize_aboutme(data):
    biography = request.form.get("biography")
    biography = bleach.clean(biography)
    credentials = request.form.get("credentials")
    credentials = bleach.clean(credentials)
    image_path = request.files.get("image_path")
    # Set a default image path if no new image is uploaded
    default_path = "static/images/profile_pictures/profile photo.jpg"
    if image_path and allowed_file(image_path.filename):
        filename = image_path.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        image_path.save(file_path)
        relative_path = os.path.join(UPLOAD_FOLDER, filename)
    else:
        # Use the existing image_path from the form if available, otherwise use default
        relative_path = request.form.get("image_path", default_path)
    data = {
        "biography": biography,
        "credentials": credentials,
        "image_path": relative_path
    }
    return data

def update_aboutme(data):
    try:
        con = sql.connect("databaseFiles/database.db")
        cur = con.cursor()
        cur.execute("UPDATE about_content SET biography = ?, credentials = ?, image_path = ? WHERE id = 1",
            (data["biography"], data["credentials"], data["image_path"]),
        )
        con.commit()
        con.close()
        return {"message": "About me successfully updated"}
    except Exception as e:
        return {"error": str(e)}


def delete_testimonial(testimonial_id):
    try:
        con = sql.connect("databaseFiles/database.db")
        cur = con.cursor()
        cur.execute("DELETE FROM testimonials WHERE id = ?", (testimonial_id,))
        con.commit()
        con.close()
        return {"message": "Testimonial deleted sucessfully"}
    except Exception as e:
        return {"error": str(e)}
    

def get_aboutme():
    con = sql.connect("databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM about_content")
    migrate_data = [
        dict(
            id=row[0],
            biography=row[1],
            credentials=row[2],
            image_path=row[3]
            
        )
        for row in cur.fetchall()
    ]
    return jsonify(migrate_data)

def validate_json(json_data):
    try:
        validate(instance=json_data, schema=schema)
        return True
    except:
        return False
    