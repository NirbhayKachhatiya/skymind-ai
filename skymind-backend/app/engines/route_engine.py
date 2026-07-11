import networkx as nx
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from ortools.linear_solver import pywraplp
from app.schemas.flight import Flight
from app.schemas.persona import TravelerPersona
from app.schemas.itinerary import ItineraryOption

class RouteOptimizationEngine:
    def __init__(self, flights: List[Flight]) -> None:
        self.flights: List[Flight] = flights
        self.graph = nx.DiGraph()
        self._build_network_graph()

    def _build_network_graph(self) -> None:
        for flight in self.flights:
            self.graph.add_edge(
                flight.origin,
                flight.destination,
                flight_id=flight.flight_id,
                flight_obj=flight,
                weight=flight.price
            )

    def find_candidate_routes(self, origin: str, destination: str, max_stops: int = 2) -> List[List[Flight]]:
        all_paths: List[List[Flight]] = []
        try:
            paths = list(nx.all_simple_paths(self.graph, source=origin, target=destination, cutoff=max_stops + 1))
            for path in paths:
                path_flights = self._resolve_path_to_flights(path)
                if path_flights:
                    all_paths.extend(path_flights)
        except nx.NetworkXNoPath:
            pass
        return all_paths

    def _resolve_path_to_flights(self, path: List[str]) -> List[List[Flight]]:
        results: List[List[Flight]] = [[]]
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            edges = [data['flight_obj'] for x, y, data in self.graph.edges(data=True) if x == u and y == v]
            
            new_results = []
            for current_itinerary in results:
                for flight in edges:
                    if not current_itinerary:
                        new_results.append([flight])
                    else:
                        last_flight = current_itinerary[-1]
                        if flight.departure_time >= last_flight.arrival_time + timedelta(minutes=45):
                            new_results.append(current_itinerary + [flight])
            results = new_results
        return [r for r in results if r]

    def optimize_itineraries(self, origin: str, destination: str, persona: TravelerPersona) -> List[ItineraryOption]:
        candidates = self.find_candidate_routes(origin, destination, max_stops=persona.max_layovers_allowed)
        if not candidates:
            return []

        solver = pywraplp.Solver.CreateSolver('GLOP')
        if not solver:
            return []

        variables = []
        for i in range(len(candidates)):
            variables.append(solver.NumVar(0.0, 1.0, f'path_{i}'))

        solver.Add(solver.Sum(variables) == 1.0)

        ranked_options = []
        for idx, path in enumerate(candidates):
            total_price = sum(f.price for f in path)
            total_duration = sum(f.duration_minutes for f in path)
            total_stops = len(path) - 1

            if total_stops > persona.max_layovers_allowed:
                continue

            airline_bonus = 0.0
            for f in path:
                if f.airline in persona.preferred_carriers:
                    airline_bonus += 150.0

            cost_component = total_price * persona.budget_sensitivity
            convenience_component = (total_duration + (total_stops * 180)) * persona.convenience_priority * 2.0
            preference_discount = airline_bonus * persona.convenience_priority

            fitness_score = cost_component + convenience_component - preference_discount

            reasons = [
                f"Base price asset matching: ${total_price}",
                f"Aggregated elapsed transit windows: {total_duration} mins"
            ]
            if airline_bonus > 0:
                reasons.append("Aligned with traveler brand affinity parameters")

            ranked_options.append(ItineraryOption(
                flights=path,
                total_price=total_price,
                total_duration_minutes=total_duration,
                total_stops=total_stops,
                pareto_score=float(fitness_score),
                fitness_reasons=reasons
            ))

        ranked_options.sort(key=lambda x: x.pareto_score)
        return ranked_options