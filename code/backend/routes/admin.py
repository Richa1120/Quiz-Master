from routes import app, db
from model.models import *
from flask import request, jsonify
from tokensJWT import *
from flask_jwt_extended import jwt_required, get_jwt_identity
import redis
import json

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

#------------------------------------ADMIN LOGIN -------------------------------------

@app.route("/admin/login", methods=["POST"])
def admin_login():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debugging

        name = data.get("name")
        password = data.get("password")

        if not name or not password:
            return jsonify({"message": "Name and password are required"}), 400

        admin = Admin.query.filter_by(name=name).first()
        if admin:
            print("Admin found:", admin.name)
        else:
            print("Admin not found!")
            return jsonify({"message": "Invalid name or password"}), 401

        # Direct string comparison instead of hashing
        if admin.password == password:
            token = admin_token(admin.name)
            return jsonify({"token": token, "userType": "admin"}), 200
        else:
            print("Invalid credentials!")
            return jsonify({"message": "Invalid name or password"}), 401

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": f"Error: {str(e)}"}), 500

#------------------------------------ SUBJECT CRUD -------------------------------------


@app.route('/admin/subjects', methods=['GET', 'POST'])
def manage_subjects():
    if request.method == 'GET':
        cached_subjects = redis_client.get("subjects")
        
        if cached_subjects:
            try:
                return jsonify(json.loads(cached_subjects))
            except json.JSONDecodeError:
                print("Invalid JSON in cache, deleting and fetching fresh data!")
                redis_client.delete("subjects")
        
        # Fetch fresh data from the database
        subjects = Subject.query.all()
        subject_list = [{'id': s.id, 'name': s.name, 'description': s.description} for s in subjects]

        redis_client.setex("subjects", 3600, json.dumps(subject_list))
        return jsonify(subject_list)

    elif request.method == 'POST':
        data = request.json
        if 'name' not in data or 'description' not in data:
            return jsonify({"error": "Missing name or description"}), 400

        new_subject = Subject(name=data['name'], description=data['description'])
        db.session.add(new_subject)
        db.session.commit()

        redis_client.delete("subjects")
        return jsonify({'message': 'Subject added successfully'}), 201


@app.route('/admin/subjects/<int:subject_id>', methods=['PUT'])
def update_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({"error": "Subject not found"}), 404

    data = request.json
    if 'name' in data:
        subject.name = data['name']
    if 'description' in data:
        subject.description = data['description']

    db.session.commit()
    redis_client.delete("subjects")
    return jsonify({'message': 'Subject updated successfully'})

