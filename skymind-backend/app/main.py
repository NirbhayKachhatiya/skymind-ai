import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from app.services.data_loader import DataIntelligenceService
from app.engines.llm_engine import DirectCloudLLMEngine
from app.schemas.recommendation import RecommendedItinerary
from app.schemas.persona import TravelerPersona
from app.schemas.itinerary import ItineraryOption
# Pull the base Flight schema that your data loader successfully uses
from app.schemas.flight import Flight 

app = FastAPI(
    title="SkyMind AI: Explainable Recommendation Engine API",
    description="Production hosting tier exposing multi-ranked flight routing trade-offs with granular explanations.",
    version="1.0.0"
)

# Enable CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize global core singletons
data_service = DataIntelligenceService()
llm_engine = DirectCloudLLMEngine()

class RecommendationRequest(BaseModel):
    user_id: str
    origin: str
    destination: str

class RecommendationResponse(BaseModel):
    traveler_name: str
    origin: str
    destination: str
    metrics_applied: dict
    recommendations: List[RecommendedItinerary]

@app.get("/api/health")
def health_check():
    return {
        "status": "active",
        "engine": "Local-Explainable-Rules-Matrix",
        "word_constraint": ">=50 words"
    }

@app.post("/api/recommendations", response_model=RecommendationResponse)
def get_flight_recommendations(payload: RecommendationRequest):
    try:
        users = data_service.load_users()
        all_flights = data_service.load_flights()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data loading layer exception: {str(e)}")

    target_user = next((u for u in users if u.user_id == payload.user_id), None)
    if not target_user:
        raise HTTPException(
            status_code=404, 
            detail=f"Traveler profile matching user_id '{payload.user_id}' could not be located."
        )

    # 1. Transform categorical data tiers into functional numerical metrics
    budget_raw = str(target_user.budget_tier).lower().strip() if hasattr(target_user, 'budget_tier') and target_user.budget_tier else "medium"
    budget_map = {"high": 0.9, "medium": 0.5, "low": 0.2}
    budget_sens = budget_map.get(budget_raw, 0.5)

    # 2. Extract preferences safely
    pref_str = str(target_user.structured_preferences).lower()
    conv_prior = 0.8 if "business" in pref_str or "direct" in pref_str else 0.4
    
    # 3. Instantiate TravelerPersona with ALL Pydantic required fields
    persona = TravelerPersona(
        user_id=target_user.user_id,                         # Matches required property 1
        name=target_user.name,
        budget_sensitivity=budget_sens,
        convenience_priority=conv_prior,
        max_layovers_allowed=2 if conv_prior > 0.5 else 3,    # Matches required property 2 (Provides a safe layout ceiling)
        confidence_score=1.0                                 # Matches required property 3 (Baseline evaluation score)
    )

    matched_flights = [
        f for f in all_flights 
        if f.origin.upper() == payload.origin.upper() and f.destination.upper() == payload.destination.upper()
    ]

    if not matched_flights:
        raise HTTPException(
            status_code=404, 
            detail=f"No flight assets matching route layout {payload.origin.upper()} -> {payload.destination.upper()} found."
        )

    # Convert your clean Flight database entities straight into ItineraryOptions 
    itinerary_options = []
    for flight in matched_flights:
        option = ItineraryOption(
            flights=[flight],
            total_price=flight.price,
            total_duration_minutes=flight.duration_minutes,
            total_stops=flight.stops,
            pareto_score=0.0  # Add this required field to pass Pydantic validation!
        )
        itinerary_options.append(option)

    # Sort options out dynamically: lower cost first
    itinerary_options.sort(key=lambda x: x.total_price)

    try:
        processed_recommendations = llm_engine.generate_recommendations(persona, itinerary_options)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explainable Pipeline Exception: {str(e)}")

    return RecommendationResponse(
        traveler_name=persona.name,
        origin=payload.origin.upper(),
        destination=payload.destination.upper(),
        metrics_applied={
            "budget_sensitivity": persona.budget_sensitivity,
            "convenience_priority": persona.convenience_priority
        },
        recommendations=processed_recommendations
    )