from flask import (Flask, render_template, request, url_for, redirect, session, make_response, g, abort)
import sqlite3 as sql
import datetime
import hashlib

app = Flask(__name__)


@app.route('/')
def index():
    with sql.connect("forum.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM topic")
        topics = cur.fetchall()
        error = request.args.get('error')

    return render_template('Register.html', topics=topics, error=error)


@app.route('/register', methods=['get', 'post'])
def register():
    time = datetime.datetime.now()
    error = None

    if request.method == 'post':
        username = request.form['username']
        password = request.form['password']
        passwordHash = hashlib.sha256(password.encode('utf-8')).hexdigest()

        with sql.connect("forum.db") as con:
            cur = con.cursor()

            cur.execute("SELECT * FROM user WHERE userName = ?", (username,))
            user = cur.fetchone()

            if user:
                error = "This Username Already Exists Try Again"
            else:
                cur.execute("INSERT INTO user (userName, passwordHash, isAdmin, creationTime, lastVisit) VALUES (?, ?, ?, ?, ?)", (username, passwordHash, 0, time, time))
                con.commit()
                return redirect(url_for('RegisterSuccess'))

    return render_template('Register.html', error=error)


@app.route('/login', methods=['get', 'post'])
def login():
    error = None

    if request.method == 'post':
        username = request.form['username']
        password = request.form['password']

        with sql.connect("forum.db") as con:
            cur = con.cursor()

            cur.execute("SELECT * FROM user WHERE userName = ?", (username,))
            user = cur.fetchone()

            if user:
                stored_hash = user[2]
                entered_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
                if entered_hash == stored_hash:
                    session['userID'] = user[0]
                    session['username'] = user[1]
                    cur.execute("UPDATE user SET lastVisit = ? WHERE userID = ?", (datetime.datetime.now(), user[0]))
                    con.commit()
                    return redirect(url_for('success'))
                else:
                    abort(401)
            else:
                return redirect(url_for('index'))

    return render_template('Login.html')
@app.route('/logout')
def logout():
    session.pop('username', None)
    error = " You Have Logged Out"
    return redirect(url_for('index', error=error))
@app.route('/success')
def success():
   return 'Your Have Successfully Logged In'
@app.route('/RegisterSuccess')
def success():
   return 'You Have Registered Successfully'

@app.route('/createTopic', methods=['get', 'post'])
def createTopic():
    time = datetime.datetime.now()
    error = None

    if request.method == 'post':
        topic_name = request.form['createtopic']
        postingUser = session['username']

        with sql.connect("forum.db") as con:
            cur = con.cursor()

            cur.execute("SELECT t.topicID, t.topicName, u.userName, t.creationTime, t.updateTime FROM topic t JOIN user u ON t.postingUser = u.userID WHERE t.topicName = ?", (topic_name,))
            topic = cur.fetchone()

            if topic:
                error = "This Topic Already Exists"
            else:
                cur.execute("INSERT INTO topic (topicName, postingUser, creationTime, updateTime) VALUES (?, (SELECT userID FROM user WHERE userName = ?), ?, ?)", (topic_name, postingUser, time, time))
                con.commit()
                error = "A new Topic Has Been Created"
                return redirect(url_for('index', error=error))

    return render_template('Topics.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
