import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.services.data_loader import DataIntelligenceService
from app.engines.preference_engine import PreferenceIntelligenceEngine
from app.engines.route_engine import RouteOptimizationEngine
from app.engines.llm_engine import DirectCloudLLMEngine

def main() -> None:
    print("=== Initializing SkyMind AI Explainable Recommendation Pipeline ===")
    
    data_service = DataIntelligenceService()
    flights = data_service.load_flights()
    users = data_service.load_users()
    
    if not users:
        print("CRITICAL: No users loaded.")
        return
        
    pref_engine = PreferenceIntelligenceEngine()
    pref_engine.index_user_personas(users)
    
    traveler_id = users[0].user_id
    persona = pref_engine.get_persona_by_id(traveler_id)
    
    sample_flight = flights[10]
    origin = sample_flight.origin
    destination = sample_flight.destination
    
    print(f"\nTarget Traveler Persona: {persona.name}")
    print(f"Target Route Constraints: {origin} -> {destination}")
    
    router = RouteOptimizationEngine(flights)
    optimized_itineraries = router.optimize_itineraries(origin=origin, destination=destination, persona=persona)
    
    if not optimized_itineraries:
        print("No paths could be resolved between targets.")
        return
        
    xai_engine = DirectCloudLLMEngine()
    recommendations = xai_engine.generate_recommendations(persona, optimized_itineraries)
    
    print("\n--- Final Recommendation Output Pack ---")
    for rec in recommendations:
        print(f"\n[RANK {rec.rank}] Flight Cost: ${rec.itinerary.total_price:.2f} | Total Time: {rec.itinerary.total_duration_minutes} mins")
        for f in rec.itinerary.flights:
            print(f"   Flight segment: {f.flight_id} ({f.origin} -> {f.destination} via {f.airline})")
        print(f"💡 Rationale: {rec.recommendation_rationale}")

if __name__ == "__main__":
    main()