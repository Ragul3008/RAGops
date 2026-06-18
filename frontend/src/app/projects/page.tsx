"use client";
import { useProjects } from "@/hooks/use-projects";
import { ProjectCard } from "@/components/projects/card";
import { CreateProjectDialog } from "@/components/projects/create-dialog";
import { Button } from "@/components/ui/button";

export default function ProjectsPage() {
  const { projects, isLoading } = useProjects();
  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-semibold">Projects</h1>
        <CreateProjectDialog>
          <Button>New Project</Button>
        </CreateProjectDialog>
      </div>
      <div className="grid grid-cols-3 gap-4">
        {projects?.map(p => (
          <ProjectCard key={p.id} project={p} />
        ))}
      </div>
    </div>
  );
}