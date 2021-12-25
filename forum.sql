CREATE TABLE IF NOT EXISTS events (
    event_id SERIAL PRIMARY KEY NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    date VARCHAR(50),
    time VARCHAR(50),
    url_local VARCHAR,
    event_link VARCHAR,
    timestamp VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS internships (
    intern_id SERIAL PRIMARY KEY NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    date VARCHAR(50),
    time VARCHAR(50),
    url_local VARCHAR,
    intern_link VARCHAR,
    timestamp VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS survey (
    survey_id SERIAL PRIMARY KEY NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    date VARCHAR(50),
    time VARCHAR(50),
    url_local VARCHAR,
    survey_link VARCHAR,
    timestamp VARCHAR(50)
);