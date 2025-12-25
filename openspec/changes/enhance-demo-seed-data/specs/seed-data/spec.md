## MODIFIED Requirements

### Requirement: Seed Data Location

The seed data files SHALL be located in the project root `seed/` folder.

#### Scenario: Seed data files in root folder

- **WHEN** the project is set up
- **THEN** seed data files SHALL be located at:
  - `seed/users.json`
  - `seed/products.json`
  - `seed/dealers.json`
  - `seed/orders.json`
- **AND** the old `data/seed/` location SHALL NOT be used

### Requirement: Admin User Seed

The system SHALL create admin users from a JSON file.

#### Scenario: Admin users loaded from seed file

- **WHEN** seed data is run
- **THEN** admin users SHALL be loaded from `seed/users.json`
- **AND** the default admin account SHALL be:
  - Username: `admin`
  - Password: `admin123`
  - Role: `admin`

### Requirement: Demo Products Seed

The system SHALL create demo products across categories.

#### Scenario: Products created with categories

- **WHEN** seed data is run
- **THEN** at least 15 demo products SHALL be created
- **AND** products SHALL span at least 3 categories (烘焙食品, 零食, 饮品)
- **AND** products SHALL have realistic Chinese names and prices

### Requirement: Demo Dealers Seed

The system SHALL create demo dealer accounts.

#### Scenario: Dealers created with various statuses

- **WHEN** seed data is run
- **THEN** at least 5 demo dealers SHALL be created
- **AND** at least 3 dealers SHALL have status `approved`
- **AND** at least 1 dealer SHALL have status `pending`
- **AND** at least 1 dealer SHALL have status `suspended`

### Requirement: Demo Orders Seed

The system SHALL create demo orders for testing.

#### Scenario: Orders created with various statuses

- **WHEN** seed data is run
- **THEN** at least 10 demo orders SHALL be created
- **AND** orders SHALL have various statuses (pending, confirmed, shipped, delivered, cancelled)
- **AND** orders SHALL be associated with approved dealers
- **AND** orders SHALL have realistic order amounts and item quantities

## ADDED Requirements

### Requirement: Pre-defined Orders File

The system SHALL load orders from a JSON file instead of generating them dynamically.

#### Scenario: Orders loaded from seed file

- **WHEN** seed data is run
- **THEN** orders SHALL be loaded from `seed/orders.json`
- **AND** order items SHALL reference existing products

### Requirement: Users Seed File

The system SHALL create users from a dedicated JSON file.

#### Scenario: Users loaded from seed file

- **WHEN** seed data is run
- **THEN** users SHALL be loaded from `seed/users.json`
- **AND** users SHALL include admin accounts separate from dealer accounts

