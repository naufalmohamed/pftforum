from flask import Flask, render_template, url_for, redirect, request, session, flash
from urllib.parse import urlparse
import psycopg2
from datetime import date, datetime
import html
import random

app = Flask(__name__)
app.secret_key = 'hello_WORLD_##$$'

avatar_names = ['Peter Parker', 'Bruce Wayne', 'Stephen Strange', 'Clark Kent', 'Natasha Romanoff']

def parse(): #parses through the DB Creds (gotta find a better method)
	result = urlparse("postgres://tflhplllsjtczu:d05ce0107a96ea44fe7e7b5d435bf3042388baf0fa08dc5bc488d7c6389057c4@ec2-3-217-91-165.compute-1.amazonaws.com:5432/dd2lj96965ak4q")
	username = result.username
	password = result.password
	database = result.path[1:]
	hostname = result.hostname
	port = result.port
	return username, password, database, hostname, port


########################################### Login Stuff #####################################
@app.route('/login_page_client') #Renders Login Page
def login_page_client():
    if 'user' in session:
            flash('User Already in Session! Logout To Continue as a Different User!')
            if session['user_type'] == 'therapist':
                return redirect(url_for('index'))
            else:
                return redirect(url_for('index'))
    else:
        return render_template('login_page_client.html')
   

@app.route('/login', methods=['POST']) #The actual login process
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
                        cursor.execute(f"SELECT * FROM cred WHERE email = %s AND type = 'therapist';",[email])
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
                        cursor.execute(f"SELECT * FROM cred WHERE email = %s AND type = 'client';",[email])
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


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


########################################### Register Stuff #####################################


@app.route('/register_client_page')
def register_client_page():
    return render_template('register.html')


@app.route('/register_client', methods=['POST'])
def register_client():
    if request.method == 'POST':
        username, password, database, hostname, port = parse()
        email = request.form.get("email")
        psw = request.form.get("psw")
        psw_repeat = request.form.get("psw_repeat")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        if psw != psw_repeat:
            flash('Passwords Dont Match!')
            return redirect(url_for('register_client_page'))
        else:
            if len(psw) < 8:
                flash('Password Must be 8 Characters Long!')
                return redirect(url_for('register_client_page'))
            else:
                dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
                cursor = dbconn.cursor()
                cursor.execute(f'''SELECT user_id FROM cred WHERE email = %s ;''',[email])
                cl = cursor.fetchall()
                if len(cl) == 0:
                    cursor.execute(f"""INSERT INTO cred (email, password, type) VALUES (%s,%s,%s);""",(email,psw,'client'))
                    cursor.execute(f'''SELECT user_id FROM cred WHERE email = %s ;''',[email])
                    id = cursor.fetchall()
                    cursor.execute(f"""INSERT INTO client_cred (id, first_name, last_name) VALUES (%s,%s,%s);""",(id[0][0],first_name,last_name))
                    dbconn.commit()
                    return redirect('login_page_client')
                else:
                    dbconn.commit()
                    flash('User Already Exists!')
                    return redirect(url_for('register_client_page'))



########################################### Index Stuff #####################################

@app.route('/')
def index():
    return render_template('index2.html')


########################################### Profile Stuff #####################################

@app.route('/profile')
def profile():
    if 'user' in session:
        email = session['user']
        username, password, database, hostname, port = parse()
        dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
        cursor = dbconn.cursor()
        cursor.execute(f"SELECT * FROM posts;")
        posts = cursor.fetchall()

        dbconn.commit()
        return render_template("profile.html", email=email, posts=posts, user_type = session['user_type'], avatar_name = random.choice(avatar_names))
    else:
        username, password, database, hostname, port = parse()
        dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
        cursor = dbconn.cursor()
        cursor.execute(f"SELECT * FROM posts;")
        posts = cursor.fetchall()

        dbconn.commit()
        return render_template("profile.html", posts=posts, avatar_name = random.choice(avatar_names))

@app.route('/info')
def info():
    username, password, database, hostname, port = parse()
    dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
    cursor = dbconn.cursor()
    cursor.execute(f"""SELECT * FROM client_cred WHERE id = %s""",[session['id']])
    data = cursor.fetchall()
    info = []
    for i in data[0][1:]:
        info.append(i)

    return render_template('info.html', info = info, email = session['user'], user_type = session['user_type'])


