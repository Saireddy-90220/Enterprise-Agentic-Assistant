import requests
import json

def fetch_external_data(query: str):
    """
    Mock function to simulate fetching data from a live Enterprise REST API.
    In a real scenario, this would dynamically hit endpoints based on the query.
    """
    print(f"--- API AGENT FETCHING LIVE DATA FOR: {query} ---")
    
    # We simulate a "live" API response based on keywords
    query_lower = query.lower()
    
    if "stock" in query_lower or "market" in query_lower:
         return json.dumps({
             "symbol": "ACME",
             "current_price": 145.67,
             "day_change": "+2.34%",
             "volume": "1.2M",
             "status": "Market Open"
         })
    
    if "weather" in query_lower or "supply chain" in query_lower:
        return json.dumps({
            "location": "Global Logistics Hub (Frankfurt)",
            "condition": "Severe Thunderstorms",
            "impact_warning": "High probability of flight delays affecting Q3 shipping SLAs."
        })
        
    return json.dumps({
        "status": "success",
        "data_source": "Enterprise Services API",
        "message": "No specific live endpoint matched. Defaulting to standard operational status: GREEN."
    })
