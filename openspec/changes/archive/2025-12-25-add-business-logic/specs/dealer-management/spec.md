## ADDED Requirements

### Requirement: Dealer Listing (Admin)

The system SHALL allow admins to list all dealers with filtering.

#### Scenario: List all dealers

- **WHEN** an admin GETs `/api/dealers`
- **THEN** all dealers SHALL be returned with their status

#### Scenario: Filter dealers by status

- **WHEN** an admin GETs `/api/dealers?status=pending`
- **THEN** only dealers with pending status SHALL be returned

### Requirement: Dealer Detail

The system SHALL return detailed information for a single dealer.

#### Scenario: Get dealer with user info

- **WHEN** a GET request is made to `/api/dealers/{id}`
- **THEN** the dealer details SHALL be returned
- **AND** the response SHALL include associated user info (username, email)

#### Scenario: Dealer views own profile

- **WHEN** a dealer GETs `/api/dealers/me`
- **THEN** their own dealer profile SHALL be returned

### Requirement: Dealer Creation (Admin)

The system SHALL allow admins to create new dealers with associated user accounts.

#### Scenario: Create dealer with new user

- **WHEN** an admin POSTs to `/api/dealers` with dealer and user data
- **THEN** a new user account SHALL be created with role `dealer`
- **AND** a new dealer profile SHALL be created linked to the user
- **AND** the dealer status SHALL default to `pending`

#### Scenario: Create dealer with existing username

- **WHEN** an admin attempts to create a dealer with an existing username
- **THEN** the response status code SHALL be 400
- **AND** an error SHALL indicate username is taken

### Requirement: Dealer Update (Admin)

The system SHALL allow admins to update dealer information.

#### Scenario: Update dealer company info

- **WHEN** an admin PUTs to `/api/dealers/{id}` with updated data
- **THEN** the dealer info SHALL be updated

### Requirement: Dealer Status Management (Admin)

The system SHALL allow admins to approve or suspend dealers.

#### Scenario: Approve pending dealer

- **WHEN** an admin PUTs to `/api/dealers/{id}/status` with status `approved`
- **THEN** the dealer status SHALL be updated to `approved`
- **AND** the dealer can now place orders

#### Scenario: Suspend dealer

- **WHEN** an admin PUTs to `/api/dealers/{id}/status` with status `suspended`
- **THEN** the dealer status SHALL be updated to `suspended`
- **AND** the dealer SHALL not be able to place new orders

### Requirement: Dealer Order History

The system SHALL allow viewing a dealer's order history.

#### Scenario: Admin views dealer's orders

- **WHEN** an admin GETs `/api/dealers/{id}/orders`
- **THEN** all orders for that dealer SHALL be returned

