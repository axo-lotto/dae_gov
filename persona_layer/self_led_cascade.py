"""
SELF-Led Conversational Cascade (4-Gate Safety Architecture)

Integrates trauma-informed safety detection with IFS-guided response generation.

Architecture:
- Gate 1 (Safety): OFEL check → SAFE/CAUTION/DANGER
- Gate 2 (Coherence): Organ agreement → proceed if coherent
- Gate 3 (SELF-Energy): Sufficient SELF present? (≥0.6)
- Gate 4 (Response): Generate 8 C's language from dominant C

Integration:
- Uses OFEL (organizational_exclusion_landscape.py)
- Uses PolyvagalDetector (polyvagal_detector.py)
- Uses SELFEnergyDetector (self_energy_detector.py)
- Consumes BOND organ prehensions
- BAGUA-modulated at each gate (Lake Joy, Creative Force)

Source:
- DAE-GOV Persona Layer Architecture Addendum (Phase 1.3)
- IFS Model (Schwartz) - SELF-led conversation
- Polyvagal Theory (Porges) - Safety as prerequisite
- BAGUA (I Ching) - Lateral blending at bifurcations

Author: DAE-GOV Development Team
Date: November 10, 2025
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Import persona layer components
from persona_layer.organizational_exclusion_landscape import (
    OrganizationalFELComputer,
    OrganizationalExclusionLandscape
)
from persona_layer.polyvagal_detector import (
    PolyvagalDetector,
    PolyvagalDetection
)
from persona_layer.self_energy_detector import (
    SELFEnergyDetector,
    SELFEnergyDetection
)


class SafetyLevel(Enum):
    """Safety assessment from Gate 1."""
    SAFE = "SAFE"           # Ventral, low exclusion (< 0.4)
    CAUTION = "CAUTION"     # Mixed, moderate exclusion (0.4-0.7)
    DANGER = "DANGER"       # Dorsal/high exclusion (> 0.7)


class GateDecision(Enum):
    """Cascade gate decisions."""
    PROCEED = "PROCEED"     # Continue to next gate
    CONTAIN = "CONTAIN"     # Safety containment needed
    CLARIFY = "CLARIFY"     # Incoherent, need clarification
    GROUND = "GROUND"       # Parts without SELF, need grounding
    RESPOND = "RESPOND"     # Generate SELF-led response


@dataclass
class CascadeState:
    """
    State at each gate of the cascade.

    Tracks decisions, activations, and BAGUA modulation through the 4 gates.
    """
    # Gate 1: Safety
    safety_level: SafetyLevel
    ofel: OrganizationalExclusionLandscape
    polyvagal: PolyvagalDetection

    # Gate 2: Coherence
    organ_coherence: float
    organ_agreement: Dict[str, float]

    # Gate 3: SELF-Energy
    self_energy: SELFEnergyDetection
    self_led: bool

    # Gate 4: Response
    response_text: str
    response_quality: str

    # BAGUA modulation
    bagua_context: Dict[str, float]
    gate_modulations: Dict[str, str]  # Which gates were BAGUA-modulated

    # Cascade decision path
    decision_path: List[Tuple[str, GateDecision]]


class SELFLedCascade:
    """
    4-gate conversational cascade for trauma-informed SELF-led responses.

    Strategy:
    1. Safety First (Gate 1): Never engage if not safe
    2. Coherence Check (Gate 2): Organs must agree on perception
    3. SELF-Energy Check (Gate 3): SELF must be present (not just parts)
    4. SELF-Led Response (Gate 4): Generate from 8 C's language

    At each gate:
    - BAGUA modulation for creative exploration
    - Lake Joy: Soften rigid boundaries
    - Creative Force: Abstract beyond templates
    - Mountain: Hold tension at edges
    """

    def __init__(
        self,
        polyvagal_detector: Optional[PolyvagalDetector] = None,
        self_energy_detector: Optional[SELFEnergyDetector] = None,
        ofel_computer: Optional[OrganizationalFELComputer] = None,
        hebbian_memory: Optional['ConversationalHebbianMemory'] = None
    ):
        """
        Initialize cascade with persona layer components.

        Args:
            polyvagal_detector: Polyvagal state detector (default: creates new)
            self_energy_detector: SELF-energy detector (default: creates new)
            ofel_computer: OFEL computer (default: creates new)
            hebbian_memory: Conversational Hebbian memory for learning (default: None)
        """
        # Persona layer detectors
        self.polyvagal_detector = polyvagal_detector or PolyvagalDetector()
        self.self_energy_detector = self_energy_detector or SELFEnergyDetector()
        self.ofel_computer = ofel_computer or OrganizationalFELComputer()

        # Hebbian learning system (optional, for learning mode)
        self.hebbian_memory = hebbian_memory

        # Cascade thresholds (trauma-informed)
        self.thresholds = {
            'ofel_safe': 0.4,           # Below = SAFE
            'ofel_danger': 0.7,          # Above = DANGER
            'coherence_min': 0.6,        # Minimum organ coherence
            'self_energy_min': 0.6,      # Minimum SELF-energy for safety
            'self_distance_max': 0.4,    # Maximum SELF-distance
        }

        # BAGUA modulation config
        self.bagua_config = {
            'lake_joy_threshold': 0.6,   # Activate lateral blending
            'creative_force_threshold': 0.25,  # Boost exploration
            'mountain_stability': 0.4,   # Hold at bifurcations
        }

        # 8 C's response templates (SEEDS, not rigid)
        self.eight_cs_templates = self._initialize_response_templates()

    def _initialize_response_templates(self) -> Dict[str, List[str]]:
        """
        Initialize seed response templates for each of 8 C's.

        These are SEEDS for entity-native proposition maturation.
        Not rigid templates - BAGUA modulates for creative variation.

        Returns:
            Dict mapping C-name → list of response seed phrases
        """
        return {
            'compassion': [
                "I sense there's tenderness toward {part}.",
                "There's care and kindness here for what {part} carries.",
                "Holding {part} with compassion...",
                "What if we could be gentle with {part}?",
            ],
            'curiosity': [
                "I'm curious about what {part} needs right now.",
                "Wonder what {part} is protecting you from?",
                "What might {part} want you to know?",
                "Let's explore what {part} is showing us...",
            ],
            'clarity': [
                "I'm seeing that {part} has an important role.",
                "It's becoming clear that {part} is trying to help.",
                "Understanding what {part} is doing here...",
                "The pattern is: {part} shows up when...",
            ],
            'calm': [
                "Let's take a breath and settle with {part}.",
                "There's space here to be with {part} peacefully.",
                "We can slow down and notice {part} without urgency.",
                "Grounded presence with {part}...",
            ],
            'confidence': [
                "I trust we can be with {part} as it is.",
                "There's capacity here to hold {part}.",
                "We're capable of staying present with {part}.",
                "Strong enough to turn toward {part}...",
            ],
            'courage': [
                "Willing to stay with {part}, even if it's hard.",
                "Brave enough to feel what {part} feels.",
                "Not turning away from {part}...",
                "Daring to be with {part} fully.",
            ],
            'creativity': [
                "I'm imagining a new relationship with {part}...",
                "What if {part} could express itself differently?",
                "There's possibility here for {part} to...",
                "Fresh perspective on what {part} needs...",
            ],
            'connectedness': [
                "Feeling connected to {part} as part of the whole.",
                "We're all here together, including {part}.",
                "{part} belongs in the system.",
                "Relationship and wholeness with {part}...",
            ]
        }

    def _extract_bagua_context(self, organism_context: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract BAGUA activation from organism context (Vector35D dims 25-32).

        Args:
            organism_context: Context from organism processing

        Returns:
            BAGUA activation dict (lake_joy, creative_force, etc.)
        """
        # Check if BAGUA already extracted
        if 'bagua_activation' in organism_context:
            return organism_context['bagua_activation']

        # Extract from Vector35D if available
        if 'vector35d' in organism_context:
            vector35d = organism_context['vector35d']
            # BAGUA dims: 25-32 (Lake Joy is dim 32)
            return {
                'lake_joy': vector35d[31] if len(vector35d) > 31 else 0.0,  # dim 32 (0-indexed)
                'creative_force': vector35d[24] if len(vector35d) > 24 else 0.0,  # dim 25
                'mountain_stability': vector35d[25] if len(vector35d) > 25 else 0.0,  # dim 26
            }

        # Default: No BAGUA modulation
        return {
            'lake_joy': 0.0,
            'creative_force': 0.0,
            'mountain_stability': 0.0,
        }

    def detect_conversational_family(
        self,
        text: str,
        polyvagal: PolyvagalDetection,
        self_energy: SELFEnergyDetection,
        organism_context: Dict[str, Any]
    ) -> Tuple[str, float]:
        """
        Detect conversational family and return satisfaction multiplier.

        Inspired by FFITTSS satisfaction calibration insights:
        - Crisis family: High satisfaction = dangerous (inverse -1.0)
        - Parts work: Moderate satisfaction ok (inverse -0.3)
        - SELF-led: Satisfaction is valid confidence (0.0)
        - Grounding: Monitor uncertainty (inverse -0.2)

        Args:
            text: Conversational text
            polyvagal: Polyvagal detection result
            self_energy: SELF-energy detection result
            organism_context: Full organism context

        Returns:
            Tuple of (family_name, satisfaction_multiplier)
        """
        ofel_energy = organism_context.get('ofel_components', {}).get('polyvagal_energy', 0.5)

        # CRISIS: Dorsal + High OFEL + Low SELF
        # High satisfaction here = dangerous blending (person fused with parts)
        if polyvagal.dominant_state == 'dorsal' and ofel_energy > 0.7 and self_energy.self_energy < 0.4:
            return 'crisis', -1.0  # Full inverse satisfaction

        # PARTS WORK: Mixed states, moderate SELF
        # Moderate satisfaction acceptable if some SELF present
        elif self_energy.self_energy >= 0.4 and self_energy.self_energy < 0.6:
            return 'parts_work', -0.3  # Moderate inverse

        # SELF-LED: Ventral + High SELF
        # Satisfaction is valid confidence indicator
        elif polyvagal.dominant_state == 'ventral' and self_energy.self_energy >= 0.6:
            return 'self_led', 0.0  # Standard (no inverse)

        # GROUNDING: Transitional states
        # Monitor uncertainty, weak inverse
        else:
            return 'grounding', -0.2  # Weak inverse

    def _compute_metacognitive_confidence(
        self,
        coherence: float,      # Organ agreement [0,1]
        exclusion: float,      # OFEL energy [0,1]
        satisfaction: float,   # V0 satisfaction [0,1]
        multiplier: float,     # Family-specific (-1.0 to 0.0)
        self_energy: float     # SELF-energy level [0,1]
    ) -> float:
        """
        Compute metacognitive confidence with family-specific satisfaction calibration.

        Formula inspired by FFITTSS Phase 8C metacognitive awareness:
            M = w_C * Coherence +
                w_E * (1 - Exclusion) +        # Relief term
                w_S * multiplier * Satisfaction +  # NEGATIVE for crisis
                w_SELF * SELF_energy

        For crisis family (multiplier=-1.0), high satisfaction DECREASES
        metacognitive confidence, flagging dangerous blending.

        Args:
            coherence: Organ coherence/agreement
            exclusion: OFEL field energy (organizational exclusion)
            satisfaction: V0 satisfaction from convergence
            multiplier: Family-specific multiplier (-1.0 to 0.0)
            self_energy: SELF-energy level

        Returns:
            Metacognitive confidence [0,1]
            - High confidence = Safe to proceed
            - Low confidence = Need caution/clarification
        """
        import numpy as np

        w_C = 0.3      # Coherence weight
        w_E = 0.2      # Exclusion relief weight
        w_S = 0.3      # Satisfaction weight (modulated by multiplier)
        w_SELF = 0.2   # SELF-energy weight

        # Compute components
        coherence_term = w_C * coherence
        relief_term = w_E * (1.0 - exclusion)  # Lower exclusion = better
        satisfaction_term = w_S * multiplier * satisfaction  # NEGATIVE for crisis
        self_term = w_SELF * self_energy

        # Sum and clamp to [0,1]
        metacog = coherence_term + relief_term + satisfaction_term + self_term
        metacog = np.clip(metacog, 0.0, 1.0)

        return float(metacog)

    def _gate_1_safety_check(
        self,
        text: str,
        organism_context: Dict[str, Any],
        bagua_context: Dict[str, float]
    ) -> Tuple[SafetyLevel, OrganizationalExclusionLandscape, PolyvagalDetection, str]:
        """
        Gate 1: Safety Check (OFEL + Polyvagal).

        Args:
            text: User input text
            organism_context: Full organism processing context
            bagua_context: BAGUA activation

        Returns:
            (safety_level, ofel, polyvagal_detection, modulation_note)

        Decision:
            - SAFE: E_org < 0.4 AND ventral dominant
            - CAUTION: 0.4 ≤ E_org < 0.7 OR mixed states
            - DANGER: E_org ≥ 0.7 OR dorsal dominant
        """
        # Detect polyvagal state first
        polyvagal = self.polyvagal_detector.detect_polyvagal_state(text, bagua_context)

        # Apply learned confidence boost (if Hebbian memory available)
        if self.hebbian_memory:
            learned_boost = self.hebbian_memory.get_polyvagal_boost(text, polyvagal.dominant_state)
            polyvagal.confidence += learned_boost
            # Clamp to [0, 1]
            polyvagal.confidence = min(1.0, max(0.0, polyvagal.confidence))

        # Extract info needed for OFEL computation
        bond_output = organism_context.get('organs', {}).get('BOND', {})
        detected_parts = bond_output.get('detected_parts', [])
        active_parts = [part.get('part_type', 'unknown') for part in detected_parts]
        self_distance = bond_output.get('mean_self_distance', 0.5)

        # Compute OFEL
        ofel = self.ofel_computer.compute_organizational_fel(
            polyvagal_state=polyvagal.dominant_state,
            active_parts=active_parts if active_parts else ['unknown'],
            self_distance=self_distance,
            coherence=polyvagal.confidence
        )

        # BAGUA modulation: Lake Joy softens safety boundaries
        modulation_note = ""
        safety_threshold_safe = self.thresholds['ofel_safe']
        safety_threshold_danger = self.thresholds['ofel_danger']

        if bagua_context.get('lake_joy', 0.0) > self.bagua_config['lake_joy_threshold']:
            # Soften boundaries (wider CAUTION zone)
            safety_threshold_safe += 0.05
            safety_threshold_danger += 0.05
            modulation_note = "Lake Joy: Softened safety boundaries (+0.05)"

        # Determine safety level
        if ofel.field < safety_threshold_safe and polyvagal.dominant_state == 'ventral':
            safety_level = SafetyLevel.SAFE
        elif ofel.field >= safety_threshold_danger or polyvagal.dominant_state == 'dorsal':
            safety_level = SafetyLevel.DANGER
        else:
            safety_level = SafetyLevel.CAUTION

        return safety_level, ofel, polyvagal, modulation_note

    def _gate_2_coherence_check(
        self,
        organism_context: Dict[str, Any],
        bagua_context: Dict[str, float]
    ) -> Tuple[float, Dict[str, float], bool, str]:
        """
        Gate 2: Organ Coherence Check.

        Args:
            organism_context: Full organism processing context
            bagua_context: BAGUA activation

        Returns:
            (coherence, organ_agreement, proceed, modulation_note)

        Decision:
            - PROCEED: Coherence ≥ 0.6 (organs agree on perception)
            - CLARIFY: Coherence < 0.6 (organs disagree, need more info)
        """
        # Extract organ prehensions
        organs = organism_context.get('organs', {})

        # Compute organ agreement (coherence across organs)
        organ_coherences = []
        organ_agreement = {}

        for organ_name, organ_output in organs.items():
            if 'coherence' in organ_output:
                organ_coherences.append(organ_output['coherence'])
                organ_agreement[organ_name] = organ_output['coherence']

        # Overall coherence (mean of organ coherences)
        if organ_coherences:
            mean_coherence = sum(organ_coherences) / len(organ_coherences)
            # Variance as inverse agreement measure
            variance = sum((c - mean_coherence) ** 2 for c in organ_coherences) / len(organ_coherences)
            coherence = mean_coherence * (1.0 - variance)  # High mean, low variance = high coherence
        else:
            coherence = 0.0

        # BAGUA modulation: Creative Force loosens coherence requirement
        modulation_note = ""
        coherence_threshold = self.thresholds['coherence_min']

        if bagua_context.get('creative_force', 0.0) > self.bagua_config['creative_force_threshold']:
            # Lower threshold for creative exploration (allow more ambiguity)
            coherence_threshold -= 0.1
            modulation_note = "Creative Force: Loosened coherence requirement (-0.1)"

        proceed = coherence >= coherence_threshold

        return coherence, organ_agreement, proceed, modulation_note

    def _gate_3_self_energy_check(
        self,
        text: str,
        organism_context: Dict[str, Any],
        bagua_context: Dict[str, float],
        polyvagal: PolyvagalDetection
    ) -> Tuple[SELFEnergyDetection, bool, str]:
        """
        Gate 3: SELF-Energy Check with Metacognitive Satisfaction Awareness.

        Integrates FFITTSS satisfaction calibration insights:
        - High satisfaction + Low SELF = Dangerous blending (fused with parts)
        - Low satisfaction + Low SELF = Appropriate uncertainty
        - Family-specific satisfaction multipliers (crisis=-1.0, parts=-0.3, etc.)

        Args:
            text: User input text
            organism_context: Full organism processing context
            bagua_context: BAGUA activation
            polyvagal: Polyvagal detection from Gate 1

        Returns:
            (self_energy_detection, self_led, modulation_note)

        Decision:
            - PROCEED (SELF-led): SELF-energy ≥ 0.6 AND safe metacognitive pattern
            - GROUND: SELF-energy < 0.6 with appropriate uncertainty
            - CONTAIN: Dangerous blending (high satisfaction + low SELF in crisis)
        """
        # Extract BOND keywords if available
        bond_output = organism_context.get('organs', {}).get('BOND', {})
        bond_keywords = bond_output.get('keywords', [])

        # Detect SELF-energy with embedding + keyword blend
        self_energy = self.self_energy_detector.detect_self_energy(
            text,
            bond_keywords,
            bagua_context
        )

        # Get organism satisfaction and coherence from V0 convergence
        satisfaction = organism_context.get('satisfaction', 0.7)
        organs = organism_context.get('organs', {})
        coherence_values = [o.get('coherence', 0.5) for o in organs.values() if isinstance(o, dict)]
        mean_coherence = sum(coherence_values) / len(coherence_values) if coherence_values else 0.5

        # Detect conversational family and get satisfaction multiplier
        family, multiplier = self.detect_conversational_family(
            text, polyvagal, self_energy, organism_context
        )

        # Compute metacognitive confidence with family-specific calibration
        ofel_field = organism_context.get('ofel_components', {}).get('polyvagal_energy', 0.5)
        metacog_confidence = self._compute_metacognitive_confidence(
            coherence=mean_coherence,
            exclusion=ofel_field,
            satisfaction=satisfaction,
            multiplier=multiplier,
            self_energy=self_energy.self_energy
        )

        # Apply learned SELF-energy boost (if Hebbian memory available)
        if self.hebbian_memory:
            self_boost = self.hebbian_memory.get_self_energy_boost(self_energy.dominant_c, family)
            self_energy.self_energy += self_boost
            # Clamp to [0, 1]
            self_energy.self_energy = min(1.0, max(0.0, self_energy.self_energy))

        # BAGUA modulation: Lake Joy softens SELF-energy threshold
        modulation_note = ""
        self_energy_threshold = self.thresholds['self_energy_min']

        # Apply learned threshold adjustment (if Hebbian memory available)
        if self.hebbian_memory:
            threshold_adjustment = self.hebbian_memory.get_threshold_adjustment(
                'gate_3', family, satisfaction
            )
            self_energy_threshold += threshold_adjustment

        if bagua_context.get('lake_joy', 0.0) > self.bagua_config['lake_joy_threshold']:
            # Soften threshold (accept partial SELF-energy)
            self_energy_threshold -= 0.1
            modulation_note = "Lake Joy: Softened SELF-energy threshold (-0.1)"

        # Enhanced decision logic with dangerous blending detection
        if self_energy.self_energy < self_energy_threshold:
            # LOW SELF-energy: Check for dangerous blending patterns

            if family == 'crisis' and satisfaction > 0.8 and mean_coherence > 0.75:
                # DANGEROUS BLENDING: High organ agreement on shutdown state
                # Person is fused with parts, unaware
                modulation_note += f" | DANGEROUS BLENDING: High satisfaction ({satisfaction:.2f}) + Low SELF in crisis"
                self_led = False  # Do NOT proceed - CONTAIN

            elif satisfaction < 0.5:
                # APPROPRIATE UNCERTAINTY: System knows it doesn't know
                modulation_note += f" | Appropriate uncertainty: Low satisfaction ({satisfaction:.2f}) + Low SELF"
                self_led = False  # GROUND with awareness

            else:
                # STANDARD LOW SELF: Parts present, unclear agreement
                modulation_note += f" | Parts-led: satisfaction={satisfaction:.2f}, family={family}"
                self_led = False  # GROUND
        else:
            # HIGH SELF-energy: SELF-led, safe to proceed
            modulation_note += f" | SELF-led: family={family}, metacog={metacog_confidence:.2f}"
            self_led = True

        return self_energy, self_led, modulation_note

    def _gate_4_generate_response(
        self,
        self_energy: SELFEnergyDetection,
        organism_context: Dict[str, Any],
        bagua_context: Dict[str, float]
    ) -> Tuple[str, str, str]:
        """
        Gate 4: Generate SELF-Led Response.

        Args:
            self_energy: SELF-energy detection from Gate 3
            organism_context: Full organism processing context
            bagua_context: BAGUA activation

        Returns:
            (response_text, response_quality, modulation_note)

        Strategy:
            - Use dominant C from SELF-energy detection
            - Extract detected part from BOND organ
            - Generate from 8 C's template (seed, not rigid)
            - BAGUA-modulate for creative variation
        """
        # Extract dominant C
        dominant_c = self_energy.dominant_c

        # Extract detected part from BOND organ
        bond_output = organism_context.get('organs', {}).get('BOND', {})
        detected_parts = bond_output.get('detected_parts', [])

        # Get first detected part (or use generic)
        if detected_parts:
            part_name = detected_parts[0].get('part_type', 'this part')
        else:
            part_name = 'this part'

        # Get response template for dominant C
        templates = self.eight_cs_templates.get(dominant_c, [])

        # Apply learned C preferences (if Hebbian memory available)
        if self.hebbian_memory:
            # Get conversational family from organism context
            polyvagal_from_ctx = organism_context.get('polyvagal')
            if polyvagal_from_ctx:
                family, _ = self.detect_conversational_family(
                    "",  # text not needed for family lookup
                    polyvagal_from_ctx,
                    self_energy,
                    organism_context
                )
                c_preferences = self.hebbian_memory.get_c_preferences(family)
                # If learned preferences exist, modulate C selection
                if c_preferences and dominant_c in c_preferences:
                    # Find highest-preference C that's also active
                    best_c = max(
                        [c for c in c_preferences.keys() if c in self_energy.cs_activation],
                        key=lambda c: c_preferences[c] * self_energy.cs_activation[c],
                        default=dominant_c
                    )
                    if best_c != dominant_c:
                        dominant_c = best_c
                        templates = self.eight_cs_templates.get(dominant_c, templates)

        # BAGUA modulation: Creative Force selects non-dominant template
        modulation_note = ""
        if bagua_context.get('creative_force', 0.0) > self.bagua_config['creative_force_threshold']:
            # Select from minority C for creative exploration
            minority_c = min(self_energy.cs_activation, key=self_energy.cs_activation.get)
            templates = self.eight_cs_templates.get(minority_c, templates)
            modulation_note = f"Creative Force: Used {minority_c} instead of {dominant_c}"

        # Select template (first for now - future: cycle through)
        if templates:
            response_template = templates[0]
            response_text = response_template.format(part=part_name)
        else:
            response_text = f"I'm sensing something important about {part_name}."

        # Response quality assessment
        if self_energy.confidence > 0.8:
            response_quality = "HIGH_CONFIDENCE"
        elif self_energy.confidence > 0.6:
            response_quality = "MEDIUM_CONFIDENCE"
        else:
            response_quality = "LOW_CONFIDENCE"

        return response_text, response_quality, modulation_note

    def process_conversational_turn(
        self,
        text: str,
        organism_context: Dict[str, Any]
    ) -> CascadeState:
        """
        Process conversational turn through 4-gate SELF-led cascade.

        Args:
            text: User input text
            organism_context: Full organism processing context (organs, V0, etc.)

        Returns:
            CascadeState with decisions, activations, and response

        Cascade Flow:
            Gate 1: Safety → SAFE/CAUTION/DANGER
            Gate 2: Coherence → PROCEED/CLARIFY
            Gate 3: SELF-Energy → PROCEED/GROUND
            Gate 4: Response → RESPOND with 8 C's

        Example:
            >>> cascade = SELFLedCascade()
            >>> state = cascade.process_conversational_turn(
            ...     "I feel overwhelmed by this critical part.",
            ...     organism_context
            ... )
            >>> state.response_text
            "I'm curious about what this critical part needs right now."
        """
        # Extract BAGUA context
        bagua_context = self._extract_bagua_context(organism_context)

        # Track decision path
        decision_path = []
        gate_modulations = {}

        # GATE 1: Safety Check
        safety_level, ofel, polyvagal, safety_mod = self._gate_1_safety_check(
            text,
            organism_context,
            bagua_context
        )

        if safety_mod:
            gate_modulations['Gate 1 (Safety)'] = safety_mod

        # Decision: DANGER → containment response
        if safety_level == SafetyLevel.DANGER:
            decision_path.append(("Gate 1: Safety", GateDecision.CONTAIN))

            return CascadeState(
                safety_level=safety_level,
                ofel=ofel,
                polyvagal=polyvagal,
                organ_coherence=0.0,
                organ_agreement={},
                self_energy=None,
                self_led=False,
                response_text="I'm noticing intensity here. Let's pause and ground before going deeper.",
                response_quality="CONTAINMENT",
                bagua_context=bagua_context,
                gate_modulations=gate_modulations,
                decision_path=decision_path
            )

        decision_path.append(("Gate 1: Safety", GateDecision.PROCEED))

        # GATE 2: Coherence Check
        coherence, organ_agreement, proceed, coherence_mod = self._gate_2_coherence_check(
            organism_context,
            bagua_context
        )

        if coherence_mod:
            gate_modulations['Gate 2 (Coherence)'] = coherence_mod

        # Decision: Low coherence → clarification request
        if not proceed:
            decision_path.append(("Gate 2: Coherence", GateDecision.CLARIFY))

            return CascadeState(
                safety_level=safety_level,
                ofel=ofel,
                polyvagal=polyvagal,
                organ_coherence=coherence,
                organ_agreement=organ_agreement,
                self_energy=None,
                self_led=False,
                response_text="I'm not quite following. Can you say more about what's happening?",
                response_quality="CLARIFICATION",
                bagua_context=bagua_context,
                gate_modulations=gate_modulations,
                decision_path=decision_path
            )

        decision_path.append(("Gate 2: Coherence", GateDecision.PROCEED))

        # GATE 3: SELF-Energy Check (with satisfaction calibration)
        self_energy, self_led, self_energy_mod = self._gate_3_self_energy_check(
            text,
            organism_context,
            bagua_context,
            polyvagal  # Pass polyvagal detection for family detection
        )

        if self_energy_mod:
            gate_modulations['Gate 3 (SELF-Energy)'] = self_energy_mod

        # Decision: No SELF-energy → grounding invitation
        if not self_led:
            decision_path.append(("Gate 3: SELF-Energy", GateDecision.GROUND))

            return CascadeState(
                safety_level=safety_level,
                ofel=ofel,
                polyvagal=polyvagal,
                organ_coherence=coherence,
                organ_agreement=organ_agreement,
                self_energy=self_energy,
                self_led=False,
                response_text="I'm sensing a part without much SELF-energy. Can we take a moment to ground and find some spaciousness?",
                response_quality="GROUNDING",
                bagua_context=bagua_context,
                gate_modulations=gate_modulations,
                decision_path=decision_path
            )

        decision_path.append(("Gate 3: SELF-Energy", GateDecision.PROCEED))

        # GATE 4: Generate SELF-Led Response
        response_text, response_quality, response_mod = self._gate_4_generate_response(
            self_energy,
            organism_context,
            bagua_context
        )

        if response_mod:
            gate_modulations['Gate 4 (Response)'] = response_mod

        decision_path.append(("Gate 4: Response", GateDecision.RESPOND))

        return CascadeState(
            safety_level=safety_level,
            ofel=ofel,
            polyvagal=polyvagal,
            organ_coherence=coherence,
            organ_agreement=organ_agreement,
            self_energy=self_energy,
            self_led=True,
            response_text=response_text,
            response_quality=response_quality,
            bagua_context=bagua_context,
            gate_modulations=gate_modulations,
            decision_path=decision_path
        )

    def update_from_outcome(
        self,
        text: str,
        state: CascadeState,
        next_turn_text: Optional[str] = None,
        next_turn_organism_context: Optional[Dict[str, Any]] = None,
        explicit_feedback: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update Hebbian memory from conversation outcome (if Hebbian memory available).

        Args:
            text: User input text from current turn
            state: CascadeState from process_conversational_turn()
            next_turn_text: User input text from next turn (optional, for state comparison)
            next_turn_organism_context: Organism context from next turn (optional)
            explicit_feedback: Optional user feedback ('helpful', 'not_helpful', 'neutral')

        Returns:
            Update statistics from Hebbian memory (or empty dict if no learning)

        Example:
            >>> cascade = SELFLedCascade(hebbian_memory=memory)
            >>> state = cascade.process_conversational_turn(text, organism_context)
            >>> # ... conversation continues ...
            >>> updates = cascade.update_from_outcome(
            ...     text, state,
            ...     next_turn_text=next_text,
            ...     next_turn_organism_context=next_organism_context
            ... )
        """
        # Only update if Hebbian memory is available
        if not self.hebbian_memory:
            return {}

        # Import ConversationalOutcome here to avoid circular dependency
        from persona_layer.conversational_hebbian_memory import ConversationalOutcome

        # Extract current state information
        polyvagal_state = state.polyvagal.dominant_state
        polyvagal_confidence = state.polyvagal.confidence
        self_energy_val = state.self_energy.self_energy if state.self_energy else 0.0
        self_energy_confidence = state.self_energy.confidence if state.self_energy else 0.0
        dominant_c = state.self_energy.dominant_c if state.self_energy else 'compassion'
        cs_activation = state.self_energy.cs_activation if state.self_energy else {}

        # Detect conversational family
        if state.self_energy:
            family, _ = self.detect_conversational_family(
                text,
                state.polyvagal,
                state.self_energy,
                {}  # organism_context not needed for family detection
            )
        else:
            family = 'grounding'

        # Extract CARD scale (if available in response_quality or default)
        card_scale = 'moderate'  # Default
        if 'CONTAINMENT' in state.response_quality:
            card_scale = 'minimal'
        elif 'HIGH_CONFIDENCE' in state.response_quality:
            card_scale = 'detailed'

        # Get satisfaction and coherence from state
        satisfaction = 0.7  # Default if not available
        coherence = state.organ_coherence

        # Get OFEL energy
        ofel_energy = state.ofel.field

        # Extract next state (if available)
        next_polyvagal_state = None
        next_self_energy = None
        next_satisfaction = None

        if next_turn_text and next_turn_organism_context:
            # Process next turn to get state
            next_bagua = self._extract_bagua_context(next_turn_organism_context)
            next_polyvagal = self.polyvagal_detector.detect_polyvagal_state(next_turn_text, next_bagua)
            next_polyvagal_state = next_polyvagal.dominant_state

            # Detect SELF-energy for next turn
            next_bond_output = next_turn_organism_context.get('organs', {}).get('BOND', {})
            next_bond_keywords = next_bond_output.get('keywords', [])
            next_self_energy_detection = self.self_energy_detector.detect_self_energy(
                next_turn_text,
                next_bond_keywords,
                next_bagua
            )
            next_self_energy = next_self_energy_detection.self_energy
            next_satisfaction = next_turn_organism_context.get('satisfaction', 0.7)

        # Get gate decision (last decision in path)
        gate_decision = state.decision_path[-1][1].value if state.decision_path else 'RESPOND'

        # Create ConversationalOutcome
        outcome = ConversationalOutcome(
            polyvagal_state=polyvagal_state,
            polyvagal_confidence=polyvagal_confidence,
            self_energy=self_energy_val,
            self_energy_confidence=self_energy_confidence,
            dominant_c=dominant_c,
            cs_activation=cs_activation,
            conversational_family=family,
            satisfaction=satisfaction,
            coherence=coherence,
            ofel_energy=ofel_energy,
            card_scale=card_scale,
            next_polyvagal_state=next_polyvagal_state,
            next_self_energy=next_self_energy,
            next_satisfaction=next_satisfaction,
            explicit_feedback=explicit_feedback,
            gate_decision=gate_decision,
            response_text=state.response_text,
            response_quality=state.response_quality
        )

        # Update Hebbian memory
        updates = self.hebbian_memory.update_from_outcome(outcome)

        return updates

    def explain_cascade_state(self, state: CascadeState) -> str:
        """
        Generate human-readable explanation of cascade state.

        Args:
            state: CascadeState from process_conversational_turn()

        Returns:
            Formatted explanation string
        """
        lines = []
        lines.append("=" * 60)
        lines.append("SELF-LED CASCADE STATE")
        lines.append("=" * 60)
        lines.append("")

        # Gate 1: Safety
        lines.append("Gate 1: SAFETY CHECK")
        lines.append("-" * 60)
        lines.append(f"  Safety Level: {state.safety_level.value}")
        lines.append(f"  OFEL Energy: {state.ofel.field:.3f}")
        lines.append(f"  Polyvagal State: {state.polyvagal.dominant_state} ({state.polyvagal.confidence:.3f})")
        if 'Gate 1 (Safety)' in state.gate_modulations:
            lines.append(f"  BAGUA Modulation: {state.gate_modulations['Gate 1 (Safety)']}")
        lines.append("")

        # Gate 2: Coherence
        lines.append("Gate 2: COHERENCE CHECK")
        lines.append("-" * 60)
        lines.append(f"  Organ Coherence: {state.organ_coherence:.3f}")
        lines.append(f"  Organ Agreement:")
        for organ, coherence in state.organ_agreement.items():
            lines.append(f"    {organ}: {coherence:.3f}")
        if 'Gate 2 (Coherence)' in state.gate_modulations:
            lines.append(f"  BAGUA Modulation: {state.gate_modulations['Gate 2 (Coherence)']}")
        lines.append("")

        # Gate 3: SELF-Energy
        if state.self_energy:
            lines.append("Gate 3: SELF-ENERGY CHECK")
            lines.append("-" * 60)
            lines.append(f"  SELF-Energy: {state.self_energy.self_energy:.3f}")
            lines.append(f"  SELF-Distance: {state.self_energy.self_distance:.3f}")
            lines.append(f"  Dominant C: {state.self_energy.dominant_c}")
            lines.append(f"  8 C's Activation:")
            for c_name, activation in state.self_energy.cs_activation.items():
                lines.append(f"    {c_name}: {activation:.3f}")
            lines.append(f"  Confidence: {state.self_energy.confidence:.3f}")
            lines.append(f"  SELF-Led: {state.self_led}")
            if 'Gate 3 (SELF-Energy)' in state.gate_modulations:
                lines.append(f"  BAGUA Modulation: {state.gate_modulations['Gate 3 (SELF-Energy)']}")
            lines.append("")

        # Gate 4: Response
        lines.append("Gate 4: RESPONSE GENERATION")
        lines.append("-" * 60)
        lines.append(f"  Response: {state.response_text}")
        lines.append(f"  Quality: {state.response_quality}")
        if 'Gate 4 (Response)' in state.gate_modulations:
            lines.append(f"  BAGUA Modulation: {state.gate_modulations['Gate 4 (Response)']}")
        lines.append("")

        # Decision Path
        lines.append("DECISION PATH")
        lines.append("-" * 60)
        for gate_name, decision in state.decision_path:
            lines.append(f"  {gate_name} → {decision.value}")
        lines.append("")

        # BAGUA Context
        lines.append("BAGUA CONTEXT")
        lines.append("-" * 60)
        for dim_name, activation in state.bagua_context.items():
            lines.append(f"  {dim_name}: {activation:.3f}")
        lines.append("")

        lines.append("=" * 60)

        return "\n".join(lines)


# Quick utility functions
def quick_cascade_check(text: str, organism_context: Dict[str, Any]) -> str:
    """
    Quick cascade check (convenience function).

    Args:
        text: User input text
        organism_context: Organism processing context

    Returns:
        Response text from cascade

    Example:
        >>> response = quick_cascade_check(
        ...     "I feel overwhelmed by this critical part.",
        ...     organism_context
        ... )
        >>> print(response)
        "I'm curious about what this critical part needs right now."
    """
    cascade = SELFLedCascade()
    state = cascade.process_conversational_turn(text, organism_context)
    return state.response_text
