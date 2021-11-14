from flask import Flask, render_template, url_for, redirect, request, session, flash
from urllib.parse import urlparse
import psycopg2
from datetime import date, datetime

app = Flask(__name__)
app.secret_key = 'hello_WORLD_##$$'


def parse():
	result = urlparse("postgres://tflhplllsjtczu:d05ce0107a96ea44fe7e7b5d435bf3042388baf0fa08dc5bc488d7c6389057c4@ec2-3-217-91-165.compute-1.amazonaws.com:5432/dd2lj96965ak4q")
	username = result.username
	password = result.password
	database = result.path[1:]
	hostname = result.hostname
	port = result.port
	return username, password, database, hostname, port


@app.route('/login_page_client')
def login_page_client():
    if 'user' in session:
            flash('User Already in Session! Logout To Continue as a Different User!')
            if session['user_type'] == 'therapist':
                return redirect(url_for('index'))
            else:
                return redirect(url_for('index'))
    else:
        return render_template('login_page_client.html')
   

@app.route('/login', methods=['POST'])
def login():
    try:
        if 'user' in session:
            flash('User Already in Session! Logout To Continue as a Different User!')
            if session['user_type'] == 'therapist':
                return redirect(url_for('index'))
            else:
                return redirect(url_for('index'))
        else:
            if request.method == 'POST':
                session.pop('user', None)
                username, password, database, hostname, port = parse()
                email = request.form.get("email")
                psw = request.form.get("psw")
                login_type = request.form.get("login_type")
                if login_type == "therapist":
                    try:
                        dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
                        cursor = dbconn.cursor()
                        cursor.execute(f"SELECT * FROM user_cred WHERE email = %s AND type = 'therapist';",[email])
                        cred = cursor.fetchall()
                        dbconn.commit()
                    except:
                        flash('User Doesnt Exist!')
                        return redirect(url_for("login_page_client"))

                    if cred[0][2] == psw:
                        session['user'] = email
                        session['id'] = cred[0][0]
                        session['user_type'] = 'therapist'
                        return redirect(url_for('profile'))
                    else:
                        flash('Bad Credentials! Try Again!')
                        return redirect(url_for('login_page'))     
                else:
                    try:
                        dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
                        cursor = dbconn.cursor()
                        cursor.execute(f"SELECT * FROM user_cred WHERE email = %s AND type = 'client';",[email])
                        cred = cursor.fetchall()
                        dbconn.commit()
                    except:
                        flash('User Doesnt Exist!')
                        return redirect(url_for("login_page_client"))

                    if cred[0][2] == psw:
                        session['user'] = email
                        session['id'] = cred[0][0]
                        session['user_type'] = 'client'

                        return redirect(url_for('profile'))
                    else:
                        flash('Bad Credentials! Try Again!')
                        return redirect(url_for('login_page_client'))
    except Exception as e:
        flash('Something Went Wrong! Try Again!')
        return redirect(url_for('login_page_client'))


@app.route('/')
def index():
    return render_template('index2.html')


@app.route("/add_new")
def add_new():
	return render_template("note.html")
	
	
@app.route("/add", methods=["POST"])
def todo_add_to_table():
    email = session['user']
    username, password, database, hostname, port = parse()
    title_ret= request.form.get("title")
    tags_ret= request.form.get("tags")
    tags = tags_ret
    description_ret= request.form.get("description")
    time = datetime.now()
	
    if len(title_ret) == 0 and len(description_ret) == 0:
        return redirect(url_for("profile"))
            
    else:		
        dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
        cursor = dbconn.cursor()
        cursor.execute(f"""INSERT INTO posts (title,time_stamp,tags,content,user_id) VALUES (%s,%s,%s,%s,%s);""",(title_ret,time,tags,description_ret,session['id']))
        dbconn.commit()
        return redirect(url_for("profile"))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/profile')
def profile():
	email = session['user']
	username, password, database, hostname, port = parse()
	dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
	cursor = dbconn.cursor()
	cursor.execute(f"SELECT * FROM posts;")
	posts = cursor.fetchall()
	dbconn.commit()
	return render_template("profile.html", email=email, posts=posts)


if __name__ == '__main__':
    app.run(debug=True)