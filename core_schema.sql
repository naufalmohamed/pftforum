CREATE TABLE IF NOT EXISTS cred (
    user_id SERIAL PRIMARY KEY NOT NULL,
    email VARCHAR(254) NOT NULL,
    password VARCHAR(18) NOT NULL,
    type VARCHAR(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS client_cred (
    id SERIAL PRIMARY KEY REFERENCES cred(user_id) NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    age VARCHAR(3),
    city VARCHAR(50),
    occupation VARCHAR(20),
    concerns VARCHAR,
    phonenumber VARCHAR(20),
    emergency_contact VARCHAR(20),
    relationship_status VARCHAR(50),
    status VARCHAR(15),
    therapist VARCHAR,
    timeperiod VARCHAR(50),
    gender VARCHAR(50)
);


CREATE TABLE IF NOT EXISTS therapist_cred (
    id SERIAL PRIMARY KEY REFERENCES cred(user_id) NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    languages VARCHAR NOT NULL,
    specializations VARCHAR NOT NULL,
    mode VARCHAR NOT NULL,
    medium VARCHAR NOT NULL,
    phonenumber VARCHAR NOT NULL
);



CREATE TABLE IF NOT EXISTS posts (
    post_id SERIAL PRIMARY KEY NOT NULL,
    user_id SERIAL REFERENCES cred(user_id) NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT(2000) COLLATE utf8_unicode_ci NOT NULL,
    tags VARCHAR(500) NOT NULL,
    date VARCHAR(50) NOT NULL,
    time VARCHAR(50) NOT NULL,
    likes INT
);


CREATE TABLE IF NOT EXISTS matches (
    id SERIAL PRIMARY KEY NOT NULL,
    client_id SERIAL REFERENCES cred(user_id) NOT NULL,
    therapist_id SERIAL REFERENCES cred(user_id) NOT NULL,
    start_date VARCHAR(50) NOT NULL,
    end_date VARCHAR(50),
    status VARCHAR(20) NOT NULL
);
