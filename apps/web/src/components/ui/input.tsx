import { cn } from "@/lib/utils";
import { InputHTMLAttributes, forwardRef } from "react";

export const Input = forwardRef<HTMLInputElement, InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => (
    <input
      ref={ref}
      className={cn(
        "w-full rounded-lg border border-pink-500/20 bg-white/5 px-4 py-2.5 text-sm text-foreground",
        "placeholder:text-muted focus:border-pink-500/50 focus:outline-none focus:ring-2 focus:ring-pink-500/20",
        "transition-all duration-200",
        className
      )}
      {...props}
    />
  )
);
Input.displayName = "Input";
