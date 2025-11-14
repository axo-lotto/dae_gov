"""
Conversational Salience Model - Standalone implementation for DAE_HYPHAE_1
Self-contained salience model adapted for therapeutic conversation context.

STANDALONE: No external dependencies on DAE 3.0 AXO ARC.

Key adaptations:
- Emphasizes trauma-aware process terms (signal_inflation, temporal_collapse, safety_gradient)
- Domain terms focused on semantic coherence and transformation readiness
- Custom calculation methods for conversational context (organ coherences, meta-atoms, nexuses)

Based on DAE 3.0 salience model concepts but reimplemented for independence.
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import numpy as np


@dataclass
class SalienceTerm:
    """Individual salience term with its properties"""
    name: str
    value: float
    weight: float = 1.0
    active: bool = True
    category: str = "process"  # "process" or "domain"


class ConversationalSalienceModel:
    """
    STANDALONE salience model for therapeutic conversation context.

    Profile: "conversation" (DAE_HYPHAE_1 native)

    Emphasis:
    - HIGH: Trauma-aware process terms (signal_inflation, temporal_collapse, safety_gradient)
    - MEDIUM: Integration process terms (field_resonance_threshold, ethical_salience_field)
    - HIGH: Domain terms for semantic coherence (semantic_intensity, transformation_readiness)

    Conversational Context:
    - prehension["organ_coherences"]: Dict[organ_name, coherence] (0.0-1.0)
    - prehension["meta_atoms"]: Dict[atom_name, activation] (0.0-1.0)
    - prehension["nexuses"]: List of nexus objects
    - prehension["v0_energy"]: Current V0 appetition (0.0-1.0)
    - prehension["cycle"]: Current convergence cycle (1-5)
    - prehension["kairos_detected"]: Boolean Kairos moment flag
    """

    # 10 Process Philosophy Terms (Core)
    PROCESS_TERMS = [
        "salience_drift", "lure_hysteresis", "concrescent_drift",
        "signal_inflation", "temporal_collapse", "attunement_delta",
        "field_resonance_threshold", "relational_recurrence",
        "safety_gradient", "ethical_salience_field"
    ]

    # 10 Domain Terms (Auxiliary)
    DOMAIN_TERMS = [
        "semantic_intensity", "spatial_coherence", "temporal_recurrence",
        "constraint_pressure", "emergence_potential", "relational_density",
        "transformation_readiness", "archetypal_resonance",
        "coherence_gradient", "satisfaction_proximity"
    ]

    def __init__(self):
        """Initialize standalone conversation profile"""
        self.profile = "conversation"
        self.terms: Dict[str, SalienceTerm] = {}
        self.salience_history: List[Dict] = []

        # Thresholds for morphogenetic pressure
        self.field_resonance_threshold = 0.6
        self.morphogenetic_threshold = 0.7
        self.crystallization_threshold = 0.85

        # Initialize terms
        self._initialize_terms()

        # Configure weights for conversation profile
        self.configure_profile()

        # Profile blend (70% process, 30% domain for conversation)
        self.process_weight = 0.7
        self.domain_weight = 0.3

    def _initialize_terms(self):
        """Initialize all salience terms with default values"""
        # Process terms
        for term_name in self.PROCESS_TERMS:
            self.terms[term_name] = SalienceTerm(
                name=term_name,
                value=0.0,
                weight=1.0,
                active=True,
                category="process"
            )

        # Domain terms
        for term_name in self.DOMAIN_TERMS:
            self.terms[term_name] = SalienceTerm(
                name=term_name,
                value=0.0,
                weight=0.5,
                active=True,
                category="domain"
            )

    def _calculate_category_salience(self, category: str) -> float:
        """Calculate weighted salience for a category of terms"""
        total = 0.0
        weight_sum = 0.0

        for term in self.terms.values():
            if term.category == category and term.active:
                total += term.value * term.weight
                weight_sum += term.weight

        if weight_sum == 0:
            return 0.0

        return total / weight_sum

    def calculate_morphogenetic_pressure(self, total_salience: float) -> float:
        """Calculate pressure for boundary formation"""
        if total_salience < self.field_resonance_threshold:
            return 0.0
        elif total_salience < self.morphogenetic_threshold:
            return (total_salience - self.field_resonance_threshold) / \
                   (self.morphogenetic_threshold - self.field_resonance_threshold)
        elif total_salience < self.crystallization_threshold:
            return 0.5 + 0.5 * (total_salience - self.morphogenetic_threshold) / \
                   (self.crystallization_threshold - self.morphogenetic_threshold)
        else:
            return 1.0

    def configure_profile(self):
        """Configure weights for conversational therapy context"""

        # PROCESS TERMS (Version 2 - Core)
        # HIGH: Trauma-aware terms (critical for therapeutic safety)
        process_weights = {
            "signal_inflation": 2.5,           # BOND/EO firefighter detection (highest priority)
            "temporal_collapse": 2.0,          # Past trauma bleeding into present moment
            "safety_gradient": 2.5,            # How much truth can be felt safely (critical)

            # MEDIUM: Integration terms (guide pattern formation)
            "field_resonance_threshold": 1.5,  # When patterns stabilize (nexus formation)
            "ethical_salience_field": 1.5,     # What matters across conversation
            "relational_recurrence": 1.3,      # Healing spirals in conversation

            # LOW: Developmental terms (less relevant for real-time conversation)
            "attunement_delta": 1.0,           # Accuracy of organ sensing
            "lure_hysteresis": 0.8,            # Less relevant (no explicit future in text)
            "salience_drift": 0.7,             # Long-term not applicable in single conv
            "concrescent_drift": 0.6           # Micro-misalignments (tracked by V0)
        }

        # DOMAIN TERMS (Version 1 - Auxiliary)
        # HIGH: Semantic and transformation terms
        domain_weights = {
            "semantic_intensity": 1.8,         # How meaningful/important (meta-atom activation)
            "transformation_readiness": 1.8,   # Capacity for change (V0 descent)
            "satisfaction_proximity": 1.5,     # Convergence closeness (Kairos)

            # MEDIUM: Relational and coherence terms
            "coherence_gradient": 1.3,         # Direction toward coherence (organ agreement)
            "relational_density": 1.0,         # Connection richness (nexus count)
            "emergence_potential": 1.0,        # Novelty (new meta-atom combinations)

            # LOW: Spatial/temporal (less applicable to text)
            "spatial_coherence": 0.5,          # Not spatial (linear text)
            "temporal_recurrence": 0.8,        # Pattern repetition (less critical)
            "constraint_pressure": 0.7,        # Boundary formation (defer to morphogenetic)
            "archetypal_resonance": 0.6        # Eternal forms (tracked by meta-atoms)
        }

        # Apply weights
        for term_name, weight in process_weights.items():
            if term_name in self.terms:
                self.terms[term_name].weight = weight

        for term_name, weight in domain_weights.items():
            if term_name in self.terms:
                self.terms[term_name].weight = weight

        # Adjust profile blend (70% process, 30% domain for conversation)
        self.process_weight = 0.7
        self.domain_weight = 0.3

    def evaluate(self, prehension: Dict[str, Any], adapter_profile: Optional[str] = None) -> Dict[str, Any]:
        """
        Evaluate salience for conversational prehension.

        Expected prehension structure:
        {
            "organ_coherences": {"BOND": 0.72, "EO": 0.65, ...},
            "meta_atoms": {"trauma_aware": 0.82, "safety_restoration": 0.45, ...},
            "nexuses": [nexus1, nexus2, ...],
            "v0_energy": 0.45,
            "cycle": 2,
            "kairos_detected": False,
            "satisfaction": 0.85,
            "text": "I feel completely overwhelmed..."
        }
        """
        # Use conversation profile (don't override)
        if adapter_profile and adapter_profile != "conversation":
            print(f"Warning: ConversationalSalienceModel designed for 'conversation' profile, ignoring '{adapter_profile}'")

        # Reset term values
        for term in self.terms.values():
            term.value = 0.0

        # Calculate process philosophy terms (adapted for conversation)
        self._calculate_conversational_process_terms(prehension)

        # Calculate domain-specific terms (adapted for conversation)
        self._calculate_conversational_domain_terms(prehension)

        # Calculate integrated salience scores
        process_salience = self._calculate_category_salience("process")
        domain_salience = self._calculate_category_salience("domain")

        # Weight based on conversation profile (70% process, 30% domain)
        total_salience = process_salience * self.process_weight + domain_salience * self.domain_weight

        # Determine morphogenetic pressure
        morphogenetic_pressure = self.calculate_morphogenetic_pressure(total_salience)

        # Package results
        results = {
            "total": total_salience,
            "process_salience": process_salience,
            "domain_salience": domain_salience,
            "morphogenetic_pressure": morphogenetic_pressure,
            "process_terms": {
                term.name: term.value
                for term in self.terms.values()
                if term.category == "process"
            },
            "domain_terms": {
                term.name: term.value
                for term in self.terms.values()
                if term.category == "domain"
            },
            "active_terms": [
                term.name for term in self.terms.values()
                if term.active and term.value > 0.3
            ],
            "profile": "conversation",
            "trauma_markers": self._extract_trauma_markers(prehension),
            "morphogenetic_guidance": self._get_conversational_guidance(morphogenetic_pressure)
        }

        # Record in history
        self.salience_history.append(results)

        return results

    def _calculate_conversational_process_terms(self, prehension: Dict[str, Any]):
        """Calculate 10 process philosophy terms adapted for conversation"""

        organ_coherences = prehension.get("organ_coherences", {})
        meta_atoms = prehension.get("meta_atoms", {})
        nexuses = prehension.get("nexuses", [])
        v0_energy = prehension.get("v0_energy", 0.5)
        cycle = prehension.get("cycle", 1)
        satisfaction = prehension.get("satisfaction", 0.5)

        # 1. Salience Drift - Long-term deviation (use conversation cycles)
        if len(self.salience_history) > 2:
            recent_avg = np.mean([h["total"] for h in self.salience_history[-3:]])
            early_avg = self.salience_history[0]["total"] if self.salience_history else 0.5
            drift = abs(recent_avg - early_avg)
            self.terms["salience_drift"].value = min(1.0, drift * 1.5)
        else:
            self.terms["salience_drift"].value = 0.1

        # 2. Lure Hysteresis - Delay between feeling and moving
        # In conversation: V0 energy vs satisfaction (high V0 + low satisfaction = high hysteresis)
        if v0_energy > 0.5 and satisfaction < 0.5:
            gap = v0_energy - satisfaction
            self.terms["lure_hysteresis"].value = max(0, min(1.0, gap * 2))
        else:
            self.terms["lure_hysteresis"].value = 0.2

        # 3. Concrescent Drift - Misalignment in organ becomings
        if organ_coherences:
            coherence_values = list(organ_coherences.values())
            variance = np.var(coherence_values)
            # High variance = high drift
            self.terms["concrescent_drift"].value = min(1.0, variance * 4)
        else:
            self.terms["concrescent_drift"].value = 0.3

        # 4. Signal Inflation - CRITICAL: Trauma response amplification
        # 🆕 FIX 2: Use BOND self_distance as PRIMARY trauma metric (SELF matrix alignment)
        #
        # SELF Matrix Zones (from SELF_MATRIX.MD):
        # - Core SELF Orbit:     [0.00, 0.15]  → MINIMAL trauma (SELF-led)
        # - Inner Relational:    [0.15, 0.25]  → LOW trauma (relational, empathy)
        # - Symbolic Threshold:  [0.25, 0.35]  → LOW trauma (creative work, NOT pathology!)
        # - Shadow/Compost:      [0.35, 0.60]  → MODERATE trauma (protective parts, burnout)
        # - Exile/Collapse:      [0.60, 1.00]  → HIGH trauma (deep exile, crisis)

        bond_self_distance = prehension.get("bond_self_distance", 0.5)

        # Map SELF-distance zones to signal inflation (base trauma level)
        if bond_self_distance >= 0.6:
            # Exile/Collapse zone (0.6-1.0) → HIGH trauma
            base_inflation = 0.7 + (bond_self_distance - 0.6) * 0.75  # 0.70-1.00
        elif bond_self_distance >= 0.35:
            # Shadow/Compost zone (0.35-0.6) → MODERATE trauma
            base_inflation = 0.4 + (bond_self_distance - 0.35) * 1.2  # 0.40-0.70
        elif bond_self_distance >= 0.25:
            # Symbolic Threshold (0.25-0.35) → LOW (creative, not pathological!)
            base_inflation = 0.1 + (bond_self_distance - 0.25) * 3.0  # 0.10-0.40
        elif bond_self_distance >= 0.15:
            # Inner Relational (0.15-0.25) → MINIMAL
            base_inflation = 0.05 + (bond_self_distance - 0.15) * 0.5  # 0.05-0.10
        else:
            # Core SELF Orbit (0.0-0.15) → MINIMAL (SELF-led, safe)
            base_inflation = bond_self_distance * 0.33  # 0.00-0.05

        # MODULATE with polyvagal state (nervous system amplifies/reduces trauma perception)
        eo_polyvagal = prehension.get("eo_polyvagal_state", "mixed_state")
        if eo_polyvagal == "dorsal_vagal":
            # Shutdown state amplifies trauma perception
            base_inflation = min(1.0, base_inflation * 1.3)
        elif eo_polyvagal == "sympathetic":
            # Fight/flight slightly amplifies
            base_inflation = min(1.0, base_inflation * 1.1)
        elif eo_polyvagal == "ventral_vagal":
            # Safe & social reduces trauma perception
            base_inflation = base_inflation * 0.8

        # AMPLIFY with NDAM urgency (crisis urgency increases trauma salience)
        ndam_urgency = prehension.get("ndam_urgency_level", 0.0)
        if ndam_urgency > 0.7:
            # High urgency adds trauma signal
            base_inflation = min(1.0, base_inflation + (ndam_urgency - 0.7) * 0.5)

        self.terms["signal_inflation"].value = min(1.0, base_inflation)

        # 5. Temporal Collapse - Past mistaken for now
        # Detect via high BOND (exile patterns) + high EO (dorsal vagal collapse) + low RNX (temporal dysregulation)
        if organ_coherences:
            bond_high = organ_coherences.get("BOND", 0.0) > 0.6
            eo_high = organ_coherences.get("EO", 0.0) > 0.6
            rnx_low = organ_coherences.get("RNX", 0.5) < 0.4

            if bond_high and eo_high and rnx_low:
                self.terms["temporal_collapse"].value = 0.8
            elif bond_high and eo_high:
                self.terms["temporal_collapse"].value = 0.6
            elif len(self.salience_history) > 1:
                # Check for repeating meta-atom patterns (freeze response)
                current_atoms = set(meta_atoms.keys())
                prev_atoms = set(self.salience_history[-1].get("meta_atoms", {}).keys()) if self.salience_history else set()
                overlap = len(current_atoms & prev_atoms) / max(len(current_atoms), 1)
                self.terms["temporal_collapse"].value = overlap * 0.5
            else:
                self.terms["temporal_collapse"].value = 0.2
        else:
            self.terms["temporal_collapse"].value = 0.1

        # 6. Attunement Delta - Gap between felt and actual
        # Use organ coherence variance (high variance = poor attunement)
        if organ_coherences:
            coherence_values = list(organ_coherences.values())
            mean_coherence = np.mean(coherence_values)
            std_coherence = np.std(coherence_values)
            # High std = low attunement
            delta = std_coherence * 2
            self.terms["attunement_delta"].value = min(1.0, delta)
        else:
            self.terms["attunement_delta"].value = 0.5

        # 7. Field Resonance Threshold - Pattern stabilization
        # Use nexus count and meta-atom activation
        if nexuses:
            nexus_count = len(nexuses)
            # More nexuses = higher resonance
            resonance = min(1.0, nexus_count / 5.0)  # 5+ nexuses = full resonance
            if resonance > self.field_resonance_threshold:
                threshold_value = (resonance - self.field_resonance_threshold) / (1.0 - self.field_resonance_threshold)
                self.terms["field_resonance_threshold"].value = threshold_value
            else:
                self.terms["field_resonance_threshold"].value = 0.0
        else:
            self.terms["field_resonance_threshold"].value = 0.0

        # 8. Relational Recurrence - Healing spirals
        # Check for increasing satisfaction + decreasing V0 energy over cycles
        if len(self.salience_history) > 2:
            # Get satisfaction trajectory from history (if tracked)
            # For now, use V0 energy descent as proxy
            if cycle > 1:
                v0_prev = prehension.get("v0_energy_prev", v0_energy)
                satisfaction_prev = prehension.get("satisfaction_prev", satisfaction)

                # Healing spiral: satisfaction up, V0 down
                if satisfaction > satisfaction_prev and v0_energy < v0_prev:
                    self.terms["relational_recurrence"].value = 0.7
                elif satisfaction > satisfaction_prev or v0_energy < v0_prev:
                    self.terms["relational_recurrence"].value = 0.5
                else:
                    self.terms["relational_recurrence"].value = 0.2
            else:
                self.terms["relational_recurrence"].value = 0.3
        else:
            self.terms["relational_recurrence"].value = 0.3

        # 9. Safety Gradient - CRITICAL: How much truth can be felt safely
        # Inverse of signal_inflation and temporal_collapse
        signal_inflation = self.terms["signal_inflation"].value
        temporal_collapse = self.terms["temporal_collapse"].value

        safety = 1.0 - signal_inflation * 0.6
        safety *= (1.0 - temporal_collapse * 0.4)

        # Boost safety if window_of_tolerance meta-atom active
        if meta_atoms.get("window_of_tolerance", 0.0) > 0.5:
            safety = min(1.0, safety * 1.2)

        self.terms["safety_gradient"].value = max(0.1, safety)

        # 10. Ethical Salience Field - What matters across conversation
        # Combine field resonance, safety, and attunement
        ethical_importance = (
            self.terms["field_resonance_threshold"].value * 0.3 +
            (1.0 - self.terms["attunement_delta"].value) * 0.3 +
            self.terms["safety_gradient"].value * 0.4
        )
        self.terms["ethical_salience_field"].value = min(1.0, ethical_importance)

    def _calculate_conversational_domain_terms(self, prehension: Dict[str, Any]):
        """Calculate 10 domain terms adapted for conversation"""

        organ_coherences = prehension.get("organ_coherences", {})
        meta_atoms = prehension.get("meta_atoms", {})
        nexuses = prehension.get("nexuses", [])
        v0_energy = prehension.get("v0_energy", 0.5)
        satisfaction = prehension.get("satisfaction", 0.5)
        kairos_detected = prehension.get("kairos_detected", False)

        # 1. Semantic Intensity - How meaningful/important
        # Use meta-atom activation count and strength
        if meta_atoms:
            num_active = sum(1 for v in meta_atoms.values() if v > 0.3)
            max_activation = max(meta_atoms.values())
            intensity = (num_active / 10.0) * 0.5 + max_activation * 0.5
            self.terms["semantic_intensity"].value = min(1.0, intensity)
        else:
            self.terms["semantic_intensity"].value = 0.1

        # 2. Spatial Coherence - Pattern consistency (not spatial in text)
        # Use organ coherence consistency
        if organ_coherences:
            coherence_values = list(organ_coherences.values())
            mean_coherence = np.mean(coherence_values)
            std_coherence = np.std(coherence_values)
            # Low variance = high spatial coherence
            spatial = mean_coherence * (1.0 - std_coherence)
            self.terms["spatial_coherence"].value = min(1.0, spatial)
        else:
            self.terms["spatial_coherence"].value = 0.3

        # 3. Temporal Recurrence - Pattern repetition
        # Check meta-atom similarity across recent cycles
        if len(self.salience_history) > 1:
            # Get previous meta-atoms if available
            prev_meta = self.salience_history[-1].get("meta_atoms", {})
            if prev_meta and meta_atoms:
                overlap = set(meta_atoms.keys()) & set(prev_meta.keys())
                recurrence = len(overlap) / max(len(meta_atoms), 1)
                self.terms["temporal_recurrence"].value = recurrence * 0.8
            else:
                self.terms["temporal_recurrence"].value = 0.2
        else:
            self.terms["temporal_recurrence"].value = 0.2

        # 4. Constraint Pressure - Boundary formation
        # Use V0 energy (high V0 = high constraint need)
        pressure = v0_energy * 0.8
        self.terms["constraint_pressure"].value = pressure

        # 5. Emergence Potential - Novelty possibility
        semantic = self.terms["semantic_intensity"].value
        constraint = self.terms["constraint_pressure"].value
        # High semantic + low constraint = high emergence
        potential = semantic * (1.0 - constraint * 0.5)
        self.terms["emergence_potential"].value = potential

        # 6. Relational Density - Connection richness
        # Use nexus count
        if nexuses:
            nexus_count = len(nexuses)
            density = min(1.0, nexus_count / 8.0)  # 8+ nexuses = full density
            self.terms["relational_density"].value = density
        else:
            self.terms["relational_density"].value = 0.0

        # 7. Transformation Readiness - Capacity for change
        # High satisfaction + low V0 = ready for transformation
        emergence = self.terms["emergence_potential"].value
        readiness = satisfaction * (1.0 - v0_energy * 0.5) * (1.0 + emergence * 0.3)
        self.terms["transformation_readiness"].value = min(1.0, readiness)

        # 8. Archetypal Resonance - Connection to eternal forms
        # Use meta-atom activation (meta-atoms are archetypal patterns)
        if meta_atoms:
            archetypal_atoms = {"kairos_emergence", "coherence_integration", "somatic_wisdom", "ethical_salience_field"}
            archetypal_values = [meta_atoms.get(atom, 0.0) for atom in archetypal_atoms if atom in meta_atoms]
            if archetypal_values:
                resonance = max(archetypal_values)
                self.terms["archetypal_resonance"].value = resonance
            else:
                self.terms["archetypal_resonance"].value = 0.3
        else:
            self.terms["archetypal_resonance"].value = 0.3

        # 9. Coherence Gradient - Direction toward coherence
        # Use organ coherence trend (increasing = positive gradient)
        if organ_coherences:
            mean_coherence = np.mean(list(organ_coherences.values()))
            # Compare to previous cycle if available
            if len(self.salience_history) > 0:
                prev_coherence = self.salience_history[-1].get("mean_coherence", 0.5)
                gradient = (mean_coherence - prev_coherence) / 2 + 0.5  # Normalize to [0,1]
                self.terms["coherence_gradient"].value = max(0, min(1.0, gradient))
            else:
                self.terms["coherence_gradient"].value = mean_coherence
        else:
            self.terms["coherence_gradient"].value = 0.4

        # 10. Satisfaction Proximity - Closeness to satisfaction
        # Use satisfaction value directly + Kairos boost
        proximity = satisfaction
        if kairos_detected:
            proximity = min(1.0, proximity * 1.2)
        self.terms["satisfaction_proximity"].value = proximity

    def _extract_trauma_markers(self, prehension: Dict[str, Any]) -> Dict[str, Any]:
        """Extract trauma markers for emission modulation"""
        return {
            "signal_inflation": self.terms["signal_inflation"].value,
            "temporal_collapse": self.terms["temporal_collapse"].value,
            "safety_gradient": self.terms["safety_gradient"].value,
            "overall_trauma_salience": (
                self.terms["signal_inflation"].value * 0.4 +
                self.terms["temporal_collapse"].value * 0.3 +
                (1.0 - self.terms["safety_gradient"].value) * 0.3
            )
        }

    def _get_conversational_guidance(self, morphogenetic_pressure: float) -> str:
        """Provide guidance for emission modulation"""
        safety = self.terms["safety_gradient"].value
        signal_inflation = self.terms["signal_inflation"].value

        if signal_inflation > 0.7:
            return "trauma_detected_gentle"
        elif morphogenetic_pressure > 0.8 and safety > 0.6:
            return "crystallize_insight"
        elif morphogenetic_pressure > 0.5 and safety > 0.4:
            return "prepare_shift"
        elif self.terms["temporal_collapse"].value > 0.7:
            return "ground_present"
        elif safety < 0.4:
            return "establish_safety"
        else:
            return "maintain_presence"
