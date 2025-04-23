from ...infrastructure.config.serializer import serializer
from ...infrastructure.config.variables import EMAIL_SALT_VERIFYCATION
from fastapi_mail import FastMail, MessageSchema, MessageType
from ...infrastructure.config.mailing import mail_config

async def send_email_verification(email: str):
    verification_token = serializer.dumps(email, salt=EMAIL_SALT_VERIFYCATION)
    confirmation_url = f"https://localhost:8000/user/email-verification/{verification_token}"
    message = MessageSchema(
        subject="Anteiku Kohi - Xác thực email",
        recipients=[email],
        body=f"Liên kết xác thực: <a href=\"{confirmation_url}\">{confirmation_url}</a>",
        subtype=MessageType.html
    )
    fm = FastMail(mail_config)
    await fm.send_message(message)
