"use client";

import { useState } from "react";
import { Send, MapPin, Users, Wallet, Utensils } from "lucide-react";
import ToolTracePanel from "./ToolTracePanel";

const PREFERENCE_CHIPS = [
  { icon: Users, label: "Group Size", query: "We are a group of 5" },
  { icon: Wallet, label: "Budget", query: "Budget is ₹2500" },
  { icon: Utensils, label: "Food", query: "Looking for good food" },
  { icon: MapPin, label: "Location", query: "Near Bhopal" },
];

export default function ChatInterface({ onSendMessage, loading, traces }) {
  const [input, setInput] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;
    onSendMessage(input);
    setInput("");
  };

  const handleChipClick = (query) => {
    setInput((prev) => (prev ? `${prev}. ${query}` : query));
  };

  return (
    <div className="w-full max-w-3xl mx-auto flex flex-col items-center">
      <div className="w-full mb-6">
        <ToolTracePanel traces={traces} />
      </div>

      <form
        onSubmit={handleSubmit}
        className="w-full relative flex items-center bg-zinc-900/50 border border-zinc-700/50 rounded-2xl p-2 shadow-2xl backdrop-blur-xl focus-within:border-blue-500/50 focus-within:bg-zinc-900/80 transition-all duration-300"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask PlanPilot anything (e.g. Suggest a rainy-day plan)..."
          className="flex-1 bg-transparent text-gray-100 placeholder-gray-500 px-4 py-3 outline-none text-lg"
          disabled={loading}
        />
        <button
          type="submit"
          disabled={!input.trim() || loading}
          className="bg-blue-600 hover:bg-blue-500 disabled:bg-zinc-800 disabled:text-zinc-600 text-white p-3 rounded-xl transition-colors duration-200"
        >
          <Send className="w-5 h-5" />
        </button>
      </form>

      <div className="flex flex-wrap items-center justify-center gap-2 mt-6">
        {PREFERENCE_CHIPS.map((chip, idx) => {
          const Icon = chip.icon;
          return (
            <button
              type="button"
              key={idx}
              onClick={() => handleChipClick(chip.query)}
              className="flex items-center gap-2 px-4 py-2 rounded-full border border-zinc-800 bg-zinc-900/30 text-sm text-gray-300 hover:bg-zinc-800 hover:text-white transition-colors"
            >
              <Icon className="w-4 h-4" />
              {chip.label}
            </button>
          );
        })}
      </div>
    </div>
  );
}
