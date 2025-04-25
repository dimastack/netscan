# netscan — Network Scanner as a Service

**netscan** is a project that demonstrates a full DevOps workflow —  
from low-level network programming with `Scapy` to containerization, CI/CD, Kubernetes orchestration, and observability.

---

## Features

**Frontend** (React):
- Visual interface to scan IP addresses
- Real-time result display
- Ping / Traceroute / Port scanning

**Backend** (Flask + Scapy):
- `/ping?ip=...` — ICMP echo requests
- `/trace?ip=...` — basic traceroute
- `/synscan?ip=...&ports=...` — SYN port scanning

**DevOps Stack:**
- Dockerized backend & frontend
- GitHub Actions for CI/CD
- Kubernetes
- Monitoring with Prometheus & Grafana
- Logging with Loki

---

## Technologies Used

| Layer         | Stack                            |
|---------------|----------------------------------|
| Frontend      | React, Axios, Docker             |
| Backend       | Flask, Scapy, Python             |
| CI/CD         | GitHub Actions                   |
| Containers    | Docker, Docker Compose           |
| Orchestration | Kubernetes                       |
| Monitoring    | Prometheus, Grafana, Loki        |

---

## Setup

**Backend setup**
```bash
cd backend
```
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```
```bash
pip install -r requirements.txt
```

Or you can use alternative way via Makefile:

```bash
make venv        → create virtual environment
make install     → install dependencies from requirements.txt
make freeze      → update dependencies in requirements.txt from current env
make run         → run the Flask app
make clean       → delete the virtual environment
```

---
