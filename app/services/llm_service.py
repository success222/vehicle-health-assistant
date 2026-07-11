import json

from fastapi import HTTPException
from google import genai
from pydantic import ValidationError

from app.core.config import settings
from app.core.logger import logger
from app.prompts.health_prompt import build_prompt
from app.schemas.response import AIHealthReport


client = genai.Client(api_key=settings.GEMINI_API_KEY)


def generate_health_report(vehicle, features) -> AIHealthReport:
    """
    Generate a vehicle health report using Gemini.
    """

    prompt = build_prompt(vehicle, features)

    try:
        logger.info("Sending request to Gemini")

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
        )

        response_text = response.text.strip()

        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "", 1)

        if response_text.endswith("```"):
            response_text = response_text[:-3]

        response_json = json.loads(response_text.strip())

        logger.info("Gemini response validated successfully")

        return AIHealthReport(**response_json)

    except json.JSONDecodeError:
        logger.exception("Gemini returned invalid JSON")

        raise HTTPException(
            status_code=500,
            detail="The AI returned an invalid response."
        )

    except ValidationError:
        logger.exception("Gemini response failed schema validation")

        raise HTTPException(
            status_code=500,
            detail="The AI response format was invalid."
        )

    except Exception:
        logger.exception("Gemini request failed")

        raise HTTPException(
            status_code=500,
            detail="Failed to generate AI health report."
        )