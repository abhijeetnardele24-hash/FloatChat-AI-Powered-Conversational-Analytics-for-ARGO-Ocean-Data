'use client'

import { motion } from 'framer-motion'
import {
    Database,
    Waves,
    Thermometer,
    Droplets,
    TrendingUp,
    BarChart3,
    Activity,
    Download,
    RefreshCw,
    ArrowUpRight,
    Sparkles,
    Zap
} from 'lucide-react'
import { StatCard } from '@/components/ui/stat-card'

export default function DashboardPage() {
    return (
        <div className="p-8 md:p-12 space-y-10">
            {/* Header */}
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex items-center justify-between"
            >
                <div className="space-y-2">
                    <div className="flex items-center gap-3">
                        <h1 className="text-4xl md:text-5xl font-bold text-gradient">
                            Ocean Analytics
                        </h1>
                        <motion.div
                            animate={{ rotate: 360 }}
                            transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                        >
                            <Sparkles className="text-primary" size={32} />
                        </motion.div>
                    </div>
                    <p className="text-muted-foreground text-lg flex items-center gap-2">
                        <Zap size={18} className="text-yellow-500" />
                        Real-time insights from 800,000+ Argo ocean profiles
                    </p>
                </div>
                <div className="flex items-center gap-3">
                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        className="flex items-center gap-2 px-6 py-3.5 rounded-2xl glass-panel hover:bg-white/10 transition-all text-sm font-semibold"
                    >
                        <RefreshCw size={18} />
                        <span className="hidden md:inline">Refresh</span>
                    </motion.button>
                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        className="flex items-center gap-2 px-6 py-3.5 rounded-2xl bg-gradient-to-r from-primary to-secondary text-white font-semibold shadow-2xl glow-primary hover:shadow-3xl transition-all text-sm"
                    >
                        <Download size={18} />
                        <span className="hidden md:inline">Export Data</span>
                    </motion.button>
                </div>
            </motion.div>

            {/* KPI Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    title="Total Profiles"
                    value="847,293"
                    change="+12.5% this month"
                    changeType="positive"
                    icon={Database}
                    delay={0}
                />
                <StatCard
                    title="Active Floats"
                    value="1,247"
                    change="98.2% operational"
                    changeType="positive"
                    icon={Waves}
                    delay={0.1}
                />
                <StatCard
                    title="Avg Temperature"
                    value="18.4°C"
                    change="+0.3°C vs last year"
                    changeType="neutral"
                    icon={Thermometer}
                    delay={0.2}
                />
                <StatCard
                    title="Avg Salinity"
                    value="35.1 PSU"
                    change="Within normal range"
                    changeType="neutral"
                    icon={Droplets}
                    delay={0.3}
                />
            </div>

            {/* Charts Section */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <ChartCard
                    title="Temperature Trends"
                    subtitle="Last 6 months"
                    icon={<TrendingUp size={20} />}
                    gradient="from-orange-500 to-red-500"
                    delay={0.4}
                />
                <ChartCard
                    title="Salinity Distribution"
                    subtitle="By ocean region"
                    icon={<BarChart3 size={20} />}
                    gradient="from-cyan-500 to-blue-500"
                    delay={0.5}
                />
            </div>

            {/* Activity Feed */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6, duration: 0.4 }}
                className="glass-panel rounded-3xl p-8"
            >
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h3 className="text-2xl font-bold text-foreground mb-1">Recent Measurements</h3>
                        <p className="text-sm text-muted-foreground">Live updates from ocean floats</p>
                    </div>
                    <button className="text-sm text-primary hover:text-secondary transition-colors font-semibold flex items-center gap-1">
                        View All
                        <ArrowUpRight size={16} />
                    </button>
                </div>
                <div className="space-y-4">
                    {[
                        { float: '5906970', location: 'Pacific Ocean', time: '2 minutes ago', temp: '18.4°C' },
                        { float: '5906971', location: 'Atlantic Ocean', time: '5 minutes ago', temp: '19.1°C' },
                        { float: '5906972', location: 'Indian Ocean', time: '12 minutes ago', temp: '22.3°C' },
                        { float: '5906973', location: 'Southern Ocean', time: '18 minutes ago', temp: '15.7°C' },
                    ].map((item, i) => (
                        <ActivityItem key={i} {...item} delay={0.7 + i * 0.05} />
                    ))}
                </div>
            </motion.div>
        </div>
    )
}

function ChartCard({ title, subtitle, icon, gradient, delay }: any) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay, duration: 0.4 }}
            whileHover={{ scale: 1.02, y: -5 }}
            className="glass-panel rounded-3xl p-8 hover:shadow-2xl transition-all group cursor-pointer"
        >
            <div className="flex items-start justify-between mb-8">
                <div>
                    <h3 className="text-xl font-bold text-foreground mb-2">{title}</h3>
                    <p className="text-sm text-muted-foreground">{subtitle}</p>
                </div>
                <div className={cn("p-3 rounded-2xl bg-gradient-to-br", gradient, "text-white shadow-lg")}>
                    {icon}
                </div>
            </div>
            <div className="h-64 rounded-2xl bg-gradient-to-br from-white/5 to-white/[0.02] border border-white/10 flex items-center justify-center relative overflow-hidden group-hover:border-white/20 transition-all">
                <div className="absolute inset-0 bg-gradient-to-br from-primary/10 to-secondary/10 opacity-0 group-hover:opacity-100 transition-opacity" />
                <div className="text-center relative z-10">
                    <Activity size={48} className="text-muted-foreground/30 mx-auto mb-4" />
                    <p className="text-muted-foreground text-sm font-medium">Chart visualization</p>
                    <p className="text-muted-foreground/50 text-xs mt-2">Coming soon with real data</p>
                </div>
            </div>
        </motion.div>
    )
}

function ActivityItem({ float, location, time, temp, delay }: any) {
    return (
        <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay }}
            className="flex items-center gap-4 p-5 rounded-2xl hover:bg-white/5 transition-all cursor-pointer group border border-transparent hover:border-white/10"
        >
            <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-br from-primary to-secondary rounded-full blur-md opacity-50 group-hover:opacity-75 transition-opacity" />
                <div className="relative h-12 w-12 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-lg">
                    <Waves size={20} className="text-white" />
                </div>
            </div>
            <div className="flex-1 min-w-0">
                <p className="text-sm font-bold text-foreground group-hover:text-primary transition-colors">
                    New profile from Float #{float}
                </p>
                <p className="text-xs text-muted-foreground mt-1">{location} • {time}</p>
            </div>
            <div className="text-right">
                <p className="text-lg font-bold text-gradient">{temp}</p>
                <p className="text-xs text-muted-foreground">Temperature</p>
            </div>
            <ArrowUpRight size={18} className="text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
        </motion.div>
    )
}

function cn(...classes: any[]) {
    return classes.filter(Boolean).join(' ')
}
