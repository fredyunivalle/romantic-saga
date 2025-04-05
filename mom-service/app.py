import pika
import time
import logging
import random

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [MOM] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Espera inicial
time.sleep(10)

def connect():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            return connection
        except pika.exceptions.AMQPConnectionError:
            logging.warning("Esperando conexión con RabbitMQ...")
            time.sleep(5)

def callback(ch, method, properties, body):
    msg = body.decode()
    logging.info(f"Escuchó que Ana está considerando: {msg}")
    
    approval = random.choice(["approved", "rejected"])
    response = f"mamá {approval} la relación con {msg}"

    # Publica la aprobación o rechazo
    channel.basic_publish(
        exchange='romantic-approval',
        routing_key='',
        body=response
    )

    logging.info(f"🔔 Mamá ha respondido: {response}")

connection = connect()
channel = connection.channel()

# Declaramos el exchange desde el que escuchamos
channel.exchange_declare(exchange='girl-thinking', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='girl-thinking', queue=queue_name)

# Exchange donde se publican las respuestas
channel.exchange_declare(exchange='romantic-approval', exchange_type='fanout')

logging.info("Esperando decisiones de Ana para opinar como mamá... 💭👩‍🦰")
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
