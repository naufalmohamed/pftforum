import psycopg2
from configparser import ConfigParser
from urllib.parse import urlparse

config = ConfigParser()
config.read('config.cfg')

def create_tables():
    commands = [
    """
    CREATE TABLE IF NOT EXISTS cred (
        user_id SERIAL PRIMARY KEY NOT NULL,
        email VARCHAR(254) NOT NULL,
        password VARCHAR(18) NOT NULL,
        type VARCHAR(10) NOT NULL
    )
    """,
    """
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
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS therapist_cred (
        id SERIAL PRIMARY KEY REFERENCES cred(user_id) NOT NULL,
        first_name VARCHAR(30) NOT NULL,
        last_name VARCHAR(30) NOT NULL,
        languages VARCHAR NOT NULL,
        specializations VARCHAR NOT NULL,
        mode VARCHAR NOT NULL,
        medium VARCHAR NOT NULL,
        phonenumber VARCHAR NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS posts (
        post_id SERIAL PRIMARY KEY NOT NULL,
        user_id SERIAL REFERENCES cred(user_id) NOT NULL,
        title VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        tags VARCHAR(500) NOT NULL,
        date VARCHAR(50) NOT NULL,
        time VARCHAR(50) NOT NULL,
        likes INT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS matches (
        id SERIAL PRIMARY KEY NOT NULL,
        client_id SERIAL REFERENCES cred(user_id) NOT NULL,
        therapist_id SERIAL REFERENCES cred(user_id) NOT NULL,
        start_date VARCHAR(50) NOT NULL,
        end_date VARCHAR(50),
        status VARCHAR(20) NOT NULL
    )
    """,
    """
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
    """,
    """
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
    """,
    """
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
    """
]


    try:
        # Replace these with your actual database connection details
        result = urlparse(config['flask']['DB_URL'])
        username = result.username
        password = result.password
        database = result.path[1:]
        hostname = result.hostname
        port = result.port
        dbconn = psycopg2.connect(
            database=database,
            user=username,
            password=password,
            host=hostname,
            port=port
        )
        cursor = dbconn.cursor()
        for command in commands:
            cursor.execute(command)
        dbconn.commit()
        cursor.close()
        dbconn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

create_tables()