@app.route('/admin/subjects/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({"error": "Subject not found"}), 404

    db.session.delete(subject)
    db.session.commit()
    redis_client.delete("subjects")
    return jsonify({'message': 'Subject deleted successfully'})

#------------------------------------ CHAPTER CRUD -------------------------------------

@app.route('/admin/chapters', methods=['GET', 'POST'])
def manage_chapters():
    if request.method == 'GET':
        cached_chapters = redis_client.get("chapters")
        
        if cached_chapters:
            try:
                return jsonify(json.loads(cached_chapters))
            except json.JSONDecodeError:
                print("Invalid JSON in cache, deleting and fetching fresh data!")
                redis_client.delete("chapters")
        
        # Fetch fresh data from the database
        chapters = Chapter.query.all()
        chapter_list = [{
            'id': c.id,
            'title': c.title,
            'description': c.description,
            'subject_id': c.subject_id
        } for c in chapters]

        redis_client.setex("chapters", 3600, json.dumps(chapter_list))
        return jsonify(chapter_list)

    elif request.method == 'POST':
        data = request.json
        if 'title' not in data or 'subject_id' not in data:
            return jsonify({"error": "Missing title or subject_id"}), 400
        
        subject = Subject.query.get(data['subject_id'])
        if not subject:
            return jsonify({"error": "Invalid subject_id"}), 400

        new_chapter = Chapter(
            title=data['title'],
            description=data.get('description', ''),
            subject_id=data['subject_id']
        )
        db.session.add(new_chapter)
        db.session.commit()

        redis_client.delete("chapters")
        return jsonify({'message': 'Chapter added successfully'}), 201

@app.route('/admin/chapters/<int:chapter_id>', methods=['PUT'])
def update_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return jsonify({"error": "Chapter not found"}), 404

    data = request.json
    if 'title' in data:
        chapter.title = data['title']
    if 'description' in data:
        chapter.description = data['description']
    if 'subject_id' in data:
        subject = Subject.query.get(data['subject_id'])
        if not subject:
            return jsonify({"error": "Invalid subject_id"}), 400
        chapter.subject_id = data['subject_id']

    db.session.commit()
    redis_client.delete("chapters")
    return jsonify({'message': 'Chapter updated successfully'})

@app.route('/admin/chapters/<int:chapter_id>', methods=['DELETE'])
def delete_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return jsonify({"error": "Chapter not found"}), 404

    db.session.delete(chapter)
    db.session.commit()
    redis_client.delete("chapters")
    return jsonify({'message': 'Chapter deleted successfully'})

@app.route('/admin/chapters/search', methods=['GET'])
def search_chapters():
    query = request.args.get('query', '').strip().lower()
    if not query:
        return jsonify([])

    chapters = Chapter.query.filter(Chapter.title.ilike(f"%{query}%")).all()
    
    return jsonify([{
        "id": chapter.id,
        "title": chapter.title,
        "description": chapter.description,
        "subject_id": chapter.subject_id
    } for chapter in chapters])

#------------------------------------ QUIZ CRUD -------------------------------------

@app.route('/admin/quizzes', methods=['GET', 'POST'])
def manage_quizzes():
    if request.method == 'GET':
        cached_quizzes = redis_client.get("quizzes")
        
        if cached_quizzes:
            try:
                return jsonify(json.loads(cached_quizzes))
            except json.JSONDecodeError:
                print("Invalid JSON in cache, deleting and fetching fresh data!")
                redis_client.delete("quizzes")
        
        # Fetch fresh data from the database
        quizzes = Quiz.query.all()
        quiz_list = [{
            'id': q.id,
            'title': q.title,
            'subject_id': q.subject_id,
            'chapter_id': q.chapter_id,
            'total_marks': q.total_marks,
            'duration': q.duration,
        } for q in quizzes]

        redis_client.setex("quizzes", 3600, json.dumps(quiz_list))
        return jsonify(quiz_list)

    elif request.method == 'POST':
        data = request.json
        if 'title' not in data or 'subject_id' not in data or 'total_marks' not in data or 'duration' not in data:
            return jsonify({"error": "Missing required fields"}), 400

        subject = Subject.query.get(data['subject_id'])
        if not subject:
            return jsonify({"error": "Invalid subject_id"}), 400

        chapter_id = data.get('chapter_id')
        if chapter_id:
            chapter = Chapter.query.get(chapter_id)
            if not chapter:
                return jsonify({"error": "Invalid chapter_id"}), 400

        new_quiz = Quiz(
            title=data['title'],
            subject_id=data['subject_id'],
            chapter_id=chapter_id,
            total_marks=data['total_marks'],
            duration=data['duration'],
            created_at=datetime.datetime.utcnow()
        )
        db.session.add(new_quiz)
        db.session.commit()

        redis_client.delete("quizzes")
        return jsonify({'message': 'Quiz added successfully'}), 201

@app.route("/admin/subjects/<int:subject_id>/chapters", methods=["GET"])
def get_chapters_by_subject(subject_id):
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    
    if not chapters:
        return jsonify({"message": "No chapters found"}), 404  # Optional

    return jsonify([{"id": c.id, "name": c.title} for c in chapters])

@app.route('/admin/quizzes/<int:quiz_id>', methods=['PUT'])
def update_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    data = request.json
    if 'title' in data:
        quiz.title = data['title']
    if 'subject_id' in data:
        subject = Subject.query.get(data['subject_id'])
        if not subject:
            return jsonify({"error": "Invalid subject_id"}), 400
        quiz.subject_id = data['subject_id']
    if 'chapter_id' in data:
        chapter = Chapter.query.get(data['chapter_id'])
        if not chapter:
            return jsonify({"error": "Invalid chapter_id"}), 400
        quiz.chapter_id = data['chapter_id']
    if 'total_marks' in data:
        quiz.total_marks = data['total_marks']
    if 'duration' in data:
        quiz.duration = data['duration']

    db.session.commit()
    redis_client.delete("quizzes")
    return jsonify({'message': 'Quiz updated successfully'})

@app.route('/admin/quizzes/<int:quiz_id>', methods=['DELETE'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    db.session.delete(quiz)
    db.session.commit()
    redis_client.delete("quizzes")
    return jsonify({'message': 'Quiz deleted successfully'})

#----------------------------------- SEARCH ----------------------------------------

@app.route("/admin/search", methods=["GET"])
def admin_search():
    query = request.args.get("query", "").strip().lower()
    if not query:
        return jsonify({"subjects": [], "chapters": [], "quizzes": []})

    subjects = Subject.query.filter(Subject.name.ilike(f"%{query}%")).all()
    chapters = Chapter.query.filter(Chapter.title.ilike(f"%{query}%")).all()
    quizzes = Quiz.query.filter(Quiz.title.ilike(f"%{query}%")).all()

    return jsonify({
    "subjects": [{"id": sub.id, "name": sub.name} for sub in subjects],
    "chapters": [
        {
            "id": chap.id,
            "title": chap.title,
            "subject_name": Subject.query.get(chap.subject_id).name
        }
        for chap in chapters
    ],
    "quizzes": [
        {
            "id": quiz.id,
            "title": quiz.title,
            "chapter_name": Chapter.query.get(quiz.chapter_id).title if quiz.chapter_id else "N/A",
            "subject_name": Subject.query.get(quiz.subject_id).name if quiz.subject_id else "N/A"
        }
        for quiz in quizzes
    ]
    })

#------------------------------------ QUESTIONS CRUD -------------------------------------

@app.route('/admin/quiz/<int:quiz_id>/questions', methods=['GET'])
def get_questions(quiz_id):
    try:
        cache_key = f"quiz_questions_{quiz_id}"
        cached_questions = redis_client.get(cache_key)
        
        if cached_questions:
            try:
                return jsonify(json.loads(cached_questions))
            except json.JSONDecodeError:
                print(f"Invalid JSON in cache for {cache_key}, deleting and fetching fresh data!")
                redis_client.delete(cache_key)

        # Fetch fresh data from the database
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404

        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        question_list = [{
            'id': q.id,
            'text': q.text,
            'option_a': q.option_a,
            'option_b': q.option_b,
            'option_c': q.option_c,
            'option_d': q.option_d,
            'correct_option': q.correct_option,
            'marks': q.marks
        } for q in questions]

        response_data = {'quiz_title': quiz.title, 'questions': question_list}
        redis_client.setex(cache_key, 3600, json.dumps(response_data))
        return jsonify(response_data), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route("/admin/quiz/<int:quiz_id>/questions", methods=["POST"])
def add_question(quiz_id):
    data = request.json
    question = Question(quiz_id=quiz_id, **data)
    db.session.add(question)
    db.session.commit()
    redis_client.delete(f"quiz_questions_{quiz_id}")
    return jsonify({"message": "Question added successfully!"})

@app.route("/admin/questions/<int:question_id>", methods=["PUT", "DELETE"])
def modify_question(question_id):
    question = Question.query.get_or_404(question_id)
    if request.method == "PUT":
        data = request.json
        for key, value in data.items():
            setattr(question, key, value)
        db.session.commit()
        redis_client.delete(f"quiz_questions_{question.quiz_id}")
        return jsonify({"message": "Question updated!"})
    elif request.method == "DELETE":
        db.session.delete(question)
        db.session.commit()
        redis_client.delete(f"quiz_questions_{question.quiz_id}")
        return jsonify({"message": "Question deleted!"})

#------------------------------------ USER MANAGEMENT -------------------------------------

@app.route('/admin/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "name": user.name, "email": user.email} for user in users])

@app.route("/admin/users/<int:user_id>/attempts", methods=["GET"])
def get_user_attempts(user_id):
    attempts = (
        db.session.query(
            QuizAttempt.quiz_id,
            Subject.name.label("subject_name"),
            Chapter.title.label("chapter_name"),
            Quiz.title.label("quiz_name"),
            QuizAttempt.score,
            QuizAttempt.start_time,
            QuizAttempt.duration,
            func.count(QuizAttempt.id).label("attempt_count")
        )
        .join(Quiz, Quiz.id == QuizAttempt.quiz_id)
        .join(Chapter, Chapter.id == Quiz.chapter_id)
        .join(Subject, Subject.id == Quiz.subject_id)
        .filter(QuizAttempt.user_id == user_id)
        .group_by(
            QuizAttempt.quiz_id,
            Subject.name,
            Chapter.title,
            Quiz.title,
            QuizAttempt.score,
            QuizAttempt.start_time,
            QuizAttempt.duration
        )
        .order_by(QuizAttempt.start_time.desc())
        .all()
    )

    results = [
        {
            "quiz_id": attempt.quiz_id,
            "subject_name": attempt.subject_name,
            "chapter_name": attempt.chapter_name,
            "quiz_name": attempt.quiz_name,
            "score": attempt.score,
            "attempt_date": attempt.start_time.strftime("%d-%m-%Y"),
            "duration": attempt.duration,
            "attempt_count": attempt.attempt_count
        }
        for attempt in attempts
    ]

    return jsonify(results)

@app.route('/admin/reports', methods=['GET'])
@jwt_required()
def get_reports():
    subjects_count = Subject.query.count()
    quizzes_count = Quiz.query.count()
    users_count = User.query.count()
    return jsonify({
        "total_subjects": subjects_count,
        "total_quizzes": quizzes_count,
        "total_users": users_count
    })

#------------------------------------- EXPORT DATA --------------------------------------

from flask import jsonify, send_file
from routes.tasks import export_admin_quiz_data
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get `routes/` absolute path
BACKEND_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))  # Move up to `backend/`
EXPORT_FOLDER = os.path.join(BACKEND_DIR, "static", "exports")

@app.route("/admin/export_quiz_data", methods=["POST"])
def request_admin_export():
    task = export_admin_quiz_data.apply_async()
    return jsonify({"task_id": task.id, "message": "Export task started"}), 202


@app.route("/admin/download_quiz_data", methods=["GET"])
def download_admin_export():
    filepath = os.path.join(EXPORT_FOLDER, "admin_exports.csv")
    try:
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#----------------------------------------- LOGOUT -------------------------------------

@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    redis_client.delete("subjects")
    redis_client.delete("chapters")
    redis_client.delete("quizzes")
    keys = redis_client.keys("quiz_questions_*")
    if keys:
        redis_client.delete(*keys)

    return jsonify({"message": "Logged out successfully"}), 200
