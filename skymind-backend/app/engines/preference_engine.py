import os
import json
import numpy as np
import faiss
from typing import List, Dict, Any, Optional
from app.schemas.user import UserProfile
from app.schemas.persona import TravelerPersona
from app.engines.embeddings import LocalDeterministicEmbedder

class PreferenceIntelligenceEngine:
    def __init__(self) -> None:
        self.embedder = LocalDeterministicEmbedder(dimension=1536)
        self.index = faiss.IndexFlatL2(1536)
        self.user_map: Dict[int, str] = {}
        self.persona_store: Dict[str, TravelerPersona] = {}

    def build_persona(self, user: UserProfile) -> TravelerPersona:
        history_lower = user.travel_history.lower()
        
        inferred_loyalty = []
        for carrier in ["delta", "united", "emirates", "lufthansa", "ryanair", "british airways", "japan airlines"]:
            if carrier in history_lower:
                inferred_loyalty.append(carrier.title())

        try:
            budget_sensitivity = float(user.budget_tier)
        except ValueError:
            budget_sensitivity = 0.9 if "high" in user.budget_tier.lower() else 0.3

        convenience_priority = 0.5
        if "direct" in history_lower or "tight schedule" in history_lower:
            convenience_priority = 0.95
        elif "layover" in history_lower:
            convenience_priority = 0.2

        max_layovers = 2
        if "direct" in history_lower:
            max_layovers = 0

        hidden_signals = []
        if "catering" in history_lower or "meals" in history_lower:
            hidden_signals.append("In-flight catering optimization target")

        persona = TravelerPersona(
            user_id=user.user_id,
            name=user.name,
            inferred_loyalty=inferred_loyalty,
            budget_sensitivity=budget_sensitivity,
            convenience_priority=convenience_priority,
            max_layovers_allowed=max_layovers,
            preferred_carriers=inferred_loyalty.copy(),
            hidden_signals=hidden_signals,
            confidence_score=0.90
        )
        
        self.persona_store[user.user_id] = persona
        return persona

    def index_user_personas(self, users: List[UserProfile]) -> None:
        vectors = []
        for idx, user in enumerate(users):
            persona = self.build_persona(user)
            semantic_text = f"Traveler {persona.name}. Budget: {persona.budget_sensitivity}. History: {user.travel_history}"
            vector = self.embedder.embed_query(semantic_text)
            vectors.append(vector)
            self.user_map[idx] = user.user_id
            
        if vectors:
            np_vectors = np.array(vectors).astype('float32')
            self.index.add(np_vectors)

    def query_closest_traveler_id(self, query_text: str) -> Optional[str]:
        if self.index.ntotal == 0:
            return None
        query_vector = np.array([self.embedder.embed_query(query_text)]).astype('float32')
        _, indices = self.index.search(query_vector, 1)
        matched_idx = indices[0][0]
        if matched_idx in self.user_map:
            return self.user_map[matched_idx]
        return None

    def get_persona_by_id(self, user_id: str) -> Optional[TravelerPersona]:
        return self.persona_store.get(user_id)