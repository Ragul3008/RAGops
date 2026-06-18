"use client";
import React from "react";
import { usePlaygroundStore } from "@/lib/store";

export function ConfigPanel() {
  const { llmProvider, promptVersion, setLlmProvider, setPromptVersion } = usePlaygroundStore();

  return (
    <div className="w-80 border-r bg-card p-6 flex flex-col justify-between">
      <div className="space-y-6">
        <div>
          <h2 className="text-lg font-semibold tracking-tight text-foreground">Configuration</h2>
          <p className="text-xs text-muted-foreground">Adjust RAG parameters and LLM settings.</p>
        </div>

        <div className="space-y-4">
          {/* LLM Provider */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              LLM Provider
            </label>
            <select
              value={llmProvider}
              onChange={(e) => setLlmProvider(e.target.value)}
              className="w-full rounded-md border bg-background px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
            >
              <option value="gemini">Google Gemini</option>
              <option value="openai">OpenAI GPT-4</option>
              <option value="ollama">Ollama Qwen3 8B</option>
            </select>
          </div>

          {/* Prompt Version */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Prompt Version
            </label>
            <select
              value={promptVersion}
              onChange={(e) => setPromptVersion(e.target.value)}
              className="w-full rounded-md border bg-background px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
            >
              <option value="v1">v1 (Strict Grounding)</option>
              <option value="v2">v2 (Flexible Generation)</option>
            </select>
          </div>

          {/* System Prompt View */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Active System Prompt
            </label>
            <div className="rounded-md border bg-muted p-2.5 text-xs font-mono max-h-48 overflow-y-auto leading-relaxed text-muted-foreground">
              {promptVersion === "v1" 
                ? "You are a helpful fact-based assistant. Answer the query ONLY using the provided context. If the context is empty, does not contain the answer, or if you cannot find the answer in the context, respond strictly with: 'I do not have the context to answer this query.'"
                : "You are a helpful assistant. Answer the query using the context when available, or fall back to general knowledge if needed."}
            </div>
          </div>
        </div>
      </div>

      <div className="pt-4 border-t text-center">
        <span className="text-[10px] uppercase font-mono tracking-widest text-muted-foreground">
          RAGOps Playground v1.0
        </span>
      </div>
    </div>
  );
}
