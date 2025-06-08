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
-  🌐 **Optional access** for public (unauthorized) `/issues`
- 🧬 **Alembic migrations** auto-generated
- 🧹 **Linting**: `black`, `isort`, `ruff` via pre-commit
- ⚙️ **.env-based config** using `pydantic-settings`
- 🤖 **Planned**: OpenAI GPT-4 powered Q&A endpoint (`/ask`)
---

## 🧰 Tech Stack

- **FastAPI** 0.115+ with async/await
- **SQLAlchemy 2.0 async ORM**
- **PostgreSQL** with Alembic migrations
- **JWT** with `pyjwt`, `OAuth2PasswordBearer`
- **Pydantic v2** for schema validation and env config
- **Black**, **Isort**, **Ruff** for linting

## 🧩 Project Structure

```
.
├── alembic/                 # Migrations
├── scripts/                 # Local run/start scripts
├── src/
│   ├── auth/                # Auth logic: login, tokens, permissions
│   ├── users/               # User models, service, endpoints
│   ├── issues/              # Issue + Message logic together
│   ├── models/              # Shared base types (intpk, etc)
│   ├── database.py
│   ├── config.py            # Pydantic settings loader
│   └── main.py              # Entry point
├── Pipfile / Pipfile.lock   # Dependencies
├── pyproject.toml           # Black, Ruff, Isort configs
├── .pre-commit-config.yaml  # Pre-commit checks
└── README.md
```

---

## 🛠 Local Setup

```bash
pip install pipenv
pipenv install --dev
pipenv shell

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
```

---

## 🔒 Auth

- Register: `/api/users`
- Login: `/api/auth/login`
- Use token in Swagger UI Authorization (🔓 top-right)

---

## 📬 Issues Flow

1. Junior creates issue
2. Senior takes it (`PUT /issues/{id}/take`)
3. Both exchange messages (`POST /issues/{id}/messages`)
4. Senior closes issue

---

## ✅ Todo (planned next)

- [ ] Docker + Docker Compose
- [ ] Redis + Celery (mail queue)
- [ ] Pytest test suite
- [ ] GitHub Actions CI
- [ ] 🧠 OpenAI integration: `/ask` endpoint for internal AI Q&A (GPT-4)
---
### 💡 Vision: AI Assistant

Planned integration with OpenAI API for a `/ask` endpoint that allows users to:

- Get instant answers to simple dev questions
- Auto-suggest tags or titles when creating an issue
- (Optional) Auto-generate a draft answer for seniors to review

This endpoint will be role-protected and use GPT-4 via OpenAI SDK.

## 💡 About

This project started as an internal support tool.  
After the company was shut down, the backend remained unused until I decided to publish it to show my backend architecture and FastAPI skills.
