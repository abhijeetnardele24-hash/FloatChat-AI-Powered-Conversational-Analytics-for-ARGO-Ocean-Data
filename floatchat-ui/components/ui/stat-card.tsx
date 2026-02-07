'use client'

import { motion } from 'framer-motion'
import { LucideIcon } from 'lucide-react'
import { cn } from '@/lib/utils'

interface StatCardProps {
    title: string
    value: string | number
    change?: string
    changeType?: 'positive' | 'negative' | 'neutral'
    icon?: LucideIcon
    delay?: number
}

export function StatCard({ title, value, change, changeType = 'neutral', icon: Icon, delay = 0 }: StatCardProps) {
    const gradients = {
        positive: 'from-emerald-500 to-teal-500',
        negative: 'from-red-500 to-orange-500',
        neutral: 'from-blue-500 to-cyan-500'
    }

    return (
        <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ delay, duration: 0.5, type: "spring", bounce: 0.3 }}
            whileHover={{ scale: 1.05, y: -10 }}
            className="group relative"
        >
            {/* Glow Effect */}
            <div className="absolute -inset-0.5 bg-gradient-to-r from-primary to-secondary rounded-3xl blur-lg opacity-30 group-hover:opacity-60 transition-opacity" />

            <div className="relative h-full glass-panel rounded-3xl p-8 transition-all duration-300 hover:shadow-2xl">
                {/* Animated Background Gradient */}
                <div className="absolute inset-0 bg-gradient-to-br from-primary/10 to-secondary/10 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity" />

                <div className="relative z-10 flex flex-col h-full">
                    <div className="flex items-start justify-between mb-6">
                        <p className="text-sm font-bold text-muted-foreground tracking-wider uppercase">{title}</p>
                        {Icon && (
                            <motion.div
                                whileHover={{ rotate: 360 }}
                                transition={{ duration: 0.6 }}
                                className={cn("p-3 rounded-2xl bg-gradient-to-br shadow-lg", gradients[changeType])}
                            >
                                <Icon size={22} className="text-white" strokeWidth={2.5} />
                            </motion.div>
                        )}
                    </div>

                    <div className="mt-auto">
                        <motion.p
                            initial={{ scale: 0.5 }}
                            animate={{ scale: 1 }}
                            transition={{ delay: delay + 0.2, type: "spring" }}
                            className="text-4xl md:text-5xl font-bold text-gradient mb-3"
                        >
                            {value}
                        </motion.p>
                        {change && (
                            <div className="flex items-center gap-2">
                                <span className={cn(
                                    "text-sm font-bold px-3 py-1.5 rounded-full",
                                    changeType === 'positive' && "bg-emerald-500/20 text-emerald-400",
                                    changeType === 'negative' && "bg-red-500/20 text-red-400",
                                    changeType === 'neutral' && "bg-blue-500/20 text-blue-400"
                                )}>
                                    {change}
                                </span>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </motion.div>
    )
}
