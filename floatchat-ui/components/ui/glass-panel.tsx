import { type MotionProps, motion } from "framer-motion"
import { cn } from "@/lib/utils"

interface GlassPanelProps extends React.HTMLAttributes<HTMLDivElement> {
    children: React.ReactNode
    variant?: "base" | "subtle"
    hoverEffect?: boolean
}

export function GlassPanel({
    children,
    className,
    variant = "base",
    hoverEffect = false,
    ...props
}: GlassPanelProps) {
    return (
        <div
            className={cn(
                "rounded-xl transition-all duration-300",
                variant === "base" && "border border-white/[0.08] bg-black/40 backdrop-blur-xl shadow-[0_4px_24px_-1px_rgba(0,0,0,0.2)]",
                variant === "subtle" && "border border-white/[0.04] bg-white/[0.02]",
                hoverEffect && "hover:bg-white/[0.04] hover:border-white/[0.12] hover:shadow-[0_8px_32px_-4px_rgba(0,0,0,0.3)] cursor-pointer group",
                className
            )}
            {...props}
        >
            {children}
        </div>
    )
}
