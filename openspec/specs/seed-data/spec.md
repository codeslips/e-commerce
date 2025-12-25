# seed-data Specification

## Purpose
TBD - created by archiving change add-business-logic. Update Purpose after archive.
## Requirements
### Requirement: Seed Data Command

The project SHALL provide a command to populate the database with demo data.

#### Scenario: Run seed data command

- **WHEN** `make seed` is executed
- **THEN** demo users, dealers, products, and orders SHALL be inserted
- **AND** existing seed data SHALL be updated if already present (upsert)

### Requirement: Admin User Seed

The system SHALL create a default admin user for initial access.

#### Scenario: Admin user created

- **WHEN** seed data is run
- **THEN** an admin user SHALL be created with:
  - Username: `admin`
  - Password: `admin123`
  - Role: `admin`

### Requirement: Demo Dealers Seed

The system SHALL create demo dealer accounts.

#### Scenario: Dealers created with various statuses

- **WHEN** seed data is run
- **THEN** at least 3 demo dealers SHALL be created
- **AND** at least one dealer SHALL have status `approved`
- **AND** at least one dealer SHALL have status `pending`

### Requirement: Demo Products Seed

The system SHALL create demo products across categories.

#### Scenario: Products created with categories

- **WHEN** seed data is run
- **THEN** at least 8 demo products SHALL be created
- **AND** products SHALL span at least 2 categories
- **AND** products SHALL have realistic Chinese names and prices

### Requirement: Demo Orders Seed

The system SHALL create demo orders for testing.

#### Scenario: Orders created with various statuses

- **WHEN** seed data is run
- **THEN** at least 5 demo orders SHALL be created
- **AND** orders SHALL have various statuses (pending, confirmed, shipped, delivered)
- **AND** orders SHALL be associated with approved dealers

### Requirement: Seed Data Idempotency

The seed data script SHALL be idempotent.

#### Scenario: Running seed multiple times

- **WHEN** `make seed` is run multiple times
- **THEN** no duplicate data SHALL be created
- **AND** existing data SHALL be preserved or updated

