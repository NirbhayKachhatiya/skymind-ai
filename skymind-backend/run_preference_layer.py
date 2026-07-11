import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.services.data_loader import DataIntelligenceService
from app.engines.preference_engine import PreferenceIntelligenceEngine

def main() -> None:
    print("=== Initializing SkyMind AI Preference Intelligence Engine ===")
    
    # 1. Load raw data assets
    data_service = DataIntelligenceService()
    users = data_service.load_users()
    
    # 2. Spin up the AI Preference Engine
    pref_engine = PreferenceIntelligenceEngine()
    
    # 3. Index raw users into behavioral personas and load into FAISS vectors
    print(f"Processing and indexing {len(users)} users into FAISS vector space...")
    pref_engine.index_user_personas(users)
    
    # 4. Extract and inspect structured persona attributes
    for user in users:
        persona = pref_engine.get_persona_by_id(user.user_id)
        if persona:
            print(f"\n[Generated Persona] ID: {persona.user_id} | Name: {persona.name}")
            print(f"   Inferred Loyalty: {persona.inferred_loyalty}")
            print(f"   Budget Sensitivity Score (0-1): {persona.budget_sensitivity}")
            print(f"   Convenience Priority Score (0-1): {persona.convenience_priority}")
            print(f"   Max Layovers Allowed: {persona.max_layovers_allowed}")
            print(f"   Hidden Directives Extracted: {persona.hidden_signals}")
            print(f"   Extraction Confidence Level: {persona.confidence_score * 100}%")

    # 5. Test semantic query matching against vector database
    test_query = "Looking for premium luxury paths with tight schedules to Tokyo"
    print(f"\n[Semantic Query Test] Searching vector space for: '{test_query}'")
    
    matched_user_id = pref_engine.query_closest_traveler_id(test_query)
    if matched_user_id:
        matched_persona = pref_engine.get_persona_by_id(matched_user_id)
        print(f"   Result: Successfully matched to User: {matched_persona.name} ({matched_user_id})")
    else:
        print("   Result: No matching user found in vector space.")

if __name__ == "__main__":
    main()