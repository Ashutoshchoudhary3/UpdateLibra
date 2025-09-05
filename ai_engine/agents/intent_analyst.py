



import os
from typing import Optional
from utils.gemini_client import get_gemini_client

class IntentAnalyst:
    def __init__(self):
        self.client = get_gemini_client()
    
    async def analyze_intent(self, summary: str, previous_chapter: Optional[str], genre: str) -> str:
        """Analyze the author's intent and create a chapter brief"""
        
        print(f"IntentAnalyst: Analyzing intent for {genre} story")
        
        # Create a comprehensive prompt for Gemini
        prompt = f"""As an expert literary analyst, analyze the following story summary and create a detailed chapter brief.

STORY SUMMARY: {summary}
GENRE: {genre}
PREVIOUS CHAPTER: {previous_chapter if previous_chapter else 'None (First chapter)'}

Please create a comprehensive chapter brief that includes:

1. TONE AND STYLE REQUIREMENTS
2. CHARACTER VOICE CONSISTENCY GUIDELINES
3. PLOT REQUIREMENTS AND DEVELOPMENT
4. WORLD-BUILDING ELEMENTS (if applicable)
5. QUALITY STANDARDS FOR THE GENRE

The brief should be specific to the {genre} genre and should guide the writing of this chapter to maintain consistency with genre conventions while avoiding clichés.

Format the response as a professional chapter brief with clear sections."""

        try:
            # Use Gemini API to generate the chapter brief
            chapter_brief = await self.client.generate_text(
                prompt=prompt,
                max_tokens=1500,
                temperature=0.7,
                system_message="You are an expert literary analyst and writing coach specializing in genre fiction."
            )
            
            print(f"Generated chapter brief: {chapter_brief[:100]}...")
            return chapter_brief
            
        except Exception as e:
            print(f"Gemini API failed in IntentAnalyst: {str(e)}")
            # Fallback to the original mock implementation
            if "fantasy" in genre.lower():
                return f"""CHAPTER BRIEF - Fantasy Genre

TONE AND STYLE REQUIREMENTS:
- Maintain a sense of wonder and magical atmosphere
- Use descriptive, evocative language that paints vivid pictures
- Balance action with world-building elements
- Keep a consistent narrative voice throughout

CHARACTER VOICE CONSISTENCY:
- Characters should speak and think in ways appropriate to a fantasy setting
- Maintain distinct personalities and speech patterns
- Show character growth through their reactions to magical events

PLOT REQUIREMENTS:
- Story Summary: {summary}
- Focus on the discovery of magical powers and its impact
- Build tension around the character's transformation
- Include sensory details about the magical experience

WORLD-BUILDING ELEMENTS:
- Establish the rules of magic in this world
- Describe the setting with rich, immersive details
- Include cultural and historical context for magical elements

QUALITY STANDARDS:
- Fantasy readers expect immersive world-building
- Avoid clichés while maintaining genre conventions
- Balance exposition with action and dialogue"""
            else:
                return f"""CHAPTER BRIEF - {genre.upper()} Genre

TONE AND STYLE REQUIREMENTS:
- Maintain appropriate tone for {genre} genre
- Use clear, engaging prose that fits the story type
- Keep narrative voice consistent throughout

CHARACTER VOICE CONSISTENCY:
- Characters should be authentic to the genre and setting
- Maintain consistent personalities and motivations
- Show character development through actions and dialogue

PLOT REQUIREMENTS:
- Story Summary: {summary}
- Focus on key plot points and character development
- Maintain appropriate pacing for the genre
- Include relevant descriptive elements

QUALITY STANDARDS:
- Follow genre conventions while avoiding clichés
- Maintain reader engagement through compelling narrative
- Balance description with action and dialogue"""



