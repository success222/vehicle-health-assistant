from datetime import UTC, datetime

from fastapi import FastAPI

from app.api.routes import router

from app.core.middleware import log_request_time


API_VERSION = "1.0.0"



app = FastAPI(
    title="Vehicle Health Assistant API",
    description=(
        "AI-powered backend for predictive vehicle maintenance "
        "using engineered vehicle features and Gemini."
    ),
    version=API_VERSION,
)

app.add_middleware(log_request_time)

app.include_router(
    router,
    prefix="/api/v1",
    tags=["Vehicle Health"]
)


@app.get(
    "/",
    tags=["System"]
)
def root():
    """
    Root endpoint confirming that the API is running.
    """

    return {
        "message": "Vehicle Health Assistant API",
        "status": "running",
        "version": API_VERSION
    }


@app.get(
    "/health",
    tags=["System"]
)
def health():
    """
    Health check endpoint for monitoring service availability.
    """

    return {
        "status": "healthy",
        "timestamp": datetime.now(UTC).isoformat(),
        "version": API_VERSION
    }