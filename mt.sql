DROP TABLE posts;

CREATE TABLE IF NOT EXISTS posts (
    post_id SERIAL PRIMARY KEY NOT NULL,
    user_id SERIAL REFERENCES cred(user_id) NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    tags VARCHAR(500) NOT NULL,
    date VARCHAR(50) NOT NULL,
    time VARCHAR(50) NOT NULL,
    likes INT NOT NULL);