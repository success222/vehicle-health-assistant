# Vehicle Health Assistant API

An AI-powered FastAPI backend that predicts vehicle health using engineered vehicle maintenance indicators and Gemini-generated insights.

The system combines deterministic feature engineering with AI reasoning. Python calculates maintenance indicators from vehicle data, while Gemini generates structured health assessments and AI-generated maintenance recommendations based on those indicators.

## Features

- API versioning (`/api/v1`)
- Input validation with Pydantic
- Vehicle maintenance feature engineering
- Gemini-powered health assessments
- Health score and confidence level
- Component-level health analysis
- Maintenance recommendations with priority levels
- Missing information detection
- Request ID tracking
- Health monitoring endpoint

## Tech Stack

- Python
- FastAPI
- Pydantic
- Google Gemini API
- Uvicorn
- Pytest

## Getting Started

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=your_model_name
```

Start the development server:

```bash
uvicorn app.main:app --reload
```

Once the server is running, the interactive API documentation is available at:

```
http://127.0.0.1:8000/docs
```

## API Endpoint

### Vehicle Health Prediction

**POST** `/api/v1/predict-health`

Generates a structured vehicle health report based on vehicle information and engineered maintenance indicators.

### Sample Request

```json
{
  "make": "Toyota",
  "model": "Corolla",
  "year": 2021,
  "mileage": 45000,
  "driving_pattern": "Medium Trips",
  "fuel_type": "Petrol",
  "last_service_date": "2026-01-15",
  "brake_installation_date": "2025-06-10",
  "battery_installation_date": "2025-03-20",
  "last_oil_change_date": "2026-03-01",
  "last_coolant_change_date": "2025-12-01"
}
```

### Sample Response

```json
{
  "confidence": "High",
  "health_score": 85,
  "component_health": {
    "engine_oil": "Good",
    "brake_pads": "Good",
    "battery": "Good",
    "coolant": "Good",
    "transmission": "Fair",
    "tires": "Fair"
  },
  "maintenance_recommendations": [
    {
      "component": "General Service",
      "recommendation": "Schedule a comprehensive vehicle service.",
      "priority": "Within 2 Weeks"
    }
  ],
  "summary": "Overall vehicle condition is good, but a general service is overdue."
}
```
Design Approach

The backend follows a hybrid AI approach:

Python performs deterministic maintenance calculations and feature engineering.
Gemini generates explanations, prioritization, and structured reporting.

This approach improves reliability by ensuring AI recommendations are grounded in calculated vehicle indicators rather than generated from general assumptions.

## Testing

Run the test suite with:

```bash
pytest
```