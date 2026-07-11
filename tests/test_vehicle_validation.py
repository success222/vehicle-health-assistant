from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_invalid_vehicle_year():

    response = client.post(
        "/api/v1/predict-health",
        json={
            "make": "Toyota",
            "model": "Camry",
            "year": 2030,
            "mileage": 50000,
            "driving_pattern": "Medium Trips",
            "fuel_type": "Petrol"
        }
    )

    assert response.status_code == 422