import { useState } from "react";
import { Sidebar } from "./components/Sidebar";
import { Trip } from "./modules/Trip/Trip";
import { MonthlyOverview } from "./modules/MonthlyOverview/MonthlyOverview";
import { StatusHandover } from "./modules/StatusHandover/StatusHandover";

export type ModuleKey = "trip" | "monthly-overview" | "status-handover";

function App() {
  const [active, setActive] = useState<ModuleKey>("trip");

  return (
    <div className="flex min-h-screen flex-col bg-slate-100 md:flex-row-reverse">
      <Sidebar active={active} onSelect={setActive} />
      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-6 sm:px-6">
        {active === "trip" && <Trip />}
        {active === "monthly-overview" && <MonthlyOverview />}
        {active === "status-handover" && <StatusHandover />}
      </main>
    </div>
  );
}

export default App;
