import smtplib

from pydantic import EmailStr

from app.config import settings
from app.tasks.celery import celery
from app.tasks.email_templates import create_purchase_confirmation_template


@celery.task
def send_purchase_confirmation_email(
    purchase: dict,
    username: str,
    email_to: EmailStr
):
    """Отправляет email с подтверждением бронирования."""
    email_to_user = settings.SMTP_USER
    email_content = create_purchase_confirmation_template(
        purchase=purchase, username=username, email_to=email_to_user
    )
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(email_content)
