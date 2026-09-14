# API Development

A FastAPI project with PostgreSQL, SQLAlchemy, and JWT-based authentication.

## Features

- CRUD endpoints for posts
- User registration with hashed passwords (`passlib`/`bcrypt`)
- Login endpoint that issues JWT access tokens (`python-jose`)
- SQLAlchemy ORM models with Pydantic request/response schemas

## Requirements

- Python 3.12
- PostgreSQL running locally

## Setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary "pydantic[email]" "passlib[bcrypt]" python-jose python-dotenv
   ```

3. Create a `.env` file in the project root (already excluded from git):

   ```bash
   echo "SECRET_KEY=$(openssl rand -hex 32)" > .env
   echo "ALGORITHM=HS256" >> .env
   echo "ACCESS_TOKEN_EXPIRE_MINUTES=30" >> .env
   ```

4. Update `app/database.py` with your PostgreSQL connection details.

## Running the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`.

## Project structure

```
app/
├── main.py          # App entrypoint, router registration
├── models.py        # SQLAlchemy ORM models
├── schemas.py        # Pydantic request/response schemas
├── database.py       # Database engine and session setup
├── oauth2.py          # JWT access token creation
├── utils.py           # Password hashing helpers
└── routers/
    ├── posts.py
    ├── users.py
    └── auth.py
```
