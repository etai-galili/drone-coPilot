import { useState } from "react";
import { Sidebar } from "./components/Sidebar";
import { Trip } from "./modules/Trip/Trip";
import { MonthlyOverview } from "./modules/MonthlyOverview/MonthlyOverview";
import { StatusHandover } from "./modules/StatusHandover/StatusHandover";
import { CustomPage } from "./modules/CustomPage/CustomPage";
import { generateId, useLocalStorage } from "./lib/storage";
import type { CustomNavItem } from "./types";

export type ModuleKey = "trip" | "monthly-overview" | "status-handover" | `custom:${string}`;

const CUSTOM_NAV_KEY = "vessel-mng:custom-nav";

function App() {
  const [active, setActive] = useState<ModuleKey>("trip");
  const [customItems, setCustomItems] = useLocalStorage<CustomNavItem[]>(CUSTOM_NAV_KEY, []);

  function addCustomItem(item: Omit<CustomNavItem, "id" | "createdAt">) {
    const newItem: CustomNavItem = { ...item, id: generateId(), createdAt: new Date().toISOString() };
    setCustomItems((prev) => [...prev, newItem]);
    if (newItem.kind === "page") setActive(`custom:${newItem.id}`);
  }

  function deleteCustomItem(id: string) {
    setCustomItems((prev) => prev.filter((c) => c.id !== id));
    if (active === `custom:${id}`) setActive("trip");
  }

  function updateCustomContent(id: string, content: string) {
    setCustomItems((prev) => prev.map((c) => (c.id === id ? { ...c, content } : c)));
  }

  const activeCustomItem = active.startsWith("custom:")
    ? customItems.find((c) => `custom:${c.id}` === active)
    : undefined;

  return (
    <div className="flex min-h-screen flex-row-reverse bg-slate-100">
      <Sidebar
        active={active}
        onSelect={setActive}
        customItems={customItems}
        onAddCustomItem={addCustomItem}
        onDeleteCustomItem={deleteCustomItem}
      />
      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-6 sm:px-6">
        {active === "trip" && <Trip />}
        {active === "monthly-overview" && <MonthlyOverview />}
        {active === "status-handover" && <StatusHandover />}
        {activeCustomItem && (
          <CustomPage
            item={activeCustomItem}
            onChangeContent={(content) => updateCustomContent(activeCustomItem.id, content)}
          />
        )}
      </main>
    </div>
  );
}

export default App;
