## 1. Backend Services Layer

- [x] 1.1 Create `app/services/storage.py` with StorageService interface and LocalStorage implementation
- [x] 1.2 Create `app/services/auth.py` with JWT token creation, validation, password hashing
- [x] 1.3 Create `app/services/user.py` with user CRUD operations
- [x] 1.4 Create `app/services/product.py` with product CRUD and category listing
- [x] 1.5 Create `app/services/order.py` with order creation, listing, status updates
- [x] 1.6 Create `app/services/dealer.py` with dealer CRUD and status management

## 2. Backend Schemas

- [x] 2.1 Create `app/schemas/auth.py` with login request/response, token schemas
- [x] 2.2 Create `app/schemas/user.py` with user create/update/response schemas
- [x] 2.3 Create `app/schemas/product.py` with product CRUD schemas
- [x] 2.4 Create `app/schemas/order.py` with order create/response schemas
- [x] 2.5 Create `app/schemas/dealer.py` with dealer CRUD schemas
- [x] 2.6 Create `app/schemas/common.py` with pagination schema

## 3. Backend Routers

- [x] 3.1 Create `app/routers/auth.py` with login, logout, refresh, me endpoints
- [x] 3.2 Create `app/routers/products.py` with CRUD and image upload endpoints
- [x] 3.3 Create `app/routers/orders.py` with order CRUD endpoints
- [x] 3.4 Create `app/routers/dealers.py` with dealer management endpoints
- [x] 3.5 Create `app/routers/files.py` for serving local uploaded files
- [x] 3.6 Update `app/main.py` to include all routers and dependencies

## 4. Seed Data

- [x] 4.1 Create `data/seed/products.json` with demo products
- [x] 4.2 Create `data/seed/dealers.json` with demo dealers
- [x] 4.3 Create `backend/scripts/seed_data.py` to populate database
- [x] 4.4 Update `Makefile` with `make seed` command

## 5. Frontend API Client

- [x] 5.1 Create `src/api/client.ts` with axios instance and auth interceptors
- [x] 5.2 Create `src/api/auth.ts` with auth API calls
- [x] 5.3 Create `src/api/products.ts` with product API calls
- [x] 5.4 Create `src/api/orders.ts` with order API calls
- [x] 5.5 Create `src/api/dealers.ts` with dealer API calls

## 6. Frontend Stores

- [x] 6.1 Create `src/stores/auth.ts` with login/logout state management
- [x] 6.2 Create `src/stores/cart.ts` with cart operations and localStorage
- [x] 6.3 Create `src/stores/product.ts` with products state and filtering

## 7. Frontend Views - Dealer Portal

- [x] 7.1 Create `src/views/Login.vue` login page
- [x] 7.2 Update `src/views/Products.vue` with real product listing and filtering
- [x] 7.3 Create `src/views/ProductDetail.vue` product detail page (integrated into Products.vue)
- [x] 7.4 Create `src/views/Cart.vue` shopping cart page
- [x] 7.5 Update `src/views/Orders.vue` with real order listing
- [x] 7.6 Create `src/views/OrderDetail.vue` order detail page (integrated into Orders.vue)
- [x] 7.7 Create `src/views/Profile.vue` dealer profile page

## 8. Frontend Views - Admin Panel

- [x] 8.1 Update `src/views/admin/Dashboard.vue` with stats and recent orders
- [x] 8.2 Create `src/views/admin/Products.vue` product management
- [x] 8.3 Create `src/views/admin/ProductForm.vue` product create/edit form (integrated into Products.vue modal)
- [x] 8.4 Create `src/views/admin/Orders.vue` order management
- [x] 8.5 Create `src/views/admin/Dealers.vue` dealer management

## 9. Frontend Router & Layout

- [x] 9.1 Update `src/router/index.ts` with all routes and guards
- [x] 9.2 Create `src/components/NavBar.vue` navigation component
- [x] 9.3 Create `src/components/Pagination.vue` reusable pagination
- [x] 9.4 Update `src/App.vue` with layout structure

## 10. Infrastructure

- [x] 10.1 Update `docker-compose.yml` to mount `/data/images` volume
- [x] 10.2 Update `backend/app/config.py` with storage configuration
- [x] 10.3 Create `/data/images/.gitkeep` placeholder

## 11. Verification

- [x] 11.1 Verify login flow works with demo admin
- [x] 11.2 Verify product CRUD in admin panel
- [x] 11.3 Verify order creation from dealer portal
- [x] 11.4 Verify seed data populates correctly
