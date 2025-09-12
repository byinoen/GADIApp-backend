# Overview

GADIApp-backend is a FastAPI web application that serves as the backend for the GADI system. The project follows a modular structure with separate directories for models, routers, and database configurations. Currently, it implements a basic health check endpoint and includes CORS middleware for cross-origin requests.

## Recent Changes (September 12, 2025)
- **MAJOR**: Replaced mock authentication with complete JWT authentication system
- Implemented real user registration, login, and profile endpoints with password hashing via bcrypt
- Updated User model with password_hash, employee_id foreign key, and proper database persistence
- Created JWT token utilities (create/validate) with configurable expiration and secret key management
- Migrated all protected endpoints from mock headers to Bearer token authentication
- Maintained Spanish error messages throughout JWT implementation
- Secured admin seeding endpoints with proper authentication controls
- Implemented production-ready configuration with mandatory environment variables
- Added user-to-employee mapping via foreign keys for better data relationships

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Framework
- **FastAPI**: Modern Python web framework chosen for its automatic API documentation, type hints support, and high performance
- **Uvicorn**: ASGI server for running the FastAPI application with standard extensions for production features

## Application Structure
- **Modular Design**: Code is organized into separate packages (`models`, `routers`) for better maintainability and scalability
- **Router Pattern**: API endpoints are organized using FastAPI's router system, allowing for logical grouping of related endpoints
- **Middleware Stack**: CORS middleware is configured to allow all origins, credentials, methods, and headers for maximum flexibility during development

## Data Layer
- **SQLite Database**: Persistent SQLite database for employee data storage
- **SQLModel**: ORM for database operations with type safety and Pydantic integration
- **Database Module**: Complete database configuration with automatic table creation and session management
- **Employee Model**: Full CRUD operations with Spanish field validation and error messages

## Configuration Management
- **Pydantic Settings**: Used for environment-based configuration management, allowing for easy deployment across different environments

## API Design
- **RESTful Architecture**: Following REST principles for API design
- **Health Check Endpoint**: Basic monitoring endpoint at `/health`
- **Authentication Endpoints**: `/auth/login` for mock user authentication
- **Employee Endpoints**: Full CRUD operations at `/employees/` with role-based protection
- **Spanish Error Messages**: Consistent Spanish language error responses throughout the API

## Security Architecture
- **JWT Authentication**: Production-ready JWT token system using HS256 algorithm
- **Password Security**: bcrypt hashing for user passwords with secure verification
- **Role-Based Authorization**: Three roles with different access levels:
  - **Trabajador**: Read-only access to employee data
  - **Encargado**: Full CRUD access to employee operations  
  - **Administrador**: Full CRUD access to employee operations + user management
- **Bearer Token Authentication**: All protected endpoints use Authorization: Bearer tokens
- **Environment-Based Security**: Production defaults with mandatory SECRET_KEY configuration
- **Secure Seeding**: Admin-protected database seeding with local development bypass
- **Spanish Error Handling**: Consistent Spanish language security error messages

# External Dependencies

## Core Framework Dependencies
- **FastAPI (0.111.0)**: Web framework for building APIs
- **Uvicorn (0.30.1)**: ASGI server with standard extensions

## Data and Validation
- **SQLModel (0.0.21)**: Database ORM with Pydantic integration
- **Pydantic Settings (2.4.0)**: Configuration management through environment variables
- **SQLite**: Embedded database for persistent data storage

## Development Features
- **CORS Support**: Built-in FastAPI CORS middleware for cross-origin request handling
- **Automatic Documentation**: FastAPI's built-in Swagger UI and ReDoc documentation generation
- **Mock Authentication**: Demo system ready for JWT implementation

# API Endpoints

## Authentication Endpoints
- `POST /auth/register` - Register new user (Admin only)
- `POST /auth/login` - Login with email/password, returns JWT token
- `GET /auth/me` - Get current user profile (requires valid JWT)

## Employees
- `GET /employees/` - List all employees (requires valid JWT)
- `POST /employees/` - Create employee (requires Encargado/Administrador)
- `GET /employees/{id}` - Get employee by ID (requires valid JWT)
- `PATCH /employees/{id}` - Update employee (requires Encargado/Administrador)
- `DELETE /employees/{id}` - Delete employee (requires Encargado/Administrador)

## Admin/Seeding Endpoints
- `POST /admin/seed` - Database seeding (local development only)
- `POST /admin/seed-admin` - Admin-protected seeding (requires Administrador JWT)
- `POST /admin/bootstrap` - Production bootstrap (requires bootstrap secret)

## Real Users (seeded)
- **ana.garcia@example.com** / **1234** (Encargado role, mapped to employee)
- **luis.martinez@example.com** / **1234** (Trabajador role, mapped to employee)
- **marta.ruiz@example.com** / **1234** (Administrador role, mapped to employee)
- **admin@gadi.com** / **admin123** (Administrador role, system admin)