'use client';

import { motion } from 'framer-motion';
import AgentCard from './AgentCard';
import { AgentState } from '@/hooks/useAgentEvents';

interface AgentPanelProps {
  agents: AgentState;
  isProcessing: boolean;
}

const AGENT_INFO = {
  manager: {
    name: 'Manager Agent',
    icon: '👔',
    description: 'Task planning, coordination, and delegation',
  },
  research: {
    name: 'Research Agent',
    icon: '🔍',
    description: 'Information gathering and analysis',
  },
  writer: {
    name: 'Writer Agent',
    icon: '✍️',
    description: 'Content creation and documentation',
  },
  developer: {
    name: 'Developer Agent',
    icon: '💻',
    description: 'Code generation and project building',
  },
  designer: {
    name: 'Designer Agent',
    icon: '🎨',
    description: 'UI/UX design and layout',
  },
};

export default function AgentPanel({ agents, isProcessing }: AgentPanelProps) {
  const agentOrder = ['manager', 'research', 'writer', 'developer', 'designer'] as const;
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.1 }}
      className="bg-background-card rounded-xl border border-border p-6"
    >
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold flex items-center gap-2">
          <span className="w-8 h-8 rounded-lg bg-secondary/20 flex items-center justify-center">
            <svg className="w-4 h-4 text-secondary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </span>
          Agent Workspace
        </h2>
        
        {/* Status indicator */}
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${
            isProcessing ? 'bg-primary animate-pulse' : 'bg-text-secondary'
          }`} />
          <span className="text-xs text-text-secondary">
            {isProcessing ? 'Processing...' : 'Idle'}
          </span>
        </div>
      </div>
      
      {/* Agent cards grid */}
      <div className="grid grid-cols-1 gap-3">
        {agentOrder.map((agentType, index) => {
          const info = AGENT_INFO[agentType];
          const state = agents[agentType];
          
          return (
            <AgentCard
              key={agentType}
              agentType={agentType}
              name={info.name}
              icon={info.icon}
              description={info.description}
              status={state.status}
              progress={state.progress}
              message={state.message}
              delay={index * 0.1}
            />
          );
        })}
      </div>
    </motion.div>
  );
}
