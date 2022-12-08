import os

from fastapi_mail import ConnectionConfig, FastMail

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('SMTP_EMAIL'),
    MAIL_PASSWORD=os.getenv('SMTP_PASSWORD'),
    MAIL_FROM="emwiautomoto@sebtota.com",
    MAIL_PORT=587,
    MAIL_SERVER="email-smtp.us-east-1.amazonaws.com",
    MAIL_FROM_NAME="EMWI Auto Moto",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

fast_mail = FastMail(conf)
