# Placement Management System API

A production-style backend application built with **FastAPI** for managing campus placement activities.

This project is part of my journey to becoming a Software Engineer. Instead of only following tutorials, I am building this project incrementally while learning backend engineering, databases, authentication, testing, deployment, and scalable software design.

---

## 📖 About the Project

The Placement Management System API is designed to simulate a real-world backend used for managing campus placements.

It provides REST APIs for managing students and will gradually expand to support companies, placement drives, applications, authentication, analytics, and other production-level features.

The project is intentionally built in phases to understand how real backend systems evolve over time.

---

## ✨ Current Features

- Student CRUD APIs
  - Get all students
  - Get student by ID
  - Create student
  - Update student
  - Delete student
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
| GET | `/students/` | Get all students |
| GET | `/students/{id}` | Get student by ID |
| POST | `/students/` | Create a student |
| PUT | `/students/{id}` | Update student details |
| DELETE | `/students/{id}` | Delete a student |

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

- [ ] PostgreSQL
- [ ] SQLAlchemy ORM
- [ ] Alembic Migrations
- [ ] Database Relationships

---

## Phase 3 — Authentication & Security

- [ ] JWT Authentication
- [ ] Password Hashing
- [ ] Login System
- [ ] Role-Based Access Control
- [ ] Protected Routes

---

## Phase 4 — Placement Management

- [ ] Company APIs
- [ ] Placement Drive APIs
- [ ] Student Applications
- [ ] Eligibility Management
- [ ] Recruitment Workflow

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
