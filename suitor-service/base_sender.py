import pika

def send_love(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.exchange_declare(exchange='romantic', exchange_type='fanout')
    channel.basic_publish(exchange='romantic', routing_key='', body=message)
    print(f"[SUITOR] Propuesta enviada: {message}")
    connection.close()

