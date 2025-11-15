# DAE_HYPHAE_1 Development Strategy
**Phase 1.7: Web Deployment & Command Expansion**
**Date:** November 14, 2025
**Goal:** Personal companion + local web server for friends/family

---

## Executive Summary

**Current State:** Production-ready conversational organism (Phase 1.6 complete)
**Target:** Web-accessible interface + expanded command set
**Approach:** Incremental refactoring → API layer → web frontend
**Timeline:** 4-6 weeks to MVP web deployment

---

## Phase 1.7 Roadmap (4-6 Weeks)

### **Week 1: Command Expansion + Hybrid Mode (Foundation)**

**Priority 1: Port CLI Commands to Interactive (Days 1-2)**
- [ ] `/identity` - Mycelial identity display
- [ ] `/projects` - Active projects summary
- [ ] `/stats` - Learning statistics
- [ ] `/patterns` - Transformation patterns
- [ ] `/trajectory` - Felt-state trajectory
- [ ] `/remember` - Memory retrieval
- [ ] `/traces` - Mycelium traces
- [ ] `/insights` - Insights filter
- [ ] `/notes` - Notes filter

**Priority 2: Enable Hybrid Mode (Day 1)**
- [ ] Set `Config.HYBRID_ENABLED = True`
- [ ] Test memory retrieval
- [ ] Verify superject recording

**Priority 3: Search & Filter Foundation (Days 3-4)**
- [ ] Create `persona_layer/conversation_search.py`
- [ ] Implement text search across sessions
- [ ] Add date filtering
- [ ] Add organ filtering

**Deliverable:** Interactive mode with 15+ commands, search capability

---

### **Week 2: Data Export + Architecture Refactoring**

**Priority 1: GDPR-Compliant Export (Days 1-2)**
- [ ] `/export_all` - Complete user data ZIP
- [ ] `/export_feedback` - Feedback CSV
- [ ] `/export_gdpr` - Privacy-compliant bundle
- [ ] `/delete_data` - Right to be forgotten

**Priority 2: Project Restructure for Web (Days 3-5)**

**Current Structure Issues:**
- 40+ test files in root directory
- Mixed concerns (training scripts, utilities, tests)
- No clear API boundary

**Target Structure:**
```
DAE_HYPHAE_1/
├── src/                          # 🆕 Core application code
│   ├── api/                      # 🆕 API layer (Flask/FastAPI)
│   │   ├── __init__.py
│   │   ├── app.py               # Main API server
│   │   ├── routes/              # API endpoints
│   │   │   ├── conversation.py  # POST /chat, GET /history
│   │   │   ├── user.py          # GET /user, PUT /profile
│   │   │   ├── commands.py      # GET /commands, POST /command
│   │   │   └── export.py        # GET /export/*
│   │   ├── middleware/          # Auth, CORS, rate limiting
│   │   └── schemas/             # Request/response models
│   │
│   ├── core/                     # Organism core (existing)
│   │   ├── organs/              # 11-organ system
│   │   ├── persona_layer/       # Conversational logic
│   │   ├── memory/              # 5-tier memory
│   │   └── monitoring/          # Identity tracking
│   │
│   ├── cli/                      # 🆕 CLI interfaces
│   │   ├── dae_interactive.py   # Interactive mode
│   │   ├── dae_gov_cli.py       # Original CLI
│   │   └── dae_orchestrator.py  # Unified entry
│   │
│   └── utils/                    # 🆕 Shared utilities
│       ├── config.py            # Configuration
│       ├── logging.py           # Logging utilities
│       └── validation.py        # Input validation
│
├── frontend/                     # 🆕 Web interface
│   ├── public/
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── Chat.jsx         # Chat interface
│   │   │   ├── Commands.jsx     # Command palette
│   │   │   ├── Profile.jsx      # User profile
│   │   │   └── Dashboard.jsx    # Statistics
│   │   ├── services/            # API client
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
├── tests/                        # Organized tests
│   ├── unit/
│   ├── integration/
│   ├── validation/
│   └── e2e/
│
├── training/                     # Training scripts
├── scripts/                      # Utilities
├── docs/                         # Documentation
├── data/                         # Persistent data
│   ├── users/                   # User profiles
│   ├── sessions/                # Session history
│   ├── knowledge_base/          # Training data
│   └── results/                 # Outputs
│
├── config.py                     # Root config (symlink to src/utils/)
├── requirements.txt              # Python dependencies
├── requirements-dev.txt          # Dev dependencies
├── .env.example                  # Environment template
├── docker-compose.yml            # 🆕 Local deployment
└── README.md                     # Updated guide
```

