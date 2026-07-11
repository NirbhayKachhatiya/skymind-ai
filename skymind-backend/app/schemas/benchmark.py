from pydantic import BaseModel, Field
from typing import List, Dict, Any

class BenchmarkPrompt(BaseModel):
    prompt_id: str
    user_id: str
    query_text: str
    expected_constraints: Dict[str, Any] = Field(default_factory=dict)