# Virtual AI Office Platform - Specification

## Project Overview

**Project Name:** AI Office  
**Type:** Full-stack Web Application  
**Core Functionality:** A virtual office platform where users can submit requests and a team of autonomous AI agents collaborate to plan, execute, and deliver results  
**Target Users:** Professionals and businesses needing AI-powered assistance for research, content creation, development, and automation tasks

---

## Architecture Overview

### Tech Stack

- **Frontend:** Next.js 14 with React, TypeScript, Tailwind CSS
- **Backend:** Python FastAPI
- **Agent Framework:** LangGraph for orchestration
- **Database:** SQLite (for simplicity) with SQLAlchemy ORM
- **Real-time:** Server-Sent Events (SSE) for live updates
- **Code Execution:** Integration with OpenHands sandbox

### System Architecture

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
│                    Agent Layer (LangGraph)                  │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐  │
│  │Manager │ │Research│ │ Writer │ │Developer│ │Designer  │  │
│  │ Agent  │ │ Agent  │ │ Agent  │ │ Agent   │ │  Agent   │  │
│  └────────┘ └────────┘ └────────┘ └────────┘ └──────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## UI/UX Specification

### Color Palette

| Role | Color | Hex |
|------|-------|-----|
| Background (Dark) | Charcoal | `#0D1117` |
| Background (Card) | Slate | `#161B22` |
| Background (Elevated) | Dark Gray | `#21262D` |
| Primary | Electric Blue | `#58A6FF` |
| Secondary | Soft Purple | `#A371F7` |
| Accent | Mint Green | `#3FB950` |
| Warning | Amber | `#D29922` |
| Error | Coral Red | `#F85149` |
| Text Primary | White | `#F0F6FC` |
| Text Secondary | Gray | `#8B949E` |
| Border | Dark Border | `#30363D` |

### Typography

- **Primary Font:** "JetBrains Mono" (monospace, tech aesthetic)
- **Secondary Font:** "Inter" (UI elements)
- **Heading Sizes:** 
  - H1: 32px, weight 700
  - H2: 24px, weight 600
  - H3: 18px, weight 600
- **Body:** 14px, weight 400
- **Small:** 12px, weight 400

### Layout Structure

