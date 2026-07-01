import { useMemo, useState } from "react";
import { ExternalLink, LinkIcon } from "lucide-react";
import { Card, CardHeader } from "../../components/ui/Card";
import { Field, TextInput } from "../../components/ui/Field";
import { ToggleYesNo } from "../../components/ui/ToggleYesNo";
import { useLocalStorage } from "../../lib/storage";
import { formatDateHe, getMonthHalfRange, getMonthKey, getMonthLabelHe } from "../../lib/dateUtils";
import type { MonthlyOverviewEntry } from "../../types";

const STORAGE_KEY = "vessel-mng:monthly-overview";

type RowId = "checklist-1" | "checklist-2" | "equipment";

function emptyEntry(): MonthlyOverviewEntry {
  return { done: false, fileLink: "", updatedAt: "" };
}

export function MonthlyOverview() {
  const currentMonthKey = getMonthKey();
  const [records, setRecords] = useLocalStorage<Record<string, MonthlyOverviewEntry>>(
    STORAGE_KEY,
    {},
  );
  const [selectedMonth, setSelectedMonth] = useState(currentMonthKey);

  const rows: { id: RowId; label: string; rangeHint: string }[] = [
    {
      id: "checklist-1",
      label: "צ'קליסט דו-שבועי — מחצית ראשונה",
      rangeHint: rangeLabel(selectedMonth, 1),
    },
    {
      id: "checklist-2",
      label: "צ'קליסט דו-שבועי — מחצית שנייה",
      rangeHint: rangeLabel(selectedMonth, 2),
    },
    { id: "equipment", label: "דוח ציוד חודשי", rangeHint: getMonthLabelHe(selectedMonth) },
  ];

  function keyFor(monthKey: string, rowId: RowId) {
    return `${monthKey}:${rowId}`;
  }

  function getEntry(rowId: RowId): MonthlyOverviewEntry {
    return records[keyFor(selectedMonth, rowId)] ?? emptyEntry();
  }

  function updateEntry(rowId: RowId, patch: Partial<MonthlyOverviewEntry>) {
    setRecords((prev) => {
      const key = keyFor(selectedMonth, rowId);
      const base = prev[key] ?? emptyEntry();
      return {
        ...prev,
        [key]: { ...base, ...patch, updatedAt: new Date().toISOString() },
      };
    });
  }

  const monthOptions = useMemo(() => {
    const months = new Set<string>([currentMonthKey]);
    Object.keys(records).forEach((key) => months.add(key.split(":")[0]));
    return Array.from(months).sort((a, b) => (a < b ? 1 : -1));
  }, [records, currentMonthKey]);

  return (
    <div className="flex flex-col gap-6">
      <Card>
        <CardHeader
          title="סקירה חודשית"
          subtitle="סטטוס הצ'קליסטים והדוח החודשי + קישור לקובץ"
          action={
            <select
              value={selectedMonth}
              onChange={(e) => setSelectedMonth(e.target.value)}
              className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-800 shadow-sm outline-none focus:border-cyan-600 focus:ring-2 focus:ring-cyan-100"
            >
              {monthOptions.map((monthKey) => (
                <option key={monthKey} value={monthKey}>
                  {getMonthLabelHe(monthKey)}
                </option>
              ))}
            </select>
          }
        />
        <div className="flex flex-col divide-y divide-slate-100">
          {rows.map((row) => {
            const entry = getEntry(row.id);
            return (
              <div key={row.id} className="flex flex-col gap-3 p-4 sm:flex-row sm:items-center sm:justify-between sm:p-5">
                <div>
                  <div className="text-sm font-bold text-slate-800">{row.label}</div>
                  <div dir="ltr" className="text-right text-xs text-slate-500">
                    {row.rangeHint}
                  </div>
                  {entry.updatedAt && (
                    <div className="mt-1 text-xs text-slate-400">
                      עודכן לאחרונה: {new Date(entry.updatedAt).toLocaleString("he-IL")}
                    </div>
                  )}
                </div>
                <div className="flex flex-wrap items-center gap-3">
                  <Field label="קישור לקובץ">
                    <div className="flex items-center gap-2">
                      <TextInput
                        value={entry.fileLink}
                        onChange={(e) => updateEntry(row.id, { fileLink: e.target.value })}
                        placeholder="https://..."
                        className="w-56"
                      />
                      {entry.fileLink && (
                        <a
                          href={entry.fileLink}
                          target="_blank"
                          rel="noreferrer"
                          className="rounded-lg p-2 text-cyan-700 hover:bg-cyan-50"
                          aria-label="פתח קובץ"
                        >
                          <ExternalLink className="size-4" />
                        </a>
                      )}
                      {!entry.fileLink && <LinkIcon className="size-4 text-slate-300" />}
                    </div>
                  </Field>
                  <ToggleYesNo
                    value={entry.done}
                    onChange={(v) => updateEntry(row.id, { done: v })}
                    yesLabel="בוצע"
                    noLabel="לא בוצע"
                  />
                </div>
              </div>
            );
          })}
        </div>
      </Card>
    </div>
  );
}

function rangeLabel(monthKey: string, half: 1 | 2): string {
  const { start, end } = getMonthHalfRange(monthKey, half);
  return `${formatDateHe(start)} - ${formatDateHe(end)}`;
}
