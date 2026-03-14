from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import asyncio
from datetime import datetime
from app.database import get_db
from app.models import Task, Conversation, Message
from app.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskEvent,
    AgentEvent,
)
from app.services.orchestrator import TaskOrchestrator

router = APIRouter(prefix="/tasks", tags=["tasks"])

# Global orchestrator instance
orchestrator = TaskOrchestrator()


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create and execute a new task."""
    # Verify conversation exists
    conversation = db.query(Conversation).filter(
        Conversation.id == task.conversation_id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Create task in database
    db_task = Task(
        conversation_id=task.conversation_id,
        agent_type=task.agent_type,
        title=task.title,
        description=task.description,
        status="pending"
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # Execute task in background
    background_tasks.add_task(
        orchestrator.execute_task,
        db_task.id,
        task.agent_type,
        task.title,
        task.description or "",
        db
    )
    
    return db_task


@router.get("", response_model=List[TaskResponse])
def list_tasks(
    conversation_id: Optional[str] = None,
    agent_type: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List tasks with optional filters."""
    query = db.query(Task)
    
    if conversation_id:
        query = query.filter(Task.conversation_id == conversation_id)
    if agent_type:
        query = query.filter(Task.agent_type == agent_type)
    if status:
        query = query.filter(Task.status == status)
    
    tasks = query.order_by(Task.created_at.desc()).limit(limit).all()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific task."""
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task


@router.get("/{task_id}/result")
def get_task_result(
    task_id: str,
    db: Session = Depends(get_db)
):
    """Get task result."""
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.status != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Task is not completed yet. Current status: {task.status}"
        )
    
    return task.result or {}


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
):
    """Update a task."""
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task_update.status is not None:
        task.status = task_update.status
        if task_update.status == "completed":
            task.completed_at = datetime.utcnow()
        elif task_update.status == "in_progress" and task.status == "pending":
            task.status = "in_progress"
    
    if task_update.result is not None:
        task.result = task_update.result
    
    if task_update.progress is not None:
        task.progress = task_update.progress
    
    db.commit()
    db.refresh(task)
    
    return task


async def event_generator(task_id: str, db: Session):
    """Generate SSE events for task updates."""
    while True:
        task = db.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            break
        
        event_data = {
            "event_type": f"task:{task.status}",
            "task_id": task.id,
            "agent_type": task.agent_type,
            "status": task.status,
            "progress": task.progress,
            "message": task.description
        }
        
        yield f"data: {json.dumps(event_data)}\n\n"
        
        if task.status in ["completed", "failed"]:
            break
        
        await asyncio.sleep(2)


@router.get("/{task_id}/stream")
async def stream_task_updates(
    task_id: str,
    db: Session = Depends(get_db)
):
    """Stream task updates via SSE."""
    return StreamingResponse(
        event_generator(task_id, db),
        media_type="text/event-stream"
    )
