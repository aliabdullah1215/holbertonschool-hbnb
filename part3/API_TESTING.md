# HBnB API Testing Guide

دليل شامل لاختبار **HBnB API** باستخدام **cURL**، **Postman**، **Python Requests**، و **HTTPie**.

## Table of Contents

1. Getting Started
2. API Documentation
3. Authentication
4. User Endpoints
5. Amenity Endpoints
6. Place Endpoints
7. Review Endpoints
8. Testing Tools
9. Complete Test Workflow
10. Common HTTP Status Codes
11. Troubleshooting

---

## 1. Getting Started

### Start the Server

```bash
cd part3
python3 run.py
```

**Server URL:**

```
http://127.0.0.1:5000
```

---

## 2. API Documentation

* **Swagger UI:**

  ```
  http://127.0.0.1:5000/api/v1/
  ```

### Default Admin Credentials

| Field    | Value                                         |
| -------- | --------------------------------------------- |
| Email    | [admin@example.com](mailto:admin@example.com) |
| Password | admin123                                      |

---

## 3. Authentication

### Login and Get JWT Token

#### cURL

```bash
curl -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

**Expected Response**

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Save Token

```bash
export TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."
```

أو:

```bash
echo "eyJ0eXAiOiJKV1QiLCJhbGc..." > token.txt
TOKEN=$(cat token.txt)
```

### Test Invalid Login

```bash
curl -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "wrongpassword"
  }'
```

**Expected:** `401 Unauthorized`

---

## 4. User Endpoints

### Create User (Admin Only)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "password123"
  }'
```

**Expected:** `201 Created`

---

### List All Users (Admin Only)

```bash
curl -X GET http://127.0.0.1:5000/api/v1/users/ \
  -H "Authorization: Bearer $TOKEN"
```

---

### Get User by ID

```bash
USER_ID="550e8400-e29b-41d4-a716-446655440000"

curl -X GET http://127.0.0.1:5000/api/v1/users/$USER_ID \
  -H "Authorization: Bearer $TOKEN"
```

---

### Update User

```bash
curl -X PUT http://127.0.0.1:5000/api/v1/users/$USER_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "first_name": "Jane"
  }'
```

> **Note:** المستخدم يمكنه تعديل ملفه فقط، إلا إذا كان Admin.

---

### Unauthorized Access Test

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Expected:** `401 Unauthorized`

---

## 5. Amenity Endpoints

### Create Amenity (Admin Only)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "WiFi"}'
```

---

### List All Amenities (Public)

```bash
curl -X GET http://127.0.0.1:5000/api/v1/amenities/
```

---

### Update / Delete Amenity (Admin Only)

```bash
curl -X PUT http://127.0.0.1:5000/api/v1/amenities/$AMENITY_ID \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "High-Speed WiFi"}'
```

```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/amenities/$AMENITY_ID \
  -H "Authorization: Bearer $TOKEN"
```

---

## 6. Place Endpoints

### Create Place (Authenticated Users)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Cozy Apartment",
    "price": 120.5,
    "latitude": 40.7128,
    "longitude": -74.0060
  }'
```

---

### Update / Delete Place

* **Allowed:** Owner or Admin
* **Unauthorized Update:** `403 Forbidden`

---

## 7. Review Endpoints

### Create Review

```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "text": "Amazing place!",
    "rating": 5
  }'
```

**Rating Range:** `1 – 5`

---

## 8. Testing Tools

### Postman

* Import from URL:

  ```
  http://127.0.0.1:5000/api/v1/
  ```

**Environment Variables**

* `BASE_URL`
* `TOKEN`

---

### Python Requests

```python
import requests

BASE_URL = "http://127.0.0.1:5000/api/v1"
```

---

### HTTPie

```bash
pip install httpie
```

---

## 9. Complete Test Workflow

1. Start server
2. Login → Get Token
3. Create Amenities
4. Create User
5. Create Place
6. Create Review
7. Verify & Test Authorization

---

## 10. Common HTTP Status Codes

| Code | Meaning      |
| ---- | ------------ |
| 200  | OK           |
| 201  | Created      |
| 204  | No Content   |
| 400  | Bad Request  |
| 401  | Unauthorized |
| 403  | Forbidden    |
| 404  | Not Found    |
| 409  | Conflict     |
| 500  | Server Error |

---

## 11. Troubleshooting

### Token Expired

```bash
# Re-login to get new token
```

### Pretty Print JSON

```bash
curl ... | jq
```

### Debug Mode

```bash
curl -v ...
```

---

**API Version:** v1
**Base URL:**

```
http://127.0.0.1:5000/api/v1
```

**Last Updated:** 2026
