import { useRef, useState } from "react";
import type { PointerEvent as ReactPointerEvent, WheelEvent as ReactWheelEvent } from "react";
import { Minus, Plus, RotateCcw } from "lucide-react";

const MIN_SCALE = 1;
const MAX_SCALE = 6;

function clamp(value: number, min: number, max: number) {
  return Math.min(max, Math.max(min, value));
}

interface ViewState {
  scale: number;
  x: number;
  y: number;
}

const INITIAL_VIEW: ViewState = { scale: 1, x: 0, y: 0 };

export function PannableMap({ src, alt }: { src: string; alt: string }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [view, setView] = useState<ViewState>(INITIAL_VIEW);
  const dragState = useRef<{ startX: number; startY: number; origX: number; origY: number } | null>(
    null,
  );

  function clampToBounds(x: number, y: number, scale: number) {
    const el = containerRef.current;
    if (!el) return { x, y };
    const maxX = (el.clientWidth * (scale - 1)) / 2;
    const maxY = (el.clientHeight * (scale - 1)) / 2;
    return { x: clamp(x, -maxX, maxX), y: clamp(y, -maxY, maxY) };
  }

  function zoomBy(factor: number) {
    setView((prev) => {
      const nextScale = clamp(prev.scale * factor, MIN_SCALE, MAX_SCALE);
      const { x, y } = clampToBounds(prev.x, prev.y, nextScale);
      return { scale: nextScale, x, y };
    });
  }

  function reset() {
    setView(INITIAL_VIEW);
  }

  function onPointerDown(e: ReactPointerEvent<HTMLDivElement>) {
    if (view.scale <= 1) return;
    dragState.current = { startX: e.clientX, startY: e.clientY, origX: view.x, origY: view.y };
    e.currentTarget.setPointerCapture(e.pointerId);
  }

  function onPointerMove(e: ReactPointerEvent<HTMLDivElement>) {
    if (!dragState.current) return;
    const dx = e.clientX - dragState.current.startX;
    const dy = e.clientY - dragState.current.startY;
    const { x, y } = clampToBounds(dragState.current.origX + dx, dragState.current.origY + dy, view.scale);
    setView((prev) => ({ ...prev, x, y }));
  }

  function onPointerUp() {
    dragState.current = null;
  }

  function onWheel(e: ReactWheelEvent<HTMLDivElement>) {
    e.preventDefault();
    zoomBy(1 - e.deltaY * 0.0015);
  }

  return (
    <div className="relative h-full w-full overflow-hidden rounded-xl border border-slate-200 bg-slate-100">
      <div
        ref={containerRef}
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerUp}
        onPointerLeave={onPointerUp}
        onWheel={onWheel}
        className="absolute inset-0 touch-none"
        style={{ cursor: view.scale > 1 ? "grab" : "default" }}
      >
        <img
          src={src}
          alt={alt}
          draggable={false}
          className="h-full w-full select-none object-cover"
          style={{
            transform: `translate(${view.x}px, ${view.y}px) scale(${view.scale})`,
            transformOrigin: "center center",
            transition: dragState.current ? "none" : "transform 0.05s linear",
          }}
        />
      </div>

      <div className="pointer-events-none absolute inset-0">
        <div className="pointer-events-auto absolute bottom-3 left-3 flex flex-col gap-1">
          <button
            type="button"
            onClick={() => zoomBy(1.3)}
            className="rounded-lg bg-white/90 p-2 text-slate-700 shadow hover:bg-white"
            aria-label="הגדל"
          >
            <Plus className="size-4" />
          </button>
          <button
            type="button"
            onClick={() => zoomBy(1 / 1.3)}
            className="rounded-lg bg-white/90 p-2 text-slate-700 shadow hover:bg-white"
            aria-label="הקטן"
          >
            <Minus className="size-4" />
          </button>
          <button
            type="button"
            onClick={reset}
            className="rounded-lg bg-white/90 p-2 text-slate-700 shadow hover:bg-white"
            aria-label="איפוס תצוגה"
          >
            <RotateCcw className="size-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
