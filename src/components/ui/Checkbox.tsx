export function Checkbox({
  checked,
  onChange,
  label,
}: {
  checked: boolean;
  onChange: (checked: boolean) => void;
  label: string;
}) {
  return (
    <label className="flex cursor-pointer items-center gap-3 rounded-lg border border-slate-200 bg-slate-50 px-4 py-3 transition hover:bg-slate-100">
      <input
        type="checkbox"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        className="size-5 rounded border-slate-300 text-cyan-700 focus:ring-cyan-600"
      />
      <span
        className={`text-sm font-medium ${checked ? "text-slate-400 line-through" : "text-slate-700"}`}
      >
        {label}
      </span>
    </label>
  );
}
