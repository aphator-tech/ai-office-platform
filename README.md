# Virtual AI Office Platform

A modern web platform where users can access a team of autonomous AI agents that collaborate to complete user requests. Think of it as a digital company with AI employees working together.

# AI Office Dashboard

## Features

- **Manager Agent** - Task planning, coordination, and delegation to worker agents
- **Research Agent** - Information gathering and web research
- **Writer Agent** - Content creation, articles, reports, documentation
- **Developer Agent** - Code generation and project building
- **Designer Agent** - UI/UX design and layout specifications

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (Next.js)                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Dashboard │  │  Task Panel │  │  Agent Activity     │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP/WebSocket
┌────────────────────────────▼────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   API       │  │   Agent     │  │   Memory            │ │
│  │   Gateway   │  │   Orchestr. │  │   System            │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                    Agent Layer (LangGraph)                   │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐  │
│  │Manager │ │Research│ │ Writer │ │Developer│ │Designer  │  │
│  │ Agent  │ │ Agent  │ │ Agent  │ │ Agent   │ │  Agent   │  │
│  └────────┘ └────────┘ └────────┘ └────────┘ └──────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Tech Stack

- **Frontend:** Next.js 14, React, TypeScript, Tailwind CSS, Framer Motion
- **Backend:** Python FastAPI, SQLAlchemy
- **Database:** SQLite (development), PostgreSQL (production)
- **Real-time:** WebSockets for live updates

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.9+
- pip

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run the server
uvicorn app.main:app --reload
```

The backend API will be available at: http://localhost:8000

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

The frontend will be available at: http://localhost:3000

## Usage

1. Open http://localhost:3000 in your browser
2. Enter a request in the text box (e.g., "Research a crypto project and generate a detailed report")
3. Click "Submit Request"
4. Watch the AI agents collaborate in real-time
5. View the results when complete

### Example Requests

- "Research a crypto project and generate a detailed report."
- "Create a landing page for an AI startup and deploy it."
- "Write a Twitter thread explaining a blockchain protocol."
- "Analyze competitors for my business."

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/conversations | Create new conversation |
| GET | /api/conversations | List conversations |
| GET | /api/conversations/{id} | Get conversation details |
| POST | /api/tasks | Create and execute task |
| GET | /api/agents/status | Get agent statuses |
| WS | /ws/{conversation_id} | WebSocket for real-time updates |

## Project Structure

```
ai-office/
├── backend/
│   ├── app/
│   │   ├── api/           # API routes
│   │   │   ├── conversations.py
│   │   │   ├── tasks.py
│   │   │   └── agents.py
│   │   ├── agents/        # Agent implementations
│   │   │   ├── base.py
│   │   │   ├── manager.py
│   │   │   ├── research.py
│   │   │   ├── writer.py
│   │   │   ├── developer.py
│   │   │   └── designer.py
│   │   ├── services/      # Business logic
│   │   │   ├── orchestrator.py
│   │   │   └── memory.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── schemas.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/           # Next.js app router
│   │   │   ├── components/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── TaskInput.tsx
│   │   │   │   ├── AgentPanel.tsx
│   │   │   │   ├── AgentCard.tsx
│   │   │   │   └── ResultsPanel.tsx
│   │   │   ├── page.tsx
│   │   │   ├── layout.tsx
│   │   │   └── globals.css
│   │   ├── lib/           # Utilities
│   │   │   ├── api.ts
│   │   │   └── types.ts
│   │   └── hooks/         # React hooks
│   │       └── useAgentEvents.ts
│   ├── package.json
│   ├── tailwind.config.js
│   └── tsconfig.json
├── SPEC.md
└── README.md
```

## Deployment

### Backend (Render/Heroku)

```bash
# Install production dependencies
pip install gunicorn

# Run with gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend (Vercel)

```bash
cd frontend
vercel deploy
```

## Adding New Agents

To add a new agent:

1. Create a new file in `backend/app/agents/`
2. Extend the `BaseAgent` class
3. Implement the `execute` method
4. Register in `AGENT_REGISTRY`

Example:

```python
from app.agents.base import BaseAgent, AGENT_REGISTRY

class NewAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.agent_type = "new_agent"
        self.name = "New Agent"
        self.description = "Description of what it does"
        self.icon = "🤖"
    
    async def execute(self, task_id, title, description):
        # Implementation
        return {"result": "output"}

AGENT_REGISTRY["new_agent"] = NewAgent
```

## License

MIT License
