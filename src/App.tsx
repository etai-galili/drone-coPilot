import { useState } from "react";
import { TopNav } from "./components/TopNav";
import { SideToolbar } from "./components/SideToolbar";
import { VesselSelect } from "./modules/Vessels/VesselSelect";
import { DocumentsPanel } from "./modules/Documents/DocumentsPanel";
import { VoyageLog } from "./modules/VoyageLog/VoyageLog";
import { MonthlyEquipmentReport } from "./modules/MonthlyEquipment/MonthlyEquipmentReport";
import { BiweeklyChecklist } from "./modules/BiweeklyChecklist/BiweeklyChecklist";
import { StatusHandover } from "./modules/StatusHandover/StatusHandover";
import { generateId, useLocalStorage } from "./lib/storage";
import type { Vessel } from "./types";

export type ModuleKey =
  | "voyage-log"
  | "monthly-equipment"
  | "biweekly-checklist"
  | "status-handover";

const VESSELS_KEY = "vessel-mng:vessels";
const ACTIVE_VESSEL_KEY = "vessel-mng:active-vessel-id";

function App() {
  const [vessels, setVessels] = useLocalStorage<Vessel[]>(VESSELS_KEY, []);
  const [activeVesselId, setActiveVesselId] = useLocalStorage<string | null>(
    ACTIVE_VESSEL_KEY,
    null,
  );
  const [active, setActive] = useState<ModuleKey>("voyage-log");
  const [documentsOpen, setDocumentsOpen] = useState(false);

  const activeVessel = vessels.find((v) => v.id === activeVesselId) ?? null;

  function addVessel(name: string) {
    const vessel: Vessel = { id: generateId(), name, createdAt: new Date().toISOString() };
    setVessels((prev) => [...prev, vessel]);
    setActiveVesselId(vessel.id);
  }

  function removeVessel(id: string) {
    setVessels((prev) => prev.filter((v) => v.id !== id));
    if (activeVesselId === id) setActiveVesselId(null);
  }

  function selectVessel(id: string) {
    setActiveVesselId(id);
  }

  if (!activeVessel) {
    return (
      <VesselSelect
        vessels={vessels}
        onAdd={addVessel}
        onSelect={selectVessel}
        onDelete={removeVessel}
      />
    );
  }

  return (
    <div className="min-h-screen bg-slate-100">
      <SideToolbar onOpenDocuments={() => setDocumentsOpen(true)} />
      <div className="md:pl-16">
        <TopNav
          active={active}
          onSelect={setActive}
          vessel={activeVessel}
          vessels={vessels}
          onSwitchVessel={selectVessel}
          onManageVessels={() => setActiveVesselId(null)}
          onOpenDocuments={() => setDocumentsOpen(true)}
        />
        <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6">
          {active === "voyage-log" && <VoyageLog vesselId={activeVessel.id} />}
          {active === "monthly-equipment" && <MonthlyEquipmentReport vesselId={activeVessel.id} />}
          {active === "biweekly-checklist" && <BiweeklyChecklist vesselId={activeVessel.id} />}
          {active === "status-handover" && <StatusHandover vesselId={activeVessel.id} />}
        </main>
      </div>

      {documentsOpen && (
        <DocumentsPanel vesselId={activeVessel.id} onClose={() => setDocumentsOpen(false)} />
      )}
    </div>
  );
}

export default App;
