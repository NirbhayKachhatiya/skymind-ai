from pydantic import BaseModel, Field
from typing import List, Dict, Any

class TravelerPersona(BaseModel) :
    user_id: str
    name: str
    inferred_loyalty: List[str] = Field(default_factory=list)
    budget_sensitivity: float = Field(..., description="Value between 0.0 (unlimited budget) and 1.0 (extremely price sensitive)")
    convenience_priority: float = Field(..., description="Value between 0.0 (tolerates high friction) and 1.0 (demands direct/luxury paths)")
    max_layovers_allowed: int
    preferred_carriers: List[str] = Field(default_factory=list)
    hidden_signals: List[str] = Field(default_factory=list)
    confidence_score: float