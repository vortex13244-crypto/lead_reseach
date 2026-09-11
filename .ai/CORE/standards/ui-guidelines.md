# UI Guidelines

> **Scope:** Visual design system, spacing, typography, component patterns, accessibility, and responsive design.
> **Audience:** AI agents building or reviewing frontend interfaces.
> **Related:** [../roles/ui-ux.md](../roles/ui-ux.md) · [../roles/frontend.md](../roles/frontend.md) · [code-style.md](./code-style.md)

---

## 1. Design System

### Design Tokens

Design tokens are the single source of truth for all visual properties. Never use arbitrary values.

#### Color Palette

```
--color-primary-50:     /* Lightest tint */
--color-primary-100:
--color-primary-200:
--color-primary-300:
--color-primary-400:
--color-primary-500:    /* Base primary color */
--color-primary-600:
--color-primary-700:
--color-primary-800:
--color-primary-900:    /* Darkest shade */

--color-neutral-0:      /* White */
--color-neutral-50:
--color-neutral-100:
--color-neutral-200:
--color-neutral-300:
--color-neutral-400:
--color-neutral-500:
--color-neutral-600:
--color-neutral-700:
--color-neutral-800:
--color-neutral-900:    /* Near-black */

--color-success:        /* Green — confirmations, success states */
--color-warning:        /* Amber — caution, non-critical alerts */
--color-error:          /* Red — errors, destructive actions */
--color-info:           /* Blue — informational messages */
```

#### Semantic Color Assignments

| Token                  | Usage                              |
| ---------------------- | ---------------------------------- |
| `--color-text-primary` | Primary body text                  |
| `--color-text-secondary`| Secondary/muted text             |
| `--color-text-inverse` | Text on dark backgrounds           |
| `--color-bg-primary`   | Primary background                 |
| `--color-bg-secondary` | Card/section backgrounds           |
| `--color-bg-elevated`  | Modals, dropdowns, popovers        |
| `--color-border`       | Default border color               |
| `--color-border-focus` | Focus ring color                   |
| `--color-interactive`  | Links, clickable text              |
| `--color-interactive-hover` | Hover state for interactive elements |

---

## 2. Spacing

### Spacing Scale (8px Base Grid)

| Token   | Value  | Usage                              |
| ------- | ------ | ---------------------------------- |
| `--sp-1`| 4px    | Tight spacing (icon-to-text gap)   |
| `--sp-2`| 8px    | Default inline spacing             |
| `--sp-3`| 12px   | Small component padding            |
| `--sp-4`| 16px   | Default component padding          |
| `--sp-5`| 20px   | Medium spacing                     |
| `--sp-6`| 24px   | Section padding                    |
| `--sp-8`| 32px   | Large spacing between sections     |
| `--sp-10`| 40px  | Extra-large spacing                |
| `--sp-12`| 48px  | Page-level spacing                 |
| `--sp-16`| 64px  | Major section separation           |

### Spacing Rules

- Use the spacing scale exclusively. No arbitrary pixel values.
- Components use `--sp-3` to `--sp-6` for internal padding.
- Sections use `--sp-8` to `--sp-16` for vertical separation.
- Form fields use `--sp-4` vertical gap between fields and `--sp-2` between label and input.

---

## 3. Typography

### Type Scale

| Token           | Size   | Line Height | Weight  | Usage                      |
| --------------- | ------ | ----------- | ------- | -------------------------- |
| `--text-xs`     | 12px   | 16px        | Regular | Captions, metadata         |
| `--text-sm`     | 14px   | 20px        | Regular | Secondary text, labels     |
| `--text-base`   | 16px   | 24px        | Regular | Body text (default)        |
| `--text-lg`     | 18px   | 28px        | Medium  | Emphasized body text       |
| `--text-xl`     | 20px   | 28px        | Semibold| Section headings (h3)      |
| `--text-2xl`    | 24px   | 32px        | Semibold| Page section headings (h2) |
| `--text-3xl`    | 30px   | 36px        | Bold    | Page titles (h1)           |
| `--text-4xl`    | 36px   | 40px        | Bold    | Hero headings              |

### Typography Rules

- Use `--text-base` (16px) as the minimum body text size. Never go below 12px.
- Limit to 2 font families maximum: one for headings, one for body (or a single family for both).
- Line length: 45–75 characters per line for body text. Use `max-width` to constrain.
- Heading hierarchy: One `<h1>` per page. Follow sequential order: h1 → h2 → h3. Never skip levels.
- Use font weight for emphasis, not font size. Use bold (`600`–`700`) sparingly.

---

## 4. Components

### Component States

Every interactive component must support these states:

