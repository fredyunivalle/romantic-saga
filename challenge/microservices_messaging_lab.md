# Microservices Messaging Project

## 📘 Project Overview
In this project, students will design and deploy a **microservices-based application** that communicates through a **message broker** such as **RabbitMQ** or **Apache Kafka**. The goal is to understand **asynchronous communication**, **message queues**, and **event-driven architectures**, while visualizing how services interact in real time.

Each student will be responsible for developing **one independent microservice or component**, which must send and/or receive messages as part of the system’s workflow.

---

## 🎯 Learning Objectives
- Understand the architecture of message-based microservices.
- Implement message producers and consumers using RabbitMQ or Kafka.
- Practice asynchronous communication and event-driven design.
- Visualize message flow between distributed components.
- Deploy the full system using Kubernetes.

---

## ⚙️ Technical Requirements
1. **Technology Stack**
   - Backend: Node.js, Python (Flask/FastAPI), or Java (Spring Boot).
   - Messaging: RabbitMQ or Apache Kafka.
   - Containerization and deployment: Kubernetes.
   - Optional visualization: tools like [RabbitMQ Management UI](https://www.rabbitmq.com/management.html) or [Kafka UI](https://github.com/provectus/kafka-ui).

2. **Minimum Architecture**
   - At least **3 microservices**: (depending on the number of members in the team)
     - **Producer service:** generates or sends messages.
     - **Consumer service:** receives and processes messages.
     - **Orchestrator or monitor service:** displays or logs the communication flow.

3. **Collaboration**
   - Each student must be responsible for **one microservice**.
   - All services must communicate through the same message broker.

---

## 🌍 Real-Life Scenarios
Below are some **realistic** and **fantasy-inspired** ideas for your system:

### 💼 Real-World Examples
1. **Online Store System**
   - Producer: Checkout service sends an order.
   - Consumer: Payment service validates and processes payment.
   - Monitor: Notification service confirms order via email.

2. **Banking Transaction System**
   - Producer: ATM service emits a withdrawal event.
   - Consumer: Ledger service updates balances.
   - Monitor: Fraud detection service analyzes transactions.

3. **Logistics and Delivery Platform**
   - Producer: Warehouse sends shipment updates.
   - Consumer: Delivery tracking service receives status.
   - Monitor: Dashboard shows delivery routes in real time.

### 🧙 Fantasy or Creative Scenarios
1. **Wizard Communication Network** 🪄
   - Producer: SpellCaster microservice sends magic spell requests.
   - Consumer: PotionMixer microservice brews the required potion.
   - Monitor: CrystalBall displays spell status updates.

2. **Space Mission Control** 🚀
   - Producer: Satellite service sends telemetry data.
   - Consumer: Ground Control processes signals.
   - Monitor: Mission Dashboard visualizes system health.

3. **Love Message System ❤️**
   - Producer: Admirer microservice sends love letters.
   - Consumer: Receiver microservice reads and reacts.
   - Monitor: Cupid Dashboard visualizes message flow and matches.

---

## 🧩 Project Deliverables
1. **Source Code:** All microservices with Dockerfiles.
2. **Kubernetes manifests:** to deploy the system.
3. **Documentation:** README explaining architecture, team roles, and execution steps.
4. **In-class DEMO (10–15 min):** showing:
   - System deployment.
   - Message interactions in real time.
   - Explanation of roles and message flow.

---

## 🧠 Suggested Tools
- **RabbitMQ Management UI** to visualize message queues.
- **Kafka UI** to monitor topics and consumers.
- **Postman or curl** to send test messages.
- **Docker Compose** to orchestrate services locally.
- **Kubernetes** to deploy all microservices.



## 👩‍💻 Team Roles
Each team member should specify:
- **Name and microservice assigned.**
- **Message type produced or consumed.**
- **Tools and language used.**

Example:
| Student | Microservice | Role | Technology |
|----------|---------------|------|-------------|
| Alice | Payment Service | Consumer | Python + RabbitMQ |
| Bob | Order Service | Producer | Node.js + RabbitMQ |
| Carol | Notification Service | Monitor | React + WebSocket |

---

## 💬 Final Recommendation
Think of your microservice as **a small character in a connected world** — it should speak through messages, react to events, and contribute to a shared goal. Whether you build a **smart city**, a **galactic control center**, or a **kingdom of talking microservices**, the key is to demonstrate clear **asynchronous communication** and teamwork.

