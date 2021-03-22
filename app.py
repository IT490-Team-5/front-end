mport requests
import logging
import os
import random
from flask_rabmq import RabbitMQ
#from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/',methods = ['GET', 'POST'])
def form():
    newPass = str(request.form['password'])
    newInfo = str(request.form['username'])
    print(newPass,newInfo)
    return render_template('login.html')
@app.route('/start',methods = ['GET', 'POST'])
def start():
    passw = str(request.form['password'])
    info = str(request.form['username'])
    print(info,passw)
    return render_template('index.html')
@app.route('/newUser',methods = ['GET', 'POST'])
def newUser():
    return render_template('register.html')
app.run(
   port=int(os.getenv('PORT',5000)),
   host=os.getenv('IP','0.0.0.0'),
   debug=True
   )  
    