**Migration Strategy:**
1. Create `src/` directory structure
2. Move `persona_layer/`, `organs/`, `memory/`, `monitoring/` → `src/core/`
3. Move CLI files → `src/cli/`
4. Create `src/api/` skeleton
5. Update imports (use `from src.core.persona_layer import...`)
6. Update `PYTHONPATH` in scripts

**Deliverable:** Clean project structure, API-ready architecture

---

### **Week 3: API Layer Development**

**Technology Choice: FastAPI (Recommended)**

**Why FastAPI:**
- ✅ Modern async support (handles concurrent users)
- ✅ Auto-generated OpenAPI docs
- ✅ Type hints = automatic validation
- ✅ WebSocket support (real-time chat)
- ✅ Easy to deploy (Uvicorn, Docker)

**API Endpoints:**

```python
# src/api/routes/conversation.py

@router.post("/chat")
async def chat(request: ChatRequest, user_id: str = Depends(get_user)):
    """
    Send message to DAE and get response.

    Request:
        {
            "message": "I'm feeling overwhelmed",
            "mode": "detailed"
        }

    Response:
        {
            "emission": "I hear you...",
            "confidence": 0.85,
            "nexuses": [...],
            "organs": {...},
            "transduction": {...}
        }
    """
    organism = get_organism()  # Singleton
    result = organism.process_text(
        text=request.message,
        user_id=user_id,
        username=get_username(user_id),
        enable_phase2=True
    )
    return format_response(result)

@router.get("/history")
async def get_history(user_id: str = Depends(get_user), limit: int = 50):
    """Get conversation history for user."""
    sessions = load_user_sessions(user_id, limit=limit)
    return {"sessions": sessions}

@router.post("/command")
async def execute_command(cmd: CommandRequest, user_id: str = Depends(get_user)):
    """
    Execute DAE command (e.g., /identity, /stats).

    Request:
        {
            "command": "identity"
        }

    Response:
        {
            "output": "...",
            "data": {...}
        }
    """
    handler = get_command_handler(cmd.command)
    result = await handler.execute(user_id)
    return result
```

**Session Management:**
```python
# src/api/middleware/auth.py

# Option 1: Simple token-based (local deployment)
# - Generate token on first visit
# - Store in localStorage
# - No passwords needed

# Option 2: Username/password (production)
# - bcrypt hashed passwords
# - JWT tokens
# - Secure cookie storage
```

**WebSocket for Real-Time Chat:**
```python
# src/api/routes/conversation.py

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket, user_id: str):
    """
    Real-time chat over WebSocket.

    Client sends: {"message": "Hello"}
    Server streams: {"chunk": "H", "done": false}
                   {"chunk": "ell", "done": false}
                   {"chunk": "o!", "done": true}
    """
    await websocket.accept()
    organism = get_organism()

    while True:
        data = await websocket.receive_json()
        message = data.get("message")

        # Stream response word-by-word
        result = organism.process_text(
            text=message,
            user_id=user_id,
            username=get_username(user_id)
        )

        # Simulate streaming (can enhance with real LLM streaming)
        emission = result['felt_states']['emission_text']
        for word in emission.split():
            await websocket.send_json({
                "chunk": word + " ",
                "done": False
            })
            await asyncio.sleep(0.05)  # Simulate typing

        await websocket.send_json({"done": True, "metadata": result})
```

**Deliverable:** Functional API with chat, history, commands

---

### **Week 4: Frontend Development**

**Technology: React + Vite (Recommended)**

**Why React:**
- ✅ Component reusability
- ✅ Large ecosystem (libraries for chat UI)
- ✅ Fast with Vite (instant hot reload)
- ✅ Easy deployment (static files)

**Core Components:**

```jsx
// frontend/src/components/Chat.jsx

import { useState, useEffect } from 'react'
import { sendMessage, useWebSocket } from '../services/api'

export function Chat({ userId, username }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const { connected, send } = useWebSocket(userId)

  const handleSend = async () => {
    if (!input.trim()) return

    // Add user message
    setMessages(prev => [...prev, {
      role: 'user',
      content: input,
      timestamp: new Date()
    }])

    // Send to API
    const response = await sendMessage(input, userId)

    // Add DAE response
    setMessages(prev => [...prev, {
      role: 'dae',
      content: response.emission,
      confidence: response.confidence,
      timestamp: new Date()
    }])

    setInput('')
  }

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, i) => (
          <Message key={i} message={msg} username={username} />
        ))}
      </div>

      <div className="input-area">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyPress={e => e.key === 'Enter' && handleSend()}
          placeholder={`Message DAE as ${username}...`}
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  )
}
```