```
┌────────────────────────────────────────────────────────────────┐
│  HEADER (Logo + Navigation + User)                              │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────────────────┐  ┌───────────────────────────┐ │
│  │                          │  │  AGENT WORKSPACE           │ │
│  │   TASK INPUT PANEL       │  │  ┌───────────────────────┐│ │
│  │                          │  │  │ Manager Agent Status  ││ │
│  │   [Request Input Area]   │  │  ├───────────────────────┤│ │
│  │                          │  │  │ Research Agent Status ││ │
│  │   [Task Type Selector]   │  │  ├───────────────────────┤│ │
│  │                          │  │  │ Writer Agent Status   ││ │
│  │   [Submit Button]        │  │  ├───────────────────────┤│ │
│  │                          │  │  │ Developer Agent Status││ │
│  │                          │  │  └───────────────────────┘│ │
│  └──────────────────────────┘  └───────────────────────────┘ │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  RESULTS PANEL                                           │ │
│  │  - Task Output                                           │ │
│  │  - Download/Export Options                               │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Components

#### 1. Header
- Logo: "AI Office" with robot icon
- Navigation: Dashboard, History, Settings
- User avatar (placeholder)

#### 2. Task Input Panel
- Large textarea for request (min 120px height)
- Task type dropdown (Research, Write, Develop, Design, General)
- Priority selector (Low, Medium, High)
- Submit button with loading state

#### 3. Agent Activity Panel
- Card for each agent showing:
  - Agent avatar/icon
  - Agent name
  - Current status (idle, working, completed, error)
  - Current task description
  - Progress indicator
- Animated pulse for active agents

#### 4. Results Panel
- Expandable sections for each deliverable
- Markdown rendering for content
- Copy to clipboard buttons
- Download options

### Animations

- Agent cards: Fade in with stagger (100ms delay between each)
- Status changes: Smooth color transitions (200ms)
- Progress bars: Animated gradient
- Active agent: Subtle pulse animation (2s infinite)
- Task submission: Button ripple effect

---

## Database Schema

### Tables

#### 1. conversations
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | String | User identifier |
| title | String | Conversation title |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update |

#### 2. tasks
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| conversation_id | UUID | FK to conversations |
| agent_type | String | Which agent owns this |
| title | String | Task title |
| description | Text | Task description |
| status | Enum | pending, in_progress, completed, failed |
| result | JSON | Task output |
| created_at | DateTime | Creation timestamp |
| completed_at | DateTime | Completion timestamp |

#### 3. messages
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| conversation_id | UUID | FK to conversations |
| role | String | user, assistant, agent |
| content | Text | Message content |
| metadata | JSON | Additional data |
| created_at | DateTime | Creation timestamp |

#### 4. user_preferences
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | String | User identifier |
| key | String | Preference key |
| value | JSON | Preference value |

---

## Agent Specifications

### Manager Agent
- **Role:** Task planning and coordination
- **Responsibilities:**
  - Parse user request
  - Break into subtasks
  - Assign to appropriate agents
  - Monitor progress
  - Aggregate results
- **Model:** GPT-4 (simulated with local LLM or mock)

### Research Agent
- **Role:** Information gathering and analysis
- **Tools:**
  - Web search (Tavily API)
  - Web scraping
  - URL content extraction
- **Output:** Summarized findings, key insights, source links

### Writer Agent
- **Role:** Content creation
- **Capabilities:**
  - Articles and blog posts
  - Technical documentation
  - Social media threads
  - Reports and summaries
- **Output:** Markdown content

### Developer Agent
- **Role:** Code generation and project building
- **Capabilities:**
  - Generate code from specifications
  - Create project structures
  - Basic debugging
- **Output:** Code files, project structure

### Designer Agent
- **Role:** UI/UX design and layout
- **Capabilities:**
  - Generate UI specifications
  - Create component layouts
  - Design system recommendations
- **Output:** Design specs, component descriptions

---

## API Endpoints

### REST API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/conversations | Create new conversation |
| GET | /api/conversations | List user conversations |
| GET | /api/conversations/{id} | Get conversation details |
| POST | /api/tasks | Submit new task |
| GET | /api/tasks/{id} | Get task status |
| GET | /api/tasks/{id}/result | Get task result |
| GET | /api/agents/status | Get all agent statuses |
| POST | /api/preferences | Save user preference |
| GET | /api/preferences | Get user preferences |

### WebSocket / SSE

| Event | Description |
|-------|-------------|
| task:started | Task execution started |
| task:progress | Agent progress update |
| task:completed | Task completed with result |
| task:failed | Task failed with error |
| agent:status | Agent status changed |

---

## Functionality Specification

### Core Features

1. **Task Submission**
   - User enters request in natural language
   - Selects task type or lets system auto-detect
   - Submits and receives confirmation

2. **Agent Orchestration**
   - Manager Agent receives task
   - Breaks into subtasks
   - Assigns to worker agents
   - Coordinates execution

3. **Real-time Updates**
   - SSE connection for live updates
   - Agent status in dashboard
   - Progress indicators

4. **Memory System**
   - Conversation history
   - Task history
   - User preferences storage

5. **Result Delivery**
   - Aggregated results from all agents
   - Export options (Markdown, PDF)
   - Copy to clipboard

### User Flows

#### Main Flow
1. User visits dashboard
2. Enters request in input panel
3. Clicks submit
4. Watches agent activity panel for progress
5. Receives results when complete

#### History Flow
1. User clicks History
2. Sees list of past conversations
3. Clicks on conversation
4. Views past results

---

## Acceptance Criteria

### Visual Checkpoints
- [ ] Dark theme with specified color palette applied
- [ ] JetBrains Mono font for code/tech elements
- [ ] Inter font for UI elements
- [ ] Agent cards display with proper status colors
- [ ] Animations smooth and performant
- [ ] Responsive layout works on desktop (1024px+)

### Functional Checkpoints
- [ ] Task submission creates new conversation
- [ ] Agent statuses update in real-time
- [ ] Results display after task completion
- [ ] Conversation history persists
- [ ] Memory system stores preferences

### Agent Checkpoints
- [ ] Manager agent can parse and break down tasks
- [ ] Research agent can gather information
- [ ] Writer agent can generate content
- [ ] Developer agent can generate code
- [ ] Designer agent can provide design specs

---

## File Structure

```
ai-office/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app
│   │   ├── config.py            # Configuration
│   │   ├── database.py         # Database setup
│   │   ├── models.py           # SQLAlchemy models
│   │   ├── schemas.py         # Pydantic schemas
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── conversations.py
│   │   │   ├── tasks.py
│   │   │   └── agents.py
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── base.py         # Base agent class
│   │   │   ├── manager.py      # Manager agent
│   │   │   ├── research.py     # Research agent
│   │   │   ├── writer.py       # Writer agent
│   │   │   ├── developer.py    # Developer agent
│   │   │   └── designer.py     # Designer agent
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── orchestrator.py # Task orchestration
│   │       └── memory.py        # Memory service
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── globals.css
│   │   │   ├── api/
│   │   │   │   └── routes.ts
│   │   │   └── components/
│   │   │       ├── Header.tsx
│   │   │       ├── TaskInput.tsx
│   │   │       ├── AgentPanel.tsx
│   │   │       ├── ResultsPanel.tsx
│   │   │       ├── AgentCard.tsx
│   │   │       └── ConversationList.tsx
│   │   ├── lib/
│   │   │   ├── api.ts
│   │   │   └── types.ts
│   │   └── hooks/
│   │       └── useAgentEvents.ts
│   ├── package.json
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── next.config.js
├── SPEC.md
└── README.md
```

---

## Deployment Instructions

### Local Development

1. **Backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   uvicorn app.main:app --reload
   ```

2. **Frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Access:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Production Deployment

- Frontend: Vercel/Netlify
- Backend: Render/Heroku/DigitalOcean
- Database: PostgreSQL (production)
