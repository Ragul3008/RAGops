import React from "react";

export function HallucinationAlert() {
  return (
    <div className="rounded-lg border border-yellow-200 bg-yellow-50 p-4 text-yellow-800 text-sm">
      <div className="flex items-center space-x-2">
        <span className="font-bold">⚠️ Warning:</span>
        <span>A recent evaluation run flagged a potential faithfulness dip (0.68) on Project: Financial Report Analysis.</span>
      </div>
    </div>
  );
}
