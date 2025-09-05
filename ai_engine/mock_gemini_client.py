"""
Mock Gemini Client for Testing
This module provides mock responses for testing without actual Gemini AI API calls.
"""

import json
import random
from typing import Dict, Any, Optional

class MockGeminiClient:
    """Mock Gemini client that returns realistic responses for testing"""
    
    def __init__(self):
        self.call_count = 0
        self.mock_responses = self._load_mock_responses()
    
    def _load_mock_responses(self) -> Dict[str, Any]:
        """Load predefined mock responses for different agent types"""
        return {
            "intent_analyst": {
                "tone": "mysterious and atmospheric",
                "style": "noir detective fiction",
                "character_voice": "cynical but determined detective",
                "setting_atmosphere": "foggy coastal town with hidden secrets",
                "narrative_perspective": "first-person detective perspective"
            },
            
            "scene_scout": {
                "plot_points": [
                    "The detective arrives at the foggy coastal town to investigate the disappearance",
                    "The detective interviews locals and discovers the lighthouse keeper had secrets",
                    "The detective uncovers a pattern of disappearances every decade",
                    "The detective realizes the town is hiding something sinister"
                ],
                "search_queries": [
                    "foggy coastal town detective investigation atmosphere",
                    "lighthouse keeper mysterious disappearance small town secrets",
                    "pattern of disappearances every decade coastal community",
                    "town hiding dark secrets detective noir atmosphere"
                ]
            },
            
            "style_analyst": {
                "genre_style_guide": """GENRE STYLE GUIDE: Noir Detective Fiction

TONE GUIDELINES:
- Dark, moody, and atmospheric
- Cynical worldview with underlying hope
- Suspenseful and mysterious
- Gritty realism with poetic descriptions

CONVENTIONS AND TROPES:
- Hard-boiled detective protagonist
- Small town with dark secrets
- Atmospheric weather (fog, rain, night)
- Layered mysteries unfolding
- Moral ambiguity

WRITING TECHNIQUES:
- First-person narrative
- Vivid sensory descriptions
- Metaphorical language
- Building tension through pacing
- Character-driven plot development""",
                "key_elements": ["atmosphere", "mystery", "character development", "suspense"]
            },
            
            "master_weaver": {
                "sections": [
                    "The fog rolled in thick as I stepped out of my car, coating the coastal town in a gray shroud that seemed to swallow sound and light alike. Three days missing, they said. The lighthouse keeper. Last seen walking toward the cliffs, never returned.",
                    
                    "I knocked on doors, asked questions. The locals had that look - you know the one. Eyes darting, voices hushed. Everyone knew something, no one wanted to talk. 'Check the old records,' one woman whispered before closing her door.",
                    
                    "In the town hall basement, I found them. Newspaper clippings going back fifty years. Same story, different names. Every ten years, someone vanishes. Always in winter. Always during the fog.",
                    
                    "That's when I understood. This town wasn't just hiding a missing person. It was hiding a pattern, a ritual, something that had been happening long before I arrived. And I was about to become part of it."
                ]
            },
            
            "correction_polish": {
                "corrected_text": "The fog rolled in thick as I stepped out of my car, coating the coastal town in a gray shroud that seemed to swallow both sound and light. Three days missing, they told me. The lighthouse keeper. Last seen walking toward the cliffs, never to return.\n\nI knocked on doors and asked questions. The locals had that look—you know the one. Eyes darting, voices hushed. Everyone knew something; no one wanted to talk. 'Check the old records,' one woman whispered before closing her door.\n\nIn the town hall basement, I found them. Newspaper clippings going back fifty years. Same story, different names. Every ten years, someone vanishes. Always in winter. Always during the fog.\n\nThat's when I understood. This town wasn't just hiding a missing person. It was hiding a pattern—a ritual—something that had been happening long before I arrived. And I was about to become part of it.",
                "improvements": ["grammar", "flow", "punctuation", "clarity"]
            },
            
            "character_extractor": {
                "characters": [
                    {
                        "name": "Detective",
                        "description": "The main protagonist investigating the disappearance",
                        "personality": "Cynical, determined, observant",
                        "first_appearance": "Arrives at the coastal town to investigate"
                    },
                    {
                        "name": "Lighthouse Keeper",
                        "description": "The missing person whose disappearance triggers the investigation",
                        "personality": "Mysterious, possibly knew town secrets",
                        "first_appearance": "Mentioned as missing person"
                    }
                ]
            },
            
            "lore_master": {
                "lore_entries": [
                    {
                        "category": "location",
                        "name": "Coastal Town",
                        "description": "Small town with a dark secret of periodic disappearances",
                        "significance": "Setting for the mystery and keeper of secrets"
                    },
                    {
                        "category": "concept",
                        "name": "The Pattern",
                        "description": "Disappearances occurring every decade for 50 years",
                        "significance": "Central mystery that drives the investigation"
                    }
                ]
            }
        }
    
    def generate_content(self, prompt: str, **kwargs) -> str:
        """Generate mock content based on the prompt"""
        self.call_count += 1
        
        # Determine which agent is calling based on prompt content
        prompt_lower = prompt.lower()
        
        if "intent" in prompt_lower or "tone" in prompt_lower:
            return json.dumps(self.mock_responses["intent_analyst"])
        
        elif "plot" in prompt_lower and "point" in prompt_lower:
            return json.dumps(self.mock_responses["scene_scout"])
        
        elif "style" in prompt_lower and "guide" in prompt_lower:
            return json.dumps(self.mock_responses["style_analyst"])
        
        elif "masterweaver" in prompt_lower or "weave together a plot point" in prompt_lower or "weave plot points" in prompt_lower:
            return json.dumps(self.mock_responses["master_weaver"])
        
        elif "correct" in prompt_lower or "polish" in prompt_lower:
            return json.dumps(self.mock_responses["correction_polish"])
        
        elif "character" in prompt_lower and "extract" in prompt_lower:
            return json.dumps(self.mock_responses["character_extractor"])
        
        elif "lore" in prompt_lower or "world" in prompt_lower:
            return json.dumps(self.mock_responses["lore_master"])
        
        else:
            # Default response for unknown prompts
            return json.dumps({
                "response": f"Mock response for prompt: {prompt[:50]}...",
                "status": "success"
            })
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate simple text response"""
        self.call_count += 1
        
        # Simple text responses for different scenarios
        if "detective" in prompt.lower():
            return "The detective stood in the fog, knowing that some mysteries are better left unsolved."
        elif "lighthouse" in prompt.lower():
            return "The lighthouse beam cut through the darkness, but some shadows are too deep for any light to reach."
        elif "disappearance" in prompt.lower():
            return "People don't just vanish. There's always a reason, always a story, always someone who knows the truth."
        else:
            return "The story continues, weaving together the threads of mystery and revelation."

# Global mock client instance
_mock_client = None

def get_mock_gemini_client() -> MockGeminiClient:
    """Get the singleton mock Gemini client instance"""
    global _mock_client
    if _mock_client is None:
        _mock_client = MockGeminiClient()
    return _mock_client

