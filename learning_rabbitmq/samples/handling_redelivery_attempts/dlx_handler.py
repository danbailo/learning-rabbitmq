import json
import time

import pika


def dlx_callback(ch, method, properties, body):
    message = json.loads(body)
    print(f'Received message from DLX: {message}')

    # Increment delivery attempts
    message['delivery_attempts'] = message.get('delivery_attempts', 0) + 1
    message['last_attempt_timestamp'] = time.strftime(
        '%Y-%m-%dT%H:%M:%SZ', time.gmtime()
    )

    if message['delivery_attempts'] <= 3:
        print('Retrying message delivery')
        # Requeue message to main exchange
        ch.basic_publish(
            exchange='main_exchange', routing_key='main_key', body=json.dumps(message)
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        print('Max delivery attempts reached. Discarding message.')
        ch.basic_ack(delivery_tag=method.delivery_tag)


# Connection parameters
connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Consume messages from DLX queue
channel.basic_consume(
    queue='dlx_queue', on_message_callback=dlx_callback, auto_ack=False
)
print('Waiting for DLX messages. To exit press CTRL+C')
channel.start_consuming()
