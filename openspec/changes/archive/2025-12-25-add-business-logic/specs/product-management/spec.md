## ADDED Requirements

### Requirement: Product Listing

The system SHALL return a paginated list of products with optional filtering.

#### Scenario: List all active products

- **WHEN** a GET request is made to `/api/products`
- **THEN** the response SHALL contain paginated active products
- **AND** each product SHALL include id, name, category, price, unit, image_url, stock

#### Scenario: Filter products by category

- **WHEN** a GET request is made to `/api/products?category=烘焙食品`
- **THEN** only products in that category SHALL be returned

#### Scenario: Search products by name

- **WHEN** a GET request is made to `/api/products?search=吐司`
- **THEN** products matching the search term SHALL be returned

### Requirement: Product Detail

The system SHALL return detailed information for a single product.

#### Scenario: Get product by ID

- **WHEN** a GET request is made to `/api/products/{id}`
- **THEN** the full product details SHALL be returned
- **AND** the response SHALL include description and min_order_quantity

#### Scenario: Product not found

- **WHEN** a GET request is made to `/api/products/{invalid_id}`
- **THEN** the response status code SHALL be 404

### Requirement: Category Listing

The system SHALL return a list of available product categories.

#### Scenario: List all categories

- **WHEN** a GET request is made to `/api/products/categories`
- **THEN** the response SHALL contain unique category names from active products

### Requirement: Product Creation (Admin)

The system SHALL allow admins to create new products.

#### Scenario: Create product with valid data

- **WHEN** an admin POSTs to `/api/products` with valid product data
- **THEN** the product SHALL be created
- **AND** the response SHALL contain the new product with generated ID

#### Scenario: Create product with missing required fields

- **WHEN** an admin POSTs to `/api/products` with missing required fields
- **THEN** the response status code SHALL be 422
- **AND** validation errors SHALL be returned

### Requirement: Product Update (Admin)

The system SHALL allow admins to update existing products.

#### Scenario: Update product successfully

- **WHEN** an admin PUTs to `/api/products/{id}` with updated data
- **THEN** the product SHALL be updated
- **AND** the updated product SHALL be returned

### Requirement: Product Deletion (Admin)

The system SHALL allow admins to soft-delete products.

#### Scenario: Delete product sets inactive

- **WHEN** an admin DELETEs `/api/products/{id}`
- **THEN** the product `is_active` SHALL be set to false
- **AND** the product SHALL no longer appear in listings

### Requirement: Product Image Upload (Admin)

The system SHALL allow admins to upload product images.

#### Scenario: Upload image successfully

- **WHEN** an admin POSTs an image file to `/api/products/{id}/image`
- **THEN** the image SHALL be saved to storage
- **AND** the product `image_url` SHALL be updated with the accessible URL

#### Scenario: Upload invalid file type

- **WHEN** an admin POSTs a non-image file to `/api/products/{id}/image`
- **THEN** the response status code SHALL be 400
- **AND** an error message SHALL indicate invalid file type

