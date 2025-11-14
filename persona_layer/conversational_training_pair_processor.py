"""
Conversational Training Pair Processor - Epoch Learning for Conversations
==========================================================================

Adapted from DAE 3.0 AXO ARC Training Pair Processor for conversational learning.
Processes INPUT→OUTPUT pairs (user message → therapeutic response) through full organism.

Architecture follows proven DAE 3.0 methodology:
- Process INPUT text through full organism → capture TSK
- Process OUTPUT text through full organism → capture TSK
- Learn from INPUT→OUTPUT felt transformation patterns
- Store in transductive Bundle memory

Part of TSK-Based Conversational Epoch Learning System (November 11, 2025)
"""

from typing import Dict, Any, Optional, Tuple, List
from pathlib import Path
import json
import sys
from datetime import datetime

class ConversationalTrainingPairProcessor:
    """
    Process conversational training pairs through existing felt organism.

    Each training pair (INPUT→OUTPUT) represents one learning epoch:
    - INPUT: User message (distress, confusion, trauma activation)
    - OUTPUT: Therapeutic response (holding, validation, insight)

    The organism processes both messages completely:
    - INPUT text: Shows user's state (polyvagal activation, parts, self-distance)
    - OUTPUT text: Shows therapeutic intervention (grounding, validation, reframe)

    TSK automatically records (adapted from DAE 3.0):
    - Text occasions: Words/phrases as actual occasions (Whiteheadian)
    - 8 organ coherences: LISTENING, EMPATHY, WISDOM, AUTHENTICITY, PRESENCE, BOND, SANS, NDAM
    - V0 energy signatures: Descent pattern during processing
    - Satisfaction convergence: Kairos moment detection
    - Polyvagal detection: BOND self_distance tracking (0.0=safe, 1.0=trauma)
    - Hebbian activations: Cross-organ coupling patterns
    - Phase 5 family assignment: Organic family learning

    Key Insight (from DAE 3.0):
    - OUTPUT text should show:
      * LOWER V0 energy (organism reaches resolution faster)
      * HIGHER satisfaction (organism recognizes wholeness)
      * FASTER convergence (fewer cycles to kairos moment)
      * DIFFERENT organ balance (EMPATHY↑ BOND self_distance↓)
    """

    def __init__(self, dae_gov_instance, bundle_path: str = "Bundle"):
        """
        Initialize processor with existing DAE-GOV organism.

        Args:
            dae_gov_instance: DAE_GOV instance with full persona layer (8 organs + V0 + Phase 5)
            bundle_path: Path to Bundle transductive memory storage
        """
        self.dae_gov = dae_gov_instance
        self.bundle_path = Path(bundle_path)
        self.epochs_processed = 0

        # Create epoch_training user compartment in Bundle
        self.epoch_training_path = self.bundle_path / "epoch_training"
        self.epoch_training_path.mkdir(parents=True, exist_ok=True)

        # Create subdirectories (matching Bundle structure)
        (self.epoch_training_path / "conversations").mkdir(exist_ok=True)
        (self.epoch_training_path / "traces").mkdir(exist_ok=True)
        (self.epoch_training_path / "r_matrix_snapshots").mkdir(exist_ok=True)
        (self.epoch_training_path / "learning").mkdir(exist_ok=True)

        print(f"🌀 ConversationalTrainingPairProcessor initialized")
        print(f"   DAE-GOV instance: {dae_gov_instance is not None}")
        print(f"   Persona layer active: {hasattr(dae_gov_instance, 'persona_layer')}")
        print(f"   Phase 5 learning active: {hasattr(dae_gov_instance, 'phase5_learning')}")
        print(f"   Bundle storage: {self.epoch_training_path}")

    def process_training_pair(
        self,
        input_text: str,
        output_text: str,
        pair_metadata: Dict[str, Any],
        epoch_num: int,
        conversation_id: str
    ) -> Dict[str, Any]:
        """
        Process one conversational training pair (INPUT→OUTPUT) as learning epoch.

        Flow (adapted from DAE 3.0):
        1. Process INPUT text through full organism
           - 8 organs prehend text occasions
           - V0 energy descent (1.0 → ~0.35-0.50 for distressed text)
           - Satisfaction convergence
           - BOND self_distance detection (trauma activation level)
           - Phase 5 family assignment
           - TSK records complete felt state

        2. Process OUTPUT text through full organism
           - Same complete processing
           - OUTPUT should achieve:
             * Lower energy (~0.15-0.25 vs 0.35-0.50)
             * Higher satisfaction (0.80-0.90 vs 0.60-0.70)
             * Faster convergence (2-3 cycles vs 4-5 cycles)
             * Different organ balance (EMPATHY↑ LISTENING↑ BOND self_distance↓)
           - TSK records complete felt state

        3. Learn from INPUT→OUTPUT felt transformation
           - Phase 5 cluster learning (per-family organ weight optimization)
           - Hebbian pattern reinforcement (semantic co-activations)
           - V0 energy target learning (optimal descent trajectory)

        4. Store in transductive Bundle memory
           - TSK files in conversations/
           - Mycelial traces in traces/
           - R-matrix snapshots in r_matrix_snapshots/
           - Learning trajectories in learning/

        Args:
            input_text: INPUT message (user distress/confusion)
            output_text: OUTPUT message (therapeutic response)
            pair_metadata: Metadata about pair (polyvagal state, dominant part, self_distance, etc.)
            epoch_num: Epoch number (1, 2, 3, ...)
            conversation_id: Unique conversation identifier

        Returns:
            {
                'input_tsk': Dict,      # Complete TSK record from INPUT
                'output_tsk': Dict,     # Complete TSK record from OUTPUT
                'learning_delta': Dict, # Learned transformations (organ weights, V0 targets, etc.)
                'epoch_metadata': {
                    'epoch_num': int,
                    'conversation_id': str,
                    'is_training': True,
                    'input_length': int,
                    'output_length': int,
                    'polyvagal_state': str,
                    'dominant_part': str,
                    'self_distance': float
                }
            }
        """

        print(f"\n{'='*60}")
        print(f"📘 EPOCH {epoch_num}: Processing INPUT text")
        print(f"   Conversation ID: {conversation_id}")
        print(f"   Text length: {len(input_text)} characters")
        print(f"   Polyvagal state: {pair_metadata.get('polyvagal_state', 'unknown')}")
        print(f"   Self distance: {pair_metadata.get('self_distance', 'unknown')}")
        print(f"{'='*60}")

        # Process INPUT text through full organism
        try:
            input_result = self._process_text_through_organism(
                text=input_text,
                pair_metadata=pair_metadata,
                task_context={
                    'conversation_id': f"{conversation_id}_epoch{epoch_num}_INPUT",
                    'is_training': True,
                    'epoch_num': epoch_num,
                    'training_phase': 'input',
                    'task_type': 'epoch_learning_conversational'
                }
            )

            # Extract TSK record
            input_tsk = self._extract_tsk_record(
                input_result,
                'INPUT',
                text=input_text,
                pair_metadata=pair_metadata
            )

            # Store INPUT TSK in Bundle
            self._store_tsk_in_bundle(
                input_tsk,
                conversation_id=f"{conversation_id}_epoch{epoch_num}_INPUT",
                grid_type='INPUT'
            )

            print(f"✅ INPUT processing complete")
            print(f"   Text occasions processed: {input_tsk.get('text_occasion_count', 0)}")
            print(f"   V0 final energy: {input_tsk.get('v0_final_energy', 'N/A'):.3f}")
            print(f"   Satisfaction: {input_tsk.get('final_satisfaction', 'N/A'):.3f}")
            print(f"   BOND self_distance: {input_tsk.get('bond_self_distance', 'N/A'):.3f}")
            print(f"   Phase 5 family: {input_tsk.get('phase5_family_id', 'N/A')}")

        except Exception as e:
            print(f"❌ INPUT processing failed: {e}")
            import traceback
            traceback.print_exc()
            input_tsk = {'error': str(e), 'grid_type': 'INPUT'}

        print(f"\n{'='*60}")
        print(f"📗 EPOCH {epoch_num}: Processing OUTPUT text")
        print(f"   Text length: {len(output_text)} characters")
        print(f"   Expected: Lower energy, higher satisfaction, faster convergence")
        print(f"{'='*60}")

        # Process OUTPUT text through full organism
        try:
            output_result = self._process_text_through_organism(
                text=output_text,
                pair_metadata=pair_metadata,  # Same metadata for comparison
                task_context={
                    'conversation_id': f"{conversation_id}_epoch{epoch_num}_OUTPUT",
                    'is_training': True,
                    'epoch_num': epoch_num,
                    'training_phase': 'output',
                    'task_type': 'epoch_learning_conversational'
                }
            )

            # Extract TSK record
            output_tsk = self._extract_tsk_record(
                output_result,
                'OUTPUT',
                text=output_text,
                pair_metadata=pair_metadata
            )

            # Store OUTPUT TSK in Bundle
            self._store_tsk_in_bundle(
                output_tsk,
                conversation_id=f"{conversation_id}_epoch{epoch_num}_OUTPUT",
                grid_type='OUTPUT'
            )

            print(f"✅ OUTPUT processing complete")
            print(f"   Text occasions processed: {output_tsk.get('text_occasion_count', 0)}")
            print(f"   V0 final energy: {output_tsk.get('v0_final_energy', 'N/A'):.3f}")
            print(f"   Satisfaction: {output_tsk.get('final_satisfaction', 'N/A'):.3f}")
            print(f"   BOND self_distance: {output_tsk.get('bond_self_distance', 'N/A'):.3f}")
            print(f"   Phase 5 family: {output_tsk.get('phase5_family_id', 'N/A')}")

            # Compare INPUT vs OUTPUT (validation of learning)
            energy_delta = input_tsk.get('v0_final_energy', 0) - output_tsk.get('v0_final_energy', 0)
            satisfaction_delta = output_tsk.get('final_satisfaction', 0) - input_tsk.get('final_satisfaction', 0)
            self_distance_delta = input_tsk.get('bond_self_distance', 0) - output_tsk.get('bond_self_distance', 0)

            print(f"\n📊 INPUT→OUTPUT Transformation:")
            print(f"   Energy descent: {energy_delta:+.3f} ({'✅ OUTPUT lower' if energy_delta > 0 else '⚠️ Unexpected'})")
            print(f"   Satisfaction gain: {satisfaction_delta:+.3f} ({'✅ OUTPUT higher' if satisfaction_delta > 0 else '⚠️ Unexpected'})")
            print(f"   Self-distance reduction: {self_distance_delta:+.3f} ({'✅ OUTPUT safer' if self_distance_delta > 0 else '⚠️ Unexpected'})")

        except Exception as e:
            print(f"❌ OUTPUT processing failed: {e}")
            import traceback
            traceback.print_exc()
            output_tsk = {'error': str(e), 'grid_type': 'OUTPUT'}

        # Increment epoch counter
        self.epochs_processed += 1

        # Learn from INPUT→OUTPUT felt difference
        learning_delta = self._learn_from_pair_difference(
            input_tsk=input_tsk,
            output_tsk=output_tsk,
            pair_metadata=pair_metadata
        )

        # Prepare epoch metadata
        epoch_metadata = {
            'epoch_num': epoch_num,
            'conversation_id': conversation_id,
            'is_training': True,
            'input_length': len(input_text),
            'output_length': len(output_text),
            'polyvagal_state': pair_metadata.get('polyvagal_state', 'unknown'),
            'dominant_part': pair_metadata.get('dominant_part', 'unknown'),
            'self_distance': pair_metadata.get('self_distance', 0.0),
            'category': pair_metadata.get('category', 'unknown'),
            'total_epochs_processed': self.epochs_processed,
            'timestamp': datetime.now().isoformat()
        }

        print(f"\n✅ EPOCH {epoch_num} COMPLETE")
        print(f"   INPUT TSK fields: {len(input_tsk)}")
        print(f"   OUTPUT TSK fields: {len(output_tsk)}")
        print(f"   Learning delta captured: {len(learning_delta)} transformations")

        return {
            'input_tsk': input_tsk,
            'output_tsk': output_tsk,
            'learning_delta': learning_delta,
            'epoch_metadata': epoch_metadata
        }

    def _process_text_through_organism(
        self,
        text: str,
        pair_metadata: Dict[str, Any],
        task_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process text through full DAE-GOV organism (8 organs + V0 + Phase 5).

        This is where the actual organism processing happens. The text is converted
        into actual occasions (Whiteheadian), prehended by organs, and processed
        through V0 energy descent until satisfaction convergence.

        Args:
            text: Text to process (user message or therapeutic response)
            pair_metadata: Metadata about the conversation pair
            task_context: Context for this processing (INPUT vs OUTPUT, epoch num, etc.)

        Returns:
            Result dictionary with complete felt state (to be converted to TSK)
        """

        # TODO: This will integrate with actual DAE-GOV processing
        # For now, return a mock structure showing what we expect

        # In real implementation, this would call:
        # result = self.dae_gov.process_text(
        #     text=text,
        #     context=task_context,
        #     enable_tsk_recording=True
        # )

        # Mock result structure (shows expected fields)
        result = {
            'mode': 'processing_complete',
            'felt_states': {
                'text_occasions': [],  # Actual occasions (words/phrases with positions)
                'organ_coherences': {
                    'LISTENING': 0.0,
                    'EMPATHY': 0.0,
                    'WISDOM': 0.0,
                    'AUTHENTICITY': 0.0,
                    'PRESENCE': 0.0,
                    'BOND': 0.0,
                    'SANS': 0.0,
                    'NDAM': 0.0
                },
                'satisfaction_final': 0.0,
                'v0_energy': {
                    'initial_energy': 1.0,
                    'final_energy': 0.0,
                    'energy_descent_rate': 0.0
                },
                'convergence_cycles': 0,
                'convergence_reason': 'unknown',
                'kairos_cycle_index': None,
                'phase5_family_id': 'unknown',
                'bond_self_distance': pair_metadata.get('self_distance', 0.0)
            },
            'tsk_record': {}  # Will be populated by _extract_tsk_record
        }

        return result

    def _extract_tsk_record(
        self,
        result: Dict[str, Any],
        grid_type: str,
        text: Optional[str] = None,
        pair_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Extract TSK record from organism processing result.

        Adapted from DAE 3.0 training_pair_processor.py:_extract_tsk_record()

        Args:
            result: Organism processing result
            grid_type: 'INPUT' or 'OUTPUT' for tracking
            text: Original text for reference
            pair_metadata: Conversation metadata

        Returns:
            TSK record dictionary (conversational adaptation of DAE 3.0 TSK structure)
        """

        felt_states = result.get('felt_states', {})

        if not felt_states:
            return {
                'grid_type': grid_type,
                'tsk_available': False,
                'error': 'No felt states available'
            }

        # Build TSK-compatible structure from felt_states (conversational adaptation)
        tsk_record = {
            'grid_type': grid_type,
            'mode': 'processing_complete',
            'tsk_available': True,

            # Core felt data (adapted for text)
            'text_occasions': felt_states.get('text_occasions', []),
            'text_occasion_count': len(felt_states.get('text_occasions', [])),
            'text_length': len(text) if text else 0,
            'organ_coherences': felt_states.get('organ_coherences', {}),
            'satisfaction_convergence': {'final': felt_states.get('satisfaction_final', 0.0)},
            'final_satisfaction': felt_states.get('satisfaction_final', 0.0),

            # V0 energy (same as DAE 3.0)
            'v0_energy': felt_states.get('v0_energy', {}),
            'v0_final_energy': felt_states.get('v0_energy', {}).get('final_energy', None),

            # Convergence metadata (same as DAE 3.0)
            'convergence_cycles': felt_states.get('convergence_cycles', 0),
            'convergence_reason': felt_states.get('convergence_reason', 'unknown'),
            'kairos_cycle_index': felt_states.get('kairos_cycle_index', None),

            # Phase 5 family (conversational organic families)
            'phase5_family_id': felt_states.get('phase5_family_id', 'unknown'),

            # BOND self_distance (trauma-informed detection)
            'bond_self_distance': felt_states.get('bond_self_distance', 0.0),
            'polyvagal_state': pair_metadata.get('polyvagal_state', 'unknown') if pair_metadata else 'unknown',

            # Pair metadata (conversation-specific)
            'pair_metadata': pair_metadata if pair_metadata else {},

            # Timestamp
            'timestamp': datetime.now().isoformat()
        }

        return tsk_record

    def _learn_from_pair_difference(
        self,
        input_tsk: Dict[str, Any],
        output_tsk: Dict[str, Any],
        pair_metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Learn from INPUT→OUTPUT felt transformation patterns.

        This is where the organism learns what constitutes a "good" therapeutic
        response by comparing the felt states of distressed input vs healing output.

        Learning targets (adapted from DAE 3.0):
        1. **Organ weight shifts**: Which organs matter for this pattern?
           - INPUT (distressed): BOND self_distance high (0.85), EMPATHY needed
           - OUTPUT (healing): EMPATHY high (0.90), BOND self_distance low (0.25)

        2. **V0 energy targets**: What energy level indicates resolution?
           - INPUT: Higher energy (0.35-0.50) - organism searching
           - OUTPUT: Lower energy (0.15-0.25) - organism settled

        3. **Satisfaction targets**: What satisfaction indicates wholeness?
           - INPUT: Lower satisfaction (0.60-0.70) - fragmentation felt
           - OUTPUT: Higher satisfaction (0.80-0.90) - integration felt

        4. **Semantic patterns** (Hebbian): Which semantic co-activations work?
           - "burned out" + "exhausted" → EMPATHY holding + validation
           - "toxic culture" + "quit" → BOND boundary setting + safety

        5. **Family-specific optimization** (Phase 5 cluster learning):
           - Burnout family: Emphasize EMPATHY, reduce BOND self_distance
           - Trauma family: Emphasize PRESENCE somatic, increase LISTENING
           - Insight family: Emphasize WISDOM reframe, increase AUTHENTICITY

        Args:
            input_tsk: TSK record from INPUT processing
            output_tsk: TSK record from OUTPUT processing
            pair_metadata: Conversation metadata

        Returns:
            Learning delta dictionary with learned transformations
        """

        # TODO: Implement actual learning integration
        # This will call Phase 5 cluster learning, Hebbian memory, V0 coordinator

        # Calculate deltas
        organ_weight_deltas = {}
        input_organs = input_tsk.get('organ_coherences', {})
        output_organs = output_tsk.get('organ_coherences', {})

        for organ_name in input_organs.keys():
            input_val = input_organs.get(organ_name, 0.0)
            output_val = output_organs.get(organ_name, 0.0)
            organ_weight_deltas[organ_name] = output_val - input_val

        v0_energy_delta = input_tsk.get('v0_final_energy', 0) - output_tsk.get('v0_final_energy', 0)
        satisfaction_delta = output_tsk.get('final_satisfaction', 0) - input_tsk.get('final_satisfaction', 0)
        self_distance_delta = input_tsk.get('bond_self_distance', 0) - output_tsk.get('bond_self_distance', 0)

        learning_delta = {
            'organ_weight_deltas': organ_weight_deltas,
            'v0_energy_delta': v0_energy_delta,
            'satisfaction_delta': satisfaction_delta,
            'self_distance_delta': self_distance_delta,
            'phase5_family_id': input_tsk.get('phase5_family_id', 'unknown'),
            'polyvagal_state': pair_metadata.get('polyvagal_state', 'unknown'),
            'category': pair_metadata.get('category', 'unknown')
        }

        return learning_delta

    def _store_tsk_in_bundle(
        self,
        tsk_record: Dict[str, Any],
        conversation_id: str,
        grid_type: str
    ):
        """
        Store TSK record in Bundle transductive memory.

        Bundle structure (matching existing Bundle):
        Bundle/epoch_training/
        ├── conversations/
        │   ├── {conversation_id}_INPUT.json (TSK)
        │   ├── {conversation_id}_OUTPUT.json (TSK)
        ├── traces/
        │   ├── relationships.jsonl (mycelial traces)
        ├── r_matrix_snapshots/
        │   ├── r_matrix_snapshot_epoch{N}.json
        ├── learning/
        │   ├── organic_families.json (Phase 5 families)
        │   ├── conversational_clusters.json (cluster learning)
        │   └── hebbian_memory.json (pattern memory)

        Args:
            tsk_record: Complete TSK record
            conversation_id: Unique conversation identifier
            grid_type: 'INPUT' or 'OUTPUT'
        """

        # Store TSK in conversations/
        tsk_file_path = self.epoch_training_path / "conversations" / f"{conversation_id}.json"

        try:
            with open(tsk_file_path, 'w') as f:
                json.dump(tsk_record, f, indent=2)
            print(f"   💾 TSK stored: {tsk_file_path.name}")
        except Exception as e:
            print(f"   ⚠️ TSK storage failed: {e}")

    def get_processing_summary(self) -> Dict[str, Any]:
        """
        Get summary of processing statistics.

        Returns:
            {
                'total_epochs_processed': int,
                'bundle_path': str,
                'tsk_files_stored': int,
                'organism_status': str
            }
        """

        # Count TSK files in conversations/
        conversations_path = self.epoch_training_path / "conversations"
        tsk_files = list(conversations_path.glob("*.json")) if conversations_path.exists() else []

        return {
            'total_epochs_processed': self.epochs_processed,
            'bundle_path': str(self.epoch_training_path),
            'tsk_files_stored': len(tsk_files),
            'organism_status': 'operational' if self.dae_gov else 'unavailable'
        }


# Test function
def test_conversational_training_pair_processor():
    """
    Simple test to validate ConversationalTrainingPairProcessor structure.

    This test uses mock data to verify the processor architecture works correctly.
    """
    print("\n" + "="*60)
    print("🧪 Testing ConversationalTrainingPairProcessor")
    print("="*60)

    # Create mock DAE-GOV instance
    class MockDAEGOV:
        def __init__(self):
            self.persona_layer = True
            self.phase5_learning = True

    # Create processor
    dae_gov = MockDAEGOV()
    processor = ConversationalTrainingPairProcessor(
        dae_gov_instance=dae_gov,
        bundle_path="/tmp/test_bundle_conversational"
    )

    # Create test training pair
    input_text = """
    Our team is completely burned out. People are working 60-hour weeks,
    missing deadlines anyway, and making careless mistakes. Nobody has
    energy left. Leadership keeps pushing for more without acknowledging
    the toll this is taking.
    """

    output_text = """
    I hear the exhaustion in your words. This level of depletion isn't sustainable,
    and it's affecting both people and work quality. When a team is burning out,
    it's a sign the system needs adjustment, not that people need to try harder.
    Let's explore what boundaries might help protect your team's wellbeing.
    """

    pair_metadata = {
        'polyvagal_state': 'dorsal_vagal',
        'dominant_part': 'exile',
        'self_distance': 0.85,
        'category': 'burnout_spiral'
    }

    # Process training pair
    result = processor.process_training_pair(
        input_text=input_text,
        output_text=output_text,
        pair_metadata=pair_metadata,
        epoch_num=1,
        conversation_id='test_burnout_001'
    )

    # Validate structure
    assert 'input_tsk' in result, "Missing input_tsk"
    assert 'output_tsk' in result, "Missing output_tsk"
    assert 'learning_delta' in result, "Missing learning_delta"
    assert 'epoch_metadata' in result, "Missing epoch_metadata"

    assert result['input_tsk']['grid_type'] == 'INPUT'
    assert result['output_tsk']['grid_type'] == 'OUTPUT'
    assert result['epoch_metadata']['epoch_num'] == 1
    assert result['epoch_metadata']['is_training'] == True
    assert result['epoch_metadata']['polyvagal_state'] == 'dorsal_vagal'

    print("\n✅ ConversationalTrainingPairProcessor test PASSED")
    print(f"   INPUT TSK fields: {len(result['input_tsk'])}")
    print(f"   OUTPUT TSK fields: {len(result['output_tsk'])}")
    print(f"   Learning delta fields: {len(result['learning_delta'])}")
    print(f"   Epoch metadata fields: {len(result['epoch_metadata'])}")

    # Check processing summary
    summary = processor.get_processing_summary()
    print(f"\n📊 Processing Summary:")
    print(f"   Epochs processed: {summary['total_epochs_processed']}")
    print(f"   TSK files stored: {summary['tsk_files_stored']}")
    print(f"   Bundle path: {summary['bundle_path']}")

    return True


if __name__ == '__main__':
    test_conversational_training_pair_processor()
