const HEBREW_MONTHS = [
  "ינואר",
  "פברואר",
  "מרץ",
  "אפריל",
  "מאי",
  "יוני",
  "יולי",
  "אוגוסט",
  "ספטמבר",
  "אוקטובר",
  "נובמבר",
  "דצמבר",
];

export function todayISO(): string {
  return toISODate(new Date());
}

export function toISODate(date: Date): string {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

export function formatDateHe(iso: string): string {
  if (!iso) return "";
  const [y, m, d] = iso.split("-");
  return `${d}/${m}/${y}`;
}

export function getMonthKey(date: Date = new Date()): string {
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}`;
}

export function getMonthLabelHe(monthKey: string): string {
  const [y, m] = monthKey.split("-").map(Number);
  return `${HEBREW_MONTHS[m - 1]} ${y}`;
}

// Anchor: Monday, Jan 1 2024 — used to derive stable, non-overlapping 14-day periods.
const BIWEEK_ANCHOR = new Date(2024, 0, 1).getTime();
const MS_PER_DAY = 24 * 60 * 60 * 1000;

export function getPeriodIndex(date: Date = new Date()): number {
  const midnight = new Date(date);
  midnight.setHours(0, 0, 0, 0);
  const diffDays = Math.floor((midnight.getTime() - BIWEEK_ANCHOR) / MS_PER_DAY);
  return Math.floor(diffDays / 14);
}

export function getPeriodKey(date: Date = new Date()): string {
  return `p${getPeriodIndex(date)}`;
}

export function getPeriodRange(periodKey: string): { start: string; end: string } {
  const index = Number(periodKey.slice(1));
  const start = new Date(BIWEEK_ANCHOR + index * 14 * MS_PER_DAY);
  const end = new Date(BIWEEK_ANCHOR + (index * 14 + 13) * MS_PER_DAY);
  return { start: toISODate(start), end: toISODate(end) };
}

export function getCurrentPeriod(): { key: string; start: string; end: string } {
  const key = getPeriodKey();
  const { start, end } = getPeriodRange(key);
  return { key, start, end };
}
