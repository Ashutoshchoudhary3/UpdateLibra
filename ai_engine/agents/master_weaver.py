









import os
from typing import List
from utils.gemini_client import get_gemini_client

class MasterWeaver:
    def __init__(self):
        self.client = get_gemini_client()
    
    async def weave_content(self, plot_point: str, scraped_content: str, style_guide: str, chapter_brief: str) -> str:
        """Weave plot point with scraped human-written content into a polished paragraph"""
        
        print(f"MasterWeaver: Weaving content for plot point: {plot_point[:50]}...")
        
        try:
            # Use Gemini API to weave content intelligently
            return await self._weave_with_gemini(plot_point, scraped_content, style_guide, chapter_brief)
        except Exception as e:
            print(f"Gemini API failed in MasterWeaver: {str(e)}")
            # Fallback to mock implementation
            return self._get_mock_woven_content(plot_point)
    
    async def _weave_with_gemini(self, plot_point: str, scraped_content: str, style_guide: str, chapter_brief: str) -> str:
        """Use Gemini API to weave content intelligently"""
        
        prompt = f"""You are a MasterWeaver AI agent. Your task is to weave together a plot point with human-written descriptive content into a single, polished paragraph.

CORE PHILOSOPHY: You are NOT being creative. You are ASSEMBLING existing human-written content to serve the user's plot.

PLOT POINT (what MUST happen):
{plot_point}

HUMAN-WRITTEN DESCRIPTIVE CONTENT (use this, don't replace it):
{scraped_content}

STYLE GUIDE (follow this style):
{style_guide}

CHAPTER BRIEF (maintain consistency):
{chapter_brief}

INSTRUCTIONS:
1. Use the human-written descriptive content as your foundation
2. Weave in the plot point naturally
3. Follow the style guide exactly
4. Maintain consistency with the chapter brief
5. Create ONE polished paragraph (3-5 sentences)
6. Make it feel organic and natural
7. DO NOT add creative elements not in the plot point
8. DO NOT replace the human-written content - weave it in

WEAVE TOGETHER:
Create a single paragraph that seamlessly combines the plot point with the descriptive content, following the style guide."""

        try:
            response = await self.client.generate_text(
                prompt=prompt,
                max_tokens=500,
                temperature=0.4,
                system_message="You are a MasterWeaver AI that assembles human-written content with plot points into polished paragraphs."
            )
            
            return response.strip()
            
        except Exception as e:
            print(f"Gemini weaving failed: {e}")
            return self._get_mock_woven_content(plot_point)
    
    def _get_mock_woven_content(self, plot_point: str) -> str:
        """Fallback mock woven content when API is unavailable"""
        if "magical powers" in plot_point.lower():
            return f"""The morning light filtered through the curtains as Sarah stretched languidly in her bed, unaware that today would change everything. {plot_point} She had always been an ordinary girl, living an ordinary life in her small suburban town, but as the sun climbed higher in the sky, she felt an unfamiliar tingling sensation spreading through her fingertips. The air around her seemed to shimmer with possibility, and for the first time in her eighteen years, Sarah wondered if there might be more to the world than she had ever imagined."""
        else:
            return f"""The scene unfolded with the quiet intensity of a moment that would echo through the years. {plot_point} Every detail seemed sharper, more vivid than before—the way the light caught on unexpected surfaces, the subtle shifts in atmosphere that spoke of change coming. In the space between heartbeats, everything shifted, and what had been merely potential became inevitable, written in the fabric of the day with invisible ink that only time would reveal."""









