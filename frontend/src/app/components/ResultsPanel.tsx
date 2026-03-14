'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { WorkflowResult, AgentType } from '@/lib/types';

interface ResultsPanelProps {
  result: WorkflowResult | null;
  isProcessing: boolean;
}

const AGENT_NAMES: Record<AgentType, string> = {
  manager: 'Manager',
  research: 'Research',
  writer: 'Writer',
  developer: 'Developer',
  designer: 'Designer',
};

export default function ResultsPanel({ result, isProcessing }: ResultsPanelProps) {
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set(['manager']));
  
  const toggleSection = (section: string) => {
    setExpandedSections(prev => {
      const next = new Set(prev);
      if (next.has(section)) {
        next.delete(section);
      } else {
        next.add(section);
      }
      return next;
    });
  };
  
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };
  
  if (isProcessing) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-background-card rounded-xl border border-border p-6"
      >
        <h2 className="text-lg font-semibold flex items-center gap-2">
          <span className="w-8 h-8 rounded-lg bg-accent/20 flex items-center justify-center">
            <svg className="w-4 h-4 text-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </span>
          Results
        </h2>
        
        <div className="mt-6 flex flex-col items-center justify-center py-12">
          <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin" />
          <p className="mt-4 text-text-secondary">Agents are working on your request...</p>
          <p className="mt-2 text-xs text-text-secondary">This may take a moment</p>
        </div>
      </motion.div>
    );
  }
  
  if (!result) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-background-card rounded-xl border border-border p-6"
      >
        <h2 className="text-lg font-semibold flex items-center gap-2">
          <span className="w-8 h-8 rounded-lg bg-accent/20 flex items-center justify-center">
            <svg className="w-4 h-4 text-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </span>
          Results
        </h2>
        
        <div className="mt-6 flex flex-col items-center justify-center py-12 text-text-secondary">
          <svg className="w-16 h-16 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p className="mt-4">Results will appear here</p>
          <p className="mt-1 text-xs">Submit a request to get started</p>
        </div>
      </motion.div>
    );
  }
  
  const sections = [
    { key: 'manager', data: result.manager, label: 'Manager Analysis' },
    { key: 'research', data: result.agent_results?.research, label: 'Research Findings' },
    { key: 'writer', data: result.agent_results?.writer, label: 'Written Content' },
    { key: 'developer', data: result.agent_results?.developer, label: 'Code & Project' },
    { key: 'designer', data: result.agent_results?.designer, label: 'Design Specs' },
  ].filter(section => section.data);
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-background-card rounded-xl border border-border p-6"
    >
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold flex items-center gap-2">
          <span className="w-8 h-8 rounded-lg bg-accent/20 flex items-center justify-center">
            <svg className="w-4 h-4 text-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </span>
          Results
        </h2>
        
        <button
          onClick={() => copyToClipboard(JSON.stringify(result, null, 2))}
          className="flex items-center gap-2 px-3 py-1.5 text-xs bg-background-elevated border border-border rounded-lg hover:border-primary/50 transition-colors"
        >
          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
          Copy All
        </button>
      </div>
      
      <div className="space-y-3">
        {sections.map((section) => (
          <div key={section.key} className="border border-border rounded-lg overflow-hidden">
            <button
              onClick={() => toggleSection(section.key)}
              className="w-full flex items-center justify-between p-4 bg-background-elevated hover:bg-background-elevated/80 transition-colors"
            >
              <span className="font-medium">{section.label}</span>
              <svg
                className={`w-4 h-4 text-text-secondary transition-transform ${
                  expandedSections.has(section.key) ? 'rotate-180' : ''
                }`}
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            
            <AnimatePresence>
              {expandedSections.has(section.key) && (
                <motion.div
                  initial={{ height: 0 }}
                  animate={{ height: 'auto' }}
                  exit={{ height: 0 }}
                  className="overflow-hidden"
                >
                  <div className="p-4 border-t border-border">
                    {section.key === 'writer' && section.data?.content ? (
                      <div className="prose prose-invert prose-sm max-w-none">
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          components={{
                            code({ node, className, children, ...props }) {
                              const match = /language-(\w+)/.exec(className || '');
                              return match ? (
                                <SyntaxHighlighter
                                  language={match[1]}
                                  PreTag="div"
                                  customStyle={{
                                    background: '#0D1117',
                                    borderRadius: '8px',
                                    padding: '16px',
                                  }}
                                >
                                  {String(children).replace(/\n$/, '')}
                                </SyntaxHighlighter>
                              ) : (
                                <code className={className} {...props}>
                                  {children}
                                </code>
                              );
                            },
                          }}
                        >
                          {section.data.content}
                        </ReactMarkdown>
                      </div>
                    ) : section.key === 'developer' && section.data?.files ? (
                      <div className="space-y-3">
                        {section.data.files.map((file: any, i: number) => (
                          <div key={i} className="border border-border rounded-lg overflow-hidden">
                            <div className="flex items-center justify-between px-3 py-2 bg-background-dark border-b border-border">
                              <span className="font-mono text-sm">{file.name}</span>
                              <button
                                onClick={() => copyToClipboard(file.content)}
                                className="p-1 hover:text-primary transition-colors"
                              >
                                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                </svg>
                              </button>
                            </div>
                            <SyntaxHighlighter
                              language={file.language}
                              PreTag="div"
                              customStyle={{
                                background: '#0D1117',
                                margin: 0,
                                borderRadius: 0,
                              }}
                            >
                              {file.content}
                            </SyntaxHighlighter>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <pre className="text-sm text-text-secondary overflow-x-auto font-mono">
                        {JSON.stringify(section.data, null, 2)}
                      </pre>
                    )}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
