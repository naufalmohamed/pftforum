CREATE TABLE IF NOT EXISTS posts (
    post_id SERIAL PRIMARY KEY NOT NULL,
    user_id SERIAL REFERENCES cred(user_id) NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    tags VARCHAR(500) NOT NULL,
    date VARCHAR(50) NOT NULL,
    time VARCHAR(50) NOT NULL,
    likes INT NOT NULL);

INSERT INTO survey (title,description,date,time,survey_link) 
VALUES ('OCD','OCD durvey','12/12/21','9:00 - 10:00','ocd.pft');

INSERT INTO survey (title,description,date,time,survey_link) 
VALUES ('Behavioural Survey','survey on behaviour','12/01/21','9:00 - 10:00','benny.pft');

INSERT INTO survey (title,description,date,time,survey_link) 
VALUES ('PTSD Survey','survey on google','13/12/22','12:00 - 13:00','film.pft');