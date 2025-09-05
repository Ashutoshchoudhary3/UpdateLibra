







import os
import asyncio
import httpx
from database.db_manager import DatabaseManager
from utils.gemini_client import get_gemini_client

class StyleAnalyst:
    def __init__(self):
        self.client = get_gemini_client()
        self.db_manager = DatabaseManager()
    
    async def research_genre(self, genre: str) -> str:
        """Research writing style for the specified genre"""
        
        print(f"StyleAnalyst: Researching style guide for {genre}")
        
        # First check if we have a cached style guide
        cached_guide = await self._get_cached_style_guide(genre)
        if cached_guide:
            print(f"Using cached style guide for {genre}")
            return cached_guide
        
        # Generate new style guide using Gemini API
        try:
            style_guide = await self._create_style_guide_with_gemini(genre)
            formatted_guide = self._format_style_guide(style_guide)
            
            # Cache the style guide for future use
            await self._cache_style_guide(genre, formatted_guide)
            
            return formatted_guide
            
        except Exception as e:
            print(f"Gemini API failed in StyleAnalyst: {str(e)}")
            # Fallback to mock implementation
            return self._get_mock_style_guide(genre)
    
    async def _create_style_guide_with_gemini(self, genre: str) -> dict:
        """Create comprehensive style guide using Gemini API"""
        
        prompt = f"""You are a StyleAnalyst AI agent. Create a comprehensive style guide for writing in the {genre} genre.

CORE PHILOSOPHY: You are analyzing existing styles, NOT creating new ones. Base your guide on established conventions.

Genre: {genre}

Create a detailed style guide including:

1. STYLE DESCRIPTION
   - Key characteristics of {genre} writing
   - What makes it distinctive
   - Essential elements that define the genre

2. TONE GUIDELINES
   - Appropriate emotional tone
   - Voice and perspective recommendations
   - Atmosphere and mood requirements

3. COMMON TROPES AND CONVENTIONS
   - Frequently used literary devices
   - Genre-specific conventions
   - Elements readers expect

4. WRITING TECHNIQUES
   - Sentence structure preferences
   - Vocabulary choices
   - Pacing and rhythm guidelines
   - Dialogue style (if applicable)

5. QUALITY STANDARDS
   - What makes {genre} writing effective
   - Common pitfalls to avoid
   - Benchmarks for good writing in this genre

Be specific and detailed. This guide will be used by other AI agents to maintain authentic {genre} style.

Format your response as a structured guide with clear sections."""

        try:
            response = await self.client.generate_text(
                prompt=prompt,
                max_tokens=1500,
                temperature=0.3,
                system_message=f"You are a StyleAnalyst AI that creates comprehensive style guides for {genre} writing."
            )
            
            # Parse the response into structured format
            sections = self._parse_style_guide(response)
            
            return {
                'style_description': sections.get('style_description', ''),
                'tone_guidelines': sections.get('tone_guidelines', ''),
                'common_tropes': sections.get('common_tropes', ''),
                'writing_tips': sections.get('writing_tips', '')
            }
            
        except Exception as e:
            print(f"Style guide creation with Gemini failed: {e}")
            return self._get_default_style_guide(genre)
    
    async def _research_genre_style(self, genre: str) -> dict:
        """Research genre style by analyzing examples and guides"""
        
        # Generate research queries for this genre
        research_queries = [
            f"{genre.replace('_', ' ')} writing style guide techniques",
            f"how to write {genre.replace('_', ' ')} fiction style",
            f"{genre.replace('_', ' ')} genre conventions writing",
            f"{genre.replace('_', ' ')} literary techniques examples"
        ]
        
        style_research = {
            'descriptions': [],
            'techniques': [],
            'conventions': [],
            'examples': []
        }
        
        for query in research_queries:
            try:
                # This would normally call the scraper service
                # For now, we'll simulate the research
                print(f"Researching: {query}")
                # In a real implementation, this would scrape actual content
                await asyncio.sleep(1)  # Simulate research time
                
            except Exception as e:
                print(f"Research query failed: {e}")
                continue
        
        return style_research
    
    async def _get_cached_style_guide(self, genre: str) -> str:
        """Check if we have a cached style guide for this genre"""
        try:
            # This would normally check the database
            # For now, return None to always generate new guides
            return None
        except Exception as e:
            print(f"Error checking cached style guide: {e}")
            return None
    
    async def _cache_style_guide(self, genre: str, style_guide: str) -> None:
        """Cache the style guide for future use"""
        try:
            # This would normally save to database
            # For now, just log that we're caching
            print(f"Caching style guide for {genre}")
        except Exception as e:
            print(f"Error caching style guide: {e}")
    
    def _get_mock_style_guide(self, genre: str) -> str:
        """Fallback mock style guide when API is unavailable"""
        if "fantasy" in genre.lower():
            style_guide = {
                'style_description': 'Wonder, magic, and epic scale',
                'tone_guidelines': 'Rich, descriptive world-building with evocative sensory details',
                'common_tropes': 'Clear magic system rules, heroic character arcs, good vs evil conflicts',
                'writing_tips': 'Show magic through character experience, build immersive worlds with layered details'
            }
        else:
            style_guide = {
                'style_description': 'Authentic and engaging',
                'tone_guidelines': 'Clear, accessible prose with strong character voice',
                'common_tropes': 'Follow genre expectations while maintaining reader engagement',
                'writing_tips': 'Show character through action and dialogue, use specific concrete details'
            }
        
        return self._format_style_guide(style_guide)
    
    def _parse_style_guide(self, guide_text: str) -> dict:
        """Parse the generated style guide into structured sections"""
        sections = {}
        current_section = None
        current_content = []
        
        lines = guide_text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for section headers
            if any(keyword in line.upper() for keyword in ['STYLE', 'TONE', 'TROPE', 'TECHNIQUE', 'QUALITY']):
                if current_section and current_content:
                    sections[current_section] = ' '.join(current_content)
                current_section = line.lower().replace(':', '').replace(' ', '_')
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # Add the last section
        if current_section and current_content:
            sections[current_section] = ' '.join(current_content)
        
        return sections
    
    def _get_default_style_guide(self, genre: str) -> dict:
        """Fallback style guide for when AI generation fails"""
        return {
            'style_description': f'Authentic {genre.replace("_", " ")} writing style with rich descriptive language',
            'tone_guidelines': 'Maintain consistent tone appropriate to the genre and story context',
            'common_tropes': f'Use established {genre} conventions while avoiding clichés',
            'writing_tips': 'Focus on sensory details, character development, and authentic voice'
        }
    
    def _format_style_guide(self, style_guide: dict) -> str:
        """Format style guide for use by other agents"""
        return f"""
GENRE STYLE GUIDE: {style_guide.get('style_description', '')}

TONE GUIDELINES:
{style_guide.get('tone_guidelines', '')}

CONVENTIONS AND TROPES:
{style_guide.get('common_tropes', '')}

WRITING TECHNIQUES:
{style_guide.get('writing_tips', '')}
""".strip()





