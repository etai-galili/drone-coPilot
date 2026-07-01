import type { ReactNode } from "react";

export function StatCard({
  icon,
  label,
  value,
  unit,
  hint,
}: {
  icon: ReactNode;
  label: string;
  value: string | number;
  unit: string;
  hint?: string;
}) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm shadow-slate-200/60">
      <div className="mb-3 flex items-center justify-between">
        <span className="text-sm font-semibold text-slate-500">{label}</span>
        <span className="rounded-lg bg-cyan-50 p-1.5 text-cyan-700">{icon}</span>
      </div>
      <div className="flex items-baseline gap-1.5">
        <span className="text-3xl font-extrabold text-slate-800">{value}</span>
        <span className="text-sm font-semibold text-slate-400">{unit}</span>
      </div>
      {hint && <div className="mt-1 text-xs text-slate-400">{hint}</div>}
    </div>
  );
}
