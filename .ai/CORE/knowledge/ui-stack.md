# shadcn/ui & UI Stack — Knowledge Base

> **Purpose:** When to use each UI library, compatibility notes, and best practices.
> **Related:** [react.md](react.md) · [../standards/ui-guidelines.md](../standards/ui-guidelines.md)

---

## UI Stack Overview

| Library | Role | Priority |
|---------|------|----------|
| **shadcn/ui** | Functional components (forms, tables, dialogs, nav) | Primary — use first |
| **MagicUI** | Animations, decorative effects, visual flair | Secondary — enhance with this |
| **Tailwind CSS** | All layout, spacing, color, responsive | Always |
| **Lucide React** | Icons | Default icon library |
| **Framer Motion** | Complex custom animations | When MagicUI isn't enough |

---

## shadcn/ui

### Overview

shadcn/ui is not a traditional component library — it copies component code into your project, giving you full control. Built on Radix UI primitives for accessibility.

### When to Use shadcn/ui

✅ **Use for:**
- All functional UI: forms, buttons, inputs, selects, checkboxes
- Navigation: menus, sidebars, breadcrumbs, tabs
- Overlays: dialogs, sheets, popovers, tooltips, dropdowns
- Data display: tables, cards, badges, avatars
- Feedback: toasts (Sonner), alerts, progress bars
- Layout: separators, scroll areas, aspect ratios

❌ **Do NOT use shadcn/ui when:**
- You need complex animations or visual effects → use MagicUI
- The component doesn't exist in shadcn → build custom with Radix UI directly
- The design heavily diverges from shadcn's aesthetic → build custom

### Installation & Usage

```bash
# Initialize (once per project)
npx shadcn@latest init

# Add components as needed (NOT all at once)
npx shadcn@latest add button
npx shadcn@latest add form
npx shadcn@latest add dialog
npx shadcn@latest add table
npx shadcn@latest add toast
```

### Best Practices

```tsx
// ✅ Extend components via className, don't modify the source
<Button className="bg-brand hover:bg-brand/90">Custom CTA</Button>

// ✅ Use the Form component for all forms (integrates with react-hook-form)
<Form {...form}>
  <FormField
    control={form.control}
    name="email"
    render={({ field }) => (
      <FormItem>
        <FormLabel>Email</FormLabel>
        <FormControl><Input {...field} /></FormControl>
        <FormMessage />
      </FormItem>
    )}
  />
</Form>

// ✅ Use Sheet for mobile sidebars, Dialog for modals
// ✅ Use Command for search palettes
// ✅ Use Sonner for toast notifications (not the built-in Toast)
```

### Compatibility

- **React:** 18+
- **Next.js:** 13+ (App Router and Pages Router)
- **Tailwind:** v3.4+
- **TypeScript:** Full support

---

## MagicUI

### Overview

MagicUI provides animated components and effects built on Framer Motion. Use it to add visual polish on top of shadcn/ui.

### When to Use MagicUI

✅ **Use for:**
- Hero section animations (animated text, particles, beams)
- Loading states with visual flair
- Card hover effects
- Number counters, shimmer effects
- Backgrounds (animated gradient, grid, dot patterns)
- Transition animations between states

❌ **Do NOT use MagicUI when:**
- You need a functional component (form, table, input) → use shadcn/ui
- Performance is critical and animations would reduce it → skip animations
- Users have `prefers-reduced-motion` set → always respect this

### Usage

```tsx
// Animated text reveal
import { AnimatedGradientText } from "@/components/magicui/animated-gradient-text"
import { BorderBeam } from "@/components/magicui/border-beam"
import { SparklesText } from "@/components/magicui/sparkles-text"

// Card with beam effect
<div className="relative overflow-hidden rounded-xl border bg-card p-6">
  <BorderBeam duration={6} />
  <h3>Premium Feature</h3>
</div>

// Always respect reduced motion
import { useReducedMotion } from "framer-motion"
const shouldReduce = useReducedMotion()

<motion.div
  animate={shouldReduce ? {} : { y: [0, -10, 0] }}
  transition={{ duration: 2, repeat: Infinity }}
>
```

### Compatibility

- **React:** 18+
- **Framer Motion:** 11+
- **Tailwind:** v3+
- Works alongside shadcn/ui

---

## Tailwind CSS

### Core Principles

```tsx
// Mobile-first responsive design
<div className="text-sm md:text-base lg:text-lg">
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

// Use semantic design tokens, not raw values
// ✅ bg-background, text-foreground, border-border (from CSS variables)
// ❌ bg-white, text-gray-900 (hardcoded, breaks dark mode)

// Dark mode via class strategy
// Add 'dark' class to <html> via next-themes
<div className="bg-white dark:bg-gray-900">
```

### Custom Design Tokens (globals.css)

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --border: 214.3 31.8% 91.4%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    /* ... */
  }
}
```

---

## Architecture Decision: When to Use Which Library

```
User needs a button?
  → shadcn/ui <Button>

User needs an animated hero headline?
  → MagicUI <SparklesText> or <AnimatedGradientText>

User needs a data table with sorting and pagination?
  → shadcn/ui <DataTable> + TanStack Table

User needs a page transition?
  → Framer Motion <AnimatePresence> or MagicUI page transitions

User needs a complex custom component not in shadcn?
  → Build with Radix UI primitive + Tailwind + Framer Motion

User needs an icon?
  → Lucide React
```

---

## Resources

- [shadcn/ui Docs](https://ui.shadcn.com)
- [MagicUI Docs](https://magicui.design)
- [Radix UI Docs](https://www.radix-ui.com)
- [Framer Motion](https://www.framer.com/motion/)
- [Lucide Icons](https://lucide.dev)
- [tweakcn](https://tweakcn.com) — Visual shadcn theme customizer
