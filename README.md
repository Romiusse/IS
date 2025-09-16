# Secure Flask REST API

## Project Description

A secure REST API implementation using Flask with local file storage, implementing OWASP security best practices.

## Features

- JWT-based authentication
- Protection against SQLi (using parameterized data storage)
- Protection against XSS (input sanitization)
- Secure password storage (scrypt hashing)
- CI/CD pipeline with security scanning

# API Documentation
## Authentication
### User Registration
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "new_user",
    "password": "SecurePass123!"
  }'
```
### Get Access Token
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "new_user",
    "password": "SecurePass123!"
  }'
```
## Data Operations (requires token)
### Get All Items
```bash
curl -X GET http://localhost:5000/api/items \
  -H "Authorization: Bearer your_jwt_token"
```
### Add New Item
```bash
curl -X POST http://localhost:5000/api/items \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_jwt_token" \
  -d '{"item": "New entry"}'
```
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

# Testing
## Run test suite:
```bash
pytest tests/
```
