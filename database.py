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

    -- Vikter för kombinerad filmbetyg (en rad med id=1)
    CREATE TABLE IF NOT EXISTS rating_weights (
      id INTEGER PRIMARY KEY CHECK (id = 1),
      w_overall   REAL NOT NULL DEFAULT 0.40,
      w_emotional REAL NOT NULL DEFAULT 0.20,
      w_story     REAL NOT NULL DEFAULT 0.15,
      w_visuals   REAL NOT NULL DEFAULT 0.10,
      w_sound     REAL NOT NULL DEFAULT 0.05,
      w_cast_avg  REAL NOT NULL DEFAULT 0.10
    );
    INSERT OR IGNORE INTO rating_weights(id) VALUES (1);

    -- Snittbetyg på cast per film
    CREATE VIEW IF NOT EXISTS v_movie_cast_avg AS
    SELECT
      mc.movie_id,
      AVG(mc.actor_rating) AS cast_avg_rating,
      COUNT(*) AS cast_count
    FROM movie_cast mc
    GROUP BY mc.movie_id;

    -- Kombinerat filmbetyg (vikter × dina betyg + cast-snitt)
    CREATE VIEW IF NOT EXISTS v_movie_combined AS
    SELECT
      m.id AS movie_id,
      m.title,
      m.year,
      COALESCE(m.rating_overall,   0) * rw.w_overall
    + COALESCE(m.rating_emotional, 0) * rw.w_emotional
    + COALESCE(m.rating_story,     0) * rw.w_story
    + COALESCE(m.rating_visuals,   0) * rw.w_visuals
    + COALESCE(m.rating_sound,     0) * rw.w_sound
    + COALESCE(v.cast_avg_rating,  0) * rw.w_cast_avg
      AS combined_movie_rating,
      v.cast_avg_rating,
      v.cast_count
    FROM movies m
    LEFT JOIN v_movie_cast_avg v ON v.movie_id = m.id
    JOIN rating_weights rw ON rw.id = 1;

    -- Kombinerad karriärrating per skådis (snitt av deras roll-betyg)
    CREATE VIEW IF NOT EXISTS v_actor_combined AS
    SELECT
      a.id   AS actor_id,
      a.name AS actor_name,
      AVG(mc.actor_rating) AS actor_career_rating,
      COUNT(*)             AS roles_count
    FROM actors a
    JOIN movie_cast mc ON mc.actor_id = a.id
    GROUP BY a.id, a.name;
    """)
    c.commit()
    c.close()

# --------- Skriv/uppdatera data ---------

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

# --------- Läs/queries för menyn ---------

def search_movies(query, limit=20):
    """Sök film på titel (LIKE). Returnerar (id, title, year, rating_overall, combined)."""
    q = f"%{query}%"
    c = conn()
    cur = c.cursor()
    cur.execute("""
        SELECT m.id, m.title, m.year, m.rating_overall,
               ROUND(vc.combined_movie_rating, 3)
        FROM movies m
        LEFT JOIN v_movie_combined vc ON vc.movie_id = m.id
        WHERE m.title LIKE ?
        ORDER BY m.title
        LIMIT ?
    """, (q, limit))
    rows = cur.fetchall()
    c.close()
    return rows

def get_movie_details(movie_id):
    """Detaljer för film + castlista."""
    c = conn()
    cur = c.cursor()
    movie = cur.execute("""
        SELECT m.id, m.title, m.year, m.director, m.runtime_min,
               m.rating_overall, m.rating_emotional, m.rating_story, m.rating_visuals, m.rating_sound,
               ROUND(vc.combined_movie_rating, 3), ROUND(vc.cast_avg_rating, 3), IFNULL(vc.cast_count,0)
        FROM movies m
        LEFT JOIN v_movie_combined vc ON vc.movie_id = m.id
        WHERE m.id = ?
    """, (movie_id,)).fetchone()

    cast = cur.execute("""
        SELECT a.name, mc.character_name, mc.actor_rating
        FROM movie_cast mc
        JOIN actors a ON a.id = mc.actor_id
        WHERE mc.movie_id = ?
        ORDER BY a.name
    """, (movie_id,)).fetchall()
    c.close()
    return movie, cast

def search_actors(query, limit=20):
    """Sök skådis på namn. Returnerar (actor_id, actor_name, career_rating, roles_count)."""
    q = f"%{query}%"
    c = conn()
    cur = c.cursor()
    cur.execute("""
        SELECT a.id, a.name,
               ROUND(v.actor_career_rating, 3) AS career_rating,
               IFNULL(v.roles_count, 0) as roles_count
        FROM actors a
        LEFT JOIN v_actor_combined v ON v.actor_id = a.id
        WHERE a.name LIKE ?
        ORDER BY a.name
        LIMIT ?
    """, (q, limit))
    rows = cur.fetchall()
    c.close()
    return rows

def get_actor_details(actor_id):
    """Skådisens sammanfattning + roller."""
    c = conn()
    cur = c.cursor()
    summary = cur.execute("""
        SELECT a.id, a.name,
               ROUND(v.actor_career_rating, 3),
               IFNULL(v.roles_count, 0)
        FROM actors a
        LEFT JOIN v_actor_combined v ON v.actor_id = a.id
        WHERE a.id = ?
    """, (actor_id,)).fetchone()

    roles = cur.execute("""
        SELECT m.id, m.title, m.year, mc.character_name, mc.actor_rating
        FROM movie_cast mc
        JOIN movies m ON m.id = mc.movie_id
        WHERE mc.actor_id = ?
        ORDER BY m.year, m.title
    """, (actor_id,)).fetchall()
    c.close()
    return summary, roles

def top10_movies():
    """Top 10 filmer efter kombinerad rating (visar även overall)."""
    c = conn()
    cur = c.cursor()
    cur.execute("""
        SELECT m.id, m.title, m.year,
               ROUND(vc.combined_movie_rating, 3) AS combined,
               ROUND(m.rating_overall, 3) AS overall
        FROM movies m
        LEFT JOIN v_movie_combined vc ON vc.movie_id = m.id
        WHERE vc.combined_movie_rating IS NOT NULL
        ORDER BY vc.combined_movie_rating DESC, m.rating_overall DESC, m.year DESC, m.title
        LIMIT 10
    """)
    rows = cur.fetchall()
    c.close()
    return rows


def top_actors(min_movies=2, limit=10):
    """Top actors filtered by minimum number of movies."""
    c = conn()
    cur = c.cursor()
    cur.execute("""
        SELECT a.id, a.name,
               ROUND(v.actor_career_rating, 3) AS career_rating,
               v.roles_count
        FROM v_actor_combined v
        JOIN actors a ON a.id = v.actor_id
        WHERE v.roles_count >= ?
        ORDER BY v.actor_career_rating DESC, v.roles_count DESC, a.name
        LIMIT ?
    """, (min_movies, limit))
    rows = cur.fetchall()
    c.close()
    return rows


