## 1. Seed Data Folder Migration

- [x] 1.1 Create `seed/` folder in project root
- [x] 1.2 Create `seed/users.json` with admin and standalone user accounts
- [x] 1.3 Move `data/seed/products.json` to `seed/products.json` with expanded data
- [x] 1.4 Move `data/seed/dealers.json` to `seed/dealers.json` with expanded data
- [x] 1.5 Create `seed/orders.json` with pre-defined demo orders
- [x] 1.6 Update `backend/scripts/seed_data.py` to use new `seed/` location and load users
- [x] 1.7 Remove old `data/seed/` folder

## 2. Expand Seed Data Content

- [x] 2.1 Add admin user(s) in users.json (admin / admin123)
- [x] 2.2 Add more products (15+ total) across 3+ categories (烘焙食品, 零食, 饮品)
- [x] 2.3 Add more dealers (5 total) with varied statuses (3 approved, 1 pending, 1 suspended)
- [x] 2.4 Add more orders (10+ total) with varied statuses and realistic patterns

## 3. Login Page Enhancement

- [x] 3.1 Update `Login.vue` with clickable demo account cards
- [x] 3.2 Add click handler to auto-fill username/password fields
- [x] 3.3 Style demo accounts section with clear visual hierarchy

## 4. Cleanup

- [x] 4.1 Verify seed script works with new paths
- [x] 4.2 Update docker-compose volume mapping if needed
