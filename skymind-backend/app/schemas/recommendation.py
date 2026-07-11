from pydantic import BaseModel, Field
from typing import List
from app.schemas.itinerary import ItineraryOption

class RecommendedItinerary(BaseModel):
    itinerary: ItineraryOption
    rank: int
    recommendation_rationale: str = Field(..., description="Natural language explanation of structural trade-offs.")