'use client'

import { User, Bell, Globe, Lock, Database, Palette } from 'lucide-react'

export default function SettingsPage() {
    return (
        <div className="p-6 md:p-8 space-y-6 max-w-4xl">
            {/* Header */}
            <div>
                <h1 className="text-2xl md:text-3xl font-bold text-white">Settings</h1>
                <p className="text-sm text-zinc-400 mt-1">Manage your preferences and account</p>
            </div>

            {/* Settings Sections */}
            <div className="space-y-4">
                <SettingsSection
                    icon={<User size={18} />}
                    title="Profile"
                    description="Update your personal information"
                />
                <SettingsSection
                    icon={<Bell size={18} />}
                    title="Notifications"
                    description="Configure email and push notifications"
                />
                <SettingsSection
                    icon={<Palette size={18} />}
                    title="Appearance"
                    description="Theme and display preferences"
                />
                <SettingsSection
                    icon={<Globe size={18} />}
                    title="Language & Region"
                    description="Set your language and units"
                />
                <SettingsSection
                    icon={<Database size={18} />}
                    title="Data Sources"
                    description="Configure GDAC endpoints"
                />
                <SettingsSection
                    icon={<Lock size={18} />}
                    title="Privacy & Security"
                    description="Manage your data and security settings"
                />
            </div>
        </div>
    )
}

function SettingsSection({ icon, title, description }: any) {
    return (
        <div className="rounded-2xl border border-white/[0.08] bg-white/[0.02] backdrop-blur-xl p-5 hover:border-white/[0.12] transition-all cursor-pointer group">
            <div className="flex items-center gap-4">
                <div className="p-3 rounded-lg bg-white/[0.05] text-zinc-400 group-hover:text-zinc-200 transition-colors">
                    {icon}
                </div>
                <div className="flex-1">
                    <h3 className="text-sm font-semibold text-white group-hover:text-indigo-300 transition-colors">
                        {title}
                    </h3>
                    <p className="text-xs text-zinc-500 mt-0.5">{description}</p>
                </div>
                <div className="text-zinc-600 group-hover:text-zinc-400 transition-colors">
                    →
                </div>
            </div>
        </div>
    )
}
