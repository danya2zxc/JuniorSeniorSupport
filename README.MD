# 🧠 JuniorSeniorSupport

[![Python Version](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)
[![Tests](https://img.shields.io/badge/Tests-Pytest-informational.svg)](https://pytest.org/)
[![codecov](https://codecov.io/gh/danya2zxc/JuniorSeniorSupport/graph/badge.svg)](https://codecov.io/gh/danya2zxc/JuniorSeniorSupport)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)


> An internal mentorship support tool for managing Issues between Junior and Senior developers. Originally built for internal use at a startup, this project was later polished and published as a backend architecture and development skills showcase.

---

## ✨ Key Features

- **Authentication & Authorization**: Secure system based on JWT tokens with role-based access control (Junior, Senior, Admin).
- **User Management**: Full lifecycle from registration with email activation to password changes and profile deletion.
- **Issue Tracking System**:
  - **Junior**: Can create issues and participate in the chat.
  - **Senior**: Can take issues, resolve them, and participate in the chat.
  - **Admin**: Has full CRUD access to all issues.
- **Internal Chat**: Exchange messages within each issue between the assigned Junior and Senior.
- **AI Assistant**: OpenAI integration (`/assistant/ask`) to help resolve issues, protected by JWT and rate-limiting.
- **Background Tasks**: Celery and RabbitMQ for asynchronous operations like sending emails without blocking the main application.
- **Caching**: Redis for storing activation tokens and implementing rate-limiting.
- **Database Migrations**: Alembic for managing the database schema.
- **Comprehensive Test Coverage**: Code reliability ensured by integration and unit tests with Pytest.
- **API Documentation**: Auto-generated interactive documentation via Swagger UI and ReDoc.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, Uvicorn
- **Database**: PostgreSQL (asynchronous with `SQLAlchemy 2.0` and `asyncpg`)
- **Migrations**: Alembic
- **Background Tasks**: Celery
- **Message Broker**: RabbitMQ
- **Cache / In-memory DB**: Redis
- **Typing & Config**: Pydantic V2
- **Testing**: Pytest, `httpx`, `unittest.mock`
- **Dependency Management**: Poetry
- **Linting & Formatting**: Ruff, Black, isort (via `pre-commit`)

---

## 🔌 Integrations

- **AI Services**: OpenAI API for the assistant feature.

---

## 🚀 Getting Started / Local Setup

### Prerequisites
- Python 3.11+
- Poetry
- Docker and Docker Compose (for PostgreSQL, Redis, RabbitMQ)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/JuniorSeniorSupport.git
    cd JuniorSeniorSupport
    ```

2.  **Create and configure the `.env` file:**
    Copy the example environment file and fill in your details.
    ```bash
    cp .env.example .env
    ```
    *You will need to provide your database credentials, a secret key, and an OpenAI token.*

3.  **Launch services with Docker:**
    This command will start the PostgreSQL, Redis, and RabbitMQ containers.
    ```bash
    docker-compose up -d
    ```

4.  **Install project dependencies:**
    Poetry will create a virtual environment and install all required packages.
    ```bash
    poetry install
    ```

5.  **Apply the database migrations:**
    This command will create all the necessary tables in your database.
    ```bash
    poetry run alembic upgrade head
    ```

6.  **Run the application:**
    ```bash
    poetry run uvicorn src.main:app --reload
    ```

7.  **Run the Celery worker (in a separate terminal):**
    ```bash
    poetry run celery -A src.mailing.tasks worker -l INFO
    ```

The application is now available at `http://127.0.0.1:8000`, and the interactive API documentation is at `http://127.0.0.1:8000/docs`.

---

## ✅ Testing

To run the entire test suite (both integration and unit tests), execute the following command:

```bash
poetry run pytest
```
