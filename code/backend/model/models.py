from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from routes import db
from datetime import datetime

# -------------------- MODELS -----------------

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default='user')
    last_login = db.Column(db.DateTime, nullable=True)  # Added last_login
    quiz_attempts = db.relationship('QuizAttempt', cascade='delete')

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default='admin')  # Admin role

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)
    quizzes = db.relationship('Quiz', cascade='delete')
    chapters = db.relationship('Chapter', cascade='delete')  # Added relationship

class Chapter(db.Model):
    __tablename__ = 'chapter'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    description = db.Column(db.String, nullable=True)
    quizzes = db.relationship('Quiz', cascade='delete')  # Each chapter can have multiple quizzes

class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=True)
    total_marks = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Ensure correct default
    questions = db.relationship('Question', cascade='delete')
    attempts = db.relationship('QuizAttempt', cascade='delete')

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    text = db.Column(db.String, nullable=False)
    option_a = db.Column(db.String, nullable=False)
    option_b = db.Column(db.String, nullable=False)
    option_c = db.Column(db.String, nullable=False)
    option_d = db.Column(db.String, nullable=False)
    correct_option = db.Column(db.String, nullable=False)  # Values: 'a', 'b', 'c', 'd'
    marks = db.Column(db.Integer, nullable=False)

class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempt'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    score = db.Column(db.Integer, default=0)
    start_time = db.Column(db.DateTime(timezone=True), server_default=func.now())
    duration = db.Column(db.Integer, nullable=True)
