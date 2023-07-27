from flask import Flask, render_template, request, redirect, flash, url_for, session
from datetime import timedelta
from user.models import User
import os
import user_database as db
from flask import Flask, session
import pymongo
from pymongo import MongoClient
import requests

hostip = '192.168.1.14'
adminCitizen = "14799"

# Database
user = os.environ.get("DB_USER")
secret = os.environ.get("DB_PASS")

cluster = pymongo.MongoClient(f"mongodb://localhost:27017")
dase = cluster["pymongo_auth"]
collection = dase["users"]
##################

# Line variables
url = 'https://notify-api.line.me/api/notify'
token = 'your token'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
##################

# Website
app = Flask(__name__, static_url_path = "/static", static_folder = "static")
app.secret_key = os.environ.get("SUPERTACTIC")
@app.route('/')
def home():
    session.clear()
    if "username" in session:
        return redirect('/index')
    else:
        return redirect('/login')
@app.route('/seatsetup', methods=['POST'])
def SeatSetting():
    if request.method == 'POST':
        user = User()
        flag = user.UpdateSeat()
        if flag:
            return redirect('/status')
@app.route('/register', methods=['POST', 'GET'])
def register():
    # Handles a user signup
    if(request.method == 'POST'):
        user = User()
        success_flag = user.signup()
        if(success_flag):
            #flash('Your account was created succesfully!', "success")
            return redirect('/login')  
        else:
            #flash('Already in use.' , "error")
            return redirect('/register')      
        
    # Default GET route
    return render_template('register.html')

@app.route('/login', methods = ['POST','GET'])
def login():
    # Handles a user login
    if(request.method == 'POST'):
        user = User()
        success_flag = user.login()
        
        if(success_flag):
            return redirect('/index')
        else:
            #flash('Error logging in', 'error')
            return redirect('/register')
    
    # Default GET route
    return render_template('login.html')

@app.route('/lineapi', methods=["POST", "GET"])
def lineapi():
    if session["citizenid"] == str(adminCitizen):
        if(request.method == 'POST'):
            citizen, user, tele, status, seat = db.getData(session["citizenid"])
            User().lineSent()
            return render_template("indexAdmin.html", username=user, Citizen=citizen,Tele=tele, seat=seat, status=status)
        else:
            return render_template("lineapi.html")
    else:
        return redirect('/index')
@app.route('/index')
def indexfunc():
    if db.check_for_user(session["citizenid"] and session["citizenid"] != str(adminCitizen)):
        citizen, user, tele, status, seat = db.getData(session["citizenid"])
        return render_template("index.html", username=user, Citizen=citizen,Tele=tele, seat=seat, status=status)
    if session["citizenid"] == str(adminCitizen):
        getAllUser = db.getAllUser()
        getUserUp = db.getUserUp()
        citizen, user, tele, status, seat = db.getData(session["citizenid"])
        if int(getAllUser) == int(getUserUp):
            msg = ' : คนมาครบแล้ว :D'
            r = requests.post(url, headers=headers, data = {'message':msg})
            print (r.text)
        return render_template("indexAdmin.html", username=user, Citizen=citizen,Tele=tele, seat=seat, status=status)
@app.route('/seat')
def seatfunc():
    if db.check_for_user(session["citizenid"]):
        citizen, user, tele, status, seat = db.getData(session["citizenid"])
    return render_template("seat.html", username=user, status=status)
@app.route('/status', methods=["GET"])
def statuschange():
    if db.check_for_user(session["citizenid"]):
        citizen, user, tele, status, seat = db.getData(session["citizenid"])
    return render_template('selectStatus.html', username=user, status=status, seat=seat)
@app.route('/status/up')
def upPost():
    checkUser = db.get_user(session['citizenid'])
    if checkUser == None:
        return redirect('/index')
    else:
        db.updateStatustoUp(session['citizenid'])
        return redirect('/index')
@app.route('/status/down')
def downPost():
    checkUser = db.get_user(session['citizenid'])
    if checkUser == None:
        return redirect('/index')
    else:
        db.updateStatustoDown(session['citizenid'])
        return redirect('/index')
@app.route('/table')
def tablefunc():
    headings = ("Name", "Status", "Time")
    data2 = db.updateTable()
    return render_template("table.html", table_headings=headings, table_data=data2)
if __name__ == "__main__":
    app.secret_key="anystringhere"
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host=hostip,debug=True)
##################