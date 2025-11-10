import sqlite3

# Öppna eller skapa en databasfil
conn = sqlite3.connect("data/FrameRate.db")

# Skapa en cursor för att köra SQL-kommandon
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS movies (
  id               INTEGER PRIMARY KEY AUTOINCREMENT,
  title            TEXT NOT NULL,
  year             INTEGER,
  director         TEXT,
  runtime_min      INTEGER,
  rating_overall   REAL,
  rating_emotional REAL,
  rating_story     REAL,
  rating_visuals   REAL,
  rating_sound     REAL
);

-- People (actors/actresses)
CREATE TABLE IF NOT EXISTS actors (
  id   INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);

-- Link actors ↔ movies, with per-actor-per-movie ratings
CREATE TABLE IF NOT EXISTS movie_cast (
  movie_id        INTEGER NOT NULL,
  actor_id        INTEGER NOT NULL,
  character_name  TEXT,
  actor_rating    REAL,
  PRIMARY KEY (movie_id, actor_id),
  FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
  FOREIGN KEY (actor_id) REFERENCES actors(id) ON DELETE CASCADE
);

-- Weights for the combined movie rating (single-row table so you can tweak easily)
CREATE TABLE IF NOT EXISTS rating_weights (
  id                  INTEGER PRIMARY KEY CHECK (id = 1),
  w_overall           REAL NOT NULL DEFAULT 0.40,
  w_emotional         REAL NOT NULL DEFAULT 0.20,
  w_story             REAL NOT NULL DEFAULT 0.15,
  w_visuals           REAL NOT NULL DEFAULT 0.10,
  w_sound             REAL NOT NULL DEFAULT 0.05,
  w_cast_avg          REAL NOT NULL DEFAULT 0.10
);

-- Ensure one row exists
INSERT OR IGNORE INTO rating_weights(id) VALUES (1);

CREATE INDEX IF NOT EXISTS idx_movie_cast_movie ON movie_cast(movie_id);
CREATE INDEX IF NOT EXISTS idx_movie_cast_actor ON movie_cast(actor_id);
""")

conn.commit()  # sparar ändringar
