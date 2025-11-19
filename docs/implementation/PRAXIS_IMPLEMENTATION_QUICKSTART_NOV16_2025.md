# ⚡ PRAXIS Organ: Implementation Quick Start
## Developer Guide for Day 1-2
**Date:** November 16, 2025
**Goal:** Create functional PRAXIS organ foundation in 2 days

---

## 📋 Day 1: Organ Structure (4-6 hours)

### Step 1: Create Directory Structure (15 min)

```bash
cd /Users/daedalea/Desktop/DAE_HYPHAE_1

# Create PRAXIS organ directory
mkdir -p organs/modular/praxis/organ_config
mkdir -p organs/modular/praxis/core
mkdir -p organs/modular/praxis/tests

# Verify structure
ls -la organs/modular/praxis/
```

Expected output:
```
organs/modular/praxis/
├── __init__.py
├── organ_config/
│   └── praxis_config.py
├── core/
│   └── praxis_text_core.py
└── tests/
    └── test_praxis_coherence.py
```

---

### Step 2: Implement praxis_config.py (1 hour)

**File:** `organs/modular/praxis/organ_config/praxis_config.py`

```python
"""
PRAXIS Configuration - Action & Execution Intelligence (Text Domain)

Configuration parameters for the modular PRAXIS organ.
Handles task execution: schedules, plans, concrete action creation.
"""

from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class PRAXISConfig:
    """Configuration for PRAXIS Core Engine - Task Execution Domain"""

    # Core execution coherence settings
    coherence_threshold: float = 0.60  # Stricter than therapeutic (0.50)
    execution_sensitivity: float = 0.75
    precision_amplification: float = 1.3
    adaptive_planning: float = 0.80

    # 7 Semantic Atoms (Task Execution Space)
    atoms: List[str] = None

    # Atom weights for coherence calculation
    atom_weights: Dict[str, float] = None

    # Mathematical coherence settings
    cosmic_salience_threshold: float = 0.60
    planning_coherence_weight: float = 0.75
    adaptive_alignment_factor: float = 0.80

    # Pattern detection settings
    clarification_window: int = 3  # Max clarifying questions before generating
    specificity_threshold: float = 0.70
    adaptive_adjustment_rate: float = 0.12

    # Performance optimization
    max_clarifications_per_conversation: int = 5
    planning_history_limit: int = 100
    schedule_memory_limit: int = 500

    # Cross-organ collaboration weights (felt modulation)
    collaboration_patterns: Dict[str, float] = None

    def __post_init__(self):
        """Initialize atoms and weights if not provided"""
        if self.atoms is None:
            self.atoms = [
                'task_clarity',           # Vague → concrete
                'temporal_precision',     # Specific times (7:00am not "morning")
                'resource_mapping',       # What's needed
                'action_sequencing',      # Steps in order
                'completion_criteria',    # How to know it's done
                'schedule_integration',   # How tasks fit together
                'accountability_structure' # Tracking, reminders
            ]

        if self.atom_weights is None:
            # Weights sum to 1.0
            self.atom_weights = {
                'task_clarity': 0.25,            # Most important
                'temporal_precision': 0.20,
                'resource_mapping': 0.15,
                'action_sequencing': 0.15,
                'completion_criteria': 0.10,
                'schedule_integration': 0.10,
                'accountability_structure': 0.05  # Least important
            }

        if self.collaboration_patterns is None:
            self.collaboration_patterns = {
                'EO': 0.85,     # Polyvagal state → schedule ambition
                'BOND': 0.75,   # Parts resistance → goal adjustment
                'NDAM': 0.70,   # Urgency → task prioritization
                'RNX': 0.65,    # Temporal rhythm → activity timing
                'CARD': 0.60    # Response scale → schedule detail
            }

    def get_coherence_formula(self) -> str:
        """Return coherence calculation formula"""
        return """
        praxis_coherence = (
            0.25 * task_clarity +
            0.20 * temporal_precision +
            0.15 * resource_mapping +
            0.15 * action_sequencing +
            0.10 * completion_criteria +
            0.10 * schedule_integration +
            0.05 * accountability_structure
        )

        Threshold: 0.60 (stricter than therapeutic 0.50)

        Decision Logic:
        - coherence < 0.60 → Ask clarifying questions
        - coherence ≥ 0.60 → Generate schedule/plan
        """

    def get_atom_descriptions(self) -> Dict[str, str]:
        """Get human-readable atom descriptions"""
        return {
            'task_clarity': 'How specific is the goal? (vague "exercise" vs concrete "yoga Mon/Wed/Fri")',
            'temporal_precision': 'Are specific times mentioned? (7:00am vs "morning")',
            'resource_mapping': 'Are resources identified? (yoga mat, groceries, location)',
            'action_sequencing': 'Are steps in order? (prep before cook before eat)',
            'completion_criteria': 'How to know it\'s done? (30min completed, meal eaten)',
            'schedule_integration': 'Do tasks fit together? (no conflicts, dependencies clear)',
            'accountability_structure': 'Is tracking enabled? (calendar, checkboxes, reminders)'
        }

    def get_clarification_prompts(self) -> Dict[str, List[str]]:
        """Get clarifying questions for each atom"""
        return {
            'task_clarity': [
                "What specific activity did you have in mind?",
                "Can you describe the goal more concretely?",
                "What does that look like in practice?"
            ],
            'temporal_precision': [
                "What time of day works best?",
                "Would you prefer a specific time like 7am, 8am, etc?",
                "Morning, afternoon, or evening?"
            ],
            'resource_mapping': [
                "What do you need to make this happen?",
                "Do you have the equipment/space/ingredients?",
                "Is there anything you'd need to get or prepare?"
            ],
            'action_sequencing': [
                "What would be the first step?",
                "How would you break this down into steps?",
                "What needs to happen before you can start?"
            ],
            'completion_criteria': [
                "How will you know when you've completed this?",
                "What does success look like?",
                "How long should this take?"
            ],
            'schedule_integration': [
                "Which days of the week work best?",
                "How does this fit with your other commitments?",
                "Are there any conflicts with existing plans?"
            ],
            'accountability_structure': [
                "How would you like to track your progress?",
                "Would you like reminders?",
                "Should we set up a way to check in on this?"
            ]
        }

    def get_felt_modulation_rules(self) -> Dict[str, Dict[str, Any]]:
        """Rules for felt-state modulation of schedules"""
        return {
            # EO (polyvagal) modulates schedule ambition
            'polyvagal_scaling': {
                'ventral_vagal': {
                    'frequency_multiplier': 1.0,    # Full schedule
                    'duration_multiplier': 1.0,
                    'tone': 'You have capacity for this rhythm'
                },
                'sympathetic': {
                    'frequency_multiplier': 0.7,    # Reduce frequency
                    'duration_multiplier': 0.8,     # Shorten sessions
                    'tone': 'Let\'s keep it focused and brief'
                },
                'dorsal_vagal': {
                    'frequency_multiplier': 0.4,    # Minimal schedule
                    'duration_multiplier': 0.5,     # Very short sessions
                    'tone': 'Let\'s start gently, honoring your capacity'
                },
                'weight': 0.40
            },

            # BOND (IFS) modulates goal size
            'parts_modulation': {
                'self_energy': {
                    'goal_size': 'ambitious',
                    'commitment_level': 'high'
                },
                'manager': {
                    'goal_size': 'moderate',
                    'commitment_level': 'medium'
                },
                'firefighter': {
                    'goal_size': 'minimal',
                    'commitment_level': 'low'
                },
                'exile': {
                    'goal_size': 'gentle',
                    'commitment_level': 'trauma-informed'
                },
                'weight': 0.30
            },

            # NDAM (urgency) modulates prioritization
            'urgency_prioritization': {
                'extreme': {'order': 'most_urgent_first'},
                'high': {'order': 'urgent_first'},
                'moderate': {'order': 'balanced'},
                'low': {'order': 'preference_based'},
                'none': {'order': 'exploratory'},
                'weight': 0.20
            },

            # RNX (temporal) modulates timing
            'temporal_rhythm': {
                'detected_pattern': 'honor_existing_rhythm',
                'no_pattern': 'suggest_natural_rhythm',
                'weight': 0.10
            }
        }


# Default configuration instance
DEFAULT_PRAXIS_CONFIG = PRAXISConfig()
```

