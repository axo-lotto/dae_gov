#!/usr/bin/env python3
"""
Superject State Structures
===========================

Dataclasses for per-user superject state persistence - the accumulated
felt-state trajectory that becomes the companion's personality.

Whiteheadian foundation:
- Superject = "satisfied" actual occasion as datum for future
- User's accumulated occasions = their companion's character
- Personality emerges from trajectory, not programmed

Date: November 14, 2025
Phase: 1 - Foundation
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime
import json


@dataclass
class FeltStateSnapshot:
    """
    Single conversation turn's felt state - COMPLETE TSK CAPTURE.

    Captures the 57D organ signature + context at a moment in time.
    This is the organism's "subjective form" for this occasion.

    TSK Compliance: November 14, 2025
    Now captures ALL felt-state transformation data for pattern learning.
    """
    timestamp: str

    # Organism state (57D semantic space)
    organ_signature: List[float]  # 57D vector (11 organs × ~5 atoms each)
    active_organs: List[str]
    dominant_nexuses: List[str]

    # Zone/polyvagal (SELF matrix)
    zone: int  # 1-5
    zone_name: str
    polyvagal_state: str  # "ventral_vagal", "sympathetic", "dorsal_vagal", "mixed"
    self_distance: float  # IFS exile distance

    # V0 convergence
    v0_energy: float
    satisfaction: float
    convergence_cycles: int

    # Transduction
    transduction_mechanism: Optional[str]
    transduction_pathway: Optional[str]

    # User satisfaction (feedback - set later)
    user_satisfaction: Optional[float] = None  # 0-1, learned from continuation
    user_continued: Optional[bool] = None  # Did they keep talking?

    # 🌀 TSK COMPLIANCE ADDITIONS (November 14, 2025)
    # Complete felt-state transformation tracking

    # Crisis/urgency detection
    ndam_urgency: float = 0.0  # NDAM crisis level (0-1)

    # Meta-atom activation (bridge atoms)
    meta_atoms_activated: Dict[str, float] = field(default_factory=dict)  # {atom_name: activation}

    # Emission generation
    emission_confidence: float = 0.0  # Final emission confidence (0-1)
    emission_strategy: Optional[str] = None  # "direct", "fusion", "hebbian", "felt_guided_llm"
    emission_emoji: List[str] = field(default_factory=list)  # Emojis used in emission

    # Kairos detection (opportune moments)
    kairos_detected: bool = False  # Was V0 in Kairos window?
    kairos_cycle_index: Optional[int] = None  # Which cycle detected Kairos

    # 🌀 WAVE TRAINING METADATA (November 15, 2025 - DAE 3.0 Legacy Integration)
    # Appetitive phase tracking for satisfaction variance learning
    wave_training_enabled: bool = True  # Whether wave training was active
    appetitive_phase: Optional[str] = None  # "EXPANSIVE", "NAVIGATION", "CONCRESCENCE"
    satisfaction_raw: Optional[float] = None  # Pre-modulation satisfaction
    satisfaction_modulated: Optional[float] = None  # Post-modulation satisfaction
    satisfaction_variance: float = 0.0  # Temporal variance across cycles


@dataclass
class TransformationPattern:
    """
    Learned pattern of felt-state transformation.

    Example: "User goes from anxious (Zone 3, sympathetic) to grounded (Zone 1, ventral)
    when we use PRESENCE + somatic_wisdom nexus with moderate length responses and no humor."

    This is learned transductive intelligence - knowing what pathways work for THIS user.
    """
    pattern_id: str  # "anxious_to_grounded"

    # From state
    from_zone: int
    from_polyvagal: str
    from_v0_range: tuple  # (min, max)

    # To state
    to_zone: int
    to_polyvagal: str
    to_v0_range: tuple

    # What worked (learned from successful transitions)
    successful_organs: List[str]
    successful_nexuses: List[str]
    successful_transduction: Optional[str]

    # Style preferences for this transition
    humor_safe: bool
    humor_threshold: float  # Only if user_humor_tolerance > this
    humor_style: Optional[str]  # "dry_wit", "absurdist", "puns", "self_deprecating"
    tone: str  # "gentle", "playful", "direct", "reflective"
    preferred_length: str  # "minimal", "moderate", "comprehensive"

    # Learning metrics
    frequency: int  # How many times seen
    success_rate: float  # 0-1, based on user_satisfaction
    avg_satisfaction_gain: float  # How much satisfaction improved

    # Timestamps
    first_seen: str
    last_seen: str
    last_updated: str


@dataclass
class InsideJoke:
    """
    Relationship-building callback reference.

    These emerge organically from successful humor + user engagement.
    Example: "mushroom philosophy" mentioned in conv 5, laughed at, referenced 7 more times.
    """
    joke_id: str
    topic: str  # "mushroom philosophy", "organ bickering", etc.
    text_snippet: str  # Original joke text

    # Emergence
    first_mentioned: str  # ISO timestamp
    conversation_id: str
    context_zone: int
    user_response: str  # "positive", "neutral", "negative"

    # Evolution
    times_referenced: int
    last_referenced: str
    still_landing: bool  # False if user stopped responding positively

    # Metadata
    humor_category: str  # From humor_templates.json
    organic: bool  # True if spontaneous, False if from template


@dataclass
class HecklingTrajectory:
    """
    Tracks heckling interactions over time - Phase 1.5H Nov 14, 2025.

    Learning user's provocat style, when banter is safe, ground state resilience.
    """
    # Heckling statistics
    total_heckling_attempts: int = 0
    successful_deflections: int = 0  # Held ground, engaged appropriately
    failed_deflections: int = 0  # Collapsed or over-engaged

    # Provocation style learning
    provocation_types: Dict[str, int] = field(default_factory=dict)  # {"sarcastic": 5, "absurdist": 2}
    favorite_provocation: Optional[str] = None  # Most frequent type

    # Banter readiness
    banter_unlocked: bool = False  # Unlocks after 10+ successful deflections
    inside_jokes_from_heckling: List[str] = field(default_factory=list)  # Callbacks to heckling moments

    # Ground state resilience
    zone_held_under_provocation: List[int] = field(default_factory=list)  # Which zones maintained
    polyvagal_resilience_score: float = 0.0  # 0-1, stays ventral under provocation

    # Crisis vs heckling accuracy
    false_positive_crises: int = 0  # Treated heckling as crisis (safe error)
    false_negative_crises: int = 0  # Treated crisis as heckling (UNSAFE - track carefully)

    # Learning trajectory
    first_heckling_detected: Optional[str] = None  # ISO timestamp
    last_heckling_detected: Optional[str] = None


@dataclass
class HumorEvolution:
    """
    Tracks humor learning trajectory over time.

    Starts at 0 (no humor), calibrates through experimentation,
    eventually unlocks as safe relationship-building tool.

    Phase 1.5H Integration: Heckling deflection → humor unlocking pathway.
    """
    # Current calibration
    current_tolerance: float  # 0-1, dynamically adjusted
    humor_unlocked: bool  # False until proven safe (5+ successful attempts)

    # Attempts tracking
    total_attempts: int
    successful_attempts: int  # user_satisfaction > 0.7
    failed_attempts: int  # user_satisfaction < 0.5 or disengagement

    # What works
    successful_types: Dict[str, int]  # {"dry_wit": 5, "puns": 2}
    failed_types: Dict[str, int]  # {"absurdist": 3}

    # Inside joke library (relationship memory)
    inside_jokes: List[InsideJoke]

    # Gating conditions (learned)
    safe_zones: List[int]  # [1, 2] (never Zone 4/5)
    safe_polyvagal: List[str]  # ["ventral_vagal", "mixed"]
    unsafe_contexts: List[str]  # ["after_crying", "zone5_collapse"]

    # Calibration history
    tolerance_history: List[Dict[str, Any]]  # Track adjustments over time
    last_attempt: Optional[str]  # ISO timestamp
    last_success: Optional[str]

    # 🌀 Phase 1.5H: Heckling integration (Nov 14, 2025)
    unlocked_via_heckling: bool = False  # True if humor unlocked through successful heckling deflection


@dataclass
class EnhancedUserProfile:
    """
    Complete per-user superject state.

    This IS the companion's personality for this user - not programmed,
    but emerged from accumulated felt-state trajectory.
    """
    # Identity
    user_id: str
    created_at: str
    last_active: str

    # Basic preferences (baseline, before learning)
    response_length_preference: str = "moderate"
    humor_tolerance: float = 0.5  # Starting point, will adapt
    small_talk_openness: float = 0.5
    llm_usage_consent: bool = False

    # Relationship metrics
    total_conversations: int = 0
    total_turns: int = 0
    rapport_score: float = 0.0  # 0-1, accumulated over time
    trust_indicators: List[str] = field(default_factory=list)

    # === SUPERJECT TRAJECTORY (Core of companion personality) ===

    # 1. Felt-state accumulation (57D organ signatures over time)
    felt_trajectory: List[FeltStateSnapshot] = field(default_factory=list)

    # 2. Learned transformation patterns (transductive intelligence)
    transformation_patterns: Dict[str, TransformationPattern] = field(default_factory=dict)

    # 3. Humor evolution (relationship-building)
    humor_evolution: HumorEvolution = None

    # 3.5. Heckling trajectory (Phase 1.5H - Nov 14, 2025)
    heckling_trajectory: HecklingTrajectory = None

    # 4. Tone preferences per zone (learned from satisfaction)
    tone_preferences: Dict[int, str] = field(default_factory=dict)  # {zone: tone}

    # 5. Inside jokes & recurring themes (relationship memory)
    inside_jokes: List[InsideJoke] = field(default_factory=list)
    recurring_themes: Dict[str, int] = field(default_factory=dict)  # {theme: count}

    # 6. Organic family affinity (Phase 5 integration)
    family_affinities: Dict[str, float] = field(default_factory=dict)  # {family_id: affinity}

    # 7. Template success (PersonaLayer learning)
    template_success_rates: Dict[str, float] = field(default_factory=dict)
    favorite_templates: Dict[str, List[str]] = field(default_factory=dict)

    # === AGENT CAPABILITIES (Unlocked progressively) ===

    # Unlocked at conversation thresholds
    can_reference_past: bool = False  # Unlocked at 10 conversations
    can_use_humor: bool = False  # Unlocked when humor_evolution.humor_unlocked
    can_be_playful: bool = False  # Unlocked at 20 conversations + high rapport
    can_give_advice: bool = False  # Unlocked at 30 conversations + high trust
    can_challenge_gently: bool = False  # Unlocked at 50 conversations + very high rapport

    # Learning metadata
    last_mini_epoch: Optional[str] = None  # ISO timestamp of last pattern learning
    learning_velocity: float = 0.0  # How fast patterns are being learned

    # 🌀 Phase 1.6: Salience pattern tracking metadata (Nov 14, 2025)
    metadata: Dict[str, Any] = field(default_factory=dict)  # Flexible metadata for tracking patterns

    # 🌀 Phase 1.8: Entity extraction & memory storage (Nov 14, 2025)
    # Extracted entities from conversation (names, relationships, facts, preferences)
    entities: Dict[str, Any] = field(default_factory=dict)
    entity_history: List[Dict[str, Any]] = field(default_factory=list)  # Timeline of extractions

    def __post_init__(self):
        """Initialize nested structures."""
        if self.humor_evolution is None:
            self.humor_evolution = HumorEvolution(
                current_tolerance=self.humor_tolerance,
                humor_unlocked=False,
                total_attempts=0,
                successful_attempts=0,
                failed_attempts=0,
                successful_types={},
                failed_types={},
                inside_jokes=[],
                safe_zones=[1, 2],
                safe_polyvagal=["ventral_vagal"],
                unsafe_contexts=["zone5_collapse", "zone4_shadow"],
                tolerance_history=[],
                last_attempt=None,
                last_success=None
            )

        # 🌀 Phase 1.5H: Initialize heckling trajectory (Nov 14, 2025)
        if self.heckling_trajectory is None:
            self.heckling_trajectory = HecklingTrajectory()

    def to_dict(self) -> Dict:
        """Convert to dict for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'EnhancedUserProfile':
        """Load from dict (JSON deserialization)."""

        # Convert nested structures
        if 'felt_trajectory' in data and data['felt_trajectory']:
            data['felt_trajectory'] = [
                FeltStateSnapshot(**snapshot) for snapshot in data['felt_trajectory']
            ]

        if 'transformation_patterns' in data and data['transformation_patterns']:
            data['transformation_patterns'] = {
                k: TransformationPattern(**v) if isinstance(v, dict) else v
                for k, v in data['transformation_patterns'].items()
            }

        if 'humor_evolution' in data and data['humor_evolution']:
            he_data = data['humor_evolution']
            # Check if already a HumorEvolution object
            if isinstance(he_data, HumorEvolution):
                data['humor_evolution'] = he_data
            elif isinstance(he_data, dict):
                if 'inside_jokes' in he_data:
                    he_data['inside_jokes'] = [
                        InsideJoke(**ij) if isinstance(ij, dict) else ij
                        for ij in he_data['inside_jokes']
                    ]
                data['humor_evolution'] = HumorEvolution(**he_data)

        if 'inside_jokes' in data and data['inside_jokes']:
            data['inside_jokes'] = [
                InsideJoke(**ij) if isinstance(ij, dict) else ij
                for ij in data['inside_jokes']
            ]

        return cls(**data)

    def get_recent_trajectory(self, n: int = 10) -> List[FeltStateSnapshot]:
        """Get last N felt states."""
        return self.felt_trajectory[-n:]

    def get_dominant_zones(self, n: int = 20) -> Dict[int, int]:
        """Get zone frequency from recent history."""
        recent = self.get_recent_trajectory(n)
        zones = {}
        for snapshot in recent:
            zones[snapshot.zone] = zones.get(snapshot.zone, 0) + 1
        return zones

    def get_polyvagal_trajectory(self, n: int = 20) -> List[str]:
        """Get recent polyvagal states."""
        recent = self.get_recent_trajectory(n)
        return [s.polyvagal_state for s in recent]

    def calculate_rapport_score(self) -> float:
        """
        Calculate rapport from multiple signals.

        High rapport = long conversations, high satisfaction, humor landing,
        inside jokes accumulating, recurring engagement.
        """
        if not self.felt_trajectory:
            return 0.0

        signals = []

        # Signal 1: Average satisfaction
        recent_sats = [s.user_satisfaction for s in self.felt_trajectory[-20:]
                      if s.user_satisfaction is not None]
        if recent_sats:
            signals.append(sum(recent_sats) / len(recent_sats))

        # Signal 2: Conversation continuity
        if self.total_turns > 20:
            signals.append(min(1.0, self.total_turns / 100))

        # Signal 3: Humor success
        if self.humor_evolution.humor_unlocked:
            signals.append(0.8)

        # Signal 4: Inside jokes
        if len(self.inside_jokes) > 3:
            signals.append(0.9)

        # Signal 5: Recurring themes (user keeps coming back)
        if len(self.recurring_themes) > 5:
            signals.append(0.7)

        return sum(signals) / len(signals) if signals else 0.0

    def unlock_capabilities(self):
        """Unlock agent capabilities based on relationship progression."""
        self.rapport_score = self.calculate_rapport_score()

        if self.total_conversations >= 10:
            self.can_reference_past = True

        if self.humor_evolution.humor_unlocked:
            self.can_use_humor = True

        if self.total_conversations >= 20 and self.rapport_score > 0.6:
            self.can_be_playful = True

        if self.total_conversations >= 30 and self.rapport_score > 0.7:
            self.can_give_advice = True

        if self.total_conversations >= 50 and self.rapport_score > 0.8:
            self.can_challenge_gently = True

    # 🌀 Phase 1.8: Entity extraction utility methods (Nov 14, 2025)

    def store_entities(self, new_entities: Dict[str, Any]):
        """
        Store newly extracted entities, merging with existing.

        Args:
            new_entities: Dict from EntityExtractor.extract()
        """
        from datetime import datetime

        # Merge with existing entities
        if 'user_name' in new_entities:
            self.entities['user_name'] = new_entities['user_name']

        if 'user_role' in new_entities:
            self.entities['user_role'] = new_entities['user_role']

        # Merge mentioned names (deduplicate)
        if 'mentioned_names' in new_entities:
            existing_names = self.entities.get('mentioned_names', [])
            for name in new_entities['mentioned_names']:
                if name not in existing_names:
                    existing_names.append(name)
            self.entities['mentioned_names'] = existing_names

        # Merge relationships
        if 'relationships' in new_entities:
            existing_rels = self.entities.get('relationships', [])
            for rel in new_entities['relationships']:
                if rel not in existing_rels:
                    existing_rels.append(rel)
            self.entities['relationships'] = existing_rels

        # Store relationship count
        if 'relationship_count' in new_entities:
            self.entities['relationship_count'] = new_entities['relationship_count']

        # Store relationship context
        if 'relationship_context' in new_entities:
            self.entities['relationship_context'] = new_entities['relationship_context']

        # Store related person
        if 'related_person' in new_entities:
            self.entities['related_person'] = new_entities['related_person']

        # Merge facts
        if 'facts' in new_entities:
            existing_facts = self.entities.get('facts', [])
            for fact in new_entities['facts']:
                existing_facts.append(fact)
            self.entities['facts'] = existing_facts

        # 🌀 Nov 14, 2025: Add support for family_members, friends, preferences
        # Merge family_members (deduplicate by name)
        if 'family_members' in new_entities:
            existing_family = self.entities.get('family_members', [])
            existing_names = {m.get('name') for m in existing_family if isinstance(m, dict)}
            for member in new_entities['family_members']:
                if isinstance(member, dict) and member.get('name') not in existing_names:
                    existing_family.append(member)
                    existing_names.add(member.get('name'))
            self.entities['family_members'] = existing_family

        # Merge friends (deduplicate by name)
        if 'friends' in new_entities:
            existing_friends = self.entities.get('friends', [])
            existing_names = {f.get('name') for f in existing_friends if isinstance(f, dict)}
            for friend in new_entities['friends']:
                if isinstance(friend, dict) and friend.get('name') not in existing_names:
                    existing_friends.append(friend)
                    existing_names.add(friend.get('name'))
            self.entities['friends'] = existing_friends

        # Merge preferences (update dict)
        if 'preferences' in new_entities:
            existing_prefs = self.entities.get('preferences', {})
            if isinstance(new_entities['preferences'], dict):
                existing_prefs.update(new_entities['preferences'])
            self.entities['preferences'] = existing_prefs

        # Add to history
        self.entity_history.append({
            'timestamp': datetime.now().isoformat(),
            'entities': new_entities
        })

    def get_entity_context_string(self) -> str:
        """
        Get formatted string of known entities for LLM context.

        🌀 Nov 14, 2025: Supports open-ended memory format (not hardcoded types).

        Returns:
            Formatted string with known information
        """
        if not self.entities:
            return ""

        lines = []

        # User name (if known)
        if 'user_name' in self.entities:
            lines.append(f"- Name: {self.entities['user_name']}")

        # 🌀 Nov 14, 2025: Open-ended memories (natural evolution)
        if 'memories' in self.entities:
            memories = self.entities['memories']

            # Group by type for readable context
            by_type = {}
            for mem in memories:
                mem_type = mem.get('type', 'fact')
                if mem_type not in by_type:
                    by_type[mem_type] = []
                by_type[mem_type].append(mem.get('value', ''))

            # Format by category
            for mem_type, values in by_type.items():
                if values:
                    values_str = ", ".join(values[:5])  # Max 5 per type to avoid context bloat
                    lines.append(f"- {mem_type.capitalize()}: {values_str}")

        # Legacy support for old entity types
        if 'user_role' in self.entities:
            lines.append(f"- Role: {self.entities['user_role']}")

        if 'relationships' in self.entities:
            rels = ', '.join(self.entities['relationships'])
            lines.append(f"- Relationships: {rels}")

        if 'relationship_count' in self.entities:
            count = self.entities['relationship_count']
            context = self.entities.get('relationship_context', 'family')
            lines.append(f"- {context.capitalize()}: {count} members")

        if 'mentioned_names' in self.entities:
            names = ', '.join(self.entities['mentioned_names'])
            lines.append(f"- Mentioned names: {names}")

        if 'related_person' in self.entities:
            rp = self.entities['related_person']
            lines.append(f"- {rp['relationship'].capitalize()}: {rp['name']}")

        if 'facts' in self.entities and len(self.entities['facts']) > 0:
            for fact in self.entities['facts'][:5]:  # Max 5 facts
                if isinstance(fact, dict):
                    lines.append(f"- {fact.get('type', 'Fact')}: {fact.get('value', '')}")
                else:
                    lines.append(f"- Fact: {fact}")

        # 🌀 Nov 14, 2025: Add family_members, friends, preferences to context
        if 'family_members' in self.entities and len(self.entities['family_members']) > 0:
            family_list = []
            for member in self.entities['family_members']:
                if isinstance(member, dict):
                    name = member.get('name', 'Unknown')
                    relation = member.get('relation', '')
                    if relation:
                        family_list.append(f"{name} ({relation})")
                    else:
                        family_list.append(name)
            if family_list:
                lines.append(f"- Family: {', '.join(family_list)}")

        if 'friends' in self.entities and len(self.entities['friends']) > 0:
            friend_names = []
            for friend in self.entities['friends']:
                if isinstance(friend, dict):
                    friend_names.append(friend.get('name', 'Unknown'))
            if friend_names:
                lines.append(f"- Friends: {', '.join(friend_names)}")

        if 'preferences' in self.entities and len(self.entities['preferences']) > 0:
            prefs = self.entities['preferences']
            pref_list = [f"{k}: {v}" for k, v in prefs.items()]
            if pref_list:
                lines.append(f"- Preferences: {', '.join(pref_list)}")

        if not lines:
            return ""

        # 🌀 Nov 14, 2025: More personal framing for open-ended memories
        return "Known about this person:\n" + "\n".join(lines)

    def has_entity_memory(self) -> bool:
        """Check if any entities have been extracted."""
        return len(self.entities) > 0


def create_default_profile(user_id: str) -> EnhancedUserProfile:
    """Create new user profile with defaults."""
    now = datetime.now().isoformat()
    return EnhancedUserProfile(
        user_id=user_id,
        created_at=now,
        last_active=now
    )


def save_profile(profile: EnhancedUserProfile, filepath: str):
    """Save profile to JSON."""
    with open(filepath, 'w') as f:
        json.dump(profile.to_dict(), f, indent=2)


def load_profile(filepath: str) -> EnhancedUserProfile:
    """Load profile from JSON."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return EnhancedUserProfile.from_dict(data)
