# Change: Refactor Frontend to TailwindCSS with Reference Design Styling

## Why

The current frontend uses custom scoped CSS with a dark blue color scheme. To improve maintainability, development speed, and achieve a more modern visual design matching the 欣与甜 brand reference site, we need to refactor the styling to use TailwindCSS with an amber/orange accent color palette on slate backgrounds.

## What Changes

### Infrastructure
- Add TailwindCSS and PostCSS to the Vue 3 + Vite frontend
- Configure `tailwind.config.js` with custom brand colors
- Update `vite.config.ts` if needed for PostCSS
- Remove custom scoped CSS and replace with Tailwind utility classes

### Design System (matching reference)
- **Color palette**: Slate backgrounds (`bg-slate-50`), amber/orange accents (`amber-400`, `orange-500`, `orange-600`)
- **Typography**: Clean sans-serif with proper weight hierarchy
- **Header**: Sticky header with backdrop-blur effect, gradient logo badge
- **Buttons**: Dark slate primary buttons (`bg-slate-900`), amber accents for highlights
- **Cards**: White cards with subtle shadows (`shadow-xl shadow-slate-200/60`)
- **Inputs**: Rounded inputs with focus rings (`ring-amber-500`)
- **Footer**: Clean dark footer with brand tagline

### Pages to Update
- `App.vue` - Global styles, footer
- `NavBar.vue` - Sticky header with backdrop-blur, logo badge
- `Home.vue` - Hero section with gradient text, feature cards
- `Login.vue` - Login form styling
- `Products.vue` - Product grid, search form, category filters
- `Orders.vue` - Order cards, status badges
- `Cart.vue` - Cart layout, summary panel
- `Profile.vue` - Profile cards
- `admin/Dashboard.vue` - Stats cards, quick links
- `admin/Products.vue` - Table styling, modal
- `admin/Orders.vue` - Table styling
- `admin/Dealers.vue` - Table styling

### Preserved Functionality
- All existing functionality remains unchanged
- No modifications to API calls, stores, or business logic
- Only visual styling is updated

## Impact

- Affected specs: `frontend-ui` (MODIFIED)
- Affected code:
  - `frontend/package.json` - Add tailwindcss, postcss, autoprefixer
  - `frontend/tailwind.config.js` - New file
  - `frontend/postcss.config.js` - New file
  - `frontend/src/main.ts` - Import Tailwind CSS
  - `frontend/src/App.vue` - Global styles
  - `frontend/src/components/NavBar.vue` - Header styling
  - `frontend/src/views/*.vue` - All view components

## Out of Scope

- Adding new features or pages
- Modifying API endpoints or data models
- Adding new components
- Changing routing or navigation logic