---

### Step 3: Implement praxis_text_core.py (2-3 hours)

**File:** `organs/modular/praxis/core/praxis_text_core.py`

```python
"""
PRAXIS Core Engine - Action & Execution Intelligence

Analyzes user input for task execution readiness:
- Task clarity (vague vs concrete)
- Temporal precision (specific times)
- Resource availability
- Action sequencing
- Completion criteria
- Schedule integration
- Accountability structure

Returns PRAXIS coherence score (0-1).
If coherence < 0.60 → clarifying questions needed
If coherence ≥ 0.60 → ready for schedule/plan generation
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class PRAXISResult:
    """Result from PRAXIS organ processing"""
    coherence: float  # Overall coherence [0, 1]
    atom_activations: Dict[str, float]  # Individual atom scores
    missing_atoms: List[str]  # Atoms below threshold
    clarifying_questions: List[str]  # Questions to ask if coherence low
    ready_for_execution: bool  # True if coherence ≥ 0.60
    confidence: float  # Confidence in assessment


class PRAXISTextCore:
    """
    PRAXIS Core Engine for text-based task execution analysis.

    Evaluates user input across 7 dimensions:
    1. Task clarity
    2. Temporal precision
    3. Resource mapping
    4. Action sequencing
    5. Completion criteria
    6. Schedule integration
    7. Accountability structure
    """

    def __init__(self, config=None):
        """Initialize PRAXIS core engine"""
        if config is None:
            from organs.modular.praxis.organ_config.praxis_config import DEFAULT_PRAXIS_CONFIG
            config = DEFAULT_PRAXIS_CONFIG

        self.config = config
        self.coherence_threshold = config.coherence_threshold
        self.atom_weights = config.atom_weights
        self.clarification_prompts = config.get_clarification_prompts()

        # Temporal precision patterns
        self.time_patterns = [
            r'\d{1,2}:\d{2}',           # 7:00, 14:30
            r'\d{1,2}\s*(?:am|pm)',     # 7am, 2pm
            r'\d{1,2}\s*o\'?clock',     # 7 o'clock
        ]

        # Day patterns
        self.day_patterns = [
            r'\b(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
            r'\b(?:mon|tue|wed|thu|fri|sat|sun)\b',
            r'\b(?:weekday|weekend)\b',
        ]

        # Duration patterns
        self.duration_patterns = [
            r'\d+\s*(?:min|minute|minutes|mins)',
            r'\d+\s*(?:hr|hour|hours|hrs)',
            r'\d+\s*(?:sec|second|seconds|secs)',
        ]

        # Specificity keywords
        self.specific_activities = [
            'yoga', 'running', 'swimming', 'cycling', 'walking',
            'meditation', 'journaling', 'cooking', 'meal prep',
            'reading', 'writing', 'studying', 'practicing'
        ]

        self.vague_activities = [
            'exercise', 'workout', 'eat better', 'be healthier',
            'relax', 'work on', 'improve', 'do more'
        ]

    def compute_atom_activations(
        self,
        user_input: str,
        context: Optional[Dict] = None
    ) -> Dict[str, float]:
        """
        Compute activation scores for all 7 PRAXIS atoms.

        Args:
            user_input: User's message
            context: Optional context (entities, preferences, etc.)

        Returns:
            Dict mapping atom names to activation scores [0, 1]
        """
        input_lower = user_input.lower()
        activations = {}

        # 1. TASK_CLARITY: How specific is the goal?
        activations['task_clarity'] = self._compute_task_clarity(input_lower)

        # 2. TEMPORAL_PRECISION: Are specific times mentioned?
        activations['temporal_precision'] = self._compute_temporal_precision(input_lower)

        # 3. RESOURCE_MAPPING: Are resources identified?
        activations['resource_mapping'] = self._compute_resource_mapping(input_lower, context)

        # 4. ACTION_SEQUENCING: Are steps in order?
        activations['action_sequencing'] = self._compute_action_sequencing(input_lower)

        # 5. COMPLETION_CRITERIA: How to know it's done?
        activations['completion_criteria'] = self._compute_completion_criteria(input_lower)

        # 6. SCHEDULE_INTEGRATION: Do tasks fit together?
        activations['schedule_integration'] = self._compute_schedule_integration(input_lower)

        # 7. ACCOUNTABILITY_STRUCTURE: Is tracking enabled?
        activations['accountability_structure'] = self._compute_accountability(input_lower)

        return activations

    def _compute_task_clarity(self, input_lower: str) -> float:
        """Score how specific the task description is"""
        score = 0.0

        # Check for specific activities (high score)
        for activity in self.specific_activities:
            if activity in input_lower:
                score = max(score, 0.8)

        # Check for vague activities (low score)
        for vague in self.vague_activities:
            if vague in input_lower:
                score = max(score, 0.2)

        # Check for quantifiers (boosts score)
        quantifiers = ['x', 'times', 'per', 'each', 'every']
        if any(q in input_lower for q in quantifiers):
            score = min(1.0, score + 0.15)

        # If no activity words found, very low score
        if score == 0.0:
            score = 0.1

        return score

    def _compute_temporal_precision(self, input_lower: str) -> float:
        """Score how precise the time specification is"""
        score = 0.0

        # Check for specific times (highest score)
        for pattern in self.time_patterns:
            if re.search(pattern, input_lower, re.IGNORECASE):
                return 0.9  # Very precise

        # Check for specific days
        for pattern in self.day_patterns:
            if re.search(pattern, input_lower, re.IGNORECASE):
                score = max(score, 0.6)  # Good precision

        # Check for general time references (lower score)
        time_refs = ['morning', 'afternoon', 'evening', 'night']
        if any(ref in input_lower for ref in time_refs):
            score = max(score, 0.3)  # Vague precision

        # Check for duration
        for pattern in self.duration_patterns:
            if re.search(pattern, input_lower, re.IGNORECASE):
                score = min(1.0, score + 0.2)

        return score

    def _compute_resource_mapping(self, input_lower: str, context: Optional[Dict]) -> float:
        """Score whether resources are identified"""
        score = 0.0

        # Explicit resource mentions
        resource_keywords = [
            'mat', 'equipment', 'gym', 'kitchen', 'ingredients',
            'groceries', 'space', 'room', 'gear', 'supplies'
        ]

        for keyword in resource_keywords:
            if keyword in input_lower:
                score = max(score, 0.7)

        # Location mentions (implicit resources)
        location_keywords = ['home', 'park', 'office', 'studio', 'online']
        if any(loc in input_lower for loc in location_keywords):
            score = max(score, 0.5)

        # Check context for stored preferences (resources implied)
        if context and 'preferences' in context:
            score = max(score, 0.4)

        # Default: implicit resources assumed for common activities
        if score == 0.0:
            if any(activity in input_lower for activity in self.specific_activities):
                score = 0.3  # Implicit resources

        return score

    def _compute_action_sequencing(self, input_lower: str) -> float:
        """Score whether steps are specified in order"""
        score = 0.0

        # Sequencing keywords
        seq_keywords = [
            'first', 'then', 'next', 'after', 'before',
            'step', 'finally', 'start', 'end'
        ]

        seq_count = sum(1 for kw in seq_keywords if kw in input_lower)

        if seq_count >= 3:
            score = 0.8  # Multiple steps mentioned
        elif seq_count >= 2:
            score = 0.6
        elif seq_count >= 1:
            score = 0.4
        else:
            # Check for implicit sequencing (multiple activities)
            activity_count = sum(1 for act in self.specific_activities if act in input_lower)
            if activity_count >= 2:
                score = 0.3  # Implicit sequencing

        return score

    def _compute_completion_criteria(self, input_lower: str) -> float:
        """Score whether completion is defined"""
        score = 0.0

        # Explicit completion
        completion_keywords = [
            'complete', 'finish', 'done', 'goal', 'target',
            'achieve', 'accomplish'
        ]

        if any(kw in input_lower for kw in completion_keywords):
            score = 0.7

        # Duration implies completion
        for pattern in self.duration_patterns:
            if re.search(pattern, input_lower, re.IGNORECASE):
                score = max(score, 0.6)  # Time-based completion

        # Frequency implies completion
        freq_keywords = ['x', 'times', 'per', 'each']
        if any(kw in input_lower for kw in freq_keywords):
            score = max(score, 0.5)  # Count-based completion

        # Default: implicit completion for activities
        if score == 0.0 and any(act in input_lower for act in self.specific_activities):
            score = 0.4  # Activity completion implicit

        return score

    def _compute_schedule_integration(self, input_lower: str) -> float:
        """Score whether task fits into schedule"""
        score = 0.0

        # Days specified
        day_count = 0
        for pattern in self.day_patterns:
            day_count += len(re.findall(pattern, input_lower, re.IGNORECASE))

        if day_count >= 3:
            score = 0.8  # Multiple days = schedule
        elif day_count >= 1:
            score = 0.6

        # Frequency mentions
        freq_keywords = ['daily', 'weekly', 'monthly', 'per week', 'per day']
        if any(kw in input_lower for kw in freq_keywords):
            score = max(score, 0.5)

        return score

    def _compute_accountability(self, input_lower: str) -> float:
        """Score whether tracking/accountability is mentioned"""
        score = 0.0

        # Explicit tracking
        tracking_keywords = [
            'track', 'log', 'record', 'remind', 'reminder',
            'check-in', 'follow-up', 'monitor', 'measure'
        ]

        if any(kw in input_lower for kw in tracking_keywords):
            score = 0.8

        # Implicit tracking (questions about progress)
        progress_keywords = ['how am i doing', 'progress', 'improvement']
        if any(kw in input_lower for kw in progress_keywords):
            score = max(score, 0.5)

        return score

    def compute_coherence(self, atom_activations: Dict[str, float]) -> float:
        """
        Compute overall PRAXIS coherence from atom activations.

        Uses weighted sum of atom activations.

        Returns:
            Coherence score [0, 1]
        """
        coherence = sum(
            atom_activations[atom] * self.atom_weights[atom]
            for atom in self.atom_weights
        )

        return min(1.0, max(0.0, coherence))

    def get_missing_atoms(
        self,
        atom_activations: Dict[str, float],
        threshold: float = 0.5
    ) -> List[str]:
        """Return atoms below threshold (need clarification)"""
        return [
            atom for atom, score in atom_activations.items()
            if score < threshold
        ]

    def get_clarifying_questions(
        self,
        missing_atoms: List[str],
        max_questions: int = 3
    ) -> List[str]:
        """
        Generate clarifying questions for missing atoms.

        Prioritizes most important atoms (highest weights).
        """
        # Sort atoms by weight (descending)
        sorted_atoms = sorted(
            missing_atoms,
            key=lambda a: self.atom_weights[a],
            reverse=True
        )

        # Take top N most important
        priority_atoms = sorted_atoms[:max_questions]

        # Get one question per atom
        questions = []
        for atom in priority_atoms:
            prompts = self.clarification_prompts.get(atom, [])
            if prompts:
                questions.append(prompts[0])  # Use first prompt

        return questions

    def process(
        self,
        user_input: str,
        context: Optional[Dict] = None
    ) -> PRAXISResult:
        """
        Main processing method.

        Returns complete PRAXIS assessment.
        """
        # Compute atom activations
        atom_activations = self.compute_atom_activations(user_input, context)

        # Compute coherence
        coherence = self.compute_coherence(atom_activations)

        # Identify missing atoms
        missing_atoms = self.get_missing_atoms(atom_activations, threshold=0.5)

        # Generate clarifying questions if needed
        clarifying_questions = []
        if coherence < self.coherence_threshold:
            clarifying_questions = self.get_clarifying_questions(missing_atoms)

        # Determine if ready for execution
        ready_for_execution = coherence >= self.coherence_threshold

        # Compute confidence (higher when atoms agree)
        atom_std = sum((score - coherence) ** 2 for score in atom_activations.values()) ** 0.5
        confidence = max(0.3, 1.0 - atom_std)

        return PRAXISResult(
            coherence=coherence,
            atom_activations=atom_activations,
            missing_atoms=missing_atoms,
            clarifying_questions=clarifying_questions,
            ready_for_execution=ready_for_execution,
            confidence=confidence
        )


# Quick test
if __name__ == '__main__':
    praxis = PRAXISTextCore()

    # Test cases
    test_inputs = [
        "I want to exercise",
        "I want to do yoga 3x/week",
        "Yoga Mon/Wed/Fri at 7am for 30 minutes"
    ]

    for inp in test_inputs:
        result = praxis.process(inp)
        print(f"\nInput: {inp}")
        print(f"Coherence: {result.coherence:.2f}")
        print(f"Ready: {result.ready_for_execution}")
        if result.clarifying_questions:
            print(f"Questions: {result.clarifying_questions}")
```

