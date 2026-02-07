'use client'

import { usePathname } from 'next/navigation'
import Link from 'next/link'
import { motion, AnimatePresence } from 'framer-motion'
import {
    LayoutDashboard,
    MessageSquare,
    Globe2,
    Database,
    BarChart3,
    Waves,
    FileText,
    Settings,
    Menu,
    X,
    Bell,
    Search,
    Sparkles,
    Zap
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { useState } from 'react'

const navigation = [
    { name: 'Dashboard', href: '/', icon: LayoutDashboard, gradient: 'from-blue-500 to-cyan-500' },
    { name: 'AI Chat', href: '/chat', icon: MessageSquare, gradient: 'from-purple-500 to-pink-500' },
    { name: 'Ocean Map', href: '/map', icon: Globe2, gradient: 'from-cyan-500 to-teal-500' },
    { name: 'Data Explorer', href: '/explorer', icon: Database, gradient: 'from-indigo-500 to-blue-500' },
    { name: 'Analytics', href: '/analytics', icon: BarChart3, gradient: 'from-violet-500 to-purple-500' },
    { name: 'Float Management', href: '/floats', icon: Waves, gradient: 'from-teal-500 to-emerald-500' },
    { name: 'Reports', href: '/reports', icon: FileText, gradient: 'from-orange-500 to-red-500' },
    { name: 'Settings', href: '/settings', icon: Settings, gradient: 'from-gray-500 to-slate-500' },
]

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode
}) {
    const pathname = usePathname()
    const [isSidebarOpen, setIsSidebarOpen] = useState(true)
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

    return (
        <div className="flex h-screen w-full bg-background overflow-hidden relative">
            {/* Animated Background */}
            <div className="absolute inset-0 animated-gradient opacity-50" />
            <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-primary/20 via-transparent to-secondary/20" />

            {/* Floating Orbs */}
            <div className="absolute top-20 left-20 w-72 h-72 bg-primary/20 rounded-full blur-3xl animate-pulse" />
            <div className="absolute bottom-20 right-20 w-96 h-96 bg-secondary/20 rounded-full blur-3xl animate-pulse delay-1000" />

            {/* Sidebar */}
            <motion.aside
                initial={{ width: 280 }}
                animate={{ width: isSidebarOpen ? 280 : 80 }}
                className="h-full glass-panel relative z-40 hidden md:flex flex-col border-r border-white/20"
            >
                {/* Logo */}
                <div className="p-6 flex items-center justify-between border-b border-white/10">
                    <Link href="/" className={cn("flex items-center gap-3 overflow-hidden group", !isSidebarOpen && "justify-center")}>
                        <div className="relative">
                            <div className="absolute inset-0 bg-gradient-to-br from-primary to-secondary rounded-2xl blur-md opacity-75 group-hover:opacity-100 transition-opacity" />
                            <div className="relative h-12 w-12 rounded-2xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-lg">
                                <Waves size={24} className="text-white" strokeWidth={2.5} />
                            </div>
                        </div>
                        {isSidebarOpen && (
                            <motion.div
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                className="flex flex-col"
                            >
                                <span className="font-bold text-xl tracking-tight text-gradient">FloatChat</span>
                                <span className="text-xs text-muted-foreground tracking-wider uppercase font-semibold">Ultra Edition</span>
                            </motion.div>
                        )}
                    </Link>
                    {isSidebarOpen && (
                        <button
                            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                            className="p-2 hover:bg-white/10 rounded-xl transition-all hover:scale-110"
                        >
                            <Menu size={18} className="text-muted-foreground" />
                        </button>
                    )}
                </div>

                {/* Navigation */}
                <nav className="p-4 space-y-2 flex-1 overflow-y-auto">
                    {navigation.map((item) => {
                        const isActive = pathname === item.href || (item.href !== '/' && pathname.startsWith(item.href))
                        const Icon = item.icon

                        return (
                            <Link
                                key={item.name}
                                href={item.href}
                                className="block relative group"
                            >
                                {isActive && (
                                    <motion.div
                                        layoutId="activeNav"
                                        className={cn("absolute inset-0 bg-gradient-to-r rounded-2xl", item.gradient)}
                                        transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                                    />
                                )}
                                <div className={cn(
                                    "relative flex items-center gap-4 px-4 py-3.5 rounded-2xl transition-all duration-300",
                                    isActive
                                        ? "text-white shadow-2xl"
                                        : "text-muted-foreground hover:bg-white/5 hover:text-foreground"
                                )}>
                                    <div className={cn(
                                        "p-2 rounded-xl transition-all",
                                        isActive
                                            ? "bg-white/20"
                                            : "bg-white/5 group-hover:bg-white/10"
                                    )}>
                                        <Icon size={20} strokeWidth={2} />
                                    </div>
                                    {isSidebarOpen && (
                                        <span className="font-semibold text-sm">{item.name}</span>
                                    )}
                                    {isActive && isSidebarOpen && (
                                        <motion.div
                                            initial={{ scale: 0 }}
                                            animate={{ scale: 1 }}
                                            className="ml-auto"
                                        >
                                            <Sparkles size={16} className="text-white/80" />
                                        </motion.div>
                                    )}
                                </div>
                            </Link>
                        )
                    })}
                </nav>

                {/* User Profile */}
                <div className="p-4 border-t border-white/10">
                    <div className="glass-panel-subtle rounded-2xl p-4 flex items-center gap-3 hover:bg-white/10 transition-all cursor-pointer group">
                        <div className="relative">
                            <div className="absolute inset-0 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full blur-md opacity-75 group-hover:opacity-100 transition-opacity" />
                            <div className="relative h-11 w-11 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white font-bold text-sm shadow-lg">
                                AN
                            </div>
                        </div>
                        {isSidebarOpen && (
                            <div className="flex flex-col flex-1 min-w-0">
                                <span className="text-sm font-bold text-foreground truncate">Abhijeet Nardele</span>
                                <span className="text-xs text-muted-foreground flex items-center gap-1">
                                    <Zap size={10} className="text-yellow-500" />
                                    Premium Pro
                                </span>
                            </div>
                        )}
                    </div>
                </div>
            </motion.aside>

            {/* Main Content Area */}
            <div className="flex-1 flex flex-col relative overflow-hidden">
                {/* Top Bar */}
                <header className="h-20 glass-panel-subtle flex items-center justify-between px-8 z-30 shrink-0 border-b border-white/10">
                    <div className="flex items-center gap-6">
                        <button
                            onClick={() => setIsMobileMenuOpen(true)}
                            className="md:hidden p-3 hover:bg-white/10 rounded-xl transition-all hover:scale-110"
                        >
                            <Menu size={22} />
                        </button>

                        {/* Global Search */}
                        <div className="hidden md:flex items-center gap-3 px-6 py-3.5 rounded-2xl glass-panel hover:border-primary/50 transition-all w-[500px] group">
                            <Search size={20} className="text-muted-foreground group-hover:text-primary transition-colors" />
                            <input
                                type="text"
                                placeholder="Search anything..."
                                className="bg-transparent border-none outline-none text-sm text-foreground placeholder:text-muted-foreground w-full font-medium"
                            />
                            <kbd className="px-3 py-1.5 text-xs font-bold text-muted-foreground bg-white/10 rounded-lg border border-white/20">
                                ⌘K
                            </kbd>
                        </div>
                    </div>

                    <div className="flex items-center gap-4">
                        {/* Notifications */}
                        <button className="relative p-3 hover:bg-white/10 rounded-xl transition-all hover:scale-110 group">
                            <Bell size={20} className="text-muted-foreground group-hover:text-foreground transition-colors" />
                            <span className="absolute top-2 right-2 h-2.5 w-2.5 bg-gradient-to-br from-red-500 to-pink-500 rounded-full animate-pulse shadow-lg shadow-red-500/50" />
                        </button>

                        {/* User Menu */}
                        <button className="hidden md:flex items-center gap-3 px-4 py-2 hover:bg-white/10 rounded-xl transition-all hover:scale-105">
                            <div className="relative">
                                <div className="absolute inset-0 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full blur-sm opacity-75" />
                                <div className="relative h-9 w-9 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white font-bold text-xs shadow-lg">
                                    AN
                                </div>
                            </div>
                        </button>
                    </div>
                </header>

                {/* Page Content */}
                <main className="flex-1 overflow-y-auto relative">
                    <AnimatePresence mode="wait">
                        <motion.div
                            key={pathname}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            transition={{ duration: 0.3 }}
                            className="h-full"
                        >
                            {children}
                        </motion.div>
                    </AnimatePresence>
                </main>
            </div>
        </div>
    )
}
