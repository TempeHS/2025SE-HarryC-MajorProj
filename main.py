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
import testimonials as test
import admin 

# Code snippet for logging a message
# app.logger.critical("message")

app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="security_log.log",
    encoding="utf-8",
    level=logging.DEBUG, 
    format="%(asctime)s %(message)s",
)

# Generate a unique basic 16 key: https://acte.ltd/utils/randomkeygen
app = Flask(__name__)
app.secret_key = b"_53oi3uriq9pifpff;apl"
auth_key = "4L50v92nOgcDCYUM"
csrf = CSRFProtect(app)

app_header = {"Authorization": "4L50v92nOgcDCYUM"}

# Redirect index.html to domain root for consistent UX
@app.route("/index", methods=["GET"])
@app.route("/index.htm", methods=["GET"])
@app.route("/index.asp", methods=["GET"])
@app.route("/index.php", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)


@app.route("/", methods=["POST", "GET"])
@csp_header(
    {
        # Server Side CSP is consistent with meta CSP in layout.html
    }
)
def index():
    return render_template("/index.html")

@app.route("/admin_login.html", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if dbHandler.checkAdmin(username, password):
            admin_email = dbHandler.getAdminEmail(username)
            otp_code = twofa.generate_otp()
            session["username"] = username
            session["admin_email"] = admin_email
            print(f"OTP code: {otp_code}")
            print(f"Admin email: {admin_email}")
            session["otp_code"] = otp_code
            twofa.send_otp_via_email(admin_email, otp_code)
            return render_template("2fa.html", session=username)
        else:
            app.logger.critical("Failed login attempt")
            return render_template("admin_login.html", error=True)
    return render_template("admin_login.html")



@app.route("/admin.html", methods=["GET"])
def admin_page():
    return render_template("/admin.html")

# Methods for getting and changing testimonials
def get_testimonials():
    url = "http://127.0.1:3000/get_testimonials"
    data = []
    try:
        response = requests.get(url, headers=app_header)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        app.logger.critical(f"Failed to fetch testimonials: {e}")
        data = {"error": "Failed to fetch testimonials"}
    return data

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

@app.route("/admin_testimonials.html", methods=["GET", "POST"])
def add_testiominals():
    if request.method == "POST":
        delete_id = request.form.get("id")
        if delete_id:
            delete = delete_testimonial(delete_id)
            data = get_testimonials()
            return render_template("admin_testimonials.html", data=data, delete=delete)
        else:
            form_data = test.sanitize_testimonial(request.form)
            success = add_testimonial(form_data)
            data = get_testimonials()
            return render_template("admin_testimonials.html", data=data, success=success)
    data = get_testimonials() # Explain why here you have to call the api again and again
    return render_template("admin_testimonials.html", data=data)

@app.route("/2fa.html", methods=["POST"])
def twofa_page():
    if request.method == "POST":
        # Generate OTP and send it via email
        user_input = request.form["otp_code"]
        otp_code = session.get("otp_code")
        if twofa.verify_otp(user_input, otp_code):
            app.logger.critical("Successful 2FA attempt")
            return redirect("/admin.html")
        else:
            app.logger.critical("Failed 2FA attempt")
            return render_template("2fa.html", error=True)
    return render_template("2fa.html")

@app.route("/booking.html", methods=["GET"])
def booking():
    data = get_testimonials()
    return render_template("/booking.html", data=data)


def get_aboutme():
    url = "http://127.0.0.1:3000/get_aboutme"
    data = []
    try:
        response = requests.get(url, headers=app_header)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        app.logger.critical(f"Failed to fetch testimonials: {e}")
        data = {"error": "Failed to get about me data"}
    return data

def update_aboutme(data):
    url = "http://127.0.0.1:3000/update_aboutme"
    try:
        response = requests.post(url,json=data, headers=app_header)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        app.logger.critical(f"Failed to change about me: {e}")
        return False

@app.route("/admin_about.html", methods=["GET", "POST"])
def admin_about():
    if request.method == "POST":
        form_data = admin.sanatize_aboutme(request)
        print(form_data)
        success = update_aboutme(form_data)
        data = get_aboutme()
        return render_template("/admin_about.html", success=success, data=data)
    data = get_aboutme()
    return render_template("/admin_about.html", data=data)

@app.route("/admin_change_password.html", methods=["GET", "POST"])
def admin_change_password():
    admin_email = session.get("admin_email")
    username = session.get("username")
    if request.method == "GET":
        otp_code = twofa.generate_otp()
        print(f"Change OTP Code: {otp_code}")
        print(f"Change Admin email: {admin_email}")
        session["otp_code"] = otp_code
        twofa.send_otp_via_email(admin_email, otp_code)
        return render_template("/admin_change_password.html")
    if request.method == "POST":
        input_code = request.form["input_code"]
        otp_code = session.get("otp_code")
        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        if twofa.verify_otp(input_code, otp_code) and dbHandler.checkAdmin(username, current_password):
            print("Passed verification check")
            dbHandler.changePassword(username, new_password)
            return render_template("/admin_change_password.html", success=True)
        else:
            return render_template("/admin_change_password.html", error="Invalid 2FA code or current password")

@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html")

@app.route("/about.html", methods=["GET"])
def about():
    data = {}
    data = get_aboutme()
    return render_template("/about.html", data=data)

@app.route("/blog.html", methods=["GET"])
def blog():
    return render_template("/blog.html")

# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
