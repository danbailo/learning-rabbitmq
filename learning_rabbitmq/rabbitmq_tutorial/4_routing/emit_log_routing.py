import sys

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5672))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(
    exchange='direct_logs',
    routing_key=severity,
    body=message,
    # properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)
)
print(f' [x] Sent {severity}:{message}')

connection.close()
