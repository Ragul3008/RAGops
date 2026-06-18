"use client";
import React from "react";

interface MetricsPanelProps {
  metrics: {
    faithfulness: number;
    latency: string;
    tokens: number;
  };
}

export function MetricsPanel({ metrics }: MetricsPanelProps) {
  const isFaithful = metrics.faithfulness === 1.0;

  return (
    <div className="rounded-xl border bg-card p-5 shadow-sm space-y-4">
      <div>
        <h3 className="text-lg font-semibold text-foreground">Pipeline Evaluation & Metrics</h3>
        <p className="text-xs text-muted-foreground">Real-time validation of the retrieval quality.</p>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {/* Faithfulness Card */}
        <div className="p-4 border rounded-lg bg-background flex flex-col justify-between">
          <div className="flex justify-between items-start">
            <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Faithfulness
            </span>
            <span
              className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                isFaithful
                  ? "bg-green-500/10 text-green-500 border border-green-500/20"
                  : "bg-red-500/10 text-red-500 border border-red-500/20"
              }`}
            >
              {isFaithful ? "FAITHFUL" : "UNFAITHFUL"}
            </span>
          </div>
          <div className="mt-4 flex items-baseline space-x-2">
            <span className="text-2xl font-bold tracking-tight text-foreground">
              {metrics.faithfulness * 100}%
            </span>
            <span className="text-xs text-muted-foreground">score</span>
          </div>
          <p className="mt-2 text-xs text-muted-foreground leading-normal">
            Verifies if the generated answer is entirely grounded in the retrieved contexts.
          </p>
        </div>

        {/* Latency Card */}
        <div className="p-4 border rounded-lg bg-background flex flex-col justify-between">
          <div className="flex justify-between items-start">
            <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Latency
            </span>
            <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-blue-500/10 text-blue-500 border border-blue-500/20">
              PERFORMANCE
            </span>
          </div>
          <div className="mt-4 flex items-baseline space-x-2">
            <span className="text-2xl font-bold tracking-tight text-foreground">
              {metrics.latency}
            </span>
          </div>
          <p className="mt-2 text-xs text-muted-foreground leading-normal">
            Total round-trip time for embedding generation, vector search, and LLM synthesis.
          </p>
        </div>

        {/* Tokens Card */}
        <div className="p-4 border rounded-lg bg-background flex flex-col justify-between">
          <div className="flex justify-between items-start">
            <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Tokens Used
            </span>
            <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-purple-500/10 text-purple-500 border border-purple-500/20">
              COST
            </span>
          </div>
          <div className="mt-4 flex items-baseline space-x-2">
            <span className="text-2xl font-bold tracking-tight text-foreground">
              {metrics.tokens}
            </span>
            <span className="text-xs text-muted-foreground">tokens</span>
          </div>
          <p className="mt-2 text-xs text-muted-foreground leading-normal">
            Total number of prompt and generation tokens processed by the LLM.
          </p>
        </div>
      </div>
    </div>
  );
}
