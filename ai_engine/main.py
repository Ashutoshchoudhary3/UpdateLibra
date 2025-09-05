

import os
import asyncio
import httpx
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Import agents
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.intent_analyst import IntentAnalyst
from agents.scene_scout import SceneScout
from agents.style_analyst import StyleAnalyst
from agents.master_weaver import MasterWeaver
from agents.correction_polish import CorrectionPolishAI
from agents.character_extractor import CharacterExtractor
from agents.lore_master import LoreMaster

# Import database
from database.db_manager import DatabaseManager

load_dotenv()

app = FastAPI(title="AI Research Assistant for Writers", version="1.0.0")

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChapterRequest(BaseModel):
    summary: str
    genre: str
    previous_chapter_id: Optional[int] = None

class ChapterResponse(BaseModel):
    chapter_id: int
    title: str
    content: str
    word_count: int
    style_guide: str
    characters: List[Dict[str, Any]]
    lore: List[Dict[str, Any]]
    chapter_number: int
    previous_chapter_id: Optional[int] = None

class HealthResponse(BaseModel):
    status: str
    services: Dict[str, str]

# Initialize agents
intent_analyst = IntentAnalyst()
scene_scout = SceneScout()
style_analyst = StyleAnalyst()
master_weaver = MasterWeaver()
correction_polish = CorrectionPolishAI()
character_extractor = CharacterExtractor()
lore_master = LoreMaster()

# Initialize database
db_manager = DatabaseManager()

# Configuration
SCRAPER_SERVICE_URL = os.getenv("SCRAPER_SERVICE_URL", "http://localhost:3002")
FALLBACK_SCRAPER_URL = os.getenv("FALLBACK_SCRAPER_URL", "http://localhost:3003")

