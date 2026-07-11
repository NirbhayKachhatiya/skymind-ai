import os
import sys

# Ensure python knows where to find the 'app' module
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.services.data_loader import DataIntelligenceService

def main() -> None:
    print("=== Initializing SkyMind AI Data Intelligence Layer ===")
    service = DataIntelligenceService()
    
    # Load and test flights
    flights = service.load_flights()
    print(f" Successfully loaded {len(flights)} flight options.")
    if flights:
        sample_flight = flights[0]
        print(f"   Sample Flight: {sample_flight.flight_id} ({sample_flight.origin} -> {sample_flight.destination})")
        print(f"   Holiday Pricing Active: {sample_flight.features.is_holiday_season}")
    
    # Load and test users
    users = service.load_users()
    print(f"\n Successfully loaded {len(users)} traveler profiles.")
    if users:
        sample_user = users[0]
        print(f"   Sample User: {sample_user.name} (Budget Tier: {sample_user.budget_tier})")
        print(f"   History Segment: {sample_user.travel_history[:60]}...")

    # Load and test benchmarks
    benchmarks = service.load_benchmarks()
    print(f"\n Successfully loaded {len(benchmarks)} automated benchmark conditions.")

if __name__ == "__main__":
    main()