import pika


def callback(ch, method, properties, body):
    message = body.decode()
    print(f' [x] Consumer 1 received: {message}')

    # Processar a mensagem e produzir uma nova
    nova_mensagem = f'Processed by Consumer 1 - "{message}"'

    ch.basic_ack(delivery_tag=method.delivery_tag)

    # publish the message in second_queue
    ch.basic_publish(exchange='', routing_key='second_queue', body=nova_mensagem)
    print(f' [x] Consumidor 1 sent: "{nova_mensagem}"')


# connection with rabbitmq server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# declare initial_queue
channel.queue_declare(queue='initial_queue')

# declare the second_queue
channel.queue_declare(queue='second_queue')

# define the callback function that will consume queue
channel.basic_consume(queue='initial_queue', on_message_callback=callback)

print(' [*] Consumer 1 waiting for messages. Press CTRL+C to exit')
channel.start_consuming()
