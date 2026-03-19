# SaaSIQ — Frontend System Design (E2E)
## Every Concept You Will Use — Nothing Extra

> **Scope**: Only concepts that directly apply to building SaaSIQ's Angular frontend  
> **Generated**: 7 March 2026  
> **Prototype Reference**: 15+ screens, 3 themes, 3 density modes, 6 accent colors, AI Copilot, real-time alerts

---

## Table of Contents

1. [Component Architecture](#1-component-architecture)
2. [State Management Architecture](#2-state-management-architecture)
3. [Rendering & Performance](#3-rendering--performance)
4. [Routing & Navigation Design](#4-routing--navigation-design)
5. [Design System & Theming Architecture](#5-design-system--theming-architecture)
6. [Real-Time Communication](#6-real-time-communication)
7. [API & Data Layer Design](#7-api--data-layer-design)
8. [Caching Architecture](#8-caching-architecture)
9. [Authentication & Security](#9-authentication--security)
10. [Error Handling & Resilience](#10-error-handling--resilience)
11. [Forms & Validation](#11-forms--validation)
12. [Accessibility (a11y)](#12-accessibility-a11y)
13. [Browser APIs You Will Use](#13-browser-apis-you-will-use)
14. [Logging & Error Tracking](#14-logging--error-tracking)
15. [Performance Monitoring](#15-performance-monitoring)
16. [Testing Architecture](#16-testing-architecture)
17. [Build, Bundle & Deployment](#17-build-bundle--deployment)
18. [Study Priority Roadmap](#18-study-priority-roadmap)

---

## 1. Component Architecture

### 1.1 Atomic Design Pattern

Structure components from smallest to largest. Every component in SaaSIQ maps to one level:

| Level | Definition | SaaSIQ Examples |
|-------|-----------|-----------------|
| **Atoms** | Single-purpose, no children | `BadgeComponent`, `AvatarComponent`, `ToggleSwitchComponent`, `ButtonComponent` |
| **Molecules** | Combine 2-3 atoms | `KpiCardComponent` (icon + value + badge), `SearchBarComponent` (input + icon + shortcut hint) |
| **Organisms** | Complex, self-contained sections | `SidebarComponent`, `DataTableComponent`, `AiCopilotChatComponent` |
| **Templates** | Page layouts with slots | `AppShellComponent` (sidebar + topbar + `<router-outlet>`), `AuthLayoutComponent` (split left/right) |
| **Pages** | Route-level components with data | `DashboardHomeComponent`, `SpendComponent`, `SettingsAppearanceComponent` |

### 1.2 Smart vs Presentational Components

| Type | Role | Data | SaaSIQ Example |
|------|------|------|----------------|
| **Smart (Container)** | Fetches data, manages state, handles side effects | Owns data | `DashboardHomeComponent` — calls API, holds KPI state, passes to children |
| **Presentational (Dumb)** | Renders UI, emits events, zero logic | Receives `@Input`, emits `@Output` | `KpiCardComponent` — receives `{ title, value, change, icon }`, displays it |

**Rule**: Presentational components never inject services. Smart components never have complex templates.

### 1.3 Component Composition Patterns

| Pattern | When to Use | SaaSIQ Usage |
|---------|-------------|--------------|
| **Content Projection** (`<ng-content>`) | Wrapper components that accept arbitrary children | `ModalComponent` — header/body/footer slots, `ChartCardComponent` — any chart inside |
| **Template Outlets** (`<ng-template>`) | When parent decides how to render child items | `DataTableComponent` — parent provides cell templates per column |
| **Component Inputs** (`@Input` / `input()`) | Passing data down | Every shared component |
| **Component Outputs** (`@Output` / `output()`) | Child → parent events | `FilterGroupComponent` emits `filterChange`, `AlertListComponent` emits `snooze` |

### 1.4 Standalone Components (Angular 19)

Every component is standalone — no `NgModule` declarations. Each component explicitly imports what it needs:

```typescript
@Component({
  standalone: true,
  selector: 'app-kpi-card',
  imports: [CommonModule, FaIconComponent, BadgeComponent],
  templateUrl: './kpi-card.component.html',
})
export class KpiCardComponent {
  title = input.required<string>();
  value = input.required<string>();
  change = input<number>();
  icon = input<IconDefinition>();
}
```

**Benefits**: Tree-shakeable (unused components don't ship), explicit dependency graph, faster compilation.

### 1.5 Component Communication Patterns

| Pattern | Direction | SaaSIQ Usage |
|---------|-----------|--------------|
| `input()` / `output()` | Parent → Child, Child → Parent | All parent-child pairs |
| **Service with Signals** | Any → Any (siblings, distant) | `ToastService.toasts` signal — any component triggers, `ToastContainerComponent` renders |
| **NgRx SignalStore** | Global shared state | `AppearanceStore` — Settings page writes, AppShell reads |
| **Router params/query** | Route → Component | Filters in URL: `/dashboard/discovery?status=unapproved&dept=engineering` |
| **Angular CDK Portal** | Teleport DOM to another location | Modal content rendered inside `<app-modal>` overlay |

---

## 2. State Management Architecture

### 2.1 Three Categories of State

Every piece of state in SaaSIQ falls into exactly one category. Never mix them:

| Category | What It Is | Tool | SaaSIQ Examples |
|----------|-----------|------|-----------------|
| **Server State** | Data from APIs that can become stale | **TanStack Query** | Apps list, KPI values, alerts, contracts, compliance scores |
| **Global UI State** | App-wide UI state shared across routes | **NgRx SignalStore** | Theme, accent color, density, current org, sidebar collapsed, user profile |
| **Local UI State** | Component-scoped, ephemeral | **Angular Signals** | Modal open/closed, active filter tab, search input text, form dirty state |

### 2.2 Signal-Based Reactivity (Angular 19)

Angular 19 replaces RxJS for most UI state with Signals — synchronous, glitch-free, fine-grained:

```typescript
// Local UI state with Signals
@Component({ /* ... */ })
export class AlertsComponent {
  // Local state — no store needed
  activeFilter = signal<'all' | 'critical' | 'warning' | 'info'>('all');
  searchQuery = signal('');
  
  // Derived state — auto-recomputes when dependencies change
  filteredAlerts = computed(() => {
    const alerts = this.alertsQuery.data() ?? [];
    const filter = this.activeFilter();
    const query = this.searchQuery().toLowerCase();
    
    return alerts
      .filter(a => filter === 'all' || a.severity === filter)
      .filter(a => a.title.toLowerCase().includes(query));
  });
}
```

**What to study**: `signal()`, `computed()`, `effect()`, `input()`, `output()`, `model()`, `linkedSignal()`, `resource()`.

### 2.3 Single Source of Truth

| Anti-Pattern | Correct Pattern |
|-------------|-----------------|
| Same alert count stored in sidebar badge AND alerts page AND topbar | Single `alertsQuery` in TanStack Query → all 3 components read from same cache |
| Copy user name into multiple component properties | `OrgStore.currentUser()` signal → all components reference it |
| Sync theme state manually across components | `AppearanceStore.theme()` → single signal, everyone subscribes |

### 2.4 Immutability

Never mutate state directly — always produce new references:

```typescript
// WRONG — Angular won't detect this change
this.alerts().push(newAlert);

// CORRECT — new array reference
this.alerts.update(list => [...list, newAlert]);

// WRONG — mutating object
this.user().name = 'New Name';

// CORRECT — new object
this.user.update(u => ({ ...u, name: 'New Name' }));
```

### 2.5 Optimistic Updates

Update UI immediately, then sync with backend. Revert if it fails:

| SaaSIQ Action | Optimistic Behavior |
|--------------|---------------------|
| Approve an app | Move to "Approved" instantly → API call in background → revert if 500 |
| Snooze an alert | Remove from list instantly → API call → re-add if fails |
| Toggle notification setting | Switch flips instantly → API call → flip back on error + show toast |
| Mark all alerts read | Clear unread badges instantly → API call |

```typescript
// TanStack Query optimistic update
useMutation({
  mutationFn: (alertId: string) => api.snoozeAlert(alertId),
  onMutate: async (alertId) => {
    await queryClient.cancelQueries({ queryKey: ['alerts'] });
    const previous = queryClient.getQueryData(['alerts']);
    queryClient.setQueryData(['alerts'], (old) =>
      old.filter(a => a.id !== alertId)
    );
    return { previous }; // saved for rollback
  },
  onError: (err, alertId, context) => {
    queryClient.setQueryData(['alerts'], context.previous); // rollback
    toast.danger('Failed to snooze alert');
  },
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ['alerts'] }); // refetch truth
  },
});
```

### 2.6 State Persistence

| What to Persist | Storage | Why |
|----------------|---------|-----|
| Theme, accent, density | `localStorage` | Survive page reload, apply before Angular boots |
| Current org ID | `localStorage` | Remember which org was active |
| Auth tokens | `httpOnly` cookie (preferred) or `localStorage` | Session persistence |
| Last visited route | `sessionStorage` | Redirect back after login |
| Filter selections | URL query params | Shareable, back-button friendly |

---

## 3. Rendering & Performance

### 3.1 Lazy Loading

SaaSIQ has 15+ dashboard sections. Loading all upfront wastes bandwidth:

```typescript
// Each route = separate JS chunk, downloaded on demand
{ path: 'spend', loadComponent: () => import('./features/dashboard/spend/spend.component') }
```

**What gets lazy loaded in SaaSIQ:**
- Every dashboard section (15 chunks)
- Landing page (1 chunk)
- Auth pages (1 chunk)
- Onboarding (1 chunk)
- Demo walkthrough (1 chunk)
- ECharts library (loaded only on pages with charts)

### 3.2 Change Detection — OnPush Strategy

Set on **every** component. Angular only re-renders when:
- An `input()` signal changes
- A signal read in the template changes
- An event handler fires within the component

```typescript
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,  // Always set this
  // ...
})
```

### 3.3 Virtual Scrolling

For long lists where rendering all DOM nodes would lag:

| SaaSIQ List | Estimated Items | Virtual Scroll? |
|-------------|----------------|-----------------|
| App discovery table | 50-500+ apps | Yes |
| Alerts list | 100+ alerts | Yes |
| Audit log (Security settings) | 1000+ entries | Yes |
| Team members table | 10-50 | No (too small) |
| Contracts timeline | 20-50 | No |

```typescript
import { ScrollingModule } from '@angular/cdk/scrolling';

@Component({
  imports: [ScrollingModule],
  template: `
    <cdk-virtual-scroll-viewport itemSize="56" class="alert-list">
      <app-alert-row *cdkVirtualFor="let alert of alerts()" [alert]="alert" />
    </cdk-virtual-scroll-viewport>
  `
})
```

### 3.4 Debouncing & Throttling

| Interaction | Strategy | Delay | SaaSIQ Usage |
|-------------|----------|-------|--------------|
| Search input typing | **Debounce** | 300ms | Search bar (⌘K), discovery filter, alerts search |
| Window resize | **Throttle** | 100ms | Sidebar responsive collapse |
| Scroll events | **Throttle** | 16ms (60fps) | Infinite scroll, scroll-spy |
| API mutation buttons | **Debounce** (leading edge) | 500ms | Prevent double-click on "Approve", "Block", "Save" |

```typescript
// Debounced search with signals
searchInput = signal('');
debouncedSearch = toSignal(
  toObservable(this.searchInput).pipe(debounceTime(300)),
  { initialValue: '' }
);
```

### 3.5 Bundle Splitting & Tree Shaking

| What | How |
|------|-----|
| Route-based splitting | `loadComponent()` — Angular CLI creates per-route chunks automatically |
| ECharts tree shaking | Import only used chart types: `import { LineChart, PieChart, BarChart } from 'echarts/charts'` |
| Font Awesome tree shaking | Import only used icons: `import { faHome, faBell } from '@fortawesome/free-solid-svg-icons'` |
| Dead code elimination | esbuild removes unused exports automatically |

### 3.6 Image & Asset Optimization

| Asset | Strategy |
|-------|----------|
| Inter font | Self-hosted via `@fontsource/inter` — no Google Fonts CDN request |
| App logos/icons | SVG where possible (infinite scale, small size) |
| Landing page images | `loading="lazy"`, `width`/`height` attributes to prevent CLS |
| Font Awesome icons | SVG rendering via `angular-fontawesome` (not CSS webfont — tree-shakeable) |

### 3.7 Skeleton Screens (Loading States)

Show layout-matching placeholder shimmer instead of spinners:

```typescript
@Component({
  template: `
    @if (kpisQuery.isLoading()) {
      <div class="kpi-grid">
        @for (i of [1,2,3,4]; track i) {
          <div class="kpi-card skeleton shimmer"></div>
        }
      </div>
    } @else {
      <div class="kpi-grid">
        @for (kpi of kpisQuery.data(); track kpi.id) {
          <app-kpi-card [data]="kpi" />
        }
      </div>
    }
  `
})
```

```scss
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 12px;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

**Every async section in SaaSIQ needs three states:**
1. **Loading** → Skeleton screen
2. **Success** → Actual content
3. **Error** → Error message + retry button

---

## 4. Routing & Navigation Design

### 4.1 Lazy-Loaded Route Configuration

```typescript
export const routes: Routes = [
  // Public pages
  { path: '', loadComponent: () => import('./features/landing/landing.component') },
  { path: 'login', loadComponent: () => import('./features/auth/login/login.component') },
  { path: 'signup', loadComponent: () => import('./features/auth/signup/signup.component') },
  { path: 'onboarding', loadComponent: () => import('./features/onboarding/onboarding.component') },
  { path: 'demo', loadComponent: () => import('./features/demo/demo.component') },
  
  // Protected dashboard
  {
    path: 'dashboard',
    loadComponent: () => import('./layout/app-shell/app-shell.component'),
    canActivate: [authGuard],
    children: [
      { path: '', redirectTo: 'home', pathMatch: 'full' },
      { path: 'home', loadComponent: () => import('./features/dashboard/home/home.component') },
      // ... 14 more dashboard sections
      {
        path: 'settings',
        loadComponent: () => import('./features/dashboard/settings/settings.component'),
        children: [
          { path: '', redirectTo: 'general', pathMatch: 'full' },
          // ... 8 settings tabs
        ]
      }
    ]
  },
  
  { path: '**', redirectTo: '' }
];
```

### 4.2 Route Guards

| Guard | Purpose | SaaSIQ Usage |
|-------|---------|--------------|
| `canActivate` | Block navigation to a route | `authGuard` — redirect to `/login` if no valid token |
| `canDeactivate` | Warn before leaving | Settings forms — "You have unsaved changes. Leave?" |
| `canMatch` | Conditionally load route based on condition | Role-based: only admins see `/settings/billing` |

```typescript
// auth.guard.ts
export const authGuard: CanActivateFn = (route, state) => {
  const auth = inject(AuthService);
  const router = inject(Router);
  
  if (auth.isAuthenticated()) return true;
  
  // Save intended URL for post-login redirect
  sessionStorage.setItem('redirectUrl', state.url);
  return router.createUrlTree(['/login']);
};
```

### 4.3 URL as State (Deep Linking)

Filters, tabs, and search queries live in the URL — enables sharing and back-button navigation:

```
/dashboard/discovery?status=unapproved&dept=engineering&search=slack
/dashboard/alerts?severity=critical&unread=true
/dashboard/settings/appearance
/dashboard/contracts?filter=expiring-soon
```

```typescript
// Reading and writing URL query params
@Component({ /* ... */ })
export class DiscoveryComponent {
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  // Read from URL
  status = toSignal(
    this.route.queryParamMap.pipe(map(p => p.get('status') ?? 'all'))
  );

  // Write to URL (no page reload)
  setFilter(status: string) {
    this.router.navigate([], {
      queryParams: { status },
      queryParamsHandling: 'merge', // preserve other params
    });
  }
}
```

### 4.4 Route Preloading

After initial page loads, prefetch likely-next routes in background:

```typescript
// app.config.ts
export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes, withPreloading(PreloadAllModules)),
    // OR custom strategy: only preload dashboard routes after login
  ],
};
```

### 4.5 Nested Router Outlets

SaaSIQ has 3 levels of nesting:

```
Level 1: AppComponent           → <router-outlet> renders Landing OR AppShell
Level 2: AppShellComponent      → <router-outlet> renders Dashboard sections
Level 3: SettingsComponent      → <router-outlet> renders Settings tabs
```

---

## 5. Design System & Theming Architecture

### 5.1 Design Tokens

Single source of truth for all visual values. Defined once, consumed everywhere:

```typescript
// tailwind.config.ts — defines the token system
export default {
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: '#7C3AED', light: '#A78BFA', dark: '#5B21B6', bg: '#F5F3FF' },
        // ... full palette
      },
      spacing: { sidebar: '260px', 'sidebar-collapsed': '68px', topbar: '64px' },
      borderRadius: { sm: '8px', DEFAULT: '12px' },
      boxShadow: { /* ... */ },
    }
  }
};
```

**Also exposed as CSS custom properties** for runtime changes (accent color switching):

```scss
:root {
  --primary: #7C3AED;
  --primary-light: #A78BFA;
  --primary-dark: #5B21B6;
  --primary-bg: #F5F3FF;
}
```

### 5.2 Theme Switching (Light / Dark / System)

Uses CSS class on `<body>` + CSS custom property overrides:

```scss
// Light theme — default (no class needed, tokens in :root are light)

// Dark theme — override every token
body.theme-dark {
  --gray-50: #111827;
  --gray-100: #1F2937;
  --gray-800: #F3F4F6;
  --gray-900: #F9FAFB;
  --card-bg: #1F2937;
  --card-border: #374151;
  --green-light: #064E3B;
  --red-light: #7F1D1D;
  // ... ~50 variable overrides
}

// System theme — detect via JS
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
prefersDark.addEventListener('change', (e) => {
  themeService.applyTheme(e.matches ? 'dark' : 'light');
});
```

**Key principle**: Components NEVER reference hardcoded colors. Always use `var(--primary)` or Tailwind classes. Theme switch = change variables, everything updates.

### 5.3 Dynamic Accent Color System

6 accent colors user can pick in Settings > Appearance. Changed at runtime:

```typescript
const ACCENTS = [
  { name: 'Purple', color: '#7C3AED', light: '#F5F3FF', dark: '#5B21B6' },
  { name: 'Blue',   color: '#3B82F6', light: '#EFF6FF', dark: '#1D4ED8' },
  { name: 'Green',  color: '#10B981', light: '#ECFDF5', dark: '#047857' },
  { name: 'Orange', color: '#F59E0B', light: '#FFFBEB', dark: '#B45309' },
  { name: 'Red',    color: '#EF4444', light: '#FEF2F2', dark: '#B91C1C' },
  { name: 'Teal',   color: '#14B8A6', light: '#F0FDFA', dark: '#0F766E' },
];

// Apply by changing CSS custom properties
document.documentElement.style.setProperty('--primary', accent.color);
document.documentElement.style.setProperty('--primary-light', accent.light);
document.documentElement.style.setProperty('--primary-dark', accent.dark);
```

### 5.4 Density Modes

3 density levels via CSS class on `<html>`:

```scss
.density-comfortable {
  --spacing-unit: 1.25;  // 25% more padding
  --font-size-base: 15px;
}

.density-default {
  --spacing-unit: 1;
  --font-size-base: 14px;
}

.density-compact {
  --spacing-unit: 0.8;  // 20% less padding
  --font-size-base: 13px;
}
```

### 5.5 Responsive Design Strategy

Mobile-first with 5 breakpoints matching the prototype:

| Breakpoint | Width | SaaSIQ Behavior |
|-----------|-------|-----------------|
| Default | < 640px | Single column, sidebar hidden, hamburger menu |
| `sm` | 640px | Stacked cards, compact tables |
| `md` | 768px | 2-column grids, sidebar as overlay |
| `lg` | 1024px | Sidebar visible but collapsible |
| `xl` | 1200px | Full layout, sidebar expanded |

**Sidebar responsive behavior:**
- **xl+**: Sidebar expanded (260px), collapsible with ⌘B
- **lg**: Sidebar collapsed by default (68px), expandable
- **< lg**: Sidebar hidden, slide-in drawer on hamburger click with backdrop overlay

---

## 6. Real-Time Communication

### 6.1 Server-Sent Events (SSE) — AI Copilot Streaming

**Why SSE for AI Copilot**: LLM APIs (OpenAI, Claude, etc.) return responses as SSE streams. The frontend reads tokens as they arrive, displaying text character-by-character like ChatGPT.

**How it works:**
```
Client                           Server (AI Engine)
  |                                    |
  |--- POST /api/copilot/stream ------>|
  |    { query: "Analyze my spend" }   |
  |                                    |
  |<--- data: {"token": "Your"}  ------|  (SSE event)
  |<--- data: {"token": " total"} -----|
  |<--- data: {"token": " SaaS"} ------|
  |<--- data: {"token": " spend"} -----|
  |<--- data: {"done": true}     ------|
  |                                    |
```

**Angular implementation:**

```typescript
@Injectable()
export class CopilotService {
  
  async streamResponse(query: string, onChunk: (text: string) => void): Promise<void> {
    const response = await fetch('/api/copilot/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.auth.getToken()}`,
      },
      body: JSON.stringify({ query }),
    });

    const reader = response.body!.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      
      const chunk = decoder.decode(value, { stream: true });
      // Parse SSE format: "data: {...}\n\n"
      const lines = chunk.split('\n').filter(l => l.startsWith('data: '));
      for (const line of lines) {
        const data = JSON.parse(line.slice(6));
        if (data.token) onChunk(data.token);
      }
    }
  }
}
```

**What to study:**
- `ReadableStream` API and `getReader()`
- `TextDecoder` for stream chunk decoding
- SSE data format: `data: {json}\n\n`
- Handling connection drops mid-stream
- AbortController to cancel ongoing streams

### 6.2 WebSocket — Real-Time Alerts & Live Data

**Why WebSocket for alerts/live data**: Bi-directional, persistent connection. Server pushes new alerts the moment they're detected — no polling delay.

**SaaSIQ WebSocket events:**

| Event (Server → Client) | Trigger | UI Update |
|-------------------------|---------|-----------|
| `alert:new` | New shadow IT detected, compliance violation | Toast notification + sidebar badge increment + alert list update |
| `scan:progress` | SaaS re-scan running | Progress ring percentage update |
| `scan:complete` | Re-scan finished | Refresh discovery data, show completion toast |
| `kpi:update` | Spend/usage data changed | Dashboard KPI cards live update |
| `org:switch` | Another admin switched org context | Sync state across tabs |

| Event (Client → Server) | Trigger | Purpose |
|-------------------------|---------|---------|
| `alert:ack` | User reads an alert | Update server-side read status |
| `presence:active` | User is on dashboard | Track active users for team features |

**Angular implementation with RxJS:**

```typescript
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';

@Injectable({ providedIn: 'root' })
export class RealtimeService {
  private ws$!: WebSocketSubject<any>;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 10;

  connect(token: string) {
    this.ws$ = webSocket({
      url: `wss://api.saasiq.com/ws?token=${token}`,
      openObserver: { next: () => { this.reconnectAttempts = 0; console.log('WS connected'); } },
      closeObserver: { next: () => this.reconnect(token) },
    });

    this.ws$.subscribe({
      next: (msg) => this.handleMessage(msg),
      error: () => this.reconnect(token),
    });
  }

  private reconnect(token: string) {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) return;
    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000); // exponential backoff, max 30s
    this.reconnectAttempts++;
    setTimeout(() => this.connect(token), delay);
  }

  private handleMessage(msg: any) {
    switch (msg.type) {
      case 'alert:new':
        // Invalidate TanStack Query cache → triggers refetch
        this.queryClient.invalidateQueries({ queryKey: ['alerts'] });
        this.toast.warning(msg.data.title);
        break;
      case 'scan:progress':
        this.scanProgress.set(msg.data.percent);
        break;
      case 'kpi:update':
        this.queryClient.invalidateQueries({ queryKey: ['dashboard', 'kpis'] });
        break;
    }
  }

  send(event: string, data: any) {
    this.ws$.next({ type: event, data });
  }

  disconnect() {
    this.ws$.complete();
  }
}
```

**What to study:**
- WebSocket handshake (HTTP → WS upgrade)
- `wss://` (TLS-encrypted WebSocket)
- `rxjs/webSocket` — turns WebSocket into Observable
- Reconnection with exponential backoff
- Heartbeat/ping-pong to detect zombie connections
- Authentication: token in query param or first message
- Multiplexing: single connection, multiple event types

### 6.3 SSE vs WebSocket — When to Use Which

| Criteria | SSE | WebSocket |
|----------|-----|-----------|
| Direction | Server → Client only | Bi-directional |
| Protocol | HTTP (works with HTTP/2) | Separate WS protocol |
| Reconnection | Auto-reconnect built-in | Manual reconnection needed |
| Auth headers | Yes (via fetch) | No (workaround: query param or first message) |
| Binary data | No | Yes |
| **SaaSIQ use** | AI Copilot streaming | Alerts, live KPIs, scan progress |

### 6.4 Webhooks — Outgoing Event Notifications

**Direction**: SaaSIQ Server → External URL (configured by user in Settings > API & Webhooks)

**SaaSIQ webhook events users can subscribe to:**
- `alert.created` — New alert triggered
- `app.discovered` — New SaaS app detected
- `contract.expiring` — Contract within 30 days of renewal
- `compliance.violation` — New compliance issue
- `scan.completed` — Discovery scan finished

**Frontend responsibility (Settings > API & Webhooks page):**
- CRUD UI: Create webhook (URL + events + secret), edit, delete
- Test button: Fire a test event to verify URL works
- Delivery log viewer: Show success/failure/retry for each delivery
- Display the HMAC-SHA256 signing secret (for receiver to verify authenticity)

**What to study:**
- Webhook concept: HTTP POST callback when event occurs
- HMAC-SHA256 payload signing (backend implements, frontend displays secret)
- Retry strategies (3 attempts with backoff)
- Idempotency keys (prevent duplicate processing)

---

## 7. API & Data Layer Design

### 7.1 API Abstraction (Service Layer)

Never call `HttpClient` directly in components. Always go through typed service classes:

```
Component → Service → HttpClient → Backend API
                ↓
         TanStack Query (caching layer)
```

```typescript
// services/discovery.service.ts
@Injectable({ providedIn: 'root' })
export class DiscoveryService {
  private http = inject(HttpClient);
  private baseUrl = environment.apiUrl;

  getApps(filters?: AppFilters): Observable<App[]> {
    return this.http.get<App[]>(`${this.baseUrl}/apps`, { params: filters as any });
  }

  approveApp(appId: string): Observable<void> {
    return this.http.patch<void>(`${this.baseUrl}/apps/${appId}/approve`, {});
  }

  blockApp(appId: string): Observable<void> {
    return this.http.patch<void>(`${this.baseUrl}/apps/${appId}/block`, {});
  }

  rescan(): Observable<{ scanId: string }> {
    return this.http.post<{ scanId: string }>(`${this.baseUrl}/apps/rescan`, {});
  }
}
```

### 7.2 TanStack Query Integration

Wraps service calls with caching, background refetch, loading/error states:

```typescript
// In component
@Component({ /* ... */ })
export class DiscoveryComponent {
  private discoveryService = inject(DiscoveryService);

  appsQuery = injectQuery(() => ({
    queryKey: ['apps', this.activeFilter()],
    queryFn: () => lastValueFrom(this.discoveryService.getApps({ status: this.activeFilter() })),
    staleTime: 5 * 60 * 1000, // Fresh for 5 minutes
  }));

  // In template:
  // appsQuery.isLoading()  → show skeleton
  // appsQuery.data()       → render list
  // appsQuery.isError()    → show error + retry
  // appsQuery.isFetching() → show subtle refresh indicator
}
```

### 7.3 HTTP Interceptors

Chain of middleware that processes every HTTP request/response:

```
Request flow:  Component → Service → [Auth Interceptor] → [Logging Interceptor] → Backend
Response flow: Backend → [Error Interceptor] → [Logging Interceptor] → Service → Component
```

**SaaSIQ needs 3 interceptors:**

```typescript
// 1. Auth Interceptor — attach JWT to every request
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const auth = inject(AuthService);
  const token = auth.getAccessToken();
  
  if (token) {
    req = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` }
    });
  }
  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        return auth.refreshToken().pipe(
          switchMap((newToken) => {
            req = req.clone({
              setHeaders: { Authorization: `Bearer ${newToken}` }
            });
            return next(req); // retry with new token
          }),
          catchError(() => {
            auth.logout(); // refresh failed → force login
            return throwError(() => error);
          })
        );
      }
      return throwError(() => error);
    })
  );
};

