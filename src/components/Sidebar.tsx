import { useState } from "react";
import { Anchor, CalendarRange, LayoutGrid, Menu, Users, X } from "lucide-react";
import type { ModuleKey } from "../App";

const NAV_ITEMS: { key: ModuleKey; label: string; icon: typeof Anchor }[] = [
  { key: "trip", label: "Trip", icon: CalendarRange },
  { key: "monthly-overview", label: "סקירה חודשית", icon: LayoutGrid },
  { key: "status-handover", label: "העברת סטטוס", icon: Users },
];

export function Sidebar({
  active,
  onSelect,
}: {
  active: ModuleKey;
  onSelect: (key: ModuleKey) => void;
}) {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <>
      <header className="sticky top-0 z-30 flex items-center justify-between border-b border-cyan-900/40 bg-cyan-950 px-4 py-3 text-white md:hidden">
        <div className="flex items-center gap-2 text-lg font-extrabold tracking-tight">
          <Anchor className="size-6 text-cyan-300" />
          <span>vessel-MNG</span>
        </div>
        <button
          className="rounded-lg p-2 text-cyan-100 hover:bg-white/10"
          onClick={() => setMobileOpen((o) => !o)}
          aria-label="פתח תפריט"
        >
          {mobileOpen ? <X className="size-6" /> : <Menu className="size-6" />}
        </button>
      </header>

      <aside className="hidden w-64 shrink-0 flex-col border-r border-slate-200 bg-white md:flex">
        <SidebarContent active={active} onSelect={onSelect} />
      </aside>

      {mobileOpen && (
        <div className="fixed inset-0 z-40 flex justify-end md:hidden">
          <div
            className="absolute inset-0 bg-black/40"
            onClick={() => setMobileOpen(false)}
            aria-hidden
          />
          <aside className="relative flex w-72 max-w-[80%] flex-col bg-white shadow-xl">
            <SidebarContent
              active={active}
              onSelect={(key) => {
                onSelect(key);
                setMobileOpen(false);
              }}
            />
          </aside>
        </div>
      )}
    </>
  );
}

function SidebarContent({
  active,
  onSelect,
}: {
  active: ModuleKey;
  onSelect: (key: ModuleKey) => void;
}) {
  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center gap-2 border-b border-slate-100 px-5 py-5 text-lg font-extrabold tracking-tight text-cyan-950">
        <Anchor className="size-6 text-cyan-700" />
        <span>vessel-MNG</span>
      </div>

      <nav className="flex flex-col gap-1 p-3">
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
      </nav>
    </div>
  );
}
