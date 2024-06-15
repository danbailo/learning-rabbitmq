import pika

# Connection parameters
connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Declare main exchange and queue with DLX settings
channel.exchange_declare(exchange='main_exchange', exchange_type='direct')
channel.queue_declare(
    queue='main_queue', arguments={'x-dead-letter-exchange': 'dlx_exchange'}
)
channel.queue_bind(exchange='main_exchange', queue='main_queue', routing_key='main_key')

# Declare dead letter exchange and queue
channel.exchange_declare(exchange='dlx_exchange', exchange_type='direct')
channel.queue_declare(queue='dlx_queue')
channel.queue_bind(exchange='dlx_exchange', queue='dlx_queue', routing_key='dlx_key')

print('RabbitMQ setup complete')

connection.close()
