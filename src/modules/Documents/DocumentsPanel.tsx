import { useState } from "react";
import { ExternalLink, FileText, Link2, Plus, Trash2, X } from "lucide-react";
import { Field, TextInput } from "../../components/ui/Field";
import { Button } from "../../components/ui/Button";
import { generateId, useLocalStorage } from "../../lib/storage";
import type { DocumentLink } from "../../types";

function storageKey(vesselId: string) {
  return `vessel-mng:${vesselId}:documents`;
}

export function DocumentsPanel({ vesselId, onClose }: { vesselId: string; onClose: () => void }) {
  const [documents, setDocuments] = useLocalStorage<DocumentLink[]>(storageKey(vesselId), []);
  const [title, setTitle] = useState("");
  const [url, setUrl] = useState("");

  function addDocument() {
    const trimmedTitle = title.trim();
    const trimmedUrl = url.trim();
    if (!trimmedTitle || !trimmedUrl) return;
    const doc: DocumentLink = {
      id: generateId(),
      title: trimmedTitle,
      url: trimmedUrl,
      createdAt: new Date().toISOString(),
    };
    setDocuments((prev) => [doc, ...prev]);
    setTitle("");
    setUrl("");
  }

  function removeDocument(id: string) {
    setDocuments((prev) => prev.filter((d) => d.id !== id));
  }

  return (
    <div className="fixed inset-0 z-40 flex">
      <button
        className="flex-1 bg-slate-900/40"
        onClick={onClose}
        aria-label="סגור מסמכים"
      />
      <div className="flex h-full w-full max-w-sm flex-col border-r border-slate-200 bg-white shadow-xl">
        <div className="flex items-center justify-between border-b border-slate-100 p-4">
          <div className="flex items-center gap-2 text-lg font-bold text-slate-800">
            <FileText className="size-5 text-cyan-700" />
            מסמכים וקישורים
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-2 text-slate-400 hover:bg-slate-100 hover:text-slate-700"
            aria-label="סגור"
          >
            <X className="size-5" />
          </button>
        </div>

        <div className="flex flex-col gap-3 border-b border-slate-100 p-4">
          <Field label="כותרת המסמך" required>
            <TextInput
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="לדוגמה: נוהל בטיחות"
            />
          </Field>
          <Field label="קישור (URL)" required>
            <TextInput
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  e.preventDefault();
                  addDocument();
                }
              }}
              placeholder="https://..."
            />
          </Field>
          <Button onClick={addDocument} disabled={!title.trim() || !url.trim()}>
            <Plus className="size-4" />
            הוסף מסמך
          </Button>
        </div>

        <div className="flex-1 overflow-y-auto">
          {documents.length === 0 && (
            <div className="p-10 text-center text-slate-400">אין עדיין מסמכים או קישורים</div>
          )}
          <div className="flex flex-col divide-y divide-slate-100">
            {documents.map((doc) => (
              <div key={doc.id} className="flex items-center justify-between gap-2 p-4">
                <a
                  href={doc.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex min-w-0 flex-1 items-center gap-2 text-sm font-medium text-cyan-700 hover:underline"
                >
                  <Link2 className="size-4 shrink-0" />
                  <span className="truncate">{doc.title}</span>
                  <ExternalLink className="size-3.5 shrink-0 text-cyan-400" />
                </a>
                <button
                  onClick={() => removeDocument(doc.id)}
                  className="shrink-0 rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600"
                  aria-label="מחק מסמך"
                >
                  <Trash2 className="size-4" />
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