@app.route('/edit')
def edit():
    return render_template('edit.html')


@app.route('/edit_info', methods=['POST'])
def edit_info():
    if request.method == 'POST':
        user_dict = {}
        user_dict['first_name'] = request.form.get('first_name')
        user_dict['last_name'] = request.form.get('last_name')
        user_dict['phonenumber'] = request.form.get('phonenumber')
        user_dict['age'] = request.form.get('age')
        user_dict['city'] = request.form.get('city')
        user_dict['occupation'] = request.form.get('occupation')
        user_dict['concerns'] = request.form.get('concerns')
        user_dict['relationship_status'] = request.form.get('relationship_status')
        user_dict['timeperiod'] = request.form.get('timeperiod')
        user_dict['gender'] = request.form.get('gender')
        user_dict['emergency_contact'] = request.form.get('emergency_contact')
        username, password, database, hostname, port = parse()
        dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
        cursor = dbconn.cursor()
        cursor.execute(f'''DELETE FROM client_cred WHERE id = %s''',[session['id']])
        cursor.execute(f'''INSERT INTO client_cred 
                            (first_name,last_name,phonenumber,age,city,occupation,concerns,relationship_status,timeperiod,emergency_contact,id,gender,status) 
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
                            ,(
                                user_dict['first_name'],
                                user_dict['last_name'],
                                user_dict['phonenumber'],
                                user_dict['age'],
                                user_dict['city'],
                                user_dict['occupation'],
                                user_dict['concerns'],
                                user_dict['relationship_status'],
                                user_dict['timeperiod'],
                                user_dict['emergency_contact'],
                                session['id'],
                                user_dict['gender'],
                                'completed'
                            ))
        dbconn.commit()
        return redirect(url_for('profile'))

    

@app.route("/add_new")
def add_new():
	return render_template("note.html", user_type = session['user_type'])
	
	
@app.route("/add", methods=["POST"])
def add():
    email = session['user']
    username, password, database, hostname, port = parse()
    title_ret= request.form.get("title")
    tags_ret= request.form.get("tags")
    tags = tags_ret
    description_ret= request.form.get("description")
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    zero = 0
	
    if len(title_ret) == 0 and len(description_ret) == 0:
        return redirect(url_for("profile"))
            
    else:		
        dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
        cursor = dbconn.cursor()
        cursor.execute(f"""INSERT INTO posts (title,tags,description,user_id,date,time,likes) VALUES (%s,%s,%s,%s,%s,%s,%s);""",(title_ret,tags,description_ret,session['id'],today,current_time,zero))
        dbconn.commit()
        return redirect(url_for("profile"))


@app.route('/peace/<int:post_id>')
def peace(post_id):
    username, password, database, hostname, port = parse()
    dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
    cursor = dbconn.cursor()
    cursor.execute(f'''SELECT likes FROM posts WHERE post_id = %s''',[post_id])
    likes = cursor.fetchall()
    cursor.execute(f"""UPDATE posts SET likes = %s WHERE post_id = %s;""",(likes[0][0]+1,post_id))
    dbconn.commit()
    return redirect(url_for('profile'))


@app.route('/ad_listing')
def ad_listing():
    if 'user' in session:
        return render_template('ad_listing.html', user_type = session['user_type'])
    else:
        return render_template('ad_listing.html')

@app.route('/intern_listing')
def intern_listing():
    return render_template("intern_listing.html", user_type = session['user_type'])


@app.route('/shoutitout')
def shoutitout():
    return render_template('shoutitout.html', user_type = session['user_type'])


@app.route('/test2')
def test2():
    return render_template('test2.html')


########################################### Profile Stuff #####################################

@app.route('/interested_therapists')
def interested_therapists():
    username, password, database, hostname, port = parse()
    dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
    cursor = dbconn.cursor()
    cursor.execute(f'''SELECT status FROM client_cred WHERE id = %s''',[session['id']])
    status = cursor.fetchall()
    dbconn.commit()
    return render_template('interested_therapists.html', status = status, user_type = session['user_type'])


@app.route('/get_me_a_therapist')
def get_me_a_therapist():
    username, password, database, hostname, port = parse()
    dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
    cursor = dbconn.cursor()
    dbconn.commit()



if __name__ == '__main__':
    app.run(debug=True)
  