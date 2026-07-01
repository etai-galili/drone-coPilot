export interface TripEntry {
  id: string;
  date: string; // YYYY-MM-DD
  departureTime: string; // HH:MM
  returnTime: string; // HH:MM
  missionType: string;
  crewNames: string[];
  distanceNm: string;
  fuelConsumed: string;
  fuelRemaining: string;
  cleanupDone: boolean;
  refuelNeeded: boolean;
  notes: string;
  createdAt: string;
}

export interface MonthlyOverviewEntry {
  done: boolean;
  fileLink: string;
  updatedAt: string;
}

export interface CustomNavItem {
  id: string;
  kind: "link" | "page";
  label: string;
  url: string; // used when kind === "link"
  content: string; // used when kind === "page"
  createdAt: string;
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
