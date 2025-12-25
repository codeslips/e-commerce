## ADDED Requirements

### Requirement: Demo Account Quick Login

The login page SHALL provide clickable demo account buttons for easy testing.

#### Scenario: Demo accounts displayed as clickable cards

- **WHEN** user views the login page
- **THEN** demo accounts SHALL be displayed as clickable cards
- **AND** each card SHALL show:
  - Account type/role (管理员, 经销商)
  - Username
  - Account status (for dealers)

#### Scenario: Clicking demo account fills credentials

- **WHEN** user clicks on a demo account card
- **THEN** the username field SHALL be filled with the demo username
- **AND** the password field SHALL be filled with the demo password
- **AND** user can click login to proceed

#### Scenario: Multiple demo accounts available

- **WHEN** user views the login page
- **THEN** at least 3 demo accounts SHALL be shown:
  - 1 admin account
  - 2+ dealer accounts (with different statuses)

