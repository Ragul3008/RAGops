"use client";
import { AreaChart, Area, XAxis, YAxis,
         Tooltip, ResponsiveContainer } from "recharts";
import { useCostData } from "@/hooks/use-cost";

export function CostChart() {
  const { data } = useCostData({ days: 30 });
  return (
    <div className="rounded-lg border p-4">
      <h3 className="text-sm font-medium mb-3">LLM Spend (30d)</h3>
      <ResponsiveContainer width="100%" height={200}>
        <AreaChart data={data}>
          <XAxis dataKey="date" />
          <YAxis tickFormatter={v => "$"+v} />
          <Tooltip formatter={v => ["$"+v, "Cost"]} />
          <Area type="monotone" dataKey="cost_usd"
                stroke="#3b82f6" fill="#3b82f633" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}