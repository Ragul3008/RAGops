import React from "react";

export function CreateProjectDialog({ children }: { children: React.ReactNode }) {
  return (
    <div onClick={() => alert("New project configuration is coming soon!")}>
      {children}
    </div>
  );
}
