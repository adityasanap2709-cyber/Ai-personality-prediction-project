from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_file,
    flash,
    session
)

import os

from dotenv import load_dotenv

from werkzeug.utils import secure_filename

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from reportlab.pdfgen import canvas

import easyocr

from authlib.integrations.flask_client import OAuth

from database import init_db

from models import (
    db,
    User,
    Prediction
)

from training.predict import (
    predict_personality
)

# ==========================================
# APPLICATION SETUP
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY"
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "static",
    "uploads"
)

app.config[
    "UPLOAD_FOLDER"
] = UPLOAD_FOLDER

if not os.path.exists(
    UPLOAD_FOLDER
):
    os.makedirs(
        UPLOAD_FOLDER
    )

init_db(app)

reader = easyocr.Reader(
    ["en"]
)

oauth = OAuth(app)
# ==========================================
# GOOGLE OAUTH
# ==========================================

google = oauth.register(

    name="google",

    client_id=os.getenv("GOOGLE_CLIENT_ID"),

    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),

    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",

    client_kwargs={
        "scope": "openid email profile"
    }

)
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    latest = Prediction.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Prediction.created_at.desc()
    ).first()

    return render_template(
        "dashboard.html",
        result=latest
    )


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully!")

    return redirect(url_for("home"))



# ==========================================
# HOME
# ==========================================

# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():
    return render_template("home.html")

# ================= ABOUT =================

@app.route("/about")
def about():
    return render_template("about.html")


# ================= ANALYZE =================

# ==========================================
# ANALYZE
# ==========================================

@app.route("/analyze", methods=["GET", "POST"])
def analyze():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        # Logged-in User
        user_id = session["user_id"]

        analysis_type = request.form.get("analysis_type")

        # ================= Username Analysis =================

        if analysis_type == "username":

            username = request.form.get("username", "").strip()

            # Future X API Integration
            text_to_analyze = username

        # ================= Manual Posts =================

        else:

            username = "Manual Posts"

            posts = request.form.get("posts", "")

            image = request.files.get("post_image")

            text_to_analyze = posts

            # OCR

            if image and image.filename != "":

                filename = secure_filename(image.filename)

                image_path = os.path.join(

                    app.config["UPLOAD_FOLDER"],

                    filename

                )

                image.save(image_path)

                result = reader.readtext(image_path)

                ocr_text = ""

                for item in result:

                    ocr_text += item[1] + " "

                print("OCR TEXT :")

                print(ocr_text)

                text_to_analyze = ocr_text

        # ================= AI Prediction =================

        text_to_analyze = text_to_analyze.strip()

        if text_to_analyze == "":

            flash("Please enter text or upload an image.")

            return redirect(url_for("analyze"))

        prediction = predict_personality(text_to_analyze)

        new_prediction = Prediction(

            user_id=user_id,

            username=username,

            openness=prediction["Openness"],

            conscientiousness=prediction["Conscientiousness"],

            extraversion=prediction["Extraversion"],

            agreeableness=prediction["Agreeableness"],

            neuroticism=prediction["Neuroticism"]

        )

        db.session.add(new_prediction)

        db.session.commit()

        session["analysis_done"] = True

        flash("Analysis Completed Successfully!")

        return redirect(url_for("dashboard"))

    return render_template("analyze.html")

# ==========================================
# HISTORY
# ==========================================

@app.route("/history")
def history():

    if "user_id" not in session:

        return redirect(url_for("login"))

    history_data = Prediction.query.filter_by(

        user_id=session["user_id"]

    ).order_by(

        Prediction.created_at.desc()

    ).all()

    return render_template(

        "history.html",

        history=history_data

    )
