from flask import Flask, render_template, url_for, redirect, request, session, flash
from urllib.parse import urlparse
import psycopg2
from datetime import date, datetime
import html
import random

app = Flask(__name__)
app.secret_key = 'hello_WORLD_##$$'

avatars = [
('Peter Parker','https://cdn.dribbble.com/users/1634115/screenshots/6245839/spiderman-dribbble.png?compress=1&resize=800x600'), 
('Bruce Wayne','https://www.dccomics.com/sites/default/files/Char_Gallery_Batman_DTC1018_6053f2162bdf03.97426416.jpg'), 
('Stephen Strange','https://www.denofgeek.com/wp-content/uploads/2021/09/what-if-episode-4-review.jpg?resize=768%2C432'), 
('Clark Kent','https://upload.wikimedia.org/wikipedia/en/3/35/Supermanflying.png'), 
('Natasha Romanoff','https://www.seekpng.com/png/full/435-4357026_black-widow-avengers-black-widow-cartoon.png')]

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
            if session['user_type'] == 'therapist' or session['user_type'] == 'client':
                return redirect(url_for('profile'))
            else:
                return redirect(url_for('index'))
    else:
        return render_template('login_page_client.html')
   

@app.route('/login', methods=['POST']) #The actual login process
def login():
    try:
        if 'user' in session:
            flash('User Already in Session! Logout To Continue as a Different User!')
            if session['user_type'] == 'therapist' or session['user_type'] == 'client':
                return redirect(url_for('profile'))
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
                        flash(f'Hello {email}!')
                        flash('Welcome to PFT')
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
                        flash(f'Hello {email}!')
                        flash('Welcome to PFT')
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
        cursor.execute(f"SELECT * FROM posts ORDER BY post_id DESC;")
        posts = cursor.fetchall()

        dbconn.commit()
        return render_template("profile.html", email=email, posts=posts, user_type = session['user_type'],random=random, avatars = avatars)
    else:
        flash('Welcome to PFT!')
        flash('Please Create an Account to Avail Free Therapy')
        username, password, database, hostname, port = parse()
        dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
        cursor = dbconn.cursor()
        cursor.execute(f"SELECT * FROM posts ORDER BY post_id DESC;")
        posts = cursor.fetchall()

        dbconn.commit()
        return render_template("profile.html", posts=posts,random=random, avatars = avatars)


