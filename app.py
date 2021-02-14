import requests
import os
import random
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def form():
    return render_template('index.html')
    
app.run(
   port=int(os.getenv('PORT',8080)),
   host=os.getenv('IP','127.0.0.1'),
   debug=True
   )  
