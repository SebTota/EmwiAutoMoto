import os

from fastapi_mail import ConnectionConfig, FastMail

from backend.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USERNAME,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.SMTP_MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER="email-smtp.us-east-1.amazonaws.com",
    MAIL_FROM_NAME="EMWI Auto Moto",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

fast_mail = FastMail(conf)
