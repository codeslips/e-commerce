## ADDED Requirements

### Requirement: User Login

The system SHALL authenticate users with username and password, returning JWT tokens on success.

#### Scenario: Successful login with valid credentials

- **WHEN** a POST request is made to `/api/auth/login` with valid username and password
- **THEN** the response status code SHALL be 200
- **AND** the response body SHALL contain `access_token` and `token_type`
- **AND** a refresh token SHALL be set as an httpOnly cookie

#### Scenario: Login fails with invalid credentials

- **WHEN** a POST request is made to `/api/auth/login` with invalid credentials
- **THEN** the response status code SHALL be 401
- **AND** the response body SHALL contain an error message

### Requirement: Token Refresh

The system SHALL allow refreshing access tokens using a valid refresh token.

#### Scenario: Successful token refresh

- **WHEN** a POST request is made to `/api/auth/refresh` with a valid refresh token cookie
- **THEN** a new access token SHALL be returned
- **AND** the refresh token cookie SHALL be renewed

#### Scenario: Refresh fails with expired token

- **WHEN** a POST request is made to `/api/auth/refresh` with an expired refresh token
- **THEN** the response status code SHALL be 401

### Requirement: Current User Info

The system SHALL return the current authenticated user's information.

#### Scenario: Get current user with valid token

- **WHEN** a GET request is made to `/api/auth/me` with a valid access token
- **THEN** the response SHALL contain user id, username, email, and role

#### Scenario: Unauthorized access without token

- **WHEN** a GET request is made to `/api/auth/me` without a token
- **THEN** the response status code SHALL be 401

### Requirement: User Logout

The system SHALL invalidate the user's session on logout.

#### Scenario: Successful logout

- **WHEN** a POST request is made to `/api/auth/logout`
- **THEN** the refresh token cookie SHALL be cleared
- **AND** the response status code SHALL be 200

### Requirement: Role-Based Access Control

The system SHALL enforce role-based access control for protected endpoints.

#### Scenario: Admin-only endpoint accessed by dealer

- **WHEN** a dealer attempts to access an admin-only endpoint
- **THEN** the response status code SHALL be 403

#### Scenario: Dealer must be approved to place orders

- **WHEN** a pending dealer attempts to create an order
- **THEN** the response status code SHALL be 403
- **AND** the error message SHALL indicate pending approval

