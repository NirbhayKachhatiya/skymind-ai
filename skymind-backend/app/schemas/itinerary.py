from pydantic import BaseModel, Field
from typing import List
from app.schemas.flight import Flight

class ItineraryOption(BaseModel):
    flights: List[Flight]
    total_price: float
    total_duration_minutes: int
    total_stops: int
    pareto_score: float
    fitness_reasons: List[str] = Field(default_factory=list)