import requests
import logging
import os
import random
import pika
import json
from flask_rabmq import RabbitMQ
#from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(
   pika.ConnectionParameters(host ='25.121.196.54', port=5672, virtual_host = "vh1", credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='hello')
channel.queue_declare(queue='bye')


@app.route('/',methods = ['GET', 'POST'])
def newUser():
    return render_template('register.html')
@app.route('/form',methods = ['GET', 'POST'])
def form():
    try:
    	newPass = str(request.form['password'])
    	newInfo = str(request.form['username'])
    	message = {"from": "front", "reason": "create", "user": newInfo, "password": newPass}
    	msg_json = json.dumps(message)
    	channel.basic_publish(exchange='', routing_key='hello', body=msg_json)
    	return render_template('login.html')
    except KeyError:
    	return render_template('login.html')	
@app.route('/start',methods = ['GET', 'POST'])
def start():
    try:
    	passw = str(request.form['password'])
    	info = str(request.form['username'])
    	channel.basic_publish(exchange='', routing_key='hello', body=nfo)
    	print(info,passw)
    	return render_template('index.html')
    except KeyError:
    	return render_template('index.html')
app.run(
   port=int(os.getenv('PORT',5000)),
   host=os.getenv('IP','0.0.0.0'),
   debug=True
   )  
    
