from pydantic import BaseModel, EmailStr


class EmailMessage(BaseModel):
    body: str
    subject: str
    recepient: EmailStr
    sender: EmailStr
