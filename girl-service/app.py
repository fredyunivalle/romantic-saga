import pika
import time
import logging
import threading

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [GIRL] %(message)s',
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

# Callback para propuestas románticas
def on_proposal(ch, method, properties, body):
    msg = body.decode()
    logging.info(f"Escuchó propuesta: {msg}")
    logging.info("Ana está considerando la propuesta...")

    # Publicar que Ana está considerando formalizar
    channel.exchange_declare(exchange='girl-thinking', exchange_type='fanout')
    channel.basic_publish(
        exchange='girl-thinking',
        routing_key='',
        body=body
    )
    logging.info(f"Ana notificó que está considerando formalizar: {msg}")

# Callback para la decisión final
def on_final_decision(ch, method, properties, body):
    msg = body.decode()
    if "APPROVED" in msg.upper():
        logging.info(f"💍 Ana responde: ¡Sí acepto! ({msg})")
    elif "REJECTED" in msg.upper():
        logging.info(f"💔 Ana responde: Me rompieron el corazón... ({msg})")
    else:
        logging.info(f"Ana recibió un resultado desconocido: {msg}")

# Inicia un consumidor en un hilo separado
def start_consumer(exchange_name, callback_fn, tag):
    conn = connect()
    ch = conn.channel()
    ch.exchange_declare(exchange=exchange_name, exchange_type='fanout')
    result = ch.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    ch.queue_bind(exchange=exchange_name, queue=queue_name)
    logging.info(f"[{tag}] Escuchando exchange '{exchange_name}'")
    ch.basic_consume(queue=queue_name, on_message_callback=callback_fn, auto_ack=True)
    ch.start_consuming()

# Conexión principal para publicar desde propuesta
connection = connect()
channel = connection.channel()

# Iniciar hilo para escuchar decisiones finales
threading.Thread(target=start_consumer, args=('romantic-decision', on_final_decision, 'DECISION'), daemon=True).start()

# Escuchar propuestas románticas (bloqueante)
channel.exchange_declare(exchange='romantic', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='romantic', queue=queue_name)
logging.info("Esperando propuestas de amor... 💘")
channel.basic_consume(queue=queue_name, on_message_callback=on_proposal, auto_ack=True)
channel.start_consuming()
