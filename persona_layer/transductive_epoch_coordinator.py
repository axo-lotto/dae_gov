"""
Transductive Epoch Coordinator - TSK-Based Epoch Learning Infrastructure
==========================================================================

Epoch coordinator that uses Transductive Summary Kernels (TSKs) for proper
transformation-based learning. Inspired by DAE 3.0's epoch learning system
that achieved 37 families with Zipf's law (R² > 0.85).

Key Innovation:
- Clusters TRANSFORMATIONS (how things change), not SNAPSHOTS (what they are)
- Complete TSK capture: INITIAL → FINAL felt-state transformation
- 57D transformation signatures for family clustering
- Progressive learning from transformation patterns

Architecture:
- Uses ConversationalTSKRecorder for TSK creation
- Integrates with existing wrapper (optional layer, doesn't break dae_interactive.py)
- Stores TSKs persistently for epoch replay
- FeltDifferenceLearner for transformation pattern learning

Expected Outcomes (from DAE 3.0):
- Epoch 20: 3-5 families (organ differentiation begins)
- Epoch 50: 15-25 families (mature taxonomy)
- Epoch 100: 20-30 families (Zipf's law emerges, R² > 0.85)

Created: November 16, 2025
Status: Core TSK-based epoch learning infrastructure
"""

import json
import time
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from dataclasses import asdict

# Import our new TSK infrastructure
from persona_layer.conversational_tsk_recorder import (
    ConversationalTSKRecorder,
    TransductiveSummaryKernel
)

# Import existing organism wrapper
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

# Import Phase 5 learning integration
try:
    from persona_layer.phase5_learning_integration import Phase5LearningIntegration
    PHASE5_AVAILABLE = True
except ImportError:
    PHASE5_AVAILABLE = False
    print("⚠️ Phase5LearningIntegration not available")


