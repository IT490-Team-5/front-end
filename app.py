#!/usr/bin/python -tt

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
    pika.ConnectionParameters(host='25.121.196.54',
                              port=5672,
                              virtual_host="vh1",
                              credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
<<<<<<< HEAD
	#We have gotten info from the database
	info = json.loads(body)
	print(info)
	global En 
	
	if(info.get('query2') == 'success'):
	# then login
		En = 1
		print(En)
	else:
		En = 0
		print(En)
		print("ya don goofed")
	
	channel.basic_cancel(consumer_tag='front')

def add_on_close_callback():
	return render_template('login.html')



@app.route('/',methods = ['GET', 'POST'])
def landing():
    return render_template('landing.html')
    
    
@app.route("/register", methods = ['GET', 'POST'])
def newUser():
	return render_template('register.html')
    
@app.route('/form',methods = ['GET', 'POST'])
=======
    info = json.loads(body)
    print('INFO HERE: ', info)
    global En
    En = 0
    if (info.get('query2') == 'success'):
        En = 1
    else:
        En = 0
    channel.stop_consuming()


@app.route('/', methods=['GET', 'POST'])
def newUser():
    return render_template('register.html', message='')


@app.route('/form', methods=['GET', 'POST'])
>>>>>>> 937f4be7b9efedcfff0c47214e2760e3aa3ea5d4
def form():
    try:
        newPass = str(request.form['password'])
        newInfo = str(request.form['username'])

        message = {
            "from": "front",
            "reason": "create",
            "user": newInfo,
            "password": newPass
        }
        msg_json = json.dumps(message)

        channel.basic_publish(exchange='', routing_key='hello', body=msg_json)
        channel.basic_consume('front', callback, auto_ack=True)
        print("Waiting for result...")

        channel.start_consuming()

        if (En == 1):
            channel.stop_consuming()
            return render_template('login.html', message='')
        else:
            return render_template(
                'register.html',
                message='ALERT: Username already exists. Try again.')

    except KeyError:
        return render_template('login.html', message='')


@app.route('/start', methods=['GET', 'POST'])
def start():
    try:
        passw = str(request.form['password'])
        info = str(request.form['username'])

        message = {
            "from": "front",
            "reason": "login",
            "user": info,
            "password": passw
        }
        msg_json = json.dumps(message)

        channel.basic_publish(exchange='', routing_key='hello', body=msg_json)
        channel.basic_consume('front', callback, auto_ack=True)
        print("Waiting for result...")

        channel.start_consuming()
        if (En == 1):
            return render_template('index.html',
                                   message='',
                                   name=info,
                                   score=100)
        else:
            return render_template(
                'login.html',
                message='ALERT: Username has not been registered. Try again.')

    except KeyError:
        return render_template('index.html', message='')


app.run(port=int(os.getenv('PORT', 5000)),
        host=os.getenv('IP', '0.0.0.0'),
        debug=True)

