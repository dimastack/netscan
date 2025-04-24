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
