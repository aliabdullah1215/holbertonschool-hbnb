---

# 🏠 HBnB Project – Part 3

**Enhanced Backend with Authentication & Database Integration**

## 📌 Overview

Part 3 of the **HBnB Project** focuses on transforming the backend from a prototype-level implementation into a **secure, scalable, and production-ready system**.
This phase introduces **JWT-based authentication**, **role-based authorization**, and **persistent data storage** using **SQLAlchemy** with **SQLite** for development and **MySQL** for production readiness.

The project follows clean architecture principles, including the **Repository Pattern**, **Facade Pattern**, and clear separation between API, services, and persistence layers.

---

## 🎯 Objectives

By completing this part, the backend will:

* Implement **JWT Authentication** using `flask-jwt-extended`
* Enforce **Role-Based Access Control (RBAC)** with admin privileges
* Replace in-memory storage with **SQLAlchemy ORM**
* Persist data using **SQLite** (development) and prepare for **MySQL** (production)
* Secure sensitive operations (users, places, reviews, amenities)
* Design and visualize the database schema using **Mermaid.js**
* Ensure data integrity, validation, and scalability

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

* Implemented using **JWT (JSON Web Tokens)**
* Users authenticate via:

  ```
  POST /api/v1/auth/login
  ```
* A valid JWT is required for protected endpoints

### Authorization

* Role-based access using `is_admin`
* Two roles:

  * **Regular User**
  * **Administrator**

---

## 👤 User Roles & Permissions

### Public Endpoints (No Authentication)

* `GET /api/v1/places/`
* `GET /api/v1/places/<place_id>`

### Authenticated User Endpoints

* Create and manage **own places**
* Create, update, and delete **own reviews**
* Update **own user profile** (excluding email & password)

### Administrator Endpoints

* Create and modify **any user**
* Modify **email and password** of users
* Add and modify **amenities**
* Bypass ownership restrictions for places and reviews

---

## 🗄️ Database & Persistence

### ORM

* **SQLAlchemy** with **Flask-SQLAlchemy**

### Databases

* **SQLite** → Development
* **MySQL** → Production-ready configuration

### Repository Pattern

* Generic `SQLAlchemyRepository` for CRUD
* Specialized repositories (e.g. `UserRepository`) for entity-specific queries

---

## 🔗 Entity Relationships

* **User → Place**: One-to-Many
* **User → Review**: One-to-Many
* **Place → Review**: One-to-Many
* **Place ↔ Amenity**: Many-to-Many

All relationships are enforced via **foreign keys** and **association tables**.

---

## 🧩 Database Diagram (Mermaid.js)


Below is the ER diagram representing the core entities and their relationships in the HBnB system, created using Mermaid.js:

```
mermaid

erDiagram
    USERS {
        uuid id PK
        string first_name
        string last_name
        string email UK
        string password
        boolean is_admin
        datetime created_at
        datetime updated_at
    }

    PLACES {
        uuid id PK
        string title
        string description
        decimal price
        float latitude
        float longitude
        uuid owner_id FK
        datetime created_at
        datetime updated_at
    }

    REVIEWS {
        uuid id PK
        string text
        int rating
        uuid user_id FK
        uuid place_id FK
        datetime created_at
        datetime updated_at
    }

    AMENITIES {
        uuid id PK
        string name UK
        datetime created_at
        datetime updated_at
    }

    PLACE_AMENITY {
        uuid place_id PK,FK
        uuid amenity_id PK,FK
        datetime created_at
        datetime updated_at
    }

    USERS ||--o{ PLACES : "owns"
    USERS ||--o{ REVIEWS : "writes"
    PLACES ||--o{ REVIEWS : "has"
    PLACES ||--o{ PLACE_AMENITY : ""
    AMENITIES ||--o{ PLACE_AMENITY : ""

```

---

## 🔑 Security Measures

* Passwords are hashed using **bcrypt**
* Passwords are never exposed in API responses
* JWT tokens are required for protected operations
* Ownership validation for user-generated content
* Unique constraints enforced at database level

---

## 🧪 Testing

* API tested using **Postman** and **cURL**
* Manual testing of:

  * Authentication flow
  * Authorization checks
  * Ownership restrictions
  * Admin privileges
  * CRUD operations

---

## 🛠️ Installation & Setup

### Requirements

```txt
flask
flask-restx
flask-jwt-extended
flask-bcrypt
flask-sqlalchemy
sqlalchemy
```

### Initialize Database

```bash
flask shell
>>> from app import db
>>> db.create_all()
```

### Run Application

```bash
python run.py
```

---

## 🚀 Expected Outcome

By the end of **Part 3**, the HBnB backend:

* Is fully **authenticated and authorized**
* Uses **persistent relational storage**
* Follows **clean architecture principles**
* Is **secure**, **scalable**, and **production-ready**
* Is well-documented with **ER diagrams and SQL scripts**

---

## 🧑‍💻 Authors

* Ali Abdullah Summan
* Ali Hassan Almaghrabi
* Omar Hail Alanzi

---

## 📚 References

* Flask Documentation
* Flask-JWT-Extended
* Flask-SQLAlchemy
* SQLAlchemy ORM
* OWASP Security Best Practices
* Mermaid.js Documentation
