# Overview

GADIApp-backend is a FastAPI web application that serves as the backend for the GADI system. The project follows a modular structure with separate directories for models, routers, and database configurations. Currently, it implements a basic health check endpoint and includes CORS middleware for cross-origin requests.

## Recent Changes (September 10, 2025)
- Created initial FastAPI backend project structure with SQLite database
- Implemented complete employee CRUD operations with Spanish error messages
- Added Spanish role-based authentication system with three mock users:
  - trabajador@example.com (Trabajador role) - read-only access
  - encargado@example.com (Encargado role) - full access to employee operations
  - admin@example.com (Administrador role) - full access to employee operations
- Protected write endpoints (POST/PATCH/DELETE) with role-based authorization
- Configured CORS middleware and health check endpoint
- Set up development workflow running on port 8000

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
- **Mock Authentication**: Demo authentication system using X-Demo-Token header
- **Role-Based Authorization**: Three roles with different access levels:
  - **Trabajador**: Read-only access to employee data
  - **Encargado**: Full CRUD access to employee operations
  - **Administrador**: Full CRUD access to employee operations
- **Protected Endpoints**: Write operations (POST/PATCH/DELETE) require Encargado or Administrador roles
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

## Authentication
- `POST /auth/login` - Login with mock credentials (password: "1234" for all users)

## Employees
- `GET /employees/` - List all employees (public)
- `POST /employees/` - Create employee (requires Encargado/Administrador)
- `GET /employees/{id}` - Get employee by ID (public)
- `PATCH /employees/{id}` - Update employee (requires Encargado/Administrador)
- `DELETE /employees/{id}` - Delete employee (requires Encargado/Administrador)

## Mock Users
- **trabajador@example.com** / **1234** (Trabajador role)
- **encargado@example.com** / **1234** (Encargado role) 
- **admin@example.com** / **1234** (Administrador role)