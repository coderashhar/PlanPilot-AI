"use client";

import RecommendationCard from "./RecommendationCard";
import { Calendar, CloudSun } from "lucide-react";
import { motion } from "framer-motion";

export default function MessageBubble({ msg }) {
  if (msg.role === "user") {
    return (
      <div className="flex justify-end mb-8">
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="max-w-2xl px-6 py-4 rounded-3xl bg-blue-600 text-white rounded-br-sm shadow-xl"
        >
          <p className="text-lg">{msg.content}</p>
        </motion.div>
      </div>
    );
  }

  if (msg.error) {
    return (
      <div className="flex justify-start mb-8">
        <div className="max-w-2xl px-6 py-4 rounded-3xl bg-red-950/40 border border-red-900/50 text-red-300 rounded-bl-sm">
          <p>{msg.content}</p>
        </div>
      </div>
    );
  }

  const { summary, recommendations, events, weather } = msg.content;

  return (
    <div className="flex justify-start mb-16 w-full">
      <motion.div 
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-4xl w-full"
      >
        {/* Summary Statement */}
        <div className="mb-6 inline-block bg-zinc-900/60 border border-zinc-800/80 px-6 py-4 rounded-2xl rounded-bl-sm">
          <p className="text-xl leading-relaxed text-gray-100">{summary}</p>
        </div>

        {/* Dynamic Context */}
        {weather && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="mb-8 inline-flex items-center gap-3 bg-zinc-900/80 border border-zinc-700/50 rounded-full px-5 py-2.5 shadow-lg"
          >
            <CloudSun className="text-yellow-400 w-5 h-5" />
            <span className="text-gray-200 font-medium capitalize">
              {weather.condition}, {weather.temperature}°C
            </span>
          </motion.div>
        )}

        {/* Core Recommendations Matrix */}
        {recommendations && recommendations.length > 0 && (
          <div className="mb-10">
            <h4 className="flex items-center gap-2 text-xs uppercase tracking-[0.2em] text-gray-500 font-bold mb-4 ml-1">
              Top Recommendations
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {recommendations.map((rec, i) => (
                <RecommendationCard key={i} rec={rec} index={i} />
              ))}
            </div>
          </div>
        )}

        {/* Event Context Array */}
        {events && events.length > 0 && (
          <div>
            <h4 className="flex items-center gap-2 text-xs uppercase tracking-[0.2em] text-gray-500 font-bold mb-4 ml-1">
              Events & Context
            </h4>
            <div className="space-y-3 max-w-2xl">
              {events.map((event, i) => (
                <motion.a 
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.1 + 0.3 }}
                  key={i} 
                  href={event.location} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center justify-between bg-zinc-900/40 hover:bg-zinc-800 border border-zinc-800/80 rounded-xl p-4 transition-all duration-300 group hover:border-zinc-600"
                >
                  <span className="text-blue-400/90 font-medium group-hover:text-blue-400 truncate pr-4">{event.name}</span>
                  <Calendar className="w-5 h-5 text-gray-600 group-hover:text-blue-400 shrink-0 transition-colors" />
                </motion.a>
              ))}
            </div>
          </div>
        )}
      </motion.div>
    </div>
  );
}
