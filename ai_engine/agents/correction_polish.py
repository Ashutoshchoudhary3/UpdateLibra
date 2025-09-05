












import os
from utils.gemini_client import get_gemini_client

class CorrectionPolishAI:
    def __init__(self):
        self.client = get_gemini_client()
    
    async def polish_chapter(self, raw_chapter: str, style_guide: str, chapter_brief: str) -> str:
        """Edit and polish the entire chapter for grammar, flow, and quality"""
        
        print(f"CorrectionPolishAI: Polishing chapter ({len(raw_chapter)} characters)")
        
        try:
            # Use Gemini API for intelligent polishing
            return await self._polish_with_gemini(raw_chapter, style_guide, chapter_brief)
        except Exception as e:
            print(f"Gemini API failed in CorrectionPolishAI: {str(e)}")
            # Fallback to basic polishing
            return self._basic_polish(raw_chapter)
    
    async def _polish_with_gemini(self, raw_chapter: str, style_guide: str, chapter_brief: str) -> str:
        """Use Gemini API for intelligent chapter polishing"""
        
        prompt = f"""You are a CorrectionPolish AI agent. Your task is to edit and polish a chapter for grammar, flow, and quality while preserving the author's intent.

CORE PHILOSOPHY: You are an EDITOR, not a rewriter. Preserve the author's voice and intent.

RAW CHAPTER (edit this):
{raw_chapter}

STYLE GUIDE (maintain this style):
{style_guide}

CHAPTER BRIEF (ensure consistency):
{chapter_brief}

EDITING INSTRUCTIONS:
1. Fix grammar, spelling, and punctuation errors
2. Improve sentence flow and readability
3. Ensure consistent tense and point of view
4. Maintain the author's voice and style
5. Preserve all plot points and character development
6. Do NOT add new creative content
7. Do NOT remove important details
8. Ensure smooth transitions between paragraphs
9. Check for logical consistency
10. Maintain the established tone and atmosphere

EDITING APPROACH:
- Be conservative - only make necessary changes
- Preserve the raw authenticity of the writing
- Focus on technical improvements, not creative changes
- Ensure the chapter reads naturally and professionally

Return the polished chapter that maintains all the original content while being technically sound and well-flowing."""

        try:
            response = await self.client.generate_text(
                prompt=prompt,
                max_tokens=2000,
                temperature=0.2,
                system_message="You are a CorrectionPolish AI that edits and polishes chapters while preserving author intent."
            )
            
            return response.strip()
            
        except Exception as e:
            print(f"Gemini polishing failed: {e}")
            return self._basic_polish(raw_chapter)
    
    def _basic_polish(self, raw_chapter: str) -> str:
        """Fallback basic polishing when API is unavailable"""
        # Simple polishing - fix obvious issues while preserving content
        polished = raw_chapter
        
        # Basic grammar fixes
        polished = polished.replace("  ", " ")  # Remove double spaces
        polished = polished.replace(" .", ".")  # Fix spacing before periods
        polished = polished.replace(" ,", ",")  # Fix spacing before commas
        
        # Ensure proper paragraph breaks
        paragraphs = polished.split("\n\n")
        cleaned_paragraphs = []
        for para in paragraphs:
            if para.strip():  # Only include non-empty paragraphs
                cleaned_paragraphs.append(para.strip())
        
        polished = "\n\n".join(cleaned_paragraphs)
        
        return polished













