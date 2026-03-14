from typing import Dict, Any, List, Optional, Callable
from sqlalchemy.orm import Session
from datetime import datetime
import asyncio
import uuid

from app.models import Task, Message, Conversation
from app.agents.base import BaseAgent, AGENT_REGISTRY


class TaskOrchestrator:
    """Orchestrates task execution across multiple agents."""
    
    def __init__(self):
        self.agents = {}
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all agent instances."""
        for agent_type, agent_class in AGENT_REGISTRY.items():
            if agent_class:
                self.agents[agent_type] = agent_class()
    
    async def execute_task(
        self,
        task_id: str,
        agent_type: str,
        title: str,
        description: str,
        db: Session,
        callback: Optional[Callable] = None
    ):
        """Execute a task using the specified agent."""
        # Get the agent
        agent = self.agents.get(agent_type)
        if not agent:
            await self._update_task_status(db, task_id, "failed", "Unknown agent type")
            return
        
        # Register callback for updates
        if callback:
            agent.on_update(callback)
        
        try:
            # Update task to in_progress
            await self._update_task_status(db, task_id, "in_progress", "Starting...")
            
            # Execute the agent's task
            result = await agent.execute(task_id, title, description)
            
            # Update task with result
            await self._update_task_status(
                db, 
                task_id, 
                "completed", 
                "Completed",
                result=result
            )
            
            # Add completion message
            await self._add_message(
                db,
                task_id.split('-')[0] if '-' in task_id else task_id,  # conversation_id
                "agent",
                agent_type,
                f"Task completed: {title}"
            )
            
            return result
            
        except Exception as e:
            await self._update_task_status(db, task_id, "failed", str(e))
            raise
    
    async def execute_workflow(
        self,
        conversation_id: str,
        user_request: str,
        db: Session,
        callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Execute a complete workflow using multiple agents.
        
        This is the main entry point for handling user requests.
        """
        # Step 1: Get Manager Agent to analyze and plan
        manager = self.agents.get("manager")
        if not manager:
            raise ValueError("Manager agent not available")
        
        # Create manager task
        manager_task = Task(
            conversation_id=conversation_id,
            agent_type="manager",
            title="Analyze and plan task execution",
            description=user_request,
            status="pending"
        )
        db.add(manager_task)
        db.commit()
        db.refresh(manager_task)
        
        # Execute manager agent
        if callback:
            manager.on_update(callback)
        
        manager_result = await manager.execute(
            manager_task.id,
            "Task Analysis",
            user_request
        )
        
        # Update manager task
        manager_task.status = "completed"
        manager_task.result = manager_result
        manager_task.completed_at = datetime.utcnow()
        db.commit()
        
        # Step 2: Execute subtasks based on manager's plan
        task_breakdown = manager_result.get("task_breakdown", {})
        subtasks = task_breakdown.get("subtasks", [])
        
        results = {
            "manager": manager_result,
            "agent_results": {}
        }
        
        # Execute each subtask
        for subtask in subtasks:
            agent_type = subtask.get("agent")
            if agent_type == "manager":
                continue  # Skip manager as we already ran it
            
            # Create subtask in database
            subtask_db = Task(
                conversation_id=conversation_id,
                agent_type=agent_type,
                title=subtask.get("title", ""),
                description=subtask.get("description", ""),
                status="pending"
            )
            db.add(subtask_db)
            db.commit()
            db.refresh(subtask_db)
            
            # Get the agent and execute
            agent = self.agents.get(agent_type)
            if not agent:
                continue
            
            if callback:
                agent.on_update(callback)
            
            try:
                result = await agent.execute(
                    subtask_db.id,
                    subtask.get("title", ""),
                    subtask.get("description", "")
                )
                
                # Update subtask
                subtask_db.status = "completed"
                subtask_db.result = result
                subtask_db.completed_at = datetime.utcnow()
                db.commit()
                
                results["agent_results"][agent_type] = result
                
            except Exception as e:
                subtask_db.status = "failed"
                db.commit()
                results["agent_results"][agent_type] = {"error": str(e)}
        
        # Add final message
        await self._add_message(
            db,
            conversation_id,
            "assistant",
            "manager",
            f"Workflow completed. Executed tasks for: {', '.join(results['agent_results'].keys())}"
        )
        
        return results
    
    async def _update_task_status(
        self,
        db: Session,
        task_id: str,
        status: str,
        progress_message: str,
        result: Optional[Dict[str, Any]] = None
    ):
        """Update task status in database."""
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            task.status = status
            if status == "completed":
                task.completed_at = datetime.utcnow()
                task.progress = "100%"
            elif status == "in_progress":
                task.progress = "50%"
            if result:
                task.result = result
            db.commit()
    
    async def _add_message(
        self,
        db: Session,
        conversation_id: str,
        role: str,
        agent_type: Optional[str],
        content: str
    ):
        """Add a message to the conversation."""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            agent_type=agent_type,
            content=content,
            extra_data={}
        )
        db.add(message)
        db.commit()