// 2. Error Interceptor — global error handling
export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const toast = inject(ToastService);
  const router = inject(Router);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      switch (error.status) {
        case 403: toast.danger('You don\'t have permission for this action'); break;
        case 404: toast.danger('Resource not found'); break;
        case 429: toast.warning('Too many requests. Please wait.'); break;
        case 500: toast.danger('Server error. Please try again.'); break;
        case 0:   toast.danger('Network error. Check your connection.'); break;
      }
      return throwError(() => error);
    })
  );
};

// 3. Logging Interceptor — dev-only request/response logging
export const loggingInterceptor: HttpInterceptorFn = (req, next) => {
  if (!environment.production) {
    const start = Date.now();
    return next(req).pipe(
      tap(() => {
        console.log(`[HTTP] ${req.method} ${req.url} — ${Date.now() - start}ms`);
      })
    );
  }
  return next(req);
};

// Register in app.config.ts
provideHttpClient(
  withInterceptors([authInterceptor, errorInterceptor, loggingInterceptor])
)
```

### 7.4 Request Deduplication

Multiple components on the same page requesting the same data → only 1 HTTP call:

```
DashboardHome shows KPIs        → queryKey: ['kpis']  ─┐
Sidebar badge shows alert count  → queryKey: ['alerts'] ─┤→ TanStack Query deduplicates
Topbar badge shows alert count   → queryKey: ['alerts'] ─┘   → only 1 HTTP call per unique key
```

TanStack Query handles this automatically when components use the same `queryKey`.

### 7.5 Pagination Patterns

| Pattern | When to Use | SaaSIQ Usage |
|---------|-------------|--------------|
| **Offset-based** (`?page=2&limit=25`) | Tables with page numbers | Discovery apps table, audit log |
| **Cursor-based** (`?after=abc123&limit=25`) | Infinite scroll, real-time lists | Alerts feed, AI copilot chat history |

```typescript
// Infinite scroll with TanStack Query
alertsQuery = injectInfiniteQuery(() => ({
  queryKey: ['alerts', this.filter()],
  queryFn: ({ pageParam }) => lastValueFrom(
    this.alertService.getAlerts({ after: pageParam, limit: 25 })
  ),
  initialPageParam: undefined as string | undefined,
  getNextPageParam: (lastPage) => lastPage.nextCursor,
}));
```

---

## 8. Caching Architecture

### 8.1 Multi-Layer Caching

| Layer | Tool | What's Cached | TTL |
|-------|------|--------------|-----|
| **Browser HTTP Cache** | `Cache-Control` headers | Static assets (JS, CSS, fonts, images) | Long (1 year with hash) |
| **Application Cache** | TanStack Query | API responses | Configured per-query |
| **Memory Cache** | Angular Signals / Stores | UI state (theme, org, sidebar) | Session lifetime |
| **Persistent Cache** | `localStorage` | User preferences, tokens | Until cleared |
| **URL Cache** | Query params | Filter state, search, active tab | Browser history |

### 8.2 TanStack Query Cache Config (Per Feature)

| Data | `staleTime` | `gcTime` | Why |
|------|-------------|----------|-----|
| Dashboard KPIs | 5 min | 30 min | Updates aren't instant, polling is fine |
| App discovery list | 2 min | 15 min | Can change on scan, but not constantly |
| Alerts | 30 sec | 10 min | Near real-time (also WebSocket push) |
| User profile | 30 min | 60 min | Rarely changes |
| Settings (all tabs) | 10 min | 30 min | Admin changes infrequently |
| Compliance scores | 5 min | 30 min | Updated on scan |
| Contract list | 10 min | 30 min | Changes are rare |

### 8.3 Cache Invalidation

When data changes, tell TanStack Query to refetch:

| Action | Invalidate |
|--------|-----------|
| Approve/block app | `['apps']` |
| Snooze/dismiss alert | `['alerts']` |
| Save settings | `['settings', tabName]` |
| Complete re-scan | `['apps']`, `['kpis']`, `['compliance']` |
| Switch org | **Everything** (`queryClient.clear()`) |
| WebSocket `alert:new` | `['alerts']`, `['kpis']` (badge count) |

```typescript
// After approving an app
this.queryClient.invalidateQueries({ queryKey: ['apps'] });
// This triggers a background refetch → UI updates automatically
```

---

## 9. Authentication & Security

### 9.1 OAuth 2.0 + PKCE (Login with Google/Microsoft)

SaaSIQ's onboarding Step 1 is "Connect SSO (Google Workspace / Microsoft)". This uses OAuth 2.0 Authorization Code Flow with PKCE.

**The flow:**

```
1. User clicks "Sign in with Google"
2. Angular generates:
   - code_verifier: random 128-char string
   - code_challenge: SHA256(code_verifier), base64url-encoded
