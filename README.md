
# 💘 Romantic Saga Simulation with Microservices and RabbitMQ

This project is a fun and educational simulation of the SAGA pattern using microservices, RabbitMQ, and Flask. The story revolves around several suitors trying to win Ana's heart. To succeed, they must first gain the approval of her mom and dad — two other independent microservices. The decision is coordinated by a central orchestrator that finalizes the outcome. A real-time web dashboard shows the state of each suitor's journey. ❤️

---

## 🧩 Architecture

- `suitor-service`: Contains individual scripts (`.py`) for each suitor with culturally-themed love messages. You can enter the container and execute each script manually.
- `girl-service`: Ana receives love proposals and broadcasts that she is considering them.
- `mom-service`: Mom gives her approval or rejection.
- `dad-service`: Dad gives his approval or rejection.
- `love-coordinator`: Listens to both parents and makes the final decision based on both responses.
- `love-dashboard`: A Flask web app that shows each suitor's status (mom, dad, and final decision).
- `rabbitmq`: The message broker that allows communication between all services.

---

## 📦 Tech Stack

- Python 3.10
- RabbitMQ with Management UI
- Flask
- Docker & Docker Compose
- HTML + Bootstrap (in the dashboard)

---

## 🔁 Message Flow and Exchanges

### What is an exchange?

An **exchange** in RabbitMQ is a routing mechanism that receives messages and determines where to send them. Exchanges are not queues; they **route messages to queues** based on rules.

### Types used in this project

This project uses the `fanout` exchange type, which broadcasts messages to **all connected queues** (like a radio tower sending signals to all listeners).

### Exchanges in this simulation:

| Exchange            | Purpose                                                         | Who publishes     | Who listens         |
|---------------------|------------------------------------------------------------------|-------------------|----------------------|
| `romantic`          | Where love proposals are sent                                    | suitor-service    | girl-service         |
| `girl-thinking`     | Ana announces she's considering a proposal                       | girl-service      | mom-service, dad-service |
| `romantic-approval` | Parents respond with approval or rejection                       | mom/dad services  | love-coordinator     |
| `romantic-decision` | Final outcome (approved or rejected) from coordinator            | love-coordinator  | girl-service, dashboard |

Each microservice declares its own exclusive queue and binds it to the relevant exchange. Example:

```python
channel.exchange_declare(exchange='romantic', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
channel.queue_bind(exchange='romantic', queue=result.method.queue)
```

Messages are sent like this:

```python
channel.basic_publish(exchange='romantic', routing_key='', body=message)
```

---

## 🚀 Running the Project

1. **Clone this repository:**
   ```bash
   git clone https://github.com/fredyunivalle/romantic-saga.git
   cd romantic-saga
   ```

2. **Build and run the system:**
   ```bash
   docker-compose up --build
   ```

3. **Access the dashboard:**
   - [http://localhost:5000](http://localhost:5000)

4. **Enter the `suitor-service` container and trigger proposals:**
   ```bash
   docker exec -it romantic-saga-suitor-service-1 bash
   python juan.py
   python jampier.py
   python pedro.py
   ```

---

## 📊 Dashboard

The dashboard shows real-time status of each suitor:
| Pretender | Mom | Dad | Final Decision |
|-----------|-----|-----|----------------|
| Juan      | ✅  | ❌  | 💔 Rejected     |
| Jampier   | ✅  | ✅  | 💍 Approved      |

---

## 🎓 Student Challenge: Bring it to Kubernetes!

You're now challenged to replicate or improve this project using **Kubernetes**! 💡

### Things you must consider:
- Deploy each microservice as a pod (Deployment or StatefulSet).
- Use a **Helm chart** or **Kustomize** for packaging the full system.
- Configure RabbitMQ via a `StatefulSet` and expose its UI.
- Use **ConfigMaps** or **Secrets** for messages or dynamic logic.
- Optional: Use **Ingress + TLS** for accessing the dashboard.

### Bonus ideas:
- Add logging with **Fluentd** or **Loki + Grafana**.
- Persist message history in **MongoDB** or **PostgreSQL**.
- Add **Prometheus metrics** for each service.
- Support for "breakup recovery" logic 💔🥲
- Add more **industrial examples** (e.g., loan approval, booking systems).
- Add more **cliché romantic cases** (e.g., long-distance relationship resolver 🤣).

### 🏆 Final Goal:
A working romantic SAGA flow running in a local or cloud-based Kubernetes cluster, viewable through a dashboard, and deployable by your team.

Good luck — and may love be on your side! 💞

---

## ✨ Author

Created with love by Fredy Ballesteros — DevOps Engineer & Educator.  
Inspired by microservices patterns and a bit of drama.
