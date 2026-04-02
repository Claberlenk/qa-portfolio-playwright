# QA Automation Portfolio — Playwright + Pytest

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-1.50-green?logo=playwright&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-8.3-orange?logo=pytest&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-CI-D24939?logo=jenkins&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

End-to-end QA automation project covering **UI tests** (Playwright / saucedemo.com) and **API tests** (Requests / reqres.in), built with Python, Pytest, and Docker.

## Project structure

```
qa-portfolio-playwright/
├── tests/
│   ├── ui/                  # Playwright UI tests — saucedemo.com
│   │   ├── test_login.py
│   │   ├── test_inventory.py
│   │   ├── test_cart.py
│   │   └── test_checkout.py
│   └── api/                 # Pytest + Requests API tests — reqres.in
│       ├── test_users.py
│       └── test_auth.py
├── pages/                   # Page Object Model
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── utils/
│   ├── helpers.py           # API wrappers, shared constants
│   └── fixtures.py          # Reusable pytest fixtures
├── conftest.py              # Root fixtures (Playwright pages, logged_in)
├── Dockerfile
├── Jenkinsfile
├── pytest.ini
└── requirements.txt
```

---

## Tech stack

| Layer      | Tool / Library        | Version |
|------------|-----------------------|---------|
| Language   | Python                | 3.12    |
| UI testing | Playwright            | 1.50    |
| Runner     | Pytest                | 8.3     |
| API calls  | Requests              | 2.32    |
| Reporting  | pytest-html / Allure  | latest  |
| CI/CD      | Jenkins (Docker agent)|         |
| Container  | Docker                |         |

---

## Quick start

### 1. Clone and install

```bash
git clone https://github.com/Claberlenk/qa-portfolio-playwright.git
cd qa-portfolio-playwright

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

### 2. Run tests

```bash
# All tests
pytest

# Only API tests
pytest -m api

# Only UI tests (headed)
pytest -m ui --headed

# Specific browser
pytest -m ui --browser firefox

# With HTML report
pytest --html=reports/report.html --self-contained-html
```

### 3. Run in Docker

```bash
docker build -t qa-portfolio .
docker run --rm --ipc=host qa-portfolio

# API only
docker run --rm qa-portfolio pytest -m api

# UI only (headless, default in container)
docker run --rm --ipc=host qa-portfolio pytest -m ui
```

---

## Test coverage

### UI — [saucedemo.com](https://www.saucedemo.com)

| Module          | Scenarios |
|-----------------|-----------|
| Login           | Successful login, locked user, wrong password, empty fields, logout |
| Inventory       | Items count, add/remove to cart, sort by name A-Z/Z-A and price |
| Cart            | Items present, remove item, continue shopping, proceed to checkout |
| Checkout        | Full happy path, missing first/last name, missing postal code, total display |

### API — [reqres.in](https://reqres.in)

| Endpoint              | Scenarios |
|-----------------------|-----------|
| `GET /users`          | 200 status, schema validation, pagination |
| `GET /users/{id}`     | 200 status, schema, correct id, 404 for unknown |
| `POST /users`         | 201 status, id returned, payload echoed |
| `PUT /users/{id}`     | 200 status, `updatedAt` present |
| `PATCH /users/{id}`   | 200 status, `updatedAt` present |
| `DELETE /users/{id}`  | 204 status, empty body |
| `POST /login`         | Success with token, 400 on missing fields |
| `POST /register`      | Success with id+token, 400 on missing/undefined user |

---

## CI/CD

The `Jenkinsfile` defines a declarative pipeline with three stages:

1. **Install dependencies** — `pip install`
2. **API Tests** — runs `pytest -m api`, publishes JUnit XML
3. **UI Tests** — runs `pytest -m ui`, publishes JUnit XML + Playwright HTML report

The pipeline uses the official `mcr.microsoft.com/playwright/python` Docker image as its agent.

---

## Author

**Claberlenk** — QA Automation Engineer portfolio project.
