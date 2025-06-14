import uuid

from src.mailing.tasks import send_activation_mail
from src.shared.cache import CacheService


class ActivationService:

    def create_token(self, email) -> uuid.UUID:
        return uuid.uuid3(namespace=uuid.uuid4(), name=email)

    def create_link(self, activation_token: uuid.UUID) -> str:
        return f"https://frontend.com/users/activate/{activation_token}"

    def send_user_activation_email(
        self,
        email: str,
        activation_token,
    ) -> None:
        activation_link = self.create_link(activation_token)
        send_activation_mail.delay(
            recipient=email, activation_link=activation_link
        )

    def save_activation_information(
        self, internal_user_id: int, activation_token: uuid.UUID
    ) -> None:

        cache = CacheService()
        payload = {"user_id": internal_user_id}
        cache.save(
            namespace="activation",
            key=activation_token,
            instance=payload,
            ttl=86_400,
        )

    def validate_activation(self, activation_token: uuid.UUID) -> None | dict:

        cache = CacheService()

        result = cache.get("activation", activation_token)
        if not result:
            return None

        cache.delete(activation_token)

        return result