```jsx
// frontend/src/components/Commands.jsx

export function CommandPalette({ userId }) {
  const [open, setOpen] = useState(false)
  const [commands] = useState([
    { cmd: 'identity', desc: 'Show mycelial identity' },
    { cmd: 'stats', desc: 'Learning statistics' },
    { cmd: 'patterns', desc: 'Transformation patterns' },
    { cmd: 'remember', desc: 'Retrieve similar moments' },
    // ... more commands
  ])

  const handleCommand = async (cmd) => {
    const result = await executeCommand(cmd, userId)
    // Display result in modal or side panel
    setOpen(false)
  }

  return (
    <>
      <button onClick={() => setOpen(!open)}>
        Commands (/)
      </button>

      {open && (
        <div className="command-palette">
          {commands.map(({ cmd, desc }) => (
            <div key={cmd} onClick={() => handleCommand(cmd)}>
              <strong>/{cmd}</strong> - {desc}
            </div>
          ))}
        </div>
      )}
    </>
  )
}
```

**UI/UX Considerations:**
- Dark mode by default (option for light)
- Keyboard shortcuts (`/` for commands, `Ctrl+K` for search)
- Mobile-responsive (flexbox/grid)
- Accessibility (ARIA labels, keyboard nav)

**Deliverable:** Functional web chat interface

---

### **Weeks 5-6: Polish & Deployment**

**Week 5: Testing & Optimization**
- [ ] E2E tests (Playwright/Cypress)
- [ ] Load testing (Locust - simulate 10+ concurrent users)
- [ ] Performance profiling (identify bottlenecks)
- [ ] Security audit (OWASP Top 10)

**Week 6: Local Deployment Setup**
- [ ] Docker Compose configuration
- [ ] Nginx reverse proxy (optional, for HTTPS)
- [ ] Auto-start scripts (systemd/launchd)
- [ ] Backup/restore procedures
- [ ] User documentation

---

## Deployment Architecture

### **Option A: Local-Only (Simplest)**

```yaml
# docker-compose.yml

version: '3.8'

services:
  backend:
    build: ./src/api
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - PYTHONPATH=/app
      - HYBRID_ENABLED=true

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

**Access:** `http://localhost:3000`

**Pros:**
- ✅ No hosting costs
- ✅ Full privacy (data never leaves machine)
- ✅ Easy to run (`docker-compose up`)

**Cons:**
- ❌ No remote access
- ❌ Requires Docker installation

---

### **Option B: Local Network (Friends/Family)**

**Setup:**
1. Run on home server/Mac mini
2. Configure local DNS (e.g., `dae.local`)
3. Access from any device on home WiFi

**Tools:**
- **Tailscale** (free VPN) - Access from anywhere securely
- **ngrok** (free tier) - Temporary public URL for demos

**Access:** `http://dae.local` or `https://[random].ngrok.io`

**Pros:**
- ✅ Access from phone, tablet, other computers
- ✅ Still private (not on public internet)
- ✅ Low cost (just home internet)

**Cons:**
- ❌ Requires always-on machine
- ❌ Limited to your network (or VPN)

---

### **Option C: Cloud Hosting (Production) - Future Phase**

**Not recommended for Phase 1.7**, but here's the path if needed later:

```
┌─────────────────────────────────────────────┐
│ Frontend: Vercel/Netlify (static hosting)  │
│ - React app                                 │
│ - Free tier: unlimited bandwidth            │
└─────────────┬───────────────────────────────┘
              │ API calls
              ▼
┌─────────────────────────────────────────────┐
│ Backend: DigitalOcean/Railway              │
│ - Docker container                          │
│ - $5-20/month                               │
└─────────────┬───────────────────────────────┘
              │ Data storage
              ▼
┌─────────────────────────────────────────────┐
│ Database: PostgreSQL + S3                  │
│ - Managed service                           │
│ - $10-30/month                              │
└─────────────────────────────────────────────┘
```

**Total Cost:** $15-50/month
**When to consider:** >10 regular users, need 24/7 uptime

---

## Migration Plan (Week 2 Detailed)

### **Step 1: Create New Structure (Non-Breaking)**

```bash
# Day 1: Create directories
mkdir -p src/{api,core,cli,utils}
mkdir -p src/api/{routes,middleware,schemas}
mkdir -p frontend/src/{components,services}

# Day 2: Copy (don't move yet) core files
cp -r persona_layer src/core/
cp -r organs src/core/
cp -r memory src/core/
cp -r monitoring src/core/

# Day 3: Create API skeleton
touch src/api/app.py
touch src/api/routes/{conversation,user,commands,export}.py

# Day 4: Test imports work
python3 -c "from src.core.persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper"

# Day 5: If tests pass, remove old locations
# rm -rf persona_layer organs memory monitoring
```

