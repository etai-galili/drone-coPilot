import { useState } from "react";
import {
  Anchor,
  CalendarRange,
  ChevronDown,
  ClipboardList,
  FileText,
  ListChecks,
  Menu,
  Settings,
  X,
} from "lucide-react";
import type { ModuleKey } from "../App";
import type { Vessel } from "../types";

const TABS: { key: ModuleKey; label: string; icon: typeof Anchor }[] = [
  { key: "voyage-log", label: "יומן הפלגות", icon: CalendarRange },
  { key: "monthly-equipment", label: "דוח ציוד חודשי", icon: ClipboardList },
  { key: "biweekly-checklist", label: "צ'קליסט דו-שבועי", icon: ListChecks },
  { key: "status-handover", label: "העברת סטטוס", icon: Anchor },
];

export function TopNav({
  active,
  onSelect,
  vessel,
  vessels,
  onSwitchVessel,
  onManageVessels,
  onOpenDocuments,
}: {
  active: ModuleKey;
  onSelect: (key: ModuleKey) => void;
  vessel: Vessel;
  vessels: Vessel[];
  onSwitchVessel: (id: string) => void;
  onManageVessels: () => void;
  onOpenDocuments: () => void;
}) {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="sticky top-0 z-20 border-b border-cyan-900/40 bg-gradient-to-l from-cyan-950 to-slate-900 text-white shadow-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-3 px-4 py-3 sm:px-6">
        <div className="flex items-center gap-2 text-lg font-extrabold tracking-tight">
          <Anchor className="size-6 text-cyan-300" />
          <span>vessel-MNG</span>
        </div>

        <VesselSwitcher
          vessel={vessel}
          vessels={vessels}
          onSwitchVessel={onSwitchVessel}
          onManageVessels={onManageVessels}
        />

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
          <button
            onClick={() => {
              onOpenDocuments();
              setMobileOpen(false);
            }}
            className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-sm font-semibold text-cyan-100/80 transition hover:bg-white/10 hover:text-white"
          >
            <FileText className="size-4" />
            מסמכים
          </button>
        </nav>
      )}
    </header>
  );
}

function VesselSwitcher({
  vessel,
  vessels,
  onSwitchVessel,
  onManageVessels,
}: {
  vessel: Vessel;
  vessels: Vessel[];
  onSwitchVessel: (id: string) => void;
  onManageVessels: () => void;
}) {
  const [open, setOpen] = useState(false);

  return (
    <div className="relative">
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex items-center gap-1.5 rounded-lg bg-white/10 px-3 py-2 text-sm font-semibold text-white transition hover:bg-white/20"
      >
        <span className="max-w-[10rem] truncate">{vessel.name}</span>
        <ChevronDown className="size-4" />
      </button>

      {open && (
        <>
          <button
            className="fixed inset-0 z-10 cursor-default"
            onClick={() => setOpen(false)}
            aria-label="סגור"
          />
          <div className="absolute top-full z-20 mt-1 w-56 overflow-hidden rounded-lg border border-slate-200 bg-white text-right shadow-lg">
            <div className="max-h-64 overflow-y-auto py-1">
              {vessels.map((v) => (
                <button
                  key={v.id}
                  onClick={() => {
                    onSwitchVessel(v.id);
                    setOpen(false);
                  }}
                  className={`flex w-full items-center gap-2 px-3 py-2 text-sm font-medium transition ${
                    v.id === vessel.id
                      ? "bg-cyan-50 text-cyan-800"
                      : "text-slate-700 hover:bg-slate-50"
                  }`}
                >
                  <Anchor className="size-4 shrink-0" />
                  <span className="truncate">{v.name}</span>
                </button>
              ))}
            </div>
            <button
              onClick={() => {
                onManageVessels();
                setOpen(false);
              }}
              className="flex w-full items-center gap-2 border-t border-slate-100 px-3 py-2 text-sm font-medium text-slate-600 hover:bg-slate-50"
            >
              <Settings className="size-4" />
              ניהול כלי שיט
            </button>
          </div>
        </>
      )}
    </div>
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