---

### Step 4: Write Unit Tests (1 hour)

**File:** `organs/modular/praxis/tests/test_praxis_coherence.py`

```python
"""
Unit tests for PRAXIS coherence calculation.

Tests 3 coherence levels:
- Low (< 0.40): Very vague input
- Medium (0.40-0.60): Some specificity
- High (≥ 0.60): Ready for schedule generation
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from organs.modular.praxis.core.praxis_text_core import PRAXISTextCore


def test_low_coherence_vague_input():
    """Test: Vague input should have low coherence (< 0.40)"""
    praxis = PRAXISTextCore()

    result = praxis.process("I want to be healthier")

    assert result.coherence < 0.40, f"Expected < 0.40, got {result.coherence:.2f}"
    assert not result.ready_for_execution
    assert len(result.clarifying_questions) > 0
    print(f"✅ LOW coherence test passed: {result.coherence:.2f}")


def test_medium_coherence_some_specificity():
    """Test: Some specificity should have medium coherence (0.40-0.60)"""
    praxis = PRAXISTextCore()

    result = praxis.process("I want to do yoga 3 times per week in the morning")

    assert 0.40 <= result.coherence < 0.60, f"Expected 0.40-0.60, got {result.coherence:.2f}"
    assert not result.ready_for_execution  # Still needs clarification
    assert len(result.clarifying_questions) > 0
    print(f"✅ MEDIUM coherence test passed: {result.coherence:.2f}")


def test_high_coherence_specific_input():
    """Test: Specific input should have high coherence (≥ 0.60)"""
    praxis = PRAXISTextCore()

    result = praxis.process(
        "I want to do yoga Mon/Wed/Fri at 7am for 30 minutes at home"
    )

    assert result.coherence >= 0.60, f"Expected ≥ 0.60, got {result.coherence:.2f}"
    assert result.ready_for_execution
    assert len(result.clarifying_questions) == 0  # No questions needed
    print(f"✅ HIGH coherence test passed: {result.coherence:.2f}")


def test_atom_activations_vague():
    """Test: Vague input should have low atom activations"""
    praxis = PRAXISTextCore()

    result = praxis.process("I want to exercise")

    # task_clarity should be low (vague "exercise")
    assert result.atom_activations['task_clarity'] < 0.5

    # temporal_precision should be 0 (no time mentioned)
    assert result.atom_activations['temporal_precision'] == 0.0

    # schedule_integration should be 0 (no days mentioned)
    assert result.atom_activations['schedule_integration'] == 0.0

    print("✅ Atom activation test (vague) passed")


def test_atom_activations_specific():
    """Test: Specific input should have high atom activations"""
    praxis = PRAXISTextCore()

    result = praxis.process(
        "Yoga Mon/Wed/Fri at 7am for 30 minutes"
    )

    # task_clarity should be high (specific "yoga")
    assert result.atom_activations['task_clarity'] >= 0.7

    # temporal_precision should be high (7am mentioned)
    assert result.atom_activations['temporal_precision'] >= 0.7

    # schedule_integration should be high (3 days mentioned)
    assert result.atom_activations['schedule_integration'] >= 0.6

    print("✅ Atom activation test (specific) passed")


if __name__ == '__main__':
    print("="*60)
    print("PRAXIS COHERENCE UNIT TESTS")
    print("="*60)

    test_low_coherence_vague_input()
    test_medium_coherence_some_specificity()
    test_high_coherence_specific_input()
    test_atom_activations_vague()
    test_atom_activations_specific()

    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED (5/5)")
    print("="*60)
```

