import { useState } from "react";
import {
  Anchor,
  CalendarRange,
  ExternalLink,
  FileText,
  LayoutGrid,
  Link as LinkIcon,
  Plus,
  Users,
  X,
} from "lucide-react";
import type { ModuleKey } from "../App";
import type { CustomNavItem } from "../types";

const NAV_ITEMS: { key: ModuleKey; label: string; icon: typeof Anchor }[] = [
  { key: "trip", label: "Trip", icon: CalendarRange },
  { key: "monthly-overview", label: "סקירה חודשית", icon: LayoutGrid },
  { key: "status-handover", label: "העברת סטטוס", icon: Users },
];

export function Sidebar({
  active,
  onSelect,
  customItems,
  onAddCustomItem,
  onDeleteCustomItem,
}: {
  active: ModuleKey;
  onSelect: (key: ModuleKey) => void;
  customItems: CustomNavItem[];
  onAddCustomItem: (item: Omit<CustomNavItem, "id" | "createdAt">) => void;
  onDeleteCustomItem: (id: string) => void;
}) {
  return (
    <aside className="flex w-56 shrink-0 flex-col border-r border-slate-200 bg-white sm:w-64">
      <div className="flex items-center gap-2 border-b border-slate-100 px-5 py-5 text-lg font-extrabold tracking-tight text-cyan-950">
        <Anchor className="size-6 text-cyan-700" />
        <span>vessel-MNG</span>
      </div>

      <nav className="flex flex-1 flex-col gap-1 overflow-y-auto p-3">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive = active === item.key;
          return (
            <button
              key={item.key}
              onClick={() => onSelect(item.key)}
              className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-semibold transition ${
                isActive
                  ? "bg-cyan-700 text-white shadow-sm"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
              }`}
            >
              <Icon className="size-5" />
              {item.label}
            </button>
          );
        })}

        {customItems.length > 0 && <div className="my-2 border-t border-slate-100" />}

        {customItems.map((item) => {
          const key: ModuleKey = `custom:${item.id}`;
          const isActive = active === key;
          return (
            <div key={item.id} className="group flex items-center gap-1">
              <button
                onClick={() =>
                  item.kind === "link"
                    ? window.open(item.url, "_blank", "noopener,noreferrer")
                    : onSelect(key)
                }
                className={`flex flex-1 items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-semibold transition ${
                  isActive
                    ? "bg-cyan-700 text-white shadow-sm"
                    : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                }`}
              >
                {item.kind === "link" ? (
                  <ExternalLink className="size-5 shrink-0" />
                ) : (
                  <FileText className="size-5 shrink-0" />
                )}
                <span className="truncate">{item.label}</span>
              </button>
              <button
                onClick={() => onDeleteCustomItem(item.id)}
                className="rounded-lg p-1.5 text-slate-300 opacity-0 hover:bg-rose-50 hover:text-rose-600 group-hover:opacity-100"
                aria-label="מחק"
              >
                <X className="size-3.5" />
              </button>
            </div>
          );
        })}
      </nav>

      <AddCustomItemForm onAdd={onAddCustomItem} />
    </aside>
  );
}

function AddCustomItemForm({
  onAdd,
}: {
  onAdd: (item: Omit<CustomNavItem, "id" | "createdAt">) => void;
}) {
  const [open, setOpen] = useState(false);
  const [kind, setKind] = useState<"link" | "page">("link");
  const [label, setLabel] = useState("");
  const [url, setUrl] = useState("");

  function submit() {
    if (!label.trim()) return;
    if (kind === "link" && !url.trim()) return;
    onAdd({ kind, label: label.trim(), url: url.trim(), content: "" });
    setLabel("");
    setUrl("");
    setOpen(false);
  }

  if (!open) {
    return (
      <div className="border-t border-slate-100 p-3">
        <button
          onClick={() => setOpen(true)}
          className="flex w-full items-center justify-center gap-2 rounded-lg border border-dashed border-slate-300 px-3 py-2 text-sm font-semibold text-slate-500 hover:border-cyan-400 hover:text-cyan-700"
        >
          <Plus className="size-4" />
          הוסף קישור / עמוד
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-2 border-t border-slate-100 p-3">
      <div className="inline-flex overflow-hidden rounded-lg border border-slate-300 text-xs">
        <button
          type="button"
          onClick={() => setKind("link")}
          className={`flex flex-1 items-center justify-center gap-1 px-2 py-1.5 font-semibold ${
            kind === "link" ? "bg-cyan-700 text-white" : "bg-white text-slate-600"
          }`}
        >
          <LinkIcon className="size-3.5" />
          קישור
        </button>
        <button
          type="button"
          onClick={() => setKind("page")}
          className={`flex flex-1 items-center justify-center gap-1 px-2 py-1.5 font-semibold ${
            kind === "page" ? "bg-cyan-700 text-white" : "bg-white text-slate-600"
          }`}
        >
          <FileText className="size-3.5" />
          עמוד
        </button>
      </div>
      <input
        value={label}
        onChange={(e) => setLabel(e.target.value)}
        placeholder="שם בתפריט"
        className="rounded-lg border border-slate-300 px-2.5 py-1.5 text-sm outline-none focus:border-cyan-600"
      />
      {kind === "link" && (
        <input
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://..."
          className="rounded-lg border border-slate-300 px-2.5 py-1.5 text-sm outline-none focus:border-cyan-600"
        />
      )}
      <div className="flex gap-2">
        <button
          onClick={submit}
          className="flex-1 rounded-lg bg-cyan-700 px-2.5 py-1.5 text-sm font-semibold text-white hover:bg-cyan-800"
        >
          הוסף
        </button>
        <button
          onClick={() => setOpen(false)}
          className="rounded-lg bg-slate-100 px-2.5 py-1.5 text-sm font-semibold text-slate-600 hover:bg-slate-200"
        >
          ביטול
        </button>
      </div>
    </div>
  );
}
