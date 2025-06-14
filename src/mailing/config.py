from fastapi_mail import ConnectionConfig
from pydantic import SecretStr

from src.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.email.mail_username,
    MAIL_PASSWORD=SecretStr(settings.email.mail_password),
    MAIL_FROM=settings.email.mail_from,
    MAIL_PORT=settings.email.mail_port,
    MAIL_SERVER=settings.email.mail_server,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=False,
    VALIDATE_CERTS=False,
)
