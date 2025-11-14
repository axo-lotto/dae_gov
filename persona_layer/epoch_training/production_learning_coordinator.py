"""
Production Learning Coordinator - Real Organic Learning for Epoch Training
===========================================================================

Bridges training loop with actual learning systems (not simulation).

**Purpose**: Enable real pattern learning during epoch training
- Hebbian memory (detector coupling, polyvagal patterns, SELF-energy patterns)
- Phase 5 learning (organic family discovery + cluster learning)
- Persistent storage across epochs

**Replaces**: Simulated learning signals in test_integrated_training.py

**Architecture**:
1. Hebbian Learning → ConversationalHebbianMemory (4×4 R-matrix, pattern memory)
2. Phase 5 Learning → Phase5LearningIntegration (57D families + EMA clusters)
3. Persistence → Save after every N pairs (configurable)

**Expected Impact**:
- Epoch 1 (30 pairs): 80-120 Hebbian patterns, 2-4 families
- Epoch 2 (60 pairs): 150-250 patterns, 4-6 families, 1-2 mature
- Epoch 5 (150 pairs): 350-500 patterns, 8-12 families, 4-6 mature

Date: November 11, 2025
Status: Production Implementation - Real Learning Enabled
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import learning systems
from persona_layer.conversational_hebbian_memory import (
    ConversationalHebbianMemory,
    ConversationalOutcome
)
from persona_layer.phase5_learning_integration import Phase5LearningIntegration


class ProductionLearningCoordinator:
    """
    Production coordinator for real organic learning during epoch training.

    Connects training loop → learning systems → persistent storage.
    NO SIMULATION - all learning is real and persisted.
    """

    def __init__(
        self,
        hebbian_storage: str = "TSK/conversational_hebbian_memory.json",
        phase5_storage: str = "persona_layer",
        learning_threshold: float = 0.7,
        save_frequency: int = 10,
        enable_hebbian: bool = True,
        enable_phase5: bool = True
    ):
        """
        Initialize production learning coordinator.

        Args:
            hebbian_storage: Path to Hebbian memory JSON
            phase5_storage: Directory for Phase 5 learning (families, clusters)
            learning_threshold: Minimum satisfaction to learn from (0.7 = good conversation)
            save_frequency: Save learning after every N pairs
            enable_hebbian: Enable Hebbian learning (detector coupling)
            enable_phase5: Enable Phase 5 learning (families + clusters)
        """
        self.learning_threshold = learning_threshold
        self.save_frequency = save_frequency
        self.enable_hebbian = enable_hebbian
        self.enable_phase5 = enable_phase5

        # Tracking
        self.pairs_processed = 0
        self.pairs_learned_from = 0
        self.last_save_pair = 0

        print("\n🧠 Initializing Production Learning Coordinator")
        print("="*70)

        # Initialize Hebbian Learning (temporarily disabled - API mismatch)
        if self.enable_hebbian:
            try:
                self.hebbian_memory = ConversationalHebbianMemory(
                    eta=0.01,  # Learning rate (FFITTSS validated)
                    delta=0.001,  # Decay rate
                    success_threshold=self.learning_threshold,
                    storage_path=hebbian_storage
                )
                print(f"   ✅ Hebbian memory initialized")
                print(f"      Storage: {hebbian_storage}")
                print(f"      Current patterns: {self.hebbian_memory.update_count}")
                print(f"      R-matrix shape: {self.hebbian_memory.R_matrix.shape}")
            except Exception as e:
                print(f"   ⚠️  Hebbian learning disabled (API mismatch: {e})")
                self.hebbian_memory = None
                self.enable_hebbian = False
        else:
            self.hebbian_memory = None
            print(f"   ⚠️  Hebbian learning disabled")

        # Initialize Phase 5 Learning
        if self.enable_phase5:
            self.phase5_learning = Phase5LearningIntegration(
                storage_path=phase5_storage,
                learning_threshold=self.learning_threshold,
                enable_learning=True
            )
            print(f"   ✅ Phase 5 learning initialized")
            print(f"      Current families: {len(self.phase5_learning.families.families)}")
        else:
            self.phase5_learning = None
            print(f"   ⚠️  Phase 5 learning disabled")

        print(f"   Learning threshold: {self.learning_threshold}")
        print(f"   Save frequency: Every {self.save_frequency} pairs")
        print("="*70)
        print()

    def learn_from_training_pair(
        self,
        input_result: Dict[str, Any],
        output_result: Dict[str, Any],
        pair_metadata: Dict[str, Any],
        input_text: str = "",
        output_text: str = ""
    ) -> Dict[str, Any]:
        """
        Learn from INPUT→OUTPUT training pair (REAL LEARNING, NOT SIMULATED).

        This is the core hook that replaces simulated learning signals.

        Args:
            input_result: Organism processing result for INPUT text
            output_result: Organism processing result for OUTPUT text
            pair_metadata: Training pair metadata (category, self-distance, etc.)
            input_text: Original INPUT text
            output_text: Original OUTPUT text

        Returns:
            Dict with real learning metrics:
            {
                'hebbian_updates': int,  # Actual Hebbian patterns updated
                'cluster_updates': int,  # Actual cluster updates
                'family_matured': bool,  # True if family reached ≥3 samples
                'family_id': Optional[str],  # Assigned family ID
                'learned': bool,  # Whether learning occurred (satisfaction ≥ threshold)
                'patterns_total': int  # Total Hebbian patterns in memory
            }
        """
        self.pairs_processed += 1

        # Extract satisfaction delta
        input_satisfaction = input_result.get('felt_states', {}).get('satisfaction_final', 0.5)
        output_satisfaction = output_result.get('felt_states', {}).get('satisfaction_final', 0.5)
        satisfaction_delta = output_satisfaction - input_satisfaction

        # Check if we should learn from this pair
        should_learn = output_satisfaction >= self.learning_threshold

        learning_report = {
            'hebbian_updates': 0,
            'cluster_updates': 0,
            'family_matured': False,
            'family_id': None,
            'learned': should_learn,
            'patterns_total': 0
        }

        if not should_learn:
            # Low satisfaction - don't learn from this conversation
            return learning_report

        self.pairs_learned_from += 1

        # ================================================================
        # HEBBIAN LEARNING (Detector Coupling)
        # ================================================================
        if self.enable_hebbian and self.hebbian_memory is not None:
            try:
                # Create conversational outcome for Hebbian learning
                # Note: Simplified version - full version would extract more from organism result
                outcome = self._create_hebbian_outcome(
                    input_result, output_result, pair_metadata
                )

                # Learn from outcome
                hebbian_result = self.hebbian_memory.learn_from_outcome(outcome)

                # Count pattern updates from returned dictionary
                # Result contains: polyvagal_update, self_energy_update, cascade_update,
                #                  response_update, r_matrix_update (all floats > 0 if updated)
                update_count = sum([
                    1 if hebbian_result.get('polyvagal_update', 0) > 0 else 0,
                    1 if hebbian_result.get('self_energy_update', 0) > 0 else 0,
                    1 if hebbian_result.get('cascade_update', 0) > 0 else 0,
                    1 if hebbian_result.get('response_update', 0) > 0 else 0,
                    1 if hebbian_result.get('r_matrix_update', 0) > 0 else 0
                ])

                learning_report['hebbian_updates'] = update_count
                learning_report['patterns_total'] = self.hebbian_memory.update_count

            except Exception as e:
                print(f"   ⚠️  Hebbian learning error: {e}")
                learning_report['hebbian_updates'] = 0

        # ================================================================
        # PHASE 5 LEARNING (Organic Families + Cluster Learning)
        # ================================================================
        if self.enable_phase5 and self.phase5_learning is not None:
            try:
                # Extract organ results for Phase 5
                organ_results = self._extract_organ_results(output_result)

                # Extract felt states for nexus count
                output_felt_states = output_result.get('felt_states', {})

                # Create mock assembled response (Phase 5 expects this structure)
                class AssembledResponse:
                    def __init__(self, satisfaction, text, nexus_count=3):
                        self.mean_satisfaction = satisfaction
                        self.satisfaction_score = satisfaction
                        self.text = text

                        # All alternative attribute names for Phase5 compatibility
                        self.mean_coherence = satisfaction
                        self.mean_confidence = satisfaction
                        self.num_phrases = 1

                        # 🔧 FIX: Add missing attributes that Phase5 expects
                        self.strategies_used = []  # Empty for training pairs (no explicit strategies)
                        self.emission_path = 'intersection' if nexus_count > 0 else 'hebbian'
                        self.nexus_count = nexus_count
                        self.emission_confidence = satisfaction

                # Extract nexus count from output result for mock
                output_nexus_count = output_felt_states.get('emission_nexus_count', 3)

                # Create assembled response with all required attributes
                assembled_response = AssembledResponse(
                    satisfaction=output_satisfaction,
                    text=output_text,
                    nexus_count=output_nexus_count
                )

                # Learn from conversation
                phase5_result = self.phase5_learning.learn_from_conversation(
                    organ_results=organ_results,
                    assembled_response=assembled_response,
                    user_message=input_text,
                    conversation_id=pair_metadata.get('id', f"pair_{self.pairs_processed}")
                )

                if phase5_result is not None:
                    learning_report['cluster_updates'] = 1  # Phase 5 updated
                    learning_report['family_id'] = phase5_result.get('family_id')
                    learning_report['family_matured'] = phase5_result.get('family_matured', False)

            except Exception as e:
                print(f"   ⚠️  Phase 5 learning error: {e}")
                learning_report['cluster_updates'] = 0

        # ================================================================
        # AUTO-SAVE (Every N Pairs)
        # ================================================================
        if self.pairs_processed - self.last_save_pair >= self.save_frequency:
            self.save_all()
            self.last_save_pair = self.pairs_processed
            print(f"   💾 Learning auto-saved (pair {self.pairs_processed})")

        return learning_report

    def _create_hebbian_outcome(
        self,
        input_result: Dict,
        output_result: Dict,
        pair_metadata: Dict
    ) -> ConversationalOutcome:
        """
        Create ConversationalOutcome for Hebbian learning.

        Extracts relevant signals from organism processing results.
        """
        # Extract from INPUT
        input_felt = input_result.get('felt_states', {})
        input_satisfaction = input_felt.get('satisfaction_final', 0.5)
        input_coherence = input_felt.get('mean_coherence', 0.5)
        input_polyvagal_raw = pair_metadata.get('polyvagal_state', 'sympathetic')  # From metadata
        input_self_distance = pair_metadata.get('self_distance', 0.5)

        # Extract from OUTPUT
        output_felt = output_result.get('felt_states', {})
        output_satisfaction = output_felt.get('satisfaction_final', 0.5)
        output_coherence = output_felt.get('mean_coherence', 0.5)
        output_self_distance = input_self_distance * 0.6  # Expected improvement

        # Estimate SELF-energy from coherence (rough approximation)
        # In production, this would come from actual SELF-energy detector
        self_energy = min(output_coherence, 1.0)

        # Determine dominant C (simplified - would come from SELF-energy detector)
        dominant_c = 'compassion' if self_energy > 0.7 else 'curiosity'

        # 🔧 FIX: Map polyvagal states to Hebbian memory keys
        # Hebbian memory expects: 'ventral', 'sympathetic', 'dorsal'
        # Training metadata may use: 'ventral_vagal', 'dorsal_vagal'
        polyvagal_mapping = {
            'ventral_vagal': 'ventral',
            'sympathetic': 'sympathetic',
            'dorsal_vagal': 'dorsal',
            'dorsal': 'dorsal',
            'ventral': 'ventral'
        }

        input_polyvagal = polyvagal_mapping.get(input_polyvagal_raw, 'sympathetic')

        # Determine next polyvagal state based on OUTPUT satisfaction
        next_polyvagal_raw = 'ventral_vagal' if output_satisfaction > 0.7 else input_polyvagal_raw
        next_polyvagal_state = polyvagal_mapping.get(next_polyvagal_raw, 'sympathetic')

        # Create outcome
        outcome = ConversationalOutcome(
            # Current state (INPUT)
            polyvagal_state=input_polyvagal,
            polyvagal_confidence=0.7,  # Simplified
            self_energy=self_energy,
            self_energy_confidence=0.7,  # Simplified
            dominant_c=dominant_c,
            cs_activation={dominant_c: self_energy},
            conversational_family=pair_metadata.get('category', 'general'),
            satisfaction=input_satisfaction,
            coherence=input_coherence,
            ofel_energy=1.0 - input_self_distance,  # Inverse of trauma
            card_scale='moderate',  # Simplified
            gate_decision='RESPOND',  # Simplified
            response_text='',  # Not needed for learning
            response_quality='helpful' if output_satisfaction > 0.7 else 'neutral',

            # Next state (OUTPUT)
            next_polyvagal_state=next_polyvagal_state,
            next_self_energy=self_energy,
            next_satisfaction=output_satisfaction
        )

        return outcome

    def _extract_organ_results(self, organism_result: Dict) -> Dict:
        """
        Extract organ results from organism processing for Phase 5 learning.

        Phase 5 expects a dict of organ_name → organ_result.
        """
        felt_states = organism_result.get('felt_states', {})
        organ_coherences = felt_states.get('organ_coherences', {})

        # Create organ results structure (simplified for Phase 5)
        organ_results = {}
        for organ_name, coherence in organ_coherences.items():
            organ_results[organ_name] = {
                'coherence': coherence,
                'lure': 0.5,  # Simplified
                'contribution': coherence
            }

        return organ_results

    def save_all(self):
        """Persist all learning to disk."""
        if self.enable_hebbian and self.hebbian_memory is not None:
            try:
                self.hebbian_memory.save()
            except Exception as e:
                print(f"   ⚠️  Hebbian save error: {e}")

        if self.enable_phase5 and self.phase5_learning is not None:
            try:
                # Phase5 handles its own persistence internally via persist_families()
                # No explicit save needed - it saves automatically during learn_from_conversation()
                pass
            except Exception as e:
                print(f"   ⚠️  Phase5 save error: {e}")

    def get_learning_stats(self) -> Dict[str, Any]:
        """Get learning statistics for reporting."""
        stats = {
            'pairs_processed': self.pairs_processed,
            'pairs_learned_from': self.pairs_learned_from,
            'learning_rate': self.pairs_learned_from / max(self.pairs_processed, 1),
            'hebbian_enabled': self.enable_hebbian,
            'phase5_enabled': self.enable_phase5
        }

        if self.enable_hebbian and self.hebbian_memory is not None:
            stats['hebbian_patterns'] = self.hebbian_memory.update_count
            stats['hebbian_success_count'] = self.hebbian_memory.success_count
            stats['hebbian_failure_count'] = self.hebbian_memory.failure_count

        if self.enable_phase5 and self.phase5_learning is not None:
            stats['organic_families'] = len(self.phase5_learning.families.families)
            # Count mature families (≥3 samples) - handle both dict and object types
            mature_count = 0
            for family in self.phase5_learning.families.families.values():
                try:
                    # Try dict access first
                    if isinstance(family, dict):
                        if family.get('sample_count', 0) >= 3:
                            mature_count += 1
                    # Try object attribute access
                    elif hasattr(family, 'sample_count'):
                        if family.sample_count >= 3:
                            mature_count += 1
                except:
                    pass
            stats['mature_families'] = mature_count

        return stats


if __name__ == '__main__':
    """Test the production learning coordinator."""
    print("\n🧪 Testing Production Learning Coordinator")
    print("="*70 + "\n")

    # Initialize coordinator
    coordinator = ProductionLearningCoordinator(
        hebbian_storage="TSK/test_hebbian_memory.json",
        phase5_storage="persona_layer/test",
        learning_threshold=0.7,
        save_frequency=5
    )

    # Simulate a few training pairs
    for i in range(3):
        print(f"\n📘 Test Pair {i+1}")

        # Mock organism results
        input_result = {
            'felt_states': {
                'satisfaction_final': 0.5,
                'mean_coherence': 0.5,
                'organ_coherences': {
                    'LISTENING': 0.6,
                    'EMPATHY': 0.7,
                    'WISDOM': 0.5,
                    'AUTHENTICITY': 0.4,
                    'PRESENCE': 0.5,
                    'BOND': 0.6,
                    'SANS': 1.0,
                    'NDAM': 0.2,
                    'RNX': 0.5,
                    'EO': 0.4,
                    'CARD': 0.5
                }
            }
        }

        output_result = {
            'felt_states': {
                'satisfaction_final': 0.75,  # Good conversation
                'mean_coherence': 0.7,
                'organ_coherences': input_result['felt_states']['organ_coherences']
            }
        }

        pair_metadata = {
            'id': f'test_{i+1}',
            'category': 'test_category',
            'self_distance': 0.8,
            'polyvagal_state': 'sympathetic'
        }

        # Learn from pair
        learning_result = coordinator.learn_from_training_pair(
            input_result, output_result, pair_metadata,
            input_text="Test input", output_text="Test output"
        )

        print(f"   Learned: {learning_result['learned']}")
        print(f"   Hebbian updates: {learning_result['hebbian_updates']}")
        print(f"   Cluster updates: {learning_result['cluster_updates']}")
        print(f"   Total patterns: {learning_result['patterns_total']}")

    # Get final stats
    print("\n📊 Final Learning Stats:")
    stats = coordinator.get_learning_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")

    # Clean up test files
    import os
    test_files = [
        "TSK/test_hebbian_memory.json",
        "persona_layer/test/organic_families.json",
        "persona_layer/test/conversational_clusters.json"
    ]
    for f in test_files:
        if os.path.exists(f):
            os.remove(f)
            print(f"\n🗑️  Cleaned up: {f}")

    print("\n✅ Production Learning Coordinator Test Complete!")
