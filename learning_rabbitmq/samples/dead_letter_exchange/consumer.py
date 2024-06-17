import random
import time

import pika
import pika.exchange_type

from learning_rabbitmq.samples.dead_letter_exchange.settings import (
    DEAD_LETTER_EXCHANGE,
    DEAD_LETTER_QUEUE,
    DEAD_LETTER_ROUTING_KEY,
    MAIN_EXCHANGE,
    MAIN_QUEUE,
    MAIN_ROUTING_KEY,
    MESSAGE_TTL,
)

# connect with rabbitmq server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# declaring the exchange and queues
channel.exchange_declare(exchange=MAIN_EXCHANGE, exchange_type='direct')
channel.queue_declare(
    queue=MAIN_QUEUE,
    arguments={
        'x-dead-letter-exchange': DEAD_LETTER_EXCHANGE,
        'x-dead-letter-routing-key': DEAD_LETTER_ROUTING_KEY,
    },    
    exclusive=True
)
channel.queue_bind(
    exchange=MAIN_EXCHANGE, queue=MAIN_QUEUE, routing_key=MAIN_ROUTING_KEY
)

channel.exchange_declare(exchange=DEAD_LETTER_EXCHANGE, exchange_type='direct')
channel.queue_declare(
    DEAD_LETTER_QUEUE,
    # declare dead letter configs in args
    arguments={
        'x-message-ttl': MESSAGE_TTL,
        'x-dead-letter-exchange': MAIN_EXCHANGE,
        'x-dead-letter-routing-key': MAIN_ROUTING_KEY,
    },
    exclusive=True,
)
channel.queue_bind(
    exchange=DEAD_LETTER_EXCHANGE,
    queue=DEAD_LETTER_QUEUE,
    routing_key=DEAD_LETTER_ROUTING_KEY,
)


# callback function to consume messages
def callback(ch, method, properties, body):
    print(f'received: "{body.decode()}"')
    try:
        print('trying to processing message...')

        if random.choice([True, False]):
            print('an error occurred!')
            raise Exception()

        time_to_wait = random.randint(0, 10)
        print(f'processing message - {time_to_wait} seconds')
        time.sleep(time_to_wait)

        print('message processed with sucessfully!')
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print('message acked!')

    except Exception:
        print('occur an error when processing message!')
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        print('message nack!')

        # ch.basic_publish(
        #     exchange=DEAD_LETTER_EXCHANGE,
        #     routing_key=DEAD_LETTER_ROUTING_KEY,
        #     body=body,
        # )
        # print('message published to dead letter queue')


# consuming messages
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=MAIN_QUEUE, on_message_callback=callback)

print('Waiting messages. Press CTRL+C to exit.')

channel.start_consuming()
