const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PATCH' | 'DELETE';
  body?: any;
  headers?: Record<string, string>;
}

async function request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
  const { method = 'GET', body, headers = {} } = options;
  
  const config: RequestInit = {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
  };
  
  if (body) {
    config.body = JSON.stringify(body);
  }
  
  const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }
  
  if (response.status === 204) {
    return {} as T;
  }
  
  return response.json();
}

// Conversations API
export const conversationsApi = {
  list: (userId: string = 'default_user', limit: number = 50) =>
    request<any[]>(`/conversations?user_id=${userId}&limit=${limit}`),
  
  get: (id: string) =>
    request<any>(`/conversations/${id}`),
  
  create: (title: string, userId: string = 'default_user') =>
    request<any>('/conversations', {
      method: 'POST',
      body: { title, user_id: userId },
    }),
  
  delete: (id: string) =>
    request<void>(`/conversations/${id}`, { method: 'DELETE' }),
};

// Tasks API
export const tasksApi = {
  list: (conversationId?: string, agentType?: string, status?: string) => {
    let endpoint = '/tasks?';
    const params = new URLSearchParams();
    if (conversationId) params.append('conversation_id', conversationId);
    if (agentType) params.append('agent_type', agentType);
    if (status) params.append('status', status);
    return request<any[]>(`/tasks?${params.toString()}`);
  },
  
  get: (id: string) =>
    request<any>(`/tasks/${id}`),
  
  getResult: (id: string) =>
    request<any>(`/tasks/${id}/result`),
  
  create: (conversationId: string, agentType: string, title: string, description?: string) =>
    request<any>('/tasks', {
      method: 'POST',
      body: { conversation_id: conversationId, agent_type: agentType, title, description },
    }),
  
  update: (id: string, updates: any) =>
    request<any>(`/tasks/${id}`, {
      method: 'PATCH',
      body: updates,
    }),
};

// Agents API
export const agentsApi = {
  getStatus: () =>
    request<any[]>('/agents/status'),
  
  getTypes: () =>
    request<any[]>('/agents/types'),
};

// WebSocket helper
export function createWebSocket(conversationId: string): WebSocket {
  const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000';
  return new WebSocket(`${wsUrl}/ws/${conversationId}`);
}
