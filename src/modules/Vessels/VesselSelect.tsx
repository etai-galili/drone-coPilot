import { useState } from "react";
import { Anchor, ArrowLeft, Plus, Trash2 } from "lucide-react";
import { Card, CardHeader } from "../../components/ui/Card";
import { Field, TextInput } from "../../components/ui/Field";
import { Button } from "../../components/ui/Button";
import type { Vessel } from "../../types";

export function VesselSelect({
  vessels,
  onAdd,
  onSelect,
  onDelete,
}: {
  vessels: Vessel[];
  onAdd: (name: string) => void;
  onSelect: (id: string) => void;
  onDelete: (id: string) => void;
}) {
  const [name, setName] = useState("");

  function submit() {
    const trimmed = name.trim();
    if (!trimmed) return;
    onAdd(trimmed);
    setName("");
  }

  return (
    <div className="min-h-screen bg-slate-100">
      <header className="border-b border-cyan-900/40 bg-gradient-to-l from-cyan-950 to-slate-900 px-4 py-4 text-white sm:px-6">
        <div className="mx-auto flex max-w-3xl items-center gap-2 text-lg font-extrabold tracking-tight">
          <Anchor className="size-6 text-cyan-300" />
          <span>vessel-MNG</span>
        </div>
      </header>

      <main className="mx-auto max-w-3xl px-4 py-8 sm:px-6">
        <Card className="mb-6">
          <CardHeader title="בחירת כלי שיט" subtitle="בחרו כלי שיט קיים או הוסיפו כלי שיט חדש" />
          <div className="flex flex-col divide-y divide-slate-100">
            {vessels.map((vessel) => (
              <div key={vessel.id} className="flex items-center justify-between gap-3 p-4">
                <div className="flex items-center gap-3">
                  <span className="flex size-10 items-center justify-center rounded-full bg-cyan-50 text-cyan-700">
                    <Anchor className="size-5" />
                  </span>
                  <span className="text-sm font-bold text-slate-800">{vessel.name}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Button onClick={() => onSelect(vessel.id)}>
                    כניסה
                    <ArrowLeft className="size-4" />
                  </Button>
                  <button
                    onClick={() => onDelete(vessel.id)}
                    className="rounded-lg p-2 text-slate-400 hover:bg-rose-50 hover:text-rose-600"
                    aria-label="מחק כלי שיט"
                  >
                    <Trash2 className="size-4" />
                  </button>
                </div>
              </div>
            ))}
            {vessels.length === 0 && (
              <div className="p-10 text-center text-slate-400">אין עדיין כלי שיט רשומים</div>
            )}
          </div>
        </Card>

        <Card>
          <CardHeader title="הוספת כלי שיט חדש" />
          <div className="flex flex-wrap items-end gap-3 p-4 sm:p-5">
            <div className="min-w-[220px] flex-1">
              <Field label="שם כלי השיט" required>
                <TextInput
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault();
                      submit();
                    }
                  }}
                  placeholder="לדוגמה: רס״ן 3"
                />
              </Field>
            </div>
            <Button onClick={submit} disabled={!name.trim()}>
              <Plus className="size-4" />
              הוסף כלי שיט
            </Button>
          </div>
        </Card>
      </main>
    </div>
  );
}
