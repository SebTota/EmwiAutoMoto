from typing import Any

from fastapi import APIRouter
from fastapi_mail import MessageSchema, MessageType

from backend import schemas
from backend.utils.email import fast_mail

router = APIRouter()


@router.post("/email")
async def send_email(contact_send_email: schemas.ContactSendEmail) -> Any:
    """
    Email the website admin from the contact page
    """
    body = f'{contact_send_email.message}\n\n' \
           f'Od: {contact_send_email.first_name} {contact_send_email.last_name} - {contact_send_email.phone_number}'

    message = MessageSchema(
        subject=f'EMWI Auto Moto Kontakt - {contact_send_email.first_name} {contact_send_email.last_name}',
        recipients=[contact_send_email.email],
        body=body,
        subtype=MessageType.plain)
    await fast_mail.send_message(message)

    return {'details': 'Email sent'}
