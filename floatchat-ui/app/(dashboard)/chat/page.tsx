'use client'

import { motion } from 'framer-motion'
import {
    Sparkles,
    Send,
    Globe2,
    Thermometer,
    TrendingUp,
    Database,
    Plus,
    Clock,
    Trash2
} from 'lucide-react'
import { useState } from 'react'

export default function ChatPage() {
    const [messages, setMessages] = useState<any[]>([])
    const [input, setInput] = useState('')

    const suggestions = [
        { icon: <Globe2 size={16} />, text: "Show Pacific Ocean temperature data" },
        { icon: <Thermometer size={16} />, text: "Find temperature anomalies in 2024" },
        { icon: <TrendingUp size={16} />, text: "Analyze salinity trends last 6 months" },
    ]

    return (
        <div className="h-full flex">
            {/* Chat History Sidebar */}
            <div className="w-64 border-r border-white/[0.08] bg-black/10 backdrop-blur-sm p-4 space-y-4 hidden lg:block">
                <div className="flex items-center justify-between">
                    <h3 className="text-sm font-semibold text-white">Chat History</h3>
                    <button className="p-1.5 hover:bg-white/10 rounded-lg transition-colors">
                        <Plus size={16} className="text-zinc-400" />
                    </button>
                </div>

                <div className="space-y-2">
                    {[
                        { title: "Pacific Ocean Analysis", time: "2 hours ago" },
                        { title: "Salinity Trends 2024", time: "Yesterday" },
                        { title: "Float #5906970 Data", time: "2 days ago" },
                    ].map((chat, i) => (
                        <button
                            key={i}
                            className="w-full text-left p-3 rounded-lg border border-white/[0.06] bg-white/[0.02] hover:bg-white/[0.06] transition-colors group"
                        >
                            <div className="flex items-start justify-between gap-2">
                                <div className="flex-1 min-w-0">
                                    <p className="text-sm font-medium text-zinc-300 group-hover:text-white transition-colors truncate">
                                        {chat.title}
                                    </p>
                                    <p className="text-xs text-zinc-600 mt-1 flex items-center gap-1">
                                        <Clock size={10} />
                                        {chat.time}
                                    </p>
                                </div>
                                <button className="opacity-0 group-hover:opacity-100 p-1 hover:bg-white/10 rounded transition-all">
                                    <Trash2 size={12} className="text-zinc-500" />
                                </button>
                            </div>
                        </button>
                    ))}
                </div>
            </div>

            {/* Main Chat Area */}
            <div className="flex-1 flex flex-col">
                {messages.length === 0 ? (
                    <div className="flex-1 flex items-center justify-center p-6">
                        <div className="w-full max-w-3xl space-y-8">
                            {/* Hero */}
                            <div className="text-center space-y-4">
                                <motion.div
                                    initial={{ scale: 0.9, opacity: 0 }}
                                    animate={{ scale: 1, opacity: 1 }}
                                    transition={{ delay: 0.1, duration: 0.5 }}
                                    className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-white/[0.08] bg-white/[0.02] backdrop-blur-xl"
                                >
                                    <Sparkles size={16} className="text-indigo-400" />
                                    <span className="text-sm text-zinc-300 font-medium">AI-Powered Ocean Intelligence</span>
                                </motion.div>

                                <motion.h1
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: 0.2 }}
                                    className="text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight text-white"
                                >
                                    Ask Anything About
                                    <br />
                                    <span className="bg-gradient-to-r from-indigo-400 via-cyan-400 to-blue-400 bg-clip-text text-transparent">
                                        The Ocean
                                    </span>
                                </motion.h1>

                                <motion.p
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    transition={{ delay: 0.3 }}
                                    className="text-zinc-400 text-lg max-w-2xl mx-auto"
                                >
                                    Explore 800,000+ Argo profiles with natural language. Get instant insights on temperature, salinity, and ocean dynamics.
                                </motion.p>
                            </div>

                            {/* Suggestions */}
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                                {suggestions.map((item, i) => (
                                    <motion.button
                                        key={i}
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: 0.4 + i * 0.1 }}
                                        className="flex items-center gap-3 p-4 text-left rounded-xl border border-white/[0.06] bg-white/[0.02] hover:bg-white/[0.06] hover:border-white/[0.12] transition-all group"
                                    >
                                        <div className="p-2.5 rounded-lg bg-white/[0.04] text-zinc-400 group-hover:text-zinc-200 transition-colors">
                                            {item.icon}
                                        </div>
                                        <span className="text-sm font-medium text-zinc-400 group-hover:text-zinc-200 transition-colors">
                                            {item.text}
                                        </span>
                                    </motion.button>
                                ))}
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="flex-1 overflow-y-auto p-6">
                        {/* Messages will go here */}
                    </div>
                )}

                {/* Input Area */}
                <div className="p-6 border-t border-white/[0.08] bg-black/20 backdrop-blur-sm">
                    <div className="max-w-4xl mx-auto">
                        <div className="relative rounded-2xl border border-white/[0.1] bg-white/[0.03] backdrop-blur-xl p-1.5 shadow-2xl shadow-black/20 hover:border-white/[0.15] transition-colors">
                            <textarea
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                placeholder="What would you like to know about the ocean?"
                                className="w-full bg-transparent border-none outline-none text-white placeholder:text-zinc-500 resize-none px-4 py-3 text-base leading-relaxed min-h-[80px]"
                            />
                            <div className="flex items-center justify-between px-2">
                                <div className="flex items-center gap-2">
                                    <button className="p-2 rounded-lg hover:bg-white/[0.05] text-zinc-400 hover:text-zinc-200 transition-colors">
                                        <Database size={18} />
                                    </button>
                                </div>
                                <button className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-indigo-500 to-cyan-500 text-white font-medium hover:shadow-lg hover:shadow-indigo-500/25 transition-all hover:scale-[1.02] active:scale-[0.98]">
                                    <span className="text-sm">Send</span>
                                    <Send size={16} />
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
