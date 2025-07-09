from routes import app
from model.models import *
from flask import request, jsonify
from tokensJWT import *
import base64
import os
import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
import redis
import json

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

#------------------------------------ USER REGISTRATION -------------------------------------

@app.route("/register", methods=["POST"])
def user_signup():
    name = request.json.get("name")
    email=request.json.get("email")
    password = request.json.get("password")

    if not name or not password:
        return jsonify({"message": "Name and password are required"}), 400

    if User.query.filter_by(name=name).first():
        return jsonify({"message": "Username already taken"}), 409

    user = User(name=name, password=password, email=email)
    db.session.add(user)
    db.session.commit()

    token = user_token(name)
    return jsonify({"message": "User Created", "token": token, "userType": "user", "userId": user.id})

#------------------------------------ USER LOGIN -------------------------------------

@app.route("/login", methods=["POST"])
def user_login():
    name = request.json.get("name")
    password = request.json.get("password")

    user = User.query.filter_by(name=name).first()
    if not user or not user.password==password:
        return jsonify({"message": "Invalid credentials"}), 401

    token = user_token(name)
    user.last_login = datetime.datetime.utcnow()
    db.session.commit()

    return jsonify({"token": token, "userType": "user", "userId": user.id, "username": user.name})

#--------------------------------- USER DASHBOARD --------------------------------------

@app.route("/user/quizzes", methods=["GET"])
def get_quizzes():
    print("Loading quizzes")
    cached_quizzes = redis_client.get("quizzes")
    print("cached=",cached_quizzes)
    if cached_quizzes:
        return jsonify(json.loads(cached_quizzes))  # ✅ Use `json.loads()`

    quizzes = (
        db.session.query(Quiz, Subject.name, Chapter.title)
        .join(Subject, Quiz.subject_id == Subject.id)
        .outerjoin(Chapter, Quiz.chapter_id == Chapter.id)
        .all()
    )

    quiz_list = []
    for quiz_obj in quizzes:
        quiz, subject_name, chapter_name = quiz_obj  # ✅ Explicit unpacking
        quiz_list.append({
            "id": quiz.id,
            "title": quiz.title,
            "duration": quiz.duration,
            "subject_name": subject_name,
            "chapter_name": chapter_name if chapter_name else "N/A"
        })

    redis_client.setex("quizzes", 3600, json.dumps(quiz_list))  # ✅ Fix caching
    return jsonify(quiz_list)


@app.route("/user/subjects/<int:subject_id>", methods=["GET"])
def get_chapters_with_quizzes(subject_id):
    """Returns all chapters under a subject with their quizzes."""
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()

    if not chapters:
        return jsonify({"error": "No chapters found for this subject"}), 404

    return jsonify({
        "subject_id": subject_id,
        "chapters": [
            {
                "id": chap.id,
                "title": chap.title,
                "quizzes": [
                    {"id": quiz.id, "title": quiz.title, "duration": quiz.duration}
                    for quiz in Quiz.query.filter_by(chapter_id=chap.id).all()
                ]
            }
            for chap in chapters
        ]
    })

@app.route("/user/quizzes/<int:chapter_id>", methods=["GET"])
def get_quizzes_by_chapter(chapter_id):
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()

    if not quizzes:
        return jsonify({"error": "No quizzes found for this chapter"}), 404
    print(len(quizzes))
    return jsonify({
        "quizzes": [
            {"id": quiz.id, "title": quiz.title, "duration": quiz.duration}
            for quiz in quizzes
        ]
    })
#--------------------------------------- QUIZ -------------------------------------------

