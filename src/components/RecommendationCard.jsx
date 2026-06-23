"use client";

import { Star, IndianRupee, MapPin } from "lucide-react";
import { motion } from "framer-motion";

export default function RecommendationCard({ rec, index }) {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className="bg-zinc-800/80 border border-zinc-700/50 rounded-xl p-5 hover:bg-zinc-800 transition-colors group h-full flex flex-col justify-between"
    >
      <div>
        <div className="flex justify-between items-start mb-2 gap-2">
          <h3 className="text-lg font-bold text-white group-hover:text-blue-400 transition-colors leading-tight">
            {rec.name}
          </h3>
          <div className="flex items-center gap-1 bg-emerald-500/20 text-emerald-300 px-2 py-1 rounded text-xs font-semibold shrink-0">
            <Star className="w-3 h-3 fill-emerald-300" />
            {(rec.score / 20).toFixed(1)}
          </div>
        </div>
        
        {rec.url && (
          <a href={rec.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1 text-xs text-blue-400 hover:text-blue-300 hover:underline mb-3">
            <MapPin className="w-3 h-3" />
            View on Map
          </a>
        )}
        
        <p className="text-sm text-gray-400 mb-4 leading-relaxed">{rec.reason}</p>
      </div>
      
      <div className="flex items-center gap-4 text-sm text-gray-300 mt-auto pt-4 border-t border-zinc-700/50">
        {rec.estimated_cost != null && rec.estimated_cost > 0 && (
          <div className="flex items-center gap-1">
            <IndianRupee className="w-4 h-4 text-emerald-400" />
            <span className="font-medium text-emerald-400">~{rec.estimated_cost}</span>
          </div>
        )}
        {rec.estimated_cost === 0 && (
          <div className="flex items-center gap-1 text-emerald-400 font-medium">
            <span>Free</span>
          </div>
        )}
        {rec.estimated_cost == null && (
          <div className="flex items-center gap-1 text-gray-500 font-medium">
            <span>Price Unknown</span>
          </div>
        )}
      </div>
    </motion.div>
  );
}
