from celery.schedules import crontab
from routes import celery
from routes.tasks import send_daily_reminders, send_monthly_report

def schedules():
    # Schedule daily reminders at 7 PM every day
    celery.conf.beat_schedule = {
        "daily-reminder-task": {
            "task": "routes.tasks.send_daily_reminders",
            "schedule": crontab(hour=15, minute=5),
        },
        "monthly-report-task": {
            "task": "routes.tasks.send_monthly_report",
            "schedule": crontab(day_of_month=30, hour=15, minute=10),  # Runs on the 1st of every month
        }
    }

    celery.conf.timezone = "Asia/Kolkata"

schedules=schedules()

