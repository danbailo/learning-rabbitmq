import pika

# Define RabbitMQ server settings
rabbitmq_host = 'localhost'

# Define queue and exchange names
main_queue = 'main_queue'
delay_queue = 'delay_queue'
exchange = 'main_exchange'
delay_exchange = 'delay_exchange'
routing_key = 'task'
delay_routing_key = 'delay_task'

# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()

# Declare the main exchange
channel.exchange_declare(exchange=exchange, exchange_type='direct')

# Declare the main queue
channel.queue_declare(queue=main_queue)

# Bind the main queue to the main exchange
channel.queue_bind(exchange=exchange, queue=main_queue, routing_key=routing_key)

# Declare the delay exchange
channel.exchange_declare(exchange=delay_exchange, exchange_type='direct')

# Declare the delay queue with TTL and DLX settings
args = {
    'x-message-ttl': 30000,  # Message TTL in milliseconds
    'x-dead-letter-exchange': exchange,  # DLX
    'x-dead-letter-routing-key': routing_key,  # Routing key for DLX
}
channel.queue_declare(queue=delay_queue, arguments=args)

# Bind the delay queue to the delay exchange
channel.queue_bind(
    exchange=delay_exchange, queue=delay_queue, routing_key=delay_routing_key
)


# Function to publish a message
def publish_message(message, delay=False):
    if delay:
        channel.basic_publish(
            exchange=delay_exchange, routing_key=delay_routing_key, body=message
        )
    else:
        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
    print(f" [x] Sent '{message}'")


# Publish a message with a delay
publish_message('Hello after 30 seconds', delay=True)

# Close the connection
connection.close()
