CREATE TABLE mood_history (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    track_name TEXT NOT NULL,
    artist_name TEXT NOT NULL,
    mood TEXT NOT NULL,
    listened_at TIMESTAMP NOT NULL
);
