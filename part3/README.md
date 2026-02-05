# 🏠 HBnB Project – Part 3  
**Enhanced Backend with Authentication & Database Integration**

---

## 📌 Overview

Part 3 of the **HBnB Project** focuses on transforming the backend from a prototype-level implementation into a **secure, scalable, and production-ready system**.

This phase introduces:
- JWT-based authentication
- Role-based authorization
- Persistent data storage using SQLAlchemy

The application uses **SQLite** for development and is prepared for **MySQL** in production.

The project follows clean architecture principles such as:
- Repository Pattern  
- Facade Pattern  
- Clear separation between API, services, and persistence layers  

---

## 🎯 Objectives

By completing this part, the backend will:

- Implement JWT Authentication using `flask-jwt-extended`
- Enforce Role-Based Access Control (RBAC) with admin privileges
- Replace in-memory storage with SQLAlchemy ORM
- Persist data using SQLite (development) and prepare for MySQL (production)
- Secure sensitive operations (users, places, reviews, amenities)
- Design and visualize the database schema using Mermaid.js
- Ensure data integrity, validation, and scalability

---

## 🧱 Project Architecture

```
├── API_TESTING.md
├── DATABASE_DIAGRAM.md
├── README.md
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   └── v1
│   │       ├── __init__.py
│   │       ├── amenities.py
│   │       ├── auth.py
│   │       ├── places.py
│   │       ├── protected.py
│   │       ├── reviews.py
│   │       └── users.py
│   ├── extensions.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── amenity.py
│   │   ├── base_model.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── user.py
│   ├── persistence
│   │   ├── __init__.py
│   │   └── repository.py
│   └── services
│       ├── __init__.py
│       ├── facade.py
│       └── repositories
│           ├── __init__.py
│           └── user_repository.py
├── config.py
├── crud_tests.sql
├── development.db
├── initial_data.sql
├── requirements.txt
├── run.py
├── tables.sql
└── test
    ├── test_amenities.py
    ├── test_auth.py
    ├── test_places.py
    └── test_reviews.py
```

---

## 🔐 Authentication & Authorization

### Authentication
- Implemented using **JWT (JSON Web Tokens)**
- Users authenticate via:


- A valid JWT is required for protected endpoints

### Authorization
- Role-based access using `is_admin`
- Two roles:
  - Regular User
  - Administrator

---

## 👤 User Roles & Permissions

### Public Endpoints (No Authentication)
- `GET /api/v1/places/`
- `GET /api/v1/places/<place_id>`

### Authenticated User Endpoints
- Create and manage own places
- Create, update, and delete own reviews
- Update own user profile (excluding email and password)

### Administrator Endpoints
- Create and modify any user
- Modify email and password of users
- Add and modify amenities
- Bypass ownership restrictions for places and reviews

---

## 🗄️ Database & Persistence

### ORM
- SQLAlchemy with Flask-SQLAlchemy

### Databases
- SQLite → Development
- MySQL → Production-ready configuration

### Repository Pattern
- Generic SQLAlchemyRepository for CRUD operations
- Specialized repositories (e.g. UserRepository) for entity-specific queries

---

## 🔗 Entity Relationships

- User → Place: One-to-Many  
- User → Review: One-to-Many  
- Place → Review: One-to-Many  
- Place ↔ Amenity: Many-to-Many  
