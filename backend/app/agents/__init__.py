# Import all agents to register them
from app.agents.base import BaseAgent, AGENT_REGISTRY
from app.agents.manager import ManagerAgent
from app.agents.research import ResearchAgent
from app.agents.writer import WriterAgent
from app.agents.developer import DeveloperAgent
from app.agents.designer import DesignerAgent

__all__ = [
    "BaseAgent",
    "AGENT_REGISTRY",
    "ManagerAgent",
    "ResearchAgent",
    "WriterAgent", 
    "DeveloperAgent",
    "DesignerAgent"
]
