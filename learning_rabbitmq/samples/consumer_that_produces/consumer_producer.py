import pika


def callback(ch, method, properties, body):
    message = body.decode()
    print(f' [x] Consumidor 1 recebeu: {message}')

    # Processar a mensagem e produzir uma nova
    nova_mensagem = f'Processado por Consumidor 1: {message}'

    # Conectar novamente para enviar nova mensagem para a fila_secundaria
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='fila_secundaria')

    channel.basic_publish(
        exchange='', routing_key='fila_secundaria', body=nova_mensagem
    )
    print(f' [x] Consumidor 1 enviou: {nova_mensagem}')

    connection.close()


# Conexão com o servidor RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declaração da fila inicial
channel.queue_declare(queue='fila_inicial')

# Definição da função de callback para o consumidor
channel.basic_consume(queue='fila_inicial', on_message_callback=callback, auto_ack=True)

print(' [*] Consumidor 1 esperando por mensagens. Para sair pressione CTRL+C')
channel.start_consuming()
