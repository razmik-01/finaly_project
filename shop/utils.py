from django.core.mail import send_mail
from django.conf import settings


def send_verification_email(user):
    """Отправляет код подтверждения на email"""
    subject = "Подтверждение регистрации"
    message = f"Ваш код подтверждения: {user.email_verification_code}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
