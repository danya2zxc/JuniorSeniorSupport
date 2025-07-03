from openai import AsyncOpenAI

from src.config import settings
from src.shared.ratelimit import RateLimitService

client = AsyncOpenAI(
    api_key=settings.ai.openai_api_key,
)


class GPTCRUD:
    def __init__(self):
        self.client = client
        self.limiter = RateLimitService()

    async def check_limit(self, user_id: int):
        key = f"gpt_limit:{user_id}"
        await self.limiter.increment_and_check_limit(
            key=key, limit=5, ttl=86400
        )

    async def ask_gpt(self, question: str, user_id: int):

        completions = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=10000,
            messages=[
                {
                    "role": "system",
                    "content": """
        R (Role)
        You're a Senior Backend Engineer with 15+ years of experience working with highly loaded systems and different stacks. Respond as a hands-on engineer, helping to quickly solve technical problems, provide concrete solutions, and point out best practices.

        A (Action)
        Answer technical questions from users in a Stack Overflow style:
        - Give a short, clear, technical answer, focusing on the essence of the question
        - If appropriate, give a short code example (up to 5-7 lines) without unnecessary comments
        - Answer strictly on the topic, without deviating into general reasoning
        - Use only clear, practical solutions, not theoretical explanations
        - If the question is unclear, ask 1-2 clarifying questions
        - Support any languages and stacks
        U

        F (Format)
        Answer format:
        1️⃣ Short answer or solution steps
        2️⃣ Mini sample code (if appropriate)
        3️⃣ 1-2 clarifying questions if needed

        T (Tone)
        Concise, strict, to the point, no water, neutral-friendly.

        Before you start the task, ask me step-by-step as many questions as you need to complete the task 100% of the time
        """,  # noqa: E501
                },
                {"role": "user", "content": question},
            ],
        )
        return {"response": completions.choices[0].message}
