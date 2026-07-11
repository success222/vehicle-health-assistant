# Vehicle Health Assistant API

An AI-powered FastAPI backend for predictive vehicle maintenance. The system combines deterministic feature engineering with Gemini-generated insights. Python calculates maintenance indicators from vehicle data, and Gemini produces structured health assessments and prioritized recommendations grounded in those indicators.

## Features

- FastAPI REST API
- API versioning (`/api/v1`)
- Vehicle maintenance feature engineering
- Gemini-powered structured health assessments
- Component-level health analysis
- Maintenance recommendations with priority levels
- Missing information detection
- Request ID tracking and structured logging
- Health monitoring endpoint

## Tech Stack

- Python 3.12
- FastAPI
- Pydantic
- Google Gemini API
- Uvicorn
- Pytest
- Docker

## Getting Started

Requirements: Python 3.12+

Create and activate a virtual environment:
```bash
python -m venv .venv
   source .venv/bin/activate  # Windows: venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```bash
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-3.5-flash
```

Start the development server:

```bash
uvicorn app.main:app --reload
```
Interactive API docs will be available at: http://127.0.0.1:8000/docs

## API Endpoint

**POST** `/api/v1/predict-health`

Example request and response payloads are available in the `examples/` directory.

## Design Approach

The backend follows a hybrid AI approach to improve reliability and consistency.

Python handles all deterministic work — calculating maintenance indicators, mileage thresholds, and component wear estimates from the raw vehicle data. Gemini then receives these pre-calculated indicators and generates explanations, prioritization, and structured reporting.

This means AI recommendations are always grounded in calculated vehicle data rather than inferred from general assumptions, reducing hallucination risk and making outputs auditable.

## Testing

Run the test suite with:

```bash
pytest -v --tb=short
```

## Running with Docker

Ensure your `.env` file exists in the project root before running — the container reads credentials from it at startup.

Build the image:

```bash
docker build -t vehicle-health-assistant .
```

Run the container:

```bash
docker run -p 8000:8000 --env-file .env vehicle-health-assistant
```

The API will be available at http://localhost:8000