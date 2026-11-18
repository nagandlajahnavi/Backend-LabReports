# Lab 4: Registration, login and JWT

**Name:** N. Jahnavi  
**Registration number:** 252U1R3063  
**Section:** CSE-DS-2B  
---

## Overview

This project implements secure user registration and authentication using **Node.js**, **Express.js**, **SQLite**, **Bcrypt** (for password hashing), and **JSON Web Tokens (JWT)**. It ensures that passwords are never stored or logged in plain text, validates user inputs, enforces unique usernames, and issues signed JWT tokens upon successful authentication.

---

## How to Run

### Prerequisites
- Node.js (v18+ recommended)
- npm (v9+ recommended)

### Installation Steps

1. **Navigate to `lab-04` directory:**
   ```bash
   cd lab-04
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure Environment Variables:**
   Create a `.env` file from `.env.example`:
   ```bash
   cp .env.example .env
   ```
   *Example `.env` configuration:*
   ```env
   PORT=3000
   NODE_ENV=development
   DB_PATH=./database.db
   JWT_SECRET=your_jwt_secret_key_here
   ```

4. **Start the API Server:**
   ```bash
   # Development mode (auto-reload)
   npm run dev

   # Production mode
   npm start
   ```

5. **Run Integration Tests:**
   ```bash
   npm test
   ```

---

## Endpoints Table

| Method | Path | Description | Request Body Parameters | Status Codes |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | API Information and Welcome Route | None | `200 OK` |
| `POST` | `/register` | Register a new user with hashed password | `username`, `name`, `password` | `201 Created`, `400 Bad Request` |
| `POST` | `/login` | Authenticate user and return JWT token | `username`, `password` | `200 OK`, `400 Bad Request` |

---

## Screenshots

### 1. POST /register - Success (201 Created)
Hashes password with `bcrypt.hash` and stores the new user in the SQLite database.
![POST /register Success](screenshots/01_post_register_success.png)

### 2. POST /register - Username Conflict (400 Bad Request)
Rejects registration attempt when the username already exists in the database.
![POST /register Conflict](screenshots/02_post_register_conflict.png)

### 3. POST /register - Validation Error (400 Bad Request)
Validates required fields and minimum password length, returning 400 with error details.
![POST /register Validation Error](screenshots/03_post_register_validation.png)

### 4. POST /login - Success (200 OK)
Compares password with `bcrypt.compare` and returns a signed `{ jwt_token }` containing only the username.
![POST /login Success](screenshots/04_post_login_success.png)

### 5. POST /login - Unknown User Error (400 Bad Request)
Returns HTTP 400 when attempting login with a non-existent username.
![POST /login Unknown User](screenshots/05_post_login_unknown_user.png)

### 6. POST /login - Wrong Password Error (400 Bad Request)
Returns HTTP 400 when authentication fails due to incorrect password.
![POST /login Wrong Password](screenshots/06_post_login_wrong_password.png)

---

## Notes: Problems Faced and How You Solved Them

1. **Plain-Text Password Security Risk**:
   - *Issue:* Storing passwords in plain text in the database is a major security vulnerability.
   - *Fix:* Integrated `bcrypt` to securely salt and hash passwords using `bcrypt.hash()` during registration and verify credentials using `bcrypt.compare()` during login.

2. **JWT Payload Sensitive Data Exposure**:
   - *Issue:* Risk of including sensitive info (such as password hashes or personal data) inside the JWT payload.
   - *Fix:* Restricted the JWT payload strictly to the non-sensitive identifier (`username`), ensuring passwords and hashes are never exposed in tokens.

3. **Database Unique Constraint Handling**:
   - *Issue:* Duplicate username registration attempts could cause unhandled SQL unique constraint exceptions.
   - *Fix:* Added explicit pre-check queries (`SELECT * FROM users WHERE username = ?`) in the `/register` endpoint to return a clean `400 Bad Request` response with `"Username already exists"`.

---

## Viva Questions & Answers

### 1. Why POST for login?
- **POST** is used for login because authentication sends sensitive credentials (username and password) in the request body rather than URL query parameters, preventing credentials from appearing in server access logs, browser history, or proxy caches. Furthermore, login creates an authentication session/token rather than retrieving a static resource.

### 2. Hash vs encrypt?
- **Hashing (e.g., bcrypt):** A one-way mathematical transformation that is irreversible. It is used for password verification (comparing hashes without needing the original plaintext).
- **Encryption (e.g., AES):** A two-way transformation that is reversible with a secret key or decryption key. It is used for secure data transmission or storage where the original data needs to be retrieved.

### 3. What does jwt.sign need?
- `jwt.sign()` requires three main arguments:
  1. **Payload:** The data object to encode (e.g., `{ username }`).
  2. **Secret or Private Key:** A secret string used to sign the token and verify its authenticity.
  3. **Options (optional):** Configuration parameters such as token expiration (`expiresIn`).

### 4. What should never go into the payload?
- **Passwords, password hashes, API keys, and highly sensitive personal data** should never be placed in a JWT payload because JWT payloads are only base64-encoded, not encrypted, meaning anyone who intercepts the token can easily decode and read the payload contents.
