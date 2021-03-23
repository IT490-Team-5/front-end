import pika
import json

def callback(ch, method, properties, body):
    info = json.loads(body)
    print(info)
    if info.get("reason") == "create":
    #This is when we get something to turn into SQL Statement add AND process register
      query = "INSERT INTO test(user, pass) VALUES( " + info["user"] + ", " + info["password"] + ")"
      message = {'create':query, 'reason':'query'}
      msgjson= json.dumps(message)
      channel.basic_publish(exchange='', routing_key='hello', body=msgjson)
      
    if info.get("reason") == "login":
    #This is when we get something to turn into SQL Statement add AND process login
    	query = "SELECT * FROM test WHERE user=" + info['user'] + " AND pass=" + info['password']
    	message = {'login':query, 'reason':'query'}
    	msgjson = json.dumps(message)
    	channel.basic_publish(exchange='', routing_key='hello', body=msgjson)
    


#def callback2(cd, method, propoerties, body):
	



creds = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(pika.ConnectionParameters('25.121.196.54', 5672, "vh1", creds))
channel = connection.channel()
channel.queue_declare(queue='right')
channel.basic_consume('right', callback, auto_ack=True)




print('Waiting for messages..')
channel.start_consuming()
