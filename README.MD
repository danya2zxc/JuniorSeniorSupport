# 🧠 JuniorSeniorSupport

> Internal mentorship support tool for managing Issues between Juniors and Seniors.
> Originally built for internal use at a startup focused on mentorship matching.
> After the company closed, I decided to polish and publish the backend to demonstrate architecture skills.

---

## 🚀 Features

- 🧠 **FastAPI 0.115+** async backend
- 🔐 **JWT authentication** (pyjwt + passlib + OAuth2PasswordBearer)
- 🛡️ **Role-based access**: Junior, Senior, Admin
- 👤 **Users**: register, login, patch, delete, change password
- 📌 **Issues**:
  - ✍️ Create (Junior)
  - 🛠️ Take / ✅ Close (Senior)
  - 🧑‍💼 Full CRUD (Admin)
- 💬 **Messages**: chat inside issues (Junior ⇄ Senior only)
- 🤖 **Assistant**: OpenAI-powered `/assistant/ask` endpoint for Q&A (JWT protected, 5 req/day for Juniors)
- 🧾 **Swagger UI** with full FormData support
- 🌐 **Optional access** for public (unauthorized) `/issues`
- 🧬 **Alembic migrations** auto-generated
- 🧹 **Linting**: `black`, `isort`, `ruff` via pre-commit
- ⚙️ **.env-based config** using `pydantic-settings`
- 📬 **Email activation**: Redis-based with Celery + RabbitMQ
- 🧪 **Dockerized**: API, PostgreSQL, Redis, RabbitMQ, Celery, Mailhog

---

## 🧰 Tech Stack

- **FastAPI** 0.115+ with async/await
- **SQLAlchemy 2.0 async ORM**
- **PostgreSQL** with Alembic migrations
- **JWT** with `pyjwt`, `OAuth2PasswordBearer`
- **Celery + RabbitMQ**
- **Redis** for caching (activation, assistant rate limits)
- **Mailhog** for email testing
- **Docker Compose**
- **Pydantic v2**
- **Black**, **Isort**, **Ruff** for linting

---

## 🐳 Docker Compose

```bash
make up           # starts API, db, redis, mailhog, celery worker
make worker       # starts only celery worker (if needed separately)
make fix          # run lint/format checks
```

---

## 🛠 Local Setup

```bash
poetry install
poetry shell

# Setup DB
alembic upgrade head

# Run
uvicorn src.main:app --reload
```

---

## 🧪 Lint + Pre-commit

```bash
pre-commit install
pre-commit
```

---

## 📦 ENV Example

```env
# -------------------- PostgreSQL --------------------
POSTGRES_HOST=database
POSTGRES_PORT=5432
POSTGRES_DB=support_jss
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# -------------------- JWT ---------------------------
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ALGORITHM=HS256

# -------------------- RabbitMQ ----------------------
RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASS=guest

# -------------------- Celery ------------------------
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
CELERY_RESULT_BACKEND=rpc://

# -------------------- Mailing ------------------------
MAIL_USERNAME=dummy
MAIL_PASSWORD=dummy
MAIL_FROM=test@example.com
MAIL_PORT=1025
MAIL_SERVER=localhost

# -------------------- Redis -------------------------
REDIS_URL=redis://cache:6379/0

# -------------------- OpenAI API --------------------
OPENAI_API_KEY=your-secret-key
```

ℹ️ **Note:** Replace `OPENAI_API_KEY` with your actual key for assistant functionality.

---

## 🔒 Auth

- Register: `/auth/signup`
- Login: `/auth/login`
- Resend activation: `/auth/resend-activation-email`
- Confirm email: `/auth/complete-activation`

---

## 📬 Issues Flow

1. Junior creates issue
2. Senior takes it (`PUT /issues/{id}/take`)
3. Both exchange messages (`POST /issues/{id}/messages`)
4. Senior closes issue

---

## ✅ Roadmap

- [x] Celery + RabbitMQ for mailing
- [x] Redis caching (activation flow, rate limiting)
- [x] Assistant `/assistant/ask` endpoint (OpenAI)
- [ ] Pytest test suite
---

## 💡 About

This project started as an internal support tool.
After the company was shut down, I decided to polish and publish it to showcase backend architecture skills with FastAPI.

