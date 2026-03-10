import { cn } from "@/lib/utils";
import { AlertCircle } from "lucide-react";

interface ErrorMessageProps {
  className?: string;
  message?: string;
}

export function ErrorMessage({ className, message = "An error occurred." }: ErrorMessageProps) {
  return (
    <div
      className={cn(
        "flex items-center gap-3 rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700",
        className
      )}
    >
      <AlertCircle className="w-5 h-5 shrink-0" />
      <span>{message}</span>
    </div>
  );
}
