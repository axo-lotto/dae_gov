"""
Transduction Pathway Evaluator
================================

Evaluates transduction pathways between nexus types.

Implements the 9 primary pathways from 14_NEXUS_DESIGN.md:
1. Urgency → Relational (salience_recalibration)
2. Urgency → Disruptive (incoherent_broadcasting)
3. Recursive → Protective (contrast_reestablishment)
4. Recursive → Innate (ontological_rebinding)
5. Fragmented → Relational (salience_realignment)
6. Fragmented → Absorbed (projective_ingression)
7. Innate → Pre-Existing (recursive_grounding)
8. Innate → Absorbed (field_hijacking)
9. Relational → Protective (boundary_fortification)

Date: November 12, 2025
Purpose: Dynamic transductive nexus flows for DAE_HYPHAE_1
"""

from typing import List, Dict, Any, Optional
import numpy as np


class TransductionPathwayEvaluator:
    """
    Evaluate transduction pathways between nexus types.

    Implements the 9 primary pathways + additional pathways based on
    V0 energy descent, mutual satisfaction, and rhythmic coherence.
    """

    def __init__(self):
        """Initialize pathway evaluator."""
        # Pathway definitions loaded from logic (not JSON for now)
        pass

    def evaluate_pathways(
        self,
        current_nexus_type: str,
        v0_energy: float,
        satisfaction: float,
        mutual_satisfaction: float,
        rhythm_coherence: float,
        relational_field_available: bool,
        organ_insights: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Evaluate all available transduction pathways from current nexus.

        Args:
            current_nexus_type: Current nexus type (e.g., "Urgency")
            v0_energy: Current V0 appetition energy (0-1)
            satisfaction: Current satisfaction level (0-1)
            mutual_satisfaction: Co-satisfaction across parts (0-1)
            rhythm_coherence: Rhythmic entrainment (0-1)
            relational_field_available: Can attunement occur?
            organ_insights: Dictionary of organ-specific metrics

        Returns:
            List of pathway dictionaries: {type, mechanism, probability, description}
        """

        # Route to appropriate pathway evaluator
        if current_nexus_type == "Urgency":
            return self._evaluate_urgency_pathways(
                v0_energy, satisfaction, mutual_satisfaction,
                rhythm_coherence, relational_field_available, organ_insights
            )

        elif current_nexus_type == "Recursive":
            return self._evaluate_recursive_pathways(
                v0_energy, satisfaction, mutual_satisfaction,
                rhythm_coherence, relational_field_available, organ_insights
            )

        elif current_nexus_type == "Fragmented":
            return self._evaluate_fragmented_pathways(
                v0_energy, satisfaction, mutual_satisfaction,
                rhythm_coherence, relational_field_available, organ_insights
            )

        elif current_nexus_type == "Innate":
            return self._evaluate_innate_pathways(
                v0_energy, satisfaction, mutual_satisfaction,
                rhythm_coherence, relational_field_available, organ_insights
            )

        elif current_nexus_type == "Relational":
            return self._evaluate_relational_pathways(
                v0_energy, satisfaction, mutual_satisfaction,
                rhythm_coherence, relational_field_available, organ_insights
            )

        # Default: Return maintenance pathway
        else:
            return [{
                'type': current_nexus_type,
                'mechanism': 'maintain',
                'probability': 1.0,
                'description': f'Maintain {current_nexus_type} state'
            }]

    def _evaluate_urgency_pathways(
        self, v0_energy, satisfaction, mutual_satisfaction,
        rhythm_coherence, relational_field_available, organ_insights
    ) -> List[Dict]:
        """
        Urgency has 2 primary pathways.

        Path 1: Urgency → Relational (salience_recalibration)
                Via relational witnessing, urgency becomes metabolizable

        Path 2: Urgency → Disruptive (incoherent_broadcasting)
                Via relational rejection, urgency leaks into dysregulated action
        """

        pathways = []

        # Path 1: Urgency → Relational (healing pathway)
        if relational_field_available and rhythm_coherence > 0.5:
            prob = mutual_satisfaction * rhythm_coherence * 0.9
            pathways.append({
                'type': 'Relational',
                'mechanism': 'salience_recalibration',
                'probability': float(prob),
                'description': 'Urgency becomes metabolizable through relational witnessing'
            })

        # Path 2: Urgency → Disruptive (crisis pathway)
        if not relational_field_available or rhythm_coherence < 0.3:
            prob = (1 - mutual_satisfaction) * 0.8
            pathways.append({
                'type': 'Disruptive',
                'mechanism': 'incoherent_broadcasting',
                'probability': float(prob),
                'description': 'Urgency leaks into dysregulated social action'
            })

        return pathways

    def _evaluate_recursive_pathways(
        self, v0_energy, satisfaction, mutual_satisfaction,
        rhythm_coherence, relational_field_available, organ_insights
    ) -> List[Dict]:
        """
        Recursive has 2 primary pathways.

        Path 3: Recursive → Protective (contrast_reestablishment)
                When boundaries need fortifying

        Path 4: Recursive → Innate (ontological_rebinding)
                When grounding into core self
        """

        pathways = []

        bond_self_distance = organ_insights.get('bond_self_distance', 0.5)

        # Path 3: Recursive → Protective
        if bond_self_distance > 0.4 and mutual_satisfaction < 0.6:
            prob = (1 - mutual_satisfaction) * rhythm_coherence * 0.85
            pathways.append({
                'type': 'Protective',
                'mechanism': 'contrast_reestablishment',
                'probability': float(prob),
                'description': 'Recursive patterns fortify protective boundaries'
            })

        # Path 4: Recursive → Innate (healing pathway)
        if bond_self_distance < 0.3 and satisfaction > 0.7:
            prob = mutual_satisfaction * (1 - v0_energy) * 0.9
            pathways.append({
                'type': 'Innate',
                'mechanism': 'ontological_rebinding',
                'probability': float(prob),
                'description': 'Recursive loops ground into essential self'
            })

        return pathways

    def _evaluate_fragmented_pathways(
        self, v0_energy, satisfaction, mutual_satisfaction,
        rhythm_coherence, relational_field_available, organ_insights
    ) -> List[Dict]:
        """
        Fragmented has 2 primary pathways.

        Path 5: Fragmented → Relational (salience_realignment)
                Via relational repair of scattered parts

        Path 6: Fragmented → Absorbed (projective_ingression)
                Via losing self in external field
        """

        pathways = []

        # Path 5: Fragmented → Relational (healing pathway)
        if relational_field_available and rhythm_coherence > 0.4:
            prob = mutual_satisfaction * rhythm_coherence * 0.85
            pathways.append({
                'type': 'Relational',
                'mechanism': 'salience_realignment',
                'probability': float(prob),
                'description': 'Fragmented parts realign through relational witnessing'
            })

        # Path 6: Fragmented → Absorbed (crisis pathway)
        if not relational_field_available:
            prob = (1 - mutual_satisfaction) * v0_energy * 0.75
            pathways.append({
                'type': 'Absorbed',
                'mechanism': 'projective_ingression',
                'probability': float(prob),
                'description': 'Fragmented self dissolves into external field'
            })

        return pathways

    def _evaluate_innate_pathways(
        self, v0_energy, satisfaction, mutual_satisfaction,
        rhythm_coherence, relational_field_available, organ_insights
    ) -> List[Dict]:
        """
        Innate has 2 primary pathways.

        Path 7: Innate → Pre-Existing (recursive_grounding)
                Via stabilizing into ontological bedrock

        Path 8: Innate → Absorbed (field_hijacking)
                Via losing boundaries to external demands
        """

        pathways = []

        bond_self_distance = organ_insights.get('bond_self_distance', 0.5)

        # Path 7: Innate → Pre-Existing (deepening pathway)
        if satisfaction > 0.8 and bond_self_distance < 0.2:
            prob = satisfaction * rhythm_coherence * 0.9
            pathways.append({
                'type': 'Pre-Existing',
                'mechanism': 'recursive_grounding',
                'probability': float(prob),
                'description': 'Innate patterns stabilize into ontological bedrock'
            })

        # Path 8: Innate → Absorbed (crisis pathway)
        if not relational_field_available and v0_energy > 0.6:
            prob = v0_energy * (1 - mutual_satisfaction) * 0.7
            pathways.append({
                'type': 'Absorbed',
                'mechanism': 'field_hijacking',
                'probability': float(prob),
                'description': 'Innate self loses boundaries to external field'
            })

        return pathways

    def _evaluate_relational_pathways(
        self, v0_energy, satisfaction, mutual_satisfaction,
        rhythm_coherence, relational_field_available, organ_insights
    ) -> List[Dict]:
        """
        Relational has 1 primary pathway + general pathways.

        Path 9: Relational → Protective (boundary_fortification)
                When relational field becomes overwhelming
        """

        pathways = []

        bond_self_distance = organ_insights.get('bond_self_distance', 0.5)

        # Path 9: Relational → Protective
        if bond_self_distance > 0.35 and v0_energy > 0.5:
            prob = v0_energy * (1 - mutual_satisfaction) * 0.8
            pathways.append({
                'type': 'Protective',
                'mechanism': 'boundary_fortification',
                'probability': float(prob),
                'description': 'Relational field becomes overwhelming, boundaries needed'
            })

        # Relational can also deepen to Innate
        if satisfaction > 0.85 and bond_self_distance < 0.2:
            prob = satisfaction * mutual_satisfaction * 0.85
            pathways.append({
                'type': 'Innate',
                'mechanism': 'deepening_attunement',
                'probability': float(prob),
                'description': 'Relational attunement deepens into innate presence'
            })

        return pathways

    # Additional pathway evaluators for other nexus types

    def _evaluate_disruptive_pathways(
        self, v0_energy, satisfaction, mutual_satisfaction,
        rhythm_coherence, relational_field_available, organ_insights
    ) -> List[Dict]:
        """
        Disruptive pathways (crisis state).

        Disruptive → Urgency (escalation)
        Disruptive → Fragmented (fracturing)
        """

        pathways = []

        # Disruptive → Urgency (escalation)
        if v0_energy > 0.7:
            prob = v0_energy * (1 - satisfaction) * 0.9
            pathways.append({
                'type': 'Urgency',
                'mechanism': 'crisis_escalation',
                'probability': float(prob),
                'description': 'Disruption escalates to urgent crisis'
            })

        # Disruptive → Fragmented (if relational field appears)
        if relational_field_available and rhythm_coherence > 0.4:
            prob = mutual_satisfaction * 0.7
            pathways.append({
                'type': 'Fragmented',
                'mechanism': 'pattern_softening',
                'probability': float(prob),
                'description': 'Disruption softens into fragmented parts seeking repair'
            })

        return pathways

    def _evaluate_protective_pathways(
        self, v0_energy, satisfaction, mutual_satisfaction,
        rhythm_coherence, relational_field_available, organ_insights
    ) -> List[Dict]:
        """
        Protective pathways (boundary maintenance).

        Protective → Relational (when safe)
        Protective → Recursive (when threatened)
        """

        pathways = []

        bond_self_distance = organ_insights.get('bond_self_distance', 0.5)

        # Protective → Relational (healing)
        if relational_field_available and satisfaction > 0.7:
            prob = mutual_satisfaction * rhythm_coherence * 0.85
            pathways.append({
                'type': 'Relational',
                'mechanism': 'boundary_softening',
                'probability': float(prob),
                'description': 'Protective boundaries soften into relational availability'
            })

        # Protective → Recursive (threat response)
        if bond_self_distance > 0.5 or v0_energy > 0.6:
            prob = v0_energy * (1 - mutual_satisfaction) * 0.8
            pathways.append({
                'type': 'Recursive',
                'mechanism': 'pattern_reinforcement',
                'probability': float(prob),
                'description': 'Protective patterns loop recursively when threatened'
            })

        return pathways

    def get_mechanism_description(self, mechanism: str) -> str:
        """
        Get human-readable description of transduction mechanism.

        Args:
            mechanism: Mechanism name (e.g., "salience_recalibration")

        Returns:
            Human-readable description
        """

        mechanism_descriptions = {
            'salience_recalibration': 'Urgency becomes metabolizable through relational witnessing',
            'incoherent_broadcasting': 'Urgency leaks into dysregulated social action',
            'contrast_reestablishment': 'Protective boundaries fortify against overwhelm',
            'ontological_rebinding': 'Recursive patterns ground into essential self',
            'salience_realignment': 'Fragmented parts realign through witnessing',
            'projective_ingression': 'Fragmented self dissolves into external field',
            'recursive_grounding': 'Innate patterns stabilize into ontological bedrock',
            'field_hijacking': 'Innate self loses boundaries to external demands',
            'boundary_fortification': 'Relational field becomes overwhelming',
            'deepening_attunement': 'Relational connection deepens into innate presence',
            'maintain': 'Current nexus state maintained',
            'crisis_escalation': 'Disruption intensifies into urgent crisis',
            'pattern_softening': 'Rigid patterns soften into seeking repair',
            'boundary_softening': 'Protective walls soften into relational availability',
            'pattern_reinforcement': 'Protective patterns loop recursively when threatened'
        }

        return mechanism_descriptions.get(mechanism, f'Transduction via {mechanism}')

    def get_healing_vs_crisis_score(self, pathways: List[Dict]) -> float:
        """
        Score pathways as healing vs crisis-oriented.

        Healing pathways: → Relational, → Innate, → Pre-Existing
        Crisis pathways: → Disruptive, → Urgency, → Absorbed, → Fragmented

        Returns:
            Score from -1 (crisis) to +1 (healing)
        """

        if not pathways:
            return 0.0

        healing_types = {'Relational', 'Innate', 'Pre-Existing'}
        crisis_types = {'Disruptive', 'Urgency', 'Absorbed', 'Fragmented', 'Looped'}

        total_prob = 0.0
        healing_prob = 0.0
        crisis_prob = 0.0

        for pathway in pathways:
            prob = pathway['probability']
            total_prob += prob

            if pathway['type'] in healing_types:
                healing_prob += prob
            elif pathway['type'] in crisis_types:
                crisis_prob += prob

        if total_prob == 0:
            return 0.0

        # Normalize and compute score
        healing_score = healing_prob / total_prob
        crisis_score = crisis_prob / total_prob

        return healing_score - crisis_score  # Range: -1 to +1
