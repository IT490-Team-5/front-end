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

global PassFail


credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(
   pika.ConnectionParameters(host ='25.121.196.54', port=5672, virtual_host = "vh1", credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
	info = json.loads(body)
	if info.get('reason') == 'results':
	#Then I got something
	    PassFail = 1
		



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
    	channel.basic_consume('front', callback, auto_ack = True)
    	print("Waiting for result")
    	
    	
    	channel.start_consuming()
    	return render_template('login.html')
    		
    		
    except KeyError:
    	return render_template('login.html')	
    	
    	
@app.route('/start',methods = ['GET', 'POST'])
def start():
    try:
    	passw = str(request.form['password'])
    	info = str(request.form['username'])
    	message = {"from": "front", "reason": "login", "user": info, "password": passw}
    	msg_json = json.dumps(message)
    	
    	channel.basic_publish(exchange='', routing_key='hello', body=msg_json)
    	channel.basic_consume('front', callback, auto_ack = True)
    	print("Waiting for result")
    	
    	channel.start_consuming()
    	if(PassFail == 1):
    		return render_template('index.html')
    		
    		
    except KeyError:
    	return render_template('index.html')
app.run(
   port=int(os.getenv('PORT',5000)),
   host=os.getenv('IP','0.0.0.0'),
   debug=True
   )  
    
