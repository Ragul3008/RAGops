import React from "react";
import { Project } from "@/hooks/use-projects";

export function ProjectCard({ project }: { project: Project }) {
  return (
    <div className="rounded-lg border p-4 shadow-sm hover:shadow-md transition-shadow bg-card text-card-foreground">
      <h3 className="text-lg font-semibold mb-1">{project.name}</h3>
      <p className="text-sm text-muted-foreground mb-3">{project.description}</p>
      <div className="flex items-center justify-between text-xs text-muted-foreground">
        <span>Created {project.created_at}</span>
        <span className="px-2 py-0.5 rounded-full bg-secondary text-secondary-foreground">Active</span>
      </div>
    </div>
  );
}
