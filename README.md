# User management API

# Features Implemented:
- [x] Users
  - [x] Create user
  - [x] Get user details, get paginated list of users
  - [x] Update user
  - [x] Delete user
# Project Structure Explanation:
```text
.
├── DockerfileLocal                # Dockerfile for local development
├── DockerfileProd                 # Dockerfile for production environment
├── README.md
├── alembic.ini                    # Alembic configuration file for database migrations
├── docker-compose-dev.yml         # Docker Compose file for development environment
├── docker-compose-prod.yml        # Docker Compose file for production environment
├── docker-compose-test.yml        # Docker Compose file for testing environment
├── init-database.sh               # Shell script to initialize the database in the docker compose
├── migrations                     # Database migration scripts generated by Alembic
├── requirements.txt               # Python dependencies
├── src                            # Main application source code
│   ├── core                       # Core functionalities like app initialization and configuration
│   │   ├── __init__.py            # Marks directory as a Python package
│   │   ├── app_factory.py         # Factory function to create Flask app
│   │   ├── database.py            # Database setup and session handling
│   │   └── settings.py            # Application settings and configurations
│   ├── dependencies               # Dependency injection and service registration
│   │   ├── __init__.py
│   │   └── user_service.py        # User service dependency injection
│   ├── exceptions                 # Custom exceptions and error handling
│   │   ├── __init__.py
│   │   └── user.py                # User-related exception handling
│   ├── extensions.py              # Flask extensions setup (e.g., Flask-RESTx)
│   ├── main.py                    # Application entry point
│   ├── models                     # Database models
│   │   ├── __init__.py
│   │   ├── base.py                # Base model for all ORM models
│   │   └── user.py                # User model definition
│   ├── repositories               # Data access layer (Repositories and Unit of Work)
│   │   ├── __init__.py
│   │   ├── base                   # Base repository definitions
│   │   │   ├── __init__.py
│   │   │   ├── abstract.py        # Abstract base class for repositories
│   │   │   └── implementation.py  # Base repository implementation
│   │   ├── unit_of_work           # Unit of Work pattern for transaction management
│   │   │   ├── __init__.py
│   │   │   ├── abstract.py        # Abstract class for Unit of Work
│   │   │   └── implementation.py  # Implementation of Unit of Work
│   │   └── user                   # User repository
│   │       ├── __init__.py
│   │       ├── abstract.py        # Abstract user repository
│   │       └── implementation.py  # Implementation of user repository
│   ├── resources                  # API routes and controllers
│   │   ├── __init__.py
│   │   ├── healthcheck.py         # API health check endpoint
│   │   └── user.py                # User API endpoints
│   ├── schemes                    # Data validation and serialization
│   │   ├── __init__.py
│   │   ├── dtos                   # Data Transfer Objects (DTOs)
│   │   │   ├── __init__.py
│   │   │   ├── pagination.py      # Pagination DTO
│   │   │   └── user.py            # User DTO
│   │   ├── request_parsers        # Parsers to render swagger UI docs
│   │   │   ├── pagination.py      # Pagination request parser
│   │   │   └── user.py            # User request parser
│   │   ├── request_validators     # Request validation classes
│   │   │   ├── __init__.py
│   │   │   ├── pagination.py      # Pagination validation
│   │   │   └── user.py            # User validation rules
│   │   └── response_parsers       # Response formatters (For swagger UI)
│   │       ├── __init__.py
│   │       ├── error.py           # Error response format
│   │       ├── pagination.py      # Pagination response format
│   │       └── user.py            # User response formatter
│   └── services                   # Business logic layer
│       ├── __init__.py
│       └── user                   # User service layer
│           ├── __init__.py
│           ├── abstract.py        # Abstract user service
│           └── implementation.py  # Implementation of user service
└── tests                          # Test suite
```
# Setup
**Note that the setup assumes you are using any Linux distribution**
### 1. Clone the project:
```shell
git clone https://github.com/GhostMEn20034/user_management_api.git
```
### 2. Change permissions for `init-database.sh`:
```shell
chmod 755 init-database.sh
```
### 3. Create a `.env` file, using the following command:
```shell
touch .env
```
### 4. Open the file created above in whatever editor you want
### 5. Insert the next variables (Don't forget to remove comments):
```shell
DB_CONNECTION_STRING=postgresql+psycopg://<SQL_USER>:<SQL_PASSWORD>@db:5432/<SQL_DATABASE>
SQL_USER=your_db_user # Needed only for DB initialization
SQL_PASSWORD=your_pwd # Needed only for DB initialization
SQL_DATABASE=your_db_name # Needed only for DB initialization
SUPER_USER_PWD=your_postgres_user_pwd # Needed only for DB initialization
```
Example to copy:
```shell
DB_CONNECTION_STRING=postgresql+psycopg://user_manager:1234abcd@db:5432/user_management
SQL_USER=user_manager
SQL_PASSWORD=1234abcd
SQL_DATABASE=user_management
SUPER_USER_PWD=5678abcd
```
# Running the App In Development Mode
### 1. Make sure you are in the root project directory and the `.env` file is populated.
### 2. Use the following command to run the app:
```shell
docker compose -f docker-compose-dev.yml up -d --build
```
### 3. Go to [localhost:5000/docs](http://localhost:5000/docs) to see interactive documentation
# Running the App In Production Mode
### 1. Make sure you are in the root project directory and the `.env` file is populated.
### 2. Use the following command to run the app:
```shell
docker compose -f docker-compose-prod.yml up -d --build
```
### 3. [localhost/](http://localhost/) is a base url
# Running integration tests
### 1. Make sure you are in the root project directory.
### 2. Create env file with the name `.env.test`:
```shell
touch .env.test
```
### 3. Open the file in any editor and paste variables:
```shell
DB_CONNECTION_STRING=postgresql+psycopg://user_manager:1234abcd@db:5432/user_management
SQL_USER=user_manager
SQL_PASSWORD=1234abcd
SQL_DATABASE=user_management
SUPER_USER_PWD=5678abcd
```
### 4. Use the following command to run integration tests:
```shell
docker compose -f docker-compose-test.yml --env-file .env.test up --build
```
### 5. After tests are completed, press `Ctrl + C` to shut down test containers
### 6. Delete Compose Project by the command:
```shell
docker compose -f docker-compose-test.yml down
```