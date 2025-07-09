from flask_mail import Message
from routes import mail, app

def send_email(recipient, subject, body, html=False):
    """Send email using Flask-Mail."""
    with app.app_context():
        msg = Message(subject, recipients=[recipient])
        if html:
            msg.html = body
        else:
            msg.body = body
        mail.send(msg)