# ==========================================
# REGISTER
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        print("REGISTER ROUTE CALLED")

        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        print("Name :", name)
        print("Email:", email)

        # Password check
        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for("register"))

        # Email already exists?
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            print("Email already exists")
            flash("Email already registered!")
            return redirect(url_for("register"))

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create user
        new_user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        # Save to PostgreSQL
        try:

            db.session.add(new_user)
            db.session.commit()

            print("✅ USER SAVED SUCCESSFULLY")

            flash("Registration Successful!")

            return redirect(url_for("login"))

        except Exception as e:

            db.session.rollback()

            print("❌ REGISTER ERROR:", e)

            flash("Registration Failed!")

            return str(e)

    return render_template("register.html")
# ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"]

        print("\n========== LOGIN ==========")
        print("Email :", email)

        user = User.query.filter_by(email=email).first()

        if user:

            print("User Found :", user.name)
            print("Stored Hash :", user.password)

            if check_password_hash(user.password, password):

                print("✅ Password Matched")

                session["user_id"] = user.id
                session["user_name"] = user.name
                session["analysis_done"] = False

                flash("Login Successful!", "success")

                return redirect(url_for("analyze"))

            else:

                print("❌ Wrong Password")

                flash("Invalid Email or Password", "danger")

                return redirect(url_for("login"))

        else:

            print("❌ User Not Found")

            flash("Email not registered!", "danger")

            return redirect(url_for("register"))

    return render_template("login.html")
# ==========================================
# PROFILE
# ==========================================
# ==========================================
# PROFILE
# ==========================================

@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    latest = Prediction.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Prediction.created_at.desc()
    ).first()

    return render_template(
        "profile.html",
        user=user,
        latest=latest
    )
    
# ==========================================
# EDIT PROFILE
# ==========================================

@app.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():

    if "user_id" not in session:

        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    if request.method == "POST":

        user.name = request.form["name"]

        image = request.files.get("photo")

        if image and image.filename != "":

            filename = secure_filename(image.filename)

            image.save(

                os.path.join(

                    app.config["UPLOAD_FOLDER"],

                    filename

                )

            )

            user.profile_photo = filename

        db.session.commit()

        flash("Profile Updated Successfully!")

        return redirect(url_for("profile"))

    return render_template(

        "edit_profile.html",

        user=user

    )
# ==========================================
# DOWNLOAD REPORT
# ==========================================

@app.route("/download_report")
def download_report():

    if "user_id" not in session:

        return redirect(url_for("login"))

    result = Prediction.query.filter_by(

        user_id=session["user_id"]

    ).order_by(

        Prediction.created_at.desc()

    ).first()

    if not result:

        flash("No Report Found!")

        return redirect(url_for("dashboard"))

    pdf_name = "Personality_Report.pdf"

    c = canvas.Canvas(pdf_name)

    c.setFont("Helvetica-Bold",18)
    c.drawString(160,800,"OCEAN Personality Report")

    c.setFont("Helvetica",12)

    c.drawString(50,750,f"Username : {result.username}")

    c.drawString(50,720,f"Openness : {result.openness}")

    c.drawString(50,690,f"Conscientiousness : {result.conscientiousness}")

    c.drawString(50,660,f"Extraversion : {result.extraversion}")

    c.drawString(50,630,f"Agreeableness : {result.agreeableness}")

    c.drawString(50,600,f"Neuroticism : {result.neuroticism}")

    c.save()

    return send_file(

        pdf_name,

        as_attachment=True

    )
# ==========================================
# GOOGLE LOGIN
# ==========================================

@app.route("/google")
def google_login():

    redirect_uri = url_for(

        "authorize",

        _external=True

    )

    return google.authorize_redirect(

        redirect_uri

    )
# ==========================================
# GOOGLE CALLBACK
# ==========================================

@app.route("/authorize")
def authorize():

    token = google.authorize_access_token()

    user_info = token["userinfo"]

    email = user_info["email"]

    name = user_info["name"]

    user = User.query.filter_by(

        email=email

    ).first()

    if not user:

        user = User(

            name=name,

            email=email,

            password="google_login"

        )

        db.session.add(user)

        db.session.commit()

    session["user_id"] = user.id

    session["user_name"] = user.name

    flash("Google Login Successful!")

    return redirect(

        url_for("dashboard")

    )
    
 # ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)