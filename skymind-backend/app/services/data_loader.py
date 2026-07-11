import os
import json
import csv
from datetime import datetime
from typing import List, Dict, Any
from app.core.config import settings
from app.schemas.flight import Flight, FlightFeatures
from app.schemas.user import UserProfile
from app.schemas.benchmark import BenchmarkPrompt
from pathlib import Path

class DataIntelligenceService:
    def __init__(self) -> None:
        self.data_dir: str = settings.DATA_DIR

    def _normalize_key(self, row: Dict[str, Any], target_key: str) -> str:
        aliases: Dict[str, List[str]] = {
            "departure_time": ["departure_time", "departure_utc", "dep_time"],
            "arrival_time": ["arrival_time", "arrival_utc", "arr_time"],
            "travel_date": ["travel_date", "date"],
            "travel_history": ["travel_history", "raw_history", "history"],
            "structured_preferences": ["structured_preferences", "preferences"],
            "loyalty_programs": ["loyalty_programs", "frequent_flyer", "loyalty"],
            "budget_tier": ["budget_tier", "price_sensitivity"]
        }
        
        target_lower = target_key.lower()
        search_terms = aliases.get(target_lower, [target_lower])
        
        for k in row.keys():
            normalized_header = k.lower().replace(" ", "_").replace("-", "_")
            if normalized_header in search_terms or normalized_header == target_lower:
                return row[k]
                
        if target_key == "travel_date":
            try:
                dep_val = self._normalize_key(row, "departure_time")
                return dep_val.split("T")[0]
            except KeyError:
                pass
                
        if target_key == "name":
            return row.get("user_id", "Unknown Traveler")
            
        if target_key == "structured_preferences":
            return json.dumps({
                "preferred_cabin": row.get("preferred_cabin", ""),
                "direct_preference": row.get("direct_preference", ""),
                "max_layover_minutes": row.get("max_layover_minutes", "")
            })
            
        raise KeyError(f"Could not resolve structural column mapping for: '{target_key}' in CSV headers: {list(row.keys())}")

    def load_flights(self) -> List[Flight]:
        flights: List[Flight] = []
        project_root = Path(__file__).resolve().parent.parent.parent
        path = project_root / "data" / "flights_data.csv" 

        if not os.path.exists(path):
            print(f"\n⚠️ File hunting check! Looking at: {os.path.abspath(path)}")
            path = project_root / "flights_data.csv"
        
        with open(path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                flight_id = self._normalize_key(row, "flight_id")
                origin = self._normalize_key(row, "origin")
                destination = self._normalize_key(row, "destination")
                dep_str = self._normalize_key(row, "departure_time")
                arr_str = self._normalize_key(row, "arrival_time")
                price_str = self._normalize_key(row, "price")
                airline = row.get("airline_name") or row.get("airline") or self._normalize_key(row, "airline_name")
                dur_str = self._normalize_key(row, "duration_minutes")
                stops_str = self._normalize_key(row, "stops")
                layover_str = self._normalize_key(row, "layover_airports")
                season = self._normalize_key(row, "season")
                travel_str = self._normalize_key(row, "travel_date")

                layovers = [x.strip() for x in layover_str.split(",")] if layover_str else []
                dep_time = datetime.fromisoformat(dep_str.replace("Z", ""))
                arr_time = datetime.fromisoformat(arr_str.replace("Z", ""))
                
                if " " in travel_str:
                    travel_str = travel_str.split(" ")[0]
                elif "T" in travel_str:
                    travel_str = travel_str.split("T")[0]
                travel_dt = datetime.strptime(travel_str, "%Y-%m-%d")
                
                price = float(price_str)
                duration = int(dur_str)
                
                is_holiday = "Peak" in season or dep_time.month in [7, 8, 12]
                price_per_min = price / duration if duration > 0 else 0.0
                route = f"{origin}-{destination}"
                
                features = FlightFeatures(
                    is_holiday_season=is_holiday,
                    price_per_minute=price_per_min,
                    route_key=route,
                    day_of_week=dep_time.weekday()
                )
                
                flight = Flight(
                    flight_id=flight_id,
                    origin=origin,
                    destination=destination,
                    departure_time=dep_time,
                    arrival_time=arr_time,
                    price=price,
                    airline=airline,
                    duration_minutes=duration,
                    stops=int(stops_str),
                    layover_airports=layovers,
                    season=season,
                    travel_date=travel_dt,
                    features=features
                )
                flights.append(flight)
        return flights

    def load_users(self) -> List[UserProfile]:
        users: List[UserProfile] = []
        project_root = Path(__file__).resolve().parent.parent.parent
        path = project_root / "data" / "user_data.csv"

        if not os.path.exists(path):
            path = project_root / "users_data.csv"

        with open(path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                user_id = self._normalize_key(row, "user_id")
                name = self._normalize_key(row, "name")
                struct_pref = self._normalize_key(row, "structured_preferences")
                history = self._normalize_key(row, "travel_history")
                loyalty = self._normalize_key(row, "loyalty_programs")
                budget = self._normalize_key(row, "budget_tier")

                user = UserProfile(
                    user_id=user_id,
                    name=name,
                    structured_preferences=json.loads(struct_pref) if isinstance(struct_pref, str) and struct_pref.startswith("{") else {},
                    travel_history=history,
                    loyalty_programs=json.loads(loyalty) if isinstance(loyalty, str) and loyalty.startswith("{") else {"programs": loyalty},
                    budget_tier=budget
                )
                users.append(user)
        return users

    def load_benchmarks(self) -> List[BenchmarkPrompt]:
        path = os.path.join(self.data_dir, "benchmark_prompts.json")
        with open(path, mode="r", encoding="utf-8") as f:
            data = json.load(f)
        return [BenchmarkPrompt(**item) for item in data]