@app.get("/")
async def root():
    return {"message": "AI Research Assistant for Writers", "status": "running"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check health of all services"""
    services = {
        "ai_engine": "healthy",
        "database": "healthy"
    }
    
    # Check scraper service
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{SCRAPER_SERVICE_URL}/health", timeout=5.0)
            if response.status_code == 200:
                services["scraper_service"] = "healthy"
            else:
                services["scraper_service"] = "unhealthy"
    except Exception as e:
        services["scraper_service"] = f"error: {str(e)}"
    
    return HealthResponse(
        status="healthy" if all("healthy" in str(v) for v in services.values()) else "degraded",
        services=services
    )

@app.post("/generate-chapter", response_model=ChapterResponse)
async def generate_chapter(request: ChapterRequest):
    """Generate a chapter based on summary and genre"""
    try:
        print(f"🚀 Starting chapter generation for genre: {request.genre}")
        
        # Step 0: Determine chapter number and get previous chapter if needed
        chapter_number = 1
        previous_chapter_content = None
        
        if request.previous_chapter_id:
            previous_chapter = await db_manager.get_chapter_by_id(request.previous_chapter_id)
            if previous_chapter:
                previous_chapter_content = previous_chapter['chapter_content']
                chapter_number = previous_chapter['chapter_number'] + 1
        
        # Step 1: Intent Analysis
        print("📋 Step 1: Intent Analysis")
        chapter_brief = await intent_analyst.analyze_intent(
            request.summary, 
            previous_chapter_content,
            request.genre
        )
        print(f"Chapter brief created: {chapter_brief[:100]}...")
        
        # Step 2: Scene Scouting
        print("🗺️ Step 2: Scene Scouting")
        plot_points = await scene_scout.deconstruct_summary(request.summary)
        print(f"Generated {len(plot_points)} plot points")
        
        # Step 3: Style Analysis
        print("🎨 Step 3: Style Analysis")
        style_guide = await style_analyst.research_genre(request.genre)
        print(f"Style guide retrieved: {style_guide[:100]}...")
        
        # Step 4: Master Weaving
        print("🧵 Step 4: Master Weaving")
        chapter_sections = []
        
        for i, plot_point in enumerate(plot_points):
            print(f"Weaving plot point {i+1}/{len(plot_points)}: {plot_point[:50]}...")
            
            # Generate search query for this plot point
            search_query = await scene_scout.generate_search_query(plot_point, request.genre, chapter_brief)
            print(f"Search query: {search_query}")
            
            # Scrape content
            scraped_content = await scrape_content(search_query)
            print(f"Scraped {len(scraped_content)} characters of content")
            
            # Weave plot point with scraped content
            woven_section = await master_weaver.weave_content(
                plot_point,
                scraped_content,
                style_guide,
                chapter_brief
            )
            chapter_sections.append(woven_section)
            print(f"Section {i+1} woven successfully")
        
        # Combine sections into raw chapter
        raw_chapter = "\n\n".join(chapter_sections)
        print(f"Raw chapter created: {len(raw_chapter)} characters")
        
        # Step 5: Correction & Polish
        print("✨ Step 5: Correction & Polish")
        polished_chapter = await correction_polish.polish_chapter(
            raw_chapter,
            style_guide,
            chapter_brief
        )
        print(f"Chapter polished: {len(polished_chapter)} characters")
        
        # Step 6: World Building
        print("🏗️ Step 6: World Building")
        characters = await character_extractor.extract_characters(polished_chapter)
        lore = await lore_master.extract_lore(polished_chapter)
        print(f"Extracted {len(characters)} characters and {len(lore)} lore entries")
        
        # Save to database
        await db_manager.store_chapter(
            request.summary,
            request.genre,
            polished_chapter,
            chapter_number,
            request.previous_chapter_id
        )
        
        # Get the chapter ID of the newly created chapter
        latest_chapter = await db_manager.get_latest_chapter()
        chapter_id = latest_chapter['id']
        
        # Generate title
        title = await generate_title(polished_chapter, request.genre)
        
        print("✅ Chapter generation complete!")
        
        return ChapterResponse(
            chapter_id=chapter_id,
            title=title,
            content=polished_chapter,
            word_count=len(polished_chapter.split()),
            style_guide=style_guide,
            characters=characters,
            lore=lore,
            chapter_number=chapter_number,
            previous_chapter_id=request.previous_chapter_id
        )
        
    except Exception as e:
        print(f"❌ Chapter generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chapter generation failed: {str(e)}")

async def scrape_content(query: str) -> str:
    """Scrape content from the web using the scraper service with fallback mechanism"""
    
    # First, try the enhanced scraper service
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SCRAPER_SERVICE_URL}/scrape",
                json={"query": query, "source": "ai_engine"},
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data.get("content", "")
                source = data.get("source", "scraped")
                session_id = data.get("sessionId", "unknown")
                
                if content:
                    print(f"✅ Enhanced scraper returned {len(content)} characters from {source} (session: {session_id})")
                    return content
                elif data.get("fallback"):
                    print(f"✅ Enhanced scraper returned fallback content (session: {session_id})")
                    return data["fallback"]
                    
    except Exception as e:
        print(f"⚠️  Enhanced scraper failed: {str(e)}")
    
    # If enhanced scraper fails, try the fallback scraper
    try:
        print(f"🔄 Trying fallback scraper for: {query[:50]}...")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{FALLBACK_SCRAPER_URL}/scrape",
                json={"query": query, "source": "ai_engine"},
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data.get("content", "")
                
                if content:
                    print(f"✅ Fallback scraper returned {len(content)} characters")
                    return content
                    
    except Exception as e:
        print(f"❌ Fallback scraper also failed: {str(e)}")
    
    # If both scrapers fail, return a basic fallback
    print(f"⚠️  All scrapers failed, using basic fallback for: {query[:50]}...")
    return f"Descriptive content related to: {query}"

async def generate_title(chapter_content: str, genre: str) -> str:
    """Generate a title for the chapter"""
    try:
        # Simple title generation - could be enhanced with AI
        words = chapter_content.split()
        if len(words) > 10:
            # Take first few meaningful words
            title_words = []
            for word in words[:20]:
                if len(word) > 3 and word.lower() not in ['the', 'and', 'but', 'for', 'are', 'this', 'that']:
                    title_words.append(word)
                if len(title_words) >= 3:
                    break
            
            if title_words:
                return " ".join(title_words)
        
        return f"{genre.title()} Chapter"
        
    except Exception as e:
        print(f"Title generation failed: {str(e)}")
        return f"{genre.title()} Chapter"

@app.get("/chapters/{chapter_id}")
async def get_chapter(chapter_id: int):
    """Retrieve a specific chapter by ID"""
    try:
        chapter = await db_manager.get_chapter_by_id(chapter_id)
        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")
        
        return chapter
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve chapter: {str(e)}")

@app.get("/chapters")
async def list_chapters():
    """List all chapters"""
    try:
        chapters = await db_manager.list_chapters()
        return {"chapters": chapters}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list chapters: {str(e)}")

@app.get("/chapters/latest")
async def get_latest_chapter():
    """Get the most recently created chapter"""
    try:
        chapter = await db_manager.get_latest_chapter()
        if not chapter:
            raise HTTPException(status_code=404, detail="No chapters found")
        
        return chapter
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve latest chapter: {str(e)}")





@app.delete("/chapters/{chapter_id}")
async def delete_chapter(chapter_id: int):
    """Delete a specific chapter"""
    try:
        success = await db_manager.delete_chapter(chapter_id)
        if not success:
            raise HTTPException(status_code=404, detail="Chapter not found")
        
        return {"message": "Chapter deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete chapter: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Starting AI Research Assistant for Writers")
    print(f"📡 Server running on http://{host}:{port}")
    print(f"🔗 Scraper service: {SCRAPER_SERVICE_URL}")
    
    uvicorn.run(app, host=host, port=port)

