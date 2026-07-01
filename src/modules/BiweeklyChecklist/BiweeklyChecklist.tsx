import { useMemo } from "react";
import { Card, CardHeader } from "../../components/ui/Card";
import { Checkbox } from "../../components/ui/Checkbox";
import { useLocalStorage } from "../../lib/storage";
import { formatDateHe, getCurrentPeriod, getPeriodRange } from "../../lib/dateUtils";
import { BIWEEKLY_MAINTENANCE_ITEMS } from "../../data/checklistItems";
import type { BiweeklyChecklistReport } from "../../types";

const STORAGE_KEY = "vesselcrm:biweekly-checklist";

function freshItems() {
  return BIWEEKLY_MAINTENANCE_ITEMS.map((item) => ({ id: item.id, checked: false }));
}

export function BiweeklyChecklist() {
  const period = getCurrentPeriod();
  const [reports, setReports] = useLocalStorage<Record<string, BiweeklyChecklistReport>>(
    STORAGE_KEY,
    {},
  );

  const activeReport: BiweeklyChecklistReport =
    reports[period.key] ?? {
      periodKey: period.key,
      periodStart: period.start,
      periodEnd: period.end,
      items: freshItems(),
      updatedAt: "",
    };

  function toggleItem(itemId: string, checked: boolean) {
    setReports((prev) => {
      const base = prev[period.key] ?? activeReport;
      const items = base.items.map((it) => (it.id === itemId ? { ...it, checked } : it));
      return {
        ...prev,
        [period.key]: { ...base, items, updatedAt: new Date().toISOString() },
      };
    });
  }

  const lastFilledLabel = useMemo(() => {
    const allUpdated = Object.values(reports)
      .map((r) => r.updatedAt)
      .filter(Boolean)
      .sort();
    const last = allUpdated.at(-1);
    return last ? new Date(last).toLocaleString("he-IL") : "טרם מולא";
  }, [reports]);

  const doneCount = activeReport.items.filter((i) => i.checked).length;
  const totalCount = BIWEEKLY_MAINTENANCE_ITEMS.length;

  const pastPeriods = useMemo(
    () =>
      Object.values(reports)
        .filter((r) => r.periodKey !== period.key)
        .sort((a, b) => (a.periodKey < b.periodKey ? 1 : -1)),
    [reports, period.key],
  );

  return (
    <div className="flex flex-col gap-6">
      <Card>
        <CardHeader
          title="צ'קליסט דו-שבועי"
          subtitle={`תקופה נוכחית: ${formatDateHe(period.start)} - ${formatDateHe(period.end)} · מולא לאחרונה: ${lastFilledLabel}`}
        />
        <div className="p-4 sm:p-5">
          <div className="mb-4 flex items-center justify-between text-sm text-slate-500">
            <span>{`${doneCount}/${totalCount} פריטים בוצעו`}</span>
          </div>
          <div className="mb-4 h-2 w-full overflow-hidden rounded-full bg-slate-100">
            <div
              className="h-full rounded-full bg-cyan-600 transition-all"
              style={{ width: `${totalCount ? (doneCount / totalCount) * 100 : 0}%` }}
            />
          </div>
          <div className="grid grid-cols-1 gap-2.5 sm:grid-cols-2">
            {BIWEEKLY_MAINTENANCE_ITEMS.map((item) => {
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

      {pastPeriods.length > 0 && (
        <Card>
          <CardHeader title="היסטוריית תקופות קודמות" />
          <div className="flex flex-col divide-y divide-slate-100 p-2">
            {pastPeriods.map((r) => {
              const range = getPeriodRange(r.periodKey);
              const done = r.items.filter((i) => i.checked).length;
              return (
                <div key={r.periodKey} className="flex items-center justify-between px-3 py-3">
                  <span className="text-sm font-medium text-slate-700">
                    {formatDateHe(range.start)} - {formatDateHe(range.end)}
                  </span>
                  <span className="text-sm text-slate-500">
                    {done}/{totalCount} בוצעו
                  </span>
                </div>
              );
            })}
          </div>
        </Card>
      )}
    </div>
  );
}
