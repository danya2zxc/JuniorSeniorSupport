import uuid

from src.mailing.tasks import send_activation_mail
from src.shared.cache import CacheService

ACTIVATION_NAMESPACE = uuid.NAMESPACE_DNS


class ActivationService:
    def create_token(self, email) -> uuid.UUID:
        return uuid.uuid3(namespace=ACTIVATION_NAMESPACE, name=email)

    async def create_link(self, activation_token: uuid.UUID) -> str:
        return f"https://frontend.com/users/activate/{activation_token}"

    async def send_user_activation_email(
        self,
        email: str,
        activation_token,
    ) -> None:
        activation_link = await self.create_link(activation_token)
        send_activation_mail.delay(
            recipient=email, activation_link=activation_link
        )

    async def save_activation_information(
        self, internal_user_id: int, activation_token: uuid.UUID
    ) -> None:
        cache = CacheService()
        payload = {"user_id": internal_user_id}
        await cache.save(
            namespace="activation",
            key=activation_token,
            instance=payload,
            ttl=86_400,
        )

    async def validate_activation(
        self,
        activation_token: uuid.UUID,
    ) -> None | dict:
        cache = CacheService()

        result = await cache.get("activation", activation_token)
        if not result:
            return None

        await cache.delete(activation_token)

        return result
