# order-management Specification

## Purpose
TBD - created by archiving change add-business-logic. Update Purpose after archive.
## Requirements
### Requirement: Order Creation

The system SHALL allow approved dealers to create orders from their cart.

#### Scenario: Create order with valid items

- **WHEN** an approved dealer POSTs to `/api/orders` with order items
- **THEN** an order SHALL be created with status `pending`
- **AND** a unique order number SHALL be generated in format `ORD{YYYYMMDD}{NNN}`
- **AND** order items SHALL snapshot product name and unit price

#### Scenario: Create order with insufficient stock

- **WHEN** a dealer attempts to order more than available stock
- **THEN** the response status code SHALL be 400
- **AND** the error SHALL indicate which product has insufficient stock

#### Scenario: Create order with inactive product

- **WHEN** a dealer attempts to order an inactive product
- **THEN** the response status code SHALL be 400

### Requirement: Order Listing

The system SHALL return orders filtered by user role.

#### Scenario: Dealer sees only their orders

- **WHEN** a dealer GETs `/api/orders`
- **THEN** only orders belonging to that dealer SHALL be returned

#### Scenario: Admin sees all orders

- **WHEN** an admin GETs `/api/orders`
- **THEN** all orders from all dealers SHALL be returned

#### Scenario: Filter orders by status

- **WHEN** a GET request is made to `/api/orders?status=pending`
- **THEN** only orders with that status SHALL be returned

### Requirement: Order Detail

The system SHALL return detailed information for a single order.

#### Scenario: Get order with items

- **WHEN** a GET request is made to `/api/orders/{id}`
- **THEN** the order details SHALL be returned
- **AND** the response SHALL include all order items with product snapshots

#### Scenario: Dealer cannot view other dealer's order

- **WHEN** a dealer attempts to view another dealer's order
- **THEN** the response status code SHALL be 403

### Requirement: Order Status Update (Admin)

The system SHALL allow admins to update order status.

#### Scenario: Update status from pending to confirmed

- **WHEN** an admin PUTs to `/api/orders/{id}/status` with status `confirmed`
- **THEN** the order status SHALL be updated
- **AND** the `updated_at` timestamp SHALL be refreshed

#### Scenario: Valid status transitions

- **WHEN** an admin updates order status
- **THEN** only valid transitions SHALL be allowed:
  - pending → confirmed, cancelled
  - confirmed → shipped, cancelled
  - shipped → delivered
  - delivered → (no further changes)
  - cancelled → (no further changes)

### Requirement: Order Cancellation

The system SHALL allow order cancellation under specific conditions.

#### Scenario: Dealer cancels pending order

- **WHEN** a dealer DELETEs their pending order
- **THEN** the order status SHALL be set to `cancelled`

#### Scenario: Cannot cancel shipped order

- **WHEN** a dealer attempts to cancel a shipped order
- **THEN** the response status code SHALL be 400

