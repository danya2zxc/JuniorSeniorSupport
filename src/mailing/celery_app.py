from celery import Celery

from src.config import settings

celery_app = Celery(
    "src.celery.app",
    broker=settings.celery.celery_broker_url,
    backend=settings.celery.celery_result_backend,
)

celery_app.autodiscover_tasks(["src.mailing.service"])
