import { useMemo, useState } from "react";
import { Fuel, Gauge, Plus, Trash2, X } from "lucide-react";
import { Card, CardHeader } from "../../components/ui/Card";
import { Field, TextArea, TextInput } from "../../components/ui/Field";
import { Button } from "../../components/ui/Button";
import { ToggleYesNo } from "../../components/ui/ToggleYesNo";
import { StatCard } from "../../components/ui/StatCard";
import { MapPanel } from "../../components/MapPanel";
import { generateId, useLocalStorage } from "../../lib/storage";
import { formatDateHe, toISODate, todayISO } from "../../lib/dateUtils";
import type { TripEntry } from "../../types";

const STORAGE_KEY = "vessel-mng:trip-log";

function emptyDraft(): Omit<TripEntry, "id" | "createdAt"> {
  return {
    date: todayISO(),
    departureTime: "",
    returnTime: "",
    missionType: "",
    crewNames: [],
    distanceNm: "",
    fuelConsumed: "",
    fuelRemaining: "",
    cleanupDone: false,
    refuelNeeded: false,
    notes: "",
  };
}

export function Trip() {
  const [entries, setEntries] = useLocalStorage<TripEntry[]>(STORAGE_KEY, []);
  const [draft, setDraft] = useState(emptyDraft());
  const [crewInput, setCrewInput] = useState("");
  const [fromFilter, setFromFilter] = useState("");
  const [toFilter, setToFilter] = useState("");
  const [returnDraft, setReturnDraft] = useState("");

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
    if (!draft.date || !draft.missionType) return;
    const entry: TripEntry = {
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

  const sorted = useMemo(
    () => [...entries].sort((a, b) => (a.date < b.date ? 1 : -1)),
    [entries],
  );

  const activeTrip = useMemo(
    () => sorted.find((e) => e.departureTime && !e.returnTime),
    [sorted],
  );

  function markReturned() {
    if (!activeTrip || !returnDraft) return;
    setEntries((prev) =>
      prev.map((e) => (e.id === activeTrip.id ? { ...e, returnTime: returnDraft } : e)),
    );
    setReturnDraft("");
  }

  const filtered = useMemo(() => {
    return sorted
      .filter((e) => (fromFilter ? e.date >= fromFilter : true))
      .filter((e) => (toFilter ? e.date <= toFilter : true));
  }, [sorted, fromFilter, toFilter]);

  const last7 = useMemo(() => {
    const cutoff = toISODate(new Date(Date.now() - 6 * 24 * 60 * 60 * 1000));
    return entries.filter((e) => e.date >= cutoff);
  }, [entries]);

  const totalDistance = last7.reduce((sum, e) => sum + (Number(e.distanceNm) || 0), 0);
  const totalFuel = last7.reduce((sum, e) => sum + (Number(e.fuelConsumed) || 0), 0);

  return (
    <div className="flex flex-col gap-6">
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader title="מסלול פעיל" subtitle="ההפלגה האחרונה שטרם הסתיימה" />
          <div className="p-4 sm:p-5">
            <MapPanel
              isActive={!!activeTrip}
              missionType={activeTrip?.missionType}
              departureTime={activeTrip?.departureTime}
              eta={activeTrip?.returnTime}
            />
            {activeTrip && (
              <div className="mt-4 flex flex-wrap items-end gap-2">
                <Field label="עדכון שעת חזרה בפועל">
                  <TextInput
                    type="time"
                    value={returnDraft}
                    onChange={(e) => setReturnDraft(e.target.value)}
                    className="w-auto"
                  />
                </Field>
                <Button variant="secondary" onClick={markReturned} disabled={!returnDraft}>
                  סמן כשבה לנמל
                </Button>
              </div>
            )}
          </div>
        </Card>

        <div className="flex flex-col gap-4">
          <StatCard
            icon={<Gauge className="size-5" />}
            label="מרחק כולל (7 ימים)"
            value={totalDistance.toLocaleString("he-IL")}
            unit="נ״מ"
          />
          <StatCard
            icon={<Fuel className="size-5" />}
            label="דלק שנצרך (7 ימים)"
            value={totalFuel.toLocaleString("he-IL")}
            unit="ליטר"
          />
        </div>
      </div>

      <Card>
        <CardHeader title="יומן הפלגה חדש" subtitle="Trip — רישום הפלגה חדשה" />
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

          <Field label="סוג משימה" required>
            <TextInput
              value={draft.missionType}
              onChange={(e) => setDraft((d) => ({ ...d, missionType: e.target.value }))}
              placeholder="לדוגמה: אימון ניווט, סיור שגרתי..."
            />
          </Field>

          <Field label="מרחק (נ״מ)">
            <TextInput
              type="number"
              inputMode="decimal"
              value={draft.distanceNm}
              onChange={(e) => setDraft((d) => ({ ...d, distanceNm: e.target.value }))}
              placeholder="0"
            />
          </Field>
          <Field label="דלק שנצרך (ליטר)">
            <TextInput
              type="number"
              inputMode="decimal"
              value={draft.fuelConsumed}
              onChange={(e) => setDraft((d) => ({ ...d, fuelConsumed: e.target.value }))}
              placeholder="0"
            />
          </Field>

          <Field label="כמה דלק נשאר">
            <TextInput
              value={draft.fuelRemaining}
              onChange={(e) => setDraft((d) => ({ ...d, fuelRemaining: e.target.value }))}
              placeholder="לדוגמה: 75%, 120 ליטר"
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
          <Button onClick={submit} disabled={!draft.date || !draft.missionType}>
            שמור הפלגה
          </Button>
        </div>
      </Card>

      <Card>
        <CardHeader
          title="הפלגות אחרונות"
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
          <table className="w-full min-w-[780px] text-right text-sm">
            <thead className="bg-slate-50 text-slate-500">
              <tr>
                <th className="px-4 py-3 font-semibold">תאריך</th>
                <th className="px-4 py-3 font-semibold">סוג משימה</th>
                <th className="px-4 py-3 font-semibold">יציאה - חזרה</th>
                <th className="px-4 py-3 font-semibold">מרחק (נ״מ)</th>
                <th className="px-4 py-3 font-semibold">דלק שנצרך (L)</th>
                <th className="px-4 py-3 font-semibold">מפליגים</th>
                <th className="px-4 py-3 font-semibold"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filtered.map((e) => (
                <tr key={e.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-medium text-slate-800">{formatDateHe(e.date)}</td>
                  <td className="px-4 py-3 text-slate-600">{e.missionType}</td>
                  <td dir="ltr" className="px-4 py-3 text-right text-slate-600">
                    {e.departureTime || "--"} - {e.returnTime || "בהפלגה"}
                  </td>
                  <td className="px-4 py-3 text-slate-600">{e.distanceNm || "--"}</td>
                  <td className="px-4 py-3 text-slate-600">{e.fuelConsumed || "--"}</td>
                  <td className="px-4 py-3 text-slate-600">{e.crewNames.join(", ") || "--"}</td>
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
                  <td colSpan={7} className="px-4 py-10 text-center text-slate-400">
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
