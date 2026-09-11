# Checklist: Frontend

> **Purpose:** Frontend quality verification checklist for features and releases.
> **Related:** [roles/frontend.md](../roles/frontend.md) · [roles/ui-ux.md](../roles/ui-ux.md) · [standards/ui-guidelines.md](../standards/ui-guidelines.md)

---

## Component Quality

- [ ] Component has a single, clear responsibility
- [ ] Props are typed with TypeScript (no `any`)
- [ ] Component handles all data states:
  - [ ] Loading state: skeleton or spinner shown
  - [ ] Empty state: meaningful empty state, not blank screen
  - [ ] Error state: error message with recovery action
  - [ ] Success state: intended content shown correctly
- [ ] No hardcoded colors, sizes, or spacing (use design tokens)
- [ ] No business logic in components (logic in hooks or services)

---

## Design System

- [ ] Components use shadcn/ui where applicable
- [ ] Animations use MagicUI or Tailwind transitions
- [ ] Follows color tokens from `standards/ui-guidelines.md`
- [ ] Follows spacing scale (4/8/12/16/24/32/48/64px)
- [ ] Typography uses defined type scale
- [ ] Icons from Lucide React (or configured icon library)

---

## Responsive Design

- [ ] Layout works on mobile (375px width)
- [ ] Layout works on tablet (768px width)
- [ ] Layout works on desktop (1280px+ width)
- [ ] No horizontal overflow/scroll on mobile
- [ ] Touch targets ≥ 44×44px
- [ ] Images scale correctly at all sizes

---

## Accessibility (WCAG 2.1 AA)

- [ ] Color contrast ≥ 4.5:1 for normal text
- [ ] Color contrast ≥ 3:1 for large text and UI components
- [ ] All images have `alt` text (or `alt=""` if decorative)
- [ ] All form inputs have associated `<label>`
- [ ] Interactive elements are keyboard accessible (Tab, Enter, Space)
- [ ] Focus visible on all interactive elements
- [ ] ARIA labels on icon-only buttons
- [ ] Modal dialogs trap focus and return focus on close
- [ ] Error messages are announced to screen readers

---

## Performance

- [ ] Images use `next/image` (or lazy loading equivalent)
- [ ] Large components are lazy-loaded with `dynamic()`
- [ ] No unnecessary re-renders (check React DevTools)
- [ ] No memory leaks (event listeners removed, subscriptions cleaned up)
- [ ] `useEffect` dependencies are correct (no stale closures)

---

## User Experience

- [ ] Actions have immediate visual feedback (loading, disabled state)
- [ ] Errors are user-friendly (not raw error codes or stack traces)
- [ ] Success states are confirmed (toast, redirect, or visual update)
- [ ] Destructive actions require confirmation
- [ ] Forms can be submitted with keyboard (Enter in last field)
- [ ] Back navigation works as expected

---

## Code Quality

- [ ] No inline styles (use Tailwind classes)
- [ ] No prop drilling deeper than 2 levels (use context or Zustand)
- [ ] Keys in lists are stable and unique (not array index)
- [ ] `useEffect`, `useMemo`, `useCallback` used correctly
- [ ] Component files ≤ 300 lines

---

## Testing

- [ ] Component tests written for complex components
- [ ] All interactive states tested
- [ ] `data-testid` attributes added for E2E tests

---

*Related: [roles/frontend.md](../roles/frontend.md) · [standards/ui-guidelines.md](../standards/ui-guidelines.md)*
