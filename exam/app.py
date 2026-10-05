from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_connection, close_connection
from config import *

import base64
import cv2
import numpy as np
from ml.detect_face import detect_faces
from monitoring import save_log

# Secret key for session management
app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY



warning_count = {}


@app.route('/')
def home():
    return render_template('index.html')

# -------------------------------
# Registration
# -------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form["name"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        gender = request.form["gender"]
        dob = request.form["dob"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("register"))

        conn = get_connection()
        cursor = conn.cursor()

        query = """
                INSERT INTO students
                (full_name,email,password,mobile,gender,dob)
                VALUES(%s,%s,%s,%s,%s,%s)
                """

        cursor.execute(query,
                       (name, email, password, mobile, gender, dob))

        conn.commit()  # IMPORTANT

        cursor.close()
        conn.close()


        flash("Registration Successful!")
        return redirect(url_for('login'))

    return render_template('register.html')

# -------------------------------
# Login
# -------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT * FROM students
        WHERE email=%s AND password=%s
        """

        cursor.execute(query, (email, password))

        student = cursor.fetchone()

        if student:

            session['student_id'] = student['student_id']
            session['student_name'] = student['full_name']
            session['student_email'] = student['email']
            print("session: ",session)
            return redirect('/dashboard')

        else:

            flash("Invalid Email or Password")
        cursor.close()
        conn.close()

    return render_template('login.html')
# -------------------------------
# Dashboard
# -------------------------------

@app.route('/dashboard')
def dashboard():


    if 'student_id' not in session:
        return redirect(url_for('login'))

    return render_template(
        'dashboard.html',
        student_name=session['student_name'],
        student_email=session['student_email']
    )

@app.route('/profile')
def profile():

    if 'student_id' not in session:
        return redirect(url_for('login'))

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM students WHERE student_id=%s",
        (session['student_id'],)
    )

    student = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "profile.html",
        student=student
    )

@app.route('/accessibility')
def accessibility():

    if 'student_id' not in session:
        return redirect(url_for('login'))

    return render_template('accessibility.html')

@app.route("/results")
def results():

    if "student_id" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM history_result
        WHERE student_id=%s
        ORDER BY exam_date DESC
        LIMIT 1
    """,(session["student_id"],))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "result.html",
        result=result
    )

@app.route('/save_accessibility', methods=['POST'])
def save_accessibility():

    if 'student_id' not in session:
        return redirect(url_for('login'))

    voice = 1 if request.form.get('voice') else 0
    high_contrast = 1 if request.form.get('high_contrast') else 0
    font_size = request.form.get('font_size')
    speech_speed = request.form.get('speech_speed')

    # For now, just store in the session
    session["voice"] = request.form.get("voice") is not None
    session['high_contrast'] = high_contrast
    session['font_size'] = font_size
    session['speech_speed'] = speech_speed

    flash("Accessibility settings saved successfully!")

    return redirect(url_for('dashboard'))


@app.route("/camera_frame", methods=["POST"])
def camera_frame():

    data = request.get_json()

    image = data["image"]

    image = image.split(",")[1]

    img = base64.b64decode(image)

    arr = np.frombuffer(img, np.uint8)

    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    status, faces = detect_faces(frame)

    student_id = session.get("student_id")

    if student_id not in warning_count:
        warning_count[student_id] = 0

    suspicious = False

    if status == "No Face":

        warning_count[student_id] += 1

        suspicious = True

        save_log(student_id, "No Face")

    elif status == "Multiple Faces":

        warning_count[student_id] += 1

        suspicious = True

        save_log(student_id, "Multiple Faces")

    return {

        "status": status,

        "faces": faces,

        "warnings": warning_count[student_id],

        "suspicious": suspicious

    }
# -------------------------------
# Instructions Page
# -------------------------------

@app.route('/instructions')
def instructions():

    if 'student_id' not in session:
        return redirect(url_for('login'))

    return render_template('instructions.html')

# -------------------------------
# Exam Page
# -------------------------------



@app.route("/exam")
def exam():

    if 'student_id' not in session:
        return redirect(url_for('login'))

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM questions")

    questions = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "exam.html",
        questions=questions
    )

@app.route('/history')
def history():

    if 'student_id' not in session:
        return redirect(url_for('login'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM history_result
        WHERE student_id=%s
        ORDER BY exam_date DESC
    """, (session['student_id'],))

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "history.html",
        results=results
    )

# -------------------------------
# Submit Exam
# -------------------------------

@app.route('/submit', methods=['POST'])
def submit():

    if 'student_id' not in session:
        return redirect(url_for('login'))

    conn = get_connection()

    # Read questions
    read_cursor = conn.cursor(dictionary=True)

    read_cursor.execute("SELECT * FROM questions")

    questions = read_cursor.fetchall()

    score = 0

    for q in questions:

        student_answer = request.form.get(f"q{q['question_id']}")

        if student_answer == q['correct_answer']:
            score += 1

    total_questions = len(questions)

    if total_questions > 0:
        percentage = round((score / total_questions) * 100, 2)
    else:
        percentage = 0

    read_cursor.close()

    # Save result into history_result table
    write_cursor = conn.cursor()

    insert_query = """
    INSERT INTO history_result
    (student_id, score, total_questions, percentage)
    VALUES (%s, %s, %s, %s)
    """

    write_cursor.execute(
        insert_query,
        (
            session['student_id'],
            score,
            total_questions,
            percentage
        )
    )

    conn.commit()

    write_cursor.close()

    conn.close()

    return render_template(
        "result.html",
        score=score,
        total=total_questions,
        percentage=percentage
    )
# -------------------------------
# Logout
# -------------------------------

@app.route('/logout')
def logout():

    session.clear()

    flash("Logged out successfully!")

    return redirect(url_for('home'))

# -------------------------------
# Run Application
# -------------------------------

if __name__ == '__main__':
    app.run(debug=True)