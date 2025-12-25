# order-query Specification

## Purpose
TBD - created by archiving change complete-demo-implementation. Update Purpose after archive.
## Requirements
### Requirement: Order Search Interface

The frontend SHALL provide a search form allowing users to query orders by order ID, tracking number, recipient name, or phone number.

#### Scenario: User searches by recipient name

- **WHEN** user enters a recipient name in the search input and clicks "查一下"
- **THEN** the system SHALL send a POST request to `/api/orders/search` with the query
- **AND** display matching orders in the results area

#### Scenario: User searches by phone number

- **WHEN** user enters a phone number in the search input and clicks "查一下"
- **THEN** the system SHALL send a POST request to `/api/orders/search` with the query
- **AND** display matching orders in the results area

#### Scenario: No matching orders found

- **WHEN** user searches with a query that matches no orders
- **THEN** the system SHALL display a message indicating no results found

### Requirement: Order Result Display

The frontend SHALL display order search results with complete order and tracking information.

#### Scenario: Single order result displayed

- **WHEN** search returns one or more matching orders
- **THEN** each order SHALL display: order ID, tracking number, recipient name, product name, status, courier
- **AND** tracking history SHALL be displayed as a timeline

### Requirement: Search History

The frontend SHALL maintain a search history using localStorage, allowing users to quickly repeat previous searches.

#### Scenario: Search query saved to history

- **WHEN** user performs a search
- **THEN** the query string SHALL be saved to localStorage
- **AND** displayed in the search history section

#### Scenario: Clear search history

- **WHEN** user clicks the clear history button
- **THEN** all search history SHALL be removed from localStorage
- **AND** the history section SHALL be hidden

#### Scenario: Click history item to search

- **WHEN** user clicks a search history item
- **THEN** the query SHALL populate the search input
- **AND** the search SHALL be executed automatically

