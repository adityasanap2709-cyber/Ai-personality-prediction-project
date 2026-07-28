from flask import Flask, render_template, request, redirect, url_for, send_file, flash, session
import sqlite3
from reportlab.pdfgen import canvas
import os
from flask import flash
from werkzeug.utils import secure_filename
import os
import easyocr
from PIL import Image
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv()
DB_PATH = os.path.join(BASE_DIR, "database.db")
app = Flask(__name__)
reader = easyocr.Reader(['en'])
app.secret_key = os.getenv("SECRET_KEY")
UPLOAD_FOLDER = "static/uploads"
oauth = OAuth(app)

google = oauth.register(

    name="google",

    client_id=os.getenv("GOOGLE_CLIENT_ID"),

    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),

    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",

    client_kwargs={

        "scope":"openid email profile"

    }

)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ================= HOME =================

@app.route("/")
def home():
    return render_template("home.html")


# ================= ABOUT =================

@app.route("/about")
def about():
    return render_template("about.html")


# ================= ANALYZE =================

@app.route("/analyze", methods=["GET", "POST"])
def analyze():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        # Logged-in User ID
        user_id = session["user_id"]

        analysis_type = request.form.get("analysis_type")

        # ================= Username Analysis =================

        if analysis_type == "username":

            username = request.form.get("username")

            # (Future X API integration)

        # ================= Posts Analysis =================

        else:

            username = "Manual Posts"

            posts = request.form.get("posts", "")

            image = request.files.get("post_image")

            # Default text = Typed Posts
            ocr_text = posts

            # If Image Uploaded
            if image and image.filename != "":

                filename = secure_filename(image.filename)

                image_path = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )

                image.save(image_path)

                print("Image Uploaded :", filename)

                # OCR
                result = reader.readtext(image_path)

                ocr_text = ""

                for item in result:
                    ocr_text += item[1] + " "

                print("OCR TEXT:")
                print(ocr_text)

        # ================= Dummy AI Result =================

        personality = "INTJ"
        confidence = 95
        introvert = 90
        thinking = 85
        judging = 88
        intuition = 82

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO predictions
        (
            user_id,
            username,
            personality_type,
            confidence,
            introvert,
            thinking,
            judging,
            intuition
        )
        VALUES (?,?,?,?,?,?,?,?)
        """, (
            user_id,
            username,
            personality,
            confidence,
            introvert,
            thinking,
            judging,
            intuition
        ))

        conn.commit()
        conn.close()

        session["analysis_done"] = True

        return redirect(url_for("dashboard"))

    return render_template("analyze.html")
# ================= DASHBOARD =================

@app.route("/dashboard")
def dashboard():

    # User Login Check
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Latest Result of Logged-in User
    cursor.execute("""
    SELECT username,
           personality_type,
           confidence,
           introvert,
           thinking,
           judging,
           intuition
    FROM predictions
    WHERE user_id = ?
    ORDER BY id DESC
    LIMIT 1
    """, (session["user_id"],))

    result = cursor.fetchone()

    # Total Analysis of Logged-in User
    cursor.execute("""
    SELECT COUNT(*)
    FROM predictions
    WHERE user_id = ?
    """, (session["user_id"],))

    total_analysis = cursor.fetchone()[0]

    # Average Confidence of Logged-in User
    cursor.execute("""
    SELECT ROUND(AVG(confidence),2)
    FROM predictions
    WHERE user_id = ?
    """, (session["user_id"],))

    average_confidence = cursor.fetchone()[0]

    if average_confidence is None:
        average_confidence = 0

    # Most Common Personality of Logged-in User
    cursor.execute("""
    SELECT personality_type
    FROM predictions
    WHERE user_id = ?
    GROUP BY personality_type
    ORDER BY COUNT(*) DESC
    LIMIT 1
    """, (session["user_id"],))

    data = cursor.fetchone()

    if data:
        most_common = data[0]
    else:
        most_common = "--"

    conn.close()

    return render_template(
        "dashboard.html",
        result=result,
        total_analysis=total_analysis,
        average_confidence=average_confidence,
        most_common=most_common
    )




# ================= HISTORY =================

@app.route("/history")
def history():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
      SELECT username,
        personality_type,
        confidence
      FROM predictions
      WHERE user_id = ?
      ORDER BY id DESC
    """, (session["user_id"],))

    history_data = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        history=history_data
    )
#register
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return "Passwords do not match!"

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()

        if user:
            conn.close()
            return "Email already registered!"

        cursor.execute(
            """
            INSERT INTO users
            (name, email, password)
            VALUES (?, ?, ?)
            """,
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/google")

def google_login():

    redirect_uri = url_for(

        "authorize_google",

        _external=True

    )

    return google.authorize_redirect(

        redirect_uri

    )
@app.route("/login/google/authorized")
def authorize_google():

    token = google.authorize_access_token()

    user = token["userinfo"]

    email = user["email"]

    name = user["name"]

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(

        "SELECT id FROM users WHERE email=?",

        (email,)

    )

    existing = cursor.fetchone()

    if existing:

        user_id = existing[0]

    else:

        cursor.execute(

            """

            INSERT INTO users

            (name,email,password)

            VALUES(?,?,?)

            """,

            (

                name,

                email,

                "GOOGLE_LOGIN"

            )

        )

        conn.commit()

        user_id = cursor.lastrowid

    conn.close()

    session["user_id"] = user_id

    session["analysis_done"] = False

    return redirect(

        url_for("analyze")

    )
#login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id, name
        FROM users
        WHERE email=? AND password=?
        """, (email, password))

        user = cursor.fetchone()

        conn.close()

        if user:

            session["user_id"] = user[0]
            session["analysis_done"] = False

            return redirect(url_for("analyze"))

        return "Invalid Email or Password"

    return render_template("login.html")
# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))   
# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)

