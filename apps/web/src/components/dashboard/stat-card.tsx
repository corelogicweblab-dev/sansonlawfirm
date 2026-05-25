import { LucideIcon } from "lucide-react";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface StatCardProps {
  title: string;
  value: string | number;
  change?: string;
  icon: LucideIcon;
  trend?: "up" | "down" | "neutral";
}

export function StatCard({ title, value, change, icon: Icon, trend = "neutral" }: StatCardProps) {
  return (
    <Card className="relative overflow-hidden">
      <div className="absolute right-4 top-4 opacity-10">
        <Icon className="h-16 w-16 text-pink-500" />
      </div>
      <p className="text-sm text-[var(--muted)]">{title}</p>
      <p className="mt-2 text-3xl font-bold text-foreground">{value}</p>
      {change && (
        <p
          className={cn(
            "mt-1 text-xs",
            trend === "up" && "text-[var(--success)]",
            trend === "down" && "text-[var(--destructive)]",
            trend === "neutral" && "text-[var(--muted)]"
          )}
        >
          {change}
        </p>
      )}
    </Card>
  );
}
