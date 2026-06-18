import { DashboardStats }   from "@/components/dashboard/stats";
import { RecentActivity }   from "@/components/dashboard/activity";
import { CostChart }        from "@/components/dashboard/cost-chart";
import { EvalScoreCard }    from "@/components/dashboard/eval-scorecard";
import { HallucinationAlert } from "@/components/dashboard/hallucination-alert";

export default function DashboardPage() {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-semibold">Dashboard</h1>
      <DashboardStats />
      <div className="grid grid-cols-2 gap-6">
        <CostChart />
        <EvalScoreCard />
      </div>
      <HallucinationAlert />
      <RecentActivity />
    </div>
  );
}