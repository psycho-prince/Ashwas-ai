import re
from typing import Dict, List

class SafetyGuardrails:
    def __init__(self, crisis_keywords: List[str]):
        self.crisis_keywords = crisis_keywords

    def analyze_message(self, message: str) -> Dict:
        is_crisis = any(kw in message.lower() for kw in self.crisis_keywords)
        return {"requires_emergency": is_crisis}

    def generate_safe_response(self, message: str, analysis: Dict) -> Optional[Dict]:
        if analysis["requires_emergency"]:
            return {
                "response": "🚨 EMERGENCY: Please call 911 or 988 immediately. You are not alone.",
                "is_emergency": True
            }
        return None
