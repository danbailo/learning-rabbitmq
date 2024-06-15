import pika

from learning_rabbitmq.samples.dead_letter_exchange.settings import (
    MAIN_EXCHANGE,
    MAIN_ROUTING_KEY,
)

# Conexão com o servidor RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange=MAIN_EXCHANGE, exchange_type='direct')

message = 'Published message'
channel.basic_publish(
    exchange=MAIN_EXCHANGE, routing_key=MAIN_ROUTING_KEY, body=message
)
print(f' [x] Sent "{message}" to {MAIN_EXCHANGE}:{MAIN_ROUTING_KEY}')

# Fechando a conexão
connection.close()
