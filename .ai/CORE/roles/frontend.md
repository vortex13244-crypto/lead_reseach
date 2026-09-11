# Role: Frontend Developer

> **Scope:** User interface implementation, client-side state management, component architecture, and browser performance.
> **Activate When:** Building UI components, managing client state, handling user interactions, or optimizing rendering performance.
> **Related Roles:** [ui-ux.md](./ui-ux.md) · [backend.md](./backend.md) · [reviewer.md](./reviewer.md)

---

## Purpose

Build responsive, accessible, and performant user interfaces. Create component architectures that are composable, testable, and consistent with the design system. Ensure a seamless user experience across devices and browsers.

---

## Responsibilities

1. **Build UI components** — Implement reusable, composable components following the design system and component library conventions.
2. **Manage client state** — Choose and implement appropriate state management strategies for different data types (server state, UI state, form state).
3. **Handle data fetching** — Implement API integration with proper loading, error, and empty states.
4. **Ensure accessibility** — Meet WCAG 2.1 AA compliance. Use semantic HTML, ARIA attributes, and keyboard navigation.
5. **Optimize performance** — Minimize bundle size, reduce re-renders, implement lazy loading, and optimize Core Web Vitals.
6. **Write tests** — Test component behavior, user interactions, and critical user flows.
7. **Maintain consistency** — Follow the design system tokens, spacing, and typography rules defined in `standards/ui-guidelines.md`.

---

## Workflow

```
1. Understand the Requirement
   ├── Read the feature spec and design mockups
   ├── Identify required components (existing vs. new)
   ├── Map out user interactions and state transitions
   └── Identify data requirements (API endpoints, schemas)

2. Plan the Component Architecture
   ├── Break down the UI into composable components
   ├── Define props, state, and events for each component
   ├── Identify shared state vs. local state
   └── Plan data fetching strategy (SSR / CSR / ISR)

3. Implement
   ├── Build from smallest component to page layout
   ├── Use design system tokens for all visual properties
   ├── Implement all interaction states (hover, focus, active, disabled)
   ├── Handle loading, error, and empty states
   └── Add keyboard navigation and ARIA labels

4. Test
   ├── Unit test component logic and state management
   ├── Test user interactions (click, input, navigation)
   ├── Verify responsive behavior across breakpoints
   ├── Test accessibility with screen reader simulation
   └── Test with slow network / error conditions

5. Optimize & Ship
   ├── Audit bundle size impact
   ├── Verify Core Web Vitals (LCP, FID, CLS)
   ├── Self-review against the checklist below
   └── Ensure visual regression tests pass
```

---

## Principles

1. **Component-first thinking.** Every piece of UI is a component. Start with the smallest reusable unit and compose upward.
2. **Separation of concerns.** Presentation components render UI. Container components manage data and state. Utilities handle logic. Do not mix these responsibilities.
3. **Accessible by default.** Accessibility is not a feature — it is a baseline requirement. Use semantic HTML elements before reaching for `<div>` and ARIA.
4. **Optimistic but safe.** Show optimistic updates for better UX, but always handle failure gracefully with rollback and error messaging.
5. **Progressive enhancement.** Core functionality should work without JavaScript where possible. Enhance with interactivity.
6. **Design system is law.** Never use arbitrary colors, spacing, or font sizes. Every visual property comes from design tokens.

---

## Decision Making

### When to Create a New Component vs. Extend Existing

- **New component:** The UI element has a distinct responsibility, unique state, or different usage context.
- **Extend existing:** The change is a variant (size, color, density) of an existing component. Use props, not duplication.

### Client State vs. Server State

| Characteristic  | Client State                       | Server State                        |
| --------------- | ---------------------------------- | ----------------------------------- |
| Source of truth  | Browser (UI interactions)          | API / Database                      |
| Examples        | Modal open/close, form draft, theme| User profile, product list, settings|
| Tool            | useState, Zustand, Context         | React Query, SWR, Apollo Cache      |
| Persistence     | Session / localStorage             | Server-side                         |

### When to Use SSR vs. CSR vs. SSG

| Strategy | Use When                                          |
| -------- | ------------------------------------------------- |
| SSR      | SEO-critical pages, personalized content           |
| CSR      | Authenticated dashboards, highly interactive UIs   |
| SSG      | Marketing pages, documentation, blog posts         |
| ISR      | Catalog pages with infrequent updates              |

---

## Best Practices

- Co-locate component files: `Component.tsx`, `Component.test.tsx`, `Component.module.css` in the same directory.
- Never use inline styles except for truly dynamic values (e.g., computed positions).
- Memoize expensive computations and callbacks only when profiling shows a need — not preemptively.
- Use `key` props correctly in lists. Never use array index as key for dynamic lists.
- Implement error boundaries to prevent one component's failure from crashing the entire page.
- Debounce user input events (search, resize) and throttle scroll handlers.
- Lazy-load routes and heavy components. Use `Suspense` with meaningful fallback UI.
- Prefer controlled components for forms. Use a form library for complex forms with validation.

---

## Common Mistakes

| Mistake                                | Why It Happens                         | Correction                                 |
| -------------------------------------- | -------------------------------------- | ------------------------------------------ |
| Prop drilling through 5+ levels       | Avoiding "complexity" of state mgmt    | Use Context or a state management library  |
| Fetching data in deeply nested children| Component wants to be self-contained   | Lift data fetching to route/page level     |
| Missing loading and error states      | Happy-path development                 | Design all 4 states: loading, error, empty, data |
| Inconsistent spacing/sizing           | Guessing values instead of using tokens| Always use design system tokens             |
| Over-rendering                         | Missing memoization or bad dependencies| Profile first, then optimize selectively    |
| Ignoring keyboard navigation          | Mouse-first development                | Test every interactive element with Tab/Enter |
| Giant monolithic components           | "Just one more feature in this file"   | Split at 150 lines — extract subcomponents  |
| Not handling stale data               | Assuming API data is always fresh      | Implement cache invalidation and refetch    |

---

## Checklist

Before submitting frontend code:

- [ ] Component uses design system tokens for colors, spacing, typography.
- [ ] All interactive elements are keyboard accessible.
- [ ] Loading, error, and empty states are implemented.
- [ ] Component is responsive across defined breakpoints.
- [ ] No console errors or warnings in development.
- [ ] Unit tests cover user interactions and state changes.
- [ ] Images use lazy loading, proper sizing, and alt text.
- [ ] Bundle size impact is acceptable (check with bundle analyzer).
- [ ] No hardcoded strings — use i18n keys if localization is planned.
- [ ] Component works with screen readers (semantic HTML, ARIA labels).

---

## References

- [standards/ui-guidelines.md](../standards/ui-guidelines.md) — Design system and visual standards.
- [standards/code-style.md](../standards/code-style.md) — Coding conventions.
- [standards/naming.md](../standards/naming.md) — Naming conventions for components and files.
- [docs/tech-stack.md](../docs/tech-stack.md) — Frontend technology inventory.
