CREATE DATABASE recensio;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(100),
    lastname VARCHAR(100),
    username VARCHAR(100),
    email VARCHAR(255),
    password TEXT,
    pfp BYTEA
);

  -- Movies/Shows Table - Store our custom data per movie/show
CREATE TABLE content (
    id SERIAL PRIMARY KEY,
    tmdb_id INTEGER NOT NULL UNIQUE,  -- TMDB's unique ID
    media_type VARCHAR(10) NOT NULL,  -- 'movie' or 'tv'
    title VARCHAR(500) NOT NULL,
    poster_path VARCHAR(500),
    backdrop_path VARCHAR(500),
    release_date DATE,
    watched_count INTEGER DEFAULT 0,  -- How many users marked as watched
    list_count INTEGER DEFAULT 0,     -- How many lists it appears in
    avg_score DECIMAL(5,2) DEFAULT 0, -- Average score 0-100 with 2 decimals
    total_scores INTEGER DEFAULT 0,   -- For calculating average
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User watched status
CREATE TABLE user_watched (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content_id INTEGER NOT NULL REFERENCES content(id) ON DELETE CASCADE,
    watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, content_id)
);

-- User ratings/scores
CREATE TABLE user_ratings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content_id INTEGER NOT NULL REFERENCES content(id) ON DELETE CASCADE,
    score INTEGER NOT NULL CHECK (score >= 0 AND score <= 100),
    rated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, content_id)
);

ALTER TABLE user_ratings 
ADD COLUMN review_text TEXT;

-- Lists table
CREATE TABLE user_lists (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    is_public BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- List items
CREATE TABLE list_items (
    id SERIAL PRIMARY KEY,
    list_id INTEGER NOT NULL REFERENCES user_lists(id) ON DELETE CASCADE,
    content_id INTEGER NOT NULL REFERENCES content(id) ON DELETE CASCADE,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(list_id, content_id)
);

-- Create indexes for performance
CREATE INDEX idx_content_tmdb_id ON content(tmdb_id);
CREATE INDEX idx_content_media_type ON content(media_type);
CREATE INDEX idx_user_watched_user_id ON user_watched(user_id);
CREATE INDEX idx_user_watched_content_id ON user_watched(content_id);
CREATE INDEX idx_user_ratings_user_id ON user_ratings(user_id);
CREATE INDEX idx_user_ratings_content_id ON user_ratings(content_id);
CREATE INDEX idx_list_items_list_id ON list_items(list_id);
CREATE INDEX idx_list_items_content_id ON list_items(content_id);