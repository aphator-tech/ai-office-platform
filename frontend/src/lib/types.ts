// Types for the AI Office platform

export interface Conversation {
  id: string;
  user_id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: string;
  conversation_id: string;
  agent_type: AgentType;
  title: string;
  description?: string;
  status: TaskStatus;
  result?: any;
  progress: string;
  created_at: string;
  completed_at?: string;
}

export type TaskStatus = 'pending' | 'in_progress' | 'completed' | 'failed';

export type AgentType = 'manager' | 'research' | 'writer' | 'developer' | 'designer';

export interface Agent {
  agent_type: AgentType;
  name: string;
  description: string;
  status: AgentStatus;
  current_task?: string;
  progress: string;
  icon: string;
}

export type AgentStatus = 'idle' | 'working' | 'completed' | 'error';

export interface Message {
  id: string;
  conversation_id: string;
  role: 'user' | 'assistant' | 'agent';
  agent_type?: AgentType;
  content: string;
  metadata?: any;
  created_at: string;
}

export interface AgentUpdate {
  agent_type: AgentType;
  status: AgentStatus;
  progress: string;
  message: string;
  timestamp: string;
}

export interface TaskBreakdown {
  main_task: string;
  description: string;
  subtasks: SubTask[];
  required_agents: AgentType[];
  execution_order: AgentType[];
}

export interface SubTask {
  agent: AgentType;
  title: string;
  description: string;
  status: TaskStatus;
}

export interface WorkflowResult {
  manager: any;
  agent_results: {
    [key in AgentType]?: any;
  };
}

export interface WebSocketMessage {
  type: 'agent_update' | 'task_complete' | 'pong';
  data?: AgentUpdate;
  conversation_id?: string;
  result?: WorkflowResult;
}
