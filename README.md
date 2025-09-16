# Secure Flask REST API

A secure REST API implementation using Flask with local file storage, implementing OWASP security best practices.

## Features

- JWT-based authentication
- Protection against SQLi (using parameterized data storage)
- Protection against XSS (input sanitization)
- Secure password storage (scrypt hashing)
- CI/CD pipeline with security scanning

## API Endpoints

### Authentication
- `POST /auth/login` - Authenticate and get JWT token
  - Request body: `{"username": "user", "password": "pass"}`
  - Response: `{"token": "jwt.token.here"}`

- `POST /auth/register` - Register new user
  - Request body: `{"username": "newuser", "password": "newpass"}`
  - Response: `{"message": "User created successfully"}`

### Protected Endpoints (require JWT in Authorization header)
- `GET /api/data` - Get all items
  - Response: `["item1", "item2", ...]`

- `POST /api/items` - Add new item
  - Request body: `{"item": "new item"}`
  - Response: `{"message": "Item added successfully"}`

## Security Measures

1. **SQL Injection Protection**:
   - All data is stored in JSON format with proper serialization
   - No direct string concatenation in data operations

2. **XSS Protection**:
   - All user input is sanitized using `markupsafe.escape` and `bleach.clean`
   - Output is always properly escaped

3. **Authentication**:
   - JWT tokens with expiration (1 hour)
   - Secure password hashing using Werkzeug's `scrypt`
   - Middleware for protected endpoints

4. **CI/CD Security**:
   - Bandit for static code analysis
   - Safety for dependency vulnerability checking

## CI/CD Pipeline

The GitHub Actions pipeline includes:
1. Automated testing
2. Static code analysis with Bandit
3. Dependency vulnerability scanning with Safety

![CI/CD Pipeline Screenshot](screenshots/pipeline.png)