@app.route("/user/quiz/<int:quiz_id>", methods=["GET"])
def get_quiz_questions(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    questions = Question.query.filter_by(quiz_id=quiz_id).all()

    return jsonify({
        "title": quiz.title,
        "duration": quiz.duration,
        "questions": [
            {
                "id": q.id,
                "text": q.text,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d
            } for q in questions
        ]
    })

@app.route("/user/quiz/<int:quiz_id>/submit", methods=["POST"])
def submit_quiz(quiz_id):
    data = request.json
    user_id = data.get("user_id")
    duration = data.get("duration")  # Get duration from frontend
    answers = data.get("answers", {})

    if not user_id or duration is None:
        return jsonify({"error": "User ID and duration are required!"}), 400

    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    correct_answers = {q.id: q.correct_option for q in questions}
    answers = {int(k): v for k, v in answers.items()}

    score = sum(1 for q in questions if answers.get(q.id) == correct_answers[q.id])

    # Create a new attempt **only when quiz is submitted**
    new_attempt = QuizAttempt(
        user_id=user_id,
        quiz_id=quiz_id,
        score=score,
        duration=duration,
        start_time=datetime.datetime.utcnow()
    )
    db.session.add(new_attempt)
    db.session.commit()

    # Invalidate cached quiz history
    redis_client.delete(f"quiz_history_{user_id}")

    return jsonify({
        "score": score,
        "correct_answers": correct_answers,
        "total_marks": len(questions),
        "time_taken": duration
    })

#----------------------------------- SEARCH FUNCTIONALITY -----------------------------------------

@app.route("/user/search", methods=["GET"])
def search():
    query = request.args.get("query", "").strip().lower()
    if not query:
        return jsonify({"subjects": [], "chapters": [], "quizzes": []})

    subjects = Subject.query.filter(Subject.name.ilike(f"%{query}%")).all()

    # ✅ Join Subject in the Chapter Query
    chapters = (
        db.session.query(Chapter.id, Chapter.title, Subject.name.label("subject_name"))
        .join(Subject, Chapter.subject_id == Subject.id)
        .filter(Chapter.title.ilike(f"%{query}%"))
        .all()
    )

    # ✅ Join Chapter in the Quiz Query
    quizzes = (
        db.session.query(Quiz.id, Quiz.title, Chapter.title.label("chapter_name"))
        .join(Chapter, Quiz.chapter_id == Chapter.id)
        .filter(Quiz.title.ilike(f"%{query}%"))
        .all()
    )

    return jsonify({
        "subjects": [{"id": sub.id, "name": sub.name} for sub in subjects],
        "chapters": [{"id": chap.id, "title": chap.title, "subject_name": chap.subject_name} for chap in chapters],  # ✅ FIXED
        "quizzes": [{"id": quiz.id, "title": quiz.title, "chapter_name": quiz.chapter_name} for quiz in quizzes],
    })

#-------------------------------------------- QUIZ HISTORY ------------------------------------

@app.route("/user/quiz-history", methods=["GET"])
def get_quiz_history():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    cached_history = redis_client.get(f"quiz_history_{user_id}")
    if cached_history:
        return jsonify(eval(cached_history))

    quiz_attempts = db.session.query(
        QuizAttempt.id,
        Quiz.title.label("quiz_name"),
        Subject.name.label("subject"),
        Chapter.title.label("chapter_name"),
        QuizAttempt.score,
        QuizAttempt.start_time.label("attempt_date"),
    ).join(Quiz, QuizAttempt.quiz_id == Quiz.id) \
    .join(Subject, Quiz.subject_id == Subject.id) \
    .join(Chapter, Quiz.chapter_id == Chapter.id) \
    .filter(QuizAttempt.user_id == user_id) \
    .order_by(QuizAttempt.start_time.desc()).all()

    history = [
        {
            "id": attempt.id,
            "quiz_name": attempt.quiz_name,
            "subject": attempt.subject,
            "chapter_name": attempt.chapter_name,
            "score": attempt.score,
            "attempt_date": attempt.attempt_date.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for attempt in quiz_attempts
    ]

    redis_client.setex(f"quiz_history_{user_id}", 1800, str(history))  # Cache for 30 minutes
    return jsonify(history)

#-------------------------------- USER PERFORMANCE -----------------------------------

@app.route('/user/performance', methods=['GET'])
def get_performance():
    user_id = request.args.get("user_id")
    quiz_id = request.args.get("quiz_id")

    if not user_id or not quiz_id:
        return jsonify({"error": "User ID and Quiz ID are required"}), 400

    attempts = QuizAttempt.query.filter_by(user_id=user_id, quiz_id=quiz_id).order_by(QuizAttempt.start_time).all()

    if not attempts:
        return jsonify({"dates": [], "scores": []})

    performance_data = {
        "dates": [attempt.start_time.strftime('%Y-%m-%d') for attempt in attempts],
        "scores": [attempt.score for attempt in attempts]
    }

    return jsonify(performance_data), 200

@app.route("/user/subjects")
def get_subjects():
    cached_subjects = redis_client.get("subjects")
    if cached_subjects:
        return jsonify(eval(cached_subjects))

    subjects = Subject.query.all()
    subject_list = [{"id": sub.id, "name": sub.name} for sub in subjects]

    redis_client.setex("subjects", 3600, str(subject_list))  # Cache for 1 hour
    return jsonify(subject_list)

@app.route("/user/chapters")
def get_chapters():
    subject_id = request.args.get('subject_id')

    cached_chapters = redis_client.get(f"chapters_{subject_id}")
    if cached_chapters:
        return jsonify(eval(cached_chapters))

    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    chapter_list = [{"id": chap.id, "title": chap.title} for chap in chapters]

    redis_client.setex(f"chapters_{subject_id}", 3600, str(chapter_list))  # Cache for 1 hour
    return jsonify(chapter_list)

@app.route('/user/quiz')
def get_quizzes_names():
    subject_id = request.args.get('subject_id')
    chapter_id = request.args.get('chapter_id')
    print(f"Received subject_id: {subject_id}, chapter_id: {chapter_id}")
    query = Quiz.query

    if subject_id:
        query = query.filter_by(subject_id=subject_id)
    if chapter_id:
        query = query.filter_by(chapter_id=chapter_id)

    quizzes = query.all()

    return jsonify([{"id": quiz.id, "title": quiz.title} for quiz in quizzes])

#--------------------------- EXPORTS --------------------------------------

from flask import request, jsonify, send_from_directory, send_file
from celery.result import AsyncResult
from routes.tasks import export_user_quiz_data
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get `routes/` absolute path
BACKEND_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))  # Move up to `backend/`
EXPORT_FOLDER = os.path.join(BACKEND_DIR, "static", "exports")

