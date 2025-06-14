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
- 🧾 **Swagger UI** with full FormData support
- 🌐 **Optional access** for public (unauthorized) `/issues`
- 🧬 **Alembic migrations** auto-generated
- 🧹 **Linting**: `black`, `isort`, `ruff` via pre-commit
- ⚙️ **.env-based config** using `pydantic-settings`
- 📬 **Email activation**: Redis-based with Celery task and 1-day TTL
- 🧪 **Dockerized** full stack with Redis, RabbitMQ, Mailhog, Celery
- 🤖 **Planned**: OpenAI GPT-4 powered Q&A endpoint (`/ask`)

---

## 🧰 Tech Stack

- **FastAPI** 0.115+ with async/await
- **SQLAlchemy 2.0 async ORM**
- **PostgreSQL** with Alembic migrations
- **JWT** with `pyjwt`, `OAuth2PasswordBearer`
- **Celery + RabbitMQ**
- **Redis** for caching (activation)
- **Mailhog** for email testing
- **Docker Compose**
- **Pydantic v2**
- **Black**, **Isort**, **Ruff** for linting

## 📬 Email Verification

- Upon registration, a user receives an email with an activation link
- Token is stored in Redis with a 1-day TTL
- Until verified, the user cannot log in
- You can resend activation via `/auth/resend-activation-email`
- You can verify via `/auth/complete-activation?token=...`

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
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_NAME=support_jss
POSTGRES_USER=postgres
POSTGRES_PASS=postgres

SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ALGORITHM=HS256

CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
CELERY_RESULT_BACKEND=rpc://

MAIL_PORT=1025
MAIL_SERVER=localhost
MAIL_USERNAME=admin@example.com
MAIL_PASSWORD=admin
MAIL_FROM=admin@example.com

REDIS_URL=redis://cache:6379/0
```

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

## ✅ Todo

- [ ] Pytest test suite
- [ ] OpenAI `/ask` endpoint (GPT-4)
