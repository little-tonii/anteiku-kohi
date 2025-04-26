from fastapi_mail import FastMail, MessageSchema, MessageType
from ...infrastructure.config.mailing import mail_config

async def send_email_reset_password_code(email: str, code: str) -> None:
    message = MessageSchema(
        subject="Anteiku Kohi - Yêu cầu đổi mật khẩu",
        recipients=[email],
        body=f"<p color='black'>Mã yêu cầu đổi mật khẩu của bạn là <strong>{code}</strong> có hiệu lực trong vòng 5 phút, vui lòng không cung cấp mã này cho bất kỳ ai.</p>",
        subtype=MessageType.html
    )
    fm = FastMail(mail_config)
    await fm.send_message(message)