class TransductiveEpochCoordinator:
    """
    Epoch coordinator that uses Transductive Summary Kernels (TSKs) for
    transformation-based learning.

    Key Differences from MinimalEpochCoordinator:
    - Creates TSKs with complete INITIAL→FINAL transformation record
    - Clusters on 57D transformation signatures (not organ activation snapshots)
    - Stores TSKs persistently for epoch replay and pattern analysis
    - Supports FeltDifferenceLearner for learning what pathways work

    Usage:
    ------
    >>> coordinator = TransductiveEpochCoordinator()
    >>> results = coordinator.run_epoch(training_pairs, epoch_id=1)
    >>> coordinator.analyze_transformation_patterns()
    """

    def __init__(
        self,
        organism_wrapper: Optional[ConversationalOrganismWrapper] = None,
        state_dir: str = 'persona_layer/state/active',
        tsk_storage_dir: str = 'persona_layer/state/tsks',
        enable_auto_save: bool = True,
        enable_phase5: bool = True
    ):
        """
        Initialize transductive epoch coordinator.

        Args:
            organism_wrapper: ConversationalOrganismWrapper instance (creates one if None)
            state_dir: Directory for epoch state persistence
            tsk_storage_dir: Directory for TSK storage
            enable_auto_save: Auto-save epoch state after each epoch
            enable_phase5: Enable Phase 5 learning integration
        """
        # Initialize organism wrapper if not provided
        if organism_wrapper is None:
            self.organism = ConversationalOrganismWrapper()
        else:
            self.organism = organism_wrapper

        # Initialize TSK recorder
        self.tsk_recorder = ConversationalTSKRecorder(storage_dir=tsk_storage_dir)

        # State management
        self.state_dir = Path(state_dir)
        self.tsk_storage_dir = Path(tsk_storage_dir)
        self.enable_auto_save = enable_auto_save
        self.enable_phase5 = enable_phase5 and PHASE5_AVAILABLE

        # Epoch state
        self.current_epoch = 0
        self.total_epochs = 0
        self.epoch_history = []
        self.epoch_tsks = {}  # {epoch_id: [TSK objects]}

        # Learning metrics
        self.transformation_families = {}  # family_id -> [TSK signatures]
        self.family_centroids = {}  # family_id -> centroid signature

        # Initialize Phase 5 if available
        if self.enable_phase5:
            self.phase5_learner = Phase5LearningIntegration()
        else:
            self.phase5_learner = None

        # Ensure directories exist
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.tsk_storage_dir.mkdir(parents=True, exist_ok=True)

        # Load existing epoch state (resume training)
        self._load_epoch_state()

        print(f"✅ TransductiveEpochCoordinator initialized")
        print(f"   State directory: {self.state_dir}")
        print(f"   TSK storage: {self.tsk_storage_dir}")
        print(f"   Current epoch: {self.current_epoch}")
        print(f"   Phase 5 enabled: {self.enable_phase5}")
        print(f"   Total TSKs stored: {len(self.tsk_recorder)}")

    def run_epoch(
        self,
        training_pairs: List[Dict],
        epoch_id: int,
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        Run single epoch with TSK-based transformation learning.

        This creates complete TSK records for each conversation, enabling:
        - Transformation-based clustering (not snapshot clustering)
        - 57D signature computation from INITIAL→FINAL transformation
        - Proper family formation based on HOW things change

        Args:
            training_pairs: List of {id, input_text, expected_output} dicts
            epoch_id: Epoch number (1-indexed)
            verbose: Print progress messages

        Returns:
            Epoch statistics dict
        """
        if verbose:
            print(f"\n{'='*80}")
            print(f"🌀 TRANSDUCTIVE EPOCH {epoch_id}")
            print(f"{'='*80}")
            print(f"   Training pairs: {len(training_pairs)}")
            print(f"   TSK-based transformation learning enabled")
            print(f"{'='*80}\n")

        epoch_start = time.time()
        results = []
        epoch_tsks = []
        families_discovered = set()

        for i, pair in enumerate(training_pairs, 1):
            pair_id = pair.get('id', f'pair_{i}')
            conversation_id = f"epoch{epoch_id}_{pair_id}"

            if verbose:
                print(f"[{i}/{len(training_pairs)}] {pair_id}", end="")

            # === CRITICAL: TSK-based processing ===

            # Step 1: Create initial felt state (BEFORE processing)
            initial_state = self.tsk_recorder.create_initial_state()

            # Step 2: Process through organism wrapper
            result = self.organism.process_text(
                pair['input_text'],
                context={
                    'epoch_id': epoch_id,
                    'pair_id': pair_id,
                    'conversation_id': conversation_id,
                    'tsk_recording': True
                }
            )
            results.append(result)

            # Step 3: Extract final felt states from result
            final_felt_states = self._extract_final_felt_states(result)

            # Step 4: Extract transduction trajectory from result
            transduction_trajectory = self._extract_transduction_trajectory(result)

            # Step 5: Create TSK from INITIAL → FINAL transformation
            tsk = self.tsk_recorder.create_tsk_from_processing(
                conversation_id=conversation_id,
                user_input=pair['input_text'],
                initial_state=initial_state,
                final_felt_states=final_felt_states,
                transduction_trajectory=transduction_trajectory,
                response_text=result.get('emission', '')
            )
            epoch_tsks.append(tsk)

            # Step 6: Assign to transformation family (57D signature clustering)
            family_id, similarity, is_new = self._assign_to_transformation_family(tsk)
            families_discovered.add(family_id)

            # Store TSK persistently
            self.tsk_recorder.store_tsk(tsk, epoch_id=epoch_id)

            if verbose:
                action = "CREATED" if is_new else "JOINED"
                print(f" → {action} {family_id} (sim: {similarity:.3f}, "
                      f"V0: {tsk.initial_v0_energy:.2f}→{tsk.final_v0_energy:.2f})")

        # Store epoch TSKs
        self.epoch_tsks[epoch_id] = epoch_tsks

        # Aggregate epoch statistics
        epoch_stats = self._aggregate_epoch_stats(results, epoch_tsks, epoch_id)
        epoch_stats['duration'] = time.time() - epoch_start
        epoch_stats['families_discovered_this_epoch'] = len(families_discovered)
        epoch_stats['total_families'] = len(self.transformation_families)

        # Update state
        self.current_epoch = epoch_id
        self.epoch_history.append(epoch_stats)

        # Auto-save
        if self.enable_auto_save:
            self._save_epoch_state()
            self._save_family_centroids()

        # Print summary
        if verbose:
            self._print_epoch_summary(epoch_stats)

        return epoch_stats

    def _extract_final_felt_states(self, result: Dict) -> Dict:
        """
        Extract final felt states from organism processing result.

        Args:
            result: Result dict from organism.process_text()

        Returns:
            Final felt state dict for TSK creation
        """
        felt_states = result.get('felt_states', {})

        return {
            'v0_energy': felt_states.get('v0_energy_final', 0.5),
            'organ_coherences': felt_states.get('organ_coherences', {}),
            'polyvagal_state': felt_states.get('polyvagal_state', 'ventral_vagal'),
            'zone': felt_states.get('zone', 1),
            'urgency': felt_states.get('urgency', 0.0),
            'satisfaction': felt_states.get('satisfaction_final', 0.5),
            'emission_path': felt_states.get('emission_path', 'hebbian'),
            'confidence': result.get('confidence', 0.3),

            # Transduction-specific
            'nexus_type': felt_states.get('nexus_type', 'Relational'),
            'transduction_enabled': felt_states.get('transduction_enabled', False),

            # RNX/TSK dimensions
            'bond_constraint': felt_states.get('bond_constraint', 0.0),
            'ndam_urgency': felt_states.get('ndam_urgency', 0.0),
            'sans_coherence': felt_states.get('sans_coherence', 0.0),
            'eo_polyvagal': felt_states.get('eo_polyvagal', 0.5),
        }

    def _extract_transduction_trajectory(self, result: Dict) -> List[Dict]:
        """
        Extract multi-cycle transduction trajectory from organism result.

        Args:
            result: Result dict from organism.process_text()

        Returns:
            List of per-cycle transduction state dicts
        """
        felt_states = result.get('felt_states', {})
        trajectory = felt_states.get('transduction_trajectory', [])

        # Convert to dicts if they're NexusTransductionState objects
        trajectory_dicts = []
        for state in trajectory:
            if hasattr(state, '__dict__'):
                trajectory_dicts.append(vars(state))
            elif isinstance(state, dict):
                trajectory_dicts.append(state)

        return trajectory_dicts

    def _assign_to_transformation_family(
        self,
        tsk: TransductiveSummaryKernel
    ) -> Tuple[str, float, bool]:
        """
        Assign TSK to transformation family based on 57D signature similarity.

        This is the core of TSK-based learning:
        - Cluster HOW things transform, not WHAT they are
        - 57D signature captures transformation pattern
        - Families emerge from similar transformation patterns

        Args:
            tsk: Transductive Summary Kernel to assign

        Returns:
            Tuple of (family_id, similarity, is_new_family)
        """
        signature = np.array(tsk.transformation_signature)

        # If no families yet, create first one
        if not self.transformation_families:
            family_id = "TFamily_001"
            self.transformation_families[family_id] = [signature]
            self.family_centroids[family_id] = signature
            return family_id, 1.0, True

        # Find most similar family
        best_family = None
        best_similarity = -1

        for family_id, centroid in self.family_centroids.items():
            # Cosine similarity (signatures are L2 normalized)
            similarity = float(np.dot(signature, centroid))
            if similarity > best_similarity:
                best_similarity = similarity
                best_family = family_id

        # Adaptive threshold based on number of families
        threshold = self._get_adaptive_threshold()

        if best_similarity >= threshold:
            # Join existing family
            self.transformation_families[best_family].append(signature)
            # Update centroid (incremental mean)
            family_signatures = self.transformation_families[best_family]
            self.family_centroids[best_family] = np.mean(family_signatures, axis=0)
            return best_family, best_similarity, False
        else:
            # Create new family
            family_num = len(self.transformation_families) + 1
            family_id = f"TFamily_{family_num:03d}"
            self.transformation_families[family_id] = [signature]
            self.family_centroids[family_id] = signature
            return family_id, best_similarity, True

    def _get_adaptive_threshold(self) -> float:
        """
        Get adaptive similarity threshold based on family count.

        Follows DAE 3.0 pattern:
        - Few families (<8): 0.55 (aggressive exploration)
        - Medium (8-24): 0.65 (balanced growth)
        - Many (25+): 0.75 (consolidation)

        Returns:
            Similarity threshold (0-1)
        """
        num_families = len(self.transformation_families)

        if num_families < 8:
            return 0.55  # Aggressive exploration
        elif num_families < 25:
            return 0.65  # Balanced growth
        else:
            return 0.75  # Consolidation

    def _aggregate_epoch_stats(
        self,
        results: List[Dict],
        tsks: List[TransductiveSummaryKernel],
        epoch_id: int
    ) -> Dict[str, Any]:
        """
        Aggregate statistics from all TSKs in epoch.

        Args:
            results: List of organism processing results
            tsks: List of TSKs created this epoch
            epoch_id: Current epoch number

        Returns:
            Aggregated statistics dict
        """
        # Extract transformation metrics from TSKs
        v0_descents = [tsk.v0_energy_descent for tsk in tsks]
        convergence_cycles = [tsk.convergence_cycles for tsk in tsks]
        satisfactions = [tsk.final_satisfaction for tsk in tsks]
        confidences = [tsk.emission_confidence for tsk in tsks]

        # Constraint delta analysis
        bond_deltas = [tsk.bond_constraint_delta for tsk in tsks]
        ndam_deltas = [tsk.ndam_constraint_delta for tsk in tsks]
        sans_deltas = [tsk.sans_constraint_delta for tsk in tsks]
        eo_deltas = [tsk.eo_constraint_delta for tsk in tsks]

        # Kairos detection
        kairos_count = sum(1 for tsk in tsks if tsk.kairos_detected)

        # Signature variance (measure of transformation diversity)
        signatures = np.array([tsk.transformation_signature for tsk in tsks])
        signature_variance = float(np.var(signatures)) if len(signatures) > 1 else 0.0

        return {
            'epoch_id': epoch_id,
            'total_conversations': len(tsks),

            # Core transformation metrics
            'mean_v0_descent': float(np.mean(v0_descents)),
            'mean_convergence_cycles': float(np.mean(convergence_cycles)),
            'mean_satisfaction': float(np.mean(satisfactions)),
            'mean_confidence': float(np.mean(confidences)),

            # Constraint evolution
            'mean_bond_delta': float(np.mean(bond_deltas)),
            'mean_ndam_delta': float(np.mean(ndam_deltas)),
            'mean_sans_delta': float(np.mean(sans_deltas)),
            'mean_eo_delta': float(np.mean(eo_deltas)),

            # Learning progress
            'kairos_detection_rate': kairos_count / len(tsks) if tsks else 0.0,
            'signature_variance': signature_variance,

            # Timestamp
            'timestamp': datetime.now().isoformat()
        }

    def _print_epoch_summary(self, stats: Dict[str, Any]):
        """Print epoch summary with TSK-specific metrics."""
        print(f"\n{'─'*80}")
        print(f"📊 TRANSDUCTIVE EPOCH {stats['epoch_id']} SUMMARY")
        print(f"{'─'*80}")
        print(f"   Total conversations: {stats['total_conversations']}")
        print(f"   Mean V0 descent: {stats['mean_v0_descent']:.3f}")
        print(f"   Mean convergence cycles: {stats['mean_convergence_cycles']:.1f}")
        print(f"   Mean satisfaction: {stats['mean_satisfaction']:.3f}")
        print(f"   Mean confidence: {stats['mean_confidence']:.3f}")
        print(f"   Kairos detection rate: {stats['kairos_detection_rate']:.2%}")

        print(f"\n   Constraint Evolution:")
        print(f"      BOND Δ: {stats['mean_bond_delta']:+.4f}")
        print(f"      NDAM Δ: {stats['mean_ndam_delta']:+.4f}")
        print(f"      SANS Δ: {stats['mean_sans_delta']:+.4f}")
        print(f"      EO Δ: {stats['mean_eo_delta']:+.4f}")

        print(f"\n   Transformation Families:")
        print(f"      Total families: {stats.get('total_families', 0)}")
        print(f"      New families this epoch: {stats.get('families_discovered_this_epoch', 0)}")
        print(f"      Signature variance: {stats['signature_variance']:.6f}")

        print(f"\n   Duration: {stats.get('duration', 0):.1f}s")
        print(f"{'─'*80}\n")

    def run_training(
        self,
        training_pairs: List[Dict],
        num_epochs: int,
        verbose: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Run multi-epoch training with TSK-based transformation learning.

        Args:
            training_pairs: Training data
            num_epochs: Number of epochs to run
            verbose: Print progress

        Returns:
            List of epoch statistics (one per epoch)
        """
        self.total_epochs = num_epochs
        epoch_results = []

        print(f"\n{'='*80}")
        print(f"🚀 TRANSDUCTIVE EPOCH TRAINING")
        print(f"{'='*80}")
        print(f"   Total epochs: {num_epochs}")
        print(f"   Training pairs per epoch: {len(training_pairs)}")
        print(f"   TSK-based transformation learning: ENABLED")
        print(f"   Expected: 3-5 families by epoch 20, 15-25 by epoch 50")
        print(f"{'='*80}\n")

        for epoch_id in range(1, num_epochs + 1):
            epoch_stats = self.run_epoch(training_pairs, epoch_id, verbose)
            epoch_results.append(epoch_stats)

            # Check for family emergence (key metric)
            if verbose and epoch_id % 5 == 0:
                print(f"\n📈 Family Emergence Check (Epoch {epoch_id}):")
                print(f"   Total families: {len(self.transformation_families)}")
                self._analyze_zipf_distribution()

        if verbose:
            self._print_training_summary(epoch_results)

        return epoch_results

    def _analyze_zipf_distribution(self):
        """
        Analyze if family sizes follow Zipf's law.

        Zipf's law: size ∝ 1/rank
        Expected for self-organizing systems (R² > 0.85)
        """
        if len(self.transformation_families) < 3:
            print(f"   Not enough families for Zipf analysis (need ≥3)")
            return

        # Get family sizes
        sizes = [len(signatures) for signatures in self.transformation_families.values()]
        sizes.sort(reverse=True)

        # Compute Zipf correlation
        ranks = np.arange(1, len(sizes) + 1)
        log_ranks = np.log(ranks)
        log_sizes = np.log(sizes)

        # Linear regression in log-log space
        correlation = np.corrcoef(log_ranks, log_sizes)[0, 1]
        r_squared = correlation ** 2

        print(f"   Family sizes: {sizes[:5]}{'...' if len(sizes) > 5 else ''}")
        print(f"   Zipf R²: {r_squared:.3f} (target: >0.85)")

        if r_squared > 0.85:
            print(f"   ✅ Zipf's law emerging! Self-organization confirmed.")
        elif r_squared > 0.70:
            print(f"   📈 Progress toward Zipf's law")
        else:
            print(f"   🔄 More epochs needed for self-organization")

    def _print_training_summary(self, epoch_results: List[Dict]):
        """Print overall training summary."""
        print(f"\n{'='*80}")
        print(f"🎯 TRANSDUCTIVE TRAINING COMPLETE - {len(epoch_results)} EPOCHS")
        print(f"{'='*80}\n")

        print("Transformation Learning Progress:")
        print(f"{'Epoch':<8} {'V0 Descent':<12} {'Cycles':<8} {'Families':<10} {'Zipf':<10}")
        print(f"{'-'*8} {'-'*12} {'-'*8} {'-'*10} {'-'*10}")

        for stats in epoch_results:
            print(f"{stats['epoch_id']:<8} "
                  f"{stats['mean_v0_descent']:<12.3f} "
                  f"{stats['mean_convergence_cycles']:<8.1f} "
                  f"{stats.get('total_families', 0):<10} "
                  f"{stats['signature_variance']:<10.6f}")

        print(f"\n{'='*80}")
        print(f"Final State:")
        print(f"   Total families: {len(self.transformation_families)}")
        print(f"   Total TSKs stored: {len(self.tsk_recorder)}")
        print(f"   Adaptive threshold: {self._get_adaptive_threshold():.2f}")

        self._analyze_zipf_distribution()

        print(f"{'='*80}\n")

    def _save_epoch_state(self):
        """Persist epoch state to JSON for resumable training."""
        state = {
            'current_epoch': self.current_epoch,
            'total_epochs': self.total_epochs,
            'epoch_history': self.epoch_history,
            'total_families': len(self.transformation_families),
            'total_tsks': len(self.tsk_recorder),
            'last_updated': datetime.now().isoformat()
        }

        state_path = self.state_dir / 'transductive_epoch_state.json'

        with open(state_path, 'w') as f:
            json.dump(state, f, indent=2)

    def _save_family_centroids(self):
        """Save transformation family centroids to disk."""
        centroids_path = self.tsk_storage_dir / 'transformation_families.json'

        # Convert numpy arrays to lists for JSON serialization
        centroids_data = {
            family_id: centroid.tolist()
            for family_id, centroid in self.family_centroids.items()
        }

        data = {
            'centroids': centroids_data,
            'family_sizes': {
                family_id: len(sigs)
                for family_id, sigs in self.transformation_families.items()
            },
            'total_families': len(self.transformation_families),
            'adaptive_threshold': self._get_adaptive_threshold(),
            'last_updated': datetime.now().isoformat()
        }

        with open(centroids_path, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"💾 Saved {len(centroids_data)} transformation family centroids")

    def _load_epoch_state(self):
        """Load epoch state from JSON (resume training)."""
        state_path = self.state_dir / 'transductive_epoch_state.json'

        if not state_path.exists():
            return

        try:
            with open(state_path) as f:
                state = json.load(f)

            self.current_epoch = state.get('current_epoch', 0)
            self.total_epochs = state.get('total_epochs', 0)
            self.epoch_history = state.get('epoch_history', [])

            print(f"📂 Loaded existing transductive epoch state:")
            print(f"   Current epoch: {self.current_epoch}")
            print(f"   Total families: {state.get('total_families', 0)}")
            print(f"   Total TSKs: {state.get('total_tsks', 0)}")

        except Exception as e:
            print(f"⚠️  Failed to load epoch state: {e}")
            print(f"   Starting fresh")

        # Load family centroids
        centroids_path = self.tsk_storage_dir / 'transformation_families.json'
        if centroids_path.exists():
            try:
                with open(centroids_path) as f:
                    data = json.load(f)

                for family_id, centroid_list in data.get('centroids', {}).items():
                    self.family_centroids[family_id] = np.array(centroid_list)
                    # Reconstruct empty signatures list (centroids are what matter)
                    self.transformation_families[family_id] = []

                print(f"   Loaded {len(self.family_centroids)} family centroids")

            except Exception as e:
                print(f"⚠️  Failed to load family centroids: {e}")

    def get_transformation_insights(self) -> Dict[str, Any]:
        """
        Analyze transformation patterns across all TSKs.

        Returns:
            Dict with transformation insights
        """
        if not self.epoch_tsks:
            return {'error': 'No TSKs recorded yet'}

        # Flatten all TSKs
        all_tsks = []
        for tsks in self.epoch_tsks.values():
            all_tsks.extend(tsks)

        if not all_tsks:
            return {'error': 'No TSKs available'}

        # Analyze transformation patterns
        v0_descents = [tsk.v0_energy_descent for tsk in all_tsks]
        kairos_rate = sum(1 for tsk in all_tsks if tsk.kairos_detected) / len(all_tsks)

        # Dominant nexus types
        nexus_final_counts = {}
        for tsk in all_tsks:
            nexus_type = tsk.nexus_type_final
            nexus_final_counts[nexus_type] = nexus_final_counts.get(nexus_type, 0) + 1

        return {
            'total_tsks': len(all_tsks),
            'mean_v0_descent': float(np.mean(v0_descents)),
            'std_v0_descent': float(np.std(v0_descents)),
            'kairos_detection_rate': kairos_rate,
            'nexus_type_distribution': nexus_final_counts,
            'total_families': len(self.transformation_families),
            'adaptive_threshold': self._get_adaptive_threshold()
        }

    def save_training_history(self, output_path: str):
        """
        Save complete training history including TSK statistics.

        Args:
            output_path: Path to save training history JSON
        """
        history = {
            'coordinator_type': 'TransductiveEpochCoordinator',
            'epochs_completed': len(self.epoch_history),
            'total_tsks': len(self.tsk_recorder),
            'total_families': len(self.transformation_families),
            'epoch_history': self.epoch_history,
            'transformation_insights': self.get_transformation_insights(),
            'family_sizes': {
                family_id: len(sigs)
                for family_id, sigs in self.transformation_families.items()
            },
            'saved_at': datetime.now().isoformat()
        }

        with open(output_path, 'w') as f:
            json.dump(history, f, indent=2)

        print(f"💾 Training history saved to: {output_path}")


# Example usage & testing
if __name__ == "__main__":
    print("🌀 Transductive Epoch Coordinator - Standalone Test\n")

    # Create coordinator (will initialize organism wrapper automatically)
    coordinator = TransductiveEpochCoordinator()

    # Sample training data
    training_pairs = [
        {
            'id': 'burnout_1',
            'input_text': 'I feel completely exhausted and burned out',
            'expected_output': 'Witnessing presence for burnout'
        },
        {
            'id': 'safety_1',
            'input_text': 'This conversation feels really safe',
            'expected_output': 'Acknowledge safety and presence'
        },
        {
            'id': 'overwhelm_1',
            'input_text': 'I need some space from all of this',
            'expected_output': 'Honor need for space'
        }
    ]

    print("\n" + "="*80)
    print("STEP 1: Running single epoch with TSK-based learning...")
    print("="*80)

    results = coordinator.run_epoch(training_pairs, epoch_id=1, verbose=True)

    print("\n" + "="*80)
    print("STEP 2: Analyzing transformation insights...")
    print("="*80)

    insights = coordinator.get_transformation_insights()
    print(f"\nTransformation Insights:")
    print(f"   Total TSKs: {insights['total_tsks']}")
    print(f"   Mean V0 descent: {insights['mean_v0_descent']:.3f}")
    print(f"   Kairos rate: {insights['kairos_detection_rate']:.2%}")
    print(f"   Total families: {insights['total_families']}")

    print("\n✅ Transductive epoch coordinator test complete!")
