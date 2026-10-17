import React from "react";
import {
  Activity,
  Home,
  AlertTriangle,
  Skull,
  CheckCircle2,
} from "lucide-react";

interface SummaryProps {
  data: any;
}

export function DamageSummary({ data }: SummaryProps) {
  const summary = data.damage_summary;

  const stats = [
    {
      label: "Total Buildings",
      value: summary.total_buildings,
      icon: Home,
      color: "text-slate-400",
    },
    {
      label: "Destroyed",
      value: summary.destroyed,
      icon: Skull,
      color: "text-red-500",
    },
    {
      label: "Major Damage",
      value: summary.major_damage,
      icon: AlertTriangle,
      color: "text-orange-500",
    },
    {
      label: "Minor Damage",
      value: summary.minor_damage,
      icon: Activity,
      color: "text-yellow-500",
    },
    {
      label: "No Damage",
      value: summary.no_damage,
      icon: CheckCircle2,
      color: "text-green-500",
    },
  ];

  return (
    <div className="grid grid-cols-1 gap-4">
      {stats.map((stat) => (
        <div
          key={stat.label}
          className="p-4 bg-slate-800 rounded-lg border border-slate-700 flex items-center justify-between"
        >
          <div className="flex items-center gap-3">
            <stat.icon className={`w-5 h-5 ${stat.color}`} />
            <span className="text-slate-300 font-medium">{stat.label}</span>
          </div>
          <span className="text-xl font-bold text-white">{stat.value}</span>
        </div>
      ))}
    </div>
  );
}
