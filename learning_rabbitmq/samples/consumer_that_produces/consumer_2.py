import pika


def callback(ch, method, properties, body):
    message = body.decode()
    print(f' [x] Consumer 2 received: {message}')
    ch.basic_ack(delivery_tag=method.delivery_tag)


# connection with rabbitmq server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# declare the second_queue
channel.queue_declare(queue='second_queue')

# define the callback function that will consume queue
channel.basic_consume(queue='second_queue', on_message_callback=callback)

print(' [*] Consumer 2 waiting for messages. Press CTRL+C to exit')
channel.start_consuming()
