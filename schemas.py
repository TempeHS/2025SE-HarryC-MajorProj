from jsonschema import validate

about = {
    "type": "object",
    "ValidationLevel": "strict",
    "properties": {
        "id": {
            "type": "integer",
            "title": "ID",
            "description": "Unique identifier for the about content",
        },
        "biography": {
            "type": "string",
            "title": "Biography",
            "description": "Admin biography text",
        },
        "credentials": {
            "type": "string",
            "title": "Credentials",
            "description": "Admin credentials or qualifications",
        },
        "image_path": {
            "type": "string",
            "title": "Profile Image Path",
            "description": "URL or path to the admin profile image",
        },
    },
    "required": ["biography", "credentials", "image_path"],
    "additionalProperties": False,
}

blog = {
    "type": "object",
    "ValidationLevel": "strict",
    "properties": {
        "id": {
            "type": "integer",
            "title": "ID",
            "description": "Unique identifier for the blog post",
        },
        "title": {
            "type": "string",
            "title": "Title",
            "description": "Title of the blog post",
        },
        "blog_content": {
            "type": "string",
            "title": "Blog Content",
            "description": "Content of the blog post",
        },
        "created_at": {
            "type": "string",
            "format": "date-time",
            "title": "Created At",
            "description": "Timestamp when the blog post was created",
        },
    },
    "required": ["title", "blog_content"],
    "additionalProperties": False,
}

testimonials = {
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

def validate_json(json_data, schema):
    try:
        validate(instance=json_data, schema=schema)
        return True
    except Exception:
        return False