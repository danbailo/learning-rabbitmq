import json

import pika


def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f'Received message: {message}')

    try:
        # Simulate message processing failure
        raise Exception('Processing failed')
    except Exception as e:
        print(f'Error: {e}, sending to DLX')
        # Reject the message and send it to DLX
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        ch.basic_publish(
            exchange='dlx_exchange', routing_key='dlx_key', body=body.decode()
        )


# Connection parameters
connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Consume messages from main queue
channel.basic_consume(queue='main_queue', on_message_callback=callback, auto_ack=False)
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
