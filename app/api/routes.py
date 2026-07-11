import uuid
from datetime import UTC, datetime

from fastapi import APIRouter

from app.core.logger import logger
from app.schemas.response import VehicleResponse
from app.schemas.vehicle import VehicleRequest
from app.services.feature_engineering import engineer_features
from app.services.llm_service import generate_health_report


router = APIRouter()


@router.post(
    "/predict-health",
    response_model=VehicleResponse
)
def predict_vehicle_health(vehicle: VehicleRequest):
    """
    Predict the health of a vehicle based on its information
    and maintenance history.
    """

    # Generate request metadata
    request_id = str(uuid.uuid4())
    generated_at = datetime.now(UTC)

    logger.info(
        f"Prediction request received | Request ID: {request_id}"
    )

    # Identify missing optional maintenance information
    optional_fields = {
        "last_service_date": "Last service date",
        "last_oil_change_date": "Last oil change date",
        "battery_installation_date": "Battery installation date",
        "brake_installation_date": "Brake installation date",
        "last_coolant_change_date": "Last coolant change date",
    }

    missing_information = [
        label
        for field, label in optional_fields.items()
        if getattr(vehicle, field) is None
    ]

    try:
        # Engineer features
        features = engineer_features(vehicle)

        # Generate AI assessment
        health_report = generate_health_report(
            vehicle,
            features
        )

        # Combine backend metadata + AI output
        final_response = VehicleResponse(
            request_id=request_id,
            generated_at=generated_at,
            missing_information=missing_information or None,
            **health_report.model_dump()
        )

        logger.info(
            f"Prediction completed | Request ID: {request_id}"
        )

        return final_response

    except Exception:
        logger.exception(
            f"Prediction failed | Request ID: {request_id}"
        )

        raise