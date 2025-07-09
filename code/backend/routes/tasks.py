import csv
import os
from flask import Flask
from model.models import *
from routes import db
from routes import celery
from routes import app
from jinja2 import Template
from datetime import datetime, timedelta
from routes.mail_service import send_email
from flask import render_template

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get `routes/` absolute path
BACKEND_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))  # Move up to `backend/`
EXPORT_FOLDER = os.path.join(os.getcwd(), "static", "exports")  # Ensure correct path
os.makedirs(EXPORT_FOLDER, exist_ok=True)   # Ensure the directory exists

@celery.task()
def export_user_quiz_data(user_id):
    """Generate CSV for a specific user's quiz history."""
    print(f"🚀 [CELERY] Task Started: Exporting User {user_id} Quiz Data...")

    filename = f"user_{user_id}_export.csv"
    filepath = os.path.join(EXPORT_FOLDER, filename)

    with app.app_context():  # Ensure DB access
        attempts = (
            db.session.query(
                QuizAttempt, Quiz.title, Chapter.title, Subject.name
            )
            .join(Quiz, Quiz.id == QuizAttempt.quiz_id)
            .join(Chapter, Chapter.id == Quiz.chapter_id)
            .join(Subject, Subject.id == Quiz.subject_id)
            .filter(QuizAttempt.user_id == user_id)
            .all()
        )

        print(f"✅ [CELERY] Query executed! Found {len(attempts)} rows.")

        if not attempts:
            print("⚠️ [CELERY] No quiz attempts found! CSV will be empty.")
            return None

        # ✅ Open CSV safely
        with open(filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Quiz ID", "Subject", "Chapter", "Quiz Name", "Score", "Start Time", "Duration"])

            for i, row in enumerate(attempts):
                attempt, quiz_name, chapter_name, subject_name = row

                print(f"📌 Writing row {i + 1}: {row}")  # Debugging each row
                
                writer.writerow([
                    attempt.quiz_id,  # From QuizAttempt
                    subject_name,
                    chapter_name,
                    quiz_name,
                    attempt.score,  # From QuizAttempt
                    attempt.start_time,  # From QuizAttempt
                    attempt.duration  # From QuizAttempt
                ])

        print(f"✅ [CELERY] CSV Exported Successfully: {filepath}")
        return filename

@celery.task()
def export_admin_quiz_data():
    """Generate CSV for admin with all users' quiz performance."""
    from routes import app  # Import Flask app dynamically inside Celery

    print("🚀 [CELERY] Task Started: Exporting Admin Quiz Data...")

    # ✅ Ensure Celery gets access to the Flask app context
    with app.app_context():
        print("🔍 [CELERY] Initializing new database session...")
        
        # ✅ Manually create a new database session
        session = db.session()
        
        try:
            filename = "admin_exports.csv"
            filepath = os.path.join(EXPORT_FOLDER, filename)

            print("🔍 [CELERY] About to fetch quiz attempts...")

            attempts = (
                session.query(
                    QuizAttempt.user_id,
                    User.name,
                    Quiz.title,
                    QuizAttempt.score,
                    QuizAttempt.start_time,
                    QuizAttempt.duration
                )
                .join(User, User.id == QuizAttempt.user_id)
                .join(Quiz, Quiz.id == QuizAttempt.quiz_id)
                .all()
            )

            print(f"✅ [CELERY] Query executed! Found {len(attempts)} rows.")

            if not attempts:
                print("⚠️ [CELERY] No quiz attempts found! CSV will be empty.")
                return None

            with open(filepath, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["User ID", "User Name", "Quiz Name", "Score", "Start Time", "Duration"])

                for attempt in attempts:
                    if len(attempt) != 6:
                        print(f"❌ [CELERY] Skipping malformed row: {attempt}")
                        continue
                    writer.writerow(attempt)

            print(f"✅ [CELERY] CSV Exported Successfully: {filepath}")

            return filename

        except Exception as e:
            print(f"❌ [CELERY] ERROR: {e}")
        
        finally:
            print("🔴 [CELERY] Closing database session...")
            session.close()

@celery.task()
def send_daily_reminders():
    print("🚀 [CELERY] Daily Reminder Task Started...")

    with app.app_context():
        today = datetime.utcnow().date()
        yesterday = today - timedelta(days=1)

        # Find inactive users (users who didn't visit since yesterday)
        inactive_users = User.query.filter(User.last_login < yesterday).all()

        # Find new quizzes added today
        new_quizzes = Quiz.query.filter(func.date(Quiz.created_at) == today).all()

        # Send reminders to inactive users
        for user in inactive_users:
            message = f"Hello {user.name}, you haven't visited the platform recently. Check out the latest quizzes!"
            send_email(user.email, "Quiz Master - Daily Reminder", message)

        # Notify all users about new quizzes
        for quiz in new_quizzes:
            users = User.query.all()
            for user in users:
                message = f"A new quiz '{quiz.title}' is available. Attempt it now!"
                send_email(user.email, "New Quiz Available!", message)

        print("✅ [CELERY] Daily reminders sent successfully!")

@celery.task()
def send_monthly_report():
    print("🚀 [CELERY] Monthly Report Task Started...")

    with app.app_context():
        users = User.query.all()
        one_month_ago = datetime.utcnow() - timedelta(days=30)

        for user in users:
            # Fetch quiz attempts for the last month
            attempts = (
                db.session.query(QuizAttempt, Quiz.title)
                .join(Quiz, Quiz.id == QuizAttempt.quiz_id)
                .filter(QuizAttempt.user_id == user.id, QuizAttempt.start_time >= one_month_ago)
                .all()
            )

            if not attempts:
                print(f"⚠️ [CELERY] No quiz attempts for {user.name}, skipping report.")
                continue

            total_quizzes = len(attempts)
            total_score = sum([attempt.QuizAttempt.score for attempt in attempts])
            average_score = total_score / total_quizzes if total_quizzes > 0 else 0

            # Ranking calculation
            all_users_attempts = db.session.query(
                QuizAttempt.user_id, db.func.sum(QuizAttempt.score).label("total_score")
            ).group_by(QuizAttempt.user_id).all()
            
            sorted_users = sorted(all_users_attempts, key=lambda x: x.total_score, reverse=True)
            ranking = next((i + 1 for i, u in enumerate(sorted_users) if u.user_id == user.id), "N/A")

            # ✅ Generate HTML table dynamically
            quiz_history_table = """
                <table border="1" style="border-collapse: collapse; width: 100%;">
                    <thead>
                        <tr>
                            <th>Quiz</th>
                            <th>Score</th>
                            <th>Attempt Date</th>
                        </tr>
                    </thead>
                    <tbody>
            """

            # ✅ Loop through attempts and add rows dynamically
            for attempt in attempts:
                quiz_history_table += f"""
                    <tr>
                        <td>{attempt.title}</td>
                        <td>{attempt.QuizAttempt.score}</td>
                        <td>{attempt.QuizAttempt.start_time.strftime('%d-%m-%Y')}</td>
                    </tr>
                """

            quiz_history_table += """
                    </tbody>
                </table>
            """

            # ✅ Generate email content (Jinja2 template)
            template = Template("""
                <h2>Monthly Quiz Activity Report</h2>
                <p>Hello {{ user_name }},</p>
                <p>Here is your activity summary for the last month:</p>
                <ul>
                    <li><strong>Total quizzes attempted:</strong> {{ total_quizzes }}</li>
                    <li><strong>Total score:</strong> {{ total_score }}</li>
                    <li><strong>Average score:</strong> {{ average_score }}</li>
                    <li><strong>Ranking:</strong> {{ ranking }}</li>
                </ul>
                <h3>📊 Your Quiz History</h3>
                {{ quiz_table|safe }}
                <p>Keep up the good work!</p>
            """)

            html_report = template.render(
                user_name=user.name,
                total_quizzes=total_quizzes,
                total_score=total_score,
                average_score=average_score,
                ranking=ranking,
                quiz_table=quiz_history_table
            )

            # ✅ Send the email with the rendered table
            send_email(user.email, "Monthly Quiz Report", html_report, html=True)


        print("✅ [CELERY] Monthly reports sent successfully!")
