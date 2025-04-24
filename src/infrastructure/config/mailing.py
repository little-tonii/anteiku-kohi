from fastapi_mail import ConnectionConfig
from .variables import ANTEIKU_KOHI_EMAIL, ANTEIKU_KOHI_EMAIL_APP_PASSWORD
from pydantic import SecretStr

mail_config = ConnectionConfig(
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
