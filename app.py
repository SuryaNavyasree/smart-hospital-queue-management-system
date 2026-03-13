from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from crowd_detection import detect_people
from nlp_predictor import predict_urgency

app = Flask(__name__)

# -----------------------------
# Create Database
# -----------------------------
def init_db():

    conn = sqlite3.connect("hospital.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        problem TEXT,
        urgency TEXT,
        queue TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def index():

    conn = sqlite3.connect("hospital.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM patients ORDER BY id DESC")
    patients = cur.fetchall()

    conn.close()

    # AI crowd detection
    people = detect_people()

    return render_template(
        "index.html",
        patients=patients,
        people=people
    )


# -----------------------------
# Add Patient
# -----------------------------
@app.route("/add_patient", methods=["POST"])
def add_patient():

    name = request.form["name"]
    problem = request.form["problem"]

    # NLP Urgency Prediction
    urgency = predict_urgency(problem)

    if urgency == "High":
        queue = "Emergency Queue 🚨"

    elif urgency == "Medium":
        queue = "Priority Queue ⚠"

    else:
        queue = "Normal Queue"

    conn = sqlite3.connect("hospital.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO patients(name, problem, urgency, queue) VALUES (?, ?, ?, ?)",
        (name, problem, urgency, queue)
    )

    conn.commit()
    conn.close()

    # Redirect prevents duplicate submission
    return redirect(url_for("index"))


# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)