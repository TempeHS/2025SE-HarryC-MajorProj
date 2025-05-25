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
csrf = CSRFProtect(app)


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
def admin():
    return render_template("/admin.html")

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
    return render_template("/booking.html")

@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html")

@app.route("/about.html", methods=["GET"])
def about():
    return render_template("/about.html")

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
