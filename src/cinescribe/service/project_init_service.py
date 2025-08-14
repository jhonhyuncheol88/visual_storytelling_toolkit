from __future__ import annotations

import os
import sqlite3
from typing import Optional


class ProjectInitService:
    def create_new_project(self, db_path: str, title: Optional[str] = None) -> None:
        os.makedirs(os.path.dirname(os.path.abspath(db_path)) or ".", exist_ok=True)
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            # Core tables (minimal columns to start)
            cur.executescript(
                """
                PRAGMA foreign_keys=ON;
                CREATE TABLE IF NOT EXISTS Project_Info (
                  id INTEGER PRIMARY KEY CHECK (id=1),
                  title TEXT NOT NULL,
                  logline TEXT DEFAULT '',
                  synopsis TEXT DEFAULT '',
                  intent TEXT DEFAULT '',
                  review_notes TEXT DEFAULT '',
                  created_at TEXT DEFAULT (datetime('now')),
                  updated_at TEXT
                );

                CREATE TABLE IF NOT EXISTS Characters (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  age TEXT,
                  job TEXT,
                  personality TEXT,
                  goal TEXT,
                  conflict TEXT,
                  design_prompt TEXT,
                  image_asset_id INTEGER,
                  created_at TEXT DEFAULT (datetime('now')),
                  updated_at TEXT
                );

                CREATE TABLE IF NOT EXISTS Scenes (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  number INTEGER,
                  name TEXT,
                  location TEXT,
                  time_of_day TEXT,
                  summary TEXT,
                  sort_index INTEGER,
                  created_at TEXT DEFAULT (datetime('now')),
                  updated_at TEXT
                );

                CREATE TABLE IF NOT EXISTS Shots (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  scene_id INTEGER NOT NULL,
                  code TEXT,
                  description TEXT,
                  shot_type TEXT,
                  angle TEXT,
                  movement TEXT,
                  lens TEXT,
                  lighting TEXT,
                  image_prompt TEXT,
                  video_prompt TEXT,
                  storyboard_asset_id INTEGER,
                  sort_index INTEGER,
                  duration_sec REAL,
                  created_at TEXT DEFAULT (datetime('now')),
                  updated_at TEXT,
                  FOREIGN KEY(scene_id) REFERENCES Scenes(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS Audio_Cues (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  shot_id INTEGER NOT NULL,
                  cue_type TEXT,
                  style_prompt TEXT,
                  lyrics_prompt TEXT,
                  start_offset_sec REAL,
                  duration_sec REAL,
                  asset_id INTEGER,
                  created_at TEXT DEFAULT (datetime('now')),
                  updated_at TEXT,
                  FOREIGN KEY(shot_id) REFERENCES Shots(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS Assets (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  kind TEXT,
                  original_path TEXT,
                  project_path TEXT,
                  filename TEXT,
                  ext TEXT,
                  width INTEGER,
                  height INTEGER,
                  duration_sec REAL,
                  hash_sha256 TEXT,
                  tags TEXT,
                  created_at TEXT DEFAULT (datetime('now')),
                  thumbnail_path TEXT
                );
                CREATE UNIQUE INDEX IF NOT EXISTS idx_assets_hash ON Assets(hash_sha256);
                
                -- Text/JSON documents for narrative and other structured notes
                CREATE TABLE IF NOT EXISTS Documents (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  key TEXT NOT NULL UNIQUE,
                  format TEXT NOT NULL CHECK (format IN ('json','text')),
                  content TEXT NOT NULL,
                  updated_at TEXT DEFAULT (datetime('now'))
                );
                CREATE INDEX IF NOT EXISTS idx_documents_key ON Documents(key);
                """
            )
            if title is None:
                title = os.path.splitext(os.path.basename(db_path))[0]
            # Upsert single row into Project_Info (id=1)
            cur.execute(
                "INSERT INTO Project_Info(id, title) VALUES(1, ?) ON CONFLICT(id) DO UPDATE SET title=excluded.title",
                (title,),
            )
            conn.commit()