| State      | Visual Treatment                                |
| ---------- | ----------------------------------------------- |
| Default    | Base appearance                                 |
| Hover      | Subtle background change or underline           |
| Focus      | Visible focus ring (2px solid, offset 2px)      |
| Active     | Pressed/depressed visual (darker bg, slight scale) |
| Disabled   | Reduced opacity (0.5), no pointer events         |
| Loading    | Spinner or skeleton, disabled interaction        |
| Error      | Red border, error message below                  |

### Button Hierarchy

| Variant    | Usage                              | Visual                              |
| ---------- | ---------------------------------- | ----------------------------------- |
| Primary    | Main action (1 per view)           | Solid background, high contrast     |
| Secondary  | Alternative actions                | Outlined or muted background        |
| Tertiary   | Low-emphasis actions               | Text-only, no background            |
| Destructive| Delete, remove, irreversible       | Red variant of primary              |

### Form Component Rules

- Labels above inputs (not placeholder-only — placeholders disappear on focus).
- Error messages below the input field, in `--color-error`, with `--text-sm`.
- Required fields marked with an asterisk (`*`) in the label.
- Disabled inputs show a clear visual distinction (muted background).
- Group related fields with `<fieldset>` and `<legend>`.

### Modal / Dialog Rules

- Maximum width: 480px for confirmation, 640px for forms, 800px for complex content.
- Always include a visible close button (top-right `✕`).
- Trap focus within the modal when open. Return focus to trigger on close.
- Clicking the backdrop or pressing `Escape` closes the modal.
- Destructive confirmations require explicit action text ("Delete Project"), not generic ("OK").

---

## 5. Accessibility

### WCAG 2.1 AA Requirements

| Criterion                    | Requirement                               |
| ---------------------------- | ----------------------------------------- |
| Color contrast (text)        | ≥ 4.5:1 for normal text, ≥ 3:1 for large |
| Color contrast (UI)          | ≥ 3:1 for interactive elements            |
| Focus visibility             | All focusable elements have visible focus  |
| Keyboard navigation          | All functionality available via keyboard   |
| Touch target size            | ≥ 44 × 44px                               |
| Alternative text             | All images have descriptive `alt` text     |
| Form labels                  | All inputs have associated `<label>`       |
| Error identification         | Errors identified by more than color alone |

### Implementation Checklist

- Use semantic HTML: `<button>`, `<nav>`, `<main>`, `<article>`, `<aside>`, `<header>`, `<footer>`.
- Add ARIA labels only when semantic HTML is insufficient.
- Do not rely on color alone to convey information (add icons, text, or patterns).
- Ensure all images, icons, and media have text alternatives.
- Test with keyboard only: Tab, Shift+Tab, Enter, Escape, Arrow keys.
- Provide skip navigation link for keyboard users.
- Ensure screen reader announces dynamic content changes (`aria-live`).

---

## 6. Responsiveness

### Breakpoints

| Token          | Width    | Target                        |
| -------------- | -------- | ----------------------------- |
| `--bp-mobile`  | 0–639px  | Mobile phones                 |
| `--bp-tablet`  | 640–1023px | Tablets, small laptops       |
| `--bp-desktop` | 1024–1279px | Standard desktops           |
| `--bp-wide`    | 1280px+  | Large monitors                |

### Responsive Rules

- Design mobile-first: base styles target mobile, then enhance with `min-width` media queries.
- Content should be readable and usable at every breakpoint. No horizontal scrolling on body.
- Navigation: use hamburger menu on mobile, horizontal nav on desktop.
- Tables: use horizontal scroll container or card layout on mobile. Do not shrink text below readable sizes.
- Images: use `srcset` and `sizes` for responsive images. Set `max-width: 100%`.
- Touch interfaces: increase spacing between interactive elements. Thumb-friendly placement for primary actions.

### Layout Patterns

| Pattern           | Mobile              | Tablet                | Desktop               |
| ----------------- | ------------------- | --------------------- | --------------------- |
| Content width     | Full width (padding)| Max 720px centered    | Max 1200px centered   |
| Grid columns      | 1 column            | 2 columns             | 3–4 columns           |
| Sidebar           | Hidden / drawer     | Collapsible            | Persistent            |
| Navigation        | Bottom bar / burger | Top bar               | Top bar / sidebar     |
| Modal             | Full screen         | Centered, max 640px   | Centered, max 640px   |

---

## Quick Reference

### Do

- Use design tokens for all visual properties.
- Support all interactive states (hover, focus, active, disabled).
- Test at every breakpoint.
- Provide visible focus indicators.
- Use semantic HTML elements.

### Don't

- Use arbitrary pixel values for spacing, sizing, or color.
- Hide functionality behind hover-only interactions (no hover on touch).
- Skip heading levels.
- Use placeholder text as the only label.
- Disable zoom/pinch on mobile.
