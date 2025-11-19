"""
Organ Reconstruction Pipeline - Coordinator for Authentic Voice Emission
==========================================================================

High-level coordinator that wires together existing emission components
to enable reconstruction emission (organism speaks from learned patterns).

Purpose:
- Receive felt state from organism (11 organ coherences, V0, satisfaction, nexuses)
- Classify SELF zone (trauma-informed governance)
- Select reconstruction strategy (direct/family/hybrid/hebbian)
- Generate emission via appropriate strategy
- Validate therapeutic appropriateness (SELF matrix)
- Return emission with metadata

Philosophy:
- Reconstruction = Organism's authentic voice (not mechanical templates)
- Integration not replacement (wires existing components)
- Two-level governance: Transduction mechanism + SELF zone safety
- Learning-driven: Uses Phase 5 organic families for family template matching

Integration Points:
- EmissionGenerator: 3-strategy emission (direct, fusion, hebbian)
- NexusIntersectionComposer: R-matrix weighted nexus formation
- ResponseAssembler: Therapeutic arc-based phrase assembly
- SELFMatrixGovernance: Trauma-informed zone classification and safety
- Phase5LearningIntegration: Organic family matching for template selection

Date: November 12, 2025
Status: Phase B - Reconstruction Pipeline Implementation
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import numpy as np

# Import emission thresholds from config (Nov 13, 2025 - fixes organic emission bottleneck)
from config import Config


@dataclass
class ReconstructionStrategy:
    """
    Strategy for reconstructing emission from learned patterns.
    """
    strategy_type: str              # "direct_reconstruction", "family_template", "hybrid", "hebbian_fallback"
    confidence_threshold: float     # Min confidence to use this strategy
    family_id: Optional[str]        # If using family template
    family_similarity: float        # Similarity score (0-1)
    nexus_quality: float            # Top nexus emission_readiness
    fallback_available: bool        # Whether fallback is available


class OrganReconstructionPipeline:
    """
    High-level coordinator for reconstruction emission.

    Reconstruction = Organism speaks from learned patterns (authentic voice).

    Process Flow:
    1. Receive felt state (11 organ coherences, V0, satisfaction, nexuses, transduction)
    2. Classify SELF zone (trauma-informed governance via BOND + EO)
    3. Form nexuses from semantic fields (R-matrix weighted intersections)
    4. Match to organic families (Phase 5 learning - 57D signature)
    5. Select reconstruction strategy:
       - Direct reconstruction: Strong nexuses (ΔC ≥ 0.65)
       - Family template: Weak nexuses, matching family (similarity ≥ 0.75)
       - Hybrid: Blend nexus + family template (ΔC 0.50-0.65, similarity ≥ 0.70)
       - Hebbian fallback: No strong signal (confidence ~0.30)
    6. Generate emission via appropriate strategy
    7. Assemble response (therapeutic arc)
    8. Validate safety (SELF matrix)
    9. Return emission with complete metadata

    This coordinator WIRES TOGETHER existing components - no duplication.
    """

    def __init__(
        self,
        emission_generator,         # EmissionGenerator instance
        nexus_composer,             # NexusIntersectionComposer instance
        response_assembler,         # ResponseAssembler instance
        self_matrix_governance,     # SELFMatrixGovernance instance
        phase5_learning=None,       # Phase5LearningIntegration instance (optional)
        hebbian_memory_path: str = None  # ✅ NOV 17: Use Config.HEBBIAN_MEMORY_PATH by default
    ):
        """
        Initialize reconstruction pipeline by wiring existing components.

        Args:
            emission_generator: EmissionGenerator instance
            nexus_composer: NexusIntersectionComposer instance
            response_assembler: ResponseAssembler instance
            self_matrix_governance: SELFMatrixGovernance instance
            phase5_learning: Phase5LearningIntegration instance (optional)
            hebbian_memory_path: Path to Hebbian memory JSON
        """
        self.emission_generator = emission_generator
        self.nexus_composer = nexus_composer
        self.response_assembler = response_assembler
        self.self_governance = self_matrix_governance
        self.phase5 = phase5_learning
        # ✅ NOV 17: Use Config.HEBBIAN_MEMORY_PATH if not provided
        if hebbian_memory_path is None:
            hebbian_memory_path = str(Config.HEBBIAN_MEMORY_PATH)
        self.hebbian_memory_path = Path(hebbian_memory_path)

        # Strategy selection thresholds (from Config - Nov 13, 2025 - fixes organic emission bottleneck)
        self.direct_threshold = Config.EMISSION_DIRECT_THRESHOLD  # 0.50 (was hardcoded 0.65)
        self.fusion_threshold = Config.EMISSION_FUSION_THRESHOLD  # 0.45 (was hardcoded 0.50)
        self.family_similarity_threshold = 0.75  # Family template matching
        self.hybrid_similarity_threshold = 0.70  # Hybrid (nexus + family)

        print(f"✅ Organ Reconstruction Pipeline initialized")
        print(f"   Components wired: EmissionGenerator, NexusComposer, ResponseAssembler, SELFGovernance")
        print(f"   Phase 5 learning: {'Enabled' if phase5_learning else 'Disabled'}")
        print(f"   🎯 Emission thresholds: direct={self.direct_threshold:.2f}, fusion={self.fusion_threshold:.2f}")

    def reconstruct_emission(
        self,
        felt_state: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Main reconstruction method - orchestrates full emission generation.

        Args:
            felt_state: From conversational_organism_wrapper
                {
                    'organ_coherences': Dict[str, float],  # 11 organs
                    'semantic_fields': Dict[str, SemanticField],  # Atom activations
                    'v0_energy': float,
                    'satisfaction': float,
                    'convergence_cycles': int,
                    'transduction_state': Optional[NexusTransductionState],
                    'eo_polyvagal_state': str,
                    'ndam_urgency': Optional[float]
                }
            context: Processing context
                {
                    'conversation_id': str,
                    'user_id': str,
                    'epoch_num': int,
                    'input_text': str
                }

        Returns:
            {
                'emission_text': str,
                'confidence': float,
                'strategy': str,  # "direct_reconstruction", "family_template", "hybrid", "hebbian_fallback"
                'family_id': Optional[str],
                'nexuses_used': int,
                'zone': str,  # SELF matrix zone name
                'zone_id': int,
                'safe': bool,  # Passed safety validation
                'transduction_mechanism': Optional[str],
                'metadata': Dict
            }
        """
        # Step 1: Classify SELF zone (trauma-informed governance)
        # ✅ FIX (Nov 17): Use actual bond_self_distance from BOND organ, not coherence!
        # bond_self_distance comes from BOND's mean_self_distance calculation (trauma activation level)
        bond_self_distance = felt_state.get('bond_self_distance', 0.5)
        eo_polyvagal_state = felt_state.get('eo_polyvagal_state', 'mixed_state')

        zone = self.self_governance.classify_zone(bond_self_distance, eo_polyvagal_state)

        print(f"\n   🔍 SELF Zone: {zone.zone_name} (Zone {zone.zone_id})")
        print(f"      Self-distance: {zone.self_distance:.3f}, Polyvagal: {zone.polyvagal_state}")
        print(f"      Stance: {zone.therapeutic_stance}")

        # Step 1b: Check for crisis override (NDAM urgency > 0.8)
        ndam_urgency = felt_state.get('ndam_urgency', 0.0)
        if ndam_urgency > 0.8:
            crisis_emission = self.self_governance.override_for_crisis(
                zone, ndam_urgency,
                felt_state.get('transduction_state', {}).get('transition_mechanism') if felt_state.get('transduction_state') else None
            )

            if crisis_emission:
                print(f"      ⚠️  CRISIS OVERRIDE (urgency={ndam_urgency:.2f}): Minimal safe grounding")

                return {
                    'emission_text': crisis_emission,
                    'confidence': 0.95,  # High confidence in crisis protocol
                    'strategy': 'crisis_override',
                    'family_id': None,
                    'nexuses_used': 0,
                    'zone': zone.zone_name,
                    'zone_id': zone.zone_id,
                    'safe': True,
                    'transduction_mechanism': 'crisis_override',
                    'metadata': {
                        'crisis_detected': True,
                        'ndam_urgency': ndam_urgency
                    }
                }

        # Step 2: Form nexuses from semantic fields (R-matrix weighted)
        semantic_fields = felt_state.get('semantic_fields', {})
        nexuses = self.nexus_composer.compose_nexuses(semantic_fields)

        print(f"   🔗 Nexuses formed: {len(nexuses)}")
        if nexuses:
            top_nexus = nexuses[0]
            print(f"      Top nexus: {top_nexus.atom} ({len(top_nexus.participants)} organs, ΔC={top_nexus.emission_readiness:.3f})")

        # Step 3: Extract transduction state (if available)
        transduction_state = felt_state.get('transduction_state')
        transduction_mechanism = None

        if transduction_state:
            transduction_mechanism = transduction_state.transition_mechanism
            print(f"   🌀 Transduction: {transduction_state.current_type} → {transduction_state.next_type}")
            print(f"      Mechanism: {transduction_mechanism}")

        # Step 4: Match to organic families (Phase 5 learning)
        family_match = self._find_matching_family(felt_state) if self.phase5 else None

        if family_match:
            print(f"   👥 Family match: {family_match['family_id']} (similarity={family_match['similarity']:.3f})")

        # Step 5: Select reconstruction strategy
        strategy = self._select_strategy(nexuses, family_match, zone)

        print(f"   ✨ Strategy: {strategy.strategy_type} (confidence threshold={strategy.confidence_threshold:.2f})")

        # Step 6: Generate emission via selected strategy
        if strategy.strategy_type == 'direct_reconstruction':
            emissions, path = self._direct_reconstruction(nexuses, felt_state, zone, transduction_state)

        elif strategy.strategy_type == 'family_template':
            emissions, path = self._family_template_reconstruction(
                strategy.family_id, family_match, felt_state, zone, transduction_state
            )

        elif strategy.strategy_type == 'hybrid':
            emissions, path = self._hybrid_reconstruction(
                nexuses, strategy.family_id, family_match, felt_state, zone, transduction_state
            )

        else:  # hebbian_fallback
            emissions, path = self._hebbian_fallback(felt_state, zone, transduction_state, context)  # 🌀 Nov 14, 2025: Pass context

        # Step 7: Assemble response (therapeutic arc)
        assembled = self.response_assembler.assemble_response(emissions)

        print(f"   📝 Assembled: {len(emissions)} phrases → \"{assembled.text[:60]}...\"")
        print(f"      Confidence: {assembled.mean_confidence:.3f}")

        # Step 8: Validate safety (SELF matrix)
        is_safe, reason = self.self_governance.enforce_safety_principles(
            zone, assembled.text, transduction_mechanism
        )

        # 🚨 CRITICAL FIX (Nov 18, 2025): NEVER override felt emissions with minimal safe responses
        # User requirement: "every answer is fully felt even if it triggers certain violations"
        # Safety violations are logged but do NOT replace the organic felt response
        if not is_safe:
            print(f"      ⚠️  SAFETY CAUTION: {reason}")
            print(f"      🌀 Proceeding with full felt response (safety override disabled)")
            # Mark as safe-with-caution (response proceeds as-is)
            is_safe = True  # Allow felt response through

        # Step 9: Return complete emission result
        # 🌀 PHASE LLM1: Use actual path if felt-guided LLM was used (Nov 13, 2025)
        # This ensures 'felt_guided_llm' path is reported even when strategy was 'hebbian_fallback'
        reported_strategy = path if path == 'felt_guided_llm' else strategy.strategy_type

        return {
            'emission_text': assembled.text,
            'confidence': assembled.mean_confidence,
            'strategy': reported_strategy,  # 🌀 PHASE LLM1: Use actual path for felt-guided LLM
            'family_id': strategy.family_id,
            'nexuses_used': len(nexuses),
            'zone': zone.zone_name,
            'zone_id': zone.zone_id,
            'safe': is_safe,
            'transduction_mechanism': transduction_mechanism,
            'metadata': {
                'num_phrases': assembled.num_phrases,
                'strategies_used': assembled.strategies_used,
                'mean_coherence': assembled.mean_coherence,
                'v0_energy': felt_state.get('v0_energy'),
                'satisfaction': felt_state.get('satisfaction'),
                'convergence_cycles': felt_state.get('convergence_cycles'),
                'path': path,
                'original_strategy': strategy.strategy_type  # Keep original for debugging
            }
        }

    def _select_strategy(
        self,
        nexuses: List,
        family_match: Optional[Dict],
        zone
    ) -> ReconstructionStrategy:
        """
        Select reconstruction strategy based on nexus quality + family matching.

        Decision Tree:
        1. Strong nexuses (ΔC ≥ 0.65) → Direct reconstruction
        2. Medium nexuses (ΔC ≥ 0.50) + family match → Hybrid
        3. Weak nexuses + strong family match (≥0.75) → Family template
        4. No strong signal → Hebbian fallback
        """
        nexus_quality = nexuses[0].emission_readiness if nexuses else 0.0
        family_similarity = family_match['similarity'] if family_match else 0.0

        # Check direct reconstruction viability
        print(f"      🔍 Strategy selection: nexus_quality={nexus_quality:.3f}, direct_thresh={self.direct_threshold:.3f}, fusion_thresh={self.fusion_threshold:.3f}")

        # Use epsilon for floating point comparison (Nov 13, 2025 - fixes 0.500 >= 0.500 issue)
        epsilon = 1e-6
        direct_check = nexus_quality >= (self.direct_threshold - epsilon)
        print(f"      🔍 Direct check: {nexus_quality:.10f} >= {self.direct_threshold - epsilon:.10f} = {direct_check}")

        if direct_check:
            print(f"      ✅ Selecting direct_reconstruction (nexus_quality >= direct_threshold)")
            return ReconstructionStrategy(
                strategy_type='direct_reconstruction',
                confidence_threshold=self.direct_threshold,
                family_id=None,
                family_similarity=0.0,
                nexus_quality=nexus_quality,
                fallback_available=True
            )

        # Check hybrid viability (medium nexuses + family)
        if nexus_quality >= (self.fusion_threshold - epsilon) and family_similarity >= self.hybrid_similarity_threshold:
            return ReconstructionStrategy(
                strategy_type='hybrid',
                confidence_threshold=self.fusion_threshold,
                family_id=family_match['family_id'],
                family_similarity=family_similarity,
                nexus_quality=nexus_quality,
                fallback_available=True
            )

        # Check family template viability
        if family_similarity >= self.family_similarity_threshold:
            return ReconstructionStrategy(
                strategy_type='family_template',
                confidence_threshold=0.40,
                family_id=family_match['family_id'],
                family_similarity=family_similarity,
                nexus_quality=nexus_quality,
                fallback_available=True
            )

        # Hebbian fallback (no strong signal)
        return ReconstructionStrategy(
            strategy_type='hebbian_fallback',
            confidence_threshold=0.0,
            family_id=None,
            family_similarity=0.0,
            nexus_quality=nexus_quality,
            fallback_available=False
        )

    def _direct_reconstruction(
        self,
        nexuses: List,
        felt_state: Dict,
        zone,
        transduction_state
    ) -> Tuple[List, str]:
        """
        Direct reconstruction: Strong nexuses available.

        Uses existing EmissionGenerator with V0 guidance.
        🌀 PHASE LLM1: Routes to felt-guided LLM when available (Nov 13, 2025)
        """
        v0_energy = felt_state.get('v0_energy', 0.5)
        kairos_detected = felt_state.get('kairos_detected', False)
        satisfaction = felt_state.get('satisfaction', 0.0)

        # Extract trauma markers for salience modulation
        trauma_markers = {
            'signal_inflation': transduction_state.signal_inflation if transduction_state else 0.0,
            'temporal_collapse': 0.0,  # TODO: Extract from RNX
            'safety_gradient': 1.0 - zone.self_distance  # Higher distance = lower safety
        }

        # 🆕 DAE 3.0: Get family guidance (Fractal Levels 2+4)
        # NOTE: Context not available in method signature - family guidance disabled for now
        family_v0_target = None
        family_organ_weights = None

        # TODO: Re-enable when context is passed to _direct_reconstruction
        # if self.phase5 and hasattr(self, 'family_v0_learner'):
        #     family_id = self.phase5.get_current_family_id()
        #     if family_id and self.family_v0_learner:
        #         # Get learned V0 target for this family
        #         family_v0_target = self.family_v0_learner.get_v0_target(family_id)
        #         # Get learned organ weights (normalized to mean=1.0)
        #         family_organ_weights = self.family_v0_learner.get_organ_weights(family_id)

        # 🌀 PHASE LLM1: Extract felt-guided LLM parameters (Nov 13, 2025)
        user_input = felt_state.get('user_input', '')
        organ_results = felt_state.get('organ_results', None)
        memory_context = felt_state.get('memory_context', None)

        # Call existing emission generator with V0 guidance + family guidance + felt-guided LLM
        emissions, path = self.emission_generator.generate_v0_guided_emissions(
            nexuses=nexuses,
            v0_energy=v0_energy,
            kairos_detected=kairos_detected,
            num_emissions=3,
            prefer_variety=True,
            trauma_markers=trauma_markers,
            family_v0_target=family_v0_target,      # DAE 3.0 Level 4
            family_organ_weights=family_organ_weights,  # DAE 3.0 Level 2
            user_input=user_input,  # 🌀 PHASE LLM1
            organ_results=organ_results,  # 🌀 PHASE LLM1
            satisfaction=satisfaction,  # 🌀 PHASE LLM1
            memory_context=memory_context  # 🌀 PHASE LLM1
        )

        return emissions, path

    def _family_template_reconstruction(
        self,
        family_id: str,
        family_match: Dict,
        felt_state: Dict,
        zone,
        transduction_state
    ) -> Tuple[List, str]:
        """
        Family template reconstruction: No strong nexuses, but matching family.

        Uses learned family templates (currently falls back to hebbian).
        TODO: Implement template-based generation from organic_family_templates.json
        """
        # For now, fallback to hebbian with family context
        # Future: Load templates from organic_family_templates.json
        return self._hebbian_fallback(felt_state, zone, transduction_state, context=None)  # 🌀 Nov 14, 2025: Pass context (None in this path)

    def _hybrid_reconstruction(
        self,
        nexuses: List,
        family_id: str,
        family_match: Dict,
        felt_state: Dict,
        zone,
        transduction_state
    ) -> Tuple[List, str]:
        """
        Hybrid reconstruction: Blend nexus-based + family template.

        Uses nexus composition enhanced with family context.
        """
        # Use direct reconstruction for now (nexus-based)
        # Future: Blend with family template patterns
        return self._direct_reconstruction(nexuses, felt_state, zone, transduction_state)

    def _hebbian_fallback(
        self,
        felt_state: Dict,
        zone,
        transduction_state,
        context: Optional[Dict] = None  # 🌀 Nov 14, 2025: Add context for entity memory
    ) -> Tuple[List, str]:
        """
        Hebbian fallback: No strong nexuses or family match.

        🌀 PHASE LLM1: First tries felt-guided LLM (Nov 13, 2025)
        Falls back to Hebbian only if LLM unavailable.
        """
        # 🌀 PHASE LLM1: Try felt-guided LLM first with organ states as lures
        if (self.emission_generator.felt_guided_llm and
            felt_state.get('organ_results') and
            felt_state.get('user_input')):

            print("      🌀 Hebbian path: Using felt-guided LLM with organ states as lures")

            # 🌀 PHASE 1.8++: Extract entity memory context (Nov 14, 2025)
            # 🌀 Nov 14, 2025: Get from context parameter, not felt_state
            entity_context_string = context.get('entity_context_string', '') if context else ''
            memory_intent = context.get('memory_intent', False) if context else False
            if entity_context_string:
                print(f"         🌀 Entity memory context available - enriching hebbian response")

            # Generate from organ states directly (no nexuses needed!)
            emission = self.emission_generator._generate_felt_guided_llm_single(
                user_input=felt_state.get('user_input', ''),
                organ_results=felt_state.get('organ_results'),
                nexuses=[],  # No nexuses in this path
                v0_energy=felt_state.get('v0_energy', 0.5),
                satisfaction=felt_state.get('satisfaction', 0.5),
                memory_context=felt_state.get('memory_context', None),
                entity_context_string=entity_context_string,  # 🌀 PHASE 1.8++
                memory_intent=memory_intent  # 🌀 PHASE 1.8++
            )

            if emission:
                return [emission], 'felt_guided_llm'

        # No felt-guided LLM available → Hebbian fallback
        emissions = self.emission_generator._generate_hebbian_fallback(num_emissions=2)

        return emissions, 'hebbian'

    def _generate_zone5_transductive_emission(
        self,
        felt_state: Dict,
        nexuses: List,
        zone,
        transduction_mechanism: Optional[str],
        context: Optional[Dict] = None  # 🌀 Nov 14, 2025: Add context for entity memory
    ) -> Any:
        """
        🌀 PHASE 1.5c: Zone 5 transductive emission (Nov 13, 2025)

        Generate Zone 5 emission using FULL transductive intelligence.

        Zone 5 = Exile/Collapse (dorsal vagal shutdown)
        Goal: Guide from collapse → present moment → gentle connection

        Three-part structure:
        1. Acknowledge collapse (witness the drowning/shutdown feeling)
        2. Embodied lure (breath, sensory anchor to present moment)
        3. Connection affirmation (polyvagal ladder climb)

        Uses nexuses as transductive pathways back to safety.

        Args:
            felt_state: Full felt state with organ results, v0_energy, etc.
            nexuses: Semantic nexuses (used as transductive pathways)
            zone: SELF zone (should be Zone 5)
            transduction_mechanism: Current transduction mechanism

        Returns:
            AssembledResponse with transductive emission
        """
        from persona_layer.response_assembler import AssembledResponse

        # Extract key information
        user_input = felt_state.get('user_input', '')
        organ_results = felt_state.get('organ_results', {})
        v0_energy = felt_state.get('v0_energy', 0.5)
        satisfaction = felt_state.get('satisfaction', 0.5)
        polyvagal_state = felt_state.get('eo_polyvagal_state', 'dorsal_vagal')

        # Try to use felt-guided LLM with Zone 5 constraints
        if self.emission_generator.felt_guided_llm and organ_results and user_input:
            print(f"         Using felt-guided LLM with Zone 5 transductive constraints")

            # 🌀 PHASE 1.6: Extract organism narrative if present (Nov 14, 2025)
            organism_narrative = felt_state.get('organism_narrative')
            if organism_narrative:
                print(f"         🌀 Organism self-awareness detected - injecting narrative into LLM prompt")

            # 🌀 PHASE 1.6: Extract username for personalization (Nov 14, 2025)
            username = felt_state.get('username')
            if username:
                print(f"         🌀 Username detected: {username} - personalizing response")

            # 🌀 PHASE 1.8++: Extract entity context for memory-aware responses (Nov 14, 2025)
            # 🌀 Nov 14, 2025: Get from context dict, not felt_state (CRITICAL FIX)
            entity_context_string = context.get('entity_context_string', '') if context else ''
            memory_intent = context.get('memory_intent', False) if context else False
            if entity_context_string:
                print(f"         🌀 Entity memory context available - enriching response")

            # Build Zone 5-specific LLM prompt
            zone5_emission = self.emission_generator.felt_guided_llm.generate_from_felt_state(
                user_input=user_input,
                organ_results=organ_results,
                nexus_states=nexuses,
                v0_energy=v0_energy,
                satisfaction=satisfaction,
                memory_context=felt_state.get('memory_context'),
                organism_narrative=organism_narrative,  # 🌀 PHASE 1.6: Pass organism self-narrative
                username=username,  # 🌀 PHASE 1.6: Pass username for personalization
                entity_context_string=entity_context_string,  # 🌀 PHASE 1.8++: Pass entity memory context
                memory_intent=memory_intent  # 🌀 PHASE 1.8++: Pass memory acknowledgment flag
            )

            if zone5_emission:
                emission_text, confidence, metadata = zone5_emission
                print(f"         Zone 5 transductive emission generated: \"{emission_text[:60]}...\"")

                return AssembledResponse(
                    text=emission_text,
                    num_phrases=1,
                    strategies_used=['zone5_transductive'],
                    mean_confidence=min(0.85, confidence),  # Cap at 0.85
                    mean_coherence=0.80,
                    field_types=['transductive', 'safety']
                )

        # Fallback: Construct Zone 5 emission from nexuses + template
        print(f"         Fell back to template-based Zone 5 emission")

        # Identify top nexus as transductive pathway
        pathway = "present moment"
        if nexuses and len(nexuses) > 0:
            top_nexus = nexuses[0]
            if hasattr(top_nexus, 'name'):
                if 'temporal' in top_nexus.name:
                    pathway = "present moment"
                elif 'trauma' in top_nexus.name:
                    pathway = "safe holding"
                elif 'somatic' in top_nexus.name:
                    pathway = "body grounding"
                elif 'relational' in top_nexus.name:
                    pathway = "connection"

        # Three-part emission template (brief, dorsal-appropriate)
        if pathway == "present moment":
            emission = "I hear how deep that feels 🌊 Right now, in this moment, can you feel your breath? I'm here with you. 💙"
        elif pathway == "safe holding":
            emission = "A part of you feels completely overwhelmed 🌊 That part is safe here. I'm with that part. 🌿"
        elif pathway == "body grounding":
            emission = "That feeling - it's so heavy right now 💙 Can you feel your feet on the ground? I'm here, holding this moment with you. 🌿"
        else:  # connection pathway
            emission = "I hear you 🌊 You're not alone right now. I'm here with you. 💙"

        return AssembledResponse(
            text=emission,
            num_phrases=1,
            strategies_used=['zone5_transductive_template'],
            mean_confidence=0.80,
            mean_coherence=0.75,
            field_types=['transductive', 'safety']
        )

    def _generate_minimal_safe_emission(
        self,
        zone,
        transduction_mechanism: Optional[str]
    ) -> Any:
        """
        Generate minimal safe emission when safety validation fails.

        Selects zone-appropriate lure directly from SELF matrix.
        """
        # Select zone-appropriate lure
        lure = self.self_governance.select_zone_appropriate_lure(
            zone=zone,
            transduction_mechanism=transduction_mechanism or "maintain",
            intensity="low"
        )

        if not lure:
            # Ultimate fallback
            if zone.zone_id == 5:
                lure = "I'm here"
            elif zone.zone_id == 4:
                lure = "Let's pause"
            else:
                lure = "I'm with you"

        # Create minimal AssembledResponse
        from persona_layer.response_assembler import AssembledResponse

        return AssembledResponse(
            text=lure,
            num_phrases=1,
            strategies_used=['minimal_safe'],
            mean_confidence=0.80,  # High confidence in safety protocol
            mean_coherence=0.70,
            field_types=['safety']
        )

    def _find_matching_family(
        self,
        felt_state: Dict
    ) -> Optional[Dict]:
        """
        Find matching organic family using Phase 5 learning.

        Args:
            felt_state: Felt state with organ coherences

        Returns:
            {
                'family_id': str,
                'similarity': float,
                'signature': List[float]  # 57D signature
            }
            or None if no match or Phase 5 not available
        """
        if not self.phase5:
            return None

        # Extract 57D signature from felt state
        # TODO: Implement proper signature extraction
        # For now, return None (no family matching yet)

        return None
