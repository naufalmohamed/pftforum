from urllib.parse import urlparse
import psycopg2

def parse():
	result = urlparse("postgres://tflhplllsjtczu:d05ce0107a96ea44fe7e7b5d435bf3042388baf0fa08dc5bc488d7c6389057c4@ec2-3-217-91-165.compute-1.amazonaws.com:5432/dd2lj96965ak4q")
	username = result.username
	password = result.password
	database = result.path[1:]
	hostname = result.hostname
	port = result.port
	return username, password, database, hostname, port


username, password, database, hostname, port = parse()
dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
cursor = dbconn.cursor()
# sql = open("mt.sql", "r").read()
# cursor.execute(sql)
cursor.execute(f'''SELECT * FROM client_cred;''')
pl = cursor.fetchall()
print(pl)
# print(len(pl))
# cursor.execute(f"""INSERT INTO cred (email, password, type) VALUES (%s,%s,%s);""",('ramu@dubakoor.com','Ramu@123','therapist'))
# cursor.execute(f"""INSERT INTO cred (email, password, type) VALUES (%s,%s,%s);""",('madhan@dubakoor.com','Madhan@123','client'))
# cursor.execute(f'''DELETE FROM posts;''')
dbconn.commit()