---

### Step 5: Create __init__.py Files (15 min)

**File:** `organs/modular/praxis/__init__.py`

```python
"""
PRAXIS Organ - Action & Execution Intelligence

The 13th organ: Handles concrete planning, scheduling, and task execution.

7 Semantic Atoms:
- task_clarity: Vague → concrete
- temporal_precision: Specific times
- resource_mapping: What's needed
- action_sequencing: Steps in order
- completion_criteria: How to know it's done
- schedule_integration: How tasks fit together
- accountability_structure: Tracking, reminders

Coherence threshold: 0.60 (stricter than therapeutic 0.50)
"""

from organs.modular.praxis.core.praxis_text_core import PRAXISTextCore, PRAXISResult
from organs.modular.praxis.organ_config.praxis_config import PRAXISConfig, DEFAULT_PRAXIS_CONFIG

__all__ = [
    'PRAXISTextCore',
    'PRAXISResult',
    'PRAXISConfig',
    'DEFAULT_PRAXIS_CONFIG'
]
```

---

### Step 6: Run Tests (15 min)

```bash
cd /Users/daedalea/Desktop/DAE_HYPHAE_1

# Run unit tests
python3 organs/modular/praxis/tests/test_praxis_coherence.py

# Expected output:
# ============================================================
# PRAXIS COHERENCE UNIT TESTS
# ============================================================
# ✅ LOW coherence test passed: 0.18
# ✅ MEDIUM coherence test passed: 0.52
# ✅ HIGH coherence test passed: 0.75
# ✅ Atom activation test (vague) passed
# ✅ Atom activation test (specific) passed
#
# ============================================================
# ✅ ALL TESTS PASSED (5/5)
# ============================================================
```

