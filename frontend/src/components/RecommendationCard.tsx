import React from "react";
import { Info } from "lucide-react";

interface RecommendationProps {
  text: string;
}

export function RecommendationCard({ text }: RecommendationProps) {
  return (
    <div className="p-6 bg-blue-900/20 border border-blue-500/50 rounded-xl shadow-lg">
      <div className="flex items-center gap-2 mb-3 text-blue-400">
        <Info className="w-5 h-5" />
        <h3 className="font-bold uppercase tracking-wider text-sm">
          Emergency Recommendation
        </h3>
      </div>
      <p className="text-slate-200 leading-relaxed italic">"{text}"</p>
    </div>
  );
}
