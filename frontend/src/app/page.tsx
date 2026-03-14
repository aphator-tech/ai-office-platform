'use client';

import { useState } from 'react';
import TaskInput from './components/TaskInput';
import AgentPanel from './components/AgentPanel';
import ResultsPanel from './components/ResultsPanel';
import { useAgentEvents } from '@/hooks/useAgentEvents';

export default function Home() {
  const { agents, isProcessing, lastResult, submitRequest, resetAgents } = useAgentEvents();
  const [currentRequest, setCurrentRequest] = useState('');
  
  const handleSubmit = async (request: string) => {
    setCurrentRequest(request);
    await submitRequest(request);
  };
  
  const handleReset = () => {
    setCurrentRequest('');
    resetAgents();
  };
  
  return (
    <div className="min-h-screen bg-background-dark">
      {/* Background decoration */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary/5 rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-secondary/5 rounded-full blur-3xl" />
      </div>
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-3">
            <span className="gradient-text">Virtual AI Office</span>
          </h1>
          <p className="text-text-secondary max-w-2xl mx-auto">
            A team of autonomous AI agents that collaborate to complete your tasks.
            Submit a request and watch our AI workforce get to work.
          </p>
        </div>
        
        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Column - Input and Agent Panel */}
          <div className="lg:col-span-5 space-y-6">
            <TaskInput onSubmit={handleSubmit} isProcessing={isProcessing} />
            <AgentPanel agents={agents} isProcessing={isProcessing} />
          </div>
          
          {/* Right Column - Results */}
          <div className="lg:col-span-7">
            <ResultsPanel result={lastResult} isProcessing={isProcessing} />
          </div>
        </div>
        
        {/* Features Section */}
        <div className="mt-16">
          <h2 className="text-2xl font-bold text-center mb-8">
            <span className="gradient-text">Meet Your AI Team</span>
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {[
              { icon: '👔', name: 'Manager', desc: 'Plans and coordinates tasks' },
              { icon: '🔍', name: 'Research', desc: 'Gathers and analyzes information' },
              { icon: '✍️', name: 'Writer', desc: 'Creates content and documentation' },
              { icon: '💻', name: 'Developer', desc: 'Builds code and projects' },
              { icon: '🎨', name: 'Designer', desc: 'Designs UI and layouts' },
            ].map((agent) => (
              <div
                key={agent.name}
                className="bg-background-card border border-border rounded-xl p-4 text-center hover:border-primary/30 transition-colors"
              >
                <div className="text-3xl mb-2">{agent.icon}</div>
                <h3 className="font-semibold">{agent.name}</h3>
                <p className="text-xs text-text-secondary mt-1">{agent.desc}</p>
              </div>
            ))}
          </div>
        </div>
        
        {/* How It Works */}
        <div className="mt-16 mb-8">
          <h2 className="text-2xl font-bold text-center mb-8">
            <span className="gradient-text">How It Works</span>
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              {
                step: '1',
                title: 'Submit Request',
                desc: 'Describe what you need in plain language',
                icon: '📝',
              },
              {
                step: '2',
                title: 'AI Team Works',
                desc: 'Our agents collaborate to complete your task',
                icon: '⚡',
              },
              {
                step: '3',
                title: 'Get Results',
                desc: 'Receive comprehensive results from all agents',
                icon: '🎯',
              },
            ].map((item) => (
              <div
                key={item.step}
                className="relative bg-background-card border border-border rounded-xl p-6"
              >
                <div className="absolute -top-3 -left-3 w-8 h-8 bg-primary rounded-full flex items-center justify-center text-sm font-bold">
                  {item.step}
                </div>
                <div className="text-4xl mb-3">{item.icon}</div>
                <h3 className="font-semibold text-lg">{item.title}</h3>
                <p className="text-text-secondary text-sm mt-1">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
