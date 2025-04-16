from fastapi_mail import MessageType, FastMail, MessageSchema, ConnectionConfig
from ...infrastructure.config.variables import ANTEIKU_KOHI_EMAIL, ANTEIKU_KOHI_EMAIL_APP_PASSWORD
from pydantic import SecretStr
from ...infrastructure.config.serializer import serializer
from ...infrastructure.config.variables import EMAIL_SALT_VERIFYCATION

conf = ConnectionConfig(
    MAIL_USERNAME=ANTEIKU_KOHI_EMAIL,
    MAIL_PASSWORD=SecretStr(ANTEIKU_KOHI_EMAIL_APP_PASSWORD),
    MAIL_FROM=ANTEIKU_KOHI_EMAIL,
    MAIL_FROM_NAME="Anteiku Team",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    USE_CREDENTIALS=True,
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=True,
)

async def send_email_verification(email: str):
    verification_token = serializer.dumps(email, salt=EMAIL_SALT_VERIFYCATION)
    confirmation_url = f"https://localhost:8000/user/email-verification/{verification_token}"
    message = MessageSchema(
        subject="Anteiku Kohi - Xác thực email",
        recipients=[email],
        body=f"Liên kết xác thực: <a href=\"{confirmation_url}\">{confirmation_url}</a>",
        subtype=MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(message)
