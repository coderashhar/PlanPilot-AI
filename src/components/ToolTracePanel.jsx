"use client";

import { CheckCircle2, Circle, Loader2 } from "lucide-react";

export default function ToolTracePanel({ traces }) {
  if (!traces || traces.length === 0) return null;

  return (
    <div className="mb-4 rounded-xl border border-white/10 bg-black/40 p-4 backdrop-blur-md transition-all duration-300">
      <h3 className="mb-3 text-xs font-semibold uppercase tracking-wider text-gray-400">
        Agent Execution Trace
      </h3>
      <div className="space-y-3">
        {traces.map((trace, idx) => (
          <div key={idx} className="flex items-center gap-3 text-sm">
            {trace.status === "loading" ? (
              <Loader2 className="h-4 w-4 animate-spin text-blue-400" />
            ) : trace.status === "done" ? (
              <CheckCircle2 className="h-4 w-4 text-emerald-400" />
            ) : (
              <Circle className="h-4 w-4 text-gray-600" />
            )}
            <span
              className={`${
                trace.status === "loading"
                  ? "text-blue-200"
                  : trace.status === "done"
                  ? "text-emerald-200"
                  : "text-gray-500"
              }`}
            >
              {trace.name}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
