# Lab 3: REST API, query parameters, validation, debugging

**Name:** N. Jahnavi
**Registration number:** 252U1R3063 
**Section:** CSE-DS-2B  
**Live link:** https://bdf-lab-03-rest-api.onrender.com

---

## Overview

This project implements a complete, production-ready RESTful API for book management using **Node.js**, **Express.js**, and **SQLite**. It features resource-oriented endpoint design, dynamic query parameter filtering (`search_q`, `min_price`, `max_price`), sorting (`order_by`, `order`), pagination (`limit`, `offset`), strict POST body validation, consistent HTTP status codes (`200`, `201`, `400`, `404`, `500`), and parameterized SQL queries for security against SQL injection.

---

## How to Run

### Prerequisites
- Node.js (v18+ recommended)
- npm (v9+ recommended)

### Installation Steps

1. **Clone the repository and navigate to `lab-03` directory:**
   ```bash
   git clone <repository-url>
   cd lab-03
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

| Method | Path | Description | Query / Body Parameters | Status Codes |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | API Information and Welcome Route | None | `200 OK` |
| `GET` | `/books` | Retrieve books list with search, filter, sort & pagination | `search_q`, `min_price`, `max_price`, `order_by`, `order`, `limit`, `offset` | `200 OK`, `400 Bad Request` |
| `GET` | `/books/:id` | Retrieve a single book by ID | Path parameter: `id` | `200 OK`, `404 Not Found` |
| `POST` | `/books` | Create a new book | Body: `title` (str), `author` (str), `price` (num) | `201 Created`, `400 Bad Request` |
| `PUT` | `/books/:id` | Update an existing book by ID | Path parameter: `id`<br>Body: `title`, `author`, `price` | `200 OK`, `400 Bad Request`, `404 Not Found` |
| `DELETE` | `/books/:id` | Delete a book by ID | Path parameter: `id` | `200 OK`, `404 Not Found` |

---

## Screenshots

### 1. GET /books with Search Query (`search_q=Clean`)
Filters title using SQL `LIKE %search_q%`.
![GET /books Search Query](screenshots/01_get_books_search.png)

### 2. GET /books with Price Range Filter (`min_price=30&max_price=50`)
Filters books using price range conditions (`price >= min_price AND price <= max_price`).
![GET /books Price Range](screenshots/02_get_books_price_range.png)

### 3. GET /books with Sorting & Pagination (`order_by=price&order=DESC&limit=3`)
Sorts results dynamically by whitelisted column and returns paginated output.
![GET /books Sort and Pagination](screenshots/03_get_books_sort_pagination.png)

### 4. GET /books/:id - Success (200 OK)
Retrieves single book object when a valid ID exists.
![GET /books/:id Success](screenshots/04_get_book_by_id_success.png)

### 5. GET /books/:id - Not Found (404 Not Found)
Returns consistent 404 error response when ID does not exist.
![GET /books/:id Not Found](screenshots/05_get_book_by_id_not_found.png)

### 6. POST /books - Success (201 Created)
Validates body payload, inserts entry using parameterized query, and returns HTTP 201.
![POST /books Success](screenshots/06_post_book_success.png)

### 7. POST /books - Validation Error (400 Bad Request)
Rejects missing title/author or invalid price with HTTP 400 and JSON error list.
![POST /books Validation Error](screenshots/07_post_book_validation_error.png)

### 8. PUT /books/:id - Success (200 OK)
Updates existing book details and returns updated resource.
![PUT /books/:id Success](screenshots/08_put_book_success.png)

### 9. PUT /books/:id - Not Found (404 Not Found)
Returns HTTP 404 when attempting to update a non-existent book ID.
![PUT /books/:id Not Found](screenshots/09_put_book_not_found.png)

### 10. DELETE /books/:id - Success (200 OK)
Deletes record from database and returns HTTP 200 with confirmation message.
![DELETE /books/:id Success](screenshots/10_delete_book_success.png)

### 11. DELETE /books/:id - Not Found (404 Not Found)
Returns HTTP 404 when attempting to delete a non-existent book ID.
![DELETE /books/:id Not Found](screenshots/11_delete_book_not_found.png)

---

## Notes: Problems Faced and How You Solved Them

1. **Port Conflict (`EADDRINUSE`)**:
   - *Issue:* Server crashed with `Error: listen EADDRINUSE: address already in use :::3000` when port 3000 was occupied by another process.
   - *Fix:* Added an `error` listener on the HTTP server instance in `src/server.js` to catch `EADDRINUSE` gracefully, display a helpful error message, and support dynamic port configuration through the `PORT` environment variable (`PORT=3001 npm start`).

2. **Wrong Import Path**:
   - *Issue:* Module resolution error (`Cannot find module './db'`) when importing modules in ES Module (`"type": "module"`) mode.
   - *Fix:* Explicitly appended exact relative file paths with file extensions (`./database.js` and `./app.js`) in all import statements across `server.js`, `app.js`, and test scripts.

3. **Table-Name Typo (`no such table`)**:
   - *Issue:* Queries thrown `SQLiteError: no such table: book` because database creation script initialized table as `books` while endpoints queried singular `book`.
   - *Fix:* Standardized table name across `database.js` table initialization script and all Express route SQL queries to `books`.

4. **Missing `await` Keyword**:
   - *Issue:* Omitting `await` on asynchronous database operations (`db.all()`, `db.get()`, `db.run()`) resulted in Express sending response before Promise resolution or sending raw Promise objects.
   - *Fix:* Ensured every database call is prepended with `await` and handled inside `async (req, res, next)` route middleware functions with proper `try/catch` error propagation.

---

## Viva Questions & Answers

### 1. Query parameter vs Path parameter?
- **Path Parameters (`/books/:id`):** Used to identify a specific resource uniquely. Essential parts of the resource URL hierarchy.
- **Query Parameters (`/books?search_q=clean&limit=10`):** Used for sorting, filtering, searching, or paginating data without altering the identity of the resource endpoint.

### 2. What does stateless mean in REST?
- **Statelessness** means every client request sent to the server must contain all necessary information (authentication tokens, query parameters, request body) for the server to fulfill that request. The server does not store client state between requests.

### 3. Which status code is used for bad input vs a missing record?
- **Bad Input / Validation Failure:** `400 Bad Request` (indicates invalid parameters, missing fields, or bad payload).
- **Missing Record:** `404 Not Found` (indicates target resource ID does not exist in database).