3. Redirect to Google: 
   https://accounts.google.com/o/oauth2/v2/auth
     ?client_id=YOUR_CLIENT_ID
     &redirect_uri=https://app.saasiq.com/auth/callback
     &response_type=code
     &scope=openid email profile
     &code_challenge=<hash>
     &code_challenge_method=S256
     &state=<random_csrf_token>
4. User consents on Google's page
5. Google redirects back:
   https://app.saasiq.com/auth/callback?code=AUTH_CODE&state=<csrf_token>
6. Angular sends AUTH_CODE + code_verifier to YOUR backend
7. Your backend exchanges code for tokens with Google
8. Backend returns JWT (access + refresh) to Angular
9. Angular stores tokens, navigates to /dashboard
```

**What to study:**
- PKCE (Proof Key for Code Exchange) — why SPAs need it (no client secret)
- `code_verifier` / `code_challenge` generation
- `state` parameter for CSRF protection
- Token exchange happens on YOUR backend (never expose client secret to browser)
- Library: `angular-oauth2-oidc` handles most of this

### 9.2 JWT Token Lifecycle

```
                                    ┌─────────────────────────┐
                                    │   Access Token (15min)   │
                                    │   Contains: userId,      │
                                    │   orgId, role, exp       │
┌──────────┐   POST /login    ┌─────┤                          │
│  Login    │ ───────────────> │ API │                          │
│  Page     │ <─────────────── │     ├─────────────────────────┤
└──────────┘   Set-Cookie:    │     │  Refresh Token (7 days)  │
               refresh_token   │     │  httpOnly, Secure, Path  │
               (httpOnly)      └─────┤  = /api/auth/refresh     │
                                    └─────────────────────────┘

