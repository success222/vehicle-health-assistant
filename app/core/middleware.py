import time

from fastapi import Request

from app.core.logger import logger


async def log_request_time(request: Request, call_next):

    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        f"{request.method} {request.url.path} "
        f"completed in {duration:.2f}s"
    )

    return response