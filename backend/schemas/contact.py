from pydantic import BaseModel


class ContactSendEmail(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: str
    message: str