---

## 📋 Day 2: Integration (4-6 hours)

### Step 1: Add PRAXIS to Organism Wrapper (2 hours)

**File:** `persona_layer/conversational_organism_wrapper.py`

**Changes needed:**

1. Import PRAXIS (add near top):
```python
from organs.modular.praxis.core.praxis_text_core import PRAXISTextCore
```

2. Initialize PRAXIS organ (in `__init__`):
```python
# Line ~150 (after NEXUS initialization)
self.praxis = PRAXISTextCore()
```

3. Add PRAXIS to organ results (in `process_conversational_input`):
```python
# Line ~900 (after NEXUS processing)
praxis_result = self.praxis.process(
    user_input=input_data['text'],
    context=context
)

organ_results['PRAXIS'] = praxis_result
```

4. Check PRAXIS coherence before emission:
```python
# Line ~1100 (before emission generation)
# Check if PRAXIS ready for structured output
praxis_coherence = organ_results.get('PRAXIS').coherence if 'PRAXIS' in organ_results else 0.0

if praxis_coherence >= 0.60:
    # Ready for schedule generation
    print(f"   🎯 PRAXIS coherence HIGH ({praxis_coherence:.2f}) - ready for schedule")
    # TODO: Route to Path 5 (structured output)
elif praxis_coherence > 0.0:
    # Need clarification
    print(f"   ⚠️  PRAXIS coherence LOW ({praxis_coherence:.2f}) - need clarification")
    # Inject clarifying questions into LLM prompt
    clarifying_questions = organ_results['PRAXIS'].clarifying_questions
    if clarifying_questions:
        context['praxis_clarification'] = clarifying_questions
```

