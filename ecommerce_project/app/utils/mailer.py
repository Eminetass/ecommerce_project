from flask_mail import Message
from app import mail
from flask import current_app

def send_reset_email(to, token):
    msg = Message(
        subject="Şifre Sıfırlama",
        sender=current_app.config["MAIL_USERNAME"],
        recipients=[to],
    )
    reset_link = f"http://localhost:5000/auth/reset-password/{token}"
    msg.body = f"Şifrenizi sıfırlamak için bağlantıya tıklayın: {reset_link}"

    mail.send(msg)


def send_cart_update_email(to):
    msg = Message(
        subject="Sepetiniz Güncellendi",
        sender=current_app.config["MAIL_USERNAME"],
        recipients=[to],
    )
    msg.body = "Sepetinize yeni bir ürün eklendi! Alışverişinize devam etmek için sitemizi ziyaret edin."
    mail.send(msg)