@app.route("/user/export_quiz_data", methods=["POST"])
def request_user_export():
    """Triggers a Celery task for user to export quiz data."""
    data = request.json
    user_id = data.get("user_id")
    
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    task = export_user_quiz_data.apply_async(args=[user_id])
    return jsonify({"task_id": task.id, "message": "Export task started"}), 202

@app.route("/export/status/<int:user_id>", methods=["GET"])
def check_export_status(user_id):
    """Check if the exported CSV is available."""
    filename = f"user_{user_id}_export.csv"
    filepath = os.path.join(EXPORT_FOLDER, filename)

    if os.path.exists(filepath):
        return jsonify({"filename": filename}), 200
    
    return jsonify({"filename": None}), 202  # Not ready yet


@app.route("/user/download_quiz_data/<int:user_id>", methods=["GET"])
def download_user_export(user_id):
    """Allows the user to download the exported CSV."""
    filename = f"user_{user_id}_export.csv"
    filepath = os.path.join(EXPORT_FOLDER, filename)

    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    
    return jsonify({"error": "Export file not found"}), 404

#-------------------------------------------- LOGOUT --------------------------------------

@app.route("/logout", methods=["POST"])
def logout():
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # Delete cached quiz history
    redis_client.delete(f"quiz_history_{user_id}")
    redis_client.delete("subjects")
    redis_client.delete("quizzes")
    keys = redis_client.keys("chapters_*")
    if keys:
        redis_client.delete(*keys)

    return jsonify({"message": "Logged out successfully"}), 200
