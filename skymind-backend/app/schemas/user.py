from pydantic import BaseModel, Field
from typing import List, Dict, Any

class UserProfile(BaseModel):
    user_id: str
    name: str
    structured_preferences: Dict[str, Any] = Field(default_factory=dict)
    travel_history: str
    loyalty_programs: Dict[str, str] = Field(default_factory=dict)
    budget_tier: str