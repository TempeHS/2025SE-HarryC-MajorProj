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


def sanatize_aboutme(data):
    biography = request.form.get("biography")
    biography = bleach.clean(biography)
    credentials = request.form.get("credentials")
    credentials = bleach.clean(credentials)
    image_path = request.files.get("image_path")
    default_path = "static/images/profile_pictures/Mum Full photo.png"
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

def sanatize_blog(data):
    allowed_tags = ['p', 'br', 'h1', 'h2', 'h3', 'ul', 'ol', 'li', 'b', 'strong', 'i', 'em']
    title = request.form.get("title")
    title = bleach.clean(title)
    blog_content = request.form.get("blog_content")
    blog_content = bleach.clean(blog_content, tags=allowed_tags)
    data = {
        "title": title,
        "blog_content": blog_content
    }
    return data

def update_aboutme(data):
    try:
        if schema.validate_json(data, schema.about):
            con = sql.connect("databaseFiles/database.db")
            cur = con.cursor()
            cur.execute("UPDATE about_content SET biography = ?, credentials = ?, image_path = ? WHERE id = 1",
                (data["biography"], data["credentials"], data["image_path"]),
            )
            con.commit()
            con.close()
            return {"message": "About me successfully updated"}
        else:
            return {"error": "Invalid data format"}
    except Exception as e:
        return {"error": str(e)}
    
def post_blog(data):
    try:
        if schema.validate_json(data, schema.blog):
            con = sql.connect("databaseFiles/database.db")
            cur = con.cursor()
            cur.execute(
                "INSERT INTO blog (title, blog_content) VALUES (?, ?)",
                (data["title"], data["blog_content"]),
            )
            con.commit()
            con.close()
            return {"message": "Blog added successfully"}
        else:
            return {"error": "Invalid data format"}
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

def delete_blog(blog_id):
    try:
        con = sql.connect("databaseFiles/database.db")
        cur = con.cursor()
        cur.execute("DELETE FROM blog WHERE id = ?", (blog_id,))
        con.commit()
        con.close()
        return {"message": "Blog deleted sucessfully"}
    except Exception as e:
        return {"error": str(e)}

def get_blogs():
    con = sql.connect("databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("""SELECT
            blog.id, 
            blog.title, 
            blog.blog_content, 
            blog.created_at, 
            about_content.image_path
        FROM blog
        JOIN about_content ON about_content.id = (
            SELECT id FROM about_content LIMIT 1
        )
    """)
    migrate_data = [
        dict(
            id=row[0],
            title=row[1],
            blog_content=row[2],
            created_at=row[3],
            image_path=row[4]
        )
        for row in cur.fetchall()
    ]
    con.close()
    return jsonify(migrate_data)


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