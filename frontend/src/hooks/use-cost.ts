import { useState } from "react";

export interface CostRecord {
  date: string;
  cost_usd: number;
}

export function useCostData({ days }: { days: number }) {
  const [data] = useState<CostRecord[]>([
    { date: "May 10", cost_usd: 12.5 },
    { date: "May 15", cost_usd: 15.2 },
    { date: "May 20", cost_usd: 18.0 },
    { date: "May 25", cost_usd: 14.5 },
    { date: "May 30", cost_usd: 22.1 },
    { date: "Jun 05", cost_usd: 25.8 },
    { date: "Jun 10", cost_usd: 30.2 },
  ]);

  return {
    data,
    isLoading: false,
    error: null,
  };
}
