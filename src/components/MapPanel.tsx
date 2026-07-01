import { MapPin, Navigation } from "lucide-react";
import { PannableMap } from "./PannableMap";

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
    <div className="relative h-96 overflow-hidden rounded-xl border border-slate-200">
      <PannableMap src="/maps/israel-maritime-space.jpg" alt="מפת המרחב הימי של ישראל" />

      <span
        className={`pointer-events-none absolute top-3 left-3 inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-bold shadow-sm ${
          isActive ? "bg-emerald-600 text-white" : "bg-white/90 text-slate-500"
        }`}
      >
        <Navigation className="size-3.5" />
        {isActive ? "בהפלגה" : "אין הפלגה פעילה"}
      </span>

      {isActive && (
        <div className="pointer-events-none absolute inset-x-3 bottom-3 flex flex-wrap gap-2 rounded-lg bg-white/90 p-3 text-xs shadow backdrop-blur">
          <div className="min-w-24 flex-1">
            <div className="font-semibold text-slate-400">סוג משימה</div>
            <div className="font-bold text-slate-800">{missionType || "--"}</div>
          </div>
          <div className="min-w-24 flex-1">
            <div className="font-semibold text-slate-400">יצאה בשעה</div>
            <div className="font-bold text-slate-800">{departureTime || "--"}</div>
          </div>
          <div className="min-w-24 flex-1">
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
