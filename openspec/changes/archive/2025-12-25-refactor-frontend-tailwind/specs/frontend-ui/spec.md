## MODIFIED Requirements

### Requirement: Reference Design Matching

The frontend UI SHALL use TailwindCSS for styling and match the visual design of the 欣与甜 brand reference site.

#### Scenario: Header displays correctly

- **WHEN** user views the page
- **THEN** a sticky header SHALL display with:
  - Backdrop blur effect (`backdrop-blur`)
  - Gradient logo badge (amber to orange)
  - "欣与甜" branding text
  - Semi-transparent background (`bg-white/80`)
  - Subtle bottom border

#### Scenario: Hero section displays correctly

- **WHEN** user views the home page
- **THEN** a hero section SHALL display containing:
  - Background with subtle pattern/gradient
  - Gradient accent text (amber to orange)
  - Clean sans-serif typography
  - Call-to-action buttons with slate/amber colors

#### Scenario: Footer displays correctly

- **WHEN** user views the page
- **THEN** a footer SHALL display with:
  - Clean dark or light design
  - Brand logo
  - Tagline "一路同行，共同见证梦想的力量"
  - Copyright text

#### Scenario: Color scheme applied consistently

- **WHEN** user views any page
- **THEN** the design SHALL use:
  - Slate backgrounds (`bg-slate-50`, `bg-slate-900`)
  - Amber/orange accent colors (`amber-400`, `amber-500`, `orange-500`, `orange-600`)
  - White cards with subtle shadows
  - Consistent typography colors (`text-slate-900`, `text-slate-600`)

### Requirement: Responsive Design

The frontend SHALL be responsive and work on both mobile and desktop devices using TailwindCSS responsive utilities.

#### Scenario: Mobile layout

- **WHEN** user views the page on a mobile device (width < 768px)
- **THEN** the layout SHALL adapt with:
  - Collapsible mobile navigation menu
  - Single-column layouts where appropriate
  - Touch-friendly button sizes
  - Appropriately sized text

#### Scenario: Desktop layout

- **WHEN** user views the page on a desktop device (width >= 768px)
- **THEN** the layout SHALL display with:
  - Full navigation bar
  - Multi-column grids for products and cards
  - Centered content with max-width constraints

### Requirement: Search History UI

The frontend SHALL display search history with TailwindCSS styling.

#### Scenario: History items styled as pills

- **WHEN** search history exists
- **THEN** history items SHALL display as rounded pill buttons with:
  - Tailwind rounded utilities (`rounded-full` or `rounded-xl`)
  - Hover state transitions
  - A clear button visible

## ADDED Requirements

### Requirement: TailwindCSS Integration

The frontend SHALL use TailwindCSS as the primary styling framework.

#### Scenario: TailwindCSS configured correctly

- **WHEN** the frontend builds
- **THEN** TailwindCSS SHALL be:
  - Installed via npm
  - Configured with custom brand colors in `tailwind.config.js`
  - Integrated with Vite via PostCSS
  - Available in all Vue components

#### Scenario: Custom brand colors available

- **WHEN** developers write component styles
- **THEN** custom brand colors SHALL be available:
  - Amber gradient accents
  - Orange gradient accents
  - Slate gray backgrounds and text
  - Semantic status colors (success, warning, error)

### Requirement: Design Consistency

The frontend SHALL maintain consistent visual design across all pages.

#### Scenario: Button styling consistent

- **WHEN** buttons are displayed across different pages
- **THEN** they SHALL use consistent Tailwind classes:
  - Primary: slate/dark background with white text
  - Secondary: outlined or light background
  - Accent: amber/orange for highlights
  - Consistent padding, border-radius, and hover states

#### Scenario: Form input styling consistent

- **WHEN** form inputs are displayed
- **THEN** they SHALL use consistent Tailwind classes:
  - Rounded borders (`rounded-xl`)
  - Focus ring with amber accent
  - Consistent padding and font sizes
  - Placeholder text styling

#### Scenario: Card styling consistent

- **WHEN** cards are displayed (products, orders, stats)
- **THEN** they SHALL use consistent Tailwind classes:
  - White backgrounds
  - Rounded corners (`rounded-2xl`)
  - Subtle shadows (`shadow-xl shadow-slate-200/60`)
  - Consistent padding

