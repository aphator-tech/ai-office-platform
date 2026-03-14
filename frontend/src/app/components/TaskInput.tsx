'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';

interface TaskInputProps {
  onSubmit: (request: string) => void;
  isProcessing: boolean;
}

export default function TaskInput({ onSubmit, isProcessing }: TaskInputProps) {
  const [request, setRequest] = useState('');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>('medium');
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (request.trim() && !isProcessing) {
      onSubmit(request.trim());
    }
  };
  
  const exampleRequests = [
    "Research a crypto project and generate a detailed report.",
    "Create a landing page for an AI startup and deploy it.",
    "Write a Twitter thread explaining a blockchain protocol.",
    "Analyze competitors for my business.",
  ];
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-background-card rounded-xl border border-border p-6"
    >
      <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
        <span className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center">
          <svg className="w-4 h-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </span>
        Submit Your Request
      </h2>
      
      <form onSubmit={handleSubmit}>
        <textarea
          value={request}
          onChange={(e) => setRequest(e.target.value)}
          placeholder="Describe what you need... (e.g., 'Research a crypto project and generate a detailed report')"
          className="w-full h-32 bg-background-dark border border-border rounded-lg p-4 text-text-primary placeholder:text-text-secondary resize-none focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-colors"
          disabled={isProcessing}
        />
        
        <div className="flex items-center justify-between mt-4">
          <div className="flex items-center gap-4">
            {/* Priority Selector */}
            <div className="flex items-center gap-2">
              <span className="text-sm text-text-secondary">Priority:</span>
              <div className="flex rounded-lg overflow-hidden border border-border">
                {(['low', 'medium', 'high'] as const).map((p) => (
                  <button
                    key={p}
                    type="button"
                    onClick={() => setPriority(p)}
                    disabled={isProcessing}
                    className={`px-3 py-1.5 text-sm font-medium transition-colors ${
                      priority === p
                        ? p === 'high'
                          ? 'bg-error/20 text-error'
                          : p === 'medium'
                          ? 'bg-warning/20 text-warning'
                          : 'bg-accent/20 text-accent'
                        : 'bg-background-dark text-text-secondary hover:text-text-primary'
                    }`}
                  >
                    {p.charAt(0).toUpperCase() + p.slice(1)}
                  </button>
                ))}
              </div>
            </div>
          </div>
          
          <motion.button
            type="submit"
            disabled={!request.trim() || isProcessing}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className={`px-6 py-2.5 rounded-lg font-semibold transition-all ${
              request.trim() && !isProcessing
                ? 'bg-gradient-to-r from-primary to-secondary text-background-dark hover:shadow-lg hover:shadow-primary/25'
                : 'bg-background-elevated text-text-secondary cursor-not-allowed'
            }`}
          >
            {isProcessing ? (
              <span className="flex items-center gap-2">
                <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Processing...
              </span>
            ) : (
              <span className="flex items-center gap-2">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                Submit Request
              </span>
            )}
          </motion.button>
        </div>
      </form>
      
      {/* Example Requests */}
      <div className="mt-4 pt-4 border-t border-border">
        <p className="text-xs text-text-secondary mb-2">Try these examples:</p>
        <div className="flex flex-wrap gap-2">
          {exampleRequests.map((example, i) => (
            <button
              key={i}
              type="button"
              onClick={() => setRequest(example)}
              disabled={isProcessing}
              className="px-3 py-1.5 text-xs bg-background-elevated border border-border rounded-full text-text-secondary hover:text-text-primary hover:border-primary/50 transition-colors"
            >
              {example.length > 40 ? example.slice(0, 40) + '...' : example}
            </button>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
