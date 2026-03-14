from typing import Dict, Any, List
from app.agents.base import BaseAgent, AGENT_REGISTRY
import asyncio


class ManagerAgent(BaseAgent):
    """Manager Agent - coordinates task execution and delegates to worker agents."""
    
    def __init__(self):
        super().__init__()
        self.agent_type = "manager"
        self.name = "Manager Agent"
        self.description = "Task planning, coordination, and delegation to worker agents"
        self.icon = "👔"
    
    async def execute(self, task_id: str, title: str, description: str) -> Dict[str, Any]:
        """
        Execute the manager's coordination role.
        
        1. Analyze the request
        2. Break into subtasks
        3. Determine which agents needed
        4. Return task breakdown for execution
        """
        await self._notify_update("working", "10%", "Analyzing request...")
        await asyncio.sleep(1.5)
        
        await self._notify_update("working", "30%", "Breaking down into subtasks...")
        await asyncio.sleep(1.5)
        
        # Analyze request and determine required agents
        required_agents = self._determine_agents(title, description)
        
        await self._notify_update("working", "50%", "Creating task plan...")
        await asyncio.sleep(1.5)
        
        await self._notify_update("working", "70%", "Assigning tasks to agents...")
        await asyncio.sleep(1.5)
        
        # Generate task breakdown
        task_breakdown = {
            "main_task": title,
            "description": description,
            "subtasks": self._create_subtasks(title, description, required_agents),
            "required_agents": required_agents,
            "execution_order": self._plan_execution_order(required_agents)
        }
        
        await self._notify_update("working", "90%", "Finalizing plan...")
        await asyncio.sleep(1)
        
        await self._notify_update("completed", "100%", "Task analysis complete")
        
        return {
            "status": "success",
            "task_breakdown": task_breakdown,
            "summary": f"Created {len(task_breakdown['subtasks'])} subtasks for {len(required_agents)} agents"
        }
    
    def _determine_agents(self, title: str, description: str) -> List[str]:
        """Determine which agents are needed based on the request."""
        combined_text = f"{title} {description}".lower()
        agents = []
        
        # Always include manager for coordination
        agents.append("manager")
        
        # Research for research tasks
        if any(kw in combined_text for kw in ["research", "analyze", "investigate", "find", "explore", "survey"]):
            agents.append("research")
        
        # Writer for content tasks
        if any(kw in combined_text for kw in ["write", "create", "generate", "draft", "document", "article", "report", "thread", "content"]):
            agents.append("writer")
        
        # Developer for code tasks
        if any(kw in combined_text for kw in ["code", "build", "develop", "program", "create website", "app", "deploy"]):
            agents.append("developer")
        
        # Designer for UI/UX tasks
        if any(kw in combined_text for kw in ["design", "ui", "ux", "layout", "interface", "visual", "mockup"]):
            agents.append("designer")
        
        return list(set(agents))  # Remove duplicates
    
    def _create_subtasks(self, title: str, description: str, agents: List[str]) -> List[Dict[str, Any]]:
        """Create subtasks for each agent."""
        subtasks = []
        
        for agent in agents:
            if agent == "manager":
                subtasks.append({
                    "agent": "manager",
                    "title": "Coordinate and monitor execution",
                    "description": "Oversee task execution and aggregate results",
                    "status": "pending"
                })
            elif agent == "research":
                subtasks.append({
                    "agent": "research",
                    "title": "Gather information",
                    "description": f"Research and gather relevant information for: {title}",
                    "status": "pending"
                })
            elif agent == "writer":
                subtasks.append({
                    "agent": "writer",
                    "title": "Generate content",
                    "description": f"Create written content for: {title}",
                    "status": "pending"
                })
            elif agent == "developer":
                subtasks.append({
                    "agent": "developer",
                    "title": "Build solution",
                    "description": f"Generate code and build solution for: {title}",
                    "status": "pending"
                })
            elif agent == "designer":
                subtasks.append({
                    "agent": "designer",
                    "title": "Design UI/UX",
                    "description": f"Create design specifications for: {title}",
                    "status": "pending"
                })
        
        return subtasks
    
    def _plan_execution_order(self, agents: List[str]) -> List[str]:
        """Plan the execution order of agents."""
        # Define optimal execution order
        order = ["research", "writer", "designer", "developer", "manager"]
        return [a for a in order if a in agents]


# Register the agent
AGENT_REGISTRY["manager"] = ManagerAgent
