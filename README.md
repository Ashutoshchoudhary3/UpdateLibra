# AI Research Assistant for Writers

A sophisticated, AI-powered writing assistant that helps authors write full chapters based on simple summaries. Unlike other AI writing tools, this system prevents AI creativity by using AI only for deconstruction, research, and assembly of human-written content.

## Architecture

The system consists of three microservices:

### frontend_app (The Waiter)
Simple HTML interface where users provide story summaries and genres.

### ai_engine (The Head Chef)  
FastAPI Python server that manages the entire chapter creation process using specialized AI agents:
- **IntentAnalyst**: Creates chapter briefs defining tone, style, and character voice
- **SceneScout**: Deconstructs summaries into plot points and generates search queries
- **StyleAnalyst**: Researches writing styles for selected genres
- **MasterWeaver**: Weaves plot points with scraped human-written text
- **CorrectionPolishAI**: Edits and polishes the final chapter
- **CharacterExtractor**: Extracts and stores character details
- **LoreMaster**: Extracts and stores world-building details

### scraper_service (The Kitchen Porter)
Node.js server that scrapes the web for human-written descriptive text using Playwright.

## Workflow

1. User submits story summary and genre
2. IntentAnalyst creates chapter brief
3. SceneScout deconstructs into plot points and generates search queries
4. StyleAnalyst researches genre writing style
5. MasterWeaver weaves plot points with scraped content
6. CorrectionPolishAI edits the final chapter
7. CharacterExtractor and LoreMaster update knowledge base

## Installation

See individual service directories for setup instructions.
