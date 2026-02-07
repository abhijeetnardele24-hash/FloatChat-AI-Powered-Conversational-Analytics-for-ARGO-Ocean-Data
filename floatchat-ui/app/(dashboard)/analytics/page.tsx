'use client'

import { BarChart3, TrendingUp, Activity, PieChart, Download } from 'lucide-react'

export default function AnalyticsPage() {
    return (
        <div className="p-6 md:p-8 space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl md:text-3xl font-bold text-white">Advanced Analytics</h1>
                    <p className="text-sm text-zinc-400 mt-1">Deep statistical analysis and visualizations</p>
                </div>
                <button className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-indigo-500 to-cyan-500 text-white font-medium hover:shadow-lg hover:shadow-indigo-500/25 transition-all text-sm">
                    <Download size={16} />
                    Export Report
                </button>
            </div>

            {/* Analytics Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <AnalyticsCard
                    title="Trend Analysis"
                    subtitle="Time series patterns"
                    icon={<TrendingUp size={18} />}
                />
                <AnalyticsCard
                    title="Distribution Analysis"
                    subtitle="Statistical breakdown"
                    icon={<PieChart size={18} />}
                />
                <AnalyticsCard
                    title="Correlation Study"
                    subtitle="Parameter relationships"
                    icon={<Activity size={18} />}
                />
                <AnalyticsCard
                    title="Regional Comparison"
                    subtitle="Ocean basin analysis"
                    icon={<BarChart3 size={18} />}
                />
            </div>
        </div>
    )
}

function AnalyticsCard({ title, subtitle, icon }: any) {
    return (
        <div className="rounded-2xl border border-white/[0.08] bg-white/[0.02] backdrop-blur-xl p-6 hover:border-white/[0.12] transition-colors group">
            <div className="flex items-start justify-between mb-6">
                <div>
                    <h3 className="text-base font-semibold text-white mb-1">{title}</h3>
                    <p className="text-sm text-zinc-500">{subtitle}</p>
                </div>
                <div className="p-2 rounded-lg bg-white/[0.05] text-zinc-400 group-hover:text-zinc-200 transition-colors">
                    {icon}
                </div>
            </div>
            <div className="h-64 rounded-xl bg-white/[0.02] border border-white/[0.04] flex items-center justify-center">
                <div className="text-center">
                    <Activity size={32} className="text-zinc-700 mx-auto mb-2" />
                    <p className="text-zinc-600 text-sm">Chart visualization</p>
                </div>
            </div>
        </div>
    )
}
