# Task Manager API (Flask + JWT Auth Backend)

A secure Flask REST API for a Task Manager application that allows users to register, login, and manage personal tasks. Each user can only access their own tasks, ensuring full authentication and authorization using JWT.

---

## Features

- User Registration & Login (JWT Authentication)
- Password hashing using Flask-Bcrypt
- Protected routes using JWT
- User-specific Tasks resource (CRUD)
- Secure access control (users cannot access others' tasks)
- RESTful API design
- Database migrations using Flask-Migrate

---

## Tech Stack

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- Flask-JWT-Extended
- SQLite

---

## Project Structure
```text
flask-c10-summative-lab-sessions-and-jwt-clients/
│
├── task-manager-api/
│   ├── app.py                  # Main Flask app (routes + setup)
│   ├── models.py               # Database models (User, Task)
│   ├── config.py               # App configuration (DB, JWT)
│   ├── requirements.txt        # Dependencies
│   ├── Pipfile / Pipfile.lock  # (if using pipenv)
│   │
│   └── instance/               # (hidden in explanation, optional in repo)
│       └── app.db
│
├── client-with-jwt/            # React frontend (JWT auth client)
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── package-lock.json
│
├── client-with-sessions/       # React frontend (session auth client)
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── package-lock.json
│
└── migrations/                 # (Flask-Migrate, auto-generated)
    ├── alembic.ini
    ├── env.py
    ├── script.py.mako
    └── versions/
```
---

## Installation Setup

git clone https://github.com/Mitchelle-git/flask-c10-summative-lab-sessions-and-jwt-clients.git
cd flask-c10-summative-lab-sessions-and-jwt-clients/task-manager-api

---

## Create Virtual Environment

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

---

## Install Dependencies

pip install -r requirements.txt

---

## Environment Variables

DATABASE_URL=sqlite:///instance/app.db
JWT_SECRET_KEY=super-secret-key

---

## Database Setup

flask db init
flask db migrate -m "initial migration"
flask db upgrade

---

## Seed (optional)

flask shell

from models import db, User, Task

db.create_all()

u1 = User(username="admin")
u1.set_password("admin123")

t1 = Task(task_name="Setup project", description="Initial task", owner=u1)

db.session.add(u1)
db.session.add(t1)
db.session.commit()

---

## Run App

flask run

http://127.0.0.1:5000

---

## Endpoints

POST /signup
POST /login
GET /me

POST /tasks
GET /tasks
GET /tasks/<id>
PATCH /tasks/<id>
DELETE /tasks/<id>

---

## Security

- bcrypt password hashing
- JWT protected routes
- user isolation enforced
