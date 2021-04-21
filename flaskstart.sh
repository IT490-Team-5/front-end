#!/bin/bash

if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null
then
	echo "Server is running"
else 
	echo "Flask server offline ..."
	echo "Turning on Web Server"
	python3 app.py
fi
