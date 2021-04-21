#!/bin/bash

if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null
then
	echo "Shutting down Flask server"
	pkill -f app.py
	echo "Flask server offline"
else
	echo "Flask server offline"
	
fi
