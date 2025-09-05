





import os
from typing import List
from utils.gemini_client import get_gemini_client

class SceneScout:
    def __init__(self):
        self.client = get_gemini_client()
    
    async def deconstruct_summary(self, summary: str) -> List[str]:
        """Deconstruct story summary into key plot points"""
        
        print(f"SceneScout: Deconstructing summary: {summary}")
        
        prompt = f"""As a story structure expert, deconstruct this story summary into 4-6 key plot points.

STORY SUMMARY: {summary}

Requirements:
- Each plot point should represent a major story beat
- Plot points should be sequential and logical
- Each should be specific and actionable for writing
- Focus on the most important moments that drive the story forward

Format your response as a numbered list with clear, descriptive sentences for each plot point."""

        try:
            # Use Gemini API to deconstruct the summary
            response = await self.client.generate_text(
                prompt=prompt,
                max_tokens=800,
                temperature=0.6,
                system_message="You are an expert in story structure and narrative development."
            )
            
            # Parse the response into a list of plot points
            plot_points = []
            lines = response.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-') or line.startswith('*')):
                    # Remove numbering/bullets and clean up
                    cleaned_line = line.lstrip('0123456789.-* ').strip()
                    if len(cleaned_line) > 10:  # Only include substantial lines
                        plot_points.append(cleaned_line)
            
            # If we didn't get enough plot points, fall back to simple approach
            if len(plot_points) < 3:
                plot_points = self._generate_mock_plot_points(summary)
            
            print(f"Generated {len(plot_points)} plot points")
            return plot_points
            
        except Exception as e:
            print(f"Gemini API failed in SceneScout deconstruction: {str(e)}")
            # Fallback to mock implementation
            return self._generate_mock_plot_points(summary)
    
    def _generate_mock_plot_points(self, summary: str) -> List[str]:
        """Generate mock plot points when API is unavailable"""
        if "magical powers" in summary.lower() and "birthday" in summary.lower():
            return [
                "A young woman wakes up on her 18th birthday feeling strange and different",
                "She discovers she has magical powers when objects start moving around her",
                "She struggles to understand and control her newfound abilities",
                "She realizes her life will never be the same again"
            ]
        else:
            # Generic plot points for any story
            return [
                "The main character faces an initial challenge or discovery",
                "They encounter obstacles and conflicts",
                "They learn something important about themselves or the world",
                "They reach a resolution or transformation"
            ]
    
    async def generate_search_query(self, plot_point: str, genre: str, chapter_brief: str) -> str:
        """Generate a search query to find human-written content for this plot point"""
        
        print(f"SceneScout: Generating search query for: {plot_point}")
        
        prompt = f"""As a research assistant, generate a specific search query to find human-written descriptive content for this plot point.

PLOT POINT: {plot_point}
GENRE: {genre}
CHAPTER BRIEF CONTEXT: {chapter_brief[:200]}...

Requirements:
- Create a search query that would find descriptive passages from existing literature
- Focus on finding authentic, human-written descriptions that could inspire this scene
- The query should be specific enough to find relevant content but broad enough to find multiple sources
- Include genre-specific terms when appropriate

Format your response as a single search query string (no more than 10-15 words)."""

        try:
            # Use Gemini API to generate search query
            search_query = await self.client.generate_text(
                prompt=prompt,
                max_tokens=100,
                temperature=0.5,
                system_message="You are a research expert skilled at finding relevant literary content."
            )
            
            # Clean up the search query
            search_query = search_query.strip().strip('"').strip("'")
            
            # If the response is too short or generic, use fallback
            if len(search_query) < 10:
                search_query = self._generate_mock_search_query(plot_point, genre)
            
            print(f"Generated search query: {search_query}")
            return search_query
            
        except Exception as e:
            print(f"Gemini API failed in SceneScout search query: {str(e)}")
            # Fallback to mock implementation
            return self._generate_mock_search_query(plot_point, genre)
    
    def _generate_mock_search_query(self, plot_point: str, genre: str) -> str:
        """Generate mock search query when API is unavailable"""
        if "magical powers" in plot_point.lower():
            return f"{genre} discovering magical abilities descriptive scene"
        elif "birthday" in plot_point.lower():
            return f"{genre} 18th birthday transformation descriptive passage"
        else:
            return f"{genre} {plot_point[:50]} descriptive narrative"





