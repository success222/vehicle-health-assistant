import json
from typing import Any

from fastapi import HTTPException
from google import genai
from pydantic import ValidationError

from app.core.config import settings
from app.core.logger import logger
from app.prompts.health_prompt import build_prompt
from app.schemas.response import AIHealthReport
from app.schemas.vehicle import VehicleRequest

# Initialize Gemini client
client = genai.Client(api_key=settings.GEMINI_API_KEY)


def generate_health_report(
    vehicle: VehicleRequest,
    features: dict[str, Any],
) -> AIHealthReport:
    """
    Generate a structured vehicle health assessment using Gemini.

    Args:
        vehicle: Validated vehicle request.
        features: Engineered vehicle maintenance indicators.

    Returns:
        AIHealthReport: Structured AI-generated assessment.
    """

    prompt = build_prompt(vehicle, features)

    try:
        logger.info(
            "Generating health report for %s %s",
            vehicle.make,
            vehicle.model,
        )
        
        logger.info("Using Gemini model: %s", settings.GEMINI_MODEL)
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
        )

        response_text = response.text.strip()

        # Remove markdown code fences if present
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "", 1)

        if response_text.endswith("```"):
            response_text = response_text[:-3]

        response_json = json.loads(response_text.strip())

        report = AIHealthReport(**response_json)

        logger.info("Gemini response validated successfully")

        return report

    except json.JSONDecodeError:
        logger.exception("Gemini returned invalid JSON")

        raise HTTPException(
            status_code=500,
            detail="The AI returned an invalid JSON response.",
        )

    except ValidationError:
        logger.exception("Gemini response failed schema validation")

        raise HTTPException(
            status_code=500,
            detail="The AI response did not match the expected schema.",
        )

    except Exception as e:
        logger.exception("Gemini request failed")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )