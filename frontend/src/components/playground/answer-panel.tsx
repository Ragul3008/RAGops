"use client";
import React from "react";
import ReactMarkdown from "react-markdown";

interface AnswerPanelProps {
  answer: string;
}

export function AnswerPanel({ answer }: AnswerPanelProps) {
  const isNoContext = answer === "I do not have the context to answer this query.";

  return (
    <div className="rounded-xl border bg-card p-5 shadow-sm space-y-4 flex flex-col h-[400px]">
      <div>
        <h3 className="text-lg font-semibold text-foreground">Generated Answer</h3>
        <p className="text-xs text-muted-foreground">The LLM response synthesized from context.</p>
      </div>

      <div className="flex-1 overflow-y-auto pr-1">
        {isNoContext ? (
          <div className="p-4 border border-destructive/20 bg-destructive/5 rounded-lg text-sm text-destructive font-medium flex flex-col items-center justify-center text-center h-full space-y-2">
            <svg
              className="w-8 h-8 text-destructive"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
            <p className="font-semibold text-base">Grounding Alert</p>
            <p className="text-xs text-muted-foreground max-w-xs leading-relaxed">
              The model refused to answer because the query wasn't supported by the retrieved context chunks (no hallucination).
            </p>
          </div>
        ) : (
          <div className="p-4 border rounded-lg bg-background text-sm leading-relaxed text-foreground h-full overflow-y-auto">
            {answer ? (
              <ReactMarkdown className="space-y-3 [&>ul]:list-disc [&>ul]:pl-5 [&>ol]:list-decimal [&>ol]:pl-5 [&>h1]:text-lg [&>h1]:font-bold [&>h2]:text-base [&>h2]:font-bold [&>p>code]:bg-muted [&>p>code]:px-1 [&>p>code]:rounded [&>pre]:bg-muted [&>pre]:p-2 [&>pre]:rounded">
                {answer}
              </ReactMarkdown>
            ) : (
              <p className="whitespace-pre-wrap text-muted-foreground">Waiting for answer...</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
