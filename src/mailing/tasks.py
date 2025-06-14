import asyncio

from fastapi_mail import FastMail, MessageSchema, MessageType

from src.mailing import celery_app
from src.mailing.config import conf


@celery_app.task
def send_mail(to_email: str):
    print(f"sending mail to {to_email}")


@celery_app.task
def send_activation_mail(recipient: str, activation_link: str):
    message = MessageSchema(
        subject="User activation",
        recipients=[recipient],
        body=f"Please, activate your account: {activation_link}",
        subtype=MessageType.html,
    )
    fm = FastMail(conf)

    asyncio.run(fm.send_message(message))

    print(f"Activation email sent to {recipient}")
    return {"message": "email has been sent"}
