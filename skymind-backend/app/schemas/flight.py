from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

class FlightBase(BaseModel):
    flight_id: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    price: float
    airline: str
    duration_minutes: int
    stops: int
    layover_airports: List[str] = Field(default_factory=list)
    season: str
    travel_date: datetime

class FlightFeatures(BaseModel):
    is_holiday_season: bool
    price_per_minute: float
    route_key: str
    day_of_week: int

class Flight(FlightBase):
    features: Optional[FlightFeatures] = None