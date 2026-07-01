import { useState } from "react";
import { TopNav } from "./components/TopNav";
import { VoyageLog } from "./modules/VoyageLog/VoyageLog";
import { MonthlyEquipmentReport } from "./modules/MonthlyEquipment/MonthlyEquipmentReport";
import { BiweeklyChecklist } from "./modules/BiweeklyChecklist/BiweeklyChecklist";
import { StatusHandover } from "./modules/StatusHandover/StatusHandover";

export type ModuleKey =
  | "voyage-log"
  | "monthly-equipment"
  | "biweekly-checklist"
  | "status-handover";

function App() {
  const [active, setActive] = useState<ModuleKey>("voyage-log");

  return (
    <div className="min-h-screen bg-slate-100">
      <TopNav active={active} onSelect={setActive} />
      <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6">
        {active === "voyage-log" && <VoyageLog />}
        {active === "monthly-equipment" && <MonthlyEquipmentReport />}
        {active === "biweekly-checklist" && <BiweeklyChecklist />}
        {active === "status-handover" && <StatusHandover />}
      </main>
    </div>
  );
}

export default App;
