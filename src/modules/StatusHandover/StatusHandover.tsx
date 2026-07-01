import { useState } from "react";
import { FileDown } from "lucide-react";
import { Card, CardHeader } from "../../components/ui/Card";
import { Field, TextArea, TextInput } from "../../components/ui/Field";
import { Button } from "../../components/ui/Button";
import { generateId, useLocalStorage } from "../../lib/storage";
import { formatDateHe, getPeriodKey, todayISO } from "../../lib/dateUtils";
import type { StatusHandoverEntry } from "../../types";
import { PrintableHandover } from "./PrintableHandover";

function storageKey(vesselId: string) {
  return `vessel-mng:${vesselId}:status-handover`;
}

function emptyDraft(): Omit<StatusHandoverEntry, "id" | "createdAt" | "periodKey"> {
  return {
    date: todayISO(),
    outgoingCommander: "",
    incomingCommander: "",
    trainingsCompleted: "",
    openFaults: "",
    openOrders: "",
    equipmentStatus: "",
    importantMessages: "",
  };
}

export function StatusHandover({ vesselId }: { vesselId: string }) {
  const [entries, setEntries] = useLocalStorage<StatusHandoverEntry[]>(storageKey(vesselId), []);
  const [draft, setDraft] = useState(emptyDraft());
  const [printEntry, setPrintEntry] = useState<StatusHandoverEntry | null>(null);

  function submit() {
    if (!draft.date || !draft.outgoingCommander || !draft.incomingCommander) return;
    const entry: StatusHandoverEntry = {
      ...draft,
      id: generateId(),
      periodKey: getPeriodKey(new Date(draft.date)),
      createdAt: new Date().toISOString(),
    };
    setEntries((prev) => [entry, ...prev]);
    setDraft(emptyDraft());
  }

  function removeEntry(id: string) {
    setEntries((prev) => prev.filter((e) => e.id !== id));
  }

  function exportPdf(entry: StatusHandoverEntry) {
    setPrintEntry(entry);
    setTimeout(() => {
      window.print();
    }, 50);
  }

  const sorted = [...entries].sort((a, b) => (a.date < b.date ? 1 : -1));

  return (
    <div className="flex flex-col gap-6">
      <Card>
        <CardHeader
          title="העברת סטטוס"
          subtitle="טופס דו-שבועי — יום חמישי"
        />
        <div className="grid grid-cols-1 gap-4 p-4 sm:grid-cols-2 sm:p-5">
          <Field label="תאריך" required>
            <TextInput
              type="date"
              value={draft.date}
              onChange={(e) => setDraft((d) => ({ ...d, date: e.target.value }))}
            />
          </Field>
          <div />

          <Field label="שם משיט מוסר" required>
            <TextInput
              value={draft.outgoingCommander}
              onChange={(e) => setDraft((d) => ({ ...d, outgoingCommander: e.target.value }))}
              placeholder="לדוגמה: מפקד 40"
            />
          </Field>
          <Field label="שם משיט מקבל" required>
            <TextInput
              value={draft.incomingCommander}
              onChange={(e) => setDraft((d) => ({ ...d, incomingCommander: e.target.value }))}
            />
          </Field>

          <div className="sm:col-span-2">
            <Field label="אימונים שבוצעו">
              <TextArea
                value={draft.trainingsCompleted}
                onChange={(e) => setDraft((d) => ({ ...d, trainingsCompleted: e.target.value }))}
              />
            </Field>
          </div>
          <div className="sm:col-span-2">
            <Field label="תקלות פתוחות">
              <TextArea
                value={draft.openFaults}
                onChange={(e) => setDraft((d) => ({ ...d, openFaults: e.target.value }))}
              />
            </Field>
          </div>
          <div className="sm:col-span-2">
            <Field label="הזמנות פתוחות">
              <TextArea
                value={draft.openOrders}
                onChange={(e) => setDraft((d) => ({ ...d, openOrders: e.target.value }))}
              />
            </Field>
          </div>
          <div className="sm:col-span-2">
            <Field label="סטטוס כלים">
              <TextArea
                value={draft.equipmentStatus}
                onChange={(e) => setDraft((d) => ({ ...d, equipmentStatus: e.target.value }))}
              />
            </Field>
          </div>
          <div className="sm:col-span-2">
            <Field label="הודעות חשובות">
              <TextArea
                value={draft.importantMessages}
                onChange={(e) => setDraft((d) => ({ ...d, importantMessages: e.target.value }))}
              />
            </Field>
          </div>
        </div>
        <div className="flex justify-end border-t border-slate-100 p-4 sm:p-5">
          <Button
            onClick={submit}
            disabled={!draft.date || !draft.outgoingCommander || !draft.incomingCommander}
          >
            שמור העברת סטטוס
          </Button>
        </div>
      </Card>

      <Card>
        <CardHeader title="היסטוריית העברות" subtitle={`${sorted.length} רשומות`} />
        <div className="flex flex-col divide-y divide-slate-100">
          {sorted.map((entry) => (
            <div key={entry.id} className="flex flex-wrap items-center justify-between gap-3 p-4">
              <div>
                <div className="text-sm font-bold text-slate-800">{formatDateHe(entry.date)}</div>
                <div className="text-sm text-slate-500">
                  {entry.outgoingCommander} ➜ {entry.incomingCommander}
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Button variant="secondary" onClick={() => exportPdf(entry)}>
                  <FileDown className="size-4" />
                  ייצוא PDF
                </Button>
                <Button variant="ghost" onClick={() => removeEntry(entry.id)}>
                  מחק
                </Button>
              </div>
            </div>
          ))}
          {sorted.length === 0 && (
            <div className="p-10 text-center text-slate-400">אין העברות סטטוס עדיין</div>
          )}
        </div>
      </Card>

      {printEntry && (
        <div id="print-area" className="hidden print:block">
          <PrintableHandover entry={printEntry} />
        </div>
      )}
    </div>
  );
}
