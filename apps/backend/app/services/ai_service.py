from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings

settings = get_settings()

INTAKE_SYSTEM_PROMPT = """You are SANSON Law Firm's AI Legal Intake Assistant.
Your role is the FIRST consultation layer — a free AI-powered legal triage system.

IMPORTANT RULES:
- You are NOT a lawyer and cannot provide legal advice.
- Gather information about the client's legal concern through conversational intake.
- Identify case category (criminal, civil, labor, family, cybercrime, administrative).
- Assess urgency and identify missing information.
- Summarize the concern clearly.
- DO NOT suggest booking a consultation — booking only happens when the client formally proceeds.
- When enough information is gathered, offer to help them "Proceed with Legal Action" if the matter seems actionable.
- Be professional, empathetic, and clear.
- Support multilingual communication when the client writes in another language.
"""


class AIService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def stream_intake_response(self, message: str) -> AsyncGenerator[str, None]:
        """Stream AI intake response. Full OpenAI integration in Phase 2."""
        if not settings.openai_api_key:
            fallback = (
                "Thank you for contacting SANSON Law Firm. I'm your AI Legal Intake Assistant. "
                "Please describe your legal concern in detail, and I'll help organize your case "
                "for our legal team. (OpenAI API key required for full AI responses — Phase 2)"
            )
            for word in fallback.split():
                yield word + " "
            return

        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=settings.openai_api_key)
            stream = await client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": INTAKE_SYSTEM_PROMPT},
                    {"role": "user", "content": message},
                ],
                stream=True,
            )
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception:
            yield "I apologize, but I'm temporarily unable to process your request. Please try again."

    async def classify_case(self, text: str) -> dict:
        categories = ["criminal", "civil", "labor", "family", "cybercrime", "administrative"]
        return {"category": "civil", "confidence": 0.5, "categories": categories}

    async def summarize_case(self, text: str) -> dict:
        return {
            "summary": "",
            "key_facts": [],
            "parties": [],
            "evidence_refs": [],
        }
