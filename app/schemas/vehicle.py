# import necessary modules
from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator

# Enumeration for driving patterns and fuel types
class DrivingPattern(str, Enum):
    SHORT = "Short Trips"
    MEDIUM = "Medium Trips"
    LONG = "Long Trips"


class FuelType(str, Enum):
    PETROL = "Petrol"
    DIESEL = "Diesel"
    HYBRID = "Hybrid"
    ELECTRIC = "Electric"
    
# class for vehicle
class VehicleRequest(BaseModel):
    make: str = Field(
        
        ...,
        min_length=1,
        description="The make of the vehicle (e.g., Toyota, Ford, BMW).",
        examples=["Toyota"]
    )
    model: str = Field(
        ...,
        min_length=1,
        description="The model of the vehicle (e.g., Camry, F-150, 3 Series).",
        examples=["Camry"]
    )
    year: int = Field(
        ...,
        ge=1886,  # The year the first automobile was invented
        le=date.today().year,  # The current year
        description="The year the vehicle was manufactured.",
        examples=[2020]
    )
    mileage: int = Field(
        ...,
        gt=0,
        description="The current mileage of the vehicle in kilometers.",
        examples=[15000]
    )
    driving_pattern: DrivingPattern = Field(
        ...,
        description="The typical driving pattern of the vehicle.",
        examples=[DrivingPattern.SHORT]
    )
    fuel_type: FuelType = Field(
        ...,
        description="The type of fuel the vehicle uses.",
        examples=[FuelType.PETROL]
    )
    last_service_date: Optional[date] = Field(
        default=None,
        description="The date when the vehicle was last serviced.",
        examples=["2023-01-15"]
    )
    brake_installation_date: Optional[date] = Field(
        default=None,
        description="The date when the brakes were last installed or serviced.",
        examples=["2023-01-15"]
    )
    battery_installation_date: Optional[date] = Field(
        default=None,
        description="The date when the battery was last installed or serviced.",
        examples=["2023-01-15"]
    )
    last_oil_change_date: Optional[date] = Field(
        default=None,
        description="The date when the oil was last changed.",
        examples=["2023-01-15"]
    )
    last_coolant_change_date: Optional[date] = Field(
        default=None,
        description="The date when the coolant was last changed.",
        examples=["2023-01-15"]
    )
    # Validators to ensure the right input from the user
    @field_validator("make", "model")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()
        
        if not value.strip():
            raise ValueError("Make and model cannot be empty")
        
        return value
    
    # Validate to ensure the year is not in the future
    @field_validator("year")
    @classmethod
    def validate_year(cls, value: int) -> int:
        current_year = date.today().year
        
        if value > current_year:
            raise ValueError(f"Manufacturing year cannot be in the future. Current year is {current_year}.")
        return value
    
    # validate dates to ensure they are today or earlier
    @field_validator(
        "last_service_date",
        "brake_installation_date",
        "battery_installation_date",
        "last_oil_change_date",
        "last_coolant_change_date"
    )
    @classmethod
    def validate_dates(cls, value: Optional[date]) -> Optional[date]:
        if value is None:
            return value
        
        if value > date.today():
            raise ValueError("Date cannot be in the future.")
        
        return value