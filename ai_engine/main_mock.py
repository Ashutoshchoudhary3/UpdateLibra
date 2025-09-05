
"""
AI Research Assistant for Writers - Mock Version
This version uses mock AI responses for testing without Gemini API dependencies.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import time
from datetime import datetime
import asyncio
from pathlib import Path

# Import mock client instead of real Gemini client
from mock_gemini_client import get_mock_gemini_client

# Import database manager
from database.db_manager import DatabaseManager

# Define Pydantic models
class ChapterRequest(BaseModel):
    summary: str
    genre: str
    previous_chapter_id: Optional[int] = None

class ChapterResponse(BaseModel):
    chapter_id: int
    title: str
    content: str
    word_count: int
    chapter_number: int
    characters: List[Dict[str, Any]] = []
    lore: List[Dict[str, Any]] = []

class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: str

# Mock agent implementations
class MockIntentAnalyst:
    def __init__(self):
        self.client = get_mock_gemini_client()
    
    async def analyze_intent(self, summary: str, previous_chapter: Optional[str] = None, genre: str = "general") -> Dict[str, Any]:
        """Mock intent analysis"""
        prompt = f"Analyze the intent and tone for this {genre} story: {summary}"
        response = self.client.generate_content(prompt)
        return json.loads(response)

class MockSceneScout:
    def __init__(self):
        self.client = get_mock_gemini_client()
    
    async def scout_scenes(self, summary: str, intent_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Mock scene scouting"""
        prompt = f"Generate plot points and search queries for: {summary}"
        response = self.client.generate_content(prompt)
        return json.loads(response)

class MockStyleAnalyst:
    def __init__(self):
        self.client = get_mock_gemini_client()
    
    async def analyze_style(self, genre: str) -> str:
        """Mock style analysis"""
        prompt = f"Generate style guide for genre: {genre}"
        response = self.client.generate_content(prompt)
        data = json.loads(response)
        return data.get("genre_style_guide", "Default style guide")

class MockMasterWeaver:
    def __init__(self):
        self.client = get_mock_gemini_client()
    
    async def weave_chapter(self, plot_points: List[str], style_guide: str, intent_analysis: Dict[str, Any]) -> str:
        """Mock chapter weaving"""
        prompt = f"Weave plot points into a chapter: {' '.join(plot_points)}"
        response = self.client.generate_content(prompt)
        data = json.loads(response)
        return "\n\n".join(data.get("sections", ["Chapter content here..."]))

class MockCorrectionPolish:
    def __init__(self):
        self.client = get_mock_gemini_client()
    
    async def correct_and_polish(self, chapter_content: str) -> str:
        """Mock correction and polishing"""
        prompt = f"Correct and polish this chapter: {chapter_content[:100]}..."
        response = self.client.generate_content(prompt)
        data = json.loads(response)
        return data.get("corrected_text", chapter_content)

class MockCharacterExtractor:
    def __init__(self):
        self.client = get_mock_gemini_client()
    
    async def extract_characters(self, chapter_content: str) -> List[Dict[str, Any]]:
        """Mock character extraction"""
        prompt = f"Extract characters from: {chapter_content[:100]}..."
        response = self.client.generate_content(prompt)
        data = json.loads(response)
        return data.get("characters", [])

class MockLoreMaster:
    def __init__(self):
        self.client = get_mock_gemini_client()
    
    async def extract_lore(self, chapter_content: str) -> List[Dict[str, Any]]:
        """Mock lore extraction"""
        prompt = f"Extract lore from: {chapter_content[:100]}..."
        response = self.client.generate_content(prompt)
        data = json.loads(response)
        return data.get("lore_entries", [])

