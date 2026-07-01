import type { ChecklistItemDef } from "../types";

export const MONTHLY_EQUIPMENT_ITEMS: ChecklistItemDef[] = [
  { id: "fire-extinguishers", label: "מטפי כיבוי אש – תקינות ותוקף" },
  { id: "life-jackets", label: "אפודי הצלה – מצאי ותקינות" },
  { id: "life-rings", label: "גלגלי הצלה" },
  { id: "first-aid-kit", label: "ערכת עזרה ראשונה" },
  { id: "flares-signal", label: "פנסים / אמצעי איתות" },
  { id: "vhf-radio", label: "רדיו VHF" },
  { id: "compass", label: "מצפן" },
  { id: "anchor-chain", label: "עוגן ושרשרת" },
  { id: "bilge-pump", label: "משאבת מים / תא מנוע" },
  { id: "main-power-cutoff", label: "מנתק חשמלי ראשי" },
  { id: "fuel-tank", label: "בוכנת דלק ומכלים" },
  { id: "repair-kit", label: "ערכת כלי תיקונים" },
];

export const BIWEEKLY_MAINTENANCE_ITEMS: ChecklistItemDef[] = [
  { id: "engine-oil", label: "בדיקת שמן מנוע" },
  { id: "fuel-filter", label: "בדיקת מסנן דלק" },
  { id: "batteries", label: "בדיקת מצברים" },
  { id: "belts", label: "בדיקת רצועות הינע" },
  { id: "cooling-system", label: "בדיקת מערכת קירור" },
  { id: "steering", label: "בדיקת מערכת הגה" },
  { id: "hull-cleaning", label: "ניקוי תחתית כלי השיט" },
  { id: "lighting", label: "בדיקת תאורה" },
  { id: "ropes-mooring", label: "בדיקת חבלים ומעגנים" },
  { id: "extinguishers-check", label: "בדיקת מטפי כיבוי אש" },
];
