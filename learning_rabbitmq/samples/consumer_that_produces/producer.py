import pika

# connect with rabbitmq server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# declare initial queue
channel.queue_declare(queue='initial_queue')

# send message
message = 'initial message'
channel.basic_publish(exchange='', routing_key='initial_queue', body=message)
print(f' [x] Sent "{message}"')

# close the connection
connection.close()
