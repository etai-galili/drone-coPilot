import { useState } from "react";
import { Anchor, CalendarRange, ClipboardList, ListChecks, Menu, X } from "lucide-react";
import type { ModuleKey } from "../App";

const TABS: { key: ModuleKey; label: string; icon: typeof Anchor }[] = [
  { key: "voyage-log", label: "יומן הפלגות", icon: CalendarRange },
  { key: "monthly-equipment", label: "דוח ציוד חודשי", icon: ClipboardList },
  { key: "biweekly-checklist", label: "צ'קליסט דו-שבועי", icon: ListChecks },
  { key: "status-handover", label: "העברת סטטוס", icon: Anchor },
];

export function TopNav({
  active,
  onSelect,
}: {
  active: ModuleKey;
  onSelect: (key: ModuleKey) => void;
}) {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="sticky top-0 z-20 border-b border-cyan-900/40 bg-gradient-to-l from-cyan-950 to-slate-900 text-white shadow-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6">
        <div className="flex items-center gap-2 text-lg font-extrabold tracking-tight">
          <Anchor className="size-6 text-cyan-300" />
          <span>vessel-MNG</span>
        </div>

        <nav className="hidden items-center gap-1 md:flex">
          {TABS.map((tab) => (
            <TabButton key={tab.key} tab={tab} active={active === tab.key} onSelect={onSelect} />
          ))}
        </nav>

        <button
          className="rounded-lg p-2 text-cyan-100 hover:bg-white/10 md:hidden"
          onClick={() => setMobileOpen((o) => !o)}
          aria-label="פתח תפריט"
        >
          {mobileOpen ? <X className="size-6" /> : <Menu className="size-6" />}
        </button>
      </div>

      {mobileOpen && (
        <nav className="flex flex-col gap-1 border-t border-white/10 bg-cyan-950/95 px-4 py-3 md:hidden">
          {TABS.map((tab) => (
            <TabButton
              key={tab.key}
              tab={tab}
              active={active === tab.key}
              onSelect={(key) => {
                onSelect(key);
                setMobileOpen(false);
              }}
              fullWidth
            />
          ))}
        </nav>
      )}
    </header>
  );
}

function TabButton({
  tab,
  active,
  onSelect,
  fullWidth,
}: {
  tab: { key: ModuleKey; label: string; icon: typeof Anchor };
  active: boolean;
  onSelect: (key: ModuleKey) => void;
  fullWidth?: boolean;
}) {
  const Icon = tab.icon;
  return (
    <button
      onClick={() => onSelect(tab.key)}
      className={`flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-semibold transition ${
        fullWidth ? "w-full justify-start" : ""
      } ${
        active
          ? "bg-cyan-600/90 text-white shadow-inner"
          : "text-cyan-100/80 hover:bg-white/10 hover:text-white"
      }`}
    >
      <Icon className="size-4" />
      {tab.label}
    </button>
  );
}
