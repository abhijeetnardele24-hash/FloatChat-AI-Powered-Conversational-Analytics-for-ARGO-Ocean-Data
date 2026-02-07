'use client'

import { Waves, Battery, MapPin, Calendar, AlertCircle } from 'lucide-react'

export default function FloatsPage() {
    return (
        <div className="p-6 md:p-8 space-y-6">
            {/* Header */}
            <div>
                <h1 className="text-2xl md:text-3xl font-bold text-white">Float Management</h1>
                <p className="text-sm text-zinc-400 mt-1">Track and monitor individual Argo floats</p>
            </div>

            {/* Float Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {[...Array(9)].map((_, i) => (
                    <FloatCard key={i} id={`590697${i}`} />
                ))}
            </div>
        </div>
    )
}

function FloatCard({ id }: { id: string }) {
    return (
        <div className="rounded-2xl border border-white/[0.08] bg-white/[0.02] backdrop-blur-xl p-5 hover:border-white/[0.12] transition-all hover:scale-[1.02] cursor-pointer group">
            <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                    <div className="p-2.5 rounded-lg bg-indigo-500/10 text-indigo-400">
                        <Waves size={18} />
                    </div>
                    <div>
                        <h3 className="text-sm font-semibold text-white">Float #{id}</h3>
                        <p className="text-xs text-zinc-500">Active</p>
                    </div>
                </div>
                <div className="h-2 w-2 rounded-full bg-emerald-400" />
            </div>

            <div className="space-y-2">
                <div className="flex items-center gap-2 text-xs text-zinc-400">
                    <MapPin size={12} />
                    <span>Pacific Ocean</span>
                </div>
                <div className="flex items-center gap-2 text-xs text-zinc-400">
                    <Battery size={12} />
                    <span>Battery: 87%</span>
                </div>
                <div className="flex items-center gap-2 text-xs text-zinc-400">
                    <Calendar size={12} />
                    <span>Last update: 2 hours ago</span>
                </div>
            </div>
        </div>
    )
}
