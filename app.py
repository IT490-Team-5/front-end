import requests
import logging
import os
import random
import pika
from flask_rabmq import RabbitMQ
#from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host ='25.121.196.54', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='hello')

@app.route('/form',methods = ['GET', 'POST'])
def form():
    #userR = str(request.form['usernameR'])
    #passR = str(request.form['passwordR'])
    #print(userR, passR)
    return render_template('login.html')
    
    
@app.route('/start',methods = ['GET', 'POST'])
def start():

    #Handle if queue gives us a pass or fail from the login

    info = str(request.form['username'])
    passw = str(request.form['password'])
    channel.basic_publish(exchange='', routing_key='hello', body= info)
    print(info,passw)
    return render_template('index.html')
    
@app.route('/',methods = ['GET', 'POST'])
def newUser():
    return render_template('register.html')
app.run(
   port=int(os.getenv('PORT',5000)),
   host=os.getenv('IP','0.0.0.0'),
   debug=True
   )  

