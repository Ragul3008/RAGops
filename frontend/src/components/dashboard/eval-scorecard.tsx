import React from "react";

export function EvalScoreCard() {
  const metrics = [
    { name: "Faithfulness", score: 0.94, desc: "Claims are grounded in context" },
    { name: "Answer Relevance", score: 0.89, desc: "Answers address the question" },
    { name: "Context Recall", score: 0.92, desc: "Retrieved chunks contain answer source" },
  ];

  return (
    <div className="rounded-lg border p-4 bg-card">
      <h3 className="text-sm font-medium mb-3">Evaluation Scores (Ragas)</h3>
      <div className="space-y-4">
        {metrics.map((m) => (
          <div key={m.name} className="space-y-1">
            <div className="flex justify-between text-sm">
              <span className="font-medium">{m.name}</span>
              <span className="font-bold text-blue-600">{m.score * 100}%</span>
            </div>
            <div className="w-full bg-secondary h-2 rounded-full overflow-hidden">
              <div
                className="bg-blue-500 h-full"
                style={{ width: `${m.score * 100}%` }}
              ></div>
            </div>
            <p className="text-xs text-muted-foreground">{m.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
