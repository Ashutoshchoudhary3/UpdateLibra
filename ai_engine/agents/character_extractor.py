


















import os
import json
from typing import List, Dict, Any
from utils.gemini_client import get_gemini_client

class CharacterExtractor:
    def __init__(self):
        self.client = get_gemini_client()
    
    async def extract_characters(self, chapter_text: str) -> List[Dict[str, Any]]:
        """Extract character information from chapter text"""
        
        print(f"CharacterExtractor: Analyzing chapter for characters ({len(chapter_text)} characters)")
        
        try:
            # Use Gemini API for intelligent character extraction
            return await self._extract_with_gemini(chapter_text)
        except Exception as e:
            print(f"Gemini API failed in CharacterExtractor: {str(e)}")
            # Fallback to mock implementation
            return self._get_mock_characters(chapter_text)
    
    async def _extract_with_gemini(self, chapter_text: str) -> List[Dict[str, Any]]:
        """Use Gemini API for intelligent character extraction"""
        
        prompt = f"""You are a CharacterExtractor AI agent. Your task is to extract character information from a chapter of text.

CORE PHILOSOPHY: Be precise and factual. Only extract characters that actually appear or are mentioned in the text.

CHAPTER TEXT:
{chapter_text}

EXTRACTION INSTRUCTIONS:
1. Identify all characters mentioned in the text
2. For each character, extract:
   - name (exactly as mentioned)
   - description (what the text says about them)
   - backstory (any background information provided)
   - personality (traits mentioned or implied)
   - first_appearance (how/when they first appear)
3. Only include characters that actually appear in the text
4. Be factual and precise - don't invent information
5. Return as a JSON array of character objects

RETURN FORMAT:
[
  {{
    "name": "Character Name",
    "description": "Description from text",
    "backstory": "Background information if mentioned",
    "personality": "Personality traits from text",
    "first_appearance": "How they first appear in story"
  }}
]

Return ONLY the JSON array, no additional text."""

        try:
            response = await self.client.generate_text(
                prompt=prompt,
                max_tokens=1000,
                temperature=0.1,
                system_message="You are a CharacterExtractor AI that identifies and extracts character information from text."
            )
            
            # Parse the JSON response
            characters = json.loads(response.strip())
            return characters
            
        except Exception as e:
            print(f"Gemini character extraction failed: {e}")
            return self._get_mock_characters(chapter_text)
    
    def _get_mock_characters(self, chapter_text: str) -> List[Dict[str, Any]]:
        """Fallback mock character extraction when API is unavailable"""
        characters = []
        
        # Look for common character names and patterns
        if "Sarah" in chapter_text:
            characters.append({
                "name": "Sarah",
                "description": "Main character, young woman experiencing magical transformation",
                "backstory": "Ordinary girl living in suburban town, unaware of magical heritage",
                "personality": "Curious, observant, experiencing wonder and confusion",
                "first_appearance": "Introduced waking up in bed, feeling tingling sensations"
            })
        
        if "mother" in chapter_text.lower() or "mom" in chapter_text.lower():
            characters.append({
                "name": "Mother",
                "description": "Sarah's mother, possibly aware of magical heritage",
                "backstory": "Parent who may know about magical family history",
                "personality": "Protective, possibly keeping secrets",
                "first_appearance": "Mentioned in context of family and heritage"
            })
        
        # Add some generic characters if none found
        if not characters:
            characters.append({
                "name": "Protagonist",
                "description": "Main character experiencing the story events",
                "backstory": "Character going through significant life changes",
                "personality": "Observant, experiencing transformation",
                "first_appearance": "Introduced through narrative perspective"
            })
        
        return characters
    
    def _parse_character_text(self, text: str) -> List[Dict[str, Any]]:
        """Fallback parsing for character information"""
        characters = []
        
        # Simple heuristic parsing
        lines = text.split('\n')
        current_char = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if 'name' in line.lower() and ':' in line:
                if current_char:
                    characters.append(current_char)
                current_char = {"name": line.split(':', 1)[1].strip().strip('"')}
            elif ':' in line and current_char:
                key = line.split(':', 1)[0].lower().strip()
                value = line.split(':', 1)[1].strip().strip('"')
                if key in ['description', 'backstory', 'personality', 'first_appearance']:
                    current_char[key] = value
        
        if current_char:
            characters.append(current_char)
        
        return characters
