Every API call:
  Request Header: Authorization: Bearer <access_token>

When access_token expires (HTTP 401):
  1. Interceptor catches 401
  2. Calls POST /api/auth/refresh (cookie sent automatically)
  3. Gets new access_token
  4. Retries original request with new token
  5. If refresh fails → logout, redirect to /login
```

**What to study:**
- JWT structure: `header.payload.signature` (base64url encoded)
- Never decode JWT on frontend for authorization (only for display — the server must always verify)
- Access token: short-lived, stored in memory (JavaScript variable)
- Refresh token: long-lived, stored in `httpOnly` cookie (JavaScript can't read it — XSS-safe)
- Token rotation: each refresh issues a new refresh token (detect stolen tokens)

### 9.3 XSS Prevention

| Risk Area in SaaSIQ | Mitigation |
|---------------------|-----------|
| AI Copilot responses (contain HTML formatting) | Angular auto-sanitizes `[innerHTML]`. Use `DomSanitizer.bypassSecurityTrustHtml()` ONLY for trusted content |
| User-generated content (org name, team member names) | Always use `{{ interpolation }}` (auto-escaped), never `[innerHTML]` |
| Search queries reflected in UI | Angular template binding is safe by default |
| Webhook URLs displayed | Sanitize display, don't render as clickable without validation |

**Content Security Policy (CSP) header:**
```
Content-Security-Policy: 
  default-src 'self';
  script-src 'self';
  style-src 'self' 'unsafe-inline';  // needed for Tailwind/inline styles
  font-src 'self';
  img-src 'self' data: https:;
  connect-src 'self' wss://api.saasiq.com;
```

### 9.4 CORS (Cross-Origin Resource Sharing)

Frontend at `https://app.saasiq.com` calls API at `https://api.saasiq.com` — different origin.

**What to study:**
- Preflight requests: browser sends `OPTIONS` before `POST`, `PUT`, `DELETE` with custom headers
- `Access-Control-Allow-Origin`, `Access-Control-Allow-Credentials`, `Access-Control-Allow-Headers`
- This is configured on the **backend** (Django), but you need to understand it to debug CORS errors
- Dev setup: Angular proxy config (`proxy.conf.json`) to avoid CORS during development

```json
// proxy.conf.json (dev only)
{
  "/api": {
    "target": "http://localhost:8000",
    "secure": false,
    "changeOrigin": true
  }
}
```

### 9.5 RBAC (Role-Based Access Control)

SaaSIQ has roles: **Owner**, **Admin**, **Member**, **Viewer**

| Feature | Owner | Admin | Member | Viewer |
|---------|-------|-------|--------|--------|
| View dashboard | Yes | Yes | Yes | Yes |
| Approve/block apps | Yes | Yes | Yes | No |
| Manage team | Yes | Yes | No | No |
| Billing & plan | Yes | No | No | No |
| Delete org | Yes | No | No | No |

**Frontend enforcement (UI-level — backend always re-validates):**

```typescript
// Directive to hide elements based on role
@Directive({ selector: '[appRequireRole]', standalone: true })
export class RequireRoleDirective {
  private role = input.required<string>({ alias: 'appRequireRole' });
  private auth = inject(AuthService);
  private vcr = inject(ViewContainerRef);
  private tmpl = inject(TemplateRef);

  constructor() {
    effect(() => {
      if (this.auth.hasRole(this.role())) {
        this.vcr.createEmbeddedView(this.tmpl);
      } else {
        this.vcr.clear();
      }
    });
  }
}

// Usage
<button *appRequireRole="'admin'" (click)="inviteMember()">Invite Member</button>
```

### 9.6 CSRF Protection

For APIs that use cookies (refresh token rotation):

```typescript
// app.config.ts
provideHttpClient(
  withXsrfConfiguration({
    cookieName: 'csrftoken',     // Django's default
    headerName: 'X-CSRFToken',   // Django's default
  })
)
```

---

## 10. Error Handling & Resilience

### 10.1 Three-State Pattern (Every Async Operation)

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│ LOADING  │ ──> │ SUCCESS  │     │  ERROR   │
│ skeleton │     │ show data│     │ message  │
│ shimmer  │     │          │     │ + retry  │
└──────────┘     └──────────┘     └──────────┘
      │                                 ▲
      └─────────────────────────────────┘
```

```html
@if (appsQuery.isLoading()) {
  <app-skeleton-table [rows]="5" />
} @else if (appsQuery.isError()) {
  <app-error-state 
    message="Failed to load apps" 
    (retry)="appsQuery.refetch()" />
} @else {
  <app-data-table [data]="appsQuery.data()" />
}
```

### 10.2 Retry Logic

TanStack Query retries failed requests automatically:

```typescript
injectQuery(() => ({
  queryKey: ['apps'],
  queryFn: () => api.getApps(),
  retry: 3,                              // retry 3 times
  retryDelay: (attempt) => Math.min(1000 * 2 ** attempt, 30000), // 1s, 2s, 4s
}));
```

### 10.3 Global Error Handler

Catches unhandled exceptions anywhere in the app:

```typescript
@Injectable()
export class GlobalErrorHandler implements ErrorHandler {
  private toast = inject(ToastService);

  handleError(error: any): void {
    // Send to Sentry
    Sentry.captureException(error.originalError || error);
    
    // Log for dev
    console.error('[SaaSIQ]', error);
    
    // Show user-friendly message (never show stack traces)
    this.toast.danger('Something went wrong. Please try again.');
  }
}

// Register in app.config.ts
{ provide: ErrorHandler, useClass: GlobalErrorHandler }
```

### 10.4 Graceful Degradation

| Failure | Fallback |
|---------|----------|
| ECharts fails to load | Show data in a table instead of chart |
| WebSocket disconnects | Fall back to HTTP polling every 30s |
| Font fails to load | CSS font stack falls back to `-apple-system, sans-serif` |
| AI Copilot stream fails mid-response | Show partial response + "Response interrupted. Try again." |
| Image 404 | Show colored initials avatar (already in prototype) |

---

## 11. Forms & Validation

### 11.1 Reactive Forms

SaaSIQ has multiple form-heavy pages. Use Angular Reactive Forms throughout:

| Page | Form Fields |
|------|-------------|
| **Login** | Email, password |
| **Signup** | Full name, company, email, password |
| **Onboarding Step 3** | Team member name + email (dynamic list) |
| **Settings > General** | Company name, fiscal year, currency |
| **Settings > Team > Invite** | Email, role dropdown |
| **Settings > API > Create Webhook** | URL, events (multi-select), secret |
| **Settings > Security** | Session timeout, 2FA settings |
| **Alert Snooze** | Duration picker |

```typescript
@Component({ /* ... */ })
export class SignupComponent {
  private fb = inject(FormBuilder);

