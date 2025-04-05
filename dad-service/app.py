import pika
import time
import logging
import random

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [DAD] %(message)s',
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
    
    # Decisión aleatoria (puedes personalizar esto si quieres)
    approval = random.choice(["approved", "rejected"])
    response = f"papá {approval} la relación con {msg}"

    # Publica la respuesta
    channel.basic_publish(
        exchange='romantic-approval',
        routing_key='',
        body=response
    )

    logging.info(f"🧔 Papá ha respondido: {response}")

# Conexión y configuración
connection = connect()
channel = connection.channel()

# Exchange de entrada (desde girl-service)
channel.exchange_declare(exchange='girl-thinking', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='girl-thinking', queue=queue_name)

# Exchange de salida (hacia love-coordinator)
channel.exchange_declare(exchange='romantic-approval', exchange_type='fanout')

logging.info("Esperando decisiones de Ana para opinar como papá... 💭🧔")
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
