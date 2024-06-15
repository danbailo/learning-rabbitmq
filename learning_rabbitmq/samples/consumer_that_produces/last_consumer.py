import pika


def callback(ch, method, properties, body):
    message = body.decode()
    print(f' [x] Consumidor 2 recebeu: {message}')
    # Aqui você pode adicionar o processamento da mensagem
    # ...


# Conexão com o servidor RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declaração da fila secundaria
channel.queue_declare(queue='fila_secundaria')

# Definição da função de callback para o consumidor
channel.basic_consume(
    queue='fila_secundaria', on_message_callback=callback, auto_ack=True
)

print(' [*] Consumidor 2 esperando por mensagens. Para sair pressione CTRL+C')
channel.start_consuming()
