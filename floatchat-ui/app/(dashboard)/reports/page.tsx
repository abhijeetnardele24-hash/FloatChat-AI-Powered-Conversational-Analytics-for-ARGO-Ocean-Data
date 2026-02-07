'use client'

import { FileText, Download, Plus, Calendar } from 'lucide-react'

export default function ReportsPage() {
    return (
        <div className="p-6 md:p-8 space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl md:text-3xl font-bold text-white">Reports</h1>
                    <p className="text-sm text-zinc-400 mt-1">Generate and manage analysis reports</p>
                </div>
                <button className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-indigo-500 to-cyan-500 text-white font-medium hover:shadow-lg hover:shadow-indigo-500/25 transition-all text-sm">
                    <Plus size={16} />
                    New Report
                </button>
            </div>

            {/* Report Templates */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {[
                    { name: 'Monthly Summary', desc: 'Comprehensive monthly overview' },
                    { name: 'Regional Analysis', desc: 'Ocean basin comparison' },
                    { name: 'Float Performance', desc: 'Individual float metrics' },
                    { name: 'Data Quality Report', desc: 'QC flags and validation' },
                    { name: 'Temperature Trends', desc: 'Long-term temperature analysis' },
                    { name: 'Custom Report', desc: 'Build your own template' },
                ].map((report, i) => (
                    <div key={i} className="rounded-2xl border border-white/[0.08] bg-white/[0.02] backdrop-blur-xl p-5 hover:border-white/[0.12] transition-all hover:scale-[1.02] cursor-pointer group">
                        <div className="flex items-start gap-3 mb-3">
                            <div className="p-2.5 rounded-lg bg-indigo-500/10 text-indigo-400">
                                <FileText size={18} />
                            </div>
                            <div className="flex-1">
                                <h3 className="text-sm font-semibold text-white group-hover:text-indigo-300 transition-colors">
                                    {report.name}
                                </h3>
                                <p className="text-xs text-zinc-500 mt-1">{report.desc}</p>
                            </div>
                        </div>
                        <button className="w-full mt-3 flex items-center justify-center gap-2 px-3 py-2 rounded-lg border border-white/[0.08] bg-white/[0.02] hover:bg-white/[0.06] transition-colors text-xs font-medium text-zinc-300">
                            <Download size={14} />
                            Generate
                        </button>
                    </div>
                ))}
            </div>
        </div>
    )
}
