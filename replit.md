# Overview

GADIApp-backend is a FastAPI web application that serves as the backend for the GADI system. The project follows a modular structure with separate directories for models, routers, and database configurations. Currently, it implements a basic health check endpoint and includes CORS middleware for cross-origin requests.

## Recent Changes (September 10, 2025)
- Created initial FastAPI backend project structure
- Implemented health check endpoint at `/health`
- Configured CORS middleware to allow all origins (temporary for development)
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
- **SQLModel**: Chosen as the ORM for database operations, providing type safety and seamless integration with Pydantic models
- **Database Module**: Separate `db.py` file prepared for database configuration and connection management

## Configuration Management
- **Pydantic Settings**: Used for environment-based configuration management, allowing for easy deployment across different environments

## API Design
- **RESTful Architecture**: Following REST principles for API design
- **Health Check Endpoint**: Basic monitoring endpoint at `/health` for service availability checks

# External Dependencies

## Core Framework Dependencies
- **FastAPI (0.111.0)**: Web framework for building APIs
- **Uvicorn (0.30.1)**: ASGI server with standard extensions

## Data and Validation
- **SQLModel (0.0.21)**: Database ORM with Pydantic integration
- **Pydantic Settings (2.4.0)**: Configuration management through environment variables

## Development Features
- **CORS Support**: Built-in FastAPI CORS middleware for cross-origin request handling
- **Automatic Documentation**: FastAPI's built-in Swagger UI and ReDoc documentation generation

Note: The application structure suggests preparation for database integration, though no specific database engine is currently configured. The empty `db.py` and `models/__init__.py` files indicate readiness for database schema and connection setup.