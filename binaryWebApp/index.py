from flask import Flask,render_template,request,redirect,url_for
import random
import time
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('database//account.db', check_same_thread=False)
c = conn.cursor()

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/login',methods=["POST","GET"])
def login():
	if request.method == "POST":
		uname = request.form['uname']
		passwrd = request.form['pass']
		log_query = "SELECT * FROM acc WHERE username = ? AND password = ?"
		c.execute(log_query,(uname,passwrd))
		if c.fetchall():
			score = c.execute(log_query,(uname,passwrd))
			for i in score:
				id = i[0]
			return redirect(url_for('profile',username=uname,userid1=id))
		else:
			return render_template('login.html')
	else:
		return render_template('login.html')
@app.route('/create_account',methods=["GET","POST"])
def create():
	if request.method == "POST":
		uname = request.form['uname']
		passwrd = request.form['pass']
		c_passwrd = request.form['cpass']
		if passwrd == c_passwrd and len(passwrd) > 8:
			query = "INSERT INTO acc (username,password,easy,medium,hard) VALUES(?,?,?,?,?)"
			c.execute(query,(uname,passwrd,0,0,0))
			conn.commit()
			log_query1 = "SELECT * FROM acc WHERE username = ? AND password = ?"
			c.execute(log_query1,(uname,passwrd))
			if c.fetchall():
				score1 = c.execute(log_query1,(uname,passwrd))
				for i in score1:
					uid = i[0]
				return redirect(url_for('profile',username = uname ,userid1 = uid))
		else:
			return 'Error'

	else:
		return render_template('createAcc.html')

@app.route('/homepage/username=<username>/id=<userid1>')
def profile(username,userid1):
	easy_score_query = "SELECT * FROM acc WHERE username = ? AND id = ?"
	c.execute(easy_score_query,(username,userid1))
	for i in c:
		easyS = i[3]
		mediumS = i[4]
		hardS = i[5]
	return render_template('profile.html',easyS = easyS,mediumS=mediumS,hardS=hardS)
	
@app.route('/easy',methods=["POST","GET"])
def easyQue():
	return render_template('easy.html')


if __name__ == '__main__':
	app.run(debug=True)