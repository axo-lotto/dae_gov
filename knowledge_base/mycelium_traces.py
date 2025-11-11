#!/usr/bin/env python3
"""
Mycelium Traces - Organism Memory Weaving
==========================================

Allows the DAE-GOV organism to create persistent memory traces (notes, insights,
projects, tasks) within the Neo4j knowledge graph. These traces form a mycelial
network of interconnected knowledge that grows with each conversation.

Architecture:
- User-compartmentalized (user0, user1, etc.)
- Trace types: Note, Insight, Project, Task, Concept
- Relationships: RELATES_TO, DERIVES_FROM, CONTRIBUTES_TO, DEPENDS_ON
- Temporal tracking: created_at, updated_at, conversation_id

Integrated with:
- Session tracking (monitoring/session_tracker.py)
- Neo4j knowledge graph (knowledge_base/neo4j_knowledge_graph.py)
- Bundle memory system (Bundle/user*/traces/)

Author: Claude Code (November 2025)
Status: Phase 2.3 - Mycelium Trace System
"""

import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict, field
from pathlib import Path
from datetime import datetime
from enum import Enum

try:
    from neo4j import GraphDatabase
except ImportError:
    print("⚠️  Neo4j driver not installed. Install with: pip install neo4j")
    GraphDatabase = None


class TraceType(Enum):
    """Types of mycelium traces the organism can create."""
    NOTE = "Note"  # Simple observation or reflection
    INSIGHT = "Insight"  # Deeper pattern recognition or understanding
    PROJECT = "Project"  # Ongoing work or initiative
    TASK = "Task"  # Actionable item with due date
    CONCEPT = "Concept"  # Abstract idea or theme
    QUESTION = "Question"  # Open inquiry for exploration


class RelationType(Enum):
    """Relationship types between traces."""
    RELATES_TO = "RELATES_TO"  # General association
    DERIVES_FROM = "DERIVES_FROM"  # Causal/source relationship
    CONTRIBUTES_TO = "CONTRIBUTES_TO"  # Supports/enables relationship
    DEPENDS_ON = "DEPENDS_ON"  # Prerequisite relationship
    ANSWERS = "ANSWERS"  # Question→Insight relationship
    PART_OF = "PART_OF"  # Hierarchical relationship


@dataclass
class Vector35DSignature:
    """
    Vector35D signature for organism felt state.

    Captures the 35-dimensional physical-feeling duality vector that represents
    the organism's felt understanding of this trace's content.

    Architecture (from DAE 3.0 AXO ARC):
    - Physical Substrate (0-9): Spatial, color, temporal reality
    - Mathematical Invariants (10-17): Symmetry, topology
    - Process Philosophy (18-24): Prehension, satisfaction, concrescence
    - Bagua Creative (25-32): Creative intervention space
    - Learning Dynamics (33-34): Confidence, gradient
    """
    dimensions: List[float] = field(default_factory=lambda: [0.0] * 35)

    # Extracted felt properties (for quick access)
    prehension_intensity: float = 0.0  # dim 18: How strongly organism feels this
    satisfaction_level: float = 0.0    # dim 19: Organism satisfaction with trace
    concrescence_phase: float = 0.0     # dim 20: Phase of becoming (0-1)
    subjective_aim: float = 0.0         # dim 21: Goal-directedness
    archetypal_lure: float = 0.0        # dim 23: Attraction to archetypal forms
    lake_joy: float = 0.0               # dim 32: EO archetypal satisfaction
    confidence_score: float = 0.5       # dim 33: Learning confidence
    learning_gradient: float = 0.0      # dim 34: Direction of improvement

    def to_dict(self) -> dict:
        return {
            'dimensions': self.dimensions,
            'felt_properties': {
                'prehension_intensity': self.prehension_intensity,
                'satisfaction_level': self.satisfaction_level,
                'concrescence_phase': self.concrescence_phase,
                'subjective_aim': self.subjective_aim,
                'archetypal_lure': self.archetypal_lure,
                'lake_joy': self.lake_joy,
                'confidence_score': self.confidence_score,
                'learning_gradient': self.learning_gradient
            }
        }