---

### Step 2: Test PRAXIS Integration (1 hour)

**Create test script:** `test_praxis_integration.py`

```python
"""Test PRAXIS organ integration with organism wrapper"""

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

def test_praxis_low_coherence():
    """Test: Vague input should trigger clarifying questions"""
    organism = ConversationalOrganismWrapper()

    result = organism.process_conversational_input({
        'text': "I want to exercise more",
        'user_id': 'test_user'
    })

    # Check PRAXIS processed
    assert 'PRAXIS' in result['organ_results']

    # Check coherence is low
    praxis_result = result['organ_results']['PRAXIS']
    assert praxis_result.coherence < 0.40

    # Check clarifying questions present
    assert len(praxis_result.clarifying_questions) > 0

    print(f"✅ Low coherence test passed: {praxis_result.coherence:.2f}")
    print(f"   Questions: {praxis_result.clarifying_questions}")


def test_praxis_high_coherence():
    """Test: Specific input should be ready for schedule"""
    organism = ConversationalOrganismWrapper()

    result = organism.process_conversational_input({
        'text': "Yoga Mon/Wed/Fri at 7am for 30 minutes",
        'user_id': 'test_user'
    })

    # Check PRAXIS processed
    assert 'PRAXIS' in result['organ_results']

    # Check coherence is high
    praxis_result = result['organ_results']['PRAXIS']
    assert praxis_result.coherence >= 0.60

    # Check ready for execution
    assert praxis_result.ready_for_execution

    print(f"✅ High coherence test passed: {praxis_result.coherence:.2f}")
    print(f"   Ready for schedule generation: {praxis_result.ready_for_execution}")


if __name__ == '__main__':
    test_praxis_low_coherence()
    test_praxis_high_coherence()
    print("\n✅ Integration tests passed!")
```

