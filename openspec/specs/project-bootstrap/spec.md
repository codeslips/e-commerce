# project-bootstrap Specification

## Purpose
TBD - created by archiving change add-minimal-scaffold. Update Purpose after archive.
## Requirements
### Requirement: Project Startability

The system SHALL be runnable via `make up` command without errors, starting frontend, backend, and PostgreSQL containers.

#### Scenario: Docker containers start successfully

- **WHEN** a user runs `make up`
- **THEN** `xinyutian-backend`, `xinyutian-frontend`, and `xinyutian-db` containers start without errors
- **AND** frontend is accessible at `http://localhost:5500`
- **AND** backend API is accessible at `http://localhost:9111`
- **AND** PostgreSQL is accessible at `localhost:5432`

### Requirement: Health Check Endpoint

The backend SHALL provide a `/health` endpoint that returns a successful HTTP response including database connectivity status.

#### Scenario: Health check returns 200 with database status

- **WHEN** a request is made to `GET /health`
- **THEN** the response status code SHALL be 200
- **AND** the response body SHALL indicate the service is healthy
- **AND** the response body SHALL include database connection status

### Requirement: Frontend Renders

The frontend SHALL display a Vue 3 application when accessed via browser.

#### Scenario: Frontend page loads

- **WHEN** a user navigates to `http://localhost:5500`
- **THEN** a valid Vue 3 application SHALL be rendered without errors
- **AND** Vue Router SHALL handle client-side navigation

### Requirement: Makefile Commands

The project SHALL provide a Makefile with standard commands for development and operations.

#### Scenario: Make up starts all services

- **WHEN** a user runs `make up`
- **THEN** all Docker containers SHALL start in production mode

#### Scenario: Make dev starts development mode

- **WHEN** a user runs `make dev`
- **THEN** services SHALL start with hot reload enabled

#### Scenario: Make stop stops all services

- **WHEN** a user runs `make stop`
- **THEN** all Docker containers SHALL stop gracefully

#### Scenario: Make db-init initializes database

- **WHEN** a user runs `make db-init`
- **THEN** database tables SHALL be created

#### Scenario: Make db-migrate runs migrations

- **WHEN** a user runs `make db-migrate`
- **THEN** pending database migrations SHALL be applied

### Requirement: Database Connection Pool

The backend SHALL use asyncpg with connection pooling for PostgreSQL access.

#### Scenario: Database connection established on startup

- **WHEN** the backend service starts
- **THEN** a connection pool to PostgreSQL SHALL be established
- **AND** the pool SHALL be closed on shutdown

### Requirement: Environment Configuration

The backend SHALL read configuration from environment variables.

#### Scenario: Database URL from environment

- **WHEN** `DATABASE_URL` environment variable is set
- **THEN** the backend SHALL use it for database connection

#### Scenario: S3 configuration from environment

- **WHEN** AWS S3 environment variables are set (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_S3_BUCKET`, `AWS_S3_REGION`)
- **THEN** the backend SHALL use them for S3 operations

### Requirement: Database Migrations

The project SHALL support database schema migrations via Alembic.

#### Scenario: Migration files are versioned

- **WHEN** a schema change is needed
- **THEN** a new migration file SHALL be created in `migrations/versions/`

#### Scenario: Migrations can be applied

- **WHEN** `make db-migrate` is run
- **THEN** all pending migrations SHALL be applied to the database

