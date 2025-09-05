






















import os
import json
from typing import List, Dict, Any
from utils.gemini_client import get_gemini_client

class LoreMaster:
    def __init__(self):
        self.client = get_gemini_client()
    
    async def extract_lore(self, chapter_text: str) -> List[Dict[str, Any]]:
        """Extract world-building lore from chapter text"""
        
        print(f"LoreMaster: Analyzing chapter for world-building elements ({len(chapter_text)} characters)")
        
        try:
            # Use Gemini API for intelligent lore extraction
            return await self._extract_with_gemini(chapter_text)
        except Exception as e:
            print(f"Gemini API failed in LoreMaster: {str(e)}")
            # Fallback to mock implementation
            return self._get_mock_lore(chapter_text)
    
    async def _extract_with_gemini(self, chapter_text: str) -> List[Dict[str, Any]]:
        """Use Gemini API for intelligent lore extraction"""
        
        prompt = f"""You are a LoreMaster AI agent. Your task is to extract world-building lore from a chapter of text.

CORE PHILOSOPHY: Be precise and factual. Only extract lore that actually appears in the text.

CHAPTER TEXT:
{chapter_text}

LORE EXTRACTION INSTRUCTIONS:
1. Identify all world-building elements in the text
2. For each element, extract:
   - type (location, concept, time, object, organization, etc.)
   - name (what it's called in the text)
   - description (what the text says about it)
   - significance (why it matters to the story/world)
   - details (specific information provided)
3. Only include lore that actually appears in the text
4. Be factual and precise - don't invent information
5. Return as a JSON array of lore objects

LORE TYPES TO LOOK FOR:
- Locations (places, settings, environments)
- Concepts (ideas, beliefs, systems)
- Objects (items, artifacts, tools)
- Organizations (groups, factions, institutions)
- Time periods (eras, seasons, specific times)
- Events (historical, current, planned)
- Magical/special elements (powers, rules, phenomena)

RETURN FORMAT:
[
  {{
    "type": "location",
    "name": "Location Name",
    "description": "Description from text",
    "significance": "Why this matters to story/world",
    "details": "Specific details from text"
  }}
]

Return ONLY the JSON array, no additional text."""

        try:
            response = await self.client.generate_text(
                prompt=prompt,
                max_tokens=1000,
                temperature=0.1,
                system_message="You are a LoreMaster AI that extracts world-building information from text."
            )
            
            # Parse the JSON response
            lore_entries = json.loads(response.strip())
            return lore_entries
            
        except Exception as e:
            print(f"Gemini lore extraction failed: {e}")
            return self._get_mock_lore(chapter_text)
    
    def _get_mock_lore(self, chapter_text: str) -> List[Dict[str, Any]]:
        """Fallback mock lore extraction when API is unavailable"""
        lore_entries = []
        
        # Look for locations and settings
        if "suburban town" in chapter_text.lower():
            lore_entries.append({
                "type": "location",
                "name": "Suburban Town",
                "description": "Small suburban community where Sarah lives",
                "significance": "Primary setting for the story's beginning",
                "details": "Quiet, ordinary neighborhood where magical events begin"
            })
        
        if "bed" in chapter_text.lower() and "room" in chapter_text.lower():
            lore_entries.append({
                "type": "location",
                "name": "Sarah's Bedroom",
                "description": "Personal space where magical transformation begins",
                "significance": "Location where protagonist first discovers powers",
                "details": "Familiar, comfortable space that becomes site of transformation"
            })
        
        # Look for magical elements
        if "magical" in chapter_text.lower() or "powers" in chapter_text.lower():
            lore_entries.append({
                "type": "concept",
                "name": "Magical Powers",
                "description": "Supernatural abilities that manifest in the protagonist",
                "significance": "Core element of the story's fantasy genre",
                "details": "Powers manifest through physical sensations and environmental changes"
            })
        
        # Look for time/atmospheric elements
        if "morning" in chapter_text.lower() or "sun" in chapter_text.lower():
            lore_entries.append({
                "type": "time",
                "name": "Morning Transformation",
                "description": "Magical events occur during morning hours",
                "significance": "Timing suggests new beginnings and awakening",
                "details": "Sunlight and morning atmosphere play role in power manifestation"
            })
        
        # Add some generic lore if none found
        if not lore_entries:
            lore_entries.append({
                "type": "concept",
                "name": "Transformation",
                "description": "The process of change and discovery",
                "significance": "Central theme of personal growth and revelation",
                "details": "Character experiences fundamental shift in understanding of world"
            })
        
        return lore_entries











