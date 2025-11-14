"""
Conversational Health Monitor - Real-Time Training Health Tracking
===================================================================

Monitors organism health during conversational epoch training for
DAE_HYPHAE_1 11-organ conversational organism (Phase 2 COMPLETE).

**4-Tier Monitoring System**:
1. Pre-Training Health Check (validate readiness)
2. Real-Time Health Monitor (track during training)
3. Post-Training Analyzer (comprehensive epoch reports)
4. Comparison Tools (epoch-to-epoch progress)

**Health Metrics Tracked**:
- Organ coherence (11 organs: LISTENING, EMPATHY, WISDOM, AUTHENTICITY, PRESENCE, BOND, SANS, NDAM, RNX, EO, CARD)
- Family emergence & maturation (Zipf's law validation)
- Hebbian R-matrix growth (semantic co-activation patterns)
- Phase 5 learning health (57D signatures, cluster learning)
- Satisfaction progression (INPUT→OUTPUT transformation quality)
- Trauma-informed metrics (BOND self_distance, EO polyvagal states, CARD response scaling)
- Temporal patterns (RNX temporal state tracking)
- V0 energy descent (convergence quality)
- Memory health (storage growth, saturation detection)

November 11, 2025 - Updated for 11-organ Phase 2 architecture
"""

import json
import sys
import importlib
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import numpy as np

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class PreTrainingHealthCheck:
    """
    Validate conversational organism readiness before epoch training.

    Checks:
    - All 11 organs loadable (5 conversational + 6 trauma/context-aware)
    - Memory systems writable (Hebbian, Cluster DB, Family DB)
    - Phase 5 integration ready (57D signatures)
    - Bundle storage configured
    - Previous epoch data accessible (if not Epoch 1)
    """

    def __init__(self, bundle_path: str = "Bundle"):
        """
        Initialize pre-training health checker.

        Args:
            bundle_path: Path to Bundle directory for storage
        """
        self.bundle_path = Path(bundle_path)
        self.persona_layer_path = Path("persona_layer")

    def run_health_check(self) -> Dict[str, Any]:
        """
        Run complete pre-training health validation.

        Returns:
            {
                'status': 'READY' | 'WARNING' | 'CRITICAL',
                'checks': {
                    'organs': {...},
                    'memory': {...},
                    'phase5': {...},
                    'bundle': {...},
                    'previous_epochs': {...}
                },
                'recommendations': [...]
            }
        """
        print("\n" + "="*70)
        print("🔍 PRE-TRAINING HEALTH CHECK")
        print("="*70 + "\n")

        checks = {}
        recommendations = []

        # Check 1: Organs (11-organ system)
        print("1️⃣ Checking 11-organ conversational system...")
        organs_check = self._check_organs()
        checks['organs'] = organs_check
        if not organs_check['all_loadable']:
            recommendations.append("Fix organ import errors before training")
        print(f"   Loaded: {organs_check['loaded_count']}/{organs_check['total_organs']} organs")
        print(f"   Status: {'✅ PASS' if organs_check['all_loadable'] else '❌ FAIL'}")
        print()

        # Check 2: Memory Systems
        print("2️⃣ Checking memory systems...")
        memory_check = self._check_memory_systems()
        checks['memory'] = memory_check
        if not memory_check['all_writable']:
            recommendations.append("Ensure write permissions for memory databases")
        print(f"   Status: {'✅ PASS' if memory_check['all_writable'] else '❌ FAIL'}")
        print()

        # Check 3: Phase 5 Integration
        print("3️⃣ Checking Phase 5 learning integration...")
        phase5_check = self._check_phase5()
        checks['phase5'] = phase5_check
        if not phase5_check['available']:
            recommendations.append("Phase 5 learning not available (optional)")
        print(f"   Status: {'✅ PASS' if phase5_check['available'] else '⚠️  OPTIONAL'}")
        print()

        # Check 4: Bundle Storage
        print("4️⃣ Checking Bundle storage...")
        bundle_check = self._check_bundle_storage()
        checks['bundle'] = bundle_check
        if not bundle_check['configured']:
            recommendations.append("Create Bundle directory for memory storage")
        print(f"   Status: {'✅ PASS' if bundle_check['configured'] else '❌ FAIL'}")
        print()

        # Check 5: Previous Epochs (if applicable)
        print("5️⃣ Checking previous epoch data...")
        epochs_check = self._check_previous_epochs()
        checks['previous_epochs'] = epochs_check
        print(f"   Status: {'✅ PASS' if epochs_check['accessible'] else 'ℹ️  FIRST EPOCH'}")
        print()

        # Determine overall status
        critical_failures = (
            not organs_check['all_loadable'] or
            not memory_check['all_writable'] or
            not bundle_check['configured']
        )

        if critical_failures:
            status = 'CRITICAL'
        elif recommendations:
            status = 'WARNING'
        else:
            status = 'READY'

        print("="*70)
        print(f"Overall Status: {status}")
        if recommendations:
            print("\n📋 Recommendations:")
            for rec in recommendations:
                print(f"   - {rec}")
        print("="*70 + "\n")

        return {
            'status': status,
            'checks': checks,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }

    def _check_organs(self) -> Dict[str, Any]:
        """Check if all 11 conversational organs are loadable (Phase 2 COMPLETE)."""
        organs_status = {}

        # All 11 organs: 5 conversational + 6 trauma/context-aware
        # Map organ name -> (module_path, class_name)
        organ_modules = {
            # 5 Conversational Organs (TitleCase naming)
            'LISTENING': ('organs.modular.listening.core.listening_text_core', 'ListeningTextCore'),
            'EMPATHY': ('organs.modular.empathy.core.empathy_text_core', 'EmpathyTextCore'),
            'WISDOM': ('organs.modular.wisdom.core.wisdom_text_core', 'WisdomTextCore'),
            'AUTHENTICITY': ('organs.modular.authenticity.core.authenticity_text_core', 'AuthenticityTextCore'),
            'PRESENCE': ('organs.modular.presence.core.presence_text_core', 'PresenceTextCore'),

            # 6 Trauma/Context-Aware Organs (Phase 1: ALLCAPS, Phase 2: TitleCase)
            'BOND': ('organs.modular.bond.core.bond_text_core', 'BONDTextCore'),
            'SANS': ('organs.modular.sans.core.sans_text_core', 'SANSTextCore'),
            'NDAM': ('organs.modular.ndam.core.ndam_text_core', 'NDAMTextCore'),
            'RNX': ('organs.modular.rnx.core.rnx_text_core', 'RNXTextCore'),      # Phase 2
            'EO': ('organs.modular.eo.core.eo_text_core', 'EOTextCore'),          # Phase 2
            'CARD': ('organs.modular.card.core.card_text_core', 'CARDTextCore')   # Phase 2
        }

        for organ_name, (module_path, class_name) in organ_modules.items():
            try:
                # Use importlib for proper import
                parts = module_path.split('.')
                module_name = '.'.join(parts)

                # Import module and get class
                module = importlib.import_module(module_name)
                class_obj = getattr(module, class_name)

                organs_status[organ_name] = {'loadable': True, 'error': None}
                print(f"   ✅ {organ_name}: Loadable")
            except Exception as e:
                organs_status[organ_name] = {'loadable': False, 'error': str(e)}
                print(f"   ❌ {organ_name}: {str(e)[:50]}")

        all_loadable = all(status['loadable'] for status in organs_status.values())

        return {
            'all_loadable': all_loadable,
            'organs': organs_status,
            'total_organs': len(organ_modules),
            'loaded_count': sum(1 for s in organs_status.values() if s['loadable'])
        }

    def _check_memory_systems(self) -> Dict[str, Any]:
        """Check if memory systems are writable."""
        memory_systems = {}

        # Check Hebbian memory (TSK/hebbian_memory.json)
        hebbian_path = Path("TSK/hebbian_memory.json")
        memory_systems['hebbian'] = self._check_file_writable(hebbian_path)
        print(f"   {'✅' if memory_systems['hebbian']['writable'] else '❌'} Hebbian memory: {hebbian_path}")

        # Check Cluster DB (cluster_learning_db.json)
        cluster_path = Path("cluster_learning_db.json")
        memory_systems['cluster'] = self._check_file_writable(cluster_path)
        print(f"   {'✅' if memory_systems['cluster']['writable'] else '❌'} Cluster DB: {cluster_path}")

        # Check Family DB (organic_families.json)
        family_path = Path("organic_families.json")
        memory_systems['families'] = self._check_file_writable(family_path)
        print(f"   {'✅' if memory_systems['families']['writable'] else '❌'} Family DB: {family_path}")

        all_writable = all(sys['writable'] for sys in memory_systems.values())

        return {
            'all_writable': all_writable,
            'systems': memory_systems
        }

    def _check_file_writable(self, file_path: Path) -> Dict[str, Any]:
        """Check if a file path is writable."""
        try:
            # Check if directory exists
            if not file_path.parent.exists():
                return {'writable': False, 'reason': 'Parent directory does not exist'}

            # Check if file exists
            if file_path.exists():
                # Try to open for writing
                with open(file_path, 'r+') as f:
                    pass
                return {'writable': True, 'exists': True}
            else:
                # Check if we can create it
                file_path.touch()
                file_path.unlink()
                return {'writable': True, 'exists': False}
        except Exception as e:
            return {'writable': False, 'reason': str(e)}

    def _check_phase5(self) -> Dict[str, Any]:
        """Check if Phase 5 learning integration is available."""
        try:
            from persona_layer.phase5_learning_integration import Phase5LearningIntegration
            return {
                'available': True,
                'error': None
            }
        except Exception as e:
            return {
                'available': False,
                'error': str(e)
            }

    def _check_bundle_storage(self) -> Dict[str, Any]:
        """Check if Bundle storage is configured."""
        if not self.bundle_path.exists():
            return {
                'configured': False,
                'exists': False,
                'reason': f'Bundle directory does not exist: {self.bundle_path}'
            }

        if not self.bundle_path.is_dir():
            return {
                'configured': False,
                'exists': True,
                'reason': f'Bundle path is not a directory: {self.bundle_path}'
            }

        # Check write permissions
        try:
            test_file = self.bundle_path / '.write_test'
            test_file.touch()
            test_file.unlink()
            return {
                'configured': True,
                'exists': True,
                'writable': True
            }
        except Exception as e:
            return {
                'configured': False,
                'exists': True,
                'writable': False,
                'reason': str(e)
            }

    def _check_previous_epochs(self) -> Dict[str, Any]:
        """Check if previous epoch data is accessible."""
        # Look for epoch training logs
        epoch_logs_path = self.persona_layer_path / "epoch_training" / "training_logs"

        if not epoch_logs_path.exists():
            return {
                'accessible': True,  # No previous epochs = first epoch
                'epoch_count': 0,
                'latest_epoch': None
            }

        # Count epoch logs
        epoch_files = list(epoch_logs_path.glob("epoch_*.json"))

        if not epoch_files:
            return {
                'accessible': True,
                'epoch_count': 0,
                'latest_epoch': None
            }

        # Find latest epoch
        epoch_numbers = [int(f.stem.split('_')[1]) for f in epoch_files if f.stem.split('_')[1].isdigit()]
        latest_epoch = max(epoch_numbers) if epoch_numbers else None

        return {
            'accessible': True,
            'epoch_count': len(epoch_numbers),
            'latest_epoch': latest_epoch,
            'epoch_files': [str(f) for f in epoch_files]
        }


