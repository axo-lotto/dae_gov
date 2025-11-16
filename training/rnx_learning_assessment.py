#!/usr/bin/env python3
"""
RNX Learning Assessment - Comprehensive Whole-System Processing Assessment
============================================================================

This script assesses DAE's learning capabilities through whole-system processing
with RNX-enabled learning, tracking 57D transformation signatures and multi-family
emergence.

Key Features:
-------------
1. Whole-system processing assessment (all 12 organs)
2. RNX-enabled learning with 57D signatures
3. Multi-cycle transduction tracking
4. Organ differentiation metrics
5. TSK spinal cord validation
6. Family emergence trajectory
7. Transformation pattern analysis

Usage:
------
python3 training/rnx_learning_assessment.py --epochs 10 --reset --verbose

Expected Outcomes:
------------------
- Epoch 5: 3-5 families (organ differentiation visible)
- Epoch 10: 8-12 families (pattern diversity increasing)
- Epoch 20: 15-25 families (Zipf's law emergence)
- Signature variance: std > 0.15 across families

Created: November 16, 2025
Author: DAE_HYPHAE_1 Development Team
Status: TSK Spinal Cord Validation Post-Root-Cause Fix
"""

import json
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import numpy as np

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper


class RNXLearningAssessment:
    """
    Comprehensive assessment of DAE's learning capabilities through
    whole-system processing with RNX-enabled 57D signatures.
    """

    def __init__(
        self,
        reset_state: bool = False,
        verbose: bool = True
    ):
        """
        Initialize RNX Learning Assessment.

        Args:
            reset_state: Reset families, R-matrix, and organ confidence
            verbose: Print detailed progress
        """
        self.verbose = verbose
        self.reset_state = reset_state

        # Paths
        self.base_dir = Path(__file__).parent.parent
        self.state_dir = self.base_dir / "persona_layer" / "state" / "active"
        # The organism uses persona_layer/ root for families, not state/active/
        self.families_dir = self.base_dir / "persona_layer"
        self.results_dir = self.base_dir / "results" / "rnx_assessment"
        self.results_dir.mkdir(parents=True, exist_ok=True)

        # Initialize state tracking
        self.assessment_results = {
            'start_time': datetime.now().isoformat(),
            'epochs': [],
            'pre_assessment': None,
            'post_assessment': None,
            'learning_trajectory': [],
            'rnx_metrics': [],
            'tsk_validation': []
        }

        # Core test inputs covering all felt-state transformations
        self.test_corpus = self._build_test_corpus()

        print("\n" + "="*80)
        print("RNX LEARNING ASSESSMENT - WHOLE-SYSTEM PROCESSING")
        print("="*80)
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Test Corpus: {len(self.test_corpus)} diverse inputs")
        print(f"Reset State: {reset_state}")
        print(f"Results Dir: {self.results_dir}")

        # Reset state if requested
        if reset_state:
            self._reset_system_state()

        # Initialize organism
        print("\nInitializing Conversational Organism...")
        self.organism = ConversationalOrganismWrapper()
        print("   Organism ready")

        # Capture pre-assessment state
        self._capture_pre_assessment()

    def _build_test_corpus(self) -> List[Dict[str, Any]]:
        """Build comprehensive test corpus for RNX learning assessment."""
        return [
            # CRISIS / HIGH URGENCY (expect: sympathetic, zone 3-4, urgency 0.6-0.9)
            {
                'id': 'crisis_acute',
                'text': 'I am in crisis and need help right now!',
                'expected_polyvagal': 'sympathetic',
                'expected_zone': 3,
                'expected_urgency': 0.65,
                'category': 'crisis'
            },
            {
                'id': 'crisis_panic',
                'text': 'Everything is falling apart and I cant breathe',
                'expected_polyvagal': 'sympathetic',
                'expected_zone': 4,
                'expected_urgency': 0.8,
                'category': 'crisis'
            },
            {
                'id': 'crisis_overwhelm',
                'text': 'I feel like I am going to lose control completely',
                'expected_polyvagal': 'sympathetic',
                'expected_zone': 4,
                'expected_urgency': 0.75,
                'category': 'crisis'
            },

            # SAFETY / GROUNDING (expect: ventral, zone 1, urgency 0.0)
            {
                'id': 'safety_grounded',
                'text': 'I feel safe and grounded in this moment',
                'expected_polyvagal': 'ventral_vagal',
                'expected_zone': 1,
                'expected_urgency': 0.0,
                'category': 'safety'
            },
            {
                'id': 'safety_present',
                'text': 'This space feels calm and secure',
                'expected_polyvagal': 'ventral_vagal',
                'expected_zone': 1,
                'expected_urgency': 0.0,
                'category': 'safety'
            },
            {
                'id': 'safety_centered',
                'text': 'I am breathing easily and feeling at peace',
                'expected_polyvagal': 'ventral_vagal',
                'expected_zone': 1,
                'expected_urgency': 0.0,
                'category': 'safety'
            },

            # PROTECTIVE / BOUNDARIES (expect: mixed, zone 2-3, urgency 0.3-0.5)
            {
                'id': 'boundary_space',
                'text': 'I need some space right now to process this',
                'expected_polyvagal': 'mixed_state',
                'expected_zone': 2,
                'expected_urgency': 0.3,
                'category': 'boundary'
            },
            {
                'id': 'boundary_protection',
                'text': 'Part of me wants to protect myself from more hurt',
                'expected_polyvagal': 'mixed_state',
                'expected_zone': 3,
                'expected_urgency': 0.4,
                'category': 'boundary'
            },
            {
                'id': 'boundary_wall',
                'text': 'I notice walls going up when we discuss this',
                'expected_polyvagal': 'sympathetic',
                'expected_zone': 3,
                'expected_urgency': 0.35,
                'category': 'boundary'
            },

            # COLLAPSE / SHUTDOWN (expect: dorsal, zone 5, urgency 0.1-0.3)
            {
                'id': 'collapse_numb',
                'text': 'I feel completely numb and disconnected',
                'expected_polyvagal': 'dorsal_vagal',
                'expected_zone': 5,
                'expected_urgency': 0.15,
                'category': 'collapse'
            },
            {
                'id': 'collapse_frozen',
                'text': 'I cant move or think anymore I am just frozen',
                'expected_polyvagal': 'dorsal_vagal',
                'expected_zone': 5,
                'expected_urgency': 0.2,
                'category': 'collapse'
            },
            {
                'id': 'collapse_dissociated',
                'text': 'I feel far away from everything including myself',
                'expected_polyvagal': 'dorsal_vagal',
                'expected_zone': 5,
                'expected_urgency': 0.1,
                'category': 'collapse'
            },

            # RELATIONAL / CONNECTION (expect: ventral, zone 1-2, urgency 0.0-0.2)
            {
                'id': 'relational_trust',
                'text': 'I feel really understood when you listen like this',
                'expected_polyvagal': 'ventral_vagal',
                'expected_zone': 1,
                'expected_urgency': 0.0,
                'category': 'relational'
            },
            {
                'id': 'relational_vulnerable',
                'text': 'This space feels safe enough to be vulnerable',
                'expected_polyvagal': 'ventral_vagal',
                'expected_zone': 1,
                'expected_urgency': 0.1,
                'category': 'relational'
            },
            {
                'id': 'relational_gratitude',
                'text': 'Thank you for holding space for me',
                'expected_polyvagal': 'ventral_vagal',
                'expected_zone': 1,
                'expected_urgency': 0.0,
                'category': 'relational'
            },

            # RECURSIVE / LOOPING (expect: sympathetic, zone 3, urgency 0.4-0.6)
            {
                'id': 'recursive_rumination',
                'text': 'I keep going over the same thoughts again and again',
                'expected_polyvagal': 'sympathetic',
                'expected_zone': 3,
                'expected_urgency': 0.45,
                'category': 'recursive'
            },
            {
                'id': 'recursive_stuck',
                'text': 'I am stuck in this pattern and cant break free',
                'expected_polyvagal': 'sympathetic',
                'expected_zone': 3,
                'expected_urgency': 0.5,
                'category': 'recursive'
            },
            {
                'id': 'recursive_cycle',
                'text': 'Every time I try to move forward I end up back here',
                'expected_polyvagal': 'sympathetic',
                'expected_zone': 3,
                'expected_urgency': 0.5,
                'category': 'recursive'
            },

            # PARADOX / AMBIVALENCE (expect: mixed, zone 2-3, urgency 0.3-0.5)
            {
                'id': 'paradox_connection',
                'text': 'I want connection but I am also terrified of it',
                'expected_polyvagal': 'mixed_state',
                'expected_zone': 2,
                'expected_urgency': 0.4,
                'category': 'paradox'
            },
            {
                'id': 'paradox_help',
                'text': 'I need help but I also dont want to be a burden',
                'expected_polyvagal': 'mixed_state',
                'expected_zone': 2,
                'expected_urgency': 0.35,
                'category': 'paradox'
            },
            {
                'id': 'paradox_strength',
                'text': 'I feel strong but also completely broken inside',
                'expected_polyvagal': 'mixed_state',
                'expected_zone': 3,
                'expected_urgency': 0.45,
                'category': 'paradox'
            },
        ]

    def _reset_system_state(self):
        """Reset families, R-matrix, and organ confidence to fresh baseline."""
        print("\n--- RESETTING SYSTEM STATE ---")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Reset organic families - BOTH locations (organism uses persona_layer root)
        families_paths = [
            self.state_dir / "organic_families.json",  # state/active location
            self.families_dir / "organic_families.json"  # persona_layer root (where organism reads)
        ]

        for families_path in families_paths:
            if families_path.exists():
                backup_path = families_path.parent / f"organic_families_backup_{timestamp}.json"
                shutil.copy(families_path, backup_path)
                print(f"   Backed up families to: {backup_path}")

                fresh_families = {
                    "families": {},
                    "conversation_to_family": {},
                    "next_family_id": 1,
                    "total_families": 0,
                    "mature_families": 0,
                    "total_conversations": 0,
                    "last_updated": datetime.now().isoformat()
                }
                with open(families_path, 'w') as f:
                    json.dump(fresh_families, f, indent=2)
                print(f"   Reset families at: {families_path}")

        # Reset R-matrix (Hebbian memory)
        rmatrix_path = self.state_dir / "conversational_hebbian_memory.json"
        if rmatrix_path.exists():
            backup_path = rmatrix_path.parent / f"rmatrix_backup_{timestamp}.json"
            shutil.copy(rmatrix_path, backup_path)
            print(f"   Backed up R-matrix to: {backup_path}")

            fresh_rmatrix = {
                "r_matrix": [[0.0] * 11 for _ in range(11)],
                "last_updated": datetime.now().isoformat(),
                "reset_reason": f"RNX Learning Assessment Reset - {timestamp}",
                "r_matrix_metadata": {
                    "shape": [11, 11],
                    "learning_rate": 0.005,
                    "initialization": "zeros",
                    "purpose": "Fresh baseline for RNX learning assessment"
                }
            }
            with open(rmatrix_path, 'w') as f:
                json.dump(fresh_rmatrix, f, indent=2)
            print("   Reset R-matrix to zeros")

        # Reset organ confidence
        organ_conf_path = self.state_dir / "organ_confidence.json"
        if organ_conf_path.exists():
            backup_path = organ_conf_path.parent / f"organ_confidence_backup_{timestamp}.json"
            shutil.copy(organ_conf_path, backup_path)
            print(f"   Backed up organ confidence to: {backup_path}")

            organ_names = ['LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
                           'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD', 'NEXUS']
            fresh_confidence = {
                "organ_metrics": {},
                "last_updated": datetime.now().isoformat(),
                "total_organs": len(organ_names)
            }
            for organ in organ_names:
                fresh_confidence["organ_metrics"][organ] = {
                    "organ_name": organ,
                    "confidence": 0.5,
                    "success_count": 0,
                    "failure_count": 0,
                    "total_participations": 0,
                    "success_rate": 0.0,
                    "weight_multiplier": 1.0,
                    "last_updated": datetime.now().isoformat(),
                    "first_seen": datetime.now().isoformat()
                }
            with open(organ_conf_path, 'w') as f:
                json.dump(fresh_confidence, f, indent=2)
            print("   Reset organ confidence to neutral (0.5)")

        print("   System state reset complete\n")

    def _capture_pre_assessment(self):
        """Capture system state before training."""
        print("\n--- PRE-ASSESSMENT STATE ---")

        state = {
            'timestamp': datetime.now().isoformat(),
            'families': self._load_family_state(),
            'r_matrix': self._load_rmatrix_state(),
            'organ_confidence': self._load_organ_confidence()
        }

        self.assessment_results['pre_assessment'] = state

        print(f"   Total families: {state['families']['total_families']}")
        print(f"   R-matrix mean: {state['r_matrix']['mean']:.4f}")
        print(f"   Mean organ confidence: {state['organ_confidence']['mean_confidence']:.4f}")

    def _load_family_state(self) -> Dict[str, Any]:
        """Load current family clustering state."""
        # Use the path organism reads from (persona_layer root)
        families_path = self.families_dir / "organic_families.json"

        if not families_path.exists():
            return {
                'total_families': 0,
                'mature_families': 0,
                'total_conversations': 0,
                'family_sizes': [],
                'centroid_dimensions': []
            }

        with open(families_path, 'r') as f:
            data = json.load(f)

        family_info = {
            'total_families': data.get('total_families', len(data.get('families', {}))),
            'mature_families': data.get('mature_families', 0),
            'total_conversations': data.get('total_conversations', 0),
            'family_sizes': [],
            'centroid_dimensions': [],
            'family_details': {}
        }

        for fam_id, fam_data in data.get('families', {}).items():
            centroid = fam_data.get('centroid', [])
            member_count = fam_data.get('member_count', 0)
            family_info['family_sizes'].append(member_count)
            family_info['centroid_dimensions'].append(len(centroid))
            family_info['family_details'][fam_id] = {
                'members': member_count,
                'dimensions': len(centroid),
                'mean_satisfaction': fam_data.get('mean_satisfaction', 0.0)
            }

        return family_info

    def _load_rmatrix_state(self) -> Dict[str, Any]:
        """Load R-matrix (Hebbian memory) state."""
        rmatrix_path = self.state_dir / "conversational_hebbian_memory.json"

        if not rmatrix_path.exists():
            return {
                'mean': 0.0,
                'std': 0.0,
                'max': 0.0,
                'min': 0.0,
                'total_updates': 0
            }

        with open(rmatrix_path, 'r') as f:
            data = json.load(f)

        r_matrix = np.array(data.get('r_matrix', [[0.0] * 11] * 11))
        # Get upper triangle (excluding diagonal)
        upper_triangle = r_matrix[np.triu_indices_from(r_matrix, k=1)]

        return {
            'mean': float(np.mean(upper_triangle)),
            'std': float(np.std(upper_triangle)),
            'max': float(np.max(upper_triangle)),
            'min': float(np.min(upper_triangle)),
            'total_updates': data.get('r_matrix_metadata', {}).get('total_updates', 0)
        }

    def _load_organ_confidence(self) -> Dict[str, Any]:
        """Load organ confidence state."""
        organ_conf_path = self.state_dir / "organ_confidence.json"

        if not organ_conf_path.exists():
            return {
                'mean_confidence': 0.5,
                'std_confidence': 0.0,
                'mean_weight': 1.0,
                'organ_details': {}
            }

        with open(organ_conf_path, 'r') as f:
            data = json.load(f)

        confidences = []
        weights = []
        organ_details = {}

        for organ_name, metrics in data.get('organ_metrics', {}).items():
            conf = metrics.get('confidence', 0.5)
            weight = metrics.get('weight_multiplier', 1.0)
            confidences.append(conf)
            weights.append(weight)
            organ_details[organ_name] = {
                'confidence': conf,
                'weight': weight,
                'success_rate': metrics.get('success_rate', 0.0),
                'total_participations': metrics.get('total_participations', 0)
            }

        return {
            'mean_confidence': float(np.mean(confidences)) if confidences else 0.5,
            'std_confidence': float(np.std(confidences)) if confidences else 0.0,
            'mean_weight': float(np.mean(weights)) if weights else 1.0,
            'std_weight': float(np.std(weights)) if weights else 0.0,
            'organ_details': organ_details
        }

    def run_assessment(
        self,
        num_epochs: int = 10,
        save_intermediate: bool = True
    ) -> Dict[str, Any]:
        """
        Run comprehensive RNX learning assessment.

        Args:
            num_epochs: Number of training epochs
            save_intermediate: Save results after each epoch

        Returns:
            Complete assessment results
        """
        print(f"\n{'='*80}")
        print(f"STARTING RNX LEARNING ASSESSMENT - {num_epochs} EPOCHS")
        print(f"{'='*80}")

        for epoch in range(num_epochs):
            epoch_num = epoch + 1
            print(f"\n{'='*80}")
            print(f"EPOCH {epoch_num}/{num_epochs}")
            print(f"{'='*80}")

            epoch_results = self._run_epoch(epoch_num)
            self.assessment_results['epochs'].append(epoch_results)

            # Capture learning trajectory
            trajectory_snapshot = self._capture_learning_trajectory(epoch_num)
            self.assessment_results['learning_trajectory'].append(trajectory_snapshot)

            # RNX-specific metrics
            rnx_metrics = self._compute_rnx_metrics(epoch_results)
            self.assessment_results['rnx_metrics'].append(rnx_metrics)

            # TSK validation
            tsk_validation = self._validate_tsk_pipeline(epoch_results)
            self.assessment_results['tsk_validation'].append(tsk_validation)

            # Print epoch summary
            self._print_epoch_summary(epoch_num, epoch_results, trajectory_snapshot, rnx_metrics)

            # Save intermediate results
            if save_intermediate and epoch_num % 2 == 0:
                self._save_results(f"intermediate_epoch_{epoch_num}")

        # Final assessment
        print(f"\n{'='*80}")
        print(f"ASSESSMENT COMPLETE")
        print(f"{'='*80}")

        self._capture_post_assessment()
        self._print_final_report()
        self._save_results("final")

        return self.assessment_results

    def _run_epoch(self, epoch_num: int) -> Dict[str, Any]:
        """Run single assessment epoch."""
        epoch_results = {
            'epoch': epoch_num,
            'timestamp': datetime.now().isoformat(),
            'inputs_processed': 0,
            'processing_results': [],
            'organ_participation': {},
            'signature_stats': {},
            'transformation_patterns': {}
        }

        # Track organ participations
        organ_activations = {organ: [] for organ in [
            'LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
            'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD'
        ]}

        # Track transformation signatures
        signatures = []
        polyvagal_accuracy = []
        zone_accuracy = []
        urgency_errors = []

        for i, test_input in enumerate(self.test_corpus):
            if self.verbose and (i + 1) % 7 == 0:
                print(f"   Processing {i+1}/{len(self.test_corpus)}...")

            try:
                # Process through whole system
                result = self.organism.process_text(
                    text=test_input['text'],
                    context={
                        'conversation_id': f"rnx_epoch{epoch_num}_{test_input['id']}",
                        'enable_transduction': True
                    },
                    enable_phase2=True
                )

                # Extract results
                felt_states = result.get('felt_states', {})
                organ_results = result.get('organ_results', {})

                # Track organ coherences
                for organ_name, organ_result in organ_results.items():
                    if organ_name == 'NEXUS':
                        # NEXUS is the 12th organ, skip if not in standard 11
                        continue
                    if hasattr(organ_result, 'coherence'):
                        organ_activations[organ_name].append(organ_result.coherence)

                # Extract TSK-critical metrics
                actual_polyvagal = felt_states.get('eo_polyvagal_state', 'ventral_vagal')
                actual_zone = felt_states.get('zone', 1)
                actual_urgency = felt_states.get('NDAM_urgency_level', 0.0)
                family_id = felt_states.get('phase5_family_id', 'NONE')

                # Validate against expectations
                poly_match = actual_polyvagal == test_input['expected_polyvagal'] or \
                            (actual_polyvagal in ['ventral', 'ventral_vagal'] and
                             test_input['expected_polyvagal'] in ['ventral', 'ventral_vagal'])
                polyvagal_accuracy.append(1.0 if poly_match else 0.0)

                zone_diff = abs(actual_zone - test_input['expected_zone'])
                zone_accuracy.append(1.0 if zone_diff <= 1 else 0.0)

                urgency_error = abs(actual_urgency - test_input['expected_urgency'])
                urgency_errors.append(urgency_error)

                # Store processing result
                processing_result = {
                    'input_id': test_input['id'],
                    'category': test_input['category'],
                    'expected': {
                        'polyvagal': test_input['expected_polyvagal'],
                        'zone': test_input['expected_zone'],
                        'urgency': test_input['expected_urgency']
                    },
                    'actual': {
                        'polyvagal': actual_polyvagal,
                        'zone': actual_zone,
                        'urgency': actual_urgency,
                        'family_id': family_id
                    },
                    'accuracy': {
                        'polyvagal_match': poly_match,
                        'zone_close': zone_diff <= 1,
                        'urgency_error': urgency_error
                    },
                    'satisfaction': felt_states.get('satisfaction_final', 0.0),
                    'emission_confidence': result.get('emission_confidence', 0.0),
                    'v0_descent': felt_states.get('v0_descent_ratio', 0.0)
                }

                epoch_results['processing_results'].append(processing_result)
                epoch_results['inputs_processed'] += 1

            except Exception as e:
                if self.verbose:
                    print(f"   Error processing {test_input['id']}: {e}")

        # Compute organ participation metrics
        for organ_name, activations in organ_activations.items():
            if activations:
                epoch_results['organ_participation'][organ_name] = {
                    'mean_coherence': float(np.mean(activations)),
                    'std_coherence': float(np.std(activations)),
                    'min_coherence': float(np.min(activations)),
                    'max_coherence': float(np.max(activations)),
                    'range': float(np.max(activations) - np.min(activations))
                }

        # Compute transformation pattern metrics
        epoch_results['transformation_patterns'] = {
            'polyvagal_accuracy': float(np.mean(polyvagal_accuracy)) if polyvagal_accuracy else 0.0,
            'zone_accuracy': float(np.mean(zone_accuracy)) if zone_accuracy else 0.0,
            'mean_urgency_error': float(np.mean(urgency_errors)) if urgency_errors else 0.0,
            'std_urgency_error': float(np.std(urgency_errors)) if urgency_errors else 0.0
        }

        return epoch_results

    def _capture_learning_trajectory(self, epoch_num: int) -> Dict[str, Any]:
        """Capture learning trajectory snapshot."""
        return {
            'epoch': epoch_num,
            'timestamp': datetime.now().isoformat(),
            'families': self._load_family_state(),
            'r_matrix': self._load_rmatrix_state(),
            'organ_confidence': self._load_organ_confidence()
        }

    def _compute_rnx_metrics(self, epoch_results: Dict[str, Any]) -> Dict[str, Any]:
        """Compute RNX-specific learning metrics."""
        # RNX dimensions in 57D signature (dims 53-56)
        # temporal_diversity, pattern_coherence, emergence_rate, stability

        organ_participation = epoch_results.get('organ_participation', {})

        # RNX organ metrics
        rnx_metrics = organ_participation.get('RNX', {})

        # Compute differentiation score across all organs
        organ_ranges = []
        for organ_name, metrics in organ_participation.items():
            organ_ranges.append(metrics.get('range', 0.0))

        avg_discrimination = float(np.mean(organ_ranges)) if organ_ranges else 0.0

        return {
            'epoch': epoch_results['epoch'],
            'rnx_mean_coherence': rnx_metrics.get('mean_coherence', 0.0),
            'rnx_coherence_range': rnx_metrics.get('range', 0.0),
            'overall_organ_discrimination': avg_discrimination,
            'active_organs': sum(1 for r in organ_ranges if r > 0.05),
            'total_organs': len(organ_ranges)
        }

    def _validate_tsk_pipeline(self, epoch_results: Dict[str, Any]) -> Dict[str, Any]:
        """Validate TSK spinal cord pipeline integrity."""
        validation = {
            'epoch': epoch_results['epoch'],
            'total_inputs': epoch_results['inputs_processed'],
            'valid_polyvagal': 0,
            'valid_zone': 0,
            'valid_urgency': 0,
            'families_formed': 0,
            'tsk_recording_success': 0
        }

        families_seen = set()

        for result in epoch_results['processing_results']:
            # Check polyvagal detection (not default)
            if result['actual']['polyvagal'] in ['sympathetic', 'dorsal_vagal', 'mixed_state']:
                validation['valid_polyvagal'] += 1
            elif result['actual']['polyvagal'] == 'ventral_vagal' and \
                 result['category'] in ['safety', 'relational']:
                validation['valid_polyvagal'] += 1

            # Check zone computation (not always 1)
            if result['actual']['zone'] != 1 or result['category'] in ['safety', 'relational']:
                validation['valid_zone'] += 1

            # Check urgency detection (not always 0)
            if result['actual']['urgency'] > 0.0 or result['category'] in ['safety', 'relational']:
                validation['valid_urgency'] += 1

            # Track families
            family_id = result['actual']['family_id']
            if family_id != 'NONE':
                families_seen.add(family_id)
                validation['tsk_recording_success'] += 1

        validation['families_formed'] = len(families_seen)

        # Compute validation rates
        total = validation['total_inputs']
        validation['polyvagal_valid_rate'] = validation['valid_polyvagal'] / total if total > 0 else 0.0
        validation['zone_valid_rate'] = validation['valid_zone'] / total if total > 0 else 0.0
        validation['urgency_valid_rate'] = validation['valid_urgency'] / total if total > 0 else 0.0
        validation['tsk_recording_rate'] = validation['tsk_recording_success'] / total if total > 0 else 0.0

        return validation

    def _print_epoch_summary(
        self,
        epoch_num: int,
        epoch_results: Dict[str, Any],
        trajectory: Dict[str, Any],
        rnx_metrics: Dict[str, Any]
    ):
        """Print epoch summary."""
        print(f"\n--- EPOCH {epoch_num} SUMMARY ---")

        # Processing results
        trans_patterns = epoch_results.get('transformation_patterns', {})
        print(f"   Inputs processed: {epoch_results['inputs_processed']}")
        print(f"   Polyvagal accuracy: {trans_patterns.get('polyvagal_accuracy', 0):.2%}")
        print(f"   Zone accuracy: {trans_patterns.get('zone_accuracy', 0):.2%}")
        print(f"   Mean urgency error: {trans_patterns.get('mean_urgency_error', 0):.3f}")

        # Family trajectory
        families = trajectory.get('families', {})
        print(f"\n   Total families: {families.get('total_families', 0)}")
        print(f"   Total conversations: {families.get('total_conversations', 0)}")

        # RNX metrics
        print(f"\n   RNX mean coherence: {rnx_metrics.get('rnx_mean_coherence', 0):.3f}")
        print(f"   Overall organ discrimination: {rnx_metrics.get('overall_organ_discrimination', 0):.3f}")
        print(f"   Active organs: {rnx_metrics.get('active_organs', 0)}/{rnx_metrics.get('total_organs', 11)}")

        # R-matrix growth
        r_matrix = trajectory.get('r_matrix', {})
        print(f"\n   R-matrix mean: {r_matrix.get('mean', 0):.4f}")
        print(f"   R-matrix std: {r_matrix.get('std', 0):.4f}")

    def _capture_post_assessment(self):
        """Capture system state after training."""
        print("\n--- POST-ASSESSMENT STATE ---")

        state = {
            'timestamp': datetime.now().isoformat(),
            'families': self._load_family_state(),
            'r_matrix': self._load_rmatrix_state(),
            'organ_confidence': self._load_organ_confidence()
        }

        self.assessment_results['post_assessment'] = state

        print(f"   Total families: {state['families']['total_families']}")
        print(f"   R-matrix mean: {state['r_matrix']['mean']:.4f}")
        print(f"   Mean organ confidence: {state['organ_confidence']['mean_confidence']:.4f}")

    def _print_final_report(self):
        """Print comprehensive final assessment report."""
        print(f"\n{'='*80}")
        print("RNX LEARNING ASSESSMENT - FINAL REPORT")
        print(f"{'='*80}")

        pre = self.assessment_results['pre_assessment']
        post = self.assessment_results['post_assessment']

        print("\n SYSTEM EVOLUTION:")
        print("-" * 60)

        # Families
        pre_families = pre['families']['total_families']
        post_families = post['families']['total_families']
        family_growth = post_families - pre_families
        print(f"   Families: {pre_families} -> {post_families} (growth: {family_growth})")

        # R-matrix
        pre_rmean = pre['r_matrix']['mean']
        post_rmean = post['r_matrix']['mean']
        rmean_growth = post_rmean - pre_rmean
        print(f"   R-matrix mean: {pre_rmean:.4f} -> {post_rmean:.4f} (growth: {rmean_growth:.4f})")

        # Organ confidence
        pre_conf = pre['organ_confidence']['mean_confidence']
        post_conf = post['organ_confidence']['mean_confidence']
        conf_growth = post_conf - pre_conf
        print(f"   Mean organ confidence: {pre_conf:.4f} -> {post_conf:.4f} (growth: {conf_growth:.4f})")

        # Learning trajectory analysis
        print("\n LEARNING TRAJECTORY:")
        print("-" * 60)

        if self.assessment_results['learning_trajectory']:
            first_trajectory = self.assessment_results['learning_trajectory'][0]
            last_trajectory = self.assessment_results['learning_trajectory'][-1]

            first_families = first_trajectory['families']['total_families']
            last_families = last_trajectory['families']['total_families']

            print(f"   Family emergence: {first_families} -> {last_families} over {len(self.assessment_results['epochs'])} epochs")

            # Compute family growth rate
            epochs = len(self.assessment_results['epochs'])
            growth_rate = (last_families - first_families) / epochs if epochs > 0 else 0
            print(f"   Family growth rate: {growth_rate:.2f} families/epoch")

        # TSK validation summary
        print("\n TSK SPINAL CORD VALIDATION:")
        print("-" * 60)

        if self.assessment_results['tsk_validation']:
            last_tsk = self.assessment_results['tsk_validation'][-1]
            print(f"   Polyvagal detection valid: {last_tsk.get('polyvagal_valid_rate', 0):.2%}")
            print(f"   Zone computation valid: {last_tsk.get('zone_valid_rate', 0):.2%}")
            print(f"   Urgency detection valid: {last_tsk.get('urgency_valid_rate', 0):.2%}")
            print(f"   TSK recording success: {last_tsk.get('tsk_recording_rate', 0):.2%}")

        # RNX learning metrics
        print("\n RNX LEARNING METRICS:")
        print("-" * 60)

        if self.assessment_results['rnx_metrics']:
            last_rnx = self.assessment_results['rnx_metrics'][-1]
            print(f"   RNX mean coherence: {last_rnx.get('rnx_mean_coherence', 0):.3f}")
            print(f"   RNX coherence range: {last_rnx.get('rnx_coherence_range', 0):.3f}")
            print(f"   Overall organ discrimination: {last_rnx.get('overall_organ_discrimination', 0):.3f}")
            print(f"   Active organs: {last_rnx.get('active_organs', 0)}/{last_rnx.get('total_organs', 11)}")

        # Overall assessment
        print("\n OVERALL ASSESSMENT:")
        print("-" * 60)

        assessment = self._compute_overall_assessment()
        print(f"   Family emergence: {assessment['family_score']}")
        print(f"   TSK pipeline integrity: {assessment['tsk_score']}")
        print(f"   Organ differentiation: {assessment['organ_score']}")
        print(f"   Learning velocity: {assessment['learning_score']}")
        print(f"\n   OVERALL: {assessment['overall']}")

        self.assessment_results['final_assessment'] = assessment

    def _compute_overall_assessment(self) -> Dict[str, str]:
        """Compute overall assessment scores."""
        post = self.assessment_results['post_assessment']

        # Family score
        total_families = post['families']['total_families']
        if total_families >= 15:
            family_score = "EXCELLENT (15+ families - Zipf's law emerging)"
        elif total_families >= 8:
            family_score = "GOOD (8-14 families - healthy diversity)"
        elif total_families >= 3:
            family_score = "MINIMUM (3-7 families - basic differentiation)"
        else:
            family_score = "POOR (< 3 families - insufficient diversity)"

        # TSK pipeline score
        if self.assessment_results['tsk_validation']:
            last_tsk = self.assessment_results['tsk_validation'][-1]
            tsk_rate = (
                last_tsk.get('polyvagal_valid_rate', 0) +
                last_tsk.get('zone_valid_rate', 0) +
                last_tsk.get('urgency_valid_rate', 0)
            ) / 3
            if tsk_rate >= 0.9:
                tsk_score = f"EXCELLENT ({tsk_rate:.2%} valid)"
            elif tsk_rate >= 0.7:
                tsk_score = f"GOOD ({tsk_rate:.2%} valid)"
            elif tsk_rate >= 0.5:
                tsk_score = f"MINIMUM ({tsk_rate:.2%} valid)"
            else:
                tsk_score = f"POOR ({tsk_rate:.2%} valid)"
        else:
            tsk_score = "UNKNOWN (no validation data)"

        # Organ differentiation score
        if self.assessment_results['rnx_metrics']:
            last_rnx = self.assessment_results['rnx_metrics'][-1]
            discrimination = last_rnx.get('overall_organ_discrimination', 0)
            if discrimination >= 0.5:
                organ_score = f"EXCELLENT ({discrimination:.3f} range)"
            elif discrimination >= 0.3:
                organ_score = f"GOOD ({discrimination:.3f} range)"
            elif discrimination >= 0.15:
                organ_score = f"MINIMUM ({discrimination:.3f} range)"
            else:
                organ_score = f"POOR ({discrimination:.3f} range)"
        else:
            organ_score = "UNKNOWN (no RNX data)"

        # Learning velocity
        pre = self.assessment_results['pre_assessment']
        r_growth = post['r_matrix']['mean'] - pre['r_matrix']['mean']
        if r_growth >= 0.1:
            learning_score = f"FAST ({r_growth:.4f} R-matrix growth)"
        elif r_growth >= 0.05:
            learning_score = f"MODERATE ({r_growth:.4f} R-matrix growth)"
        elif r_growth >= 0.01:
            learning_score = f"SLOW ({r_growth:.4f} R-matrix growth)"
        else:
            learning_score = f"STAGNANT ({r_growth:.4f} R-matrix growth)"

        # Overall
        scores = [
            1.0 if "EXCELLENT" in family_score else 0.75 if "GOOD" in family_score else 0.5 if "MINIMUM" in family_score else 0.25,
            1.0 if "EXCELLENT" in tsk_score else 0.75 if "GOOD" in tsk_score else 0.5 if "MINIMUM" in tsk_score else 0.25,
            1.0 if "EXCELLENT" in organ_score else 0.75 if "GOOD" in organ_score else 0.5 if "MINIMUM" in organ_score else 0.25,
            1.0 if "FAST" in learning_score else 0.75 if "MODERATE" in learning_score else 0.5 if "SLOW" in learning_score else 0.25
        ]
        avg_score = np.mean(scores)

        if avg_score >= 0.9:
            overall = "PRODUCTION READY - Full RNX learning capabilities operational"
        elif avg_score >= 0.7:
            overall = "GOOD - RNX learning working, minor tuning needed"
        elif avg_score >= 0.5:
            overall = "MINIMUM - Basic learning functional, needs improvement"
        else:
            overall = "REQUIRES ATTENTION - Learning capabilities compromised"

        return {
            'family_score': family_score,
            'tsk_score': tsk_score,
            'organ_score': organ_score,
            'learning_score': learning_score,
            'overall': overall
        }

    def _save_results(self, suffix: str = "final"):
        """Save assessment results to JSON."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"rnx_assessment_{suffix}_{timestamp}.json"
        filepath = self.results_dir / filename

        # Convert numpy types for JSON serialization
        results_clean = self._clean_for_json(self.assessment_results)

        with open(filepath, 'w') as f:
            json.dump(results_clean, f, indent=2)

        print(f"\n   Results saved to: {filepath}")

    def _clean_for_json(self, obj):
        """Convert numpy types to JSON-serializable Python types."""
        if isinstance(obj, dict):
            return {k: self._clean_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._clean_for_json(v) for v in obj]
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj


def main():
    """Run RNX learning assessment."""
    parser = argparse.ArgumentParser(
        description="RNX Learning Assessment - Whole-System Processing Validation"
    )
    parser.add_argument(
        '--epochs',
        type=int,
        default=10,
        help='Number of training epochs (default: 10)'
    )
    parser.add_argument(
        '--reset',
        action='store_true',
        help='Reset system state before assessment'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        default=True,
        help='Print detailed progress'
    )
    parser.add_argument(
        '--no-save-intermediate',
        action='store_true',
        help='Skip saving intermediate results'
    )

    args = parser.parse_args()

    # Initialize assessment
    assessment = RNXLearningAssessment(
        reset_state=args.reset,
        verbose=args.verbose
    )

    # Run assessment
    results = assessment.run_assessment(
        num_epochs=args.epochs,
        save_intermediate=not args.no_save_intermediate
    )

    print(f"\n{'='*80}")
    print("RNX LEARNING ASSESSMENT COMPLETE")
    print(f"{'='*80}")
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Results Directory: {assessment.results_dir}")


if __name__ == '__main__':
    main()
