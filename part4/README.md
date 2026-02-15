# Part 4 — Simple Web Client (HBnB)

## 📌 Overview
This part implements a **simple frontend web client** for the HBnB project using:
- **HTML5**
- **CSS3**
- **JavaScript (ES6)**

The web client connects to the backend API (Part 3) using the **Fetch API** and manages the session using a **JWT token stored in cookies**.

## ✅ Objectives
- Build the required pages following the provided structure and styles.
- Implement login using the backend API.
- Store the JWT token in a cookie for session management.
- Fetch and display places dynamically.
- Display place details (amenities + reviews).
- Allow authenticated users to add reviews.

## 📄 Pages
### 1) `login.html`
- Login form (email + password)
- On success:
  - stores JWT token in a cookie
  - redirects to `index.html`

### 2) `index.html`
- Displays list of places as cards
- Includes a **price filter** dropdown (`10`, `50`, `100`, `All`)
- Redirects to login if user is not authenticated
- Shows/hides Login/Logout link depending on authentication status

### 3) `place.html`
- Displays detailed information for one place:
  - host
  - price
  - description
  - amenities
  - reviews (comment + username + rating)
- Shows the review section only if the user is authenticated

### 4) `add_review.html`
- Review form (text + rating)
- Only accessible to authenticated users
- Sends review to the backend and redirects back to `place.html`

## 🧠 JavaScript Modules
### `auth.js`
- Handles login request using Fetch API
- Saves JWT token in cookies
- Redirects after successful login
- Displays error message on failure

### `places.js`
- Reads JWT token from cookies
- Loads places list from API
- Builds place cards dynamically
- Implements client-side price filtering
- Handles logout by clearing the cookie

### `place_details.js`
- Reads place ID from URL query string
- Fetches place details from the API
- Renders amenities + reviews dynamically
- Shows/hides review section based on authentication

### `add_review.js`
- Validates authentication (token must exist)
- Reads place ID from URL
- Submits review to the API using Authorization header
- Redirects back to place details after success

## 🔐 Authentication & Session
- JWT is stored in a cookie named `token`
- Authenticated requests include:
  - `Authorization: Bearer <token>`

If no token is found:
- `index.html` redirects to `login.html`
- `add_review.html` redirects to `index.html`

## 🔗 Backend API Requirements (Part 3)
The frontend expects the backend to be running and accessible at:
- `http://127.0.0.1:5000` (default)

Required endpoints:
- `POST /api/v1/auth/login`
- `GET /api/v1/places/`
- `GET /api/v1/places/<place_id>`
- `POST /api/v1/reviews/`

CORS must be enabled on the backend for browser requests.

## 📁 Directory Structure (Part 4)
```text
part4/
├── index.html
├── login.html
├── place.html
├── add_review.html
├── styles.css
└── scripts/
    ├── auth.js
    ├── places.js
    ├── place_details.js
    └── add_review.js