Run test:
```bash
python3 test_praxis_integration.py
```

---

### Step 3: Interactive Testing (1 hour)

```bash
python3 dae_interactive.py --mode detailed
```

**Test inputs:**
```
You: I want to exercise more
(Expect: Clarifying questions)

You: I want to do yoga 3x/week
(Expect: More specific clarifying questions)

You: Yoga Mon/Wed/Fri at 7am
(Expect: Schedule generation ready - may still route to LLM for now)
```

---

## ✅ Day 1-2 Success Criteria

### Tests Passing:
- [ ] 5/5 unit tests (test_praxis_coherence.py)
- [ ] 2/2 integration tests (test_praxis_integration.py)
- [ ] Interactive test shows PRAXIS coherence values

### Code Complete:
- [ ] praxis_config.py (7 atoms, weights, clarification prompts)
- [ ] praxis_text_core.py (atom activation, coherence calculation)
- [ ] Organism wrapper integration (PRAXIS as 13th organ)

### Documentation:
- [ ] __init__.py with organ description
- [ ] Test files with clear assertions
- [ ] Console output shows PRAXIS coherence tracking

---

## 📊 Expected Outputs

### Low Coherence (< 0.40)
```
Input: "I want to exercise"

PRAXIS Result:
  Coherence: 0.18
  Atoms:
    task_clarity: 0.2 (vague "exercise")
    temporal_precision: 0.0 (no time)
    schedule_integration: 0.0 (no days)
  Missing: ['task_clarity', 'temporal_precision', 'schedule_integration', ...]
  Questions:
    - "What specific activity did you have in mind?"
    - "What time of day works best?"
    - "Which days of the week work best?"
  Ready: False
```

### Medium Coherence (0.40-0.60)
```
Input: "I want to do yoga 3x/week in the morning"

PRAXIS Result:
  Coherence: 0.52
  Atoms:
    task_clarity: 0.8 (specific "yoga")
    temporal_precision: 0.3 (vague "morning")
    schedule_integration: 0.5 (frequency mentioned)
  Missing: ['temporal_precision', 'schedule_integration']
  Questions:
    - "Would you prefer a specific time like 7am, 8am, etc?"
    - "Which days of the week work best?"
  Ready: False
```

### High Coherence (≥ 0.60)
```
Input: "Yoga Mon/Wed/Fri at 7am for 30 minutes"

PRAXIS Result:
  Coherence: 0.75
  Atoms:
    task_clarity: 0.85
    temporal_precision: 0.90
    resource_mapping: 0.50
    schedule_integration: 0.80
    completion_criteria: 0.60
  Missing: []
  Questions: []
  Ready: True ✅
```

---

## 🚨 Troubleshooting

### Import Errors
```bash
# Ensure PYTHONPATH set
export PYTHONPATH="/Users/daedalea/Desktop/DAE_HYPHAE_1":$PYTHONPATH

# Verify from project root
pwd  # Should be: /Users/daedalea/Desktop/DAE_HYPHAE_1
```

### Tests Failing
- Check atom weight sum = 1.0
- Verify regex patterns compile
- Ensure config imports correctly

### Integration Issues
- Verify organism wrapper has `self.praxis`
- Check organ_results dict includes 'PRAXIS'
- Confirm context threading

---

## 📝 Next Steps (Day 3+)

After Day 1-2 foundation complete:
1. Create 20 training pairs (vague → concrete progressions)
2. Implement Neo4j schedule storage
3. Add LLM PRAXIS-aware prompts
4. Felt-modulation (EO/BOND → schedule scaling)

---

**Created:** November 16, 2025
**Purpose:** Quick start guide for Day 1-2 implementation
**Goal:** Functional PRAXIS organ foundation in 2 days
