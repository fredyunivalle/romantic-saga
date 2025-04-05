import pika
import time
import logging
from collections import defaultdict

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [COORDINATOR] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Espera inicial para asegurar que RabbitMQ esté listo
time.sleep(10)

# Estado temporal: pretendientes y sus aprobaciones
approval_state = defaultdict(lambda: {"mom": None, "dad": None})

def extract_info(message):
    try:
        if message.startswith("mamá") or message.startswith("papá"):
            before_con, _, after_con = message.partition("con")
            parent_part = before_con.strip().split()
            raw_parent = parent_part[0].strip()
            parent = "mom" if raw_parent == "mamá" else "dad"
            result = parent_part[1].strip()
            name = after_con.strip().split()[0]
            logging.info(f"[EXTRACT] parent: {parent}, result: {result}, name: {name}")
            return name, parent, result
        elif message.startswith("Relación con"):
            parts = message.split()
            name = parts[2]
            result = parts[4].lower()
            logging.info(f"[EXTRACT] Final decision for {name}: {result}")
            return name, "final", result
    except Exception as e:
        logging.error(f"Error extrayendo info: {e}")
    return None, None, None


def decide(name):
    status = approval_state[name]
    if status["mom"] == "rejected" or status["dad"] == "rejected":
        return "rejected"
    elif status["mom"] == "approved" and status["dad"] == "approved":
        return "approved"
    return None  # aún esperando

def callback(ch, method, properties, body):
    msg = body.decode()
    logging.info(f"Recibida aprobación/rechazo: {msg}")

    name, parent, result = extract_info(msg)
    if None in (name, parent, result):
        logging.warning(f"Formato de mensaje no reconocido para: {msg}")
        return
    else:
        logging.info(f"✅ Extraído correctamente → name: {name}, parent: {parent}, result: {result}")

    approval_state[name][parent] = result

    status = decide(name)
    if status:
        final_msg = f"Relación con {name} fue {status.upper()} 💌"
        channel.basic_publish(
            exchange='romantic-decision',
            routing_key='',
            body=final_msg
        )
        logging.info(f"🎉 Resultado final: {final_msg}")
        # Limpiar estado si no se quiere acumular
        del approval_state[name]

# Conexión con RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# Suscripción a aprobaciones de mamá/papá
channel.exchange_declare(exchange='romantic-approval', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='romantic-approval', queue=queue_name)

# Exchange para publicar decisiones finales
channel.exchange_declare(exchange='romantic-decision', exchange_type='fanout')

logging.info("Esperando aprobaciones para tomar una decisión final... 💘🧠")
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()