@dataclass
class FeltState:
    """
    Complete felt organism state captured during trace processing.

    Based on TSK (Trace State Kernel) from DAE 3.0 epoch learning system.
    Captures the organism's complete experiential understanding.
    """
    # V0 Energy & Convergence
    initial_energy: float = 1.0
    final_energy: float = 0.5
    energy_descent_rate: float = 0.0
    convergence_cycles: int = 0
    kairos_moment_detected: bool = False

    # Organ Coherences (6 organs)
    organ_coherences: Dict[str, float] = field(default_factory=dict)  # NDAM, SANS, BOND, RNX, EO, CARD

    # EO Family Detection
    eo_family: Optional[str] = None
    eo_entropy: float = 0.0
    eo_balance: float = 0.0

    # Hebbian Activation
    hebbian_patterns_activated: List[str] = field(default_factory=list)
    hebbian_confidence: float = 0.0

    # Satisfaction & Coherence
    satisfaction_level: float = 0.0
    satisfaction_variance: float = 0.0
    hybrid_coherence: float = 0.0

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class MyceliumTrace:
    """A single trace in the mycelial knowledge network with organism felt understanding."""
    trace_id: str
    user_id: str
    trace_type: TraceType
    title: str
    content: str
    created_at: str
    updated_at: str
    conversation_id: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    properties: Dict[str, any] = field(default_factory=dict)

    # 🌀 VECTOR SIGNATURE INTEGRATION (DAE 3.0 AXO ARC)
    vector_signature: Optional[Vector35DSignature] = None
    felt_state: Optional[FeltState] = None

    # Epoch Learning Integration
    epoch_metadata: Dict[str, any] = field(default_factory=dict)  # cluster_id, family_id, accuracy
    transformation_learned_from: Optional[str] = None  # trace_id of source trace if learned via epoch

    def to_dict(self) -> dict:
        d = asdict(self)
        d['trace_type'] = self.trace_type.value
        if self.vector_signature:
            d['vector_signature'] = self.vector_signature.to_dict()
        if self.felt_state:
            d['felt_state'] = self.felt_state.to_dict()
        return d


@dataclass
class TraceRelationship:
    """Relationship between two traces."""
    from_trace_id: str
    to_trace_id: str
    rel_type: RelationType
    strength: float = 1.0  # 0.0-1.0 confidence
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    properties: Dict[str, any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        d['rel_type'] = self.rel_type.value
        return d


class MyceliumTracer:
    """
    Manages mycelium traces in Neo4j and Bundle/ filesystem.

    Features:
    - User-compartmentalized traces
    - Automatic session tracking integration
    - Dual persistence (Neo4j + Bundle/)
    - Relationship weaving
    - Temporal queries
    - Tag-based retrieval

    The organism uses this to "remember" across conversations,
    creating a growing mycelial network of understanding.
    """

    def __init__(self,
                 user_id: str = "user0",
                 neo4j_uri: str = "bolt://localhost:7687",
                 neo4j_user: str = "neo4j",
                 neo4j_password: str = "password",
                 bundle_path: str = "/Users/daedalea/Desktop/DAE_HYPHAE_1/Bundle"):
        """
        Initialize mycelium tracer.

        Args:
            user_id: User identifier (user0, user1, etc.)
            neo4j_uri: Neo4j connection URI
            neo4j_user: Neo4j username
            neo4j_password: Neo4j password
            bundle_path: Path to Bundle/ directory
        """
        self.user_id = user_id
        self.bundle_path = Path(bundle_path)
        self.user_trace_dir = self.bundle_path / user_id / "traces"

        # Ensure trace directory exists
        self.user_trace_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Neo4j connection (optional)
        self.driver = None
        self.neo4j_available = False

        if GraphDatabase is not None:
            try:
                self.driver = GraphDatabase.driver(
                    neo4j_uri,
                    auth=(neo4j_user, neo4j_password)
                )
                # Test connection
                with self.driver.session() as session:
                    session.run("RETURN 1 as test").single()
                self.neo4j_available = True
                print(f"✅ Neo4j connected for {user_id}")
            except Exception as e:
                print(f"⚠️  Neo4j not available, using Bundle/ only: {e}")
                self.driver = None

        # Create constraints (if Neo4j available)
        if self.neo4j_available:
            self._create_constraints()

        # Initialize felt capture system (DAE 3.0 AXO ARC inspired)
        try:
            from knowledge_base.simple_felt_capture import SimpleFeltCapture
            hebbian_path = self.bundle_path.parent / "TSK" / "conversational_r_matrix.json"
            self.felt_capture = SimpleFeltCapture(
                hebbian_memory_path=str(hebbian_path) if hebbian_path.exists() else None
            )
            print(f"   ✅ Felt capture ready (epoch learning enabled)")
        except Exception as e:
            print(f"   ⚠️  Felt capture unavailable: {e}")
            self.felt_capture = None

    def _create_constraints(self):
        """Create Neo4j constraints for trace nodes."""
        if not self.neo4j_available:
            return

        with self.driver.session() as session:
            # Unique constraint on trace_id
            try:
                session.run("""
                    CREATE CONSTRAINT trace_id_unique IF NOT EXISTS
                    FOR (t:Trace) REQUIRE t.trace_id IS UNIQUE
                """)
            except Exception:
                pass  # Constraint may already exist

    def create_trace(self,
                    trace_type: TraceType,
                    title: str,
                    content: str,
                    conversation_id: Optional[str] = None,
                    tags: List[str] = None,
                    properties: Dict[str, any] = None,
                    organ_states: Optional[Dict[str, float]] = None) -> MyceliumTrace:
        """
        Create a new mycelium trace with automatic felt state capture.

        Args:
            trace_type: Type of trace (Note, Insight, Project, Task, etc.)
            title: Brief title
            content: Full content/description
            conversation_id: Optional session ID from session_tracker
            tags: Optional tags for categorization
            properties: Optional additional properties
            organ_states: Optional organ coherence states (if available from orchestrator)

        Returns:
            MyceliumTrace object with captured felt state
        """
        trace_id = f"{self.user_id}_{trace_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Capture felt state (DAE 3.0 epoch learning inspired)
        felt_state_simple = None
        vector_sig = None

        if self.felt_capture:
            try:
                # Capture conversational felt state
                felt_state_simple = self.felt_capture.capture_from_conversation(
                    text=content,
                    trace_type=trace_type.value,
                    organ_states=organ_states,
                    conversation_id=conversation_id
                )

                # Convert to vector signature for similarity search
                felt_vector = felt_state_simple.to_vector()
                vector_sig = Vector35DSignature(
                    dimensions=list(felt_vector) + [0.0] * 28,  # Pad to 35D
                    satisfaction_level=float(felt_state_simple.satisfaction_level),
                    prehension_intensity=float(felt_state_simple.processing_energy),
                    confidence_score=0.5  # Default confidence
                )

            except Exception as e:
                print(f"   ⚠️  Felt capture failed: {e}")

        trace = MyceliumTrace(
            trace_id=trace_id,
            user_id=self.user_id,
            trace_type=trace_type,
            title=title,
            content=content,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            conversation_id=conversation_id,
            tags=tags or [],
            properties=properties or {},
            vector_signature=vector_sig,
            # Store simplified felt state in epoch_metadata
            epoch_metadata={
                'felt_state_7d': felt_vector.tolist() if felt_state_simple else None,
                'organ_coherences': {
                    'LISTENING': felt_state_simple.listening_coherence if felt_state_simple else 0.5,
                    'EMPATHY': felt_state_simple.empathy_coherence if felt_state_simple else 0.5,
                    'WISDOM': felt_state_simple.wisdom_coherence if felt_state_simple else 0.5,
                    'AUTHENTICITY': felt_state_simple.authenticity_coherence if felt_state_simple else 0.5,
                    'PRESENCE': felt_state_simple.presence_coherence if felt_state_simple else 0.5
                } if felt_state_simple else {},
                'satisfaction': felt_state_simple.satisfaction_level if felt_state_simple else 0.5,
                'energy': felt_state_simple.processing_energy if felt_state_simple else 0.5
            }
        )

        # Save to Bundle/
        self._save_trace_to_bundle(trace)

        # Save to Neo4j (if available)
        if self.neo4j_available:
            self._save_trace_to_neo4j(trace)

        print(f"✅ Created trace: {trace.title} ({trace_type.value})")
        return trace

    def _save_trace_to_bundle(self, trace: MyceliumTrace):
        """Save trace to Bundle/ filesystem."""
        trace_file = self.user_trace_dir / f"{trace.trace_id}.json"
        with open(trace_file, 'w') as f:
            json.dump(trace.to_dict(), f, indent=2)

    def _save_trace_to_neo4j(self, trace: MyceliumTrace):
        """Save trace to Neo4j graph."""
        if not self.neo4j_available:
            return

        with self.driver.session() as session:
            session.run("""
                MERGE (t:Trace {trace_id: $trace_id})
                SET t.user_id = $user_id,
                    t.trace_type = $trace_type,
                    t.title = $title,
                    t.content = $content,
                    t.created_at = $created_at,
                    t.updated_at = $updated_at,
                    t.conversation_id = $conversation_id,
                    t.tags = $tags
                SET t += $properties
            """, {
                'trace_id': trace.trace_id,
                'user_id': trace.user_id,
                'trace_type': trace.trace_type.value,
                'title': trace.title,
                'content': trace.content,
                'created_at': trace.created_at,
                'updated_at': trace.updated_at,
                'conversation_id': trace.conversation_id,
                'tags': trace.tags,
                'properties': trace.properties
            })

    def create_relationship(self,
                          from_trace_id: str,
                          to_trace_id: str,
                          rel_type: RelationType,
                          strength: float = 1.0,
                          properties: Dict[str, any] = None) -> TraceRelationship:
        """
        Create relationship between two traces.

        Args:
            from_trace_id: Source trace ID
            to_trace_id: Target trace ID
            rel_type: Relationship type
            strength: Relationship strength (0.0-1.0)
            properties: Optional additional properties

        Returns:
            TraceRelationship object
        """
        relationship = TraceRelationship(
            from_trace_id=from_trace_id,
            to_trace_id=to_trace_id,
            rel_type=rel_type,
            strength=strength,
            properties=properties or {}
        )

        # Save to Neo4j (relationships are graph-native)
        if self.neo4j_available:
            self._save_relationship_to_neo4j(relationship)

        # Also save to Bundle/ for persistence
        self._save_relationship_to_bundle(relationship)

        return relationship

    def _save_relationship_to_neo4j(self, rel: TraceRelationship):
        """Save relationship to Neo4j graph."""
        if not self.neo4j_available:
            return

        with self.driver.session() as session:
            session.run(f"""
                MATCH (from:Trace {{trace_id: $from_trace_id}})
                MATCH (to:Trace {{trace_id: $to_trace_id}})
                MERGE (from)-[r:{rel.rel_type.value}]->(to)
                SET r.strength = $strength,
                    r.created_at = $created_at
                SET r += $properties
            """, {
                'from_trace_id': rel.from_trace_id,
                'to_trace_id': rel.to_trace_id,
                'strength': rel.strength,
                'created_at': rel.created_at,
                'properties': rel.properties
            })

    def _save_relationship_to_bundle(self, rel: TraceRelationship):
        """Save relationship to Bundle/ filesystem."""
        rel_file = self.user_trace_dir / "relationships.jsonl"
        with open(rel_file, 'a') as f:
            f.write(json.dumps(rel.to_dict()) + '\n')

    def get_trace(self, trace_id: str) -> Optional[MyceliumTrace]:
        """Retrieve a trace by ID."""
        # Try Bundle/ first
        trace_file = self.user_trace_dir / f"{trace_id}.json"
        if trace_file.exists():
            with open(trace_file, 'r') as f:
                data = json.load(f)
                data['trace_type'] = TraceType(data['trace_type'])
                return MyceliumTrace(**data)

        # Try Neo4j if available
        if self.neo4j_available:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (t:Trace {trace_id: $trace_id, user_id: $user_id})
                    RETURN t
                """, {'trace_id': trace_id, 'user_id': self.user_id})

                record = result.single()
                if record:
                    node = record['t']
                    return MyceliumTrace(
                        trace_id=node['trace_id'],
                        user_id=node['user_id'],
                        trace_type=TraceType(node['trace_type']),
                        title=node['title'],
                        content=node['content'],
                        created_at=node['created_at'],
                        updated_at=node['updated_at'],
                        conversation_id=node.get('conversation_id'),
                        tags=node.get('tags', []),
                        properties=dict(node)
                    )

        return None

    def search_traces(self,
                     query: str = None,
                     trace_type: TraceType = None,
                     tags: List[str] = None,
                     limit: int = 10) -> List[MyceliumTrace]:
        """
        Search traces by query, type, or tags.

        Args:
            query: Text search in title/content
            trace_type: Filter by trace type
            tags: Filter by tags
            limit: Maximum results

        Returns:
            List of matching traces
        """
        traces = []

        # Search Bundle/ (filesystem fallback)
        for trace_file in self.user_trace_dir.glob("*.json"):
            if trace_file.name == "relationships.jsonl":
                continue

            with open(trace_file, 'r') as f:
                data = json.load(f)
                data['trace_type'] = TraceType(data['trace_type'])
                trace = MyceliumTrace(**data)

                # Apply filters
                if trace_type and trace.trace_type != trace_type:
                    continue

                if tags and not any(tag in trace.tags for tag in tags):
                    continue

                if query:
                    query_lower = query.lower()
                    if query_lower not in trace.title.lower() and query_lower not in trace.content.lower():
                        continue

                traces.append(trace)

        # Sort by most recent
        traces.sort(key=lambda t: t.updated_at, reverse=True)

        return traces[:limit]

    def get_related_traces(self, trace_id: str, rel_type: RelationType = None) -> List[Tuple[MyceliumTrace, str]]:
        """
        Get traces related to a given trace.

        Args:
            trace_id: Source trace ID
            rel_type: Optional filter by relationship type

        Returns:
            List of (trace, relationship_type) tuples
        """
        if not self.neo4j_available:
            # Fallback: read relationships from Bundle/
            return self._get_related_traces_from_bundle(trace_id, rel_type)

        with self.driver.session() as session:
            query = """
                MATCH (from:Trace {trace_id: $trace_id, user_id: $user_id})-[r]->(to:Trace)
                RETURN to, type(r) as rel_type
            """

            if rel_type:
                query += " WHERE type(r) = $rel_type"

            result = session.run(query, {
                'trace_id': trace_id,
                'user_id': self.user_id,
                'rel_type': rel_type.value if rel_type else None
            })

            related = []
            for record in result:
                node = record['to']
                trace = MyceliumTrace(
                    trace_id=node['trace_id'],
                    user_id=node['user_id'],
                    trace_type=TraceType(node['trace_type']),
                    title=node['title'],
                    content=node['content'],
                    created_at=node['created_at'],
                    updated_at=node['updated_at'],
                    conversation_id=node.get('conversation_id'),
                    tags=node.get('tags', []),
                    properties=dict(node)
                )
                related.append((trace, record['rel_type']))

            return related

    def _get_related_traces_from_bundle(self, trace_id: str, rel_type: RelationType = None) -> List[Tuple[MyceliumTrace, str]]:
        """Fallback: get related traces from Bundle/ filesystem."""
        rel_file = self.user_trace_dir / "relationships.jsonl"
        if not rel_file.exists():
            return []

        related = []
        with open(rel_file, 'r') as f:
            for line in f:
                rel_data = json.load(line)
                if rel_data['from_trace_id'] == trace_id:
                    if rel_type and rel_data['rel_type'] != rel_type.value:
                        continue

                    # Load the related trace
                    related_trace = self.get_trace(rel_data['to_trace_id'])
                    if related_trace:
                        related.append((related_trace, rel_data['rel_type']))

        return related

    def get_user_stats(self) -> Dict:
        """Get statistics about user's traces."""
        traces = list(self.user_trace_dir.glob("*.json"))
        traces = [t for t in traces if t.name != "relationships.jsonl"]

        stats = {
            'user_id': self.user_id,
            'total_traces': len(traces),
            'by_type': {},
            'total_relationships': 0,
            'recent_traces': []
        }

        # Count by type
        for trace_file in traces:
            with open(trace_file, 'r') as f:
                data = json.load(f)
                trace_type = data['trace_type']
                stats['by_type'][trace_type] = stats['by_type'].get(trace_type, 0) + 1

        # Count relationships
        rel_file = self.user_trace_dir / "relationships.jsonl"
        if rel_file.exists():
            with open(rel_file, 'r') as f:
                stats['total_relationships'] = sum(1 for _ in f)

        # Get recent traces
        all_traces = []
        for trace_file in traces:
            with open(trace_file, 'r') as f:
                data = json.load(f)
                all_traces.append(data)

        all_traces.sort(key=lambda t: t['updated_at'], reverse=True)
        stats['recent_traces'] = [
            {'title': t['title'], 'type': t['trace_type'], 'created_at': t['created_at']}
            for t in all_traces[:5]
        ]

        return stats

    def close(self):
        """Close Neo4j connection."""
        if self.driver:
            self.driver.close()


# Convenience functions
def create_mycelium_tracer(user_id: str = "user0") -> MyceliumTracer:
    """Create mycelium tracer for user."""
    return MyceliumTracer(user_id=user_id)


if __name__ == "__main__":
    # Test mycelium tracer
    print("Testing Mycelium Tracer...")

    tracer = MyceliumTracer(user_id="user0")

    # Create some test traces
    note = tracer.create_trace(
        TraceType.NOTE,
        "Team burnout observation",
        "Noticed increasing burnout signals in team standup. Members reporting exhaustion.",
        tags=["burnout", "team_health"]
    )

    insight = tracer.create_trace(
        TraceType.INSIGHT,
        "Burnout correlates with lack of agency",
        "Pattern: teams with highest burnout also have least decision-making autonomy.",
        tags=["burnout", "agency", "pattern"]
    )

    project = tracer.create_trace(
        TraceType.PROJECT,
        "Restore team autonomy initiative",
        "Multi-month project to redistribute decision-making power to team level.",
        tags=["autonomy", "initiative"]
    )

    # Create relationships
    tracer.create_relationship(
        note.trace_id,
        insight.trace_id,
        RelationType.DERIVES_FROM
    )

    tracer.create_relationship(
        insight.trace_id,
        project.trace_id,
        RelationType.CONTRIBUTES_TO
    )

    # Test retrieval
    stats = tracer.get_user_stats()
    print(f"\n✅ Created {stats['total_traces']} traces")
    print(f"✅ Created {stats['total_relationships']} relationships")
    print(f"✅ Mycelium network growing for {stats['user_id']}")

    tracer.close()
