from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail
import redis
from routes.celery_config import make_celery

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Configurations
app.config['SECRET_KEY'] = 'richa2011'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz.db"

# Celery Configuration
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
app.config["result_backend"] = "redis://localhost:6379/0"

# Mail Configuration
app.config["MAIL_SERVER"] = "localhost"  # Use MailHog or SMTP
app.config["MAIL_PORT"] = 1025  # Default MailHog port
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = None
app.config["MAIL_PASSWORD"] = None
app.config["MAIL_DEFAULT_SENDER"] = "noreply@quizmaster.com"

# Initialize Extensions
db = SQLAlchemy()
mail = Mail(app)  # Initialize Flask-Mail
celery = make_celery(app)

# Import Models & Routes (After initializing Flask-Mail)
from model.models import *
from routes import admin
from routes import user
from routes import tasks
from routes.worker import schedules

# Initialize DB
with app.app_context():
    db.init_app(app)
    db.create_all()

