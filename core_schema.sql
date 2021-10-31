CREATE TABLE IF NOT EXISTS user_cred (
    user_id SERIAL PRIMARY KEY NOT NULL,
    email VARCHAR(254) NOT NULL,
    password VARCHAR(18) NOT NULL,
    type VARCHAR(10) NOT NULL
);

DROP TABLE posts;

CREATE TABLE IF NOT EXISTS posts (
    post_id SERIAL PRIMARY KEY NOT NULL,
    title VARCHAR(100) NOT NULL,
    content VARCHAR(2000) NOT NULL,
    user_id SERIAL REFERENCES user_cred(user_id),
    tags VARCHAR(500),
    time_stamp VARCHAR(50)
);

