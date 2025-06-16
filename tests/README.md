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
│  ├─ e2e/
│  │  ├─ test_dashbord_general.py
│  │  ├─ test_user_login.py
│  │  └─ test_user_registration.py
│  ├─ pages/
│  │  ├─ base_page.py
│  │  ├─ dashboard_page.py
│  │  ├─ login_page.py
│  │  └─ register_page.py
│  ├─ __init__.py
│  ├─ conftest.py
│  └─ playwright.config.py
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
│  │  ├─ test_resolve.py
│  │  └─ test_reverse_dns.py
│  ├─ web/
│  │  ├─ test_httpcheck.py
│  │  └─ test_sslcheck.py
│  └─ __init__.py
├─ config.py
├─ conftest.py
└─ README.md
```
---

## Prerequisites

- Docker is running and you have containers running with docker-compose.yml for:
  - PostgreSQL
  - Netscan backend API
- Database migrations are applied (`alembic upgrade head`)
- Python 3.13+ installed
- Install required dependencies:

```bash
pip install -r requirements-dev.txt
```
- To run frontend (React + Vite) test server you need npm>=10.9 and node>=23.11.0 installed.
```bash
cd /netscan/frontend/app
npm run dev
```
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

## Running API Tests

By default, tests run against Flask served from a Docker container and accessible at http://localhost:5001/api/v1. You can override this URL using the --api-url CLI flag.

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

## Running Playwright Tests

By default, Playwright tests run against the React frontend served from a Docker container and accessible at http://localhost:5173. You can override this URL using the --ui-url CLI flag.

```bash
pytest tests/ui
pytest -m "ui"
pytest tests/ui/e2e/test_dashbord_general.py::test_dashboard
```

To run with a custom backend:

```bash
pytest tests/ui --ui-url=http://localhost:5001/api/v1
pytest -m ui --ui-url=https://netscan.io/
```

To run on CI in headless mode:
```bash
pytest tests/ui --headless
```
---