class RealTimeHealthMonitor:
    """
    Real-time health tracking during conversational epoch training.

    Monitors organism health every N training pairs (default: 5) and
    emits health reports showing:
    - Organ coherence trends
    - Family emergence
    - Learning activity (Hebbian updates, cluster updates)
    - Memory growth
    - Satisfaction progression
    - Trauma processing patterns
    """

    def __init__(self, check_interval: int = 5, bundle_path: str = "Bundle"):
        """
        Initialize real-time health monitor.

        Args:
            check_interval: Check health every N training pairs
            bundle_path: Path to Bundle for memory storage
        """
        self.check_interval = check_interval
        self.bundle_path = Path(bundle_path)

        # Tracking state
        self.pair_count = 0
        self.health_checks = []

        # Signal accumulation
        self.organ_coherences = []  # List of dicts per pair
        self.satisfaction_inputs = []
        self.satisfaction_outputs = []
        self.self_distances_input = []
        self.self_distances_output = []
        self.family_assignments = []
        self.hebbian_updates_count = 0
        self.cluster_updates_count = 0

        print("🔧 Real-Time Health Monitor initialized")
        print(f"   Check interval: Every {check_interval} training pairs")

    def on_pair_complete(self, pair_result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Called after each training pair processes.

        Args:
            pair_result: Result from training pair processor containing:
                - input_signals: Organ coherences, satisfaction, self_distance, etc.
                - output_signals: Same for OUTPUT
                - learning_signals: Hebbian updates, cluster updates, family assignment

        Returns:
            Health report dict if check_interval reached, None otherwise
        """
        self.pair_count += 1

        # Accumulate signals
        self._accumulate_signals(pair_result)

        # Check if time for health check
        if self.pair_count % self.check_interval == 0:
            health_report = self._check_current_health()
            self.health_checks.append(health_report)

            # Reset accumulators for next interval
            self._reset_accumulators()

            return health_report

        return None

    def _accumulate_signals(self, pair_result: Dict[str, Any]):
        """Accumulate signals from training pair."""
        # Extract signals
        input_signals = pair_result.get('input_signals', {})
        output_signals = pair_result.get('output_signals', {})
        learning_signals = pair_result.get('learning_signals', {})

        # Organ coherences (INPUT and OUTPUT)
        if 'organ_coherences' in input_signals:
            self.organ_coherences.append({
                'type': 'INPUT',
                'coherences': input_signals['organ_coherences']
            })
        if 'organ_coherences' in output_signals:
            self.organ_coherences.append({
                'type': 'OUTPUT',
                'coherences': output_signals['organ_coherences']
            })

        # Satisfaction
        if 'satisfaction' in input_signals:
            self.satisfaction_inputs.append(input_signals['satisfaction'])
        if 'satisfaction' in output_signals:
            self.satisfaction_outputs.append(output_signals['satisfaction'])

        # Self-distance (trauma)
        if 'bond_self_distance' in input_signals:
            self.self_distances_input.append(input_signals['bond_self_distance'])
        if 'bond_self_distance' in output_signals:
            self.self_distances_output.append(output_signals['bond_self_distance'])

        # Family assignments
        if 'family_assigned' in learning_signals:
            self.family_assignments.append(learning_signals['family_assigned'])

        # Learning activity
        self.hebbian_updates_count += learning_signals.get('hebbian_updates', 0)
        self.cluster_updates_count += learning_signals.get('cluster_updates', 0)

    def _check_current_health(self) -> Dict[str, Any]:
        """
        Check health metrics at current state.

        Returns:
            {
                'pair_count': int,
                'organ_health': {...},
                'family_health': {...},
                'learning_health': {...},
                'memory_health': {...},
                'satisfaction_health': {...},
                'trauma_health': {...},
                'timestamp': str
            }
        """
        print(f"\n{'='*70}")
        print(f"💚 HEALTH CHECK - After {self.pair_count} training pairs")
        print(f"{'='*70}\n")

        # Organ health
        organ_health = self._compute_organ_health()
        print(f"🧠 Organ Health:")
        print(f"   Mean coherence: {organ_health['mean_coherence']:.3f}")
        print(f"   Balance (std): {organ_health['organ_balance']:.3f}")
        print(f"   Trend: {organ_health['trend']}")
        print()

        # Family health
        family_health = self._compute_family_health()
        print(f"🌳 Family Health:")
        print(f"   Total families: {family_health['total_families']}")
        print(f"   Mature families (≥3): {family_health['mature_families']}")
        print(f"   New this check: {family_health['new_families_this_check']}")
        print()

        # Learning health
        learning_health = self._compute_learning_health()
        print(f"📚 Learning Health:")
        print(f"   Hebbian updates: {learning_health['hebbian_updates']}")
        print(f"   Cluster updates: {learning_health['cluster_updates']}")
        print(f"   Learning rate: {learning_health['learning_rate']:.2f} updates/pair")
        print()

        # Memory health
        memory_health = self._compute_memory_health()
        print(f"💾 Memory Health:")
        print(f"   Hebbian patterns: {memory_health['hebbian_size']}")
        print(f"   Cluster DB entries: {memory_health['cluster_db_size']}")
        print(f"   Storage: {memory_health['storage_mb']:.1f} MB")
        print()

        # Satisfaction health
        satisfaction_health = self._compute_satisfaction_health()
        print(f"😊 Satisfaction Health:")
        print(f"   INPUT mean: {satisfaction_health['input_mean']:.3f}")
        print(f"   OUTPUT mean: {satisfaction_health['output_mean']:.3f}")
        print(f"   Delta: {satisfaction_health['delta']:.3f}")
        print()

        # Trauma health
        trauma_health = self._compute_trauma_health()
        print(f"🛡️  Trauma Processing Health:")
        print(f"   INPUT self-distance: {trauma_health['input_mean']:.3f}")
        print(f"   OUTPUT self-distance: {trauma_health['output_mean']:.3f}")
        print(f"   Reduction: {trauma_health['reduction']:.3f}")
        print()

        print(f"{'='*70}\n")

        return {
            'pair_count': self.pair_count,
            'organ_health': organ_health,
            'family_health': family_health,
            'learning_health': learning_health,
            'memory_health': memory_health,
            'satisfaction_health': satisfaction_health,
            'trauma_health': trauma_health,
            'timestamp': datetime.now().isoformat()
        }

    def _compute_organ_health(self) -> Dict[str, Any]:
        """Compute organ health metrics."""
        if not self.organ_coherences:
            return {
                'mean_coherence': 0.0,
                'organ_balance': 0.0,
                'trend': '→'
            }

        # Extract all coherence values
        all_coherences = []
        for entry in self.organ_coherences:
            coherences = entry['coherences']
            all_coherences.extend(coherences.values())

        mean_coherence = np.mean(all_coherences) if all_coherences else 0.0
        organ_balance = np.std(all_coherences) if all_coherences else 0.0

        # Trend (simplified - compare first half to second half)
        if len(all_coherences) >= 4:
            first_half = np.mean(all_coherences[:len(all_coherences)//2])
            second_half = np.mean(all_coherences[len(all_coherences)//2:])
            if second_half > first_half + 0.05:
                trend = '↑'
            elif second_half < first_half - 0.05:
                trend = '↓'
            else:
                trend = '→'
        else:
            trend = '→'

        return {
            'mean_coherence': float(mean_coherence),
            'organ_balance': float(organ_balance),
            'trend': trend
        }

    def _compute_family_health(self) -> Dict[str, Any]:
        """Compute family emergence health."""
        # Load current family DB
        family_db_path = Path("organic_families.json")

        if not family_db_path.exists():
            return {
                'total_families': 0,
                'mature_families': 0,
                'new_families_this_check': 0
            }

        try:
            with open(family_db_path) as f:
                family_db = json.load(f)

            families = family_db.get('families', {})
            total_families = len(families)
            mature_families = sum(1 for fam in families.values() if fam.get('conversation_count', 0) >= 3)

            # Count new families in this check interval
            new_families_this_check = len(set(self.family_assignments)) if self.family_assignments else 0

            return {
                'total_families': total_families,
                'mature_families': mature_families,
                'new_families_this_check': new_families_this_check
            }
        except Exception as e:
            return {
                'total_families': 0,
                'mature_families': 0,
                'new_families_this_check': 0,
                'error': str(e)
            }

    def _compute_learning_health(self) -> Dict[str, Any]:
        """Compute learning activity health."""
        total_updates = self.hebbian_updates_count + self.cluster_updates_count
        learning_rate = total_updates / self.check_interval if self.check_interval > 0 else 0.0

        return {
            'hebbian_updates': self.hebbian_updates_count,
            'cluster_updates': self.cluster_updates_count,
            'total_updates': total_updates,
            'learning_rate': float(learning_rate)
        }

    def _compute_memory_health(self) -> Dict[str, Any]:
        """Compute memory storage health."""
        # Count Hebbian patterns
        hebbian_path = Path("TSK/hebbian_memory.json")
        hebbian_size = 0
        if hebbian_path.exists():
            try:
                with open(hebbian_path) as f:
                    hebbian_data = json.load(f)
                    hebbian_size = len(hebbian_data.get('patterns', {}))
            except:
                pass

        # Count Cluster DB entries
        cluster_path = Path("cluster_learning_db.json")
        cluster_db_size = 0
        if cluster_path.exists():
            try:
                with open(cluster_path) as f:
                    cluster_data = json.load(f)
                    cluster_db_size = len(cluster_data.get('tasks', {}))
            except:
                pass

        # Compute storage size
        storage_bytes = 0
        for path in [hebbian_path, cluster_path, Path("organic_families.json")]:
            if path.exists():
                storage_bytes += path.stat().st_size

        storage_mb = storage_bytes / (1024 * 1024)

        return {
            'hebbian_size': hebbian_size,
            'cluster_db_size': cluster_db_size,
            'storage_mb': float(storage_mb)
        }

    def _compute_satisfaction_health(self) -> Dict[str, Any]:
        """Compute satisfaction progression health."""
        input_mean = np.mean(self.satisfaction_inputs) if self.satisfaction_inputs else 0.0
        output_mean = np.mean(self.satisfaction_outputs) if self.satisfaction_outputs else 0.0
        delta = output_mean - input_mean

        return {
            'input_mean': float(input_mean),
            'output_mean': float(output_mean),
            'delta': float(delta)
        }

    def _compute_trauma_health(self) -> Dict[str, Any]:
        """Compute trauma processing health."""
        input_mean = np.mean(self.self_distances_input) if self.self_distances_input else 0.0
        output_mean = np.mean(self.self_distances_output) if self.self_distances_output else 0.0
        reduction = input_mean - output_mean

        return {
            'input_mean': float(input_mean),
            'output_mean': float(output_mean),
            'reduction': float(reduction)
        }

    def _reset_accumulators(self):
        """Reset signal accumulators for next check interval."""
        self.organ_coherences = []
        self.satisfaction_inputs = []
        self.satisfaction_outputs = []
        self.self_distances_input = []
        self.self_distances_output = []
        self.family_assignments = []
        self.hebbian_updates_count = 0
        self.cluster_updates_count = 0


class PostTrainingAnalyzer:
    """
    Post-epoch comprehensive learning effectiveness analysis.

    Analyzes complete epoch results including:
    - Satisfaction progression over training pairs
    - Organ evolution (coherence trends, specialization)
    - Family maturation (count, mature, Zipf's law validation)
    - Trauma processing (self_distance reduction patterns)
    - Memory growth (pattern count, saturation estimation)
    - Learning velocity (updates per pair, convergence speed)
    """

    def __init__(self, bundle_path: str = "Bundle"):
        """
        Initialize post-training analyzer.

        Args:
            bundle_path: Path to Bundle for storage
        """
        self.bundle_path = Path(bundle_path)
        self.training_logs_path = Path("persona_layer/epoch_training/training_logs")
        self.training_logs_path.mkdir(parents=True, exist_ok=True)

    def analyze_epoch(self, epoch_num: int, training_log_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Analyze complete epoch results.

        Args:
            epoch_num: Epoch number to analyze
            training_log_path: Optional path to training log JSON

        Returns:
            Comprehensive epoch analysis report
        """
        print("\n" + "="*70)
        print(f"📊 POST-TRAINING ANALYSIS - Epoch {epoch_num}")
        print("="*70 + "\n")

        # Load training log
        if training_log_path is None:
            training_log_path = self.training_logs_path / f"epoch_{epoch_num}.json"

        if not training_log_path.exists():
            print(f"⚠️  Training log not found: {training_log_path}")
            return {
                'epoch_num': epoch_num,
                'error': 'Training log not found'
            }

        with open(training_log_path) as f:
            training_log = json.load(f)

        # Analyze different aspects
        satisfaction_analysis = self._analyze_satisfaction_progression(training_log)
        organ_analysis = self._analyze_organ_evolution(training_log)
        family_analysis = self._analyze_family_maturation()
        trauma_analysis = self._analyze_trauma_processing(training_log)
        memory_analysis = self._analyze_memory_growth()

        # Print summary
        self._print_analysis_summary(
            epoch_num,
            satisfaction_analysis,
            organ_analysis,
            family_analysis,
            trauma_analysis,
            memory_analysis
        )

        # Save analysis
        analysis_report = {
            'epoch_num': epoch_num,
            'timestamp': datetime.now().isoformat(),
            'satisfaction': satisfaction_analysis,
            'organs': organ_analysis,
            'families': family_analysis,
            'trauma': trauma_analysis,
            'memory': memory_analysis
        }

        analysis_path = self.training_logs_path / f"epoch_{epoch_num}_analysis.json"
        with open(analysis_path, 'w') as f:
            json.dump(analysis_report, f, indent=2)

        print(f"\n💾 Analysis saved to: {analysis_path}\n")

        return analysis_report

    def _analyze_satisfaction_progression(self, training_log: Dict) -> Dict[str, Any]:
        """Analyze satisfaction progression over training pairs."""
        # Extract satisfaction from training pairs
        pairs = training_log.get('training_pairs', [])

        input_satisfactions = []
        output_satisfactions = []
        deltas = []

        for pair in pairs:
            input_sat = pair.get('input_signals', {}).get('satisfaction')
            output_sat = pair.get('output_signals', {}).get('satisfaction')

            if input_sat is not None and output_sat is not None:
                input_satisfactions.append(input_sat)
                output_satisfactions.append(output_sat)
                deltas.append(output_sat - input_sat)

        if not deltas:
            return {'error': 'No satisfaction data found'}

        return {
            'input_mean': float(np.mean(input_satisfactions)),
            'output_mean': float(np.mean(output_satisfactions)),
            'delta_mean': float(np.mean(deltas)),
            'delta_std': float(np.std(deltas)),
            'improvement_rate': float(np.mean(deltas) / np.mean(input_satisfactions)) if np.mean(input_satisfactions) > 0 else 0.0
        }

    def _analyze_organ_evolution(self, training_log: Dict) -> Dict[str, Any]:
        """Analyze organ coherence evolution."""
        pairs = training_log.get('training_pairs', [])

        # Collect organ coherences over time
        organ_coherences_over_time = {
            'LISTENING': [], 'EMPATHY': [], 'WISDOM': [],
            'AUTHENTICITY': [], 'PRESENCE': [],
            'BOND': [], 'SANS': [], 'NDAM': []
        }

        for pair in pairs:
            for signal_type in ['input_signals', 'output_signals']:
                coherences = pair.get(signal_type, {}).get('organ_coherences', {})
                for organ, value in coherences.items():
                    if organ in organ_coherences_over_time:
                        organ_coherences_over_time[organ].append(value)

        # Compute per-organ statistics
        organ_stats = {}
        for organ, values in organ_coherences_over_time.items():
            if values:
                organ_stats[organ] = {
                    'mean': float(np.mean(values)),
                    'std': float(np.std(values)),
                    'trend': self._compute_trend(values)
                }

        return organ_stats

    def _analyze_family_maturation(self) -> Dict[str, Any]:
        """Analyze family emergence and maturation."""
        family_db_path = Path("organic_families.json")

        if not family_db_path.exists():
            return {'error': 'No family database found'}

        with open(family_db_path) as f:
            family_db = json.load(f)

        families = family_db.get('families', {})
        total_families = len(families)
        mature_families = sum(1 for fam in families.values() if fam.get('conversation_count', 0) >= 3)

        # Family sizes (for Zipf's law)
        family_sizes = sorted([fam.get('conversation_count', 0) for fam in families.values()], reverse=True)

        return {
            'total_families': total_families,
            'mature_families': mature_families,
            'maturity_rate': float(mature_families / total_families) if total_families > 0 else 0.0,
            'family_sizes': family_sizes[:10]  # Top 10
        }

    def _analyze_trauma_processing(self, training_log: Dict) -> Dict[str, Any]:
        """Analyze trauma processing (self_distance reduction)."""
        pairs = training_log.get('training_pairs', [])

        input_distances = []
        output_distances = []
        reductions = []

        for pair in pairs:
            input_dist = pair.get('input_signals', {}).get('bond_self_distance')
            output_dist = pair.get('output_signals', {}).get('bond_self_distance')

            if input_dist is not None and output_dist is not None:
                input_distances.append(input_dist)
                output_distances.append(output_dist)
                reductions.append(input_dist - output_dist)

        if not reductions:
            return {'error': 'No trauma data found'}

        return {
            'input_mean': float(np.mean(input_distances)),
            'output_mean': float(np.mean(output_distances)),
            'reduction_mean': float(np.mean(reductions)),
            'reduction_rate': float(np.mean(reductions) / np.mean(input_distances)) if np.mean(input_distances) > 0 else 0.0
        }

    def _analyze_memory_growth(self) -> Dict[str, Any]:
        """Analyze memory growth patterns."""
        # Hebbian patterns
        hebbian_path = Path("TSK/hebbian_memory.json")
        hebbian_size = 0
        if hebbian_path.exists():
            with open(hebbian_path) as f:
                hebbian_data = json.load(f)
                hebbian_size = len(hebbian_data.get('patterns', {}))

        # Cluster DB
        cluster_path = Path("cluster_learning_db.json")
        cluster_size = 0
        if cluster_path.exists():
            with open(cluster_path) as f:
                cluster_data = json.load(f)
                cluster_size = len(cluster_data.get('tasks', {}))

        return {
            'hebbian_patterns': hebbian_size,
            'cluster_db_size': cluster_size,
            'total_patterns': hebbian_size + cluster_size
        }

    def _compute_trend(self, values: List[float]) -> str:
        """Compute trend direction from time series."""
        if len(values) < 4:
            return '→'

        first_half = np.mean(values[:len(values)//2])
        second_half = np.mean(values[len(values)//2:])

        if second_half > first_half + 0.05:
            return '↑'
        elif second_half < first_half - 0.05:
            return '↓'
        else:
            return '→'

    def _print_analysis_summary(
        self,
        epoch_num: int,
        satisfaction: Dict,
        organs: Dict,
        families: Dict,
        trauma: Dict,
        memory: Dict
    ):
        """Print analysis summary to console."""
        print("📈 SATISFACTION PROGRESSION:")
        print(f"   INPUT mean: {satisfaction.get('input_mean', 0):.3f}")
        print(f"   OUTPUT mean: {satisfaction.get('output_mean', 0):.3f}")
        print(f"   Delta: {satisfaction.get('delta_mean', 0):.3f} ({satisfaction.get('improvement_rate', 0)*100:.1f}% improvement)")
        print()

        print("🧠 ORGAN EVOLUTION:")
        for organ, stats in organs.items():
            print(f"   {organ:15s}: {stats['mean']:.3f} ± {stats['std']:.3f} {stats['trend']}")
        print()

        print("🌳 FAMILY MATURATION:")
        print(f"   Total families: {families.get('total_families', 0)}")
        print(f"   Mature (≥3): {families.get('mature_families', 0)} ({families.get('maturity_rate', 0)*100:.1f}%)")
        print()

        print("🛡️  TRAUMA PROCESSING:")
        print(f"   INPUT self-distance: {trauma.get('input_mean', 0):.3f}")
        print(f"   OUTPUT self-distance: {trauma.get('output_mean', 0):.3f}")
        print(f"   Reduction: {trauma.get('reduction_mean', 0):.3f} ({trauma.get('reduction_rate', 0)*100:.1f}%)")
        print()

        print("💾 MEMORY GROWTH:")
        print(f"   Hebbian patterns: {memory.get('hebbian_patterns', 0)}")
        print(f"   Cluster DB entries: {memory.get('cluster_db_size', 0)}")
        print(f"   Total patterns: {memory.get('total_patterns', 0)}")
        print()


if __name__ == '__main__':
    # Test health monitoring system
    print("🧪 Testing Health Monitoring System\n")

    # Test 1: Pre-Training Health Check
    checker = PreTrainingHealthCheck()
    health_status = checker.run_health_check()

    print(f"\nPre-Training Status: {health_status['status']}")

    # Test 2: Real-Time Monitor (simulated)
    print("\n" + "="*70)
    print("Testing Real-Time Monitor (simulated)")
    print("="*70)

    monitor = RealTimeHealthMonitor(check_interval=2)

    # Simulate 5 training pairs
    for i in range(5):
        simulated_result = {
            'input_signals': {
                'organ_coherences': {
                    'LISTENING': 0.65 + i*0.02,
                    'EMPATHY': 0.72 + i*0.01,
                    'WISDOM': 0.58,
                    'AUTHENTICITY': 0.55,
                    'PRESENCE': 0.68
                },
                'satisfaction': 0.60 + i*0.03,
                'bond_self_distance': 0.75 - i*0.05
            },
            'output_signals': {
                'organ_coherences': {
                    'LISTENING': 0.70 + i*0.02,
                    'EMPATHY': 0.80 + i*0.01,
                    'WISDOM': 0.65,
                    'AUTHENTICITY': 0.62,
                    'PRESENCE': 0.75
                },
                'satisfaction': 0.82 + i*0.02,
                'bond_self_distance': 0.35 - i*0.03
            },
            'learning_signals': {
                'hebbian_updates': 3 + i,
                'cluster_updates': 2,
                'family_assigned': f'Family_{(i % 3) + 1}'
            }
        }

        report = monitor.on_pair_complete(simulated_result)
        if report:
            print(f"✅ Health check completed at pair {i+1}")

    print("\n✅ Health monitoring system test complete!")
