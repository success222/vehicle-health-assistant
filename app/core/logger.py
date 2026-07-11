import logging
from pathlib import Path

# Create logs directory if it doesn't exist
Path("logs").mkdir(exist_ok=True)

logger = logging.getLogger("vehicle_health")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# File handler
file_handler = logging.FileHandler(
    "logs/app.log",
    encoding="utf-8"
)
file_handler.setFormatter(formatter)

logger.handlers.clear()
logger.addHandler(console_handler)
logger.addHandler(file_handler)