@app.route('/your_shout_it_outs')
def your_shout_it_outs():
    username, password, database, hostname, port = parse()
    dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
    cursor = dbconn.cursor()
    cursor.execute(f"SELECT * FROM posts WHERE user_id = %s;",[session['id']])
    posts = cursor.fetchall()
    dbconn.commit()
    return render_template("your_shout_it_outs.html", posts=posts, user_type = session['user_type'],random=random, avatars = avatars)


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
        cursor.execute(f''' INTO client_cred 
                            (first_name,last_name,phonenumber,age,city,occupation,concerns,relationship_status,timeperiod,emergency_contact,id,gender,status) 
                            VALUES(%s,%s,INSERT%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
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
    cursor.execute(f'''SELECT likes FROM posts WHERE post_id = %s;''',[post_id])
    likes = cursor.fetchall()
    cursor.execute(f"""UPDATE posts SET likes = %s WHERE post_id = %s;""",(likes[0][0]+1,post_id))
    dbconn.commit()
    return redirect(url_for('profile', _anchor=post_id))


@app.route('/ad_listing')
def ad_listing():
    username, password, database, hostname, port = parse()
    dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
    cursor = dbconn.cursor()
    cursor.execute(f'''SELECT * FROM events;''')
    events = cursor.fetchall()
    dbconn.commit()
    if 'user' in session:
        return render_template('ad_listing.html', user_type = session['user_type'], events=events)
    else:
        return render_template('ad_listing.html', events=events)


@app.route('/intern_listing')
def intern_listing():
    username, password, database, hostname, port = parse()
    dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
    cursor = dbconn.cursor()
    cursor.execute(f'''SELECT * FROM internships;''')
    interns = cursor.fetchall()
    dbconn.commit()
    if 'user' in session:
        return render_template('intern_listing.html', user_type = session['user_type'], interns=interns)
    else:
        return render_template('intern_listing.html', interns=interns)


@app.route('/survey_listing')
def survey_listing():
    username, password, database, hostname, port = parse()
    dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
    cursor = dbconn.cursor()
    cursor.execute(f'''SELECT * FROM survey;''')
    surveys = cursor.fetchall()
    dbconn.commit()
    if 'user' in session:
        return render_template('survey_listing.html', user_type = session['user_type'], surveys=surveys)
    else:
        return render_template('survey_listing.html', surveys=surveys)


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
    return render_template('interested_therapists.html', status = status, user_type = 'client')


@app.route('/get_me_a_therapist')
def get_me_a_therapist():
    username, password, database, hostname, port = parse()
    dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
    cursor = dbconn.cursor()
    cursor.execute(f"""UPDATE client_cred SET status = %s WHERE id = %s;""",('free',session['id']))
    dbconn.commit()
    return redirect(url_for('interested_therapists'))


@app.route('/client_pool')
def client_pool():
    username, password, database, hostname, port = parse()
    dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
    cursor = dbconn.cursor()
    cursor.execute(f"""SELECT first_name, occupation, city, age, gender, concerns, timeperiod, id FROM client_cred WHERE status = %s;""",['free'])
    client_info = cursor.fetchall()
    dbconn.commit()

    return render_template('client_pool.html', client_info = client_info, user_type = 'therapist')


@app.route('/accept_client/<int:client_id>')
def accept_client(client_id):
    username, password, database, hostname, port = parse()
    dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
    cursor = dbconn.cursor()
    cursor.execute(f"""SELECT status FROM matches WHERE therapist_id = %s;""",[session['id']])
    statuses = cursor.fetchall()
    for status in statuses:
        if status[0] == 'accepted':
            engaged = True
            break
    if engaged:
        dbconn.commit()
        flash('You Cant Deal with more than One Client at a time!')
        return redirect(url_for('accepted_clients'))
    else:
        cursor.execute(f"""UPDATE client_cred SET status = %s WHERE id = %s;""",('accepted',client_id))
        cursor.execute(f"""INSERT INTO matches (client_id, therapist_id, start_date, status) VALUES (%s,%s,%s,%s);""",(client_id, session['id'],date.today(),'accepted'))
        dbconn.commit()
        return redirect(url_for('accepted_clients'))


@app.route('/accepted_clients')
def accepted_clients():
    username, password, database, hostname, port = parse()
    dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
    cursor = dbconn.cursor()
    cursor.execute(f"""SELECT client_id FROM matches WHERE status = %s AND therapist_id = %s;""",('accepted',session['id']))
    accepted_clients = cursor.fetchall()
    print(accepted_clients)
    cursor.execute(f"""SELECT first_name, occupation, city, age, gender, concerns, timeperiod, id FROM client_cred WHERE id = %s;""",[accepted_clients[0][0]])
    client_info = cursor.fetchall()
    dbconn.commit()
    return render_template('accepted_clients.html', client_info = client_info, user_type = 'therapist')


########################################### Find tag #####################################

@app.route("/search/<tag>")
def search(tag):
    email = session['user']
    username, password, database, hostname, port = parse()
    dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
    cursor = dbconn.cursor()
    cursor.execute(f"SELECT * FROM posts;")
    posts = cursor.fetchall()
    dbconn.commit()
    tag_list = []

    for post in posts:
        tag_array = post[4].split(',')
        for tagg in tag_array:
            if tagg == tag:
                print(post)
                tag_list.append(post)
    session['tag_list'] = tag_list
    return redirect(url_for('search_tags'))


@app.route("/search_tags")
def search_tags():  
    return render_template('search_tags.html', posts = session['tag_list'], user_type = session['user_type'], random=random, avatars = avatars)


@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    id = session['id']
    username, password, database, hostname, port = parse()
    dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
    cursor = dbconn.cursor()
    cursor.execute(f"SELECT user_id FROM posts WHERE post_id = %s;",[post_id])
    user_id = cursor.fetchall()
    if user_id[0][0] == id:
        cursor.execute(f"DELETE FROM posts WHERE post_id = %s;",[post_id])
        dbconn.commit()
        flash('Post Deleted Successfully')
        return redirect(url_for('your_shout_it_outs'))
    else:
        dbconn.commit()
        flash('Unauthorized Action')
        return redirect(url_for('profile'))

if __name__ == '__main__':
    app.run()
  