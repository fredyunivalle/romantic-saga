import pika
import threading
import logging
import time
from flask import Flask, render_template
from collections import defaultdict

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [DASHBOARD] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# Espera inicial para asegurar que RabbitMQ esté listo
time.sleep(10)

app = Flask(__name__)
pretendientes = defaultdict(lambda: {"mom": "⏳", "dad": "⏳", "final": "⏳"})

def connect():
    while True:
        try:
            return pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        except pika.exceptions.AMQPConnectionError:
            logging.warning("Esperando conexión con RabbitMQ...")
            time.sleep(5)

def extract_info(msg):
    try:
        if msg.startswith("mamá") or msg.startswith("papá"):
            before_con, _, after_con = msg.partition("con")
            parent = "mom" if "mamá" in before_con else "dad"
            result = before_con.strip().split()[1].lower()  # approved o rejected
            name = after_con.strip().split()[0]  # Carlos
            return name, parent, result
        elif msg.startswith("Relación con"):
            parts = msg.split()
            name = parts[2]
            result = parts[4].lower()
            return name, "final", result
    except Exception as e:
        logging.warning(f"[DASHBOARD] Error al extraer info de: {msg} → {e}")
    return None, None, None

def consume():
    conn = connect()
    ch = conn.channel()

    ch.exchange_declare(exchange='romantic-approval', exchange_type='fanout')
    ch.exchange_declare(exchange='romantic-decision', exchange_type='fanout')

    # Mom/Dad approvals
    result1 = ch.queue_declare(queue='', exclusive=True)
    q1 = result1.method.queue
    ch.queue_bind(exchange='romantic-approval', queue=q1)

    # Final decisions
    result2 = ch.queue_declare(queue='', exclusive=True)
    q2 = result2.method.queue
    ch.queue_bind(exchange='romantic-decision', queue=q2)

    def callback(ch, method, props, body):
        msg = body.decode()
        name, who, result = extract_info(msg)
        if not name:
            return

        # ✅ CORREGIDO: comparación correcta con "mom" y "dad"
        if who == "mom":
            pretendientes[name]["mom"] = "✅" if result == "approved" else "❌"
        elif who == "dad":
            pretendientes[name]["dad"] = "✅" if result == "approved" else "❌"
        elif who == "final":
            pretendientes[name]["final"] = "💍 Aprobada" if result == "approved" else "💔 Rechazada"

        logging.info(f"Actualizado estado: {name} -> {pretendientes[name]}")

    ch.basic_consume(queue=q1, on_message_callback=callback, auto_ack=True)
    ch.basic_consume(queue=q2, on_message_callback=callback, auto_ack=True)

    logging.info("📊 Dashboard escuchando eventos...")
    ch.start_consuming()

@app.route('/')
def index():
    return render_template('index.html', pretendientes=dict(pretendientes))

if __name__ == '__main__':
    threading.Thread(target=consume, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
