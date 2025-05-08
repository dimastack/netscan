# Tests for Netscan Backend

This directory contains automated tests for the Netscan backend. It supports:

- ✅ Unit tests for API routes using `pytest`
- 🕹 Future UI tests with `Playwright`
- 📈 Future load tests with `Locust`

---

## Directory Structure

```md
tests/
├─ load/
│  ├─ scenarios/
│  │  └─ auth.py
│  ├─ __init__.py
│  └─ locustfile.py
├─ ui/
│  ├─ __init__.py
│  └─ test_user_flow.py
├─ unit/
│  ├─ api/
│  │  └─ test_api.py
│  ├─ auth/
│  │  ├─ test_login.py
│  │  ├─ test_me.py
│  │  └─ test_register.py
│  ├─ dns/
│  │  ├─ test_lookup.py
│  │  ├─ test_reverse.py
│  │  └─ test_whois.py
│  ├─ scan/
│  │  ├─ test_banner.py
│  │  ├─ test_os_fingerprint.py
│  │  ├─ test_ping.py
│  │  ├─ test_portscan.py
│  │  └─ test_traceroute.py
│  ├─ utils/
│  │  ├─ test_headers.py
│  │  ├─ test_latency.py
│  │  └─ test_resolve.py
│  ├─ web/
│  │  ├─ test_httpcheck.py
│  │  └─ test_sslcheck.py
│  └─ __init__.py
├─ conftest.py
└─ README.md
```
---

## Prerequisites

- Docker is running and you have containers for:
  - PostgreSQL
  - Netscan backend API
- Database migrations are applied (`alembic upgrade head`)
- Python 3.13+ installed
- Install required dependencies:

```bash
pip install -r requirements-dev.txt
```
---

## Running Tests

By default, tests run against Flask running in Docker container and accessible by http://localhost:5001/api/v1. You can override it using the --api-url CLI flag.

```bash
pytest tests/unit
pytest -m "unit and not scan and not dns and not utils"
pytest tests/unit/auth/test_login.py::test_login_with_invalid_credentials
```
To run with a custom backend:

```bash
pytest tests/unit --api-url=http://localhost:5001/api/v1
pytest tests/unit -m "dns and scan" --api-url=https://api.netscan.io/api/v1
```

All availible test markers are listed in pytest.ini in the root of project.

---

## Authentication
Tests use the registered_user and token_header fixtures:
- A unique test user is registered before tests
- JWT is automatically retrieved and reused for authenticated requests

---

## Test Philosophy
- Repeatable and stateless
- Each test can run independently
- Shared setup lives in conftest.py
- Built for easy extension to UI and load tests

---

## Planned Extensions
|Type       | Tool       | Folder   |
|-----------|------------|----------|
|Unit tests | Pytest     | unit/    |
|UI tests   | Playwright | ui/      |
|Load tests | Locust     | load/    |

Each test type will use conftest.py for shared setup and will support running against local or remote API environments.

---