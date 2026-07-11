import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.services.data_loader import DataIntelligenceService
from app.engines.preference_engine import PreferenceIntelligenceEngine
from app.engines.route_engine import RouteOptimizationEngine

def main() -> None:
    print("=== Initializing SkyMind AI Route Optimization Engine ===")
    
    data_service = DataIntelligenceService()
    flights = data_service.load_flights()
    users = data_service.load_users()
    
    if not users:
        print("CRITICAL: No users found in user_data.csv. Exiting.")
        return
        
    pref_engine = PreferenceIntelligenceEngine()
    pref_engine.index_user_personas(users)
    
    router = RouteOptimizationEngine(flights)
    print(f"NetworkX graph assembled with {router.graph.number_of_nodes()} airport nodes and {router.graph.number_of_edges()} route links.")
    
    first_user_id = users[0].user_id
    traveler_persona = pref_engine.get_persona_by_id(first_user_id)
    
    print(f"\nEvaluating Route Matrices for {traveler_persona.name} (Max Layovers: {traveler_persona.max_layovers_allowed})...")
    
    sample_flight = flights[0]
    origin_airport = sample_flight.origin
    dest_airport = sample_flight.destination
    
    print(f"Attempting route optimization from: {origin_airport} -> {dest_airport}")
    
    itineraries = router.optimize_itineraries(origin=origin_airport, destination=dest_airport, persona=traveler_persona)
    
    if not itineraries:
        print(f"No valid paths found for constraints between {origin_airport} and {dest_airport}.")
        return
        
    for index, option in enumerate(itineraries[:3]):
        print(f"\n[Ranked Option #{index + 1}] Pareto Selection Score: {option.pareto_score:.2f}")
        print(f"   Stops: {option.total_stops} | Price: ${option.total_price} | Duration: {option.total_duration_minutes} mins")
        for f in option.flights:
            print(f"     Segment: {f.flight_id} | {f.origin} -> {f.destination} via {f.airline}")
        print(f"   Telemetry Signals: {option.fitness_reasons}")

if __name__ == "__main__":
    main()