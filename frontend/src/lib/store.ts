import { create } from "zustand";

interface PlaygroundState {
  llmProvider: string;
  promptVersion: string;
  setLlmProvider: (provider: string) => void;
  setPromptVersion: (version: string) => void;
}

export const usePlaygroundStore = create<PlaygroundState>((set) => ({
  llmProvider: "gemini",
  promptVersion: "v1",
  setLlmProvider: (provider) => set({ llmProvider: provider }),
  setPromptVersion: (version) => set({ promptVersion: version }),
}));
