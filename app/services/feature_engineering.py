# Imports
from datetime import date

from app.config.thresholds import (
    HIGH_MILEAGE_THRESHOLD,
    SERVICE_INTERVAL_MONTHS,
    OIL_CHANGE_INTERVAL_MONTHS,
    BRAKE_INSPECTION_INTERVAL_MONTHS,
    BATTERY_REPLACEMENT_INTERVAL_MONTHS,
    COOLANT_CHANGE_INTERVAL_MONTHS,
)

from app.schemas import vehicle
from app.schemas.vehicle import VehicleRequest

from typing import Dict, Any

# create helper function
def calculate_months_since(date_value):
    """
    Calculate the number of whole calendar months since a given date.

    Args:
        date_value (date | None): The date to calculate from.

    Returns:
        int | None: Number of months since the given date, or None if
        date_value is None.
    """
    if date_value is None:
        return None

    today = date.today()
    months_since = (
        (today.year - date_value.year) * 12
        + (today.month - date_value.month)
    )

    return months_since

# create the engineering function
def engineer_features(vehicle: VehicleRequest) -> Dict[str, Any]:
    today = date.today()

    vehicle_age = (
        today.year - vehicle.year
    )

    high_mileage = vehicle.mileage >= HIGH_MILEAGE_THRESHOLD

    mileage_per_year = vehicle.mileage / max(vehicle_age, 1)
    
    months_since_service = calculate_months_since(
        vehicle.last_service_date
    )

    months_since_brake = calculate_months_since(
        vehicle.brake_installation_date
    )

    months_since_battery = calculate_months_since(
        vehicle.battery_installation_date
    )

    months_since_oil = calculate_months_since(
        vehicle.last_oil_change_date
    )

    months_since_coolant = calculate_months_since(
        vehicle.last_coolant_change_date
    )
    
    # compute boolean flags for maintenance needs
    service_overdue = (
    months_since_service is not None
    and months_since_service >= SERVICE_INTERVAL_MONTHS
    )

    oil_change_due = (
        months_since_oil is not None
        and months_since_oil >= OIL_CHANGE_INTERVAL_MONTHS
    )

    battery_check_due = (
        months_since_battery is not None
        and months_since_battery >= BATTERY_REPLACEMENT_INTERVAL_MONTHS
    )

    brake_inspection_due = (
        months_since_brake is not None
        and months_since_brake >= BRAKE_INSPECTION_INTERVAL_MONTHS
    )

    coolant_change_due = (
        months_since_coolant is not None
        and months_since_coolant >= COOLANT_CHANGE_INTERVAL_MONTHS
    )
    
    return {
    "vehicle_age": vehicle_age,
    "high_mileage": high_mileage,
    "mileage_per_year": round(mileage_per_year, 2),
    "months_since_service": months_since_service,
    "months_since_brake": months_since_brake,
    "months_since_battery": months_since_battery,
    "months_since_oil": months_since_oil,
    "months_since_coolant": months_since_coolant,
    "service_overdue": service_overdue,
    "oil_change_due": oil_change_due,
    "battery_check_due": battery_check_due,
    "brake_inspection_due": brake_inspection_due,
    "coolant_change_due": coolant_change_due,
}