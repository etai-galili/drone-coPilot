import { formatDateHe } from "../../lib/dateUtils";
import type { StatusHandoverEntry } from "../../types";

export function PrintableHandover({ entry }: { entry: StatusHandoverEntry }) {
  return (
    <div dir="rtl" className="mx-auto max-w-3xl p-10 text-slate-900">
      <h1 className="mb-1 text-2xl font-extrabold">VesselCRM — טופס העברת סטטוס</h1>
      <p className="mb-6 text-sm text-slate-500">תאריך: {formatDateHe(entry.date)}</p>

      <div className="mb-6 grid grid-cols-2 gap-4 border-b border-slate-300 pb-4">
        <PrintField label="שם משיט מוסר" value={entry.outgoingCommander} />
        <PrintField label="שם משיט מקבל" value={entry.incomingCommander} />
      </div>

      <PrintSection title="אימונים שבוצעו" value={entry.trainingsCompleted} />
      <PrintSection title="תקלות פתוחות" value={entry.openFaults} />
      <PrintSection title="הזמנות פתוחות" value={entry.openOrders} />
      <PrintSection title="סטטוס כלים" value={entry.equipmentStatus} />
      <PrintSection title="הודעות חשובות" value={entry.importantMessages} />
    </div>
  );
}

function PrintField({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="text-xs font-semibold uppercase text-slate-500">{label}</div>
      <div className="text-base font-medium">{value || "—"}</div>
    </div>
  );
}

function PrintSection({ title, value }: { title: string; value: string }) {
  return (
    <div className="mb-4">
      <h2 className="mb-1 text-sm font-bold text-slate-700">{title}</h2>
      <p className="whitespace-pre-wrap text-sm text-slate-800">{value || "—"}</p>
    </div>
  );
}
