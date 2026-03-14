import { useState, useEffect, useCallback, useRef } from 'react';
import { AgentUpdate, AgentType, AgentStatus } from '@/lib/types';

export interface AgentState {
  [key: string]: {
    status: AgentStatus;
    progress: string;
    message: string;
  };
}

const DEFAULT_AGENTS: AgentState = {
  manager: { status: 'idle', progress: '0%', message: '' },
  research: { status: 'idle', progress: '0%', message: '' },
  writer: { status: 'idle', progress: '0%', message: '' },
  developer: { status: 'idle', progress: '0%', message: '' },
  designer: { status: 'idle', progress: '0%', message: '' },
};

export function useAgentEvents(conversationId?: string) {
  const [agents, setAgents] = useState<AgentState>(DEFAULT_AGENTS);
  const [isConnected, setIsConnected] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [lastResult, setLastResult] = useState<any>(null);
  const wsRef = useRef<WebSocket | null>(null);

  const connect = useCallback((convId: string) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return;
    }

    const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000';
    const ws = new WebSocket(`${wsUrl}/ws/${convId}`);
    wsRef.current = ws;

    ws.onopen = () => {
      setIsConnected(true);
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        
        if (message.type === 'agent_update') {
          const update = message.data;
          setAgents(prev => ({
            ...prev,
            [update.agent_type]: {
              status: update.status as AgentStatus,
              progress: update.progress,
              message: update.message,
            },
          }));
        } else if (message.type === 'task_complete') {
          setLastResult(message.result);
          setIsProcessing(false);
        }
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    };

    ws.onclose = () => {
      setIsConnected(false);
      console.log('WebSocket disconnected');
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }, []);

  const disconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    setIsConnected(false);
  }, []);

  const submitRequest = useCallback(async (request: string) => {
    setIsProcessing(true);
    setAgents(DEFAULT_AGENTS);
    setLastResult(null);

    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      // Create a new conversation first
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'}/conversations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: request.slice(0, 50) + (request.length > 50 ? '...' : ''),
          user_id: 'default_user'
        }),
      });
      
      const conversation = await response.json();
      connect(conversation.id);

      // Wait a bit for connection
      await new Promise(resolve => setTimeout(resolve, 500));
    }

    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        type: 'submit_task',
        request,
      }));
    }
  }, [connect]);

  const resetAgents = useCallback(() => {
    setAgents(DEFAULT_AGENTS);
    setLastResult(null);
  }, []);

  useEffect(() => {
    return () => {
      disconnect();
    };
  }, [disconnect]);

  return {
    agents,
    isConnected,
    isProcessing,
    lastResult,
    submitRequest,
    resetAgents,
    connect,
    disconnect,
  };
}
