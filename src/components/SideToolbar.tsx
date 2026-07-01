import type { ReactNode } from "react";
import { FileText } from "lucide-react";

export function SideToolbar({ onOpenDocuments }: { onOpenDocuments: () => void }) {
  return (
    <aside className="fixed inset-y-0 left-0 z-30 hidden w-16 flex-col items-center gap-2 border-r border-slate-200 bg-white py-4 shadow-sm md:flex">
      <ToolbarButton label="מסמכים" onClick={onOpenDocuments}>
        <FileText className="size-5" />
      </ToolbarButton>
    </aside>
  );
}

function ToolbarButton({
  label,
  onClick,
  children,
}: {
  label: string;
  onClick: () => void;
  children: ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      className="flex w-full flex-col items-center gap-1 px-1 py-2.5 text-slate-500 transition hover:bg-cyan-50 hover:text-cyan-700"
      title={label}
    >
      {children}
      <span className="text-[11px] font-semibold leading-none">{label}</span>
    </button>
  );
}
