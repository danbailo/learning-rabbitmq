import json

import pika

# Connection parameters
connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Publish message to main exchange
message = {
    'message_id': '123456789',
    'recipient': 'user@example.com',
    'content': 'Important notification: Your account balance is low.',
}

channel.basic_publish(
    exchange='main_exchange', routing_key='main_key', body=json.dumps(message)
)

print('Message sent to main exchange')
connection.close()
