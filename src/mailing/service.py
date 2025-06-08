from src.mailing import celery_app


@celery_app.task
def send_mail(to_email: str):
    print(f"sending mail to {to_email}")
