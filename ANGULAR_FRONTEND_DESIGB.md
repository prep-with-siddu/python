# SaaSIQ — Complete Angular Tech Stack Guide
## End-to-End Requirements for Production UI (Matching Prototype 1:1)

> **Generated**: 7 March 2026  
> **Prototype Reference**: `design/prototype/` (4,464 lines HTML · 2,871 lines CSS · 1,358 lines JS)  
> **Target**: Pixel-perfect Angular rebuild with production-grade architecture

---

## Table of Contents

1. [Core Framework & Build](#1-core-framework--build)
2. [CSS / Styling](#2-css--styling)
3. [Charts & Data Visualization](#3-charts--data-visualization)
4. [State Management](#4-state-management)
5. [Routing & Navigation](#5-routing--navigation)
6. [UI Components to Build](#6-ui-components-to-build)
7. [Essential Libraries (package.json)](#7-essential-libraries)
8. [Testing Strategy](#8-testing-strategy)
9. [Developer Tooling](#9-developer-tooling)
10. [Feature Implementation Notes](#10-feature-implementation-notes)
11. [Project Structure](#11-project-structure)
12. [Quick Start Commands](#12-quick-start-commands)
13. [Summary Table](#13-summary-table)

---

## 1. Core Framework & Build

| Purpose | Recommendation | Why |
|---------|---------------|-----|
| **Framework** | **Angular 19** (standalone components) | Latest stable, signal-based reactivity, SSR-ready |
| **Bundler** | **esbuild** (Angular CLI default since v17) | 3-4x faster than webpack, zero config needed |
| **Language** | **TypeScript 5.6+** | Angular requires it, strong typing for 15+ dashboard sections |
| **Package Manager** | **pnpm** | Faster installs, disk-efficient, strict dependency resolution |
| **Runtime** | **Node.js 20 LTS** | Required for Angular CLI & SSR |

### Bootstrap Command
```bash
ng new saasiq --style=scss --routing --standalone --ssr=false
```

---

## 2. CSS / Styling

### Framework: Tailwind CSS 4

| Purpose | Choice | Why |
|---------|--------|-----|
| **CSS Framework** | **Tailwind CSS 4** | Matches prototype's utility-based patterns (grids, flex, spacing, colors). Prototype has 2,871 lines of CSS — Tailwind eliminates ~80% |
| **Preprocessor** | **SCSS** (Angular CLI default) | For design tokens (`:root` vars), mixins for theme switching, nesting |
| **Component Primitives** | **Angular CDK** (no Material) | Headless primitives: overlay (modals), a11y (focus trap), drag-drop, portal — zero visual opinions |
| **Icons** | **Font Awesome 6** (`@fortawesome/angular-fontawesome`) | Prototype already uses FA 6.4 everywhere |
| **Typography** | **Inter** (`@fontsource/inter`, self-hosted) | Exact match to prototype, avoids FOIT with self-hosting |
| **Animations** | **@angular/animations** | For fade-in cards, modal transitions, toast slide-in, pulse-critical keyframes |

### Design Token Strategy (Tailwind Config)

```typescript
// tailwind.config.ts
export default {
  darkMode: 'class', // matches prototype's body.theme-dark approach
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#7C3AED',
          light: '#A78BFA',
          dark: '#5B21B6',
          bg: '#F5F3FF',
        },
        green: {
          DEFAULT: '#10B981',
          light: '#D1FAE5',
        },
        blue: {
          DEFAULT: '#3B82F6',
          light: '#DBEAFE',
        },
        orange: {
          DEFAULT: '#F59E0B',
          light: '#FEF3C7',
        },
        red: {
          DEFAULT: '#EF4444',
          light: '#FEE2E2',
        },
        teal: {
          DEFAULT: '#14B8A6',
        },
        gray: {
          50: '#F9FAFB',
          100: '#F3F4F6',
          200: '#E5E7EB',
          300: '#D1D5DB',
          400: '#9CA3AF',
          500: '#6B7280',
          600: '#4B5563',
          700: '#374151',
          800: '#1F2937',
          900: '#111827',
        },
      },
      borderRadius: {
        xs: '6px',
        sm: '8px',
        DEFAULT: '12px',
      },
      boxShadow: {
        DEFAULT: '0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06)',
        md: '0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.06)',
        lg: '0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05)',
        xl: '0 20px 25px rgba(0,0,0,0.1), 0 10px 10px rgba(0,0,0,0.04)',
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
      },
      spacing: {
        'sidebar': '260px',
        'sidebar-collapsed': '68px',
        'topbar': '64px',
      },
    },
  },
};
```

### Dark Theme

Use Tailwind's `dark:` variant with `class` strategy — matches prototype's `body.theme-dark` approach. Override CSS custom properties for the accent color live-switching:

```scss
// _dark-theme.scss
.theme-dark {
  --gray-50: #111827;
  --gray-100: #1F2937;
  --gray-200: #374151;
  --gray-300: #4B5563;
  --gray-400: #6B7280;
  --gray-500: #9CA3AF;
  --gray-600: #D1D5DB;
  --gray-700: #E5E7EB;
  --gray-800: #F3F4F6;
  --gray-900: #F9FAFB;
  --green-light: #064E3B;
  --blue-light: #1E3A5F;
  --orange-light: #78350F;
  --red-light: #7F1D1D;
}
```

---

## 3. Charts & Data Visualization

### Prototype Chart Inventory (7 types found)

| Chart in Prototype | Type | Location |
|-------------------|------|----------|
| Spend over time | Line/Area chart | Dashboard Home, Spend Intelligence |
| Category breakdown | Donut chart (SVG circles) | Dashboard Home, Spend Intelligence |
| Mock dashboard bars | Vertical bar chart (animated) | Landing hero, Demo walkthrough |
| Usage/Department/Compliance bars | Horizontal progress bars | Usage, Dept Costs, Compliance |
| Compliance score gauge | Circular SVG gauge | Compliance, Demo step 5 |
| KPI sparklines | Mini inline charts | KPI cards |
| Department spend comparison | Grouped/stacked bars | Spend Intelligence, Dept Costs |

### Recommendation: Apache ECharts via `ngx-echarts`

**Why ECharts over alternatives (ngx-charts, Chart.js, D3):**

| Criteria | ECharts | ngx-charts | Chart.js | D3 |
|----------|---------|------------|----------|----|
| Animated bar grow-up | ✅ built-in | ✅ | ✅ | Manual |
| Gradient fills | ✅ native | ❌ | Limited | Manual |
| Donut center labels | ✅ native | ✅ | Plugin | Manual |
| Dark mode theme swap | ✅ single prop | Manual | Manual | Manual |
| Density mode resize | ✅ responsive | Limited | ✅ | Manual |
| Angular integration | ✅ ngx-echarts | ✅ native | wrapper | Manual |
| Chart count (future) | 50+ types | ~15 types | ~8 types | Unlimited |
| Bundle size | ~300KB (tree-shakeable) | ~150KB | ~60KB | ~240KB |

```bash
pnpm add echarts ngx-echarts
```

### What does NOT need a chart library (pure CSS):

These are simple `div` width transitions — build as Angular components:

- Department spend bars (`.dept-bar`)
- Usage bars (`.usage-bar-fill`)
- Framework compliance bars (`.framework-fill`)
- Mini progress bars (`.mini-progress-bar`)
- Utilization bars (`.util-fill`)
- Leader board bars (`.leader-fill`)
- Department utilization bars (`.dept-util-fill`)

### SVG Gauge (hand-built component):

The re-scan progress ring and compliance gauge use `stroke-dashoffset` animation on `<svg><circle>`. Build as a standalone Angular component — no library needed:

```typescript
@Component({
  selector: 'app-svg-gauge',
  template: `
    <svg [attr.width]="size" [attr.height]="size" viewBox="0 0 100 100">
      <circle cx="50" cy="50" r="42" fill="none" stroke="#F3F4F6" stroke-width="8"/>
      <circle cx="50" cy="50" r="42" fill="none" 
        [attr.stroke]="color" stroke-width="8" stroke-linecap="round"
        [attr.stroke-dasharray]="circumference"
        [attr.stroke-dashoffset]="dashOffset"
        transform="rotate(-90 50 50)"
        style="transition: stroke-dashoffset 1s ease"/>
    </svg>
  `
})
export class SvgGaugeComponent { /* ... */ }
```

---

## 4. State Management

| Purpose | Recommendation | Why |
|---------|---------------|-----|
| **Global State** | **NgRx SignalStore** (`@ngrx/signals`) | Lightweight, signal-native. For: theme state, org context, sidebar collapse, user profile |
| **Server State** | **TanStack Query** (`@tanstack/angular-query-experimental`) | Caching, background refetch, optimistic updates for API data (apps, spend, alerts) |
| **Local UI State** | **Angular Signals** (built-in) | For: modal open/close, filter states, active tabs, toast queue |

### Store Examples

```typescript
// stores/appearance.store.ts — Theme, Accent, Density (persisted to localStorage)
import { signalStore, withState, withMethods, patchState } from '@ngrx/signals';

type AppearanceState = {
  theme: 'light' | 'dark' | 'system';
  accent: string;
  accentLight: string;
  accentDark: string;
  density: 'comfortable' | 'default' | 'compact';
};

const initialState: AppearanceState = {
  theme: (localStorage.getItem('saasiq-theme') as any) || 'light',
  accent: localStorage.getItem('saasiq-accent') || '#7C3AED',
  accentLight: localStorage.getItem('saasiq-accent-light') || '#F5F3FF',
  accentDark: localStorage.getItem('saasiq-accent-dark') || '#5B21B6',
  density: (localStorage.getItem('saasiq-density') as any) || 'default',
};

export const AppearanceStore = signalStore(
  { providedIn: 'root' },
  withState(initialState),
  withMethods((store) => ({
    setTheme(theme: AppearanceState['theme']) {
      patchState(store, { theme });
      localStorage.setItem('saasiq-theme', theme);
      document.body.classList.remove('theme-light', 'theme-dark');
      document.body.classList.add(`theme-${theme === 'system' ? (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light') : theme}`);
    },
    setAccent(accent: string, light: string, dark: string) {
      patchState(store, { accent, accentLight: light, accentDark: dark });
      document.documentElement.style.setProperty('--primary', accent);
      document.documentElement.style.setProperty('--primary-light', light);
      document.documentElement.style.setProperty('--primary-dark', dark);
    },
    setDensity(density: AppearanceState['density']) {
      patchState(store, { density });
      document.documentElement.classList.remove('density-comfortable', 'density-default', 'density-compact');
      document.documentElement.classList.add(`density-${density}`);
    },
    reset() {
      /* Reset to defaults and clear localStorage */
    },
  }))
);
```

```typescript
// stores/org.store.ts — Organization context switching
export const OrgStore = signalStore(
  { providedIn: 'root' },
  withState({
    currentOrg: { id: '1', name: 'TechCorp India', plan: 'Business', users: 25 },
    orgs: [
      { id: '1', name: 'TechCorp India', plan: 'Business', users: 25 },
      { id: '2', name: 'TechCorp Global', plan: 'Enterprise', users: 120 },
      { id: '3', name: 'TechCorp Sandbox', plan: 'Free Trial', users: 5 },
    ],
  }),
  withMethods(/* switchOrg, addOrg */)
);
```

---

## 5. Routing & Navigation

### Route Configuration

```typescript
// app.routes.ts
export const routes: Routes = [
  { path: '', loadComponent: () => import('./features/landing/landing.component') },
  { path: 'login', loadComponent: () => import('./features/auth/login/login.component') },
  { path: 'signup', loadComponent: () => import('./features/auth/signup/signup.component') },
  { path: 'onboarding', loadComponent: () => import('./features/onboarding/onboarding.component') },
  { path: 'demo', loadComponent: () => import('./features/demo/demo.component') },
  {
    path: 'dashboard',
    loadComponent: () => import('./layout/app-shell/app-shell.component'),
    canActivate: [authGuard],
    children: [
      { path: '', redirectTo: 'home', pathMatch: 'full' },
      { path: 'home', loadComponent: () => import('./features/dashboard/home/home.component') },
      { path: 'discovery', loadComponent: () => import('./features/dashboard/discovery/discovery.component') },
      { path: 'spend', loadComponent: () => import('./features/dashboard/spend/spend.component') },
      { path: 'usage', loadComponent: () => import('./features/dashboard/usage/usage.component') },
      { path: 'compliance', loadComponent: () => import('./features/dashboard/compliance/compliance.component') },
      { path: 'contracts', loadComponent: () => import('./features/dashboard/contracts/contracts.component') },
      { path: 'policies', loadComponent: () => import('./features/dashboard/policies/policies.component') },
      { path: 'ai-insights', loadComponent: () => import('./features/dashboard/ai-insights/ai-insights.component') },
      { path: 'ai-copilot', loadComponent: () => import('./features/dashboard/ai-copilot/ai-copilot.component') },
      { path: 'offboarding', loadComponent: () => import('./features/dashboard/offboarding/offboarding.component') },
      { path: 'renewals', loadComponent: () => import('./features/dashboard/renewals/renewals.component') },
      { path: 'benchmarks', loadComponent: () => import('./features/dashboard/benchmarks/benchmarks.component') },
      { path: 'dept-costs', loadComponent: () => import('./features/dashboard/dept-costs/dept-costs.component') },
      { path: 'alerts', loadComponent: () => import('./features/dashboard/alerts/alerts.component') },
      {
        path: 'settings',
        loadComponent: () => import('./features/dashboard/settings/settings.component'),
        children: [
          { path: '', redirectTo: 'general', pathMatch: 'full' },
          { path: 'general', loadComponent: () => import('./features/dashboard/settings/general/general.component') },
          { path: 'integrations', loadComponent: () => import('./features/dashboard/settings/integrations/integrations.component') },
          { path: 'team', loadComponent: () => import('./features/dashboard/settings/team/team.component') },
          { path: 'notifications', loadComponent: () => import('./features/dashboard/settings/notifications/notifications.component') },
          { path: 'security', loadComponent: () => import('./features/dashboard/settings/security/security.component') },
          { path: 'appearance', loadComponent: () => import('./features/dashboard/settings/appearance/appearance.component') },
          { path: 'api-webhooks', loadComponent: () => import('./features/dashboard/settings/api-webhooks/api-webhooks.component') },
          { path: 'billing', loadComponent: () => import('./features/dashboard/settings/billing/billing.component') },
        ],
      },
    ],
  },
  { path: '**', redirectTo: '' },
];
```

---

## 6. UI Components to Build

### Layout Components (4)

| Component | Prototype Selector | Notes |
|-----------|-------------------|-------|
| `AppShellComponent` | `.app-shell` | Sidebar + main content wrapper, handles sidebar collapse |
| `SidebarComponent` | `.sidebar` | Collapsible, org dropdown, nav sections, user dropdown, mobile slide-in |
| `TopbarComponent` | `.topbar` | Search bar, notification bell, user avatar |
| `PageNavigatorComponent` | `.page-navigator` | Floating FAB with quick-jump panel |

### Shared UI Components (18)

| Component | Prototype Selector | Variants |
|-----------|-------------------|----------|
| `KpiCardComponent` | `.kpi-card` | With icon, value, change indicator, mini-progress, highlight border |
| `ChartCardComponent` | `.chart-card` | Header with legend, body wrapper, full-width option |
| `DataTableComponent` | `.data-table` | Sortable headers, hoverable rows, shadow-row variant |
| `FilterGroupComponent` | `.filter-group` | Active toggle buttons with counts |
| `ModalComponent` | `.modal-overlay` + `.modal-dialog` | Header, body, footer slots; ESC close; backdrop click |
| `ToastComponent` + `ToastService` | `.toast-container` + `.toast` | 4 types: success/danger/info/warning; auto-dismiss 4s |
| `BadgeComponent` | `.status-badge`, `.risk-badge`, `.nav-badge`, `.days-badge`, `.role-badge` | Color variants: red/green/orange/blue/purple/yellow |
| `AvatarComponent` | `.avatar`, `.avatar-sm`, `.avatar-xs` | Sizes: 44px, 32px, 28px; initials or image |
| `ButtonComponent` | `.btn` | Variants: primary/outline/danger/icon; Sizes: lg/default/sm/full |
| `ToggleSwitchComponent` | `.toggle-switch` | Checked state with accent color |
| `ProgressBarComponent` | `.mini-progress`, `.util-bar`, `.framework-bar` | Color variants: green/orange/red; animated width |
| `DaysCircleComponent` | `.days-circle` | States: critical (pulsing)/urgent/warning/safe |
| `AppIconComponent` | `.app-icon` | Predefined colors: SF(blue)/GH(dark)/SL(purple)/Jira(blue)/AWS(orange)/Figma(red) |
| `DropdownComponent` | `.org-dropdown`, `.user-dropdown` | Click-outside close, backdrop for mobile |
| `SearchBarComponent` | `.search-bar` | With keyboard shortcut hint (⌘K) |
| `PageHeaderComponent` | `.page-header` | Title, subtitle, action buttons slot |
| `SvgGaugeComponent` | `.rescan-progress-ring`, demo gauge | Animated stroke-dashoffset circle |
| `TypingIndicatorComponent` | `.typing-indicator` | 3 bouncing dots animation |

### Feature Components (20)

| Component | Sections/Features |
|-----------|------------------|
| `LandingComponent` | Hero + stats, mock dashboard preview, trust logos, problems section (7 cards), customer needs (12 cards), features grid (12 cards), pricing (3 tiers), footer |
| `LoginComponent` | Split layout, social auth buttons, email form, testimonial sidebar |
| `SignupComponent` | Split layout, social auth, registration form, benefits sidebar |
| `OnboardingComponent` | 4-step wizard: SSO connect → Integrations → Team invite → Preferences |
| `DemoComponent` | 6-step auto-playing walkthrough with play/pause, dot nav, progress bar, timer |
| `DashboardHomeComponent` | 4 KPI cards, chart row (trend + donut), action list, renewal list |
| `DiscoveryComponent` | 5 stat cards, filter dropdowns + search, app cards grid (3-col), data table |
| `SpendComponent` | Trend chart, donut chart, department bars, anomaly list |
| `UsageComponent` | Usage bars, department usage grid (3-col cards), leaderboard |
| `ComplianceComponent` | Framework progress bars, risk app list, risk score badges |
| `ContractsComponent` | Timeline grouped by month, renewal filter bar, days-circle indicators, AI tips |
| `PoliciesComponent` | Policy cards with active status, meta info |
| `AiInsightsComponent` | 2-col grid of insight cards (savings/security/prediction/negotiation) |
| `AiCopilotComponent` | Chat container, user/AI message bubbles, typing indicator, suggestion chips, input bar |
| `OffboardingComponent` | 4 stat cards, bulk action banner, pending offboards table, completed table, HR sync, offboard wizard modal |
| `RenewalsComponent` | 4 summary cards, filter bar, contract timeline with days-circle |
| `BenchmarksComponent` | 4 overview cards, comparison data |
| `DeptCostsComponent` | Total spend card, department grid cards with bar fills |
| `AlertsComponent` | Filter tabs, alert list with severity icons, snooze modal, mark-all-read |
| `SettingsComponent` | Tab sidebar (8 tabs): General, Integrations, Team, Notifications, Security, Appearance, API & Webhooks, Billing |

### Settings Sub-Components (8)

| Tab | Key Elements |
|-----|-------------|
| **General** | Company info form, fiscal year, currency |
| **Integrations** | Integration cards (connected/disconnected), connect/disconnect buttons |
| **Team** | Team table (avatar, name, role badge, status pill, actions), invite modal |
| **Notifications** | Notification options with toggle switches |
| **Security** | Security cards with dropdowns (session timeout, 2FA), audit log |
| **Appearance** | Theme cards (light/dark/system), color dots (6 accents), density radio options, preview bar |
| **API & Webhooks** | API key list, generate key modal, key display modal, webhook list, docs link |
| **Billing** | Plan card, payment method, invoice list, usage bar |

---

## 7. Essential Libraries

### package.json Dependencies

```json
{
  "dependencies": {
    "@angular/core": "^19.x",
    "@angular/common": "^19.x",
    "@angular/router": "^19.x",
    "@angular/forms": "^19.x",
    "@angular/animations": "^19.x",
    "@angular/cdk": "^19.x",
    "@angular/platform-browser": "^19.x",

    "@fortawesome/angular-fontawesome": "^0.15.x",
    "@fortawesome/fontawesome-svg-core": "^6.x",
    "@fortawesome/free-solid-svg-icons": "^6.x",
    "@fortawesome/free-brands-svg-icons": "^6.x",

    "@fontsource/inter": "^5.x",

    "@ngrx/signals": "^19.x",
    "@tanstack/angular-query-experimental": "^5.x",

    "echarts": "^5.6.x",
    "ngx-echarts": "^19.x",

    "tailwindcss": "^4.x",

    "rxjs": "^7.8.x",
    "zone.js": "~0.15.x",
    "tslib": "^2.x"
  },
  "devDependencies": {
    "@angular/cli": "^19.x",
    "@angular/compiler-cli": "^19.x",
    "@angular-devkit/build-angular": "^19.x",

    "typescript": "~5.6.x",
    "@types/node": "^20.x",

    "@tailwindcss/postcss": "^4.x",
    "postcss": "^8.x",

    "jest": "^29.x",
    "jest-preset-angular": "^14.x",
    "@testing-library/angular": "^17.x",

    "@playwright/test": "^1.49.x",

    "eslint": "^9.x",
    "angular-eslint": "^19.x",
    "prettier": "^3.x",
    "prettier-plugin-tailwindcss": "^0.6.x",

    "husky": "^9.x",
    "lint-staged": "^15.x",

    "storybook": "^8.x",
    "@storybook/angular": "^8.x"
  }
}
```

### Install Command

```bash
# Create project
ng new saasiq --style=scss --routing --standalone --ssr=false --package-manager=pnpm

cd saasiq

# Core UI
pnpm add @angular/cdk @angular/animations

# Icons
pnpm add @fortawesome/angular-fontawesome @fortawesome/fontawesome-svg-core @fortawesome/free-solid-svg-icons @fortawesome/free-brands-svg-icons

# Fonts
pnpm add @fontsource/inter

# State Management
pnpm add @ngrx/signals @tanstack/angular-query-experimental

# Charts
pnpm add echarts ngx-echarts

# CSS
pnpm add -D tailwindcss @tailwindcss/postcss postcss

# Testing
pnpm add -D jest jest-preset-angular @testing-library/angular @playwright/test

# Dev Tools
pnpm add -D eslint angular-eslint prettier prettier-plugin-tailwindcss husky lint-staged

# Storybook
npx storybook@latest init --type angular
```

---

## 8. Testing Strategy

| Layer | Tool | What to Test |
|-------|------|-------------|
| **Unit Tests** | **Jest** + `jest-preset-angular` | Services (ThemeService, ToastService), stores (AppearanceStore, OrgStore), pipes, pure utility functions |
| **Component Tests** | **Angular Testing Library** (`@testing-library/angular`) | Component rendering, user interactions (click, type), state changes |
| **E2E Tests** | **Playwright** | Full user flows: Landing → Signup → Onboarding → Dashboard navigation → Settings → Logout |
| **Visual Regression** | **Playwright screenshots** or **Chromatic** (via Storybook) | Catch CSS regressions across all 3 themes × 3 densities × 6 accent colors |
| **Component Docs** | **Storybook 8** | Document all 18+ shared components with variant stories |

### Key E2E Test Flows

```typescript
// tests/e2e/flows.spec.ts
test('Complete onboarding flow', async ({ page }) => {
  await page.goto('/signup');
  await page.fill('[name="email"]', 'test@company.com');
  // ... fill form
  await page.click('text=Create Account');
  await expect(page).toHaveURL('/onboarding');
  // Step 1: Connect SSO
  await page.click('text=Google Workspace');
  await page.click('text=Continue');
  // Step 2-4...
  await page.click('text=Launch Dashboard');
  await expect(page).toHaveURL('/dashboard/home');
});

test('Theme switching persists across reload', async ({ page }) => {
  await page.goto('/dashboard/settings/appearance');
  await page.click('[data-theme="dark"]');
  await page.click('text=Apply');
  await page.reload();
  await expect(page.locator('body')).toHaveClass(/theme-dark/);
});

test('Sidebar collapse on desktop', async ({ page }) => {
  await page.goto('/dashboard/home');
  await page.keyboard.press('Meta+b');
  await expect(page.locator('.sidebar')).toHaveClass(/collapsed/);
});
```

---

## 9. Developer Tooling

| Tool | Purpose | Config |
|------|---------|--------|
| **ESLint 9** + angular-eslint | TypeScript & template linting | `eslint.config.mjs` |
| **Prettier 3** + tailwindcss plugin | Code formatting + class sorting | `.prettierrc` |
| **Husky 9** | Git hooks | `.husky/pre-commit` |
| **lint-staged** | Run linters on staged files only | `.lintstagedrc` |
| **Storybook 8** | Component development & docs | `.storybook/` |
| **Angular DevTools** | Chrome extension for debugging | Browser extension |
| **VS Code Extensions** | Angular Language Service, Tailwind IntelliSense, ESLint, Prettier | `.vscode/extensions.json` |

### Recommended VS Code Extensions

```json
// .vscode/extensions.json
{
  "recommendations": [
    "angular.ng-template",
    "bradlc.vscode-tailwindcss",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "nrwl.angular-console",
    "ms-playwright.playwright"
  ]
}
```

---

## 10. Feature Implementation Notes

### 10.1 Theme Engine

Matches prototype's `applyThemeToDOM()` / `body.theme-dark` approach:

```typescript
// core/services/theme.service.ts
@Injectable({ providedIn: 'root' })
export class ThemeService {
  private store = inject(AppearanceStore);

  applyTheme(theme: 'light' | 'dark' | 'system') {
    const effective = theme === 'system'
      ? (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
      : theme;
    document.documentElement.setAttribute('data-theme', effective);
    document.body.classList.remove('theme-light', 'theme-dark');
    document.body.classList.add(`theme-${effective}`);
  }

  applyAccent(color: string, light: string, dark: string) {
    const root = document.documentElement.style;
    root.setProperty('--primary', color);
    root.setProperty('--primary-light', light);
    root.setProperty('--primary-dark', dark);
    root.setProperty('--primary-bg', light);
  }

  applyDensity(density: 'comfortable' | 'default' | 'compact') {
    document.documentElement.classList.remove('density-comfortable', 'density-default', 'density-compact');
    document.documentElement.classList.add(`density-${density}`);
  }
}
```

### 10.2 Keyboard Shortcuts

Use Angular CDK or a dedicated service:

```typescript
// core/services/keyboard-shortcuts.service.ts
@Injectable({ providedIn: 'root' })
export class KeyboardShortcutsService {
  private router = inject(Router);
  private gPressed = false;
  private gTimer: any;

  init() {
    document.addEventListener('keydown', (e) => {
      if ((e.target as HTMLElement).matches('input, textarea, select')) return;

      // Cmd+K → Focus search
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        document.querySelector<HTMLInputElement>('.search-bar input')?.focus();
      }

      // Cmd+B → Toggle sidebar
      if ((e.metaKey || e.ctrlKey) && e.key === 'b') {
        e.preventDefault();
        // Emit sidebar toggle event
      }

      // Cmd+N → Open add app modal
      if ((e.metaKey || e.ctrlKey) && e.key === 'n') {
        e.preventDefault();
        // Open modal
      }

      // G+D → Dashboard, G+S → Settings, G+C → Copilot
      if (e.key === 'g' || e.key === 'G') {
        this.gPressed = true;
        clearTimeout(this.gTimer);
        this.gTimer = setTimeout(() => this.gPressed = false, 800);
        return;
      }
      if (this.gPressed) {
        this.gPressed = false;
        if (e.key === 'd') this.router.navigate(['/dashboard/home']);
        if (e.key === 's') this.router.navigate(['/dashboard/settings']);
        if (e.key === 'c') this.router.navigate(['/dashboard/ai-copilot']);
      }

      // ? → Shortcuts modal
      if (e.key === '?') {
        e.preventDefault();
        // Toggle shortcuts modal
      }

      // Esc → Close modals
      if (e.key === 'Escape') {
        // Close all open modals
      }
    });
  }
}
```

### 10.3 Toast Notification System

```typescript
// core/services/toast.service.ts
export type ToastType = 'success' | 'danger' | 'info' | 'warning';

interface Toast {
  id: number;
  type: ToastType;
  message: string;
}

@Injectable({ providedIn: 'root' })
export class ToastService {
  private counter = 0;
  toasts = signal<Toast[]>([]);

  show(type: ToastType, message: string, duration = 4000) {
    const id = ++this.counter;
    this.toasts.update(t => [...t, { id, type, message }]);
    setTimeout(() => this.dismiss(id), duration);
  }

  dismiss(id: number) {
    this.toasts.update(t => t.filter(toast => toast.id !== id));
  }

  success(message: string) { this.show('success', message); }
  danger(message: string) { this.show('danger', message); }
  info(message: string) { this.show('info', message); }
  warning(message: string) { this.show('warning', message); }
}
```

### 10.4 AI Copilot Chat

```typescript
// features/dashboard/ai-copilot/copilot.service.ts
interface CopilotResponse {
  pattern: RegExp;
  answer: string;
}

const responses: CopilotResponse[] = [
  { pattern: /spend|cost|budget/i, answer: 'Your total monthly SaaS spend is <strong>₹7.04L</strong>...' },
  { pattern: /shadow|unapproved/i, answer: 'I detected <strong>8 shadow IT applications</strong>...' },
  { pattern: /renew|contract|expir/i, answer: 'You have <strong>4 contracts renewing</strong>...' },
  { pattern: /compliance|risk|soc|gdpr/i, answer: 'Compliance Score: <strong>A+ (87/100)</strong>...' },
  { pattern: /user|utilization|unused|license/i, answer: 'License utilization is <strong>67%</strong>...' },
];

@Injectable()
export class CopilotService {
  getResponse(query: string): string {
    for (const r of responses) {
      if (r.pattern.test(query)) return r.answer;
    }
    return `I analyzed your SaaS landscape for "${query}"...`;
  }
}
```

### 10.5 Demo Walkthrough Engine

```typescript
// features/demo/demo.service.ts
@Injectable()
export class DemoService {
  state = signal({
    current: 1,
    total: 6,
    playing: true,
    elapsed: 0,
  });

  private autoPlayInterval?: ReturnType<typeof setInterval>;
  private timerInterval?: ReturnType<typeof setInterval>;

  init() {
    this.state.set({ current: 1, total: 6, playing: true, elapsed: 0 });
    this.startTimer();
    this.startAutoPlay();
  }

  goToStep(step: number) {
    this.state.update(s => ({ ...s, current: step }));
  }

  nextStep() {
    this.state.update(s => ({
      ...s,
      current: s.current < s.total ? s.current + 1 : 1,
    }));
  }

  prevStep() {
    this.state.update(s => ({
      ...s,
      current: Math.max(1, s.current - 1),
    }));
  }

  togglePlay() { /* ... */ }
  startAutoPlay() { /* 5s interval */ }
  startTimer() { /* 1s elapsed counter */ }
  destroy() { /* Clear intervals */ }
}
```

---

## 11. Project Structure

```
saasiq/
├── src/
│   ├── app/
│   │   ├── core/                           # Singletons — provided in root
│   │   │   ├── services/
│   │   │   │   ├── theme.service.ts
│   │   │   │   ├── toast.service.ts
│   │   │   │   ├── keyboard-shortcuts.service.ts
│   │   │   │   ├── auth.service.ts
│   │   │   │   └── local-storage.service.ts
│   │   │   ├── stores/
│   │   │   │   ├── appearance.store.ts      # Theme, accent, density
│   │   │   │   └── org.store.ts             # Org context
│   │   │   ├── guards/
│   │   │   │   └── auth.guard.ts
│   │   │   ├── interceptors/
│   │   │   │   └── auth.interceptor.ts
│   │   │   └── models/
│   │   │       ├── app.model.ts
│   │   │       ├── user.model.ts
│   │   │       ├── alert.model.ts
│   │   │       └── contract.model.ts
│   │   │
│   │   ├── shared/                          # Reusable, stateless components
│   │   │   ├── components/
│   │   │   │   ├── kpi-card/
│   │   │   │   │   ├── kpi-card.component.ts
│   │   │   │   │   ├── kpi-card.component.html
│   │   │   │   │   ├── kpi-card.component.scss
│   │   │   │   │   └── kpi-card.component.spec.ts
│   │   │   │   ├── chart-card/
│   │   │   │   ├── data-table/
│   │   │   │   ├── modal/
│   │   │   │   ├── toast/
│   │   │   │   ├── badge/
│   │   │   │   ├── avatar/
│   │   │   │   ├── button/
│   │   │   │   ├── toggle-switch/
│   │   │   │   ├── progress-bar/
│   │   │   │   ├── days-circle/
│   │   │   │   ├── app-icon/
│   │   │   │   ├── dropdown/
│   │   │   │   ├── filter-group/
│   │   │   │   ├── search-bar/
│   │   │   │   ├── page-header/
│   │   │   │   ├── svg-gauge/
│   │   │   │   └── typing-indicator/
│   │   │   ├── pipes/
│   │   │   │   ├── currency-inr.pipe.ts     # Indian ₹ formatting
│   │   │   │   ├── relative-time.pipe.ts    # "2 minutes ago"
│   │   │   │   └── truncate.pipe.ts
│   │   │   └── directives/
│   │   │       ├── click-outside.directive.ts
│   │   │       ├── auto-focus.directive.ts
│   │   │       └── tooltip.directive.ts
│   │   │
│   │   ├── layout/                          # App shell components
│   │   │   ├── app-shell/
│   │   │   │   ├── app-shell.component.ts
│   │   │   │   ├── app-shell.component.html
│   │   │   │   └── app-shell.component.scss
│   │   │   ├── sidebar/
│   │   │   │   ├── sidebar.component.ts
│   │   │   │   ├── sidebar.component.html
│   │   │   │   └── sidebar.component.scss
│   │   │   ├── topbar/
│   │   │   │   ├── topbar.component.ts
│   │   │   │   ├── topbar.component.html
│   │   │   │   └── topbar.component.scss
│   │   │   └── page-navigator/
│   │   │       ├── page-navigator.component.ts
│   │   │       ├── page-navigator.component.html
│   │   │       └── page-navigator.component.scss
│   │   │
│   │   ├── features/                        # Lazy-loaded feature components
│   │   │   ├── landing/
│   │   │   │   ├── landing.component.ts
│   │   │   │   ├── landing.component.html
│   │   │   │   ├── landing.component.scss
│   │   │   │   ├── hero/
│   │   │   │   ├── problems/
│   │   │   │   ├── customer-needs/
│   │   │   │   ├── features-section/
│   │   │   │   ├── pricing/
│   │   │   │   └── footer/
│   │   │   ├── auth/
│   │   │   │   ├── login/
│   │   │   │   │   ├── login.component.ts
│   │   │   │   │   ├── login.component.html
│   │   │   │   │   └── login.component.scss
│   │   │   │   └── signup/
│   │   │   │       ├── signup.component.ts
│   │   │   │       ├── signup.component.html
│   │   │   │       └── signup.component.scss
│   │   │   ├── onboarding/
│   │   │   │   ├── onboarding.component.ts
│   │   │   │   ├── onboarding.component.html
│   │   │   │   ├── onboarding.component.scss
│   │   │   │   ├── step-sso/
│   │   │   │   ├── step-integrations/
│   │   │   │   ├── step-invite/
│   │   │   │   └── step-preferences/
│   │   │   ├── demo/
│   │   │   │   ├── demo.component.ts
│   │   │   │   ├── demo.component.html
│   │   │   │   ├── demo.component.scss
│   │   │   │   ├── demo.service.ts
│   │   │   │   ├── step-connect/
│   │   │   │   ├── step-discovery/
│   │   │   │   ├── step-spend/
│   │   │   │   ├── step-ai/
│   │   │   │   ├── step-compliance/
│   │   │   │   └── step-roi/
│   │   │   └── dashboard/
│   │   │       ├── home/
│   │   │       │   ├── home.component.ts
│   │   │       │   ├── home.component.html
│   │   │       │   └── home.component.scss
│   │   │       ├── discovery/
│   │   │       ├── spend/
│   │   │       ├── usage/
│   │   │       ├── compliance/
│   │   │       ├── contracts/
│   │   │       ├── policies/
│   │   │       ├── ai-insights/
│   │   │       ├── ai-copilot/
│   │   │       │   ├── ai-copilot.component.ts
│   │   │       │   ├── ai-copilot.component.html
│   │   │       │   ├── ai-copilot.component.scss
│   │   │       │   └── copilot.service.ts
│   │   │       ├── offboarding/
│   │   │       ├── renewals/
│   │   │       ├── benchmarks/
│   │   │       ├── dept-costs/
│   │   │       ├── alerts/
│   │   │       └── settings/
│   │   │           ├── settings.component.ts
│   │   │           ├── settings.component.html
│   │   │           ├── settings.component.scss
│   │   │           ├── general/
│   │   │           ├── integrations/
│   │   │           ├── team/
│   │   │           ├── notifications/
│   │   │           ├── security/
│   │   │           ├── appearance/
│   │   │           ├── api-webhooks/
│   │   │           └── billing/
│   │   │
│   │   ├── app.component.ts
│   │   ├── app.config.ts
│   │   └── app.routes.ts
│   │
│   ├── assets/
│   │   ├── images/
│   │   └── icons/
│   │
│   ├── styles/
│   │   ├── _variables.scss                  # Design tokens (fallback for non-Tailwind)
│   │   ├── _animations.scss                 # All @keyframes
│   │   ├── _dark-theme.scss                 # Dark mode CSS variable overrides
│   │   ├── _density.scss                    # Comfortable/compact overrides
│   │   ├── _typography.scss                 # Font imports & base styles
│   │   └── styles.scss                      # Global entry point
│   │
│   ├── environments/
│   │   ├── environment.ts
│   │   └── environment.prod.ts
│   │
│   ├── index.html
│   └── main.ts
│
├── tests/
│   ├── e2e/                                 # Playwright E2E tests
│   │   ├── auth.spec.ts
│   │   ├── onboarding.spec.ts
│   │   ├── dashboard.spec.ts
│   │   ├── theme.spec.ts
│   │   └── shortcuts.spec.ts
│   └── visual/                              # Visual regression screenshots
│
├── .storybook/                              # Storybook config
│   ├── main.ts
│   └── preview.ts
│
├── angular.json
├── tailwind.config.ts
├── postcss.config.js
├── tsconfig.json
├── tsconfig.app.json
├── tsconfig.spec.json
├── jest.config.ts
├── playwright.config.ts
├── eslint.config.mjs
├── .prettierrc
├── .husky/
│   └── pre-commit
├── .lintstagedrc
├── package.json
└── README.md
```

---

## 12. Quick Start Commands

```bash
# ==============================
# Project Setup
# ==============================

# 1. Create Angular project
ng new saasiq --style=scss --routing --standalone --ssr=false --package-manager=pnpm
cd saasiq

# 2. Install all dependencies
pnpm add @angular/cdk @angular/animations \
  @fortawesome/angular-fontawesome @fortawesome/fontawesome-svg-core \
  @fortawesome/free-solid-svg-icons @fortawesome/free-brands-svg-icons \
  @fontsource/inter \
  @ngrx/signals @tanstack/angular-query-experimental \
  echarts ngx-echarts

pnpm add -D tailwindcss @tailwindcss/postcss postcss \
  jest jest-preset-angular @testing-library/angular @playwright/test \
  eslint angular-eslint prettier prettier-plugin-tailwindcss \
  husky lint-staged

# 3. Initialize Storybook
npx storybook@latest init --type angular

# 4. Initialize Playwright
npx playwright install

# 5. Initialize Husky
npx husky init

# ==============================
# Development
# ==============================

pnpm start                    # Dev server at localhost:4200
pnpm run storybook            # Storybook at localhost:6006
pnpm test                     # Run Jest unit tests
pnpm run test:e2e             # Run Playwright E2E tests
pnpm run lint                 # ESLint
pnpm run build                # Production build

# ==============================
# Generate Components
# ==============================

# Layout
ng g c layout/app-shell --standalone
ng g c layout/sidebar --standalone
ng g c layout/topbar --standalone
ng g c layout/page-navigator --standalone

# Shared Components
ng g c shared/components/kpi-card --standalone
ng g c shared/components/chart-card --standalone
ng g c shared/components/data-table --standalone
ng g c shared/components/modal --standalone
ng g c shared/components/toast --standalone
ng g c shared/components/badge --standalone
ng g c shared/components/avatar --standalone
ng g c shared/components/button --standalone
ng g c shared/components/toggle-switch --standalone
ng g c shared/components/progress-bar --standalone
ng g c shared/components/days-circle --standalone
ng g c shared/components/app-icon --standalone
ng g c shared/components/dropdown --standalone
ng g c shared/components/filter-group --standalone
ng g c shared/components/search-bar --standalone
ng g c shared/components/page-header --standalone
ng g c shared/components/svg-gauge --standalone
ng g c shared/components/typing-indicator --standalone

# Services
ng g s core/services/theme
ng g s core/services/toast
ng g s core/services/keyboard-shortcuts
ng g s core/services/auth

# Feature Components
ng g c features/landing --standalone
ng g c features/auth/login --standalone
ng g c features/auth/signup --standalone
ng g c features/onboarding --standalone
ng g c features/demo --standalone
ng g c features/dashboard/home --standalone
ng g c features/dashboard/discovery --standalone
ng g c features/dashboard/spend --standalone
ng g c features/dashboard/usage --standalone
ng g c features/dashboard/compliance --standalone
ng g c features/dashboard/contracts --standalone
ng g c features/dashboard/policies --standalone
ng g c features/dashboard/ai-insights --standalone
ng g c features/dashboard/ai-copilot --standalone
ng g c features/dashboard/offboarding --standalone
ng g c features/dashboard/renewals --standalone
ng g c features/dashboard/benchmarks --standalone
ng g c features/dashboard/dept-costs --standalone
ng g c features/dashboard/alerts --standalone
ng g c features/dashboard/settings --standalone
ng g c features/dashboard/settings/general --standalone
ng g c features/dashboard/settings/integrations --standalone
ng g c features/dashboard/settings/team --standalone
ng g c features/dashboard/settings/notifications --standalone
ng g c features/dashboard/settings/security --standalone
ng g c features/dashboard/settings/appearance --standalone
ng g c features/dashboard/settings/api-webhooks --standalone
ng g c features/dashboard/settings/billing --standalone

# Pipes
ng g p shared/pipes/currency-inr --standalone
ng g p shared/pipes/relative-time --standalone

# Directives
ng g d shared/directives/click-outside --standalone
ng g d shared/directives/auto-focus --standalone
```

---

## 13. Summary Table

| Category | Choice | Version |
|----------|--------|---------|
| **Framework** | Angular (standalone components) | 19.x |
| **Build Tool** | esbuild (Angular CLI) | Built-in |
| **Language** | TypeScript | 5.6+ |
| **Package Manager** | pnpm | Latest |
| **CSS Framework** | Tailwind CSS | 4.x |
| **CSS Preprocessor** | SCSS | Built-in |
| **Component Primitives** | Angular CDK (headless) | 19.x |
| **Charts** | Apache ECharts (ngx-echarts) | 5.6+ |
| **Icons** | Font Awesome 6 (angular-fontawesome) | 6.x |
| **Fonts** | Inter (@fontsource/inter) | 5.x |
| **Global State** | NgRx SignalStore | 19.x |
| **Server State** | TanStack Query (Angular) | 5.x |
| **Local State** | Angular Signals | Built-in |
| **Animations** | @angular/animations + CSS keyframes | 19.x |
| **Routing** | Angular Router (lazy loading) | 19.x |
| **Unit Testing** | Jest + jest-preset-angular | 29.x |
| **Component Testing** | Angular Testing Library | 17.x |
| **E2E Testing** | Playwright | 1.49+ |
| **Visual Regression** | Playwright screenshots / Chromatic | - |
| **Component Docs** | Storybook | 8.x |
| **Linting** | ESLint 9 + angular-eslint | 9.x |
| **Formatting** | Prettier + tailwindcss plugin | 3.x |
| **Git Hooks** | Husky + lint-staged | 9.x |

---

## Component Count Summary

| Category | Count |
|----------|-------|
| Layout Components | 4 |
| Shared UI Components | 18 |
| Feature Components | 20 |
| Settings Sub-Components | 8 |
| Services | 5 |
| Stores | 2 |
| Pipes | 3 |
| Directives | 3 |
| **Total Angular Files** | **~63 components + services** |

---

## Estimated Build Complexity

| Phase | Components | Estimated Effort |
|-------|-----------|-----------------|
| **Phase 1: Foundation** | Project setup, design tokens, shared components (18), layout (4) | 2-3 weeks |
| **Phase 2: Auth & Onboarding** | Landing, Login, Signup, Onboarding, Demo | 1-2 weeks |
| **Phase 3: Dashboard Core** | Home, Discovery, Spend, Usage | 2-3 weeks |
| **Phase 4: Governance** | Compliance, Contracts, Policies, AI Insights | 1-2 weeks |
| **Phase 5: Operations** | AI Copilot, Offboarding, Renewals, Benchmarks, Dept Costs, Alerts | 2-3 weeks |
| **Phase 6: Settings** | All 8 settings tabs | 1-2 weeks |
| **Phase 7: Polish** | Theme engine, keyboard shortcuts, animations, responsive, testing | 1-2 weeks |
| **Total** | 63 components | **10-17 weeks** (1 developer) |

---

> **This document covers every library, component, chart, animation, keyboard shortcut, and architectural decision needed to rebuild the SaaSIQ prototype pixel-for-pixel in Angular 19.**
