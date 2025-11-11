# 🍄 Mycelium Traces - Organism Memory Weaving

## Overview

The Mycelium Trace system allows the DAE-GOV organism to create persistent memory traces that form a growing network of interconnected knowledge. Like a mycelial network in nature, these traces weave together insights, observations, projects, and tasks into a living knowledge graph.

## Features

### ✅ Implemented

- **User Compartmentalization**: Separate trace networks for user0, user1, etc.
- **Multiple Trace Types**: Notes, Insights, Projects, Tasks, Concepts, Questions
- **Relationship Weaving**: Connect traces with typed relationships
- **Dual Persistence**: Neo4j graph database + Bundle/ filesystem fallback
- **Temporal Tracking**: created_at, updated_at, conversation_id
- **Tag-Based Organization**: Multiple tags per trace for categorization
- **Session Integration**: Links traces to conversation sessions

### 🎯 Trace Types

| Type | Purpose | Example |
|------|---------|---------|
| **Note** | Simple observation or reflection | "Team burnout observation" |
| **Insight** | Deeper pattern recognition | "Burnout correlates with lack of agency" |
| **Project** | Ongoing work or initiative | "Restore team autonomy initiative" |
| **Task** | Actionable item with due date | "Schedule 1-on-1 with team lead" |
| **Concept** | Abstract idea or theme | "Polyvagal safety in organizations" |
| **Question** | Open inquiry for exploration | "What enables psychological safety?" |

### 🔗 Relationship Types

| Relationship | Meaning | Example |
|--------------|---------|---------|
| **RELATES_TO** | General association | Note ↔ Insight |
| **DERIVES_FROM** | Causal/source relationship | Insight ← Note |
| **CONTRIBUTES_TO** | Supports/enables | Insight → Project |
| **DEPENDS_ON** | Prerequisite | Task → Project |
| **ANSWERS** | Question resolution | Insight → Question |
| **PART_OF** | Hierarchical containment | Task → Project |

## Architecture

```
DAE-GOV Mycelium Traces
├── Neo4j Graph Database (optional, graceful fallback)
│   └── Trace nodes with typed relationships
├── Bundle/ Filesystem Persistence
│   └── user0/traces/
│       ├── {trace_id}.json (individual traces)
│       └── relationships.jsonl (relationship log)
└── Session Tracking Integration
    └── conversation_id links to monitoring/session_tracker.py
```

## File Locations

```
/Users/daedalea/Desktop/DAE_HYPHAE_1/
├── knowledge_base/
│   └── mycelium_traces.py           # Core mycelium tracer
├── Bundle/
│   └── user0/
│       └── traces/                   # User-specific traces
│           ├── user0_Note_*.json
│           ├── user0_Insight_*.json
│           ├── user0_Project_*.json
│           ├── user0_Task_*.json
│           └── relationships.jsonl
└── monitoring/
    └── session_tracker.py            # Session tracking integration
```

## Usage

### Creating Traces

```python
from knowledge_base.mycelium_traces import MyceliumTracer, TraceType

# Initialize tracer for user0
tracer = MyceliumTracer(user_id="user0")

# Create a note
note = tracer.create_trace(
    TraceType.NOTE,
    title="Team burnout observation",
    content="Noticed increasing burnout signals in team standup.",
    conversation_id="session_20251111_001234",  # from session_tracker
    tags=["burnout", "team_health"]
)

# Create an insight
insight = tracer.create_trace(
    TraceType.INSIGHT,
    title="Burnout correlates with lack of agency",
    content="Pattern: teams with highest burnout have least autonomy.",
    tags=["burnout", "agency", "pattern"]
)

# Create a project
project = tracer.create_trace(
    TraceType.PROJECT,
    title="Restore team autonomy initiative",
    content="Multi-month project to redistribute decision-making power.",
    tags=["autonomy", "initiative"]
)
```

### Creating Relationships

