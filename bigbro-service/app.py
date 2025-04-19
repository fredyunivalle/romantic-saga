import pika
import logging
import time

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [BIG-BROTHER] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Espera inicial para asegurarse de que RabbitMQ esté listo
time.sleep(10)

def callback(ch, method, properties, body):
    try:
        msg = body.decode()
        logging.info("Received something...")
        logging.info(f"Content: {msg}")
        logging.info("Baa... another fool chasing my sister 😒\n")
    except Exception as e:
        logging.error(f"Error processing message: {e}")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    # Escucha cuando Ana está pensando en formalizar
    channel.exchange_declare(exchange='girl-thinking', exchange_type='fanout')

    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='girl-thinking', queue=queue_name)

    logging.info("Big Brother is eavesdropping on Ana's thoughts...")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    main()