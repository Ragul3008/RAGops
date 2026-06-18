import React from "react";

export function RecentActivity() {
  const activities = [
    { id: 1, action: "User query processed", time: "2 mins ago", detail: "Tenant id: 00000... Success" },
    { id: 2, action: "Document uploaded", time: "10 mins ago", detail: "financial_report_q1.pdf - Chunked successfully" },
    { id: 3, action: "Evaluation run finished", time: "1 hour ago", detail: "Faithfulness score: 0.96" },
  ];

  return (
    <div className="rounded-lg border p-4 bg-card">
      <h3 className="text-sm font-medium mb-3">Recent Activity</h3>
      <div className="space-y-3">
        {activities.map((a) => (
          <div key={a.id} className="flex justify-between items-start text-sm border-b pb-2 last:border-0 last:pb-0">
            <div>
              <p className="font-medium">{a.action}</p>
              <p className="text-xs text-muted-foreground mt-0.5">{a.detail}</p>
            </div>
            <span className="text-xs text-muted-foreground">{a.time}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
