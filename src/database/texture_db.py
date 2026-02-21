"""
Database Indexing System
SQLite-based indexing for massive texture libraries (200,000+ files)
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class TextureDatabase:
    """Database manager for texture indexing"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize database connection and create tables"""
        self.conn = sqlite3.connect(str(self.db_path))
        self.cursor = self.conn.cursor()
        
        # Create textures table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS textures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT UNIQUE NOT NULL,
                filename TEXT NOT NULL,
                file_size INTEGER,
                width INTEGER,
                height INTEGER,
                format TEXT,
                category TEXT,
                confidence REAL,
                lod_group TEXT,
                lod_level TEXT,
                hash TEXT,
                is_corrupted BOOLEAN DEFAULT 0,
                date_added TEXT,
                date_modified TEXT,
                last_classified TEXT
            )
        ''')
        
        # Create index for faster searches
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_category ON textures(category)
        ''')
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_filename ON textures(filename)
        ''')
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_lod_group ON textures(lod_group)
        ''')
        
        # Create settings table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        # Create operations log table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS operations_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                operation TEXT,
                file_path TEXT,
                status TEXT,
                details TEXT
            )
        ''')
        
        self.conn.commit()
    
    def add_texture(self, file_path: Path, metadata: dict) -> bool:
        """Add or update texture in database"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO textures 
                (file_path, filename, file_size, width, height, format, category, 
                 confidence, lod_group, lod_level, hash, is_corrupted, date_added, 
                 date_modified, last_classified)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                str(file_path),
                file_path.name,
                metadata.get('file_size', 0),
                metadata.get('width', 0),
                metadata.get('height', 0),
                metadata.get('format', ''),
                metadata.get('category', 'unclassified'),
                metadata.get('confidence', 0.0),
                metadata.get('lod_group', ''),
                metadata.get('lod_level', ''),
                metadata.get('hash', ''),
                metadata.get('is_corrupted', False),
                metadata.get('date_added', datetime.now().isoformat()),
                metadata.get('date_modified', datetime.now().isoformat()),
                datetime.now().isoformat()
            ))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error adding texture to database: {e}")
            return False
    
    def get_texture(self, file_path: Path) -> Optional[dict]:
        """Get texture metadata from database"""
        self.cursor.execute('SELECT * FROM textures WHERE file_path = ?', (str(file_path),))
        row = self.cursor.fetchone()
        
        if row:
            columns = [desc[0] for desc in self.cursor.description]
            return dict(zip(columns, row))
        return None
    
    def search_textures(self, category: Optional[str] = None, 
                       lod_group: Optional[str] = None,
                       filename_pattern: Optional[str] = None) -> List[dict]:
        """Search textures with filters"""
        query = 'SELECT * FROM textures WHERE 1=1'
        params = []
        
        if category:
            query += ' AND category = ?'
            params.append(category)
        
        if lod_group:
            query += ' AND lod_group = ?'
            params.append(lod_group)
        
        if filename_pattern:
            query += ' AND filename LIKE ?'
            params.append(f'%{filename_pattern}%')
        
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    
    def get_statistics(self) -> dict:
        """Get database statistics"""
        stats = {}
        
        # Total textures
        self.cursor.execute('SELECT COUNT(*) FROM textures')
        stats['total_textures'] = self.cursor.fetchone()[0]
        
        # By category
        self.cursor.execute('SELECT category, COUNT(*) FROM textures GROUP BY category')
        stats['by_category'] = dict(self.cursor.fetchall())
        
        # By format
        self.cursor.execute('SELECT format, COUNT(*) FROM textures GROUP BY format')
        stats['by_format'] = dict(self.cursor.fetchall())
        
        # Total size
        self.cursor.execute('SELECT SUM(file_size) FROM textures')
        stats['total_size_bytes'] = self.cursor.fetchone()[0] or 0
        
        # Corrupted files
        self.cursor.execute('SELECT COUNT(*) FROM textures WHERE is_corrupted = 1')
        stats['corrupted_count'] = self.cursor.fetchone()[0]
        
        return stats
    
    def log_operation(self, operation: str, file_path: Path, status: str, details: str = ""):
        """Log an operation"""
        try:
            self.cursor.execute('''
                INSERT INTO operations_log (timestamp, operation, file_path, status, details)
                VALUES (?, ?, ?, ?, ?)
            ''', (datetime.now().isoformat(), operation, str(file_path), status, details))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error logging operation: {e}")
    
    def get_recent_operations(self, limit: int = 100) -> List[dict]:
        """Get recent operations log"""
        self.cursor.execute('''
            SELECT * FROM operations_log 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    
    def clear_database(self):
        """Clear all texture records (but keep schema)"""
        self.cursor.execute('DELETE FROM textures')
        self.cursor.execute('DELETE FROM operations_log')
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
