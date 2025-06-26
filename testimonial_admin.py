import bleach
import os
from flask import request
import sqlite3 as sql
from flask import jsonify
import schemas as schema


UPLOAD_FOLDER = "static/images/profile_pictures"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def add_testimonial(data):
    try:
        if schema.validate_json(data, schema.testimonials):
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
    except Exception as e:
        return {"error": str(e)}

def update_testimonial(data):
    try: 
        if schema.validate_json(data, schema.testimonials):
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
        relative_path = "static/images/customer_profile_photos/Profile icon.png"  # Handle case where no valid file is provided
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