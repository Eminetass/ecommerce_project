from flask_mail import Message
from app import mail
from flask import current_app

def send_reset_email(to_email, token):
    reset_link = f"http://localhost:5000/auth/reset-password/{token}"  # Localhost için
    msg = Message(
        subject="Şifre Sıfırlama İsteği",
        recipients=[to_email],
        sender=current_app.config['MAIL_USERNAME'],
        body=f"Şifrenizi sıfırlamak için aşağıdaki bağlantıya tıklayın:\n{reset_link}"
    )
    mail.send(msg)
