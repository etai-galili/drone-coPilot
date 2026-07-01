export interface VoyageEntry {
  id: string;
  date: string; // YYYY-MM-DD
  departureTime: string; // HH:MM
  returnTime: string; // HH:MM
  purpose: string;
  crewNames: string[];
  cleanupDone: boolean;
  refuelNeeded: boolean;
  fuelRemaining: string;
  notes: string;
  createdAt: string;
}

export interface ChecklistItemDef {
  id: string;
  label: string;
}

export interface ChecklistItemState {
  id: string;
  checked: boolean;
}

export interface MonthlyEquipmentReport {
  monthKey: string; // YYYY-MM
  items: ChecklistItemState[];
  updatedAt: string;
}

export interface BiweeklyChecklistReport {
  periodKey: string;
  periodStart: string;
  periodEnd: string;
  items: ChecklistItemState[];
  updatedAt: string;
}

export interface StatusHandoverEntry {
  id: string;
  periodKey: string;
  date: string; // YYYY-MM-DD (Thursday of handover)
  outgoingCommander: string;
  incomingCommander: string;
  trainingsCompleted: string;
  openFaults: string;
  openOrders: string;
  equipmentStatus: string;
  importantMessages: string;
  createdAt: string;
}
