'use client';

import { motion } from 'framer-motion';
import { AgentType, AgentStatus } from '@/lib/types';

interface AgentCardProps {
  agentType: AgentType;
  name: string;
  icon: string;
  description: string;
  status: AgentStatus;
  progress: string;
  message: string;
  delay?: number;
}

const statusColors: Record<AgentStatus, { bg: string; text: string; border: string }> = {
  idle: { bg: 'bg-background-elevated', text: 'text-text-secondary', border: 'border-border' },
  working: { bg: 'bg-primary/10', text: 'text-primary', border: 'border-primary/30' },
  completed: { bg: 'bg-accent/10', text: 'text-accent', border: 'border-accent/30' },
  error: { bg: 'bg-error/10', text: 'text-error', border: 'border-error/30' },
};

export default function AgentCard({
  agentType,
  name,
  icon,
  description,
  status,
  progress,
  message,
  delay = 0,
}: AgentCardProps) {
  const colors = statusColors[status];
  const progressValue = parseInt(progress.replace('%', ''));
  
  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.3, delay }}
      className={`relative overflow-hidden rounded-xl border ${colors.border} ${colors.bg} p-4 transition-all duration-300`}
    >
      {/* Status indicator */}
      <div className="absolute top-4 right-4">
        <div className={`w-2.5 h-2.5 rounded-full ${
          status === 'working' ? 'bg-primary animate-pulse' :
          status === 'completed' ? 'bg-accent' :
          status === 'error' ? 'bg-error' :
          'bg-text-secondary'
        }`} />
      </div>
      
      {/* Agent header */}
      <div className="flex items-start gap-3">
        <div className="text-3xl">{icon}</div>
        <div className="flex-1 min-w-0">
          <h3 className={`font-semibold ${colors.text}`}>{name}</h3>
          <p className="text-xs text-text-secondary mt-0.5 line-clamp-2">{description}</p>
        </div>
      </div>
      
      {/* Progress bar */}
      <div className="mt-4">
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-xs text-text-secondary">Progress</span>
          <span className={`text-xs font-mono ${colors.text}`}>{progress}</span>
        </div>
        <div className="h-1.5 bg-background-dark rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${progressValue}%` }}
            transition={{ duration: 0.5, ease: 'easeOut' }}
            className={`h-full rounded-full progress-bar ${
              status === 'completed' ? 'bg-accent' :
              status === 'error' ? 'bg-error' :
              'bg-gradient-to-r from-primary to-secondary'
            }`}
          />
        </div>
      </div>
      
      {/* Current message */}
      {message && (
        <div className="mt-3 pt-3 border-t border-border/50">
          <p className="text-xs text-text-secondary">
            <span className="text-primary mr-1">→</span>
            {message}
          </p>
        </div>
      )}
      
      {/* Working animation overlay */}
      {status === 'working' && (
        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-primary/5 to-transparent animate-pulse" />
      )}
    </motion.div>
  );
}
