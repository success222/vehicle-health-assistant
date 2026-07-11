import requests


url = "http://127.0.0.1:8000/api/v1/predict-health"


payload = {
    "make": "Toyota",
    "model": "Camry",
    "year": 2018,
    "mileage": 120000,
    "driving_pattern": "Medium Trips",
    "fuel_type": "Petrol",

    "last_service_date": "2023-01-10",
    "last_oil_change_date": "2023-02-15",
    "battery_installation_date": "2021-01-01",
    "brake_installation_date": "2020-06-01",
    "last_coolant_change_date": "2022-01-01"
}


response = requests.post(
    url,
    json=payload
)


print("Status:", response.status_code)

print("\nResponse:")
print(response.json())