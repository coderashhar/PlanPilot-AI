"use client";

import { useState } from "react";
import ChatInterface from "@/components/ChatInterface";
import MessageBubble from "@/components/MessageBubble";

export default function Home() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [traces, setTraces] = useState([]);

  const handleSendMessage = async (query) => {
    // Add user message
    setMessages((prev) => [...prev, { role: "user", content: query }]);
    setLoading(true);
    
    // Simulate streaming trace panel
    setTraces([
      { name: "Extracting Intent", status: "loading" },
      { name: "Executing Tools (Weather, Places, Events)", status: "pending" },
      { name: "Scoring & Generating Recommendations", status: "pending" }
    ]);

    try {
      // Simulate trace progress for UX
      setTimeout(() => setTraces(prev => [{...prev[0], status: "done"}, {...prev[1], status: "loading"}, prev[2]]), 1000);
      
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      
      if (!response.ok) throw new Error("Failed to get response");
      
      const data = await response.json();
      
      setTraces(prev => [{...prev[0]}, {...prev[1], status: "done"}, {...prev[2], status: "loading"}]);
      setTimeout(() => setTraces(prev => [{...prev[0]}, {...prev[1]}, {...prev[2], status: "done"}]), 500);

      setMessages((prev) => [
        ...prev,
        { role: "agent", content: data }
      ]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { role: "agent", error: true, content: "Sorry, I encountered an error fetching recommendations." }
      ]);
      setTraces([]);
    } finally {
      setLoading(false);
      setTimeout(() => setTraces([]), 3000); // Clear traces after 3s
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-6 md:p-24 bg-zinc-950 text-white font-sans">
      <div className="z-10 w-full max-w-5xl flex flex-col flex-1 pb-32">
        <div className="mb-12 text-center">
          <h1 className="text-4xl md:text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-b from-white to-gray-400 tracking-tight">
            PlanPilot AI
          </h1>
          <p className="mt-4 text-lg text-gray-400">
            Your Agentic Local Experience Planner
          </p>
        </div>

        <div className="flex-1 flex flex-col gap-6 overflow-y-auto mb-8">
          {messages.map((msg, idx) => (
            <MessageBubble key={idx} msg={msg} />
          ))}
        </div>
      </div>

      <div className="fixed bottom-0 left-0 w-full bg-gradient-to-t from-zinc-950 via-zinc-950 to-transparent pt-20 pb-8 px-6">
        <ChatInterface
          onSendMessage={handleSendMessage}
          loading={loading}
          traces={traces}
        />
      </div>
    </main>
  );
}
