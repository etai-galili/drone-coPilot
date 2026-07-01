import { MapPin, Navigation } from "lucide-react";

export function MapPanel({
  isActive,
  missionType,
  eta,
  departureTime,
}: {
  isActive: boolean;
  missionType?: string;
  eta?: string;
  departureTime?: string;
}) {
  return (
    <div className="relative h-72 overflow-hidden rounded-xl border border-slate-200 bg-gradient-to-br from-sky-50 via-cyan-100 to-cyan-200">
      <svg viewBox="0 0 400 260" className="absolute inset-0 h-full w-full" preserveAspectRatio="none">
        {Array.from({ length: 9 }).map((_, i) => (
          <line
            key={`h${i}`}
            x1="0"
            y1={i * 32}
            x2="400"
            y2={i * 32}
            stroke="#0e7490"
            strokeOpacity="0.06"
            strokeWidth="1"
          />
        ))}
        {Array.from({ length: 13 }).map((_, i) => (
          <line
            key={`v${i}`}
            x1={i * 32}
            y1="0"
            x2={i * 32}
            y2="260"
            stroke="#0e7490"
            strokeOpacity="0.06"
            strokeWidth="1"
          />
        ))}
        <path
          d="M 40 210 C 100 150, 150 190, 210 120 S 320 60, 360 40"
          fill="none"
          stroke="#0e7490"
          strokeWidth="3"
          strokeDasharray="8 7"
          strokeLinecap="round"
          opacity={isActive ? 1 : 0.35}
        />
        <circle cx="40" cy="210" r="7" fill="#0e7490" />
        <circle cx="360" cy="40" r="7" fill={isActive ? "#059669" : "#94a3b8"} />
      </svg>

      <span
        className={`absolute top-3 left-3 inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-bold shadow-sm ${
          isActive ? "bg-emerald-600 text-white" : "bg-white/90 text-slate-500"
        }`}
      >
        <Navigation className="size-3.5" />
        {isActive ? "בהפלגה" : "אין הפלגה פעילה"}
      </span>

      {isActive && (
        <div className="absolute inset-x-3 bottom-3 flex flex-wrap gap-2 rounded-lg bg-white/90 p-3 text-xs shadow backdrop-blur">
          <div className="flex-1 min-w-24">
            <div className="font-semibold text-slate-400">סוג משימה</div>
            <div className="font-bold text-slate-800">{missionType || "--"}</div>
          </div>
          <div className="flex-1 min-w-24">
            <div className="font-semibold text-slate-400">יצאה בשעה</div>
            <div className="font-bold text-slate-800">{departureTime || "--"}</div>
          </div>
          <div className="flex-1 min-w-24">
            <div className="flex items-center gap-1 font-semibold text-slate-400">
              <MapPin className="size-3" />
              חזרה משוערת
            </div>
            <div className="font-bold text-slate-800">{eta || "--"}</div>
          </div>
        </div>
      )}
    </div>
  );
}