# Initialize FastAPI app
app = FastAPI(
    title="AI Research Assistant for Writers (Mock Version)",
    description="Mock version for testing without Gemini AI dependencies",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
db_manager = DatabaseManager()

# Initialize mock agents
intent_analyst = MockIntentAnalyst()
scene_scout = MockSceneScout()
style_analyst = MockStyleAnalyst()
master_weaver = MockMasterWeaver()
correction_polish = MockCorrectionPolish()
character_extractor = MockCharacterExtractor()
lore_master = MockLoreMaster()

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        service="ai_engine_mock",
        timestamp=datetime.now().isoformat()
    )

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Research Assistant for Writers (Mock Version)",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "generate_chapter": "/generate-chapter",
            "chapters": "/chapters"
        }
    }

@app.post("/generate-chapter", response_model=ChapterResponse)
async def generate_chapter(request: ChapterRequest):
    """Generate a chapter using mock AI agents"""
    try:
        print(f"🎯 Starting chapter generation for: {request.summary[:50]}...")
        
        # Step 1: Intent Analysis
        print("🔍 Step 1: Intent Analysis")
        previous_chapter_content = ""
        if request.previous_chapter_id:
            # In a real implementation, this would fetch from database
            previous_chapter_content = "Previous chapter content would be fetched here"
        
        intent_analysis = await intent_analyst.analyze_intent(
            request.summary, 
            previous_chapter_content,
            request.genre
        )
        await asyncio.sleep(1)  # Simulate processing time
        
        # Step 2: Scene Scouting
        print("🗺️ Step 2: Scene Scouting")
        scene_data = await scene_scout.scout_scenes(request.summary, intent_analysis)
        plot_points = scene_data.get("plot_points", ["Plot point 1", "Plot point 2", "Plot point 3", "Plot point 4"])
        await asyncio.sleep(1)
        
        # Step 3: Style Analysis
        print("🎨 Step 3: Style Analysis")
        style_guide = await style_analyst.analyze_style(request.genre)
        await asyncio.sleep(1)
        
        # Step 4: Master Weaving
        print("🧵 Step 4: Master Weaving")
        raw_chapter = await master_weaver.weave_chapter(plot_points, style_guide, intent_analysis)
        print(f"Raw chapter created: {len(raw_chapter)} characters")
        await asyncio.sleep(1)
        
        # Step 5: Correction & Polish
        print("✨ Step 5: Correction & Polish")
        polished_chapter = await correction_polish.correct_and_polish(raw_chapter)
        print(f"Chapter polished: {len(polished_chapter)} characters")
        await asyncio.sleep(1)
        
        # Step 6: World Building
        print("🏗️ Step 6: World Building")
        characters = await character_extractor.extract_characters(polished_chapter)
        lore_entries = await lore_master.extract_lore(polished_chapter)
        await asyncio.sleep(1)
        
        # Save to database
        await db_manager.store_chapter(
            summary=request.summary,
            genre=request.genre,
            chapter_content=polished_chapter,
            chapter_number=1,
            previous_chapter_id=request.previous_chapter_id
        )
        
        # Get the chapter ID of the newly created chapter
        latest_chapter = await db_manager.get_latest_chapter()
        chapter_id = latest_chapter['id']
        
        # Store characters and lore
        await db_manager.store_characters(characters)
        await db_manager.store_lore(lore_entries)
        
        print("✅ Chapter generation complete!")
        
        return ChapterResponse(
            chapter_id=chapter_id,
            title="The Lighthouse Mystery",  # Use our generated title
            content=polished_chapter,
            word_count=len(polished_chapter.split()),
            chapter_number=1,
            characters=characters,
            lore=lore_entries
        )
        
    except Exception as e:
        print(f"❌ Chapter generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Chapter generation failed: {str(e)}")

@app.get("/chapters")
async def get_chapters():
    """Get all chapters"""
    chapters = await db_manager.list_chapters()
    return {"chapters": chapters}

@app.get("/chapters/{chapter_id}")
async def get_chapter(chapter_id: int):
    """Get a specific chapter"""
    chapter = db_manager.get_chapter_by_id(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting AI Research Assistant for Writers (Mock Version)...")
    print("📖 API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)

