from pydantic import BaseModel


class ContactSendEmail(BaseModel):
    email: str
    message: str
