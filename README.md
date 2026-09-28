# Placement Management System API

A production-style backend application built with **FastAPI** for managing campus placement activities.

This project is built incrementally to explore backend engineering, databases, authentication, and scalable software design.

---

## 📖 About the Project

The Placement Management System API is designed to simulate a real-world backend used for managing campus placements.

It provides REST APIs for managing student profiles, accounts, companies, placement drives, applications, and recruitment progress.

The project is intentionally built in phases to understand how real backend systems evolve over time.

---

## ✨ Current Features

- Student profile APIs with student self-service and admin management
- JWT authentication with Argon2 password hashing
- Role-based access control for admins and students
- Company and placement drive APIs
- Eligibility checks and student applications
- Recruitment application status workflow
- PostgreSQL persistence with SQLAlchemy ORM and Alembic migrations
- FastAPI modular routing using APIRouter
- Request validation using Pydantic
- Interactive Swagger UI documentation
- OpenAPI specification generation
- RESTful API design

---

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI

### Validation
- Pydantic

### API Documentation
- OpenAPI
- Swagger UI

### Version Control
- Git
- GitHub

### Deployment
- FastAPI Cloud

---

## 📂 Project Structure

```
placement-management-api/
│
├── app/
│   ├── main.py
│   └── routers/
│       └── students.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

The project structure will continue evolving as new modules are added.

---

## 📚 API Endpoints

### Student APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/auth/register/student` | Register student account and profile |
| POST | `/auth/login` | Exchange email/password for JWT |
| GET | `/auth/me` | Get the authenticated account |
| GET | `/students/me` | Get the authenticated student's profile |
| GET | `/students/` | List students (admin) |
| GET | `/students/{student_id}` | Get a profile (self or admin) |
| POST/PUT/DELETE | `/students/`, `/students/{student_id}` | Manage profiles (admin) |
| GET/POST/PUT/DELETE | `/companies/`, `/companies/{company_id}` | Browse companies; admins manage them |
| GET/POST/PUT/DELETE | `/drives/`, `/drives/{drive_id}` | Browse open drives; admins manage them |
| GET | `/drives/{drive_id}/eligibility` | Check the authenticated student's eligibility |
| POST | `/applications/` | Apply with JSON body `{"drive_id": 1}` |
| GET | `/applications/` | List own applications (student) or all (admin) |
| PATCH | `/applications/{application_id}/status` | Advance/reject an application (admin) |

Authenticated endpoints use `Authorization: Bearer <token>`. Admins are provisioned with `python -m app.create_admin <email>`; public registration only creates student accounts. Applications advance from `submitted` through review, shortlist, interview, selection, and offer, with rejection, acceptance, and decline as terminal states.

---

## ▶️ Running the Project

Clone the repository

```bash
git clone https://github.com/kgsgunpro/placement-management-system-api.git
```

Go into the project

```bash
cd placement-management-system-api
```

Create a virtual environment

### Windows

```bash
python -m venv .venv
```

Activate it

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set the PostgreSQL credentials and a random `JWT_SECRET` of at least 32 characters. Alternatively, set `DATABASE_URL` to a PostgreSQL connection URL. The default database is `localhost:5432/placement_db`.

Apply the schema. The initial migration adds account linkage to the project's existing `students` table when present:

```bash
alembic upgrade head
```

Create the initial administrator; the password is prompted without echo and must be at least 12 characters:

```bash
python -m app.create_admin admin@example.com
```

Seed repeatable demo students, companies, placement drives, and one sample application:

```bash
python -m app.seed_demo_data
```

The two student accounts use the email addresses in `app/seed_demo_data.py` and the `DEMO_STUDENT_PASSWORD` from `.env`. One student meets the sample software drive's criteria; the other does not. These credentials are for a test database only.

To create the sample test admin, student accounts, companies, drives, and one application from the `TEST_*` values in `.env`, run:

```bash
python -m app.seed_sample_data
```

The sample accounts are `test-admin@example.com`, `test-student@example.com`, and `test-student-ineligible@example.com`; the two students share `TEST_STUDENT_PASSWORD`. Sample company and drive records are safe to re-seed. These credentials are for an isolated test database only.

Run the application

```bash
fastapi dev app/main.py
```

---

## 📄 API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

OpenAPI Specification

```
http://127.0.0.1:8000/openapi.json
```

---

# 🚀 Roadmap

This project is being developed incrementally to understand how production backend systems are built.

## Phase 1 — Foundation ✅

- [x] FastAPI setup
- [x] CRUD APIs
- [x] OpenAPI Documentation
- [x] APIRouter
- [x] Modular Project Structure

---

## Phase 2 — Database

- [x] PostgreSQL
- [x] SQLAlchemy ORM
- [x] Alembic Migrations
- [x] Database Relationships

---

## Phase 3 — Authentication & Security

- [x] JWT Authentication
- [x] Password Hashing
- [x] Login System
- [x] Role-Based Access Control
- [x] Protected Routes

---

## Phase 4 — Placement Management

- [x] Company APIs
- [x] Placement Drive APIs
- [x] Student Applications
- [x] Eligibility Management
- [x] Recruitment Workflow

---

## Phase 5 — Production Readiness

- [ ] Docker
- [ ] Environment Variables
- [ ] Logging
- [ ] Testing using pytest
- [ ] CI/CD Pipeline

---

## Phase 6 — Advanced Features

- [ ] Search
- [ ] Filtering
- [ ] Pagination
- [ ] Email Notifications
- [ ] Analytics APIs
- [ ] File Uploads

---

# 🌍 Long-Term Vision

The long-term goal is to evolve this project from a learning project into a production-ready backend platform.

Potential future capabilities include:

- Multi-college support (Multi-Tenant Architecture)
- College-specific frontends connected to the same backend
- Student Resume Management
- Company Recruitment Portal
- Interview Scheduling
- Placement Analytics Dashboard
- Notification Service
- AI-powered Resume Analysis
- AI Interview Preparation Assistant
- AI-based Student Recommendation System

---

## 💡 Engineering Philosophy

This project follows a simple philosophy:

> **Build software that is simple today, scalable tomorrow, and maintainable for years.**

Instead of copying tutorials, each feature is implemented after understanding the underlying engineering concepts.

The goal is not just to complete a project, but to learn how real backend systems are designed, built, and maintained.

---

## 👨‍💻 Author

**K Gunasekhar**

B.Tech, Electronics and Communication Engineering

National Institute of Technology Andhra Pradesh

GitHub:
https://github.com/kgsgunpro

LinkedIn:
https://linkedin.com/in/k-gunasekhar-603980337

---

⭐ If you found this project interesting, consider giving it a star.