  form = this.fb.group({
    fullName: ['', [Validators.required, Validators.minLength(2)]],
    company: ['', [Validators.required]],
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8), this.strongPasswordValidator]],
  });

  strongPasswordValidator(control: AbstractControl): ValidationErrors | null {
    const val = control.value;
    const hasUpper = /[A-Z]/.test(val);
    const hasLower = /[a-z]/.test(val);
    const hasNumber = /[0-9]/.test(val);
    if (!hasUpper || !hasLower || !hasNumber) {
      return { weakPassword: true };
    }
    return null;
  }

  onSubmit() {
    if (this.form.valid) {
      this.authService.signup(this.form.getRawValue());
    } else {
      this.form.markAllAsTouched(); // show all validation errors
    }
  }
}
```

### 11.2 Inline Validation UX

```html
<div class="form-field">
  <label for="email">Email</label>
  <input id="email" formControlName="email" 
    [class.error]="form.get('email')?.invalid && form.get('email')?.touched" />
  
  @if (form.get('email')?.hasError('required') && form.get('email')?.touched) {
    <span class="error-text">Email is required</span>
  } @else if (form.get('email')?.hasError('email') && form.get('email')?.touched) {
    <span class="error-text">Enter a valid email address</span>
  }
</div>
```

### 11.3 Unsaved Changes Guard

Warn before navigating away from dirty forms:

```typescript
export const unsavedChangesGuard: CanDeactivateFn<{ hasUnsavedChanges: () => boolean }> = (component) => {
  if (component.hasUnsavedChanges()) {
    return confirm('You have unsaved changes. Are you sure you want to leave?');
  }
  return true;
};

// On settings routes
{ path: 'general', loadComponent: () => ..., canDeactivate: [unsavedChangesGuard] }
```

---

## 12. Accessibility (a11y)

### 12.1 Semantic HTML

```html
<!-- SaaSIQ layout with correct landmarks -->
<nav class="sidebar" role="navigation" aria-label="Main navigation">...</nav>
<header class="topbar" role="banner">...</header>
<main class="main-content" role="main">
  <router-outlet />
</main>
```

### 12.2 Keyboard Navigation

| Requirement | Implementation |
|-------------|---------------|
| All interactive elements via Tab | Proper `tabindex`, native `<button>` and `<a>` elements |
| Modal focus trap | `cdkTrapFocus` from Angular CDK |
| Return focus after modal close | Save `document.activeElement` before open, restore on close |
| Skip navigation link | Hidden "Skip to main content" link, visible on focus |
| Custom components | Add `role`, `aria-expanded`, `aria-haspopup`, `aria-label` |

### 12.3 ARIA for SaaSIQ Components

| Component | Required ARIA |
|-----------|--------------|
| Sidebar nav | `role="navigation"`, `aria-label="Main navigation"`, `aria-current="page"` on active link |
| Modal | `role="dialog"`, `aria-modal="true"`, `aria-labelledby="modal-title"` |
| Toast | `role="alert"`, `aria-live="assertive"` |
| Dropdown | `aria-expanded`, `aria-haspopup="true"`, `role="menu"`, `role="menuitem"` |
| Toggle switch | `role="switch"`, `aria-checked` |
| KPI card change | `aria-label="Increased by 12%"` (screen readers can't interpret ↑ 12%) |
| Charts | `aria-label` with data summary (ECharts supports `aria` option) |
| Alert severity | Not just color — icon + text label for colorblind users |
| Search bar | `role="search"`, `aria-label="Search SaaS applications"` |

### 12.4 Color Contrast

WCAG AA requires 4.5:1 for normal text, 3:1 for large text. Must verify across:
- 3 themes (light, dark, system)
- 6 accent colors
- That's 18 combinations to test

Use Chrome DevTools → Rendering → "Emulate vision deficiencies" to test protanopia, deuteranopia, tritanopia.

---

## 13. Browser APIs You Will Use

### 13.1 Clipboard API (Copy API Key, Copy Webhook Secret)

```typescript
async copyToClipboard(text: string) {
  await navigator.clipboard.writeText(text);
  this.toast.success('Copied to clipboard');
}
```

Settings > API & Webhooks: "Copy API Key" button, "Copy Webhook Secret" button.

### 13.2 matchMedia API (System Theme Detection)

```typescript
// Detect system dark mode preference
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

// Listen for system theme changes (real-time)
prefersDark.addEventListener('change', (e) => {
  if (this.appearanceStore.theme() === 'system') {
    this.themeService.applyTheme(e.matches ? 'dark' : 'light');
  }
});
```

### 13.3 ResizeObserver (Chart Resizing, Sidebar Collapse)

```typescript
// Resize ECharts when container changes size (sidebar collapse/expand)
private resizeObserver = new ResizeObserver(() => {
  this.chartInstance?.resize();
});

ngAfterViewInit() {
  this.resizeObserver.observe(this.chartContainer.nativeElement);
}

ngOnDestroy() {
  this.resizeObserver.disconnect();
}
```

### 13.4 IntersectionObserver (Lazy Load Sections, Animate on Scroll)

```typescript
// Landing page: animate feature cards when they scroll into view
@Directive({ selector: '[appAnimateOnScroll]', standalone: true })
export class AnimateOnScrollDirective implements AfterViewInit {
  private el = inject(ElementRef);

  ngAfterViewInit() {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          this.el.nativeElement.classList.add('animate-in');
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );
    observer.observe(this.el.nativeElement);
  }
}
```

Used on: Landing page feature cards, problem cards, customer need cards, pricing cards.

### 13.5 localStorage / sessionStorage

| Storage | What | Why |
|---------|------|-----|
| `localStorage['saasiq-theme']` | `'light'` / `'dark'` / `'system'` | Persist theme across sessions |
| `localStorage['saasiq-accent']` | `'#7C3AED'` | Persist accent color |
| `localStorage['saasiq-density']` | `'default'` | Persist density mode |
| `localStorage['saasiq-org']` | `'org_123'` | Remember last org |
| `sessionStorage['redirectUrl']` | `'/dashboard/spend'` | Redirect after login |

### 13.6 requestAnimationFrame (Animated Counters)

KPI values animate from 0 to target number on page load (matching prototype):

```typescript
animateCounter(target: number, duration: number = 1500): Observable<number> {
  return new Observable(subscriber => {
    const start = performance.now();
    
    function tick(now: number) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // easeOutCubic
      
      subscriber.next(Math.round(target * eased));
      
      if (progress < 1) {
        requestAnimationFrame(tick);
      } else {
        subscriber.complete();
      }
    }
    
    requestAnimationFrame(tick);
  });
}
```

### 13.7 Notification API (Browser Push Notifications)

For critical alerts when user has SaaSIQ in background tab:

```typescript
async showBrowserNotification(title: string, body: string) {
  if (Notification.permission === 'default') {
    await Notification.requestPermission();
  }
  if (Notification.permission === 'granted') {
    new Notification(title, {
      body,
      icon: '/assets/icons/saasiq-icon.png',
      badge: '/assets/icons/saasiq-badge.png',
    });
  }
}
```

Triggered when: New critical alert via WebSocket while tab is inactive.

### 13.8 AbortController (Cancel In-Flight Requests)

```typescript
// Cancel AI copilot stream if user sends new message
private abortController?: AbortController;

async sendMessage(query: string) {
  // Cancel previous stream
  this.abortController?.abort();
  this.abortController = new AbortController();

  const response = await fetch('/api/copilot/stream', {
    method: 'POST',
    body: JSON.stringify({ query }),
    signal: this.abortController.signal, // <-- cancel mechanism
  });
  // ... read stream
}
```

---

## 14. Logging & Error Tracking

### 14.1 Sentry Integration

```typescript
// main.ts — initialize before Angular boots
import * as Sentry from '@sentry/angular';

Sentry.init({
  dsn: environment.sentryDsn,
  environment: environment.production ? 'production' : 'development',
  release: environment.appVersion,
  integrations: [
    Sentry.browserTracingIntegration(),
    Sentry.replayIntegration(), // session replay for debugging
  ],
  tracesSampleRate: 0.2,    // 20% of transactions
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0, // 100% replay on errors
});
```

**What Sentry captures in SaaSIQ:**
- Unhandled exceptions (via `GlobalErrorHandler`)
- HTTP errors (4xx, 5xx) with request details
- WebSocket connection failures
- Performance traces (route transitions, API call durations)
- Session replays (see exactly what user did before crash)
- Breadcrumbs (navigation, clicks, console logs leading to error)

### 14.2 Structured Logging (Dev)

```typescript
@Injectable({ providedIn: 'root' })
export class LoggerService {
  private isProduction = environment.production;

  debug(component: string, message: string, data?: any) {
    if (!this.isProduction) {
      console.debug(`[${component}]`, message, data ?? '');
    }
  }

  warn(component: string, message: string, data?: any) {
    console.warn(`[${component}]`, message, data ?? '');
    Sentry.addBreadcrumb({ category: component, message, level: 'warning', data });
  }

  error(component: string, message: string, error?: any) {
    console.error(`[${component}]`, message, error ?? '');
    Sentry.captureException(error);
  }
}

// Usage
this.logger.debug('DiscoveryComponent', 'Filters changed', { status: 'unapproved' });
this.logger.error('CopilotService', 'Stream failed', err);
```

### 14.3 HTTP Request Logging (Dev Only)

The logging interceptor (Section 7.3) logs every request with timing:

```
[HTTP] GET /api/apps — 234ms
[HTTP] POST /api/copilot/stream — 1,847ms
[HTTP] PATCH /api/apps/123/approve — 89ms
```

---

## 15. Performance Monitoring

### 15.1 Core Web Vitals

| Metric | What | Target | SaaSIQ Concern |
|--------|------|--------|----------------|
| **LCP** (Largest Contentful Paint) | Time until largest visible element renders | < 2.5s | Dashboard KPI grid, landing hero |
| **INP** (Interaction to Next Paint) | Latency of user interactions | < 200ms | Sidebar clicks, filter toggles, modal opens |
| **CLS** (Cumulative Layout Shift) | Visual stability (elements jumping) | < 0.1 | Font loading (Inter), lazy-loaded images, skeleton → content swap |

**Measurement:**
```typescript
// Install: pnpm add web-vitals
import { onLCP, onINP, onCLS } from 'web-vitals';

