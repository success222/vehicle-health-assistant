import socket

# Force IPv4 for all outbound connections.
# Prevents [Errno 101] Network is unreachable errors caused by
# the Gemini SDK attempting IPv6 on networks/containers that don't support it.
_original_getaddrinfo = socket.getaddrinfo

def _ipv4_only_getaddrinfo(*args, **kwargs):
    responses = _original_getaddrinfo(*args, **kwargs)
    return [r for r in responses if r[0] == socket.AF_INET]

socket.getaddrinfo = _ipv4_only_getaddrinfo

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


@app.middleware("http")
async def request_timer(request, call_next):
    return await log_request_time(request, call_next)


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