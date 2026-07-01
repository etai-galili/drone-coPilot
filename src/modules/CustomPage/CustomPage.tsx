import { Card, CardHeader } from "../../components/ui/Card";
import { TextArea } from "../../components/ui/Field";
import type { CustomNavItem } from "../../types";

export function CustomPage({
  item,
  onChangeContent,
}: {
  item: CustomNavItem;
  onChangeContent: (content: string) => void;
}) {
  return (
    <Card>
      <CardHeader title={item.label} subtitle="עמוד עצמאי" />
      <div className="p-4 sm:p-5">
        <TextArea
          value={item.content}
          onChange={(e) => onChangeContent(e.target.value)}
          placeholder="כתבו כאן כל תוכן שתרצו..."
          style={{ minHeight: "60vh" }}
        />
      </div>
    </Card>
  );
}