onLCP(metric => Sentry.captureMessage('LCP', { extra: { value: metric.value } }));
onINP(metric => Sentry.captureMessage('INP', { extra: { value: metric.value } }));
onCLS(metric => Sentry.captureMessage('CLS', { extra: { value: metric.value } }));
```

### 15.2 Bundle Size Analysis

```bash
# After build, analyze what's in each chunk
pnpm build --stats-json
npx source-map-explorer dist/saasiq/browser/*.js
```

**Size budgets (angular.json):**
```json
{
  "budgets": [
    { "type": "initial", "maximumWarning": "500kb", "maximumError": "1mb" },
    { "type": "anyComponentStyle", "maximumWarning": "4kb", "maximumError": "8kb" }
  ]
}
```

### 15.3 Runtime Performance Profiling

| What to Profile | Tool | When |
|----------------|------|------|
| Component render time | Angular DevTools Profiler | If UI feels sluggish |
| Memory leaks | Chrome DevTools Memory tab | After prolonged use (subscriptions not unsubscribed) |
| Layout thrashing | Chrome DevTools Performance tab | If animations stutter |
| Change detection cycles | Angular DevTools | If OnPush isn't reducing re-renders |

**Common memory leak sources in SaaSIQ:**
- WebSocket subscription not `unsubscribe()`'d in `ngOnDestroy`
- `setInterval` / `setTimeout` in demo walkthrough not cleared
- `ResizeObserver` not disconnected
- `IntersectionObserver` not disconnected
- `EventListener` (keyboard shortcuts) not removed

```typescript
// Always clean up in ngOnDestroy
export class ChartComponent implements OnDestroy {
  private destroyRef = inject(DestroyRef);
  
  constructor() {
    // Auto-cleanup with takeUntilDestroyed
    this.ws$.pipe(takeUntilDestroyed(this.destroyRef)).subscribe(/* ... */);
  }
}
```

---

## 16. Testing Architecture

### 16.1 Testing Pyramid

```
        ╱ E2E Tests (Playwright) ╲          ← Few: 10-15 critical flows
       ╱   Slow, expensive, high    ╲
      ╱    confidence                  ╲
     ╱─────────────────────────────────╲
    ╱ Integration / Component Tests      ╲   ← Medium: 50-80 component tests
   ╱  (Angular Testing Library)           ╲
  ╱────────────────────────────────────────╲
 ╱ Unit Tests (Jest)                         ╲ ← Many: 100-200 service/pipe/util tests
╱  Fast, cheap, narrow scope                   ╲
```

### 16.2 What to Test at Each Level

| Level | What | SaaSIQ Examples |
|-------|------|-----------------|
| **Unit** | Pure logic, no DOM | `CurrencyInrPipe.transform(704000)` → `₹7.04L`, `CopilotService.matchIntent('spend')` → savings response, `AppearanceStore.setTheme('dark')` updates signal |
| **Component** | Render + interact + assert DOM | `KpiCardComponent` renders value and change badge, `ModalComponent` closes on Escape, `FilterGroupComponent` emits on click |
| **E2E** | Full user flows across pages | Signup → Onboarding → Dashboard, Theme switch persists on reload, Sidebar collapse + keyboard shortcut |

### 16.3 Component Test Example

```typescript
// kpi-card.component.spec.ts
import { render, screen } from '@testing-library/angular';
import { KpiCardComponent } from './kpi-card.component';

describe('KpiCardComponent', () => {
  it('renders title and value', async () => {
    await render(KpiCardComponent, {
      inputs: { title: 'Total Apps', value: '127', change: 12 },
    });

    expect(screen.getByText('Total Apps')).toBeInTheDocument();
    expect(screen.getByText('127')).toBeInTheDocument();
    expect(screen.getByText('+12%')).toBeInTheDocument();
  });

  it('shows negative change in red', async () => {
    await render(KpiCardComponent, {
      inputs: { title: 'Spend', value: '₹7.04L', change: -8 },
    });

    const badge = screen.getByText('-8%');
    expect(badge).toHaveClass('badge-red');
  });
});
```

### 16.4 Visual Regression Testing

Screenshot comparison to catch unintended CSS changes:

```typescript
// tests/visual/themes.spec.ts (Playwright)
const themes = ['light', 'dark'];
const densities = ['comfortable', 'default', 'compact'];
const accents = ['#7C3AED', '#3B82F6', '#10B981'];

for (const theme of themes) {
  for (const density of densities) {
    test(`Dashboard Home - ${theme} - ${density}`, async ({ page }) => {
      await page.goto('/dashboard/home');
      await page.evaluate(([t, d]) => {
        document.body.className = `theme-${t}`;
        document.documentElement.className = `density-${d}`;
      }, [theme, density]);
      
      await expect(page).toHaveScreenshot(`home-${theme}-${density}.png`);
    });
  }
}
```

---

## 17. Build, Bundle & Deployment

### 17.1 Build Pipeline

```
Code Push → CI Trigger → Lint → Unit Tests → Build → E2E Tests → Deploy
              │            │         │          │          │          │
              │          ESLint   Jest      esbuild   Playwright  Vercel/
              │         Prettier  (parallel) (prod)   (parallel)  AWS/GCP
              │            │         │          │          │
              └── Fail fast on any step ──────────────────┘
```

### 17.2 Environment Configuration

```typescript
// environments/environment.ts (dev)
export const environment = {
  production: false,
  apiUrl: '/api',           // proxied to localhost:8000
  wsUrl: 'ws://localhost:8000/ws',
  sentryDsn: '',            // no Sentry in dev
  appVersion: 'dev',
};

// environments/environment.prod.ts
export const environment = {
  production: true,
  apiUrl: 'https://api.saasiq.com',
  wsUrl: 'wss://api.saasiq.com/ws',
  sentryDsn: 'https://xxx@sentry.io/yyy',
  appVersion: '1.0.0',
};
```

### 17.3 esbuild (Angular CLI Default Bundler)

No configuration needed — Angular CLI uses esbuild since v17:

- 3-4x faster builds than webpack
- Automatic code splitting per route
- Tree shaking built-in
- CSS minification built-in
- Source maps generated automatically

```bash
# Dev (with hot reload)
ng serve                    # esbuild dev server, ~200ms rebuilds

# Production build
ng build --configuration=production
# Outputs to dist/saasiq/browser/
# - index.html
# - main-[hash].js          (app shell + shared)
# - chunk-[hash].js          (per lazy-loaded route)
# - styles-[hash].css        (global styles)
# - media/inter-[hash].woff2 (font)
```

### 17.4 Cache Busting

Angular CLI adds content hashes to all output filenames automatically:
- `main-a1b2c3d4.js` — hash changes when code changes
- `styles-e5f6g7h8.css` — hash changes when styles change

Configure CDN/server to set long cache headers:
```
Cache-Control: public, max-age=31536000, immutable  (for hashed files)
Cache-Control: no-cache                              (for index.html only)
```

### 17.5 Feature Flags

Toggle features without deploying:

```typescript
// core/services/feature-flags.service.ts
@Injectable({ providedIn: 'root' })
export class FeatureFlagService {
  private flags = signal<Record<string, boolean>>({});

  async loadFlags() {
    const response = await fetch('/api/feature-flags');
    this.flags.set(await response.json());
  }

  isEnabled(flag: string): boolean {
    return this.flags()[flag] ?? false;
  }
}

// Usage in template
@if (featureFlags.isEnabled('ai-copilot-v2')) {
  <app-copilot-v2 />
} @else {
  <app-copilot-v1 />
}

// Usage in route guard
export const featureGuard = (flag: string): CanActivateFn => () => {
  return inject(FeatureFlagService).isEnabled(flag);
};

