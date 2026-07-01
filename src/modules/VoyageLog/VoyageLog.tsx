import { useMemo, useState } from "react";
import { Plus, Trash2, X } from "lucide-react";
import { Card, CardHeader } from "../../components/ui/Card";
import { Field, TextArea, TextInput } from "../../components/ui/Field";
import { Button } from "../../components/ui/Button";
import { ToggleYesNo } from "../../components/ui/ToggleYesNo";
import { generateId, useLocalStorage } from "../../lib/storage";
import { formatDateHe, todayISO } from "../../lib/dateUtils";
import type { VoyageEntry } from "../../types";

const STORAGE_KEY = "vesselcrm:voyage-log";

function emptyDraft(): Omit<VoyageEntry, "id" | "createdAt"> {
  return {
    date: todayISO(),
    departureTime: "",
    returnTime: "",
    purpose: "",
    crewNames: [],
    cleanupDone: false,
    refuelNeeded: false,
    fuelRemaining: "",
    notes: "",
  };
}

export function VoyageLog() {
  const [entries, setEntries] = useLocalStorage<VoyageEntry[]>(STORAGE_KEY, []);
  const [draft, setDraft] = useState(emptyDraft());
  const [crewInput, setCrewInput] = useState("");
  const [fromFilter, setFromFilter] = useState("");
  const [toFilter, setToFilter] = useState("");

  function addCrewName() {
    const name = crewInput.trim();
    if (!name) return;
    setDraft((d) => ({ ...d, crewNames: [...d.crewNames, name] }));
    setCrewInput("");
  }

  function removeCrewName(index: number) {
    setDraft((d) => ({ ...d, crewNames: d.crewNames.filter((_, i) => i !== index) }));
  }

  function submit() {
    if (!draft.date || !draft.purpose) return;
    const entry: VoyageEntry = {
      ...draft,
      id: generateId(),
      createdAt: new Date().toISOString(),
    };
    setEntries((prev) => [entry, ...prev]);
    setDraft(emptyDraft());
  }

  function removeEntry(id: string) {
    setEntries((prev) => prev.filter((e) => e.id !== id));
  }

  const filtered = useMemo(() => {
    return entries
      .filter((e) => (fromFilter ? e.date >= fromFilter : true))
      .filter((e) => (toFilter ? e.date <= toFilter : true))
      .sort((a, b) => (a.date < b.date ? 1 : -1));
  }, [entries, fromFilter, toFilter]);

  return (
    <div className="flex flex-col gap-6">
      <Card>
        <CardHeader title="יומן הפלגות" subtitle="רישום הפלגה חדשה" />
        <div className="grid grid-cols-1 gap-4 p-4 sm:grid-cols-2 sm:p-5 lg:grid-cols-3">
          <Field label="תאריך" required>
            <TextInput
              type="date"
              value={draft.date}
              onChange={(e) => setDraft((d) => ({ ...d, date: e.target.value }))}
            />
          </Field>
          <Field label="שעת יציאה">
            <TextInput
              type="time"
              value={draft.departureTime}
              onChange={(e) => setDraft((d) => ({ ...d, departureTime: e.target.value }))}
            />
          </Field>
          <Field label="שעת חזרה">
            <TextInput
              type="time"
              value={draft.returnTime}
              onChange={(e) => setDraft((d) => ({ ...d, returnTime: e.target.value }))}
            />
          </Field>

          <Field label="מטרת ההפלגה" required>
            <TextInput
              value={draft.purpose}
              onChange={(e) => setDraft((d) => ({ ...d, purpose: e.target.value }))}
              placeholder="לדוגמה: אימון ניווט, סיור שגרתי..."
            />
          </Field>

          <Field label="כמה דלק נשאר">
            <TextInput
              value={draft.fuelRemaining}
              onChange={(e) => setDraft((d) => ({ ...d, fuelRemaining: e.target.value }))}
              placeholder='לדוגמה: 75%, 120 ליטר'
            />
          </Field>

          <div className="sm:col-span-2 lg:col-span-3">
            <Field label="שמות המשיטים">
              <div className="flex flex-wrap gap-2">
                <TextInput
                  value={crewInput}
                  onChange={(e) => setCrewInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault();
                      addCrewName();
                    }
                  }}
                  placeholder="הקלד שם ולחץ הוסף"
                  className="flex-1"
                />
                <Button type="button" variant="secondary" onClick={addCrewName}>
                  <Plus className="size-4" />
                  הוסף
                </Button>
              </div>
            </Field>
            {draft.crewNames.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-2">
                {draft.crewNames.map((name, i) => (
                  <span
                    key={`${name}-${i}`}
                    className="flex items-center gap-1.5 rounded-full bg-cyan-50 px-3 py-1 text-sm font-medium text-cyan-800"
                  >
                    {name}
                    <button
                      type="button"
                      onClick={() => removeCrewName(i)}
                      className="text-cyan-500 hover:text-cyan-800"
                      aria-label="הסר"
                    >
                      <X className="size-3.5" />
                    </button>
                  </span>
                ))}
              </div>
            )}
          </div>

          <Field label="חיסול בסיום">
            <ToggleYesNo
              value={draft.cleanupDone}
              onChange={(v) => setDraft((d) => ({ ...d, cleanupDone: v }))}
            />
          </Field>
          <Field label="נדרש תדלוק">
            <ToggleYesNo
              value={draft.refuelNeeded}
              onChange={(v) => setDraft((d) => ({ ...d, refuelNeeded: v }))}
            />
          </Field>

          <div className="sm:col-span-2 lg:col-span-3">
            <Field label="הערות">
              <TextArea
                value={draft.notes}
                onChange={(e) => setDraft((d) => ({ ...d, notes: e.target.value }))}
              />
            </Field>
          </div>
        </div>
        <div className="flex justify-end border-t border-slate-100 p-4 sm:p-5">
          <Button onClick={submit} disabled={!draft.date || !draft.purpose}>
            שמור הפלגה
          </Button>
        </div>
      </Card>

      <Card>
        <CardHeader
          title="היסטוריית הפלגות"
          subtitle={`${filtered.length} רשומות`}
          action={
            <div className="flex flex-wrap items-center gap-2">
              <TextInput
                type="date"
                value={fromFilter}
                onChange={(e) => setFromFilter(e.target.value)}
                className="w-auto"
              />
              <span className="text-slate-400">עד</span>
              <TextInput
                type="date"
                value={toFilter}
                onChange={(e) => setToFilter(e.target.value)}
                className="w-auto"
              />
              {(fromFilter || toFilter) && (
                <Button
                  variant="ghost"
                  onClick={() => {
                    setFromFilter("");
                    setToFilter("");
                  }}
                >
                  נקה סינון
                </Button>
              )}
            </div>
          }
        />
        <div className="overflow-x-auto">
          <table className="w-full min-w-[720px] text-right text-sm">
            <thead className="bg-slate-50 text-slate-500">
              <tr>
                <th className="px-4 py-3 font-semibold">תאריך</th>
                <th className="px-4 py-3 font-semibold">יציאה - חזרה</th>
                <th className="px-4 py-3 font-semibold">מטרה</th>
                <th className="px-4 py-3 font-semibold">משיטים</th>
                <th className="px-4 py-3 font-semibold">חיסול</th>
                <th className="px-4 py-3 font-semibold">תדלוק</th>
                <th className="px-4 py-3 font-semibold">דלק שנותר</th>
                <th className="px-4 py-3 font-semibold"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filtered.map((e) => (
                <tr key={e.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-medium text-slate-800">{formatDateHe(e.date)}</td>
                  <td className="px-4 py-3 text-slate-600">
                    {e.departureTime || "--"} - {e.returnTime || "--"}
                  </td>
                  <td className="px-4 py-3 text-slate-600">{e.purpose}</td>
                  <td className="px-4 py-3 text-slate-600">{e.crewNames.join(", ") || "--"}</td>
                  <td className="px-4 py-3">
                    <StatusPill positive={e.cleanupDone} yesLabel="בוצע" noLabel="לא בוצע" />
                  </td>
                  <td className="px-4 py-3">
                    <StatusPill positive={e.refuelNeeded} yesLabel="נדרש" noLabel="לא נדרש" invert />
                  </td>
                  <td className="px-4 py-3 text-slate-600">{e.fuelRemaining || "--"}</td>
                  <td className="px-4 py-3">
                    <button
                      onClick={() => removeEntry(e.id)}
                      className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600"
                      aria-label="מחק"
                    >
                      <Trash2 className="size-4" />
                    </button>
                  </td>
                </tr>
              ))}
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={8} className="px-4 py-10 text-center text-slate-400">
                    אין רשומות להצגה
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}

function StatusPill({
  positive,
  yesLabel,
  noLabel,
  invert,
}: {
  positive: boolean;
  yesLabel: string;
  noLabel: string;
  invert?: boolean;
}) {
  const isGood = invert ? !positive : positive;
  return (
    <span
      className={`rounded-full px-2.5 py-1 text-xs font-semibold ${
        isGood ? "bg-emerald-50 text-emerald-700" : "bg-amber-50 text-amber-700"
      }`}
    >
      {positive ? yesLabel : noLabel}
    </span>
  );
}
