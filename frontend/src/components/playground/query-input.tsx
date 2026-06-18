"use client";
import React, { useState } from "react";
import axios from "axios";
import { usePlaygroundStore } from "@/lib/store";

interface QueryInputProps {
  onResult: (result: any) => void;
}

export function QueryInput({ onResult }: QueryInputProps) {
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const { llmProvider, promptVersion } = usePlaygroundStore();

  const handleSend = async () => {
    if (!query.trim()) return;
    setIsLoading(true);
    setError(null);

    try {
      // POST directly to the RAG Engine service running on port 8003
      const response = await axios.post("http://127.0.0.1:8003/api/v1/query", {
        query: query.trim(),
        tenant_id: "00000000-0000-0000-0000-000000000000",
        llm_provider: llmProvider,
        prompt_version: promptVersion,
      });

      // Prepare result state
      onResult({
        answer: response.data.answer,
        contexts: response.data.contexts,
        metrics: {
          faithfulness: response.data.faithful ? 1.0 : 0.0,
          latency: "7.87s", // hardcoded / mock latency representation
          tokens: 232,
        }
      });
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || err.message || "Failed to process query.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="rounded-xl border bg-card p-5 shadow-sm space-y-4">
      <div className="flex flex-col space-y-1.5">
        <h3 className="text-lg font-semibold text-foreground">Playground Query</h3>
        <p className="text-xs text-muted-foreground">Test the retrieval and generation pipeline.</p>
      </div>

      <div className="flex gap-3">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question about the uploaded documents (e.g. 'what is ragul's education qualification from uploaded resume')"
          rows={3}
          className="flex-1 rounded-lg border bg-background px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring resize-none leading-relaxed"
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
        />
        <button
          onClick={handleSend}
          disabled={isLoading || !query.trim()}
          className="px-6 rounded-lg bg-primary text-primary-foreground font-medium text-sm transition-colors hover:bg-primary/90 disabled:opacity-50 flex items-center justify-center min-w-[100px]"
        >
          {isLoading ? (
            <span className="w-5 h-5 border-2 border-primary-foreground border-t-transparent rounded-full animate-spin"></span>
          ) : (
            "Send"
          )}
        </button>
      </div>

      {error && (
        <div className="p-3 text-xs bg-destructive/10 border border-destructive/20 text-destructive rounded-lg font-medium">
          Error: {error}
        </div>
      )}
    </div>
  );
}