### **Step 2: Update Imports**

**Find/Replace Across Codebase:**
```python
# Old import
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

# New import
from src.core.persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
```

**Automated Script:**
```bash
# scripts/update_imports.sh
find . -name "*.py" -exec sed -i '' 's/from persona_layer/from src.core.persona_layer/g' {} +
find . -name "*.py" -exec sed -i '' 's/from organs/from src.core.organs/g' {} +
find . -name "*.py" -exec sed -i '' 's/from memory/from src.core.memory/g' {} +
```

### **Step 3: Update PYTHONPATH**

```bash
# Old (everywhere in scripts)
export PYTHONPATH="/Users/daedalea/Desktop/DAE_HYPHAE_1":$PYTHONPATH

# New (auto-detects project root)
export PYTHONPATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)":$PYTHONPATH

# Or add to .env
echo 'PYTHONPATH=$(pwd)' >> .env
```

### **Step 4: Validate No Breakage**

```bash
# Run all tests
python3 dae_orchestrator.py validate --full

# If 100% maturity maintained → migration successful
```

---

## Success Metrics

### **Week 1 Goals:**
- [ ] Interactive mode has 15+ commands
- [ ] Hybrid mode enabled and working
- [ ] Search across conversations functional
- [ ] No regression in organism performance

### **Week 2 Goals:**
- [ ] Project restructured (src/ directory)
- [ ] All tests passing with new structure
- [ ] GDPR export working
- [ ] API skeleton created

### **Week 4 Goals:**
- [ ] Can chat via web browser
- [ ] Commands accessible via UI
- [ ] Profile/history viewable
- [ ] Runs on `localhost:3000`

### **Week 6 Goals:**
- [ ] Docker Compose working
- [ ] Accessible on local network
- [ ] Friends/family can use
- [ ] Documentation complete

---

## Risk Mitigation

### **Risk 1: Breaking Existing Functionality**
**Mitigation:**
- Copy first, move later
- Run validation tests after each change
- Git branches for major refactors
- Keep old structure until 100% validated

### **Risk 2: Performance Degradation**
**Mitigation:**
- Profile before/after API layer
- Use async/await for concurrent requests
- Consider Redis for session caching
- Load test with 10+ users

### **Risk 3: Scope Creep**
**Mitigation:**
- MVP first (chat + commands only)
- No advanced features (analytics, teams, etc.)
- Defer cloud hosting to Phase 2
- Time-box each week strictly

---

## Next Immediate Actions (This Session)

**1. Enable Hybrid Mode (5 minutes)**
```python
# In config.py, change:
HYBRID_ENABLED = True
```

**2. Port First 3 Commands (30 minutes)**
```python
# In dae_interactive.py, add:
- cmd_identity()
- cmd_stats()
- cmd_projects()
```

**3. Test Commands Work (10 minutes)**
```bash
python3 dae_interactive.py
# Type: /identity, /stats, /projects
```

**4. Update CLAUDE.md (15 minutes)**
- Add Phase 1.6 completion status
- Update version to 5.1.0
- Add web deployment roadmap section

---

## Technology Stack Summary

**Backend:**
- Python 3.9+
- FastAPI (API framework)
- Uvicorn (ASGI server)
- Pydantic (validation)
- WebSockets (real-time)

**Frontend:**
- React 18
- Vite (build tool)
- Axios (HTTP client)
- CSS Modules / Tailwind

**Deployment:**
- Docker + Docker Compose
- Nginx (optional, for HTTPS)
- Tailscale / ngrok (remote access)

**Development:**
- Black (code formatting)
- Pylint (linting)
- Pytest (testing)
- ESLint + Prettier (frontend)

---

## Conclusion

This strategy provides a clear path from current CLI/interactive modes to a web-accessible interface suitable for personal use and sharing with friends/family.

**Key Principles:**
1. **Incremental** - No big-bang rewrite
2. **Validated** - Test after each change
3. **Backwards Compatible** - CLI still works
4. **Privacy-First** - Local deployment default
5. **User-Focused** - Commands + chat as priorities

**Timeline:** 4-6 weeks to functional web deployment
**Effort:** 40-60 hours total
**Risk:** Low (incremental approach with validation)

---

**Ready to start?** Let's begin with enabling hybrid mode and porting commands! 🚀
