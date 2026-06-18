"use client";
import { useState } from "react";
import { QueryInput }    from "@/components/playground/query-input";
import { ContextViewer } from "@/components/playground/context-viewer";
import { AnswerPanel }   from "@/components/playground/answer-panel";
import { MetricsPanel }  from "@/components/playground/metrics-panel";
import { ConfigPanel }   from "@/components/playground/config-panel";

export default function PlaygroundPage() {
  const [result, setResult] = useState(null);
  return (
    <div className="flex h-screen">
      <ConfigPanel />
      <div className="flex-1 p-6 space-y-4">
        <QueryInput onResult={setResult} />
        {result && (
          <>
            <div className="grid grid-cols-2 gap-4">
              <ContextViewer contexts={result.contexts} />
              <AnswerPanel answer={result.answer} />
            </div>
            <MetricsPanel metrics={result.metrics} />
          </>
        )}
      </div>
    </div>
  );
}