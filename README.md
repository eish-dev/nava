# Nava - Organization Management System

## Overview
Nava is a FastAPI-based organization management system that provides secure authentication and organization management capabilities. The system supports admin users who can manage organizations and their members.

## Features
- Admin Authentication System
- Organization Management
- Role-based Access Control (Admin/Member)
- Secure Password Hashing
- JWT-based Authentication
- PostgreSQL Database Integration

## Project Structure
```
nava/
├── app/
│   ├── api/
│   │   ├── deps.py
│   │   └── endpoints/
│   │       ├── admin.py
│   │       └── organization.py
│   ├── core/
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── logging.py
│   │   └── security.py
│   ├── db/
│   │   ├── base_class.py
│   │   ├── init_db.py
│   │   ├── session.py
│   │   ├── models/
│   │   │   ├── organization.py
│   │   │   ├── organization_user.py
│   │   │   └── user.py
│   │   └── repositories/
│   │       ├── base.py
│   │       ├── organization.py
│   │       └── user.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── organization.py
│   │   └── user.py
│   ├── services/
│   │   ├── auth.py
│   │   └── organization.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   ├── base_test.py
│   ├── factories.py
│   ├── utils/
│   │   ├── generators.py
│   │   └── mocks.py
│   └── api/
│       └── endpoints/
│           └── test_admin_endpoints.py
├── requirements.txt
└── README.md
```

## Prerequisites
- Python 3.8+
- PostgreSQL
- Virtual Environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nava.git
cd nava
```

2. Create and activate virtual environment:
```bash
python -m venv nenv
source nenv/bin/activate  # On Windows: nenv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/nava"
export SECRET_KEY="your-secret-key"
```

5. Initialize the database:
```bash
python -m app.db.init_db
```

## Running the Application

Start the application using uvicorn:
```bash
uvicorn app.main:app --reload
```

The application will be available at `http://localhost:8000`

## Default Admin Account
On first startup, the system creates a default admin account:
- Email: admin@admin.com
- Password: admin

**Note:** Change these credentials in production.

## API Endpoints

### Admin Routes
- `POST /admin/login` - Admin authentication
  ```bash
  curl -X POST 'http://localhost:8000/admin/login' \
  -H 'Content-Type: application/json' \
  -d '{
      "email": "admin@admin.com",
      "password": "admin"
  }'
  ```

### Organization Routes
- `POST /organizations/` - Create new organization (requires admin access)
  ```bash
  curl -X POST 'http://localhost:8000/organizations/' \
  -H 'Authorization: Bearer your_token' \
  -H 'Content-Type: application/json' \
  -d '{
      "org_in": {
          "name": "New Organization",
          "db_connection_string": "postgresql://user:pass@localhost:5432/db"
      },
      "admin_in": {
          "email": "org.admin@example.com",
          "password": "strongpassword",
          "full_name": "Org Admin"
      }
  }'
  ```

## Testing

Run tests using pytest:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/api/endpoints/test_admin_endpoints.py
```

## Project Components

### Core Components
- **Security**: JWT-based authentication, password hashing
- **Config**: Application configuration management
- **Constants**: System-wide enums and constants
- **Logging**: Centralized logging configuration

### Database
- **Models**: SQLAlchemy ORM models
- **Repositories**: Database access layer
- **Session**: Database connection management

### API
- **Dependencies**: FastAPI dependency injection
- **Endpoints**: API route handlers
- **Schemas**: Pydantic models for request/response validation

### Services
- **Auth Service**: Authentication and authorization logic
- **Organization Service**: Organization management logic

## Development

### Adding New Features
1. Create/update models in `app/db/models/`
2. Create/update schemas in `app/schemas/`
3. Implement repository methods in `app/db/repositories/`
4. Add business logic in `app/services/`
5. Create endpoints in `app/api/endpoints/`
6. Add tests in `tests/`

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-cov factory-boy

# Run tests
pytest
```

## Security Considerations
- Change default admin credentials
- Use strong passwords
- Secure database connection strings
- Implement rate limiting
- Regular security audits

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[Your License Here]
