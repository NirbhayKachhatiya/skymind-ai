import os
import json
import csv
from datetime import datetime
from typing import List, Dict, Any
from app.core.config import settings
from app.schemas.flight import Flight, FlightFeatures
from app.schemas.user import UserProfile
from app.schemas.benchmark import BenchmarkPrompt

class DataIntelligenceService:
    def __init__(self) -> None:
        self.data_dir: str = settings.DATA_DIR
        self._ensure_mock_data_exists()

    def _ensure_mock_data_exists(self) -> None:
        os.makedirs(self.data_dir, exist_ok=True)
        flights_path = os.path.join(self.data_dir, "flights_data.csv")
        users_path = os.path.join(self.data_dir, "user_data.csv")
        benchmark_path = os.path.join(self.data_dir, "benchmark_prompts.json")

        if not os.path.exists(flights_path):
            with open(flights_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["flight_id", "origin", "destination", "departure_time", "arrival_time", "price", "airline", "duration_minutes", "stops", "layover_airports", "season", "travel_date"])
                writer.writerow(["FL001", "JFK", "LAX", "2026-12-20T08:00:00", "2026-12-20T11:30:00", "450.0", "Delta", "330", "0", "", "Winter-Peak", "2026-12-20"])
                writer.writerow(["FL002", "JFK", "LHR", "2026-07-15T18:00:00", "2026-07-16T06:30:00", "850.0", "British Airways", "450", "1", "CDG", "Summer-Peak", "2026-07-15"])
                writer.writerow(["FL003", "LAX", "NRT", "2026-10-05T11:00:00", "2026-10-06T15:00:00", "920.0", "Japan Airlines", "660", "0", "", "Autumn-OffPeak", "2026-10-05"])

        if not os.path.exists(users_path):
            with open(users_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["user_id", "name", "structured_preferences", "travel_history", "loyalty_programs", "budget_tier"])
                writer.writerow(["USR-001", "Alex Mercer", '{"preferred_class": "Business", "max_layovers": 0}', "Prefers luxury travel. Traveled to Tokyo last autumn and explicitly requested direct flights only due to tight schedules. Dissatisfied with airline meals on standard carriers.", '{"Delta": "Gold Medallion", "Japan Airlines": "Emerald"}', "Premium"])
                writer.writerow(["USR-002", "Elena Rostova", '{"preferred_class": "Economy", "max_layovers": 2}', "Backpacker style. Constantly hunting for lowest pricing parameters across Europe. Tolerates long overnight structural layovers if saving exceeds 150 dollars.", '{"Ryanair": "Basic"}', "Budget"])

        if not os.path.exists(benchmark_path):
            benchmark_data = [
                {
                    "prompt_id": "BM-001",
                    "user_id": "USR-001",
                    "query_text": "Find me a direct and highly comfortable flight itinerary from JFK to Tokyo area endpoints during winter season.",
                    "expected_constraints": {"direct_only": True, "premium_tier": True}
                }
            ]
            with open(benchmark_path, mode="w", encoding="utf-8") as f:
                json.dump(benchmark_data, f, indent=4)

    def load_flights(self) -> List[Flight]:
        flights: List[Flight] = []
        path = os.path.join(self.data_dir, "flights_data.csv")
        with open(path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                layovers = [x.strip() for x in row["layover_airports"].split(",")] if row["layover_airports"] else []
                dep_time = datetime.fromisoformat(row["departure_time"])
                arr_time = datetime.fromisoformat(row["arrival_time"])
                travel_dt = datetime.fromisoformat(row["travel_date"])
                
                price = float(row["price"])
                duration = int(row["duration_minutes"])
                
                is_holiday = "Peak" in row["season"] or dep_time.month in [7, 8, 12]
                price_per_min = price / duration if duration > 0 else 0.0
                route = f"{row['origin']}-{row['destination']}"
                
                features = FlightFeatures(
                    is_holiday_season=is_holiday,
                    price_per_minute=price_per_min,
                    route_key=route,
                    day_of_week=dep_time.weekday()
                )
                
                flight = Flight(
                    flight_id=row["flight_id"],
                    origin=row["origin"],
                    destination=row["destination"],
                    departure_time=dep_time,
                    arrival_time=arr_time,
                    price=price,
                    airline=row["airline"],
                    duration_minutes=duration,
                    stops=int(row["stops"]),
                    layover_airports=layovers,
                    season=row["season"],
                    travel_date=travel_dt,
                    features=features
                )
                flights.append(flight)
        return flights

    def load_users(self) -> List[UserProfile]:
        users: List[UserProfile] = []
        path = os.path.join(self.data_dir, "user_data.csv")
        with open(path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                user = UserProfile(
                    user_id=row["user_id"],
                    name=row["name"],
                    structured_preferences=json.loads(row["structured_preferences"]),
                    travel_history=row["travel_history"],
                    loyalty_programs=json.loads(row["loyalty_programs"]),
                    budget_tier=row["budget_tier"]
                )
                users.append(user)
        return users

    def load_benchmarks(self) -> List[BenchmarkPrompt]:
        path = os.path.join(self.data_dir, "benchmark_prompts.json")
        with open(path, mode="r", encoding="utf-8") as f:
            data = json.load(f)
        return [BenchmarkPrompt(**item) for item in data]