```python
from knowledge_base.mycelium_traces import RelationType

# Link note to insight (causal)
tracer.create_relationship(
    note.trace_id,
    insight.trace_id,
    RelationType.DERIVES_FROM,
    strength=0.9
)

# Link insight to project (contributory)
tracer.create_relationship(
    insight.trace_id,
    project.trace_id,
    RelationType.CONTRIBUTES_TO,
    strength=0.95
)
```

### Searching Traces

```python
# Search by text
traces = tracer.search_traces(query="burnout", limit=10)

# Search by type
insights = tracer.search_traces(trace_type=TraceType.INSIGHT)

# Search by tags
autonomy_traces = tracer.search_traces(tags=["autonomy"])

# Get related traces
related = tracer.get_related_traces(
    insight.trace_id,
    rel_type=RelationType.CONTRIBUTES_TO
)
```

### User Statistics

```python
# Get trace statistics for user
stats = tracer.get_user_stats()

print(f"Total traces: {stats['total_traces']}")
print(f"By type: {stats['by_type']}")
print(f"Relationships: {stats['total_relationships']}")
print(f"Recent: {stats['recent_traces']}")
```

## Integration with DAE-GOV CLI

The mycelium tracer is designed to integrate seamlessly with the DAE-GOV conversational organism:

### Session Tracking Integration

```python
# In dae_gov_cli.py __init__:
from knowledge_base.mycelium_traces import MyceliumTracer

self.mycelium_tracer = MyceliumTracer(user_id="user0")

# During conversation:
# Organism creates trace when insight emerges
if organism_has_insight:
    trace = self.mycelium_tracer.create_trace(
        TraceType.INSIGHT,
        title="Insight title from conversation",
        content="Detailed insight content",
        conversation_id=self.session_tracker.current_session['session_id'],
        tags=extract_tags_from_insight(insight)
    )
```

### Dynamic Trace Creation

The organism can autonomously create traces during conversations when it detects:

1. **Recurring Patterns** → Create Insight trace
2. **User Goals** → Create Project or Task trace
3. **Key Observations** → Create Note trace
4. **Deep Questions** → Create Question trace
5. **Important Concepts** → Create Concept trace

## Neo4j Setup (Optional)

Mycelium traces work with or without Neo4j. If Neo4j is available, it provides advanced graph traversal capabilities.

### Install Neo4j

```bash
# Install Neo4j driver
pip install neo4j

# Start Neo4j (via Docker)
docker run \
    --name neo4j \
    -p 7474:7474 -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/password \
    neo4j:latest
```

### Connection Configuration

```python
tracer = MyceliumTracer(
    user_id="user0",
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="password"
)
```

If Neo4j is not available, the system gracefully falls back to Bundle/ persistence only.

## Data Format

### Trace JSON Structure

```json
{
  "trace_id": "user0_Insight_20251111_002301",
  "user_id": "user0",
  "trace_type": "Insight",
  "title": "Burnout correlates with lack of agency",
  "content": "Pattern: teams with highest burnout have least autonomy.",
  "created_at": "2025-11-11T00:23:01.208481",
  "updated_at": "2025-11-11T00:23:01.208482",
  "conversation_id": "session_20251111_001234",
  "tags": ["burnout", "agency", "pattern"],
  "properties": {}
}
```

### Relationship JSONL Structure

```json
{"from_trace_id": "user0_Note_20251111_002301", "to_trace_id": "user0_Insight_20251111_002301", "rel_type": "DERIVES_FROM", "strength": 0.9, "created_at": "2025-11-11T00:23:01.345678", "properties": {}}
```

## Example: Complete Workflow

