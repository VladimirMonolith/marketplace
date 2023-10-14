from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_purchase_confirmation_template(
    purchase: dict,
    username: str,
    email_to: EmailStr
):
    """Формирует email о подтверждении покупки."""
    email = EmailMessage()

    email['Subject'] = 'Подтверждение покупки.'
    email['From'] = settings.SMTP_USER
    email['To'] = email_to

    email.set_content(
        f"""
        <h1>Подтверждение покупки.</h1>
        Здравствуйте, {username}!
        {purchase['when']} Вы совершили покупку в нашем магазине.
        Благодарим за доверие и надеемся на дальнейшее сотрудничество.
        """,
        subtype='html'
    )
    return email
