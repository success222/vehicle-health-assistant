from datetime import UTC, datetime
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.schemas.response import (
    AIHealthReport,
    ComponentHealth,
    MaintenanceRecommendation,
)

client = TestClient(app)


@patch("app.api.routes.generate_health_report")
def test_predict_vehicle_health(mock_generate):
    """
    Test the vehicle health prediction endpoint using a mocked
    Gemini response.
    """

    mock_generate.return_value = AIHealthReport(
        confidence="High",
        health_score=90,
        component_health=ComponentHealth(
            engine_oil="Good",
            brake_pads="Good",
            battery="Good",
            coolant="Good",
            transmission="Good",
            tires="Good",
        ),
        maintenance_recommendations=[
            MaintenanceRecommendation(
                component="General Service",
                recommendation="Schedule routine servicing.",
                priority="Next Scheduled Service",
            )
        ],
        summary="Vehicle is in good overall condition.",
    )

    payload = {
        "make": "Toyota",
        "model": "Camry",
        "year": 2020,
        "mileage": 50000,
        "driving_pattern": "Medium Trips",
        "fuel_type": "Petrol",
        "last_service_date": "2026-01-10",
        "brake_installation_date": "2025-06-01",
        "battery_installation_date": "2025-01-01",
        "last_oil_change_date": "2026-03-01",
        "last_coolant_change_date": "2025-02-01",
    }

    response = client.post(
        "/api/v1/predict-health",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    # Backend-generated metadata
    assert "request_id" in data
    assert "generated_at" in data

    # AI-generated fields
    assert data["confidence"] == "High"
    assert data["health_score"] == 90

    # Nested response validation
    assert data["component_health"]["engine_oil"] == "Good"
    assert len(data["maintenance_recommendations"]) == 1
    assert (
        data["maintenance_recommendations"][0]["priority"]
        == "Next Scheduled Service"
    )