'use client'

import { Search, Filter, Download, ChevronDown, Calendar } from 'lucide-react'

export default function ExplorerPage() {
    return (
        <div className="h-full flex flex-col">
            {/* Header */}
            <div className="p-6 border-b border-white/[0.08] bg-black/20 backdrop-blur-sm">
                <div className="flex items-center justify-between mb-4">
                    <div>
                        <h1 className="text-2xl font-bold text-white">Data Explorer</h1>
                        <p className="text-sm text-zinc-400 mt-1">Search and filter ocean profile data</p>
                    </div>
                    <button className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-indigo-500 to-cyan-500 text-white font-medium hover:shadow-lg hover:shadow-indigo-500/25 transition-all text-sm">
                        <Download size={16} />
                        Export Selected
                    </button>
                </div>

                {/* Search and Filters */}
                <div className="flex items-center gap-3">
                    <div className="flex-1 flex items-center gap-2 px-4 py-2.5 rounded-xl border border-white/[0.08] bg-white/[0.02] hover:border-white/[0.12] transition-colors">
                        <Search size={18} className="text-zinc-500" />
                        <input
                            type="text"
                            placeholder="Search by float ID, region, or parameters..."
                            className="bg-transparent border-none outline-none text-sm text-zinc-200 placeholder:text-zinc-600 w-full"
                        />
                    </div>
                    <button className="flex items-center gap-2 px-4 py-2.5 rounded-xl border border-white/[0.08] bg-white/[0.02] hover:bg-white/[0.06] transition-colors text-sm font-medium text-zinc-300">
                        <Filter size={16} />
                        Filters
                        <ChevronDown size={14} />
                    </button>
                    <button className="flex items-center gap-2 px-4 py-2.5 rounded-xl border border-white/[0.08] bg-white/[0.02] hover:bg-white/[0.06] transition-colors text-sm font-medium text-zinc-300">
                        <Calendar size={16} />
                        Date Range
                        <ChevronDown size={14} />
                    </button>
                </div>
            </div>

            {/* Data Table */}
            <div className="flex-1 overflow-auto p-6">
                <div className="rounded-2xl border border-white/[0.08] bg-white/[0.02] backdrop-blur-xl overflow-hidden">
                    <table className="w-full">
                        <thead className="bg-white/[0.05] border-b border-white/[0.08]">
                            <tr>
                                <th className="text-left px-6 py-4 text-xs font-semibold text-zinc-400 uppercase tracking-wider">
                                    Float ID
                                </th>
                                <th className="text-left px-6 py-4 text-xs font-semibold text-zinc-400 uppercase tracking-wider">
                                    Location
                                </th>
                                <th className="text-left px-6 py-4 text-xs font-semibold text-zinc-400 uppercase tracking-wider">
                                    Temperature
                                </th>
                                <th className="text-left px-6 py-4 text-xs font-semibold text-zinc-400 uppercase tracking-wider">
                                    Salinity
                                </th>
                                <th className="text-left px-6 py-4 text-xs font-semibold text-zinc-400 uppercase tracking-wider">
                                    Depth
                                </th>
                                <th className="text-left px-6 py-4 text-xs font-semibold text-zinc-400 uppercase tracking-wider">
                                    Date
                                </th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-white/[0.04]">
                            {[...Array(10)].map((_, i) => (
                                <tr key={i} className="hover:bg-white/[0.03] transition-colors cursor-pointer">
                                    <td className="px-6 py-4 text-sm font-medium text-zinc-300">590697{i}</td>
                                    <td className="px-6 py-4 text-sm text-zinc-400">Pacific Ocean</td>
                                    <td className="px-6 py-4 text-sm text-zinc-400">18.{i}°C</td>
                                    <td className="px-6 py-4 text-sm text-zinc-400">35.{i} PSU</td>
                                    <td className="px-6 py-4 text-sm text-zinc-400">{100 + i * 10}m</td>
                                    <td className="px-6 py-4 text-sm text-zinc-400">2024-02-0{i + 1}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    )
}
