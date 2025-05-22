from flask_mail import Message
from app import mail
from flask import current_app


def send_reset_email(email, token):
    msg = Message('Şifre Sıfırlama İsteği',
                 sender=current_app.config['MAIL_USERNAME'],
                 recipients=[email])
    
    msg.body = f'''Şifrenizi sıfırlamak için aşağıdaki bağlantıya tıklayın:
    {current_app.config['FRONTEND_URL']}/reset-password/{token}
    
    Bu bağlantı 30 dakika süreyle geçerlidir.
    '''
    mail.send(msg)


def send_cart_update_email(email, subject, message):
    msg = Message(subject,
                 sender=current_app.config['MAIL_USERNAME'],
                 recipients=[email])
    msg.body = message
    mail.send(msg)


def send_order_confirmation(email, order_details):
    msg = Message('Siparişiniz Alındı',
                 sender=current_app.config['MAIL_USERNAME'],
                 recipients=[email])
    
    msg.body = f'''Siparişiniz başarıyla alındı!
    
    Sipariş Detayları:
    {order_details}
    
    Bizi tercih ettiğiniz için teşekkür ederiz.
    '''
    mail.send(msg)
