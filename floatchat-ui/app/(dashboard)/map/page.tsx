'use client'

import { motion } from 'framer-motion'
import { Map, Layers, ZoomIn, ZoomOut, Download, Filter } from 'lucide-react'

export default function MapPage() {
    return (
        <div className="h-full flex flex-col">
            {/* Map Controls */}
            <div className="p-6 border-b border-white/[0.08] bg-black/20 backdrop-blur-sm">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-2xl font-bold text-white">Interactive Ocean Map</h1>
                        <p className="text-sm text-zinc-400 mt-1">Visualize float locations and ocean data</p>
                    </div>
                    <div className="flex items-center gap-2">
                        <button className="flex items-center gap-2 px-4 py-2 rounded-xl border border-white/[0.08] bg-white/[0.02] hover:bg-white/[0.06] transition-colors text-sm font-medium text-zinc-300">
                            <Layers size={16} />
                            Layers
                        </button>
                        <button className="flex items-center gap-2 px-4 py-2 rounded-xl border border-white/[0.08] bg-white/[0.02] hover:bg-white/[0.06] transition-colors text-sm font-medium text-zinc-300">
                            <Filter size={16} />
                            Filters
                        </button>
                        <button className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-indigo-500 to-cyan-500 text-white font-medium hover:shadow-lg hover:shadow-indigo-500/25 transition-all text-sm">
                            <Download size={16} />
                            Export
                        </button>
                    </div>
                </div>
            </div>

            {/* Map Container */}
            <div className="flex-1 relative bg-zinc-950">
                <div className="absolute inset-0 flex items-center justify-center">
                    <div className="text-center">
                        <Map size={64} className="text-zinc-700 mx-auto mb-4" />
                        <h3 className="text-xl font-semibold text-zinc-600 mb-2">Interactive Map</h3>
                        <p className="text-zinc-700 text-sm max-w-md">
                            Mapbox GL or Deck.gl integration will be added here
                        </p>
                        <p className="text-zinc-800 text-xs mt-2">
                            Features: Float locations, temperature heatmaps, ocean currents
                        </p>
                    </div>
                </div>

                {/* Map Controls Overlay */}
                <div className="absolute top-4 right-4 flex flex-col gap-2">
                    <button className="p-3 rounded-lg bg-white/[0.1] backdrop-blur-md border border-white/[0.1] hover:bg-white/[0.15] transition-colors">
                        <ZoomIn size={18} className="text-white" />
                    </button>
                    <button className="p-3 rounded-lg bg-white/[0.1] backdrop-blur-md border border-white/[0.1] hover:bg-white/[0.15] transition-colors">
                        <ZoomOut size={18} className="text-white" />
                    </button>
                </div>
            </div>
        </div>
    )
}
