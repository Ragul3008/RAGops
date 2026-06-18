import { useState } from "react";

export interface Project {
  id: string;
  name: string;
  description: string;
  created_at: string;
}

export function useProjects() {
  const [projects, setProjects] = useState<Project[]>([
    {
      id: "1",
      name: "Customer Support RAG",
      description: "Q&A chatbot over internal support knowledge base",
      created_at: "2024-01-10",
    },
    {
      id: "2",
      name: "Financial Report Analysis",
      description: "Retrieval and synthesis of 10-K and 10-Q filings",
      created_at: "2024-02-15",
    },
  ]);

  return {
    projects,
    isLoading: false,
    error: null,
  };
}
