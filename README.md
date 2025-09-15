# ChatterDock

ChatterDock is a modern messaging app built with **Flask**, **MongoDB**, **Nginx**, and **Celery**.
It supports asynchronous message processing, real-time updates, and scalable deployment using Docker.

---

## Features

* User registration and authentication
* Send and receive messages
* Message queues handled with Celery
* MongoDB for message storage
* Nginx as a reverse proxy for Flask API
* Dockerized for easy deployment

---

## Project Structure

```
ChatterDock/
├── backend/                  # Flask backend
│   ├── app.py
│   ├── models.py
│   ├── config.py
│   ├── requirements.txt
│   └── ...
├── docker-compose.yaml
├── Dockerfile                # Flask backend
├── Dockerfile.nginx          # Nginx for backend
├── Dockerfile.celery         # Celery worker
└── README.md
```

---

## Prerequisites

* Docker & Docker Compose installed
* Python 3.10+ (for local dev)
* MongoDB (if not using Dockerized Mongo)

---

## Docker Setup

1. Build and start all services:

```bash
sudo docker compose up -d --build
```

2. Check running containers:

```bash
sudo docker ps
```

3. Stop containers:

```bash
sudo docker compose down
```

---

## API Endpoints

### 1. Get all messages (Read)

```bash
curl -X GET http://<your-domain-or-localhost>/messages
```

### 2. Get a specific message by ID (Read)

```bash
curl -X GET http://<your-domain-or-localhost>/messages/<id>
```

### 3. Send a new message (Create)

```bash
curl -X POST http://<your-domain-or-localhost>/messages \
-H "Content-Type: application/json" \
-d '{
  "sender": "Alice",
  "receiver": "Bob",
  "message": "Hello, Bob!"
}'
```

### 4. Update a message by ID (Update)

```bash
curl -X PUT http://<your-domain-or-localhost>/messages/<id> \
-H "Content-Type: application/json" \
-d '{
  "message": "Updated message content"
}'
```

### 5. Delete a message by ID (Delete)

```bash
curl -X DELETE http://<your-domain-or-localhost>/messages/<id>
```

✅ Tips:

* Replace `<id>` with the actual message ID.
* Replace `<your-domain-or-localhost>` with your deployed domain or `localhost:5000`.
* Use `-v` with curl to see detailed request/response info:

```bash
curl -v -X GET http://<your-domain-or-localhost>/messages
```

---

## Celery Worker

* Celery handles asynchronous tasks (like message processing, notifications).
---

## Nginx

* Nginx serves as a reverse proxy for Flask.
* The Nginx config is located in `Dockerfile.nginx` and `nginx.conf`.

---

*ChatterDock is a work-in-progress. Contributions and feedback are welcome!*
