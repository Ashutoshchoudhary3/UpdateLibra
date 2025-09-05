


import sqlite3
import json
import asyncio
from typing import List, Dict, Any
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path: str = "writing_assistant.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Characters table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                backstory TEXT,
                personality TEXT,
                first_appearance TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Lore table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lore (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                significance TEXT,
                first_mentioned TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Style guides table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS style_guides (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                genre TEXT NOT NULL UNIQUE,
                style_description TEXT,
                tone_guidelines TEXT,
                common_tropes TEXT,
                writing_tips TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Chapter history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chapter_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                summary TEXT,
                genre TEXT,
                chapter_content TEXT,
                chapter_number INTEGER,
                previous_chapter_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (previous_chapter_id) REFERENCES chapter_history (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    async def store_characters(self, characters: List[Dict[str, Any]]):
        """Store character information in the database"""
        def _store():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for character in characters:
                cursor.execute('''
                    INSERT OR REPLACE INTO characters 
                    (name, description, backstory, personality, first_appearance)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    character.get('name'),
                    character.get('description'),
                    character.get('backstory'),
                    character.get('personality'),
                    character.get('first_appearance')
                ))
            
            conn.commit()
            conn.close()
        
        await asyncio.get_event_loop().run_in_executor(None, _store)
    
    async def store_lore(self, lore_entries: List[Dict[str, Any]]):
        """Store lore information in the database"""
        def _store():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for lore in lore_entries:
                cursor.execute('''
                    INSERT OR REPLACE INTO lore 
                    (category, name, description, significance, first_mentioned)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    lore.get('category'),
                    lore.get('name'),
                    lore.get('description'),
                    lore.get('significance'),
                    lore.get('first_mentioned')
                ))
            
            conn.commit()
            conn.close()
        
        await asyncio.get_event_loop().run_in_executor(None, _store)
    
    async def get_style_guide(self, genre: str) -> Dict[str, Any]:
        """Get style guide for a specific genre"""
        def _get():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT style_description, tone_guidelines, common_tropes, writing_tips
                FROM style_guides
                WHERE genre = ?
            ''', (genre,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'style_description': result[0],
                    'tone_guidelines': result[1],
                    'common_tropes': result[2],
                    'writing_tips': result[3]
                }
            return None
        
        return await asyncio.get_event_loop().run_in_executor(None, _get)
    
    async def store_style_guide(self, genre: str, style_guide: Dict[str, Any]):
        """Store style guide for a specific genre"""
        def _store():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO style_guides 
                (genre, style_description, tone_guidelines, common_tropes, writing_tips)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                genre,
                style_guide.get('style_description'),
                style_guide.get('tone_guidelines'),
                style_guide.get('common_tropes'),
                style_guide.get('writing_tips')
            ))
            
            conn.commit()
            conn.close()
        
        await asyncio.get_event_loop().run_in_executor(None, _store)
    
    async def get_character_info(self, character_name: str) -> Dict[str, Any]:
        """Get information about a specific character"""
        def _get():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT name, description, backstory, personality, first_appearance
                FROM characters
                WHERE name LIKE ?
            ''', (f'%{character_name}%',))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'name': result[0],
                    'description': result[1],
                    'backstory': result[2],
                    'personality': result[3],
                    'first_appearance': result[4]
                }
            return None
        
        return await asyncio.get_event_loop().run_in_executor(None, _get)
    
    async def store_chapter(self, summary: str, genre: str, chapter_content: str, chapter_number: int = 1, previous_chapter_id: int = None):
        """Store generated chapter in history"""
        def _store():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO chapter_history (summary, genre, chapter_content, chapter_number, previous_chapter_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (summary, genre, chapter_content, chapter_number, previous_chapter_id))
            
            conn.commit()
            conn.close()
        
        await asyncio.get_event_loop().run_in_executor(None, _store)
    
    async def get_latest_chapter(self) -> Dict[str, Any]:
        """Get the most recently created chapter"""
        def _get():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, summary, genre, chapter_content, chapter_number, previous_chapter_id, created_at
                FROM chapter_history
                ORDER BY created_at DESC
                LIMIT 1
            ''')
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'id': result[0],
                    'summary': result[1],
                    'genre': result[2],
                    'chapter_content': result[3],
                    'chapter_number': result[4],
                    'previous_chapter_id': result[5],
                    'created_at': result[6]
                }
            return None
        
        return await asyncio.get_event_loop().run_in_executor(None, _get)
    
    async def get_chapter_by_id(self, chapter_id: int) -> Dict[str, Any]:
        """Get a specific chapter by ID"""
        def _get():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, summary, genre, chapter_content, chapter_number, previous_chapter_id, created_at
                FROM chapter_history
                WHERE id = ?
            ''', (chapter_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'id': result[0],
                    'summary': result[1],
                    'genre': result[2],
                    'chapter_content': result[3],
                    'chapter_number': result[4],
                    'previous_chapter_id': result[5],
                    'created_at': result[6]
                }
            return None
        
        return await asyncio.get_event_loop().run_in_executor(None, _get)
    
    async def list_chapters(self) -> List[Dict[str, Any]]:
        """List all chapters"""
        def _list():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, summary, genre, chapter_content, chapter_number, previous_chapter_id, created_at
                FROM chapter_history
                ORDER BY created_at DESC
            ''')
            
            results = cursor.fetchall()
            conn.close()
            
            chapters = []
            for result in results:
                chapters.append({
                    'id': result[0],
                    'summary': result[1],
                    'genre': result[2],
                    'chapter_content': result[3],
                    'chapter_number': result[4],
                    'previous_chapter_id': result[5],
                    'created_at': result[6]
                })
            
            return chapters
        
        return await asyncio.get_event_loop().run_in_executor(None, _list)


