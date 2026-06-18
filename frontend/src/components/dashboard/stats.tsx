import React from "react";

export function DashboardStats() {
  return (
    <div className="grid grid-cols-4 gap-4">
      <div className="rounded-lg border p-4 bg-card">
        <h4 className="text-xs text-muted-foreground font-medium uppercase">Total Requests</h4>
        <p className="text-2xl font-bold mt-1">124,582</p>
      </div>
      <div className="rounded-lg border p-4 bg-card">
        <h4 className="text-xs text-muted-foreground font-medium uppercase">Avg Latency</h4>
        <p className="text-2xl font-bold mt-1">182ms</p>
      </div>
      <div className="rounded-lg border p-4 bg-card">
        <h4 className="text-xs text-muted-foreground font-medium uppercase">Success Rate</h4>
        <p className="text-2xl font-bold mt-1">99.8%</p>
      </div>
      <div className="rounded-lg border p-4 bg-card">
        <h4 className="text-xs text-muted-foreground font-medium uppercase">Total Cost</h4>
        <p className="text-2xl font-bold mt-1">$152.00</p>
      </div>
    </div>
  );
}
