# Change: Enhance Demo Seed Data and Login Experience

## Why

This is a demo site for showcasing the platform. The current seed data is minimal (8 products, 3 dealers, 5 orders) and the login page shows demo credentials as plain text. To provide a better demo experience, we need more realistic data and an improved login page with clickable demo account buttons.

## What Changes

### Seed Data Enhancements
- Add `seed/users.json` for admin and user accounts
- Expand products from 8 to 15+ items across 3+ categories
- Expand dealers from 3 to 5 with varied statuses
- Expand orders from 5 to 10+ with realistic order patterns
- Move seed data folder from `data/seed/` to project root `seed/`
- Update seed script to reference new location and load users from JSON

### Login Page Improvements
- Add clickable demo account buttons that auto-fill credentials
- Display demo accounts in a visually appealing card format
- Show account role/type for each demo account

### Infrastructure
- Update `.gitignore` if needed for new seed folder location
- Remove old `data/seed/` folder after migration

## Impact

- Affected specs: `seed-data` (MODIFIED), `frontend-ui` (MODIFIED)
- Affected code: 
  - `seed/users.json`, `seed/products.json`, `seed/dealers.json`, `seed/orders.json` (new location)
  - `backend/scripts/seed_data.py` (update path, load users from JSON)
  - `frontend/src/views/Login.vue` (enhance demo accounts UI)
  - `data/seed/` (to be removed)

## Out of Scope

- Adding actual product images
- Modifying product/order data models
- Adding new demo features beyond seed data