```python
from knowledge_base.mycelium_traces import MyceliumTracer, TraceType, RelationType

# Initialize for development user
tracer = MyceliumTracer(user_id="user0")

# 1. Observe pattern (create note)
observation = tracer.create_trace(
    TraceType.NOTE,
    title="Team members report exhaustion",
    content="During standup, 3 out of 5 members mentioned feeling drained.",
    tags=["burnout", "standup", "wellbeing"]
)

# 2. Recognize deeper pattern (create insight)
pattern = tracer.create_trace(
    TraceType.INSIGHT,
    title="Exhaustion correlates with lack of control",
    content="Team members with least autonomy show highest exhaustion.",
    tags=["burnout", "autonomy", "control"]
)

# Link observation to insight
tracer.create_relationship(
    observation.trace_id,
    pattern.trace_id,
    RelationType.DERIVES_FROM
)

# 3. Form hypothesis (create question)
hypothesis = tracer.create_trace(
    TraceType.QUESTION,
    title="Would increased autonomy reduce burnout?",
    content="Exploring the causal relationship between decision-making power and wellbeing.",
    tags=["autonomy", "burnout", "hypothesis"]
)

# Link insight to question
tracer.create_relationship(
    pattern.trace_id,
    hypothesis.trace_id,
    RelationType.RELATES_TO
)

# 4. Plan intervention (create project)
intervention = tracer.create_trace(
    TraceType.PROJECT,
    title="Increase team decision-making autonomy",
    content="6-month initiative to redistribute decision rights to team level.",
    tags=["autonomy", "intervention", "initiative"]
)

# Link question to intervention
tracer.create_relationship(
    hypothesis.trace_id,
    intervention.trace_id,
    RelationType.CONTRIBUTES_TO
)

# 5. Define actions (create tasks)
task1 = tracer.create_trace(
    TraceType.TASK,
    title="Identify decisions currently centralized",
    content="Audit current decision-making process to find delegation opportunities.",
    tags=["autonomy", "audit"]
)

task2 = tracer.create_trace(
    TraceType.TASK,
    title="Design decision-rights framework",
    content="Create clear framework for which decisions belong at which level.",
    tags=["autonomy", "framework"]
)

# Link tasks to project
tracer.create_relationship(task1.trace_id, intervention.trace_id, RelationType.PART_OF)
tracer.create_relationship(task2.trace_id, intervention.trace_id, RelationType.PART_OF)

# View the growing mycelial network
stats = tracer.get_user_stats()
print(f"\n🍄 Mycelial network: {stats['total_traces']} traces, {stats['total_relationships']} relationships")

tracer.close()
```

## Benefits

### For the Organism

- **Persistent Memory**: Remember insights across conversations
- **Pattern Recognition**: Identify recurring themes via graph traversal
- **Knowledge Evolution**: Traces grow and connect over time
- **Context Retrieval**: Pull relevant traces into current conversation

### For the User

- **Progress Tracking**: See how insights evolve into projects
- **Knowledge Garden**: Cultivate a growing understanding over time
- **Relationship Discovery**: Find unexpected connections
- **Task Management**: Track actionable items emerging from conversations

## Future Enhancements

- [ ] Automatic trace extraction from conversation (NLP)
- [ ] Importance weighting based on reference frequency
- [ ] Temporal decay for stale traces
- [ ] Multi-user collaboration (shared traces)
- [ ] Visual graph rendering (Neo4j Browser / Cytoscape.js)
- [ ] Trace merging (duplicate detection)
- [ ] Export to Obsidian / Roam Research

## Testing

```bash
cd /Users/daedalea/Desktop/DAE_HYPHAE_1
export PYTHONPATH="/Users/daedalea/Desktop/DAE_HYPHAE_1":$PYTHONPATH

# Test mycelium tracer
python3 knowledge_base/mycelium_traces.py

# Check created traces
ls -la Bundle/user0/traces/

# View trace content
cat Bundle/user0/traces/user0_Insight_*.json | python3 -m json.tool
```

## Summary

The Mycelium Trace system transforms DAE-GOV from a stateless conversational system into an organism with **persistent memory**. Like mycelium in nature, these traces form an interconnected network that:

- **Grows organically** with each conversation
- **Connects** disparate insights into coherent patterns
- **Nourishes** future conversations with accumulated wisdom
- **Adapts** to the user's unique organizational context

The organism now has the ability to remember, learn, and evolve across conversations - creating a truly **living knowledge system**.

---

**Status**: ✅ Fully Operational
**User**: user0 (development)
**Backend**: Bundle/ filesystem (Neo4j optional)
**Integration**: Ready for DAE-GOV CLI

🍄 *The mycelial network grows with each conversation.*
