import pika
import json

def callback(ch, method, properties, body):
    info = json.loads(body)
    print(info)
    if info.get("reason") == "create":
      query = "INSERT INTO test(user, pass) VALUES( " + info["user"] + ", " + info["password"] + ")"
      message = {'create':query}
      msgjson= json.dumps(message)
      channel.basic_publish(exchange='', routing_key='right', body=msgjson)
      
    if info.get("reason") == "login":
    	query = "SELECT * FROM test WHERE user=" + info['user'] + " AND pass=" + info['password']
    	message = {'login':query}
    	msgjson = json.dumps(message)
    	channel.basic_publish(exchange='', routing_key='right', body=msgjson)
    


#def callback2(cd, method, propoerties, body):
	



creds = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(pika.ConnectionParameters('25.121.196.54', 5672, "vh1", creds))
channel = connection.channel()
channel.queue_declare(queue='right')
channel.basic_consume('hello', callback, auto_ack=True)




print('Waiting for messages..')
channel.start_consuming()
