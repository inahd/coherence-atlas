import sqlite3, time
from pathlib import Path

DB = Path("/opt/atlas/memory/corpus.db")

SCHEMA = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS files (
  sha256 TEXT PRIMARY KEY,
  path TEXT NOT NULL,
  size INTEGER NOT NULL,
  mtime INTEGER NOT NULL,
  kind TEXT NOT NULL,              -- pdf|txt|html|zip|other
  status TEXT NOT NULL DEFAULT 'new',  -- new|extracted|harvested
  added_ts INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS passages (
  passage_id TEXT PRIMARY KEY,
  source_sha256 TEXT NOT NULL,
  locator TEXT NOT NULL,
  excerpt TEXT NOT NULL,
  tags TEXT NOT NULL,
  added_ts INTEGER NOT NULL,
  FOREIGN KEY(source_sha256) REFERENCES files(sha256)
);

CREATE TABLE IF NOT EXISTS staged_relations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  from_id TEXT NOT NULL,
  relation TEXT NOT NULL,
  to_id TEXT NOT NULL,
  source_sha256 TEXT NOT NULL,
  locator TEXT NOT NULL,
  excerpt TEXT NOT NULL,
  score REAL NOT NULL,
  status TEXT NOT NULL DEFAULT 'staged', -- staged|accepted|rejected|applied
  added_ts INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_passages_tags ON passages(tags);
CREATE INDEX IF NOT EXISTS idx_staged_status ON staged_relations(status);
"""

def connect():
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    return con

def init():
    con = connect()
    con.executescript(SCHEMA)
    con.commit()
    con.close()
    print("Initialized:", DB)

if __name__ == "__main__":
    init()
