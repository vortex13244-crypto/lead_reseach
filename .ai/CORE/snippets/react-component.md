# Snippet: React Component

> **Purpose:** Production-ready React component templates for common use cases.
> **Related:** [../knowledge/react.md](../knowledge/react.md) · [../knowledge/typescript.md](../knowledge/typescript.md)

---

## Basic Component

```tsx
// src/components/ui/[component-name].tsx
import { cn } from "@/lib/utils"
import { forwardRef } from "react"

interface ComponentNameProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "outlined" | "ghost"
  size?: "sm" | "md" | "lg"
}

const ComponentName = forwardRef<HTMLDivElement, ComponentNameProps>(
  ({ className, variant = "default", size = "md", children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          "rounded-md",
          {
            "bg-primary text-primary-foreground": variant === "default",
            "border border-border": variant === "outlined",
            "bg-transparent": variant === "ghost",
          },
          {
            "px-2 py-1 text-sm": size === "sm",
            "px-4 py-2 text-base": size === "md",
            "px-6 py-3 text-lg": size === "lg",
          },
          className
        )}
        {...props}
      >
        {children}
      </div>
    )
  }
)
ComponentName.displayName = "ComponentName"

export { ComponentName }
export type { ComponentNameProps }
```

---

## Data Table Component

```tsx
// src/components/features/[feature]/[feature]-table.tsx
"use client"

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { MoreHorizontal } from "lucide-react"

interface User {
  id: string
  name: string
  email: string
  status: "active" | "inactive"
  createdAt: string
}

interface UserTableProps {
  users: User[]
  onEdit: (id: string) => void
  onDelete: (id: string) => void
}

export function UserTable({ users, onEdit, onDelete }: UserTableProps) {
  if (users.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-muted-foreground">
        <p className="text-sm">No users found</p>
      </div>
    )
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Name</TableHead>
          <TableHead>Email</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>Created</TableHead>
          <TableHead className="w-[50px]" />
        </TableRow>
      </TableHeader>
      <TableBody>
        {users.map((user) => (
          <TableRow key={user.id}>
            <TableCell className="font-medium">{user.name}</TableCell>
            <TableCell>{user.email}</TableCell>
            <TableCell>
              <Badge variant={user.status === "active" ? "default" : "secondary"}>
                {user.status}
              </Badge>
            </TableCell>
            <TableCell className="text-muted-foreground">
              {new Date(user.createdAt).toLocaleDateString()}
            </TableCell>
            <TableCell>
              <Button variant="ghost" size="icon" onClick={() => onEdit(user.id)}>
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

---

## Form Component

```tsx
// src/components/features/[feature]/[feature]-form.tsx
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Button } from "@/components/ui/button"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { toast } from "sonner"

const formSchema = z.object({
  name: z.string().min(1, "Name is required").max(100),
  email: z.string().email("Invalid email address"),
})

type FormValues = z.infer<typeof formSchema>

interface UserFormProps {
  defaultValues?: Partial<FormValues>
  onSubmit: (values: FormValues) => Promise<void>
}

export function UserForm({ defaultValues, onSubmit }: UserFormProps) {
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: { name: "", email: "", ...defaultValues },
  })

  const handleSubmit = async (values: FormValues) => {
    try {
      await onSubmit(values)
      toast.success("Saved successfully")
    } catch (error) {
      toast.error("Failed to save. Please try again.")
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input placeholder="John Doe" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input type="email" placeholder="john@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" disabled={form.formState.isSubmitting}>
          {form.formState.isSubmitting ? "Saving..." : "Save"}
        </Button>
      </form>
    </Form>
  )
}
```

---

## Custom Hook

```tsx
// src/hooks/use-[resource].ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"

interface User {
  id: string
  name: string
  email: string
}

async function fetchUsers(): Promise<User[]> {
  const res = await fetch("/api/v1/users")
  if (!res.ok) throw new Error("Failed to fetch users")
  const { data } = await res.json()
  return data
}

async function deleteUser(id: string): Promise<void> {
  const res = await fetch(`/api/v1/users/${id}`, { method: "DELETE" })
  if (!res.ok) throw new Error("Failed to delete user")
}

export function useUsers() {
  const queryClient = useQueryClient()

  const query = useQuery({
    queryKey: ["users"],
    queryFn: fetchUsers,
    staleTime: 5 * 60 * 1000,  // 5 minutes
  })

  const deleteMutation = useMutation({
    mutationFn: deleteUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] })
      toast.success("User deleted")
    },
    onError: () => {
      toast.error("Failed to delete user")
    },
  })

  return {
    users: query.data ?? [],
    isLoading: query.isLoading,
    error: query.error,
    deleteUser: deleteMutation.mutate,
    isDeletingUser: deleteMutation.isPending,
  }
}
```
