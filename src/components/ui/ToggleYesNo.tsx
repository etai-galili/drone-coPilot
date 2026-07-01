export function ToggleYesNo({
  value,
  onChange,
}: {
  value: boolean;
  onChange: (value: boolean) => void;
}) {
  return (
    <div className="inline-flex overflow-hidden rounded-lg border border-slate-300">
      <button
        type="button"
        onClick={() => onChange(true)}
        className={`px-4 py-2 text-sm font-semibold transition ${
          value ? "bg-cyan-700 text-white" : "bg-white text-slate-600 hover:bg-slate-50"
        }`}
      >
        כן
      </button>
      <button
        type="button"
        onClick={() => onChange(false)}
        className={`px-4 py-2 text-sm font-semibold transition ${
          !value ? "bg-slate-700 text-white" : "bg-white text-slate-600 hover:bg-slate-50"
        }`}
      >
        לא
      </button>
    </div>
  );
}
