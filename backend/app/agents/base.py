from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio
import uuid


class BaseAgent(ABC):
    """Base class for all AI agents in the system."""
    
    def __init__(self):
        self.agent_type: str = "base"
        self.name: str = "Base Agent"
        self.description: str = "Base agent"
        self.icon: str = "🤖"
        self.status: str = "idle"
        self.current_task: Optional[str] = None
        self.progress: str = "0%"
        self._callbacks: List[callable] = []
    
    def on_update(self, callback: callable):
        """Register a callback for status updates."""
        self._callbacks.append(callback)
    
    async def _notify_update(self, status: str, progress: str, message: str = ""):
        """Notify all registered callbacks of status update."""
        self.status = status
        self.progress = progress
        for callback in self._callbacks:
            try:
                await callback({
                    "agent_type": self.agent_type,
                    "status": status,
                    "progress": progress,
                    "message": message,
                    "timestamp": datetime.utcnow().isoformat()
                })
            except Exception as e:
                print(f"Callback error: {e}")
    
    @abstractmethod
    async def execute(self, task_id: str, title: str, description: str) -> Dict[str, Any]:
        """
        Execute the agent's task.
        
        Args:
            task_id: Unique identifier for the task
            title: Task title
            description: Task description
            
        Returns:
            Dict containing the result of the task execution
        """
        pass
    
    async def simulate_work(self, steps: List[str], task_id: str):
        """Simulate work with progress updates."""
        total = len(steps)
        for i, step in enumerate(steps):
            await self._notify_update("working", f"{int((i/total)*100)}%", step)
            # Simulate work time
            await asyncio.sleep(1.5)
        await self._notify_update("completed", "100%", "Task completed")


class AgentRegistry:
    """Registry for managing agent instances."""
    
    _agents: Dict[str, type] = {}
    
    @classmethod
    def register(cls, agent_class: type):
        """Register an agent class."""
        cls._agents[agent_class.__name__.lower().replace("agent", "")] = agent_class
        return agent_class
    
    @classmethod
    def get_agent(cls, agent_type: str) -> BaseAgent:
        """Get an agent instance by type."""
        if agent_type not in cls._agents:
            raise ValueError(f"Unknown agent type: {agent_type}")
        return cls._agents[agent_type]()
    
    @classmethod
    def list_agents(cls) -> List[str]:
        """List all registered agent types."""
        return list(cls._agents.keys())


# Global registry for agents
AGENT_REGISTRY = {
    "manager": None,  # Will be set after imports
    "research": None,
    "writer": None,
    "developer": None,
    "designer": None,
}
