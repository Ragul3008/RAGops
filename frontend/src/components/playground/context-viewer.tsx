"use client";
import React from "react";

interface ContextViewerProps {
  contexts: string[];
}

export function ContextViewer({ contexts }: ContextViewerProps) {
  return (
    <div className="rounded-xl border bg-card p-5 shadow-sm space-y-4 flex flex-col h-[400px]">
      <div>
        <h3 className="text-lg font-semibold text-foreground">Retrieved Context</h3>
        <p className="text-xs text-muted-foreground">
          Sources retrieved from the local vector store ({contexts.length} chunks).
        </p>
      </div>

      <div className="flex-1 overflow-y-auto space-y-3 pr-1">
        {contexts.length === 0 ? (
          <div className="h-full flex items-center justify-center text-sm text-muted-foreground italic border border-dashed rounded-lg">
            No context retrieved.
          </div>
        ) : (
          contexts.map((ctx, idx) => (
            <div key={idx} className="p-3 border rounded-lg bg-background text-sm leading-relaxed text-foreground font-light hover:border-muted-foreground/30 transition-colors">
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-[10px] uppercase font-mono tracking-wider text-muted-foreground bg-muted px-1.5 py-0.5 rounded">
                  Chunk #{idx + 1}
                </span>
              </div>
              <p className="whitespace-pre-wrap">{ctx}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
