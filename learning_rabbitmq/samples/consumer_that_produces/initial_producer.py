import pika

# Conexão com o servidor RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declaração da fila inicial
channel.queue_declare(queue='fila_inicial')

# Envio de mensagens
message = 'Mensagem inicial'
channel.basic_publish(exchange='', routing_key='fila_inicial', body=message)
print(f" [x] Enviado '{message}'")

# Fechando a conexão
connection.close()
