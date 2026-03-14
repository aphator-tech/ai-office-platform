from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import json
import asyncio
from datetime import datetime

from app.config import get_settings
from app.database import init_db
from app.api import conversations_router, tasks_router, agents_router
from app.services.orchestrator import TaskOrchestrator

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown."""
    # Startup
    init_db()
    yield
    # Shutdown
    pass


# Create FastAPI app
app = FastAPI(
    title="AI Office API",
    description="Backend API for the Virtual AI Office platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(conversations_router, prefix=settings.api_prefix)
app.include_router(tasks_router, prefix=settings.api_prefix)
app.include_router(agents_router, prefix=settings.api_prefix)

# Global orchestrator
orchestrator = TaskOrchestrator()

# WebSocket connections storage
websocket_connections = {}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to AI Office API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.websocket("/ws/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: str):
    """WebSocket endpoint for real-time updates."""
    await websocket.accept()
    
    # Store connection
    if conversation_id not in websocket_connections:
        websocket_connections[conversation_id] = []
    websocket_connections[conversation_id].append(websocket)
    
    try:
        while True:
            # Wait for messages from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "submit_task":
                # Execute task workflow
                user_request = message.get("request", "")
                
                # Create conversation if needed
                from app.database import SessionLocal
                from app.models import Conversation
                
                db = SessionLocal()
                try:
                    # Create new conversation
                    conversation = Conversation(
                        user_id="default_user",
                        title=user_request[:50] + "..." if len(user_request) > 50 else user_request
                    )
                    db.add(conversation)
                    db.commit()
                    db.refresh(conversation)
                    
                    # Execute workflow with callback for updates
                    async def progress_callback(update):
                        """Send progress updates to WebSocket."""
                        await websocket.send_json({
                            "type": "agent_update",
                            "data": update
                        })
                    
                    result = await orchestrator.execute_workflow(
                        conversation.id,
                        user_request,
                        db,
                        progress_callback
                    )
                    
                    # Send final result
                    await websocket.send_json({
                        "type": "task_complete",
                        "conversation_id": conversation.id,
                        "result": result
                    })
                    
                finally:
                    db.close()
                    
            elif message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
                
    except WebSocketDisconnect:
        pass
    finally:
        # Remove connection
        if conversation_id in websocket_connections:
            websocket_connections[conversation_id] = [
                w for w in websocket_connections[conversation_id] 
                if w != websocket
            ]


# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
            "type": type(exc).__name__
        }
    )
