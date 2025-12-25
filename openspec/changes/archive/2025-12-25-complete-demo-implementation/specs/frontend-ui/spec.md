## ADDED Requirements

### Requirement: Reference Design Matching

The frontend UI SHALL match the visual design of the reference site (欣与甜订单自助快递查询官网).

#### Scenario: Header displays correctly

- **WHEN** user views the page
- **THEN** a dark header SHALL display with logo and "欣与甜" branding

#### Scenario: Hero section displays correctly

- **WHEN** user views the page
- **THEN** a blue gradient hero section SHALL display containing:
  - Circular logo image
  - "欣与甜" title text
  - Search input with green "查一下" button
  - Public announcement text

#### Scenario: Footer displays correctly

- **WHEN** user views the page
- **THEN** a fixed dark footer SHALL display with tagline "一路同行，共同见证梦想的力量"

### Requirement: Responsive Design

The frontend SHALL be responsive and work on both mobile and desktop devices.

#### Scenario: Mobile layout

- **WHEN** user views the page on a mobile device (width < 768px)
- **THEN** the layout SHALL adapt with:
  - Single-column search form
  - 2-column product category grid
  - Appropriately sized text and buttons

#### Scenario: Desktop layout

- **WHEN** user views the page on a desktop device (width >= 768px)
- **THEN** the layout SHALL display with:
  - Inline search form (input + button on same row)
  - 2-column product category grid
  - Centered content with max-width constraint

### Requirement: Search History UI

The frontend SHALL display search history with styling matching the reference design.

#### Scenario: History items styled as pills

- **WHEN** search history exists
- **THEN** history items SHALL display as rounded pill buttons
- **AND** a clear button SHALL be visible

