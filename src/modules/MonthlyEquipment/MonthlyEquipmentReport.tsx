import { useMemo, useState } from "react";
import { Card, CardHeader } from "../../components/ui/Card";
import { Checkbox } from "../../components/ui/Checkbox";
import { useLocalStorage } from "../../lib/storage";
import { getMonthKey, getMonthLabelHe } from "../../lib/dateUtils";
import { MONTHLY_EQUIPMENT_ITEMS } from "../../data/checklistItems";
import type { MonthlyEquipmentReport as ReportType } from "../../types";

function storageKey(vesselId: string) {
  return `vessel-mng:${vesselId}:monthly-equipment`;
}

function freshItems() {
  return MONTHLY_EQUIPMENT_ITEMS.map((item) => ({ id: item.id, checked: false }));
}

export function MonthlyEquipmentReport({ vesselId }: { vesselId: string }) {
  const currentMonthKey = getMonthKey();
  const [reports, setReports] = useLocalStorage<Record<string, ReportType>>(
    storageKey(vesselId),
    {},
  );
  const [selectedMonth, setSelectedMonth] = useState(currentMonthKey);

  const activeReport: ReportType =
    reports[selectedMonth] ??
    (selectedMonth === currentMonthKey
      ? { monthKey: currentMonthKey, items: freshItems(), updatedAt: new Date().toISOString() }
      : { monthKey: selectedMonth, items: freshItems(), updatedAt: new Date().toISOString() });

  function toggleItem(itemId: string, checked: boolean) {
    setReports((prev) => {
      const base = prev[selectedMonth] ?? activeReport;
      const items = base.items.map((it) => (it.id === itemId ? { ...it, checked } : it));
      return {
        ...prev,
        [selectedMonth]: { ...base, items, updatedAt: new Date().toISOString() },
      };
    });
  }

  const historyMonths = useMemo(() => {
    const months = new Set([currentMonthKey, ...Object.keys(reports)]);
    return Array.from(months).sort((a, b) => (a < b ? 1 : -1));
  }, [reports, currentMonthKey]);

  const doneCount = activeReport.items.filter((i) => i.checked).length;
  const totalCount = MONTHLY_EQUIPMENT_ITEMS.length;

  return (
    <div className="flex flex-col gap-6">
      <Card>
        <CardHeader
          title="דוח ציוד חודשי"
          subtitle={`${getMonthLabelHe(selectedMonth)} · ${doneCount}/${totalCount} פריטים נבדקו`}
          action={
            <select
              value={selectedMonth}
              onChange={(e) => setSelectedMonth(e.target.value)}
              className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-800 shadow-sm outline-none focus:border-cyan-600 focus:ring-2 focus:ring-cyan-100"
            >
              {historyMonths.map((monthKey) => (
                <option key={monthKey} value={monthKey}>
                  {getMonthLabelHe(monthKey)}
                </option>
              ))}
            </select>
          }
        />
        <div className="p-4 sm:p-5">
          <div className="mb-4 h-2 w-full overflow-hidden rounded-full bg-slate-100">
            <div
              className="h-full rounded-full bg-cyan-600 transition-all"
              style={{ width: `${totalCount ? (doneCount / totalCount) * 100 : 0}%` }}
            />
          </div>
          <div className="grid grid-cols-1 gap-2.5 sm:grid-cols-2">
            {MONTHLY_EQUIPMENT_ITEMS.map((item) => {
              const state = activeReport.items.find((i) => i.id === item.id);
              return (
                <Checkbox
                  key={item.id}
                  label={item.label}
                  checked={state?.checked ?? false}
                  onChange={(checked) => toggleItem(item.id, checked)}
                />
              );
            })}
          </div>
        </div>
      </Card>

      <Card>
        <CardHeader title="היסטוריית דוחות חודשיים" subtitle="לחצו על חודש כדי לצפות בו" />
        <div className="flex flex-wrap gap-2 p-4 sm:p-5">
          {historyMonths.map((monthKey) => {
            const report = reports[monthKey];
            const done = report ? report.items.filter((i) => i.checked).length : 0;
            const isCurrent = monthKey === currentMonthKey;
            return (
              <button
                key={monthKey}
                onClick={() => setSelectedMonth(monthKey)}
                className={`rounded-xl border px-4 py-3 text-right transition ${
                  selectedMonth === monthKey
                    ? "border-cyan-600 bg-cyan-50"
                    : "border-slate-200 bg-white hover:bg-slate-50"
                }`}
              >
                <div className="text-sm font-bold text-slate-800">
                  {getMonthLabelHe(monthKey)} {isCurrent && "(נוכחי)"}
                </div>
                <div className="text-xs text-slate-500">
                  {done}/{totalCount} בוצעו
                </div>
              </button>
            );
          })}
        </div>
      </Card>
    </div>
  );
}
