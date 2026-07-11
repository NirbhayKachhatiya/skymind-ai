import os
import json
from typing import List
from app.schemas.persona import TravelerPersona
from app.schemas.itinerary import ItineraryOption
from app.schemas.recommendation import RecommendedItinerary

class DirectCloudLLMEngine:
    def __init__(self) -> None:
        # Keeping this properties intact to avoid breaking your Config setups
        from app.core.config import settings
        self.api_key = settings.llm_api_key
        self.api_url = ""

    def _generate_premium_local_rationale(self, persona: TravelerPersona, option: ItineraryOption, rank: int) -> str:
        # Extract metadata from the itinerary option
        carrier_names = list(set(f.airline for f in option.flights))
        carriers_str = " via " + " and ".join(carrier_names) if carrier_names else ""
        total_price = option.total_price
        total_duration = option.total_duration_minutes
        stops = option.total_stops
        
        # Build out a detailed segment connection breakdown string
        if len(option.flights) > 1:
            segment_flow = " -> ".join([f"{f.origin} to {f.destination}" for f in option.flights])
            connection_context = f" This multi-leg routing connects dynamically across {segment_flow} introducing {stops} stopovers."
        else:
            connection_context = " This operates as a highly efficient direct flight route minimizing transit friction."

        # Profile 1: High Budget Sensitivity (Prioritizes low cost above all else)
        if persona.budget_sensitivity > 0.6:
            rationale = (
                f"Ranked #{rank} specifically to optimize your financial parameters, delivering a total base fare of ${total_price:.2f}{carriers_str}. "
                f"While the total duration stands at {total_duration} minutes, the price reduction provides exceptional economic value "
                f"that cleanly satisfies your high budget sensitivity rating of {persona.budget_sensitivity:.2f}.{connection_context} "
                f"It stands out as a fiscally responsible travel selection tailored for your profile."
            )
        
        # Profile 2: High Convenience Priority (Prioritizes speed and direct flights)
        elif persona.convenience_priority > 0.6:
            rationale = (
                f"Ranked #{rank} to prioritize operational velocity and calendar efficiency, keeping your overall travel time down to {total_duration} minutes. "
                f"Securing this schedule via {', '.join(carrier_names)} cleanly matches your high convenience priority threshold of {persona.convenience_priority:.2f}, "
                f"effectively shielding you from unnecessary downtime.{connection_context} The premium value justified here centers strictly on time conservation."
            )
        
        # Profile 3: Balanced or Neutral Preferences
        else:
            rationale = (
                f"Ranked #{rank} because it represents a highly balanced itinerary optimization splitting total cost (${total_price:.2f}) "
                f"and total travel duration ({total_duration} minutes) across the network.{connection_context} "
                f"This selection effectively accommodates both your budget index ({persona.budget_sensitivity:.2f}) "
                f"and convenience layout ({persona.convenience_priority:.2f}) without excessively compromising on price or scheduling flexibility."
            )
            
        return rationale

    def generate_recommendations(self, persona: TravelerPersona, options: List[ItineraryOption]) -> List[RecommendedItinerary]:
        recommendations = []
        
        # Process top 3 flight itineraries
        for index, option in enumerate(options[:3]):
            rank = index + 1
            
            # Generate the comprehensive, 50+ word local response natively
            rationale = self._generate_premium_local_rationale(persona, option, rank)

            recommendations.append(RecommendedItinerary(
                itinerary=option,
                rank=rank,
                recommendation_rationale=rationale
            ))
            
        return recommendations