"""
SELF Matrix Governance - Trauma-Informed Emission Layer
=========================================================

Implements 5-zone trauma-informed governance for therapeutic appropriateness.

Purpose:
- Map BOND self_distance to 5 SELF zones (IFS-based)
- Select zone-appropriate lures (coherent attractors)
- Enforce safety principles per zone
- Integration with Polyvagal Theory + van der Kolk body-based work

Philosophy:
- SELF-energy access determines therapeutic capacity
- Safety first, insight later (or never)
- Window of tolerance respected
- No demand for performance

Integration Points:
- Called by OrganReconstructionPipeline
- Works with EmissionGenerator for final lure selection
- Uses BOND organ (self_distance) and EO organ (polyvagal_state)

Date: November 12, 2025
Status: Phase A - SELF Matrix Implementation
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass


@dataclass
class SELFZoneState:
    """
    SELF Matrix zone state for trauma-informed governance.

    Represents the current SELF-energy access level and therapeutic capacity.
    Based on IFS (Internal Family Systems) + Polyvagal Theory.
    """
    zone_id: int                        # 1-5
    zone_name: str                      # "Core SELF Orbit", "Inner Relational", etc.
    self_distance: float                # From BOND organ (0.0-1.0)
    self_distance_range: Tuple[float, float]  # Zone boundaries
    polyvagal_state: str                # From EO organ
    therapeutic_stance: str             # "Witnessing", "Relational", "Creative", "Protective", "Minimal"
    safety_principles: List[str]        # Zone-specific constraints
    exploration_permitted: bool         # Can we explore deeper material?
    inquiry_permitted: bool             # Can we ask open questions?
    interpretation_permitted: bool      # Can we offer insights?
    minimal_only: bool                  # Only minimal presence?


class SELFMatrixGovernance:
    """
    Trauma-informed emission governance via 5 SELF zones.

    Maps BOND self_distance to IFS-based zones, ensuring emissions are
    therapeutically appropriate for the person's current nervous system state.

    Architecture:
    - Zone 1 (0.00-0.15): Core SELF Orbit - Full SELF-energy access
    - Zone 2 (0.15-0.25): Inner Relational - Managers present, relational capacity
    - Zone 3 (0.25-0.35): Symbolic Threshold - Parts negotiating, creative tension
    - Zone 4 (0.35-0.60): Shadow/Compost - Firefighters active, protective only
    - Zone 5 (0.60-1.00): Exile/Collapse - Dorsal vagal, minimal presence only

    Integration with Polyvagal Theory (van der Kolk):
    - Zone 1-2: Ventral vagal (safe and social)
    - Zone 3: Mixed state (mobilization with connection)
    - Zone 4: Sympathetic (fight/flight activation)
    - Zone 5: Dorsal vagal (freeze/collapse)
    """

    def __init__(self, coherent_attractors_path: str):
        """
        Initialize SELF matrix governance.

        Args:
            coherent_attractors_path: Path to coherent_attractors.json
                Contains validated lures by zone × mechanism × intensity
        """
        self.coherent_attractors_path = Path(coherent_attractors_path)

        # Zone boundaries (self_distance ranges)
        self.zone_boundaries = [
            (0.00, 0.15),  # Zone 1: Core SELF Orbit
            (0.15, 0.25),  # Zone 2: Inner Relational
            (0.25, 0.35),  # Zone 3: Symbolic Threshold
            (0.35, 0.60),  # Zone 4: Shadow/Compost
            (0.60, 1.00),  # Zone 5: Exile/Collapse
        ]

        # Zone names
        self.zone_names = [
            "Core SELF Orbit",
            "Inner Relational",
            "Symbolic Threshold",
            "Shadow/Compost",
            "Exile/Collapse"
        ]

        # Therapeutic stances by zone
        self.therapeutic_stances = [
            "witnessing",      # Zone 1: Open inquiry, naming emergence
            "relational",      # Zone 2: Empathic reflection, co-regulation
            "creative",        # Zone 3: Pattern recognition, transformation
            "protective",      # Zone 4: Grounding, validation (NO exploration)
            "minimal"          # Zone 5: Body-based safety, presence ONLY
        ]

        # Load coherent attractors (validated lures)
        self.coherent_attractors = self._load_coherent_attractors()

        print(f"✅ SELF Matrix Governance initialized")
        print(f"   Zones: 5 (Core SELF → Exile/Collapse)")
        print(f"   Attractors loaded: {len(self.coherent_attractors)} zones")

    def _load_coherent_attractors(self) -> Dict[str, Any]:
        """
        Load coherent attractors (validated lures) from JSON.

        Returns:
            Dictionary of zone → mechanisms → intensities → lures
        """
        if not self.coherent_attractors_path.exists():
            print(f"⚠️  Coherent attractors not found at {self.coherent_attractors_path}")
            return {}

        try:
            with open(self.coherent_attractors_path, 'r') as f:
                attractors = json.load(f)

            print(f"   Loaded coherent attractors from {self.coherent_attractors_path.name}")
            return attractors

        except Exception as e:
            print(f"⚠️  Error loading coherent attractors: {e}")
            return {}

    def classify_zone(
        self,
        bond_self_distance: float,
        eo_polyvagal_state: str
    ) -> SELFZoneState:
        """
        Map BOND self_distance → 5 trauma-informed zones.

        Args:
            bond_self_distance: Self-distance from BOND organ (0.0-1.0)
                - 0.0 = Full SELF-energy access
                - 1.0 = Complete parts takeover (exiles/collapse)
            eo_polyvagal_state: Polyvagal state from EO organ
                - "ventral_vagal", "sympathetic", "dorsal_vagal", "mixed_state"

        Returns:
            SELFZoneState with zone classification and safety permissions
        """
        # Clamp self_distance to valid range
        bond_self_distance = max(0.0, min(1.0, bond_self_distance))

        # Determine zone based on boundaries
        zone_id = 1
        for i, (low, high) in enumerate(self.zone_boundaries):
            if low <= bond_self_distance < high:
                zone_id = i + 1
                break

        # Handle edge case (self_distance = 1.0 exactly)
        if bond_self_distance == 1.0:
            zone_id = 5

        # Get zone info
        zone_name = self.zone_names[zone_id - 1]
        stance = self.therapeutic_stances[zone_id - 1]
        self_distance_range = self.zone_boundaries[zone_id - 1]

        # Define safety principles by zone
        if zone_id == 1:  # Core SELF Orbit
            safety_principles = [
                "Open inquiry permitted",
                "Naming emergence allowed",
                "Spacious presence available",
                "Full exploration capacity"
            ]
            exploration_permitted = True
            inquiry_permitted = True
            interpretation_permitted = True
            minimal_only = False

        elif zone_id == 2:  # Inner Relational
            safety_principles = [
                "Empathic reflection safe",
                "Somatic tracking encouraged",
                "Co-regulation available",
                "Relational witnessing permitted"
            ]
            exploration_permitted = True
            inquiry_permitted = True
            interpretation_permitted = True
            minimal_only = False

        elif zone_id == 3:  # Symbolic Threshold
            safety_principles = [
                "Pattern recognition permitted",
                "Transformation language allowed",
                "Parts language safe",
                "Creative tension workable"
            ]
            exploration_permitted = True
            inquiry_permitted = True
            interpretation_permitted = True  # With care
            minimal_only = False

        elif zone_id == 4:  # Shadow/Compost
            safety_principles = [
                "NO exploration of deeper material",
                "YES validation of protective strategies",
                "YES grounding/somatic anchoring",
                "NO interpretation or insight-seeking",
                "Firefighters respected"
            ]
            exploration_permitted = False
            inquiry_permitted = False  # Open questions risky
            interpretation_permitted = False
            minimal_only = False

        else:  # Zone 5: Exile/Collapse
            safety_principles = [
                "NO content delivery",
                "YES minimal presence only",
                "YES body-based safety anchors",
                "NO cognitive processing demands",
                "Dorsal vagal state honored"
            ]
            exploration_permitted = False
            inquiry_permitted = False
            interpretation_permitted = False
            minimal_only = True

        return SELFZoneState(
            zone_id=zone_id,
            zone_name=zone_name,
            self_distance=bond_self_distance,
            self_distance_range=self_distance_range,
            polyvagal_state=eo_polyvagal_state,
            therapeutic_stance=stance,
            safety_principles=safety_principles,
            exploration_permitted=exploration_permitted,
            inquiry_permitted=inquiry_permitted,
            interpretation_permitted=interpretation_permitted,
            minimal_only=minimal_only
        )

    def select_zone_appropriate_lure(
        self,
        zone: SELFZoneState,
        transduction_mechanism: Optional[str] = None,
        nexus_type: Optional[str] = None,
        intensity: str = "medium",
        prefer_variety: bool = True
    ) -> Optional[str]:
        """
        Select coherent attractor (lure) appropriate for zone + mechanism.

        Two-Level Governance:
        1. Transduction mechanism suggests transformation strategy
        2. SELF zone enforces safety constraints

        Example:
            Mechanism: "salience_recalibration" (Urgency → Relational)
            Zone: Shadow/Compost (firefighters active)
            Result: Override to protective grounding
            Lure: "I see how hard you're working to stay safe. Let's pause."

        Args:
            zone: SELFZoneState from classify_zone()
            transduction_mechanism: Optional mechanism name (e.g., "salience_recalibration")
            nexus_type: Optional current nexus type (e.g., "Urgency")
            intensity: "low", "medium", or "high"
            prefer_variety: Rotate through available lures

        Returns:
            Selected lure string, or None if no attractors available
        """
        if not self.coherent_attractors:
            return None

        # Map zone to attractor key
        zone_key_map = {
            "Core SELF Orbit": "core_self_orbit",
            "Inner Relational": "inner_relational",
            "Symbolic Threshold": "symbolic_threshold",
            "Shadow/Compost": "shadow_compost",
            "Exile/Collapse": "exile_collapse"
        }

        zone_key = zone_key_map.get(zone.zone_name)
        if not zone_key or zone_key not in self.coherent_attractors:
            return None

        zone_attractors = self.coherent_attractors[zone_key]

        # Get lures by mechanism (if specified)
        if transduction_mechanism and 'lures_by_mechanism' in zone_attractors:
            mechanism_lures = zone_attractors['lures_by_mechanism'].get(transduction_mechanism)

            if mechanism_lures:
                # Check if intensities specified
                if isinstance(mechanism_lures, dict):
                    # Intensity-based lures
                    lures = mechanism_lures.get(intensity, mechanism_lures.get('medium', []))
                else:
                    # Flat list
                    lures = mechanism_lures

                if lures:
                    import random
                    return random.choice(lures)

        # Fallback: General zone lures (if available)
        if 'general_lures' in zone_attractors:
            general = zone_attractors['general_lures']

            if isinstance(general, dict):
                lures = general.get(intensity, general.get('medium', []))
            else:
                lures = general

            if lures:
                import random
                return random.choice(lures)

        # Final fallback: Any lures from lures_by_mechanism
        if 'lures_by_mechanism' in zone_attractors:
            all_mechanism_lures = []
            for mech_lures in zone_attractors['lures_by_mechanism'].values():
                if isinstance(mech_lures, dict):
                    # Flatten intensity-based lures
                    for intensity_lures in mech_lures.values():
                        all_mechanism_lures.extend(intensity_lures)
                else:
                    all_mechanism_lures.extend(mech_lures)

            if all_mechanism_lures:
                import random
                return random.choice(all_mechanism_lures)

        return None

    def enforce_safety_principles(
        self,
        zone: SELFZoneState,
        proposed_emission: str,
        transduction_mechanism: Optional[str] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate emission against zone safety principles.

        Ensures emissions are therapeutically appropriate for nervous system state.

        Zone 4 Principles:
        - NO exploration of deeper material
        - YES validation of protective strategies
        - YES grounding/somatic anchoring

        Zone 5 Principles:
        - NO content delivery
        - YES minimal presence
        - YES body-based safety only

        Args:
            zone: SELFZoneState
            proposed_emission: Emission text to validate
            transduction_mechanism: Optional mechanism (for context)

        Returns:
            (is_safe, reason_if_unsafe)
                - is_safe: True if passes safety check
                - reason_if_unsafe: Explanation if blocked
        """
        emission_lower = proposed_emission.lower()

        # Zone 5: Exile/Collapse - STRICTEST
        if zone.zone_id == 5:
            # Only minimal presence permitted
            unsafe_patterns = [
                ('what', 'Open questions not safe in collapse'),
                ('why', 'Open questions not safe in collapse'),
                ('how', 'Open questions not safe in collapse'),
                ('notice', 'Cognitive noticing too demanding'),
                ('feel', 'Feeling questions too demanding'),
                ('sense', 'Sensing questions too demanding'),
                ('explore', 'Exploration forbidden in collapse'),
            ]

            for pattern, reason in unsafe_patterns:
                if pattern in emission_lower:
                    return False, f"Zone 5 violation: {reason}"

            # Must be minimal presence
            safe_patterns = ["i'm here", "you're safe", "feel your", "breathe", "ground"]
            if not any(pattern in emission_lower for pattern in safe_patterns):
                return False, "Zone 5 requires minimal presence only (body-based safety)"

            return True, None

        # Zone 4: Shadow/Compost - PROTECTIVE ONLY
        elif zone.zone_id == 4:
            # NO exploration, NO interpretation
            unsafe_patterns = [
                ('deeper', 'Exploration forbidden in protective zone'),
                ('underneath', 'Exploration forbidden in protective zone'),
                ('really', 'Interpretation forbidden in protective zone'),
                ('actually', 'Interpretation forbidden in protective zone'),
                ('what if', 'Hypotheticals too activating'),
                ('imagine', 'Imagination too activating'),
            ]

            for pattern, reason in unsafe_patterns:
                if pattern in emission_lower:
                    return False, f"Zone 4 violation: {reason}"

            # Should emphasize safety, grounding, protection
            safe_patterns = ["safe", "ground", "pause", "slow", "breath", "here", "with you"]
            protective_patterns = ["protect", "boundary", "need", "working hard"]

            has_safety = any(pattern in emission_lower for pattern in safe_patterns)
            has_protection = any(pattern in emission_lower for pattern in protective_patterns)

            if not (has_safety or has_protection):
                return False, "Zone 4 requires grounding/protective language"

            return True, None

        # Zone 3: Symbolic Threshold - CAREFUL
        elif zone.zone_id == 3:
            # Interpretation permitted but with care
            # Avoid overly direct/confrontational language
            unsafe_patterns = [
                ('you should', 'Directive language inappropriate'),
                ('you must', 'Directive language inappropriate'),
                ('you need to', 'Directive language inappropriate'),
            ]

            for pattern, reason in unsafe_patterns:
                if pattern in emission_lower:
                    return False, f"Zone 3 caution: {reason}"

            return True, None

        # Zone 1-2: Core SELF / Inner Relational - OPEN
        else:
            # Minimal constraints - full exploration capacity
            # Only check for obviously harmful patterns
            unsafe_patterns = [
                ('you\'re wrong', 'Judgment inappropriate'),
                ('that\'s bad', 'Judgment inappropriate'),
                ('you failed', 'Shame-inducing'),
            ]

            for pattern, reason in unsafe_patterns:
                if pattern in emission_lower:
                    return False, f"Zone {zone.zone_id} caution: {reason}"

            return True, None

    def get_zone_description(self, zone: SELFZoneState) -> str:
        """
        Get human-readable zone description.

        Args:
            zone: SELFZoneState

        Returns:
            Description string with zone characteristics
        """
        polyvagal_map = {
            'ventral_vagal': 'Safe and social',
            'sympathetic': 'Mobilized (fight/flight)',
            'dorsal_vagal': 'Immobilized (freeze/collapse)',
            'mixed_state': 'Mixed activation'
        }

        polyvagal_desc = polyvagal_map.get(zone.polyvagal_state, zone.polyvagal_state)

        return (
            f"Zone {zone.zone_id}: {zone.zone_name}\n"
            f"  Self-distance: {zone.self_distance:.3f} (range: {zone.self_distance_range[0]:.2f}-{zone.self_distance_range[1]:.2f})\n"
            f"  Polyvagal: {polyvagal_desc}\n"
            f"  Stance: {zone.therapeutic_stance}\n"
            f"  Exploration: {'Yes' if zone.exploration_permitted else 'No'}\n"
            f"  Inquiry: {'Yes' if zone.inquiry_permitted else 'No'}\n"
            f"  Interpretation: {'Yes' if zone.interpretation_permitted else 'No'}\n"
            f"  Minimal only: {'Yes' if zone.minimal_only else 'No'}"
        )

    def override_for_crisis(
        self,
        zone: SELFZoneState,
        ndam_urgency: float,
        transduction_mechanism: Optional[str] = None
    ) -> Optional[str]:
        """
        Crisis override: Generate minimal safe emission for high urgency.

        When NDAM urgency is very high (>0.8), override normal zone logic
        and provide immediate grounding/safety.

        Args:
            zone: Current SELFZoneState
            ndam_urgency: Urgency level from NDAM organ (0-1)
            transduction_mechanism: Current transduction mechanism

        Returns:
            Crisis-appropriate minimal emission, or None if not in crisis
        """
        if ndam_urgency < 0.8:
            return None  # Not in crisis

        # High urgency detected - minimal safe grounding
        crisis_lures = [
            "I'm here with you",
            "Let's pause for just a moment",
            "Can we take one breath together?",
            "You're safe right now",
            "I'm not going anywhere",
            "Feel your feet on the ground"
        ]

        import random
        return random.choice(crisis_lures)


def test_self_matrix_governance():
    """
    Test SELF matrix governance classification and safety enforcement.
    """
    print("\n" + "="*70)
    print("Testing SELF Matrix Governance")
    print("="*70 + "\n")

    # Create governance (without coherent attractors for now)
    governance = SELFMatrixGovernance(
        coherent_attractors_path="persona_layer/config/symbols/coherent_attractors.json"
    )

    # Test zone classification
    test_cases = [
        (0.05, "ventral_vagal", "Zone 1: Core SELF Orbit"),
        (0.20, "ventral_vagal", "Zone 2: Inner Relational"),
        (0.30, "mixed_state", "Zone 3: Symbolic Threshold"),
        (0.45, "sympathetic", "Zone 4: Shadow/Compost"),
        (0.75, "dorsal_vagal", "Zone 5: Exile/Collapse"),
    ]

    print("Zone Classification Tests:")
    print("-" * 70)

    for self_distance, polyvagal, expected_zone in test_cases:
        zone = governance.classify_zone(self_distance, polyvagal)

        passed = zone.zone_name in expected_zone
        status = "✅" if passed else "❌"

        print(f"{status} self_distance={self_distance:.2f}, polyvagal={polyvagal}")
        print(f"   Result: {zone.zone_name} (Zone {zone.zone_id})")
        print(f"   Stance: {zone.therapeutic_stance}")
        print(f"   Exploration: {zone.exploration_permitted}, Inquiry: {zone.inquiry_permitted}")
        print()

    # Test safety enforcement
    print("\nSafety Enforcement Tests:")
    print("-" * 70)

    # Zone 5: Should block exploration
    zone5 = governance.classify_zone(0.75, "dorsal_vagal")
    is_safe, reason = governance.enforce_safety_principles(
        zone5,
        "What are you feeling underneath this?"
    )
    print(f"Zone 5 + exploratory question: {'❌ BLOCKED' if not is_safe else '✅ ALLOWED'}")
    if not is_safe:
        print(f"   Reason: {reason}")
    print()

    # Zone 5: Should allow minimal presence
    is_safe, reason = governance.enforce_safety_principles(
        zone5,
        "I'm here with you"
    )
    print(f"Zone 5 + minimal presence: {'✅ ALLOWED' if is_safe else '❌ BLOCKED'}")
    print()

    # Zone 4: Should block deeper exploration
    zone4 = governance.classify_zone(0.45, "sympathetic")
    is_safe, reason = governance.enforce_safety_principles(
        zone4,
        "Let's explore what's deeper underneath this"
    )
    print(f"Zone 4 + deeper exploration: {'❌ BLOCKED' if not is_safe else '✅ ALLOWED'}")
    if not is_safe:
        print(f"   Reason: {reason}")
    print()

    # Zone 4: Should allow grounding
    is_safe, reason = governance.enforce_safety_principles(
        zone4,
        "Let's pause and find some ground here"
    )
    print(f"Zone 4 + grounding: {'✅ ALLOWED' if is_safe else '❌ BLOCKED'}")
    print()

    # Zone 1: Should allow open inquiry
    zone1 = governance.classify_zone(0.05, "ventral_vagal")
    is_safe, reason = governance.enforce_safety_principles(
        zone1,
        "What's emerging for you in this spaciousness?"
    )
    print(f"Zone 1 + open inquiry: {'✅ ALLOWED' if is_safe else '❌ BLOCKED'}")
    print()

    print("="*70)
    print("SELF Matrix Governance Test Complete")
    print("="*70 + "\n")


if __name__ == "__main__":
    # Run tests
    test_self_matrix_governance()