{ path: 'benchmarks', canActivate: [featureGuard('benchmarks')], loadComponent: () => ... }
```

---

## 18. Study Priority Roadmap

### Phase 1 — Before Writing Code (Week 1)

| # | Concept | Effort | Section |
|---|---------|--------|---------|
| 1 | Angular Signals (`signal`, `computed`, `effect`, `input`, `output`) | 1 day | §2.2 |
| 2 | Standalone Components & Composition patterns | 1 day | §1.4, §1.3 |
| 3 | Reactive Forms & Validation | 1 day | §11 |
| 4 | Angular Router (lazy loading, guards, nested outlets) | 1 day | §4 |
| 5 | OnPush Change Detection | Half day | §3.2 |

### Phase 2 — Before Backend Integration (Week 2-3)

| # | Concept | Effort | Section |
|---|---------|--------|---------|
| 6 | OAuth 2.0 + PKCE flow | 2 days | §9.1 |
| 7 | JWT lifecycle + refresh token rotation | 1 day | §9.2 |
| 8 | HTTP Interceptors (auth, error, logging) | 1 day | §7.3 |
| 9 | TanStack Query (queries, mutations, caching, invalidation) | 2 days | §7.2, §8 |
| 10 | CORS understanding | Half day | §9.4 |

### Phase 3 — Before AI Copilot & Real-Time (Week 4)

| # | Concept | Effort | Section |
|---|---------|--------|---------|
| 11 | SSE / Streaming Fetch (`ReadableStream`) | 1 day | §6.1 |
| 12 | WebSocket + rxjs/webSocket + reconnection | 1 day | §6.2 |
| 13 | AbortController (cancel streams) | Half day | §13.8 |

### Phase 4 — Before Production (Week 5+)

| # | Concept | Effort | Section |
|---|---------|--------|---------|
| 14 | Sentry setup + Global ErrorHandler | Half day | §14.1, §10.3 |
| 15 | Core Web Vitals + bundle analysis | 1 day | §15 |
| 16 | Testing (Jest + Angular Testing Library + Playwright) | 2 days | §16 |
| 17 | Accessibility (ARIA, focus management, keyboard) | 1 day | §12 |
| 18 | RBAC + XSS + CSP | 1 day | §9.3, §9.5 |

**Total: ~18 days of focused study across 5 weeks, interleaved with coding.**

---

## Quick Reference: What You Will Use (Full List)

| Category | Concepts |
|----------|----------|
| **Architecture** | Atomic Design, Smart/Dumb Components, Standalone Components, Content Projection, Template Outlets |
| **State** | Angular Signals, NgRx SignalStore, TanStack Query, Immutability, Optimistic Updates, State Persistence |
| **Performance** | Lazy Loading, OnPush, Virtual Scrolling, Debounce/Throttle, Tree Shaking, Bundle Splitting, Skeleton Screens |
| **Routing** | Lazy Routes, Guards (canActivate, canDeactivate, canMatch), Nested Outlets, URL as State, Preloading |
| **Theming** | Design Tokens, CSS Custom Properties, Dark Mode, Accent Colors, Density Modes, Responsive Breakpoints |
| **Real-Time** | SSE (AI streaming), WebSocket (alerts/live data), Webhooks (outgoing events) |
| **API Layer** | Service Abstraction, HTTP Interceptors, Request Deduplication, Pagination (offset + cursor) |
| **Caching** | TanStack Query Cache, localStorage, sessionStorage, HTTP Cache-Control, Cache Invalidation |
| **Security** | OAuth 2.0 + PKCE, JWT + Refresh Tokens, XSS Prevention, CSRF, CORS, RBAC, CSP |
| **Error Handling** | Three-State Pattern, Retry Logic, Global ErrorHandler, Graceful Degradation |
| **Forms** | Reactive Forms, Custom Validators, Inline Validation UX, Unsaved Changes Guard |
| **Accessibility** | Semantic HTML, Keyboard Navigation, Focus Trapping, ARIA Attributes, Color Contrast |
| **Browser APIs** | Clipboard, matchMedia, ResizeObserver, IntersectionObserver, localStorage, requestAnimationFrame, Notification API, AbortController |
| **Monitoring** | Sentry (errors + replay), Core Web Vitals, Bundle Analysis, Memory Leak Detection |
| **Testing** | Jest (unit), Angular Testing Library (component), Playwright (E2E), Visual Regression |
| **Build** | esbuild, Environment Config, Cache Busting, Feature Flags, CI/CD Pipeline |

---

## 19. Learning Resources — Videos, Docs & Courses

### 19.1 Angular Core (Signals, Standalone, Routing)

| Resource | Type | Topic | Link |
|----------|------|-------|------|
| **Angular Official Docs — Signals** | Docs | `signal()`, `computed()`, `effect()`, `input()`, `output()` | https://angular.dev/guide/signals |
| **Angular Official Docs — Standalone Components** | Docs | No-module architecture | https://angular.dev/guide/components |
| **Angular Official Docs — Routing** | Docs | Lazy loading, guards, nested routes | https://angular.dev/guide/routing |
| **Angular Official Docs — Reactive Forms** | Docs | FormBuilder, validators, reactive patterns | https://angular.dev/guide/forms/reactive-forms |
| **Angular Official Docs — HTTP Client** | Docs | HttpClient, interceptors, XSRF | https://angular.dev/guide/http |
| **Decoded Frontend — Angular Signals Deep Dive** | YouTube | Signals vs RxJS, when to use which | https://www.youtube.com/c/DecodedFrontend (search "Angular Signals") |
| **Joshua Morony — Angular Signals Course** | YouTube | Practical signals in real components | https://www.youtube.com/c/JoshuaMorony (search "Signals") |
| **Angular University — Angular Course** | Course | Full A-Z Angular (paid, very thorough) | https://angular-university.io |
| **Deborah Kurata — Angular Reactive Patterns** | YouTube | Signals + RxJS patterns in Angular | https://www.youtube.com/playlist?list=PLvbp8GpONmFU-N-2aMk2sP9k_IfEkfKGR |

---

### 19.2 State Management (Signals, NgRx SignalStore, TanStack Query)

| Resource | Type | Topic | Link |
|----------|------|-------|------|
| **NgRx SignalStore Official Docs** | Docs | `withState`, `withMethods`, `withComputed`, `patchState` | https://ngrx.io/guide/signals |
| **Alex Okrushko — NgRx SignalStore Intro** | YouTube | NgRx team lead explains SignalStore from scratch | https://www.youtube.com/watch?v=wl-0DQzfGDo |
| **Brandon Roberts — NgRx Signals Deep Dive** | YouTube | Advanced patterns: custom features, entity management | https://www.youtube.com/@BrandonRobertsDev |
| **TanStack Query Official Docs** | Docs | Queries, mutations, caching, invalidation | https://tanstack.com/query/latest/docs/framework/angular/overview |
| **TanStack Query — Practical React Examples** | YouTube | Same concepts apply to Angular adapter | https://www.youtube.com/watch?v=novnyCaa7To (Theo / Web Dev Simplified) |
| **Laith Academy — React Query Tutorial** | YouTube | Best conceptual explanation of staleTime, gcTime, invalidation (concepts identical in Angular) | https://www.youtube.com/watch?v=VtWkSCZX0Ec |

---

### 19.3 CSS, Tailwind & Design Systems

| Resource | Type | Topic | Link |
|----------|------|-------|------|
| **Tailwind CSS 4 Official Docs** | Docs | Utilities, config, dark mode, responsive | https://tailwindcss.com/docs |
| **Tailwind CSS Official YouTube** | YouTube | What's new in v4, migration | https://www.youtube.com/@TailwindLabs |
| **Kevin Powell — CSS Concepts** | YouTube | CSS custom properties, responsive design, grid, flexbox | https://www.youtube.com/@KevinPowell |
| **Design Tokens W3C Spec** | Docs | Understand the token standard | https://design-tokens.github.io/community-group/format/ |
| **Theo Browne — Tailwind v4 Deep Dive** | YouTube | What changed, new features | https://www.youtube.com/@t3dotgg (search "Tailwind v4") |
| **Josh Comeau — CSS for JS Developers** | Course | Deep CSS understanding (paid, excellent) | https://css-for-js.dev |
| **Every Layout** | Reference | Layout patterns (sidebar, stack, grid, cluster) | https://every-layout.dev |

---

### 19.4 Charts (Apache ECharts)

| Resource | Type | Topic | Link |
|----------|------|-------|------|
| **ECharts Official Docs** | Docs | All chart types, options, themes | https://echarts.apache.org/en/index.html |
| **ECharts Examples Gallery** | Interactive | Live editable examples for every chart type | https://echarts.apache.org/examples/en/ |
| **ngx-echarts GitHub** | Docs | Angular integration guide | https://github.com/xieziyu/ngx-echarts |
| **ECharts Theme Builder** | Tool | Create custom dark/light themes visually | https://echarts.apache.org/en/theme-builder.html |

---

### 19.5 Real-Time: WebSocket & SSE

| Resource | Type | Topic | Link |
|----------|------|-------|------|
| **MDN — WebSocket API** | Docs | Browser WebSocket API reference | https://developer.mozilla.org/en-US/docs/Web/API/WebSocket |
| **MDN — Server-Sent Events** | Docs | EventSource API, SSE format | https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events |
| **MDN — ReadableStream (Fetch streaming)** | Docs | Stream reading for SSE via fetch | https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream |
| **RxJS webSocket Docs** | Docs | `rxjs/webSocket` — WebSocket as Observable | https://rxjs.dev/api/webSocket/webSocket |
| **Fireship — WebSockets in 100 Seconds** | YouTube | Quick conceptual overview | https://www.youtube.com/watch?v=1BfCnjr_Vjg |
| **Fireship — Server-Sent Events** | YouTube | SSE explained simply | https://www.youtube.com/watch?v=4HlNv1qpZFY |
| **Hussein Nasser — WebSocket vs SSE vs Long Polling** | YouTube | When to use which, deep comparison | https://www.youtube.com/@haborProgramming (search "WebSocket vs SSE") |
| **The Coding Train — Working with Streams** | YouTube | ReadableStream / WritableStream practical usage | https://www.youtube.com/@TheCodingTrain |

---

### 19.6 Authentication & Security (OAuth 2.0, JWT, PKCE)

| Resource | Type | Topic | Link |
|----------|------|-------|------|
| **OAuth 2.0 Simplified (Aaron Parecki)** | Book/Web | Best plain-English explanation of OAuth flows | https://www.oauth.com |
| **Auth0 — OAuth 2.0 Authorization Code + PKCE** | Docs | SPA-specific OAuth flow with diagrams | https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow-with-pkce |
| **JWT.io** | Tool | Decode, verify, and learn JWT structure | https://jwt.io |
| **Fireship — JWT in 100 Seconds** | YouTube | Quick JWT overview | https://www.youtube.com/watch?v=UBUNrFtufWo |
| **Fireship — Session vs Token Authentication** | YouTube | When to use cookies vs JWT | https://www.youtube.com/watch?v=UBUNrFtufWo |
| **Ben Awad — OAuth 2.0 + PKCE Explained** | YouTube | Practical PKCE implementation walkthrough | Search "OAuth PKCE frontend" on YouTube |
| **MDN — Content Security Policy (CSP)** | Docs | CSP header configuration | https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP |
| **OWASP — XSS Prevention Cheat Sheet** | Docs | Comprehensive XSS prevention guide | https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Scripting_Prevention_Cheat_Sheet.html |
| **OWASP — CSRF Prevention Cheat Sheet** | Docs | CSRF token patterns | https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html |
| **MDN — CORS** | Docs | Complete CORS reference | https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS |
| **Academind — Angular Auth (JWT + Interceptors)** | YouTube | Full auth implementation in Angular | https://www.youtube.com/@academind (search "Angular Authentication") |

---

### 19.7 Caching & Performance

| Resource | Type | Topic | Link |
|----------|------|-------|------|
| **web.dev — Core Web Vitals** | Docs | LCP, INP, CLS — what they are, how to improve | https://web.dev/articles/vitals |
| **web.dev — HTTP Caching** | Docs | Cache-Control, ETag, stale-while-revalidate | https://web.dev/articles/http-cache |
| **Chrome DevTools — Performance Tab** | Docs | How to profile runtime performance | https://developer.chrome.com/docs/devtools/performance |
| **Angular Official — Performance Best Practices** | Docs | OnPush, lazy loading, trackBy, profiling | https://angular.dev/best-practices/runtime-performance |
| **source-map-explorer** | Tool | Visualize bundle contents | https://github.com/nicedoc/source-map-explorer |
| **Addy Osmani — Image Optimization** | Book | Every image optimization technique | https://web.dev/learn/images |
| **Jake Archibald — Caching Best Practices** | Article | Classic reference on HTTP caching | https://jakearchibald.com/2016/caching-best-practices/ |
| **Fireship — 10 Angular Performance Tips** | YouTube | Quick actionable tips | https://www.youtube.com/watch?v=I77bJCFCJyU |

---

### 19.8 Error Handling, Logging & Monitoring

| Resource | Type | Topic | Link |
|----------|------|-------|------|
| **Sentry Docs — Angular Setup** | Docs | `@sentry/angular` installation, ErrorHandler, source maps | https://docs.sentry.io/platforms/javascript/guides/angular/ |
| **Sentry — Session Replay Docs** | Docs | Record user sessions for debugging | https://docs.sentry.io/product/explore/session-replay/ |
| **web-vitals npm package** | Docs | Measure LCP, INP, CLS in code | https://github.com/nicedoc/web-vitals |
| **LogRocket Blog — Angular Error Handling** | Article | Patterns for global and local error handling | https://blog.logrocket.com/error-handling-angular/ |

---

### 19.9 Testing (Jest, Angular Testing Library, Playwright)

| Resource | Type | Topic | Link |
|----------|------|-------|------|
| **Angular Testing Library Official Docs** | Docs | `render()`, `screen`, user-centric testing | https://testing-library.com/docs/angular-testing-library/intro |
| **Playwright Official Docs** | Docs | E2E testing, locators, assertions, screenshots | https://playwright.dev/docs/intro |
| **Jest Official Docs** | Docs | Matchers, mocks, async testing | https://jestjs.io/docs/getting-started |
| **jest-preset-angular** | Docs | Jest configuration for Angular | https://github.com/nicedoc/jest-preset-angular |
| **Kent C. Dodds — Testing JavaScript** | Course | Testing philosophy that Testing Library is built on (paid) | https://testingjavascript.com |
| **Kent C. Dodds — Common Testing Mistakes** | Article | What NOT to test, how to write maintainable tests | https://kentcdodds.com/blog/common-mistakes-with-react-testing-library (concepts apply to Angular Testing Library) |
| **Playwright YouTube Channel** | YouTube | Official tutorials and tips | https://www.youtube.com/@Aboringtech |
| **Storybook Official Docs** | Docs | Component documentation, stories, interactions | https://storybook.js.org/docs |

---

### 19.10 Accessibility (a11y)

| Resource | Type | Topic | Link |
|----------|------|-------|------|
| **MDN — ARIA Roles, States, Properties** | Docs | Complete ARIA reference | https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA |
| **web.dev — Learn Accessibility** | Course | Free, structured a11y course | https://web.dev/learn/accessibility |
| **A11y Project Checklist** | Checklist | Quick accessibility audit checklist | https://www.a11yproject.com/checklist/ |
| **Angular CDK — a11y Module** | Docs | FocusTrap, LiveAnnouncer, FocusMonitor | https://material.angular.io/cdk/a11y/overview |
| **Rob Dodson — Accessibility Fundamentals** | YouTube | Google Chrome team a11y talks | https://www.youtube.com/playlist?list=PLNYkxOF6rcICWx0C9LVWWVqvHlYJyqw7g |
| **axe DevTools** | Tool | Browser extension for a11y auditing | https://www.deque.com/axe/devtools/ |
| **Stark / Colour Contrast Checker** | Tool | Check WCAG contrast ratios | https://colourcontrast.cc |

---

### 19.11 Browser APIs

| Resource | Type | Topic | Link |
|----------|------|-------|------|
| **MDN — Clipboard API** | Docs | `navigator.clipboard.writeText()` | https://developer.mozilla.org/en-US/docs/Web/API/Clipboard_API |
| **MDN — matchMedia** | Docs | System theme detection | https://developer.mozilla.org/en-US/docs/Web/API/Window/matchMedia |
| **MDN — ResizeObserver** | Docs | Observe element size changes | https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserver |
| **MDN — IntersectionObserver** | Docs | Lazy loading, scroll animations | https://developer.mozilla.org/en-US/docs/Web/API/IntersectionObserver |
| **MDN — Notifications API** | Docs | Browser push notifications | https://developer.mozilla.org/en-US/docs/Web/API/Notifications_API |
| **MDN — AbortController** | Docs | Cancel fetch requests | https://developer.mozilla.org/en-US/docs/Web/API/AbortController |
| **MDN — requestAnimationFrame** | Docs | Smooth animations | https://developer.mozilla.org/en-US/docs/Web/API/window/requestAnimationFrame |
| **MDN — Web Storage API** | Docs | localStorage / sessionStorage | https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API |
| **Jake Archibald — IntersectionObserver Explained** | Article | Best practical explanation | https://web.dev/articles/intersectionobserver |

---

### 19.12 Build, Deployment & DevOps

| Resource | Type | Topic | Link |
|----------|------|-------|------|
| **Angular CLI Official Docs** | Docs | ng new, ng build, angular.json, budgets | https://angular.dev/tools/cli |
| **esbuild Docs** | Docs | Understand the bundler Angular uses | https://esbuild.github.io |
| **Vercel Docs — Angular Deployment** | Docs | Deploy Angular to Vercel | https://vercel.com/guides/deploying-angular-with-vercel |
| **GitHub Actions — Angular CI/CD** | Docs | Lint → Test → Build → Deploy pipeline | https://docs.github.com/en/actions |
| **ESLint Official Docs** | Docs | Configuration, rules | https://eslint.org/docs/latest/ |
| **Prettier Docs** | Docs | Formatting config | https://prettier.io/docs/en/ |
| **Husky Docs** | Docs | Git hooks setup | https://typicode.github.io/husky/ |

---

### 19.13 Frontend System Design (Big Picture)

| Resource | Type | Topic | Link |
|----------|------|-------|------|
| **Frontend Masters — Enterprise Architecture with Angular** | Course | Large-scale Angular app architecture (paid) | https://frontendmasters.com (search "Angular") |
| **Nrwl/Nx — Angular Monorepo Guide** | Docs | Scaling architecture when team grows | https://nx.dev/getting-started/tutorials/angular-monorepo-tutorial |
| **roadmap.sh — Frontend Developer Roadmap** | Visual | Complete frontend learning path | https://roadmap.sh/frontend |
| **roadmap.sh — Angular Developer Roadmap** | Visual | Angular-specific learning path | https://roadmap.sh/angular |
| **GreatFrontEnd — System Design** | Course | Frontend system design interview prep (also great for learning) | https://www.greatfrontend.com/system-design |
| **Chirag Goel — Frontend System Design** | YouTube | Real-world frontend system design breakdowns | https://www.youtube.com/@aspect_ui (search "frontend system design") |
| **Namaste Frontend System Design** | YouTube | In-depth frontend system design series (Hindi + English) | https://www.youtube.com/@AkshaySaini (search "system design") |

---

### 19.14 YouTube Channels to Follow (Frontend + Angular)

| Channel | Focus | Why Follow |
|---------|-------|-----------|
| **Joshua Morony** | Angular Signals, architecture, state | Best pure-Angular content creator. Deep dives, practical code |
| **Decoded Frontend** | Angular internals, advanced patterns | Explains how Angular works under the hood |
| **Deborah Kurata** | Angular reactive patterns, signals | Clear explanations with simple examples |
| **Kevin Powell** | CSS, responsive design, modern CSS | CSS mastery — everything from grid to custom properties |
| **Fireship** | Quick concepts, 100-second explainers | Fast overviews of any web technology |
| **Theo (t3.gg)** | Frontend ecosystem, opinions, trends | Keeps you current on tooling changes |
| **Hussein Nasser** | Networking, WebSocket, HTTP, backend | Deep understanding of protocols frontend depends on |
| **Web Dev Simplified** | JavaScript fundamentals, patterns | Clean explanations of core concepts |
| **Jack Herrington** | React/frontend patterns (transferable) | Component patterns, state management concepts apply to Angular |
| **Academind** | Angular courses, auth, full projects | Complete project tutorials in Angular |

---

### 19.15 Documentation Bookmarks (Daily Reference)

Keep these open while building SaaSIQ:

| # | Bookmark | URL |
|---|----------|-----|
| 1 | Angular Docs | https://angular.dev |
| 2 | Tailwind CSS Docs | https://tailwindcss.com/docs |
| 3 | NgRx SignalStore | https://ngrx.io/guide/signals |
| 4 | TanStack Query Angular | https://tanstack.com/query/latest/docs/framework/angular/overview |
| 5 | ECharts Options | https://echarts.apache.org/en/option.html |
| 6 | Font Awesome Icons Search | https://fontawesome.com/search |
| 7 | Angular CDK | https://material.angular.io/cdk/categories |
| 8 | RxJS Operators | https://rxjs.dev/guide/operators |
| 9 | TypeScript Handbook | https://www.typescriptlang.org/docs/handbook/ |
| 10 | MDN Web Docs | https://developer.mozilla.org |
| 11 | Can I Use (browser support) | https://caniuse.com |
| 12 | Playwright Docs | https://playwright.dev |

---

### 19.16 Suggested Learning Order (With Resources Mapped)

| Week | What to Learn | Primary Resource | Practice With |
|------|--------------|-----------------|---------------|
| **Week 1** | Angular Signals + Standalone Components | Angular Docs + Joshua Morony YouTube | Build shared components (Badge, Button, KpiCard) |
| **Week 1** | Reactive Forms + Validation | Angular Docs | Build Login + Signup forms |
| **Week 1** | Angular Router (lazy, guards, nested) | Angular Docs | Set up all SaaSIQ routes |
| **Week 2** | Tailwind CSS 4 + Dark mode + Custom theme | Tailwind Docs + Kevin Powell | Migrate prototype design tokens to Tailwind config |
| **Week 2** | ECharts (line, donut, bar) | ECharts Examples Gallery | Build dashboard charts |
| **Week 3** | OAuth 2.0 + PKCE | oauth.com + Auth0 docs | Build Login with Google flow |
| **Week 3** | JWT + HTTP Interceptors | jwt.io + Academind YouTube | Build auth interceptor chain |
| **Week 3** | TanStack Query | TanStack Docs + Laith Academy YouTube | Connect dashboard to mock API |
| **Week 4** | NgRx SignalStore | NgRx Docs + Alex Okrushko YouTube | Build AppearanceStore + OrgStore |
| **Week 4** | SSE / Streaming Fetch | MDN ReadableStream + Fireship SSE | Build AI Copilot streaming |
| **Week 4** | WebSocket + reconnection | MDN WebSocket + RxJS webSocket docs | Build real-time alerts |
| **Week 5** | Sentry + Error handling | Sentry Angular docs | Set up global error tracking |
| **Week 5** | Jest + Angular Testing Library | Testing Library docs + Kent C. Dodds | Write tests for shared components |
| **Week 5** | Playwright E2E | Playwright docs | Write critical flow tests |
| **Week 5** | Accessibility | web.dev Learn Accessibility + axe DevTools | Audit and fix all components |

---

> **This document covers every frontend system design concept you will use to build SaaSIQ. Nothing is speculative — every concept maps to a real feature in the prototype.**
