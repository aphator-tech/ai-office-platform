from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import AgentStatus
from app.agents.base import AGENT_REGISTRY

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("/status", response_model=List[AgentStatus])
def get_agent_statuses(db: Session = Depends(get_db)):
    """Get status of all available agents."""
    statuses = []
    
    for agent_type, agent_class in AGENT_REGISTRY.items():
        agent = agent_class()
        statuses.append(AgentStatus(
            agent_type=agent.agent_type,
            name=agent.name,
            description=agent.description,
            status="idle",
            current_task=None,
            progress="0%",
            icon=agent.icon
        ))
    
    return statuses


@router.get("/types")
def get_agent_types():
    """Get list of available agent types."""
    return [
        {"type": "manager", "name": "Manager Agent", "description": "Task planning and coordination"},
        {"type": "research", "name": "Research Agent", "description": "Information gathering and analysis"},
        {"type": "writer", "name": "Writer Agent", "description": "Content creation and documentation"},
        {"type": "developer", "name": "Developer Agent", "description": "Code generation and project building"},
        {"type": "designer", "name": "Designer Agent", "description": "UI/UX design and layout"},
    ]
