import sqlite3

DB_PATH = "data/FrameRate.db"

def conn():
    c = sqlite3.connect(DB_PATH)
    c.execute("PRAGMA foreign_keys = ON;")
    return c

def init_db():
    c = conn()
    cur = c.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS movies (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      year INTEGER,
      director TEXT,
      runtime_min INTEGER,
      rating_overall REAL,
      rating_emotional REAL,
      rating_story REAL,
      rating_visuals REAL,
      rating_sound REAL
    );

    CREATE TABLE IF NOT EXISTS actors (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS movie_cast (
      movie_id INTEGER NOT NULL,
      actor_id INTEGER NOT NULL,
      character_name TEXT,
      actor_rating REAL,
      PRIMARY KEY (movie_id, actor_id),
      FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
      FOREIGN KEY (actor_id) REFERENCES actors(id) ON DELETE CASCADE
    );
    """)
    c.commit()
    c.close()

def add_movie(title, year, director, runtime_min,
              rating_overall, rating_emotional,
              rating_story, rating_visuals, rating_sound):
    c = conn()
    cur = c.cursor()
    cur.execute("""
        INSERT INTO movies
        (title, year, director, runtime_min,
         rating_overall, rating_emotional, rating_story, rating_visuals, rating_sound)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (title, year, director, runtime_min,
          rating_overall, rating_emotional, rating_story, rating_visuals, rating_sound))
    c.commit()
    movie_id = cur.lastrowid
    c.close()
    return movie_id

def get_or_create_actor(name):
    c = conn()
    cur = c.cursor()
    cur.execute("INSERT OR IGNORE INTO actors(name) VALUES(?)", (name,))
    cur.execute("SELECT id FROM actors WHERE name = ?", (name,))
    actor_id = cur.fetchone()[0]
    c.commit()
    c.close()
    return actor_id

def add_actor_to_movie(movie_id, actor_name, character_name, actor_rating):
    actor_id = get_or_create_actor(actor_name)
    c = conn()
    c.execute("""
        INSERT OR REPLACE INTO movie_cast(movie_id, actor_id, character_name, actor_rating)
        VALUES (?, ?, ?, ?)
    """, (movie_id, actor_id, character_name, actor_rating))
    c.commit()
    c.close()
