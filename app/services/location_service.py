"""
Location-based services for Ashwas AI
Detects user location and provides localized emergency contacts
"""

import os
from typing import Dict, Optional, List
from datetime import datetime

class LocationService:
    """Handles user location detection and regional customization"""
    
    def __init__(self):
        # Simplified regional data for MVP/Main challenge submission
        self.regional_data = {
            "US": {
                "name": "United States",
                "emergency": {"police": {"number": "911", "label": "Emergency Services"}},
                "crisis_lines": {"suicide": {"number": "988", "label": "Suicide & Crisis Lifeline"}},
                "substance_use": {"samhsa": {"number": "1-800-662-4357", "label": "SAMHSA National Helpline"}}
            },
            "IN": {
                "name": "India",
                "emergency": {"police": {"number": "112", "label": "Emergency Services (PAN-India)"}},
                "crisis_lines": {"suicide": {"number": "9152987821", "label": "iCall Helpline"}},
                "substance_use": {"nasha_mukt": {"number": "14446", "label": "Nasha Mukt Bharat Helpline"}}
            }
        }
        self.default_region = "US"
        
    def get_regional_contacts(self, region_code: str) -> Dict:
        """Get emergency and support contacts for a region"""
        region_data = self.regional_data.get(region_code, self.regional_data[self.default_region])
        return {
            "region_name": region_data["name"],
            "emergency": region_data.get("emergency", {}),
            "crisis_lines": region_data.get("crisis_lines", {}),
            "substance_use": region_data.get("substance_use", {})
        }
