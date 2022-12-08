from typing import Any

from fastapi import APIRouter
from fastapi_mail import MessageSchema, MessageType

from backend import schemas
from backend.utils.email import fast_mail

router = APIRouter()


@router.post("/email", response_model=schemas.ContactSendEmail)
async def login_access_token(contact_send_email: schemas.ContactSendEmail) -> Any:
    """
    Email the website admin from the contact page
    """
    message = MessageSchema(
        subject='EMWI Auto Moto Kontakt',
        recipients=[contact_send_email.email],
        body=contact_send_email.message,
        subtype=MessageType.plain)
    await fast_mail.send_message(message)
    return contact_send_email
