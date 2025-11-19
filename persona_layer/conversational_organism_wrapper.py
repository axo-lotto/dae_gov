"""
Conversational Organism Wrapper - Interface for Epoch Training
================================================================

Wraps DAE-GOV organism processing for use in epoch training. Provides a clean interface for
processing text through the full 11-organ trauma-aware organism and extracting TSK records.

This wrapper enables batch training without requiring interactive CLI mode.

Architecture:
- Uses DAE-GOV's 11-organ architecture (Phase 2 COMPLETE!)
- 5 Conversational Organs: LISTENING, EMPATHY, WISDOM, AUTHENTICITY, PRESENCE
- 6 Trauma/Context-Aware Organs: BOND (IFS/trauma), SANS (semantic), NDAM (urgency), RNX (temporal), EO (polyvagal), CARD (response scaling)
- Processes text through full cascade with real-time trauma detection
- Extracts complete felt states (11 organ coherences, V0 energy, satisfaction, convergence)
- Returns structured data suitable for TSK record creation

Phase 1 Integration Complete: November 11, 2025
- ✅ BOND organ integrated (trauma/SELF-energy detection via IFS)
- ✅ SANS organ integrated (semantic coherence tracking)
- ✅ NDAM organ integrated (urgency/crisis detection)

Phase 2 Integration COMPLETE: November 11, 2025
- ✅ RNX organ integrated (temporal pattern detection - crisis/concrescent/restorative/symbolic_pull)
- ✅ EO organ integrated (polyvagal state detection - ventral/sympathetic/dorsal)
- ✅ CARD organ integrated (response scaling - minimal/brief/moderate/detailed/comprehensive)
- ✅ 11-organ felt states operational for Phase 5 organic learning!
"""

import sys
import hashlib
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# 🚨 Import Config (CRITICAL - Nov 17, 2025)
from config import Config

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import conversational organs
from organs.modular.listening.core.listening_text_core import ListeningTextCore
from organs.modular.empathy.core.empathy_text_core import EmpathyTextCore
from organs.modular.wisdom.core.wisdom_text_core import WisdomTextCore
from organs.modular.authenticity.core.authenticity_text_core import AuthenticityTextCore
from organs.modular.presence.core.presence_text_core import PresenceTextCore

# Import critical trauma-aware organs (Phase 1 integration - Nov 11, 2025)
from organs.modular.bond.core.bond_text_core import BONDTextCore
from organs.modular.sans.core.sans_text_core import SANSTextCore
from organs.modular.ndam.core.ndam_text_core import NDAMTextCore

# Import Phase 2 organs (temporal, polyvagal, and contextual awareness - Nov 11, 2025)
from organs.modular.rnx.core.rnx_text_core import RNXTextCore
from organs.modular.eo.core.eo_text_core import EOTextCore
from organs.modular.card.core.card_text_core import CARDTextCore

# 🌀 Import NEXUS organ (Neo4j memory management - Nov 15, 2025 - Quick Win #9)
from organs.modular.nexus.core.nexus_text_core import NEXUSTextCore

# Import Phase 5 learning integration
try:
    from persona_layer.phase5_learning_integration import Phase5LearningIntegration
    PHASE5_AVAILABLE = True
except ImportError:
    PHASE5_AVAILABLE = False
    print("⚠️  Phase 5 learning not available")

# 🆕 Import Organ Confidence Tracker (Level 2 Fractal Rewards - Nov 15, 2025)
try:
    from persona_layer.organ_confidence_tracker import OrganConfidenceTracker
    ORGAN_CONFIDENCE_AVAILABLE = True
except ImportError:
    ORGAN_CONFIDENCE_AVAILABLE = False

# 🌀 Import Entity-Organ Tracker (Quick Win #7 - Neo4j Mastery - Nov 15, 2025)
try:
    from persona_layer.entity_organ_tracker import EntityOrganTracker
    ENTITY_ORGAN_TRACKER_AVAILABLE = True
except ImportError:
    ENTITY_ORGAN_TRACKER_AVAILABLE = False
    print("⚠️  Organ confidence tracker not available")

# 🌀 Import Symbiotic LLM Entity Extractor (Phase 1 LLM Independence - Nov 18, 2025)
try:
    from persona_layer.local_llm_bridge import LocalLLMBridge
    from persona_layer.symbiotic_llm_entity_extractor import SymbioticLLMEntityExtractor
    SYMBIOTIC_EXTRACTOR_AVAILABLE = True
except ImportError as e:
    SYMBIOTIC_EXTRACTOR_AVAILABLE = False
    print(f"⚠️  Symbiotic LLM extractor not available: {e}")

# 🌀 Import Entity Neighbor Prehension (Phase 3B Pattern Learning - Nov 18, 2025)
try:
    from persona_layer.entity_neighbor_prehension.entity_neighbor_prehension import EntityNeighborPrehension
    ENTITY_NEIGHBOR_PREHENSION_AVAILABLE = True
except ImportError as e:
    ENTITY_NEIGHBOR_PREHENSION_AVAILABLE = False
    print(f"⚠️  Entity neighbor prehension not available: {e}")

# Import emission generation components
try:
    from persona_layer.semantic_field_extractor import SemanticFieldExtractor
    from persona_layer.nexus_intersection_composer import NexusIntersectionComposer
    from persona_layer.emission_generator import EmissionGenerator
    EMISSION_AVAILABLE = True
except ImportError as e:
    EMISSION_AVAILABLE = False
    print(f"⚠️  Emission generation not available: {e}")

# Import TextOccasion for processing
from transductive.text_occasion import TextOccasion

# Import Phase 2 ConversationalOccasion (multi-cycle V0 convergence)
try:
    from persona_layer.conversational_occasion import ConversationalOccasion
    import json
    PHASE2_CONVERGENCE_AVAILABLE = True
except ImportError as e:
    PHASE2_CONVERGENCE_AVAILABLE = False
    print(f"⚠️  Phase 2 convergence not available: {e}")

# 🆕 Import Salience Model (Phase 2 transductive core integration)
try:
    from persona_layer.conversational_salience_model import ConversationalSalienceModel
    SALIENCE_AVAILABLE = True
except ImportError as e:
    SALIENCE_AVAILABLE = False
    print(f"⚠️  Salience model not available: {e}")

# 🆕 Import Meta-Atom Activator (Phase 3 - November 12, 2025)
try:
    from persona_layer.meta_atom_activator import MetaAtomActivator
    META_ATOM_ACTIVATOR_AVAILABLE = True
except ImportError as e:
    META_ATOM_ACTIVATOR_AVAILABLE = False
    print(f"⚠️  Meta-atom activator not available: {e}")

# 🆕 Import Organ Coupling Learner (DAE 3.0 Integration - November 12, 2025)
try:
    from persona_layer.organ_coupling_learner import OrganCouplingLearner
    ORGAN_COUPLING_AVAILABLE = True
except ImportError as e:
    ORGAN_COUPLING_AVAILABLE = False
    print(f"⚠️  Organ coupling learner not available: {e}")

# 🆕 Import Family V0 Learner (DAE 3.0 Integration - November 12, 2025)
try:
    from persona_layer.family_v0_learner import FamilyV0Learner
    FAMILY_V0_AVAILABLE = True
except ImportError as e:
    FAMILY_V0_AVAILABLE = False
    print(f"⚠️  Family V0 learner not available: {e}")

# 🆕 Import Transductive Nexus Integration (November 12, 2025)
try:
    from persona_layer.nexus_transduction_state import (
        NexusTransductionState,
        classify_nexus_type_from_v0,
        compute_rhythm_coherence,
        compute_mutual_satisfaction,
        check_relational_field_available,
        compute_transductive_vocabulary
    )
    from persona_layer.transduction_pathway_evaluator import TransductionPathwayEvaluator
    TRANSDUCTION_AVAILABLE = True
except ImportError as e:
    TRANSDUCTION_AVAILABLE = False
    print(f"⚠️  Transductive nexus integration not available: {e}")

# 🆕 Import SELF Matrix Governance + Reconstruction Pipeline (November 12, 2025)
try:
    from persona_layer.self_matrix_governance import SELFMatrixGovernance
    from persona_layer.organ_reconstruction_pipeline import OrganReconstructionPipeline
    RECONSTRUCTION_AVAILABLE = True
except ImportError as e:
    RECONSTRUCTION_AVAILABLE = False
    print(f"⚠️  Reconstruction pipeline not available: {e}")

# 🆕 Import Persona Layer (Levels 8-10 Companion Integration - November 12, 2025)
try:
    from persona_layer.persona_layer import PersonaLayer, TemplateContext, QueryType
    from persona_layer.user_profile_manager import UserProfileManager
    PERSONA_LAYER_AVAILABLE = True
except ImportError as e:
    PERSONA_LAYER_AVAILABLE = False
    print(f"⚠️  Persona layer not available: {e}")

# 🆕 Import Satisfaction Regime (Enhancement #1 - November 13, 2025)
try:
    from persona_layer.epoch_training.satisfaction_regime import SatisfactionRegime, classify_satisfaction_regime
    REGIME_CLASSIFIER_AVAILABLE = True
except ImportError as e:
    REGIME_CLASSIFIER_AVAILABLE = False
    print(f"⚠️  Satisfaction regime classifier not available: {e}")

# 🌀 Import User Superject Learner (Phase 1 Foundation - November 14, 2025)
try:
    from persona_layer.user_superject_learner import UserSuperjectLearner
    SUPERJECT_LEARNER_AVAILABLE = True
except ImportError as e:
    SUPERJECT_LEARNER_AVAILABLE = False
    print(f"⚠️  User superject learner not available: {e}")

# 🛡️ Import Heckling Intelligence (Phase 1.5H - November 14, 2025)
try:
    from persona_layer.heckling_intelligence import HecklingIntelligence, enhance_ndam_with_heckling
    HECKLING_INTELLIGENCE_AVAILABLE = True
except ImportError as e:
    HECKLING_INTELLIGENCE_AVAILABLE = False
    print(f"⚠️  Heckling intelligence not available: {e}")

# 📊 Import Transductive Self-Governance (Phase 1.6 - November 14, 2025)
try:
    from persona_layer.transductive_self_governance import TransductiveSelfMonitor
    TRANSDUCTIVE_SELF_GOVERNANCE_AVAILABLE = True
except ImportError as e:
    TRANSDUCTIVE_SELF_GOVERNANCE_AVAILABLE = False
    print(f"⚠️  Transductive self-governance not available: {e}")

# 🌀 Import Unified State Manager (Phase 1.6 - November 14, 2025)
try:
    from memory.unified_state_manager import UnifiedStateManager
    UNIFIED_STATE_AVAILABLE = True
except ImportError as e:
    UNIFIED_STATE_AVAILABLE = False
    print(f"⚠️  Unified state manager not available: {e}")

# 🌀 Import Entity Differentiation (Phase 1.6 - November 14, 2025)
try:
    from persona_layer.entity_differentiation import EntityDifferentiator
    ENTITY_DIFFERENTIATION_AVAILABLE = True
except ImportError as e:
    ENTITY_DIFFERENTIATION_AVAILABLE = False
    print(f"⚠️  Entity differentiation not available: {e}")

# 🌀 Import TSK Recorder (Transductive Summary Kernel - November 16, 2025)
try:
    from persona_layer.conversational_tsk_recorder import (
        ConversationalTSKRecorder,
        TransductiveSummaryKernel
    )
    TSK_RECORDER_AVAILABLE = True
except ImportError as e:
    TSK_RECORDER_AVAILABLE = False
    print(f"⚠️  TSK recorder not available: {e}")

# 🌀 Import Pre-Emission Entity Prehension (NEXUS Entity Memory Training - November 16, 2025)
try:
    from persona_layer.pre_emission_entity_prehension import PreEmissionEntityPrehension
    PRE_EMISSION_PREHENSION_AVAILABLE = True
except ImportError as e:
    PRE_EMISSION_PREHENSION_AVAILABLE = False
    print(f"⚠️  Pre-emission entity prehension not available: {e}")

# 🌀 Import Entity Extraction Components (Nov 18, 2025 - Fix entity timing for NEXUS)
try:
    from persona_layer.memory_intent_detector import MemoryIntentDetector
    from persona_layer.entity_extractor import EntityExtractor
    ENTITY_EXTRACTION_AVAILABLE = True
except ImportError as e:
    ENTITY_EXTRACTION_AVAILABLE = False
    print(f"⚠️  Entity extraction components not available: {e}")

# 🌀 Import Session Turn Manager (USER:SESSION:TURN Hierarchy - November 16, 2025)
try:
    from persona_layer.session_turn_manager import SessionTurnManager
    SESSION_TURN_MANAGER_AVAILABLE = True
except ImportError as e:
    SESSION_TURN_MANAGER_AVAILABLE = False
    print(f"⚠️  Session turn manager not available: {e}")

# 🌀 Import LLM Bridge Components (Phase 1-2 - November 18, 2025)
try:
    from persona_layer.conversation_feedback_handler import ConversationFeedbackHandler
    from persona_layer.turn_history_manager import TurnHistoryManager
    LLM_BRIDGE_AVAILABLE = True
except ImportError as e:
    LLM_BRIDGE_AVAILABLE = False
    print(f"⚠️  LLM Bridge components not available: {e}")

# 🌀 Import Phase 3B Epoch Learning Trackers (November 18, 2025)
try:
    from persona_layer.word_occasion_tracker import WordOccasionTracker
    from persona_layer.cycle_convergence_tracker import CycleConvergenceTracker
    from persona_layer.gate_cascade_quality_tracker import GateCascadeQualityTracker
    from persona_layer.nexus_vs_llm_decision_tracker import NexusVsLLMDecisionTracker
    from persona_layer.neighbor_word_context_tracker import NeighborWordContextTracker
    PHASE3B_TRACKERS_AVAILABLE = True
except ImportError as e:
    PHASE3B_TRACKERS_AVAILABLE = False
    print(f"⚠️  Phase 3B trackers not available: {e}")

# 🌀 Import Multi-Organ Entity Extractor (Phase 0C - November 19, 2025)
try:
    from persona_layer.multi_organ_entity_extractor import MultiOrganEntityExtractor
    MULTI_ORGAN_EXTRACTOR_AVAILABLE = True
except ImportError as e:
    MULTI_ORGAN_EXTRACTOR_AVAILABLE = False
    print(f"⚠️  Multi-organ entity extractor not available: {e}")


class ConversationalOrganismWrapper:
    """
    Wrapper for DAE-GOV organism processing during epoch training.

    Provides a clean interface for batch text processing without interactive CLI overhead.
    """

    def __init__(self, bundle_path: str = "Bundle"):
        """
        Initialize organism wrapper with core organs.

        Args:
            bundle_path: Path to Bundle for memory storage
        """
        self.bundle_path = Path(bundle_path)

        print("\n🌀 Initializing 11-Organ Conversational Organism (Phase 2 Complete!)")
        print("="*70)

        # Initialize 5 conversational organs (Phase 2.0 architecture)
        print("   Loading conversational organs...")
        self.listening = ListeningTextCore()
        self.empathy = EmpathyTextCore()
        self.wisdom = WisdomTextCore()
        self.authenticity = AuthenticityTextCore()
        self.presence = PresenceTextCore()
        print(f"   ✅ 5 conversational organs loaded")

        # Initialize 3 critical trauma-aware organs (Phase 1 - Nov 11, 2025)
        print("   Loading trauma-aware organs (Phase 1)...")
        self.bond = BONDTextCore()        # IFS trauma/SELF-energy detection
        self.sans = SANSTextCore()        # Semantic coherence
        self.ndam = NDAMTextCore()        # Urgency detection
        print(f"   ✅ 3 trauma-aware organs loaded (BOND, SANS, NDAM)")

        # Initialize Phase 2 temporal/polyvagal/scaling organs (Nov 11, 2025)
        print("   Loading Phase 2 organs (temporal, polyvagal, scaling)...")
        self.rnx = RNXTextCore()          # Temporal pattern detection (crisis/restorative/etc)
        self.eo = EOTextCore()            # Polyvagal state detection (ventral/sympathetic/dorsal)
        self.card = CARDTextCore()        # Response scaling (minimal→comprehensive)
        print(f"   ✅ 3 Phase 2 organs loaded (RNX, EO, CARD)")

        # 🌀 Initialize NEXUS organ (Neo4j memory management - Nov 15, 2025 - Quick Win #9)
        print("   Loading NEXUS organ (Neo4j entity memory)...")
        self.nexus = NEXUSTextCore(enable_neo4j=True, enable_entity_tracker=True)
        print(f"   ✅ NEXUS organ loaded (12th organ - memory as prehension!)")

        print(f"\n   ✅ 12 organs total operational (NEXUS COMPLETE!)")

        # Initialize Phase 5 learning (if available)
        if PHASE5_AVAILABLE:
            try:
                self.phase5_learning = Phase5LearningIntegration(
                    storage_path="persona_layer",
                    learning_threshold=0.30,  # ✅ NOV 17: Match default (was 0.55 - too conservative!)
                    enable_learning=True  # ✅ ENABLED (Nov 15, 2025) - Pragmatic epoch learning uses existing Phase 5
                )
                print(f"   ✅ Phase 5 learning integration ready")
            except Exception as e:
                print(f"   ⚠️  Phase 5 learning unavailable: {e}")
                self.phase5_learning = None
        else:
            self.phase5_learning = None

        # 🆕 Initialize Organ Confidence Tracker (Level 2 Fractal Rewards - Nov 15, 2025)
        if ORGAN_CONFIDENCE_AVAILABLE:
            try:
                self.organ_confidence = OrganConfidenceTracker(
                    storage_path="persona_layer/state/active/organ_confidence.json",
                    ema_alpha=0.1,  # DAE 3.0 validated
                    success_threshold=0.5  # Learn from "Helpful" ratings
                )
                print(f"   ✅ Organ confidence tracker ready (Level 2 fractal rewards)")
            except Exception as e:
                print(f"   ⚠️  Organ confidence tracker unavailable: {e}")
                self.organ_confidence = None
        else:
            self.organ_confidence = None

        # 🌀 Initialize Entity-Organ Tracker (Quick Win #7 - Neo4j Mastery - Nov 15, 2025)
        if ENTITY_ORGAN_TRACKER_AVAILABLE:
            try:
                self.entity_organ_tracker = EntityOrganTracker(
                    storage_path="persona_layer/state/active/entity_organ_associations.json",
                    ema_alpha=0.15,  # Slightly faster than organ confidence
                    min_mentions_for_pattern=3  # Need 3+ mentions before pattern emerges
                )
                print(f"   ✅ Entity-organ tracker ready (entity-aware learning)")
            except Exception as e:
                print(f"   ⚠️  Entity-organ tracker unavailable: {e}")
                self.entity_organ_tracker = None
        else:
            self.entity_organ_tracker = None

        # 🌀 Initialize Phase 3B Epoch Learning Trackers (November 18, 2025)
        if PHASE3B_TRACKERS_AVAILABLE:
            try:
                # Tracker 1: Word-level organ activation patterns
                self.word_occasion_tracker = WordOccasionTracker(
                    storage_path="persona_layer/state/active/word_occasion_patterns.json",
                    ema_alpha=0.15,  # Fast adaptation to new entities
                    min_mentions_for_pattern=3
                )

                # Tracker 2: Multi-cycle convergence optimization
                self.cycle_convergence_tracker = CycleConvergenceTracker(
                    storage_path="persona_layer/state/active/cycle_convergence_stats.json"
                )

                # Tracker 3: 4-gate cascade quality monitoring
                self.gate_cascade_quality_tracker = GateCascadeQualityTracker(
                    storage_path="persona_layer/state/active/gate_cascade_quality.json",
                    optimization_interval=100  # Optimize thresholds every 100 attempts
                )

                # Tracker 4: NEXUS vs LLM decision tracking (CRITICAL for LLM independence)
                self.nexus_vs_llm_tracker = NexusVsLLMDecisionTracker(
                    storage_path="persona_layer/state/active/nexus_vs_llm_decisions.json",
                    ema_alpha=0.10  # Conservative accuracy estimates
                )

                # Tracker 5: Neighbor word → organ boost learning
                self.neighbor_word_context_tracker = NeighborWordContextTracker(
                    storage_path="persona_layer/state/active/neighbor_word_context.json",
                    ema_alpha=0.15,  # Responsive to context shifts
                    min_count_for_pattern=5
                )

                print(f"   ✅ Phase 3B epoch learning trackers ready (5/5)")
            except Exception as e:
                print(f"   ⚠️  Phase 3B trackers initialization failed: {e}")
                import traceback
                traceback.print_exc()
                self.word_occasion_tracker = None
                self.cycle_convergence_tracker = None
                self.gate_cascade_quality_tracker = None
                self.nexus_vs_llm_tracker = None
                self.neighbor_word_context_tracker = None
        else:
            self.word_occasion_tracker = None
            self.cycle_convergence_tracker = None
            self.gate_cascade_quality_tracker = None
            self.nexus_vs_llm_tracker = None
            self.neighbor_word_context_tracker = None

        # 🌀 Initialize Pre-Emission Entity Prehension (NEXUS Entity Memory Training - Nov 16, 2025)
        if PRE_EMISSION_PREHENSION_AVAILABLE:
            try:
                self.entity_prehension = PreEmissionEntityPrehension(
                    storage_dir="persona_layer/users"
                )
                print(f"   ✅ Pre-emission entity prehension ready (entity memory BEFORE organ activation)")
            except Exception as e:
                print(f"   ⚠️  Pre-emission entity prehension unavailable: {e}")
                self.entity_prehension = None
        else:
            self.entity_prehension = None

        # 🌀 Initialize Session Turn Manager (USER:SESSION:TURN Hierarchy - Nov 16, 2025)
        if SESSION_TURN_MANAGER_AVAILABLE:
            try:
                self.session_manager = SessionTurnManager(
                    storage_dir="persona_layer/users"
                )
                print(f"   ✅ Session turn manager ready (USER:SESSION:TURN temporal hierarchy)")
            except Exception as e:
                print(f"   ⚠️  Session turn manager unavailable: {e}")
                self.session_manager = None
        else:
            self.session_manager = None

        # 🌀 Initialize Symbiotic LLM Entity Extractor (Phase 1 LLM Independence - Nov 18, 2025)
        if SYMBIOTIC_EXTRACTOR_AVAILABLE and Config.LOCAL_LLM_ENABLED:
            try:
                # Initialize LocalLLMBridge for symbiotic learning
                self.local_llm_bridge = LocalLLMBridge()

                # Initialize symbiotic extractor with bootstrap mode
                self.symbiotic_extractor = SymbioticLLMEntityExtractor(
                    local_llm_bridge=self.local_llm_bridge,
                    learning_mode=getattr(Config, 'SYMBIOTIC_LEARNING_MODE', 'bootstrap'),
                    cache_dir="persona_layer/state/llm_learning_cache"
                )
                print(f"   ✅ Symbiotic LLM extractor ready (Phase 1: {self.symbiotic_extractor.learning_mode} mode, {self.symbiotic_extractor.consultation_rates[self.symbiotic_extractor.learning_mode]*100:.0f}% LLM)")
            except Exception as e:
                print(f"   ⚠️  Symbiotic LLM extractor unavailable: {e}")
                self.symbiotic_extractor = None
                self.local_llm_bridge = None
        else:
            self.symbiotic_extractor = None
            self.local_llm_bridge = None

        # 🌀 Initialize Entity Neighbor Prehension (Phase 3B Pattern Learning - Nov 18, 2025)
        if ENTITY_NEIGHBOR_PREHENSION_AVAILABLE:
            try:
                # Pass entity-organ tracker for pattern learning
                tracker = self.entity_organ_tracker if hasattr(self, 'entity_organ_tracker') else None
                self.entity_neighbor_prehension = EntityNeighborPrehension(entity_tracker=tracker)
                print(f"   ✅ Entity neighbor prehension ready (Phase 3B: 5-organ, 31D actualization)")
            except Exception as e:
                print(f"   ⚠️  Entity neighbor prehension unavailable: {e}")
                self.entity_neighbor_prehension = None
        else:
            self.entity_neighbor_prehension = None

        # 🌀 Initialize Multi-Organ Entity Extractor (Phase 0C - Nov 19, 2025)
        if MULTI_ORGAN_EXTRACTOR_AVAILABLE and getattr(Config, 'MULTI_ORGAN_ENTITY_EXTRACTION_ENABLED', False):
            try:
                self.multi_organ_extractor = MultiOrganEntityExtractor(
                    coherence_threshold=getattr(Config, 'MULTI_ORGAN_COHERENCE_THRESHOLD', 0.75),
                    min_organs=getattr(Config, 'MULTI_ORGAN_MIN_ORGANS', 3),
                    ema_alpha=getattr(Config, 'MULTI_ORGAN_EMA_ALPHA', 0.15)
                )
                print(f"   ✅ Multi-organ entity extractor ready (Phase 0C: FFITTSS T4 AffinityNexus)")
            except Exception as e:
                print(f"   ⚠️  Multi-organ entity extractor unavailable: {e}")
                self.multi_organ_extractor = None
        else:
            self.multi_organ_extractor = None
            if MULTI_ORGAN_EXTRACTOR_AVAILABLE:
                print(f"   ℹ️  Multi-organ extraction: STUB (enable via Config.MULTI_ORGAN_ENTITY_EXTRACTION_ENABLED)")

        # Initialize emission generation (if available)
        if EMISSION_AVAILABLE:
            try:
                print("   Loading emission generation components...")
                self.semantic_extractor = SemanticFieldExtractor(
                    semantic_atoms_path="persona_layer/semantic_atoms.json"
                )
                self.nexus_composer = NexusIntersectionComposer(
                    r_matrix_path=str(Config.HEBBIAN_MEMORY_PATH),  # ✅ NOV 17: Use Config constant
                    intersection_threshold=0.005  # 🌀 NOV 14: Lowered 0.01→0.005 for better nexus formation
                )

                # 🌀 PHASE LLM1: Initialize felt-guided LLM generator (Nov 13, 2025)
                felt_guided_llm = None
                if Config.FELT_GUIDED_LLM_ENABLED and Config.LOCAL_LLM_ENABLED:
                    try:
                        # LocalLLMBridge already imported at module level (line 88)
                        from persona_layer.llm_felt_guidance import FeltGuidedLLMGenerator

                        # Initialize LLM bridge for felt guidance
                        llm_bridge = LocalLLMBridge()
                        felt_guided_llm = FeltGuidedLLMGenerator(llm_bridge=llm_bridge)
                        print(f"   🌀 Felt-guided LLM initialized (unlimited felt intelligence)")
                    except Exception as e:
                        print(f"   ⚠️  Felt-guided LLM unavailable: {e}")
                        felt_guided_llm = None

                self.emission_generator = EmissionGenerator(
                    semantic_atoms_path="persona_layer/semantic_atoms.json",
                    hebbian_memory_path=str(Config.HEBBIAN_MEMORY_PATH),  # ✅ NOV 17: Use Config constant
                    direct_threshold=Config.EMISSION_DIRECT_THRESHOLD,  # 0.50 (was hardcoded 0.65)
                    fusion_threshold=Config.EMISSION_FUSION_THRESHOLD,   # 0.45 (was hardcoded 0.50)
                    felt_guided_llm_generator=felt_guided_llm  # 🌀 PHASE LLM1
                )
                print(f"   ✅ Emission generation ready (11-organ, dual-path)")
            except Exception as e:
                print(f"   ⚠️  Emission generation unavailable: {e}")
                self.semantic_extractor = None
                self.nexus_composer = None
                self.emission_generator = None
        else:
            self.semantic_extractor = None
            self.nexus_composer = None
            self.emission_generator = None

        # 🆕 Initialize salience model (Phase 2 transductive core integration)
        if SALIENCE_AVAILABLE:
            try:
                print("   Loading salience model (transductive core)...")
                self.salience_model = ConversationalSalienceModel()
                print(f"   ✅ Salience model ready (trauma-aware, morphogenetic)")
            except Exception as e:
                print(f"   ⚠️  Salience model unavailable: {e}")
                self.salience_model = None
        else:
            self.salience_model = None

        # 🆕 Initialize transduction pathway evaluator (November 12, 2025)
        if TRANSDUCTION_AVAILABLE:
            try:
                print("   Loading transductive nexus evaluator...")
                self.transduction_evaluator = TransductionPathwayEvaluator()
                print(f"   ✅ Transductive pathways ready (14 nexus types, 9 primary pathways)")
            except Exception as e:
                print(f"   ⚠️  Transduction evaluator unavailable: {e}")
                self.transduction_evaluator = None
        else:
            self.transduction_evaluator = None

        # 🆕 Initialize meta-atom activator (Phase 3 - November 12, 2025)
        if META_ATOM_ACTIVATOR_AVAILABLE:
            try:
                print("   Loading meta-atom activator...")
                self.meta_atom_activator = MetaAtomActivator(
                    rules_path="persona_layer/config/atoms/meta_atom_activation_rules.json"
                )
                print(f"   ✅ Meta-atom activator ready (10 meta-atoms, trauma-informed)")
            except Exception as e:
                print(f"   ⚠️  Meta-atom activator unavailable: {e}")
                self.meta_atom_activator = None
        else:
            self.meta_atom_activator = None

        # 🆕 Initialize organ coupling learner (DAE 3.0 Integration - November 12, 2025)
        if ORGAN_COUPLING_AVAILABLE:
            try:
                print("   Loading organ coupling learner (DAE 3.0 R-matrix)...")
                self.organ_coupling_learner = OrganCouplingLearner(
                    r_matrix_path=Path("persona_layer/state/active/conversational_hebbian_memory.json"),
                    learning_rate=Config.R_MATRIX_LEARNING_RATE  # 0.005 (fixed Nov 13, 2025)
                )
                print(f"   ✅ Organ coupling learner ready (11×11 Hebbian R-matrix)")
            except Exception as e:
                print(f"   ⚠️  Organ coupling learner unavailable: {e}")
                self.organ_coupling_learner = None
        else:
            self.organ_coupling_learner = None

        # 🆕 Initialize family V0 learner (DAE 3.0 Integration - November 12, 2025)
        if FAMILY_V0_AVAILABLE:
            try:
                print("   Loading family V0 learner (DAE 3.0 per-family optimization)...")
                self.family_v0_learner = FamilyV0Learner(
                    families_path=Path("persona_layer/state/active/organic_families.json"),
                    learning_rate=0.1
                )
                print(f"   ✅ Family V0 learner ready (per-family V0 targets)")
            except Exception as e:
                print(f"   ⚠️  Family V0 learner unavailable: {e}")
                self.family_v0_learner = None
        else:
            self.family_v0_learner = None

        # Load shared meta-atoms for Phase 2 convergence (if available)
        self.meta_atoms = None
        if PHASE2_CONVERGENCE_AVAILABLE:
            try:
                meta_atoms_path = Path(__file__).parent / "shared_meta_atoms.json"
                if meta_atoms_path.exists():
                    with open(meta_atoms_path, 'r') as f:
                        self.meta_atoms = json.load(f)
                    print(f"   ✅ Loaded {len(self.meta_atoms['meta_atoms'])} shared meta-atoms for Phase 2")
                else:
                    print(f"   ⚠️  Shared meta-atoms not found at {meta_atoms_path}")
            except Exception as e:
                print(f"   ⚠️  Could not load shared meta-atoms: {e}")

        # 🆕 Initialize SELF matrix governance (November 12, 2025)
        if RECONSTRUCTION_AVAILABLE:
            try:
                print("   Loading SELF matrix governance (trauma-informed emission)...")
                self.self_governance = SELFMatrixGovernance(
                    coherent_attractors_path="persona_layer/config/symbols/coherent_attractors.json"
                )
                print(f"   ✅ SELF matrix governance ready (5 zones, IFS + Polyvagal)")
            except Exception as e:
                print(f"   ⚠️  SELF matrix governance unavailable: {e}")
                self.self_governance = None
        else:
            self.self_governance = None

        # 🆕 Initialize reconstruction pipeline (November 12, 2025)
        # Wires together: EmissionGenerator + NexusComposer + ResponseAssembler + SELFGovernance
        if all([self.emission_generator, self.nexus_composer,
                self.self_governance, RECONSTRUCTION_AVAILABLE]):
            try:
                print("   Initializing reconstruction emission pipeline...")
                # Import response assembler here (lazy import to avoid circular deps)
                from persona_layer.response_assembler import ResponseAssembler

                self.response_assembler = ResponseAssembler(
                    max_phrases=3,
                    prefer_variety=True,
                    apply_therapeutic_arc=True
                )

                self.reconstruction_pipeline = OrganReconstructionPipeline(
                    emission_generator=self.emission_generator,
                    nexus_composer=self.nexus_composer,
                    response_assembler=self.response_assembler,
                    self_matrix_governance=self.self_governance,
                    phase5_learning=self.phase5_learning
                    # ✅ NOV 17: No longer passing hebbian_memory_path - uses Config.HEBBIAN_MEMORY_PATH by default
                )
                print(f"   ✅ Reconstruction pipeline ready (authentic voice enabled!)")
            except Exception as e:
                print(f"   ⚠️  Reconstruction pipeline unavailable: {e}")
                import traceback
                traceback.print_exc()
                self.reconstruction_pipeline = None
        else:
            self.reconstruction_pipeline = None
            if not RECONSTRUCTION_AVAILABLE:
                print(f"   ⚠️  Reconstruction pipeline disabled (RECONSTRUCTION_AVAILABLE=False)")

        # 🆕 Initialize Persona Layer (Levels 8-10 Companion - November 12, 2025)
        if PERSONA_LAYER_AVAILABLE:
            try:
                if Config.PERSONA_LAYER_ENABLED:
                    print("   Loading Persona Layer (template-based companion)...")
                    self.persona_layer = PersonaLayer()
                    self.user_profile_manager = UserProfileManager()
                    print(f"   ✅ Persona Layer ready (Levels 8-10, LLM={Config.LOCAL_LLM_ENABLED})")
                else:
                    self.persona_layer = None
                    self.user_profile_manager = None
                    print(f"   ⚠️  Persona Layer disabled (Config.PERSONA_LAYER_ENABLED=False)")
            except Exception as e:
                print(f"   ⚠️  Persona Layer unavailable: {e}")
                self.persona_layer = None
                self.user_profile_manager = None
        else:
            self.persona_layer = None
            self.user_profile_manager = None

        # 🆕 Initialize regime tracking (Enhancement #1 - November 13, 2025)
        self.current_regime = SatisfactionRegime.EXPLORING if REGIME_CLASSIFIER_AVAILABLE else None
        self.satisfaction_history = []  # Track for regime classification

        # 🌀 Initialize User Superject Learner (Phase 1 Foundation - November 14, 2025)
        if SUPERJECT_LEARNER_AVAILABLE:
            try:
                print("   Loading User Superject Learner (companion personality)...")
                self.superject_learner = UserSuperjectLearner(storage_dir="persona_layer/users")
                print(f"   ✅ Superject Learner ready (passive + mini-epoch learning)")
            except Exception as e:
                print(f"   ⚠️  Superject learner initialization failed: {e}")
                self.superject_learner = None
        else:
            self.superject_learner = None

        # 🛡️ Initialize Heckling Intelligence (Phase 1.5H - November 14, 2025)
        if HECKLING_INTELLIGENCE_AVAILABLE:
            try:
                print("   Loading Heckling Intelligence (crisis vs provocation)...")
                self.heckling_intel = HecklingIntelligence()
                print(f"   ✅ Heckling Intelligence ready (safety-first classifier)")
            except Exception as e:
                print(f"   ⚠️  Heckling intelligence initialization failed: {e}")
                self.heckling_intel = None
        else:
            self.heckling_intel = None

        # 📊 Initialize Transductive Self-Governance (Phase 1.6 - November 14, 2025)
        if TRANSDUCTIVE_SELF_GOVERNANCE_AVAILABLE:
            try:
                print("   Loading Transductive Self-Governance (DAE learns from PATTERNS not PEOPLE)...")
                self.transductive_monitor = TransductiveSelfMonitor(
                    state_path="TSK/transductive_self_state.json",
                    min_cohort_size=10,
                    privacy_epsilon=0.1
                )
                print(f"   ✅ Transductive Self-Monitor ready (k-anonymity, differential privacy)")
            except Exception as e:
                print(f"   ⚠️  Transductive self-governance initialization failed: {e}")
                self.transductive_monitor = None
        else:
            self.transductive_monitor = None

        # 🌀 Initialize Unified State Manager (Phase 1.6 Organism Self-Awareness - November 14, 2025)
        if UNIFIED_STATE_AVAILABLE:
            try:
                print("   Loading Unified State Manager (5-tier persistent organism)...")
                self.unified_state = UnifiedStateManager(base_path=Path.cwd())
                print(f"   ✅ Unified State Manager ready (T1-T5, privacy-preserving)")
            except Exception as e:
                print(f"   ⚠️  Unified state manager initialization failed: {e}")
                self.unified_state = None
        else:
            self.unified_state = None

        # 🌀 Initialize Entity Differentiator (Phase 1.6 - November 14, 2025)
        if ENTITY_DIFFERENTIATION_AVAILABLE:
            try:
                print("   Loading Entity Differentiator (DAE vs user vs relationship)...")
                self.entity_differentiator = EntityDifferentiator()
                print(f"   ✅ Entity Differentiator ready (pattern-based reference detection)")
            except Exception as e:
                print(f"   ⚠️  Entity differentiator initialization failed: {e}")
                self.entity_differentiator = None
        else:
            self.entity_differentiator = None

        # 🌀 Initialize Entity Extractors (Nov 18, 2025 - Fix entity timing for NEXUS)
        if ENTITY_EXTRACTION_AVAILABLE:
            try:
                print("   Loading Entity Extractors (extract entities BEFORE Phase 2)...")
                self._memory_intent_detector = MemoryIntentDetector()
                self._entity_extractor = EntityExtractor()
                print(f"   ✅ Entity Extractors ready (NEXUS will receive entities during V0)")
            except Exception as e:
                print(f"   ⚠️  Entity extractors initialization failed: {e}")
                self._memory_intent_detector = None
                self._entity_extractor = None
        else:
            self._memory_intent_detector = None
            self._entity_extractor = None

        # 🌀 Initialize TSK Recorder (Transductive Summary Kernel - November 16, 2025)
        if TSK_RECORDER_AVAILABLE:
            try:
                print("   Loading TSK Recorder (transformation-based epoch learning)...")
                self.tsk_recorder = ConversationalTSKRecorder(
                    storage_dir='persona_layer/state/tsks'
                )
                print(f"   ✅ TSK Recorder ready (57D transformation signatures)")
            except Exception as e:
                print(f"   ⚠️  TSK recorder initialization failed: {e}")
                self.tsk_recorder = None
        else:
            self.tsk_recorder = None

        # 🌀 Initialize pattern learner delayed feedback tracking (Week 3, Days 3-4 - Nov 17, 2025)
        # Store previous turn data for learning from satisfaction feedback
        self.previous_turn_data = None  # Will store: {signature, phrase, turn_number}

        # 🌀 Initialize FFITTSS quality modulation layers (Week 3, Day 5 - Nov 17, 2025)
        # Three-layer quality boost: Base EMA + Satisfaction Fingerprinting + Lyapunov Stability
        try:
            from persona_layer.satisfaction_fingerprinting import SatisfactionFingerprintClassifier
            from persona_layer.lyapunov_nexus_stability import LyapunovNexusStabilityGate

            self.satisfaction_fingerprinter = SatisfactionFingerprintClassifier()
            self.lyapunov_gate = LyapunovNexusStabilityGate()
            self.satisfaction_history = []  # Track satisfaction trajectory for fingerprinting

            print("   🌀 Satisfaction fingerprinting enabled (+8-12pp quality bonus for RESTORATIVE/CONCRESCENT)")
            print("   🌀 Lyapunov stability gating enabled (+5-8pp quality bonus for STABLE/ATTRACTING regimes)")
        except Exception as e:
            print(f"   ⚠️  Quality modulation layers failed to load: {e}")
            self.satisfaction_fingerprinter = None
            self.lyapunov_gate = None
            self.satisfaction_history = []

        # 🌀 Initialize LLM Bridge Components (Phase 1-2 - November 18, 2025)
        if LLM_BRIDGE_AVAILABLE:
            self.feedback_handler = ConversationFeedbackHandler()
            self.turn_history = TurnHistoryManager(
                max_turns_per_session=5,
                session_timeout_minutes=30
            )
            self.last_emission_data = {}  # Store last emission per session for feedback
            print("   🌀 LLM Bridge enabled (feedback loop + turn history)")
        else:
            self.feedback_handler = None
            self.turn_history = None
            self.last_emission_data = {}

        print("="*70)
        print("✅ 11-organ conversational organism initialized (Phase 2 COMPLETE!)\n")

    def reload_learning_state(self):
        """
        ✅ NOV 17: Reload all learned state from disk for Whiteheadian prehension.

        This method enables interactive sessions to immediately benefit from training
        updates by reloading R-matrix, organ confidence, entity-organ associations,
        and organic families before each emission.

        Whiteheadian Principle: Each occasion must prehend (feel) all past occasions
        through differentiation - not merely reference static initial state.
        """
        try:
            # Reload R-matrix (organ coupling learning)
            if self.nexus_composer is not None:
                if hasattr(self.nexus_composer, 'reload_r_matrix'):
                    self.nexus_composer.reload_r_matrix()

            # Reload Hebbian memory (emission generation)
            if self.emission_generator is not None:
                if hasattr(self.emission_generator, 'reload_hebbian_memory'):
                    self.emission_generator.reload_hebbian_memory()

            # Reload organ confidence (Level 2 fractal rewards)
            if hasattr(self, 'organ_confidence') and self.organ_confidence is not None:
                if hasattr(self.organ_confidence, 'reload'):
                    self.organ_confidence.reload()

            # Reload entity-organ associations
            if hasattr(self, 'entity_organ_tracker') and self.entity_organ_tracker is not None:
                if hasattr(self.entity_organ_tracker, 'reload'):
                    self.entity_organ_tracker.reload()

            # Reload organic families (Phase 5 learning)
            if hasattr(self, 'phase5_learning') and self.phase5_learning is not None:
                if hasattr(self.phase5_learning, 'reload'):
                    self.phase5_learning.reload()

        except Exception as e:
            # Silent failure - learning state reload is non-critical for emission
            pass

    def _record_emission_outcome(
        self,
        nexus_signature,
        emitted_phrase_text: str,
        user_satisfaction: float,
        current_turn: int,
        organ_results=None
    ):
        """
        🌀 Record emission outcome for delayed feedback learning (Week 3, Days 3-4 - Nov 17, 2025)
        🌀 ENHANCED: Three-layer quality modulation (Week 3, Day 5 - Nov 17, 2025)

        This method enables the pattern learner to update phrase quality based on user satisfaction
        from the NEXT turn (delayed feedback). Turn N satisfaction → update Turn N-1 phrase quality.

        THREE-LAYER QUALITY BOOST (FFITTSS-Proven):
        Layer 1: Base EMA Learning (nexus_phrase_pattern_learner) - EMA with α=0.15
        Layer 2: Satisfaction Fingerprinting - +8-12pp for RESTORATIVE/CONCRESCENT patterns
        Layer 3: Lyapunov Stability Gating - +5-8pp for STABLE/ATTRACTING field regimes

        Args:
            nexus_signature: NexusSignature from previous turn
            emitted_phrase_text: The phrase that was emitted in previous turn
            user_satisfaction: User satisfaction from CURRENT turn (0.0-1.0)
            current_turn: Turn number from PREVIOUS turn (for recency weighting)
            organ_results: Optional organ results for Lyapunov stability calculation

        Whiteheadian Principle: Each occasion's quality is judged by its successor's satisfaction.
        The emitted phrase's value is measured by the concrescence it enabled.
        """
        try:
            # Start with base satisfaction
            modulated_satisfaction = user_satisfaction

            # LAYER 2: Satisfaction Fingerprinting (+8-12pp bonus)
            if self.satisfaction_fingerprinter and len(self.satisfaction_history) >= 3:
                fingerprint = self.satisfaction_fingerprinter.classify(self.satisfaction_history[-3:])
                modulated_satisfaction += fingerprint.quality_adjustment
                # Clamp to [0.0, 1.0]
                modulated_satisfaction = max(0.0, min(1.0, modulated_satisfaction))

            # LAYER 3: Lyapunov Stability Gating (+5-8pp bonus)
            if self.lyapunov_gate and organ_results:
                # Extract stability metrics from organ_results
                try:
                    # Compute field coherence
                    coherences = []
                    for organ_name, organ_data in organ_results.items():
                        if hasattr(organ_data, 'coherence'):
                            coherences.append(organ_data.coherence)
                        elif isinstance(organ_data, dict):
                            coherences.append(organ_data.get('coherence', 0.5))
                    coherence = sum(coherences) / len(coherences) if coherences else 0.5

                    # Extract constraint deltas (placeholder - would need real constraint tracking)
                    constraint_deltas = {'BOND': 0.1, 'NDAM': 0.1, 'SANS': 0.05, 'EO': 0.05}

                    # Extract organ dissonances (placeholder - would need real dissonance tracking)
                    organ_dissonances = {}
                    for organ_name in organ_results.keys():
                        organ_dissonances[organ_name] = 0.1  # Placeholder

                    stability = self.lyapunov_gate.analyze_stability(
                        coherence=coherence,
                        constraint_deltas=constraint_deltas,
                        organ_dissonances=organ_dissonances
                    )
                    modulated_satisfaction += stability.quality_adjustment
                    # Clamp to [0.0, 1.0]
                    modulated_satisfaction = max(0.0, min(1.0, modulated_satisfaction))
                except Exception as e:
                    # Lyapunov calculation failed, use base satisfaction
                    pass

            # Record with modulated satisfaction (THREE-LAYER BOOST APPLIED!)
            if self.emission_generator and hasattr(self.emission_generator, 'pattern_learner'):
                self.emission_generator.pattern_learner.record_emission_outcome(
                    nexus_signature=nexus_signature,
                    emitted_phrase=emitted_phrase_text,
                    user_satisfaction=modulated_satisfaction,  # ← MODULATED, not raw!
                    current_turn=current_turn
                )
                print(f"   ✅ Recorded emission outcome (modulated satisfaction: {modulated_satisfaction:.3f})")
        except Exception as e:
            # Debug: Print exception details
            print(f"   ❌ _record_emission_outcome exception: {e}")
            import traceback
            traceback.print_exc()

    def set_exploration_context(
        self,
        regime: Optional[str] = None,
        ndam_urgency: float = 0.0,
        crisis_zone: int = 0
    ):
        """
        🎲 PHASE 1 SURFACE ENTROPY: Set exploration context for regime-adaptive emission.

        Called by multi_iteration_trainer before processing to enable voice development.

        Args:
            regime: Current satisfaction regime (EXPLORING, CONVERGING, STABLE, etc.)
            ndam_urgency: NDAM urgency level (safety gate)
            crisis_zone: Crisis zone level (safety gate)
        """
        if self.emission_generator and hasattr(self.emission_generator, 'set_exploration_context'):
            self.emission_generator.set_exploration_context(
                regime=regime,
                ndam_urgency=ndam_urgency,
                crisis_zone=crisis_zone
            )

    def process_text(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None,
        enable_tsk_recording: bool = True,
        enable_phase2: bool = True,  # ✅ ENABLED by default (Nov 15, 2025) - Phase 2 complete!
        regime: Optional[SatisfactionRegime] = None,  # 🆕 Enhancement #1: Nov 13, 2025
        user_id: Optional[str] = None,  # 🌀 Phase 1 Foundation: Nov 14, 2025
        user_satisfaction: Optional[float] = None,  # 🌀 Phase 1 Foundation: Nov 14, 2025
        username: Optional[str] = None  # 🌀 Phase 1.6: Username for personalization (Nov 14, 2025)
    ) -> Dict[str, Any]:
        """
        Process text through full organism and return complete felt state.

        This is the main entry point for epoch training. It processes text through all organs,
        computes satisfaction, and returns structured data for TSK extraction.

        Args:
            text: Text to process (user message or therapeutic response)
            context: Processing context (conversation_id, epoch_num, training_phase, etc.)
            enable_tsk_recording: Whether to enable TSK recording mode
            enable_phase2: Whether to use Phase 2 multi-cycle V0 convergence (default: False for backward compatibility)
            regime: Optional satisfaction regime for adaptive confidence modulation (🆕 Nov 13, 2025)
            user_id: Optional user identifier for superject learning (🌀 Nov 14, 2025)
            user_satisfaction: Optional explicit user satisfaction 0-1 (🌀 Nov 14, 2025)

        Returns:
            {
                'mode': 'processing_complete',
                'felt_states': {
                    'text_occasions': List[Dict],  # Words/phrases as occasions
                    'organ_coherences': Dict[str, float],  # 8 organ coherences
                    'satisfaction_final': float,  # Final satisfaction (0.0-1.0)
                    'v0_energy': {
                        'initial_energy': 1.0,
                        'final_energy': float,  # Converged energy
                        'energy_descent_rate': float
                    },
                    'convergence_cycles': int,  # Cycles to convergence
                    'convergence_reason': str,  # 'satisfaction' or 'kairos_moment'
                    'kairos_cycle_index': Optional[int],
                    'phase5_family_id': Optional[str],
                    'bond_self_distance': float,  # Trauma activation level
                    'regime': Optional[str]  # 🆕 Current regime (EXPLORING, COMMITTED, etc.)
                },
                'tsk_record': Dict  # Complete TSK record (if enabled)
            }
        """
        # ✅ NOV 17: Reload learned state for Whiteheadian prehension
        # (Each occasion must feel all past occasions, including recent training)
        self.reload_learning_state()

        context = context or {}

        # 🕐 TEMPORAL AWARENESS: Add time/date context - November 15, 2025
        context['temporal'] = self._create_temporal_context()

        # 🌀 LLM BRIDGE: Assess feedback from previous turn - November 18, 2025 (Phase 1)
        if self.feedback_handler and self.last_emission_data:
            # Get session_id from context or generate one
            session_id = context.get('conversation_id', 'default_session')

            # Check if we have previous emission for this session
            if session_id in self.last_emission_data:
                last_data = self.last_emission_data[session_id]

                try:
                    # Assess satisfaction from user's current response
                    feedback = self.feedback_handler.assess_satisfaction(
                        user_response=text,
                        organism_emission=last_data['emission'],
                        context=context
                    )

                    # Update learning patterns (Hebbian, Pattern Learner, Organ Confidence)
                    update_results = self.feedback_handler.update_patterns(
                        feedback=feedback,
                        emission_data=last_data['metadata'],
                        hebbian_memory=self.hebbian_memory if hasattr(self, 'hebbian_memory') else None,
                        pattern_learner=self.pattern_learner if hasattr(self, 'pattern_learner') else None,
                        organ_confidence_tracker=self.organ_confidence_tracker if hasattr(self, 'organ_confidence_tracker') else None
                    )

                    # Store feedback in context for potential use
                    context['feedback'] = {
                        'estimated_satisfaction': feedback.estimated_satisfaction,
                        'confidence': feedback.confidence,
                        'update_results': update_results
                    }
                except Exception as e:
                    print(f"⚠️  Feedback assessment failed: {e}")

        # ═══════════════════════════════════════════════════════════════════
        # 🌀 Nov 18, 2025: EXTRACT ENTITIES **BEFORE** PHASE 2
        # Critical: NEXUS needs entities DURING V0 convergence cycles
        # ═══════════════════════════════════════════════════════════════════

        if self._memory_intent_detector and self._entity_extractor:
            try:
                # Detect memory intent - returns tuple (is_memory, intent_type, confidence, metadata)
                is_memory_related, intent_type, confidence, metadata = self._memory_intent_detector.detect(text)

                # Extract entities if memory-related
                current_turn_entities = []
                if is_memory_related:
                    # EntityExtractor.extract() expects: (text, intent_type, context, felt_state)
                    # Returns: Dict with 'mentioned_names', 'user_name', 'family_members', etc.
                    extraction_result = self._entity_extractor.extract(
                        text,
                        intent_type,
                        metadata,  # Context dict from MemoryIntentDetector
                        felt_state=None  # Will be None at this point (pre-processing)
                    )

                    # Convert extraction_result format to current_turn_entities format
                    # extraction_result has keys like: 'user_name', 'mentioned_names', 'family_members'
                    # We need format: [{'entity_value': 'Xeno', 'entity_type': 'person', ...}]

                    # Extract user_name
                    if 'user_name' in extraction_result:
                        current_turn_entities.append({
                            'entity_value': extraction_result['user_name'],
                            'entity_type': 'person',
                            'relationship': 'self',
                            'source': 'self_introduction'
                        })

                    # Extract mentioned_names
                    if 'mentioned_names' in extraction_result:
                        for name in extraction_result['mentioned_names']:
                            current_turn_entities.append({
                                'entity_value': name,
                                'entity_type': 'person',
                                'relationship': extraction_result.get('relationship_context', 'mentioned'),
                                'source': 'others_introduction'
                            })

                    # Extract family_members (from organ_prehension fallback)
                    if 'family_members' in extraction_result:
                        for member in extraction_result['family_members']:
                            current_turn_entities.append({
                                'entity_value': member['name'],
                                'entity_type': 'person',
                                'relationship': member.get('relation', 'family'),
                                'source': 'relationship_statement'
                            })

                    # Extract friends (from organ_prehension fallback)
                    if 'friends' in extraction_result:
                        for friend in extraction_result['friends']:
                            current_turn_entities.append({
                                'entity_value': friend['name'],
                                'entity_type': 'person',
                                'relationship': 'friend',
                                'source': 'relationship_statement'
                            })

                # Populate entity_prehension (NEXUS-compatible format)
                if current_turn_entities:
                    mentioned_entities = [
                        {
                            'name': entity['entity_value'],
                            'type': entity.get('entity_type', 'person'),
                            'relationship': entity.get('relationship'),
                            'source': entity.get('source', 'explicit')
                        }
                        for entity in current_turn_entities
                    ]

                    context['entity_prehension'] = {
                        'entity_memory_available': True,
                        'mentioned_entities': mentioned_entities,
                        'user_name': context.get('username', username if username else 'User')
                    }
                else:
                    context['entity_prehension'] = {
                        'entity_memory_available': False,
                        'mentioned_entities': [],
                        'user_name': context.get('username', username if username else 'User')
                    }

                # Store for entity-organ tracking
                context['current_turn_entities'] = current_turn_entities

            except Exception as e:
                print(f"   ⚠️  Entity extraction failed: {e}")
                # Fallback to empty entity prehension
                context['entity_prehension'] = {
                    'entity_memory_available': False,
                    'mentioned_entities': [],
                    'user_name': context.get('username', username if username else 'User')
                }
                context['current_turn_entities'] = []
        else:
            # Entity extractors not available
            context['entity_prehension'] = {
                'entity_memory_available': False,
                'mentioned_entities': [],
                'user_name': context.get('username', username if username else 'User')
            }
            context['current_turn_entities'] = []

        # 🌀 PHASE 1.6: Entity differentiation (detect if user asking about DAE) - November 14, 2025
        entity_ref = 'ambiguous'
        entity_confidence = 0.0
        organism_narrative = None
        organism_context = None

        if self.entity_differentiator:
            try:
                entity_ref, entity_confidence = self.entity_differentiator.detect_entity_reference(text)

                # If user asking about DAE, load organism self-narrative
                if entity_ref == 'dae' and self.unified_state:
                    organism_narrative = self.unified_state.generate_organism_self_narrative()
                    organism_context = self.unified_state.get_organism_context()

                    # Store in context for emission generator
                    context['entity_reference'] = entity_ref
                    context['entity_confidence'] = entity_confidence
                    context['organism_narrative'] = organism_narrative
                    context['organism_context'] = organism_context

                    print(f"   🌀 Entity Reference: {entity_ref} (confidence: {entity_confidence:.2f})")
                    print(f"   🌀 Organism self-awareness activated")
            except Exception as e:
                print(f"   ⚠️  Entity differentiation failed: {e}")

        # 🌀 PHASE 1.6: Add username to context for personalization - November 14, 2025
        if username:
            context['username'] = username

        # 🆕 Update regime if provided (Enhancement #1 - November 13, 2025)
        if regime is not None:
            self.current_regime = regime
            # Pass regime to emission generator for confidence modulation
            if self.emission_generator and hasattr(self.emission_generator, 'set_exploration_context'):
                self.emission_generator.set_exploration_context(regime=regime.value if isinstance(regime, SatisfactionRegime) else regime)

        # 🌀 Nov 18, 2025: EXTRACT ENTITIES FIRST (before prehension, before Phase 2)
        # This ensures newly mentioned entities are available during V0 convergence
        newly_extracted_entities = {}  # Track entities extracted THIS turn

        # 🔍 DEBUG: Trace entity extraction flow
        print(f"   🔍 ENTITY EXTRACTION DEBUG:")
        print(f"      user_id = {user_id}")
        print(f"      superject_learner exists = {self.superject_learner is not None}")

        if user_id and self.superject_learner:
            print(f"      ✅ Entering entity extraction block...")
            try:
                # Get current user profile
                user_profile = self.superject_learner.get_or_create_profile(user_id)
                print(f"      ✅ User profile loaded: {user_profile is not None}")
                current_entities = user_profile.entities if user_profile else {}
                print(f"      📊 Current entities: {len(current_entities)} categories")

                # 🌀 PHASE 1 SYMBIOTIC MODE (Nov 18, 2025): Use symbiotic extractor if available
                if hasattr(self, 'symbiotic_extractor') and self.symbiotic_extractor and Config.ENTITY_EXTRACTION_MODE == "symbiotic":
                    print(f"      🌀 Phase 1 Symbiotic Mode: {self.symbiotic_extractor.learning_mode} ({self.symbiotic_extractor.consultation_rates[self.symbiotic_extractor.learning_mode]*100:.0f}% LLM)")

                    # Extract entities using symbiotic extractor (OLLAMA teacher)
                    extraction_result = self.symbiotic_extractor.extract_entities_llm(
                        text=text,
                        current_entities=current_entities
                    )

                    # Also run pattern extraction for comparison (if enabled)
                    if Config.PATTERN_LLM_COMPARISON_ENABLED and hasattr(self, 'entity_neighbor_prehension') and self.entity_neighbor_prehension:
                        try:
                            # Extract entities using Phase 3B neighbor prehension (no word_occasions needed for comparison)
                            pattern_result_list = self.entity_neighbor_prehension.extract_entities(text, return_word_occasions=False)

                            # Convert Phase 3B list format to Dict format for comparison
                            # Phase 3B returns: [{'entity_value': 'Emma', 'entity_type': 'Person', ...}]
                            # Comparison expects: {'relationships': [{'name': 'Emma', ...}], 'places': [...]}
                            pattern_result_dict = {'relationships': [], 'places': [], 'emotions': [], 'mentioned_names': []}
                            for ent in pattern_result_list:
                                entity_type = ent.get('entity_type', '').lower()
                                entity_value = ent.get('entity_value', '')

                                if entity_type == 'person':
                                    pattern_result_dict['relationships'].append({'name': entity_value, 'type': 'Person'})
                                    pattern_result_dict['mentioned_names'].append(entity_value)
                                elif entity_type == 'place':
                                    pattern_result_dict['places'].append({'name': entity_value, 'type': 'Place'})
                                elif entity_type == 'emotion':
                                    pattern_result_dict['emotions'].append({'name': entity_value, 'type': 'Emotion'})
                                else:
                                    # Unknown type, add as mentioned name
                                    pattern_result_dict['mentioned_names'].append(entity_value)

                            # Compare pattern vs OLLAMA extraction
                            comparison = self.symbiotic_extractor.compare_extraction_methods(
                                pattern_entities=pattern_result_dict,
                                llm_entities=extraction_result
                            )
                            print(f"      📊 Pattern-OLLAMA F1: {comparison.get('f1_score', 0):.2f} (P:{len(pattern_result_list)} vs L:{comparison.get('llm_count', 0)})")
                        except Exception as e:
                            print(f"      ⚠️  Pattern comparison failed: {e}")

                    # Use OLLAMA entities (Phase 1)
                    new_entities = extraction_result
                    print(f"      ✅ Symbiotic extraction complete")

                else:
                    # Fallback to direct LLM extraction (current behavior)
                    print(f"      🧠 Calling LLM extraction for: '{text[:60]}...'")
                    new_entities = self.superject_learner.extract_entities_llm(
                        user_input=text,
                        current_entities=current_entities
                    )

                print(f"      ✅ Entity extraction returned: {new_entities is not None}")
                print(f"      📊 new_entities = {new_entities}")  # Show full content
                if new_entities:
                    print(f"      📊 New entities keys: {list(new_entities.keys())}")
                    for key, value in new_entities.items():
                        if value:
                            print(f"         - {key}: {len(value) if isinstance(value, list) else '1 item'}")
                        else:
                            print(f"         - {key}: (empty)")

                # Store newly extracted entities IMMEDIATELY
                if new_entities and user_profile:
                    print(f"      💾 Storing {len(new_entities)} entity categories...")
                    newly_extracted_entities = new_entities  # 🚨 CRITICAL: Track what was JUST extracted
                    user_profile.store_entities(new_entities)
                    self.superject_learner.save_profile(user_profile)

                    # Show extraction feedback
                    if 'memories' in new_entities:
                        num_memories = len(new_entities['memories'])
                        print(f"      📝 Extracted {num_memories} new memories")
                else:
                    print(f"      ⚠️  No new entities to store (new_entities empty or profile missing)")

            except Exception as e:
                print(f"      ⚠️  Entity extraction failed: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"      ❌ Skipping extraction (user_id={bool(user_id)}, learner={self.superject_learner is not None})")

        # 🌀 PRE-EMISSION ENTITY PREHENSION: Retrieve entity memory BEFORE organ activation (Nov 16, 2025)
        # This is the KEY innovation: entity context is available during organ processing,
        # enabling Entity Memory Nexus (EMN) formation and relational continuity.
        entity_prehension_result = None
        if user_id and self.entity_prehension:
            try:
                entity_prehension_result = self.entity_prehension.retrieve_relevant_entities(
                    user_input=text,
                    user_id=user_id
                )

                # 🚨 CRITICAL FIX (Nov 18, 2025): If entities were JUST extracted this turn, mark memory as available
                # This handles "I am Xeno" scenarios where the name is being introduced
                if newly_extracted_entities:
                    # Force entity_memory_available = True when entities were extracted THIS turn
                    entity_prehension_result['entity_memory_available'] = True

                    # Add newly extracted entities to mentioned_entities (they're implicitly mentioned by extraction)
                    newly_mentioned = []

                    # Check for user_name in various possible formats
                    if 'user_name' in newly_extracted_entities and newly_extracted_entities['user_name']:
                        newly_mentioned.append({
                            'name': newly_extracted_entities['user_name'],
                            'type': 'user_self',
                            'context': 'User identity (just introduced)',
                            'source': 'fresh_extraction'
                        })

                    # Check for any relationships/family members/manual entities
                    for key in ['relationships', 'family_members', 'manual_entities', 'memories']:
                        if key in newly_extracted_entities and newly_extracted_entities[key]:
                            for entity in newly_extracted_entities[key]:
                                if isinstance(entity, dict) and 'name' in entity:
                                    newly_mentioned.append({
                                        'name': entity['name'],
                                        'type': entity.get('type', 'person'),
                                        'context': f"Just mentioned ({key})",
                                        'source': 'fresh_extraction'
                                    })

                    # Merge with existing mentioned entities
                    existing_mentioned = entity_prehension_result.get('mentioned_entities', [])
                    entity_prehension_result['mentioned_entities'] = existing_mentioned + newly_mentioned

                    print(f"   🚨 FRESH ENTITIES: {len(newly_mentioned)} entities just extracted, marking memory available")

                # Store in context for organ enrichment
                context['entity_prehension'] = entity_prehension_result
                context['organ_context_enrichment'] = self.entity_prehension.inject_into_organ_context(
                    entity_prehension_result
                )

                # Show entity context if relevant
                if entity_prehension_result.get('entity_memory_available', False):
                    mentioned_count = len(entity_prehension_result.get('mentioned_entities', []))
                    relational_query = entity_prehension_result.get('relational_query_detected', False)

                    if relational_query or mentioned_count > 0:
                        print(f"   🌀 Pre-emission entity prehension:")
                        if entity_prehension_result.get('user_name'):
                            print(f"      User: {entity_prehension_result['user_name']}")
                        if relational_query:
                            print(f"      🔍 Relational query detected")
                        if mentioned_count > 0:
                            print(f"      Entities mentioned: {mentioned_count}")
                        richness = entity_prehension_result.get('historical_context', {}).get('memory_richness', 0.0)
                        print(f"      Memory richness: {richness:.2f}")

            except Exception as e:
                print(f"   ⚠️  Pre-emission entity prehension failed: {e}")
                entity_prehension_result = None

        # ✅ FIX #6: Populate current_turn_entities for EntityOrganTracker (Nov 16, 2025)
        # EntityOrganTracker.update() requires context['current_turn_entities']
        # Extract from entity_prehension result if available
        if context.get('entity_prehension', {}).get('entity_memory_available', False):
            mentioned_entities = context.get('entity_prehension', {}).get('mentioned_entities', [])
            if mentioned_entities:
                # Convert from entity prehension format to EntityOrganTracker format
                context['current_turn_entities'] = [
                    {
                        'entity_value': entity.get('name', ''),
                        'entity_type': entity.get('type', 'person'),
                        'relationship': entity.get('relationship'),
                        'source': entity.get('source', 'explicit')
                    }
                    for entity in mentioned_entities
                ]
                print(f"   🔍 DEBUG Fix #6: Set current_turn_entities with {len(context['current_turn_entities'])} entities")

        # 🌀 DAE 3.0 LEGACY INTEGRATION: Capture INITIAL felt-state (November 15, 2025)
        # For transformation-based family emergence, we need to capture the organism's
        # felt-state BEFORE processing user input. This enables DAE 3.0's proven
        # INPUT→OUTPUT transformation clustering approach.
        initial_felt_state = {
            'v0_initial': 1.0,  # Default starting energy (could be carried from previous turn)
            'organ_coherences': {
                'LISTENING': 0.5, 'EMPATHY': 0.5, 'WISDOM': 0.5,
                'AUTHENTICITY': 0.5, 'PRESENCE': 0.5, 'BOND': 0.5,
                'SANS': 0.5, 'NDAM': 0.5, 'RNX': 0.5, 'EO': 0.5, 'CARD': 0.5
            },
            'polyvagal_state': 'ventral',  # Default state
            'zone': 1,  # Default zone
            'satisfaction': 0.5,  # Neutral satisfaction
            'urgency': 0.0  # No urgency yet (user input not processed)
        }

        # Route to appropriate processing path
        if enable_phase2 and PHASE2_CONVERGENCE_AVAILABLE and self.meta_atoms:
            # PHASE 2 PATH: Multi-cycle V0 convergence with Kairos detection
            result = self._multi_cycle_convergence(text, context, enable_tsk_recording, initial_felt_state)
        else:
            # PHASE 1 PATH: Single-cycle processing (backward compatible)
            result = self._process_single_cycle(text, context, enable_tsk_recording, user_satisfaction)

        # 🌀 WEEK 3, DAYS 3-4: Delayed Feedback Learning (November 19, 2025)
        # 🌀 WEEK 3, DAY 5: Three-Layer Quality Modulation (November 19, 2025)
        # 🚨 MOVED HERE (Nov 19, 2025): Learning must happen for BOTH Phase 1 & Phase 2
        # Previously in _process_single_cycle(), but training uses Phase 2 path
        # Extract data from result dict for learning
        organ_results = result.get('organ_results', {})
        emission_text = result.get('emission_text', None)

        if organ_results:  # Learning happens for both processing paths
            print(f"   🔍 DEBUG LEARNING: organ_results available, entering learning block")
            print(f"   🔍 DEBUG LEARNING: user_satisfaction = {user_satisfaction}")
            print(f"   🔍 DEBUG LEARNING: emission_text = {emission_text}")
            try:
                # Get current turn number from context (default to 0 if not provided)
                current_turn_number = context.get('turn_number', 0) if context else 0

                # Track satisfaction for fingerprinting (need 3+ for pattern detection)
                if user_satisfaction is not None:
                    self.satisfaction_history.append(user_satisfaction)
                    # Keep only recent history (last 10 turns)
                    if len(self.satisfaction_history) > 10:
                        self.satisfaction_history = self.satisfaction_history[-10:]

                # STEP 1: Record outcome for PREVIOUS turn (if exists)
                # Turn N satisfaction → update Turn N-1 phrase quality
                # 🌀 NOW WITH THREE-LAYER QUALITY BOOST!
                if self.previous_turn_data and user_satisfaction is not None:
                    self._record_emission_outcome(
                        nexus_signature=self.previous_turn_data['signature'],
                        emitted_phrase_text=self.previous_turn_data['phrase'],
                        user_satisfaction=user_satisfaction,
                        current_turn=self.previous_turn_data['turn'],
                        organ_results=organ_results  # ← For Lyapunov stability calculation
                    )

                # STEP 2: Extract nexus signature from CURRENT turn's organ_results
                # This will be used to update quality when we see NEXT turn's satisfaction
                current_signature = None
                if self.emission_generator and hasattr(self.emission_generator, '_extract_nexus_signature_from_organs'):
                    current_signature = self.emission_generator._extract_nexus_signature_from_organs(organ_results)
                    if current_signature:
                        print(f"   🌀 Signature extracted for learning: {current_signature.nexus_type}")
                    else:
                        print(f"   ⚠️  Signature extraction returned None (organ_results keys: {list(organ_results.keys()) if organ_results else 'None'})")

                # STEP 3: Store CURRENT turn data for next iteration
                # (Will be updated when we process Turn N+1)
                if current_signature:
                    # Use dummy phrase if no emission (entity-memory training doesn't generate emissions)
                    # Pattern learner needs phrase text for logging, but actual learning uses signature
                    phrase_for_learning = emission_text if emission_text else f"<felt_state_{current_signature.nexus_type}>"
                    self.previous_turn_data = {
                        'signature': current_signature,
                        'phrase': phrase_for_learning,
                        'turn': current_turn_number
                    }
                    print(f"   🌀 Previous turn data stored (turn {current_turn_number}, phrase: {phrase_for_learning[:50]}...)")
                else:
                    # No signature extracted → clear previous_turn_data
                    # (Don't learn from turns without valid signatures)
                    self.previous_turn_data = None
                    print(f"   ⚠️  Previous turn data cleared (no valid signature)")

            except Exception as e:
                # Debug: Print exception details
                print(f"   ❌ Learning feedback exception: {e}")
                import traceback
                traceback.print_exc()

        # 🌀 PHASE 1 FOUNDATION: Record turn to user superject (Nov 14, 2025)
        if user_id and self.superject_learner:
            try:
                self.superject_learner.record_turn(
                    user_id=user_id,
                    turn_data=result,
                    user_satisfaction=user_satisfaction
                )
            except Exception as e:
                # 🌀 Phase 1.7: Enhanced error reporting (Nov 14, 2025)
                print(f"⚠️  Superject recording failed: {e}")
                print(f"   Debug: result type = {type(result).__name__}")
                if isinstance(result, dict):
                    print(f"   Debug: result keys = {list(result.keys())[:10]}")

        # 🌀 USER:SESSION:TURN HIERARCHY: Track turn within session (Nov 16, 2025)
        # This enables temporal entity context preservation:
        # - WHEN entities were mentioned (turn number)
        # - IN WHAT CONTEXT (emotional state, polyvagal)
        # - HOW ENTITY REFERENCES EVOLVE (session-level tracking)
        if user_id and self.session_manager:
            try:
                # Get or create session for this user
                session = self.session_manager.get_or_create_session(user_id)

                # Extract felt_state from result for turn tracking
                felt_state_snapshot = None
                if 'felt_states' in result:
                    from persona_layer.superject_structures import FeltStateSnapshot
                    fs = result.get('felt_states', {})

                    # Create FeltStateSnapshot from result data
                    felt_state_snapshot = FeltStateSnapshot(
                        timestamp=datetime.utcnow().isoformat(),
                        turn_id=f"{user_id}_session_{session.session_id}_turn_{len(session.turns) + 1}",
                        turn_number=len(session.turns) + 1,
                        session_id=session.session_id,
                        user_input_text=text,
                        emission_text=result.get('emission', ''),
                        entity_prehension=entity_prehension_result or {},
                        mentioned_entities=[
                            e.get('name', '') for e in (entity_prehension_result or {}).get('mentioned_entities', [])
                        ],
                        entity_references=(entity_prehension_result or {}).get('entity_references', []),
                        # Core felt-state fields that FeltStateSnapshot actually expects
                        organ_signature=[],  # TODO: Extract from organ results
                        active_organs=list(result.get('organ_results', {}).keys()),
                        dominant_nexuses=[n.get('type', 'unknown') for n in fs.get('nexuses', [])[:3]],
                        zone=fs.get('zone', 3),
                        zone_name=f"Zone {fs.get('zone', 3)}",
                        polyvagal_state=fs.get('eo_polyvagal_state', 'unknown'),
                        self_distance=fs.get('bond_self_distance', 0.5),
                        v0_energy=fs.get('v0_energy', {}).get('final_energy', 0.5) if isinstance(fs.get('v0_energy'), dict) else fs.get('v0_energy_final', 0.5),
                        satisfaction=fs.get('satisfaction_final', fs.get('satisfaction', 0.5)),
                        convergence_cycles=fs.get('convergence_cycles', 1),
                        transduction_mechanism=fs.get('transduction_mechanism'),
                        transduction_pathway=fs.get('transduction_pathway'),
                        ndam_urgency=fs.get('ndam_urgency_level', 0.0),
                        emission_confidence=fs.get('emission_confidence', 0.0),
                        emission_strategy=result.get('emission_strategy'),
                        kairos_detected=fs.get('kairos_detected', False)
                    )

                # Create turn record
                turn = self.session_manager.create_turn(
                    session=session,
                    user_input=text,
                    dae_response=result.get('emission', ''),
                    entity_prehension=entity_prehension_result,
                    felt_state=felt_state_snapshot,
                    processing_time_ms=result.get('processing_time_ms', 0.0),
                    emission_strategy=result.get('emission_strategy', 'unknown'),
                    user_satisfaction=user_satisfaction
                )

                # Add turn to session (updates trajectories, entity timeline, etc.)
                self.session_manager.add_turn(session, turn)

                # Store session info in result for downstream use
                result['session_info'] = {
                    'session_id': session.session_id,
                    'turn_number': turn.turn_number,
                    'session_total_turns': session.total_turns,
                    'entities_this_session': list(session.session_entities.keys()),
                    'polyvagal_trajectory': session.polyvagal_trajectory,
                    'crisis_session': session.crisis_session,
                    'breakthrough_session': session.breakthrough_session
                }

                # Show session tracking info if entities mentioned
                if turn.mentioned_entities:
                    print(f"   🌀 Session tracking: Turn {turn.turn_number}")
                    print(f"      Session entities: {list(session.session_entities.keys())}")
                    if turn.relational_query:
                        print(f"      🔍 Relational query in turn {turn.turn_number}")

            except Exception as e:
                print(f"⚠️  Session/turn tracking failed: {e}")

        # 🌀 PHASE 1.6: Record organism occasion (privacy-preserving) - November 14, 2025
        if user_id and self.unified_state:
            try:
                self.unified_state.record_organism_occasion(
                    occasion_data=result,
                    user_id=user_id  # Will be hashed for privacy
                )
            except Exception as e:
                print(f"⚠️  Organism occasion recording failed: {e}")

        # 🆕 Level 2 Fractal Rewards: Update organ confidences (Nov 15, 2025)
        if self.organ_confidence:
            try:
                # Extract organ results and emission quality
                organ_results = result.get('organ_results', {})
                emission_confidence = result.get('emission_confidence', 0.0)

                # Update organ confidences based on emission success
                self.organ_confidence.update(
                    organ_results=organ_results,
                    emission_confidence=emission_confidence,
                    user_satisfaction=user_satisfaction
                )
            except Exception as e:
                print(f"⚠️  Organ confidence update failed: {e}")

        # 🌀 Quick Win #7: Update entity-organ associations (Nov 15, 2025)
        # 🔍 DEBUG (Nov 16): Add logging to diagnose why EntityOrganTracker not populating
        print(f"   🔍 DEBUG EntityTracker: self.entity_organ_tracker exists = {bool(self.entity_organ_tracker)}")
        print(f"   🔍 DEBUG EntityTracker: current_turn_entities exists = {bool(context.get('current_turn_entities'))}")
        if context.get('current_turn_entities'):
            print(f"   🔍 DEBUG EntityTracker: current_turn_entities count = {len(context.get('current_turn_entities'))}")

        if self.entity_organ_tracker and context.get('current_turn_entities'):
            try:
                # Extract entities from current turn (passed from dae_interactive.py)
                # Format: List[{'entity_value': 'Emma', 'entity_type': 'Person'}, ...]
                extracted_entities = context.get('current_turn_entities', [])
                organ_results = result.get('organ_results', {})

                print(f"   ✅ DEBUG EntityTracker: Calling update() with {len(extracted_entities)} entities")

                # Build felt-state context
                felt_state = {
                    'polyvagal_state': result.get('felt_states', {}).get('eo_polyvagal_state', 'mixed'),
                    'v0_energy': result.get('felt_states', {}).get('v0_energy', {}).get('final_energy', 0.5),
                    'urgency': result.get('felt_states', {}).get('ndam_urgency', 0.0),
                    'self_distance': result.get('felt_states', {}).get('bond_self_distance', 0.5)
                }

                # Update entity-organ associations
                self.entity_organ_tracker.update(
                    extracted_entities=extracted_entities,
                    organ_results=organ_results,
                    felt_state=felt_state,
                    emission_satisfaction=user_satisfaction
                )
                print(f"   ✅ DEBUG EntityTracker: update() completed successfully")
            except Exception as e:
                print(f"⚠️  Entity-organ tracking update failed: {e}")
                import traceback
                traceback.print_exc()

        # 🌀 PHASE 3B: Epoch Learning Tracker Updates (November 18, 2025)
        # 5 new trackers for neighbor prehension intelligence and LLM independence

        # Tracker 1: Word-level organ activation patterns
        if self.word_occasion_tracker and context and 'word_occasions' in context:
            try:
                word_occasions = context['word_occasions']
                self.word_occasion_tracker.update(word_occasions)

                # Optional: Log pattern growth
                stats = self.word_occasion_tracker.get_statistics()
                if stats['total_updates'] % 100 == 0:  # Every 100 updates
                    print(f"   📊 Word patterns: {stats['total_word_patterns']} words, "
                          f"{stats['reliable_patterns']} reliable")

            except Exception as e:
                print(f"⚠️  Word occasion tracker update failed: {e}")
                import traceback
                traceback.print_exc()

        # Tracker 2: Multi-cycle convergence optimization
        if self.cycle_convergence_tracker and result.get('felt_states'):
            try:
                felt_states = result['felt_states']

                # Build context for cycle pattern learning
                cycle_context = {
                    'polyvagal_state': felt_states.get('eo_polyvagal_state', 'mixed'),
                    'urgency': felt_states.get('ndam_urgency_level', 0.0)
                }

                self.cycle_convergence_tracker.update_convergence_complete(
                    cycles_used=felt_states.get('convergence_cycles', 1),
                    converged=felt_states.get('kairos_detected', False),
                    context=cycle_context
                )

                # Optional: Log optimal cycle count
                stats = self.cycle_convergence_tracker.get_statistics()
                if stats.get('global', {}).get('total_attempts', 0) % 50 == 0:  # Every 50 attempts
                    mean_cycles = stats.get('global', {}).get('mean_cycles_to_kairos', 0.0)
                    print(f"   📊 Cycle optimization: mean {mean_cycles:.2f} cycles to kairos")

            except Exception as e:
                print(f"⚠️  Cycle convergence tracker update failed: {e}")
                import traceback
                traceback.print_exc()

        # Tracker 3: 4-gate cascade quality monitoring
        if self.gate_cascade_quality_tracker and context and 'word_occasions' in context:
            try:
                # Extract gate_results from entity dicts in word_occasions
                word_occasions = context['word_occasions']
                for word_occ in word_occasions:
                    if word_occ.is_entity() and hasattr(word_occ, 'intersection_score'):
                        # Create gate_results dict from word_occasion attributes
                        gate_results = {
                            'gate_1_intersection': {
                                'passed': word_occ.intersection_score >= 1.5 if hasattr(word_occ, 'intersection_score') else False,
                                'score': getattr(word_occ, 'intersection_score', 0.0)
                            },
                            'gate_2_coherence': {
                                'passed': word_occ.coherence_score >= 0.4 if hasattr(word_occ, 'coherence_score') else False,
                                'score': getattr(word_occ, 'coherence_score', 0.0)
                            },
                            'gate_3_satisfaction': {
                                'passed': 0.45 <= word_occ.satisfaction_score <= 0.85 if hasattr(word_occ, 'satisfaction_score') else False,
                                'score': getattr(word_occ, 'satisfaction_score', 0.0)
                            },
                            'gate_4_felt_energy': {
                                'passed': word_occ.felt_energy <= 0.7 if hasattr(word_occ, 'felt_energy') else False,
                                'score': getattr(word_occ, 'felt_energy', 1.0)
                            }
                        }

                        # Update each gate
                        for gate_name, gate_data in gate_results.items():
                            self.gate_cascade_quality_tracker.update_gate(
                                gate_name=gate_name,
                                passed=gate_data.get('passed', False),
                                input_context=context
                            )

                # Optional: Log bottleneck detection
                stats = self.gate_cascade_quality_tracker.get_statistics()
                bottleneck = stats.get('bottleneck_gate')
                if bottleneck and stats['total_attempts'] % 50 == 0:  # Every 50 attempts
                    gate_stats = stats['gate_statistics'].get(bottleneck, {})
                    print(f"   📊 Gate bottleneck: {bottleneck} "
                          f"({gate_stats.get('pass_rate', 0.0):.1%} pass rate)")

            except Exception as e:
                print(f"⚠️  Gate cascade quality tracker update failed: {e}")
                import traceback
                traceback.print_exc()

        # Tracker 4: NEXUS vs LLM decision tracking (CRITICAL for LLM independence)
        if self.nexus_vs_llm_tracker and context and 'nexus_extraction_used' in context:
            try:
                decision = 'nexus' if context['nexus_extraction_used'] else 'llm'

                self.nexus_vs_llm_tracker.update(
                    nexus_confidence=context.get('nexus_confidence', 0.0),
                    nexus_entities=context.get('nexus_entities', []),
                    llm_entities=context.get('llm_entities', []),
                    decision=decision,
                    user_satisfaction=user_satisfaction if user_satisfaction else 0.5,
                    processing_time_ms=context.get('extraction_time_ms', 0.0)
                )

                # Optional: Log progress toward 80% NEXUS usage
                stats = self.nexus_vs_llm_tracker.get_statistics()
                total_decisions = stats.get('usage', {}).get('total_decisions', 0)
                if total_decisions > 0 and total_decisions % 50 == 0:  # Every 50 decisions
                    progress = self.nexus_vs_llm_tracker.get_progress_toward_target()
                    print(f"   📊 NEXUS usage: {progress['current_nexus_rate']:.1%} "
                          f"(target: {progress['target_nexus_rate']:.0%}, "
                          f"{progress['progress_percentage']:.0f}% complete)")

            except Exception as e:
                print(f"⚠️  NEXUS vs LLM tracker update failed: {e}")
                import traceback
                traceback.print_exc()

        # Tracker 5: Neighbor word → organ boost learning
        if self.neighbor_word_context_tracker and context and 'word_occasions' in context:
            try:
                word_occasions = context['word_occasions']

                # Update neighbor context patterns for each entity word
                for word_occ in word_occasions:
                    self.neighbor_word_context_tracker.update(word_occ)

                # Optional: Log top learned patterns
                stats = self.neighbor_word_context_tracker.get_statistics()
                if stats['total_updates'] % 100 == 0:  # Every 100 updates
                    print(f"   📊 Neighbor patterns: {stats['total_neighbor_patterns']} pairs, "
                          f"{stats['reliable_patterns']} reliable")

            except Exception as e:
                print(f"⚠️  Neighbor word context tracker update failed: {e}")
                import traceback
                traceback.print_exc()

        return result

    def _process_single_cycle(
        self,
        text: str,
        context: Dict[str, Any],
        enable_tsk_recording: bool,
        user_satisfaction: Optional[float] = None  # 🌀 Week 3 Day 5: For learning feedback
    ) -> Dict[str, Any]:
        """
        Phase 1 processing path: Single-cycle organ processing.

        Preserved for backward compatibility with existing epoch training.
        """
        # Create TextOccasions from input text
        # 🌀 Nov 14, 2025: Pass context for entity-aware enrichment
        occasions = self._create_text_occasions(text, context=context)

        # 🌀 Nov 14, 2025: Build entity context for all organs (Phase 2.1)
        # Extract entity data from context for organ prehension
        # 🌀 Nov 15, 2025: Extract user_id for NEXUS organ
        # 🌀 Nov 16, 2025: FIXED - Pass entity_prehension and organ_context_enrichment (was using wrong key 'stored_entities')
        # 🌀 Nov 16, 2025: ADDED - Pass temporal context for NEXUS temporal coherence horizon
        user_id = context.get('user_id', 'default_user')

        entity_context = {
            'entity_prehension': context.get('entity_prehension', {}),
            'organ_context_enrichment': context.get('organ_context_enrichment', {}),
            'temporal': context.get('temporal', {}),  # For NEXUS temporal coherence horizon
            'username': context.get('username')
        }

        # Process through ALL 12 organs (5 conversational + 6 trauma/context-aware + 1 memory)
        # Cycle=0 for single-pass epoch training
        # 🌀 Nov 14, 2025: Pass entity_context to all organs
        # 🌀 Nov 15, 2025: Added NEXUS (12th organ) for Neo4j memory prehension
        organ_results = {
            # 5 conversational organs
            'LISTENING': self.listening.process_text_occasions(occasions, cycle=0, context=entity_context),
            'EMPATHY': self.empathy.process_text_occasions(occasions, cycle=0, context=entity_context),
            'WISDOM': self.wisdom.process_text_occasions(occasions, cycle=0, context=entity_context),
            'AUTHENTICITY': self.authenticity.process_text_occasions(occasions, cycle=0, context=entity_context),
            'PRESENCE': self.presence.process_text_occasions(occasions, cycle=0, context=entity_context),

            # 3 trauma-aware organs (Phase 1 integration - Nov 11, 2025)
            'BOND': self.bond.process_text_occasions(occasions, cycle=0, context=entity_context),
            'SANS': self.sans.process_text_occasions(occasions, cycle=0, context=entity_context),
            'NDAM': self.ndam.process_text_occasions(occasions, cycle=0, context=entity_context),

            # 3 Phase 2 organs (temporal, polyvagal, scaling - Nov 11, 2025)
            'RNX': self.rnx.process_text_occasions(occasions, cycle=0, context=entity_context),
            'EO': self.eo.process_text_occasions(occasions, cycle=0, context=entity_context),

            # 🌀 12th organ: NEXUS (Neo4j entity memory - Nov 15, 2025 - Quick Win #9)
            'NEXUS': self.nexus.process_text_occasions(occasions, cycle=0, context={**entity_context, 'user_id': user_id}),
        }

        # CARD needs EXTENDED context (entity data + organ signals for response scaling)
        # Build extended context dict with entity data + signals from EO, NDAM, BOND, RNX
        eo_result = organ_results.get('EO')
        ndam_result = organ_results.get('NDAM')
        bond_result = organ_results.get('BOND')
        rnx_result = organ_results.get('RNX')

        card_context = {
            # Entity context (Nov 14, 2025) - ✅ FIX (Nov 16): Use correct keys
            'entity_prehension': entity_context.get('entity_prehension', {}),
            'organ_context_enrichment': entity_context.get('organ_context_enrichment', {}),
            'temporal': entity_context.get('temporal', {}),
            'username': entity_context.get('username'),
            # Organ signal context (existing)
            'polyvagal_state': getattr(eo_result, 'polyvagal_state', 'mixed_state') if eo_result else 'mixed_state',
            'urgency': getattr(ndam_result, 'mean_urgency', 0.5) if ndam_result else 0.5,
            'self_distance': getattr(bond_result, 'mean_self_distance', 0.5) if bond_result else 0.5,
            'temporal_state': getattr(rnx_result, 'temporal_state', 'concrescent') if rnx_result else 'concrescent'
        }

        organ_results['CARD'] = self.card.process_text_occasions(occasions, cycle=0, context=card_context)

        # Extract organ coherences from ALL 11 organs
        # Organs return typed dataclass objects (e.g., ListeningResult, BONDResult, RNXResult, EOResult, CARDResult)
        # Access coherence attribute directly (not via .get())
        organ_coherences = {}
        for organ_name, result in organ_results.items():
            # All organ result objects have 'coherence' attribute
            coherence = getattr(result, 'coherence', 0.0)
            organ_coherences[organ_name] = coherence

        # 🆕 LEVEL 2 FRACTAL REWARDS: Apply learned organ weight multipliers (November 16, 2025)
        # This transduces organ confidence learning into actual emission quality
        # High-confidence organs get boosted (1.0→1.2×), low-confidence organs get dampened (0.8×)
        if hasattr(self, 'organ_confidence') and self.organ_confidence:
            # Reload from disk to get latest learning (trainer may have updated)
            self.organ_confidence._load()
            for organ_name in organ_coherences:
                multiplier = self.organ_confidence.get_weight_multiplier(organ_name)
                organ_coherences[organ_name] *= multiplier
                # Clamp to [0.0, 1.0] after multiplication
                organ_coherences[organ_name] = min(1.0, organ_coherences[organ_name])

        # Compute mean coherence across organs
        mean_coherence = np.mean(list(organ_coherences.values()))

        # Simplified V0 energy descent (single cycle for epoch training)
        # In full organism, this would be iterative descent with Kairos detection
        initial_energy = 1.0
        final_energy = 1.0 - (mean_coherence * 0.6)  # Simple descent based on coherence
        energy_descent_rate = initial_energy - final_energy

        # Compute satisfaction based on coherence
        # Higher coherence → higher satisfaction
        # Lower energy → higher satisfaction
        satisfaction_final = (mean_coherence * 0.7) + ((1.0 - final_energy) * 0.3)
        satisfaction_final = max(0.0, min(1.0, satisfaction_final))  # Clamp to [0, 1]

        # Convergence metadata (simplified for single-cycle training)
        convergence_cycles = 1
        convergence_reason = 'satisfaction' if satisfaction_final >= 0.75 else 'max_cycles'
        kairos_cycle_index = 0 if satisfaction_final >= 0.85 else None

        # ===== EMISSION GENERATION (11-Organ Dual-Path) =====
        # Generate emission from organ felt states (optional, if emission components available)
        emission_text = None
        emission_confidence = 0.0
        emission_path = None
        zone_name = 'unknown'
        zone_id = 0
        emission_nexus_count = 0

        # 🆕 PHASE C2: Set organ_results for lure-informed phrase selection (November 13, 2025)
        if self.emission_generator and hasattr(self.emission_generator, 'set_organ_results'):
            self.emission_generator.set_organ_results(organ_results)

        if self.semantic_extractor and self.nexus_composer and self.emission_generator:
            try:
                # 🆕 PHASE 1: Build semantic fields DIRECTLY from organ atom_activations
                # Bypass semantic_field_extractor (which uses weak substring matching)
                # Use direct atom activations computed by organs
                from persona_layer.semantic_field_extractor import SemanticField

                semantic_fields = {}
                print(f"   🔍 DEBUG: Building semantic fields from {len(organ_results)} organs...")
                for organ_name, result in organ_results.items():
                    # All organs now have atom_activations field populated
                    atom_activations = getattr(result, 'atom_activations', {})
                    if atom_activations:  # Only include if not empty
                        # 🔧 FILTER OUT NaN/Inf VALUES (from SANS division by zero)
                        import math
                        filtered_activations = {
                            atom: activation
                            for atom, activation in atom_activations.items()
                            if not math.isnan(activation) and not math.isinf(activation)
                        }

                        if not filtered_activations:
                            print(f"      {organ_name}: All activations were NaN/Inf, skipping")
                            continue

                        # 🆕 LEVEL 2 FRACTAL REWARDS: Apply organ weight multipliers to atom activations
                        # This transduces learned organ confidence into nexus formation
                        # High-confidence organs contribute more to nexuses, low-confidence organs contribute less
                        organ_multiplier = 1.0
                        if hasattr(self, 'organ_confidence') and self.organ_confidence:
                            organ_multiplier = self.organ_confidence.get_weight_multiplier(organ_name)
                            # Apply multiplier to all atom activations for this organ
                            filtered_activations = {
                                atom: min(1.0, activation * organ_multiplier)
                                for atom, activation in filtered_activations.items()
                            }

                        print(f"      {organ_name}: {len(filtered_activations)} atoms (×{organ_multiplier:.3f})")
                        for atom, activation in sorted(filtered_activations.items(), key=lambda x: x[1], reverse=True)[:3]:
                            print(f"        - {atom}: {activation:.4f}")
                        # Wrap in SemanticField object (required by nexus_composer)
                        # Also apply multiplier to coherence for consistent weighting
                        weighted_coherence = min(1.0, getattr(result, 'coherence', 0.0) * organ_multiplier)
                        semantic_fields[organ_name] = SemanticField(
                            organ_name=organ_name,
                            coherence=weighted_coherence,
                            lure=getattr(result, 'lure', 0.0),
                            atom_activations=filtered_activations,
                            pattern_count=len(getattr(result, 'patterns', []))
                        )

                print(f"   🔍 DEBUG: Total semantic fields: {len(semantic_fields)}")
                print(f"   🔍 DEBUG: Intersection threshold: {self.nexus_composer.intersection_threshold}")

                # 🆕 RECONSTRUCTION PIPELINE (November 12, 2025)
                # Use reconstruction pipeline if available (wires all components with SELF governance)
                if self.reconstruction_pipeline:
                    print(f"\n   🌀 Using Reconstruction Pipeline (Authentic Voice)")

                    # Extract NDAM urgency and EO polyvagal state
                    ndam_result = organ_results.get('NDAM')
                    eo_result = organ_results.get('EO')

                    ndam_urgency = getattr(ndam_result, 'mean_urgency', 0.0) if ndam_result else 0.0
                    eo_polyvagal = getattr(eo_result, 'polyvagal_state', 'mixed_state') if eo_result else 'mixed_state'

                    # 🌀 Nov 14, 2025: Build entity context string for LLM
                    entity_context_string = None
                    if context and 'stored_entities' in context:
                        stored_entities = context['stored_entities']
                        entity_parts = []
                        if stored_entities.get('user_name'):
                            entity_parts.append(f"User's name: {stored_entities['user_name']}")
                        if stored_entities.get('family_members'):
                            family_names = [m.get('name', '') for m in stored_entities['family_members'] if m.get('name')]
                            if family_names:
                                entity_parts.append(f"Family: {', '.join(family_names)}")
                        if stored_entities.get('friends'):
                            friend_names = [f.get('name', '') for f in stored_entities['friends'] if f.get('name')]
                            if friend_names:
                                entity_parts.append(f"Friends: {', '.join(friend_names)}")
                        if entity_parts:
                            entity_context_string = " | ".join(entity_parts)

                    # Build felt state for reconstruction
                    felt_state_for_reconstruction = {
                        'organ_coherences': {name: getattr(result, 'coherence', 0.0)
                                            for name, result in organ_results.items()},
                        'semantic_fields': semantic_fields,
                        'v0_energy': final_energy,
                        'satisfaction': satisfaction_final,
                        'convergence_cycles': convergence_cycles,
                        'transduction_state': None,  # TODO: Add transduction state
                        'eo_polyvagal_state': eo_polyvagal,
                        'ndam_urgency': ndam_urgency,
                        'kairos_detected': kairos_cycle_index is not None,
                        # 🌀 PHASE LLM1: Felt-guided LLM parameters (Nov 13, 2025)
                        'user_input': text,
                        'organ_results': organ_results,
                        'memory_context': None,  # TODO: Add memory context from hybrid LLM
                        # 🌀 Nov 14, 2025: Entity-organism integration
                        'entity_context_string': entity_context_string,
                        'memory_intent': False
                    }

                    # Build context for reconstruction (includes DAE 3.0 family learner + entity context)
                    reconstruction_context = {
                        'user_message': text,
                        'family_v0_learner': self.family_v0_learner,  # 🆕 DAE 3.0 (Levels 2+4)
                        # 🌀 Nov 14, 2025: Entity-organism integration - pass stored entities
                        'stored_entities': context.get('stored_entities', {}) if context else {},
                        'username': context.get('username') if context else None,
                        # 🌀 Nov 14, 2025: Entity memory context for reconstruction pipeline (CRITICAL FIX)
                        'entity_context_string': context.get('entity_context_string', '') if context else '',
                        'memory_intent': context.get('memory_intent', False) if context else False
                    }

                    # Call reconstruction pipeline
                    reconstruction_result = self.reconstruction_pipeline.reconstruct_emission(
                        felt_state=felt_state_for_reconstruction,
                        context=reconstruction_context
                    )

                    # Extract results
                    emission_text = reconstruction_result['emission_text']
                    emission_confidence = reconstruction_result['confidence']
                    emission_path = reconstruction_result['strategy']
                    emission_nexus_count = reconstruction_result['nexuses_used']
                    zone_name = reconstruction_result.get('zone', 'unknown')
                    zone_id = reconstruction_result.get('zone_id', 0)

                    print(f"   ✅ Reconstruction complete:")
                    print(f"      Strategy: {emission_path}")
                    print(f"      Confidence: {emission_confidence:.3f}")
                    print(f"      Zone: {zone_name} (Zone {zone_id})")
                    print(f"      Safe: {reconstruction_result['safe']}")

                else:
                    # FALLBACK: Direct emission generation (backward compatible)
                    print(f"\n   ⚠️  Using direct emission (reconstruction pipeline unavailable)")

                    # Stage 2: Compose nexuses (organ coalitions in semantic space)
                    nexuses = self.nexus_composer.compose_nexuses(semantic_fields)

                    # Stage 3: Generate emission phrases (dual-path: intersection vs direct)
                    # Generate 1-3 phrases depending on nexus quality
                    num_emissions = 3 if len(nexuses) >= 5 else (2 if len(nexuses) >= 2 else 1)

                    # 🌀 Nov 14, 2025: Extract entity context from context dict
                    entity_context_string = context.get('entity_context_string', '') if context else ''
                    memory_intent = context.get('memory_intent', False) if context else False

                    # 🕐 Nov 15, 2025: Extract temporal context from context dict
                    temporal_context = context.get('temporal') if context else None

                    # 🌀 LLM BRIDGE: Get turn history for multi-turn context - November 18, 2025 (Phase 2)
                    memory_context = None
                    if self.turn_history:
                        session_id = context.get('conversation_id', 'default_session')
                        memory_context = self.turn_history.get_context_string(
                            session_id=session_id,
                            num_turns=3,  # Last 3 turns
                            include_metadata=False  # Just conversation, not felt-states
                        )

                    emitted_phrases = self.emission_generator.generate_emissions(
                        nexuses=nexuses,
                        num_emissions=num_emissions,
                        prefer_variety=True,
                        user_input=text,  # 🌀 For felt-guided LLM
                        organ_results=organ_results,  # 🌀 For felt-guided LLM
                        v0_energy=final_energy,  # 🌀 For felt-guided LLM
                        satisfaction=satisfaction_final,  # 🌀 For felt-guided LLM
                        memory_context=memory_context,  # 🌀 LLM BRIDGE: Turn history context (Phase 2 - Nov 18, 2025)
                        entity_context_string=entity_context_string,  # 🌀 PHASE 1.8++ CRITICAL FIX (Nov 14, 2025)
                        memory_intent=memory_intent,  # 🌀 PHASE 1.8++ CRITICAL FIX (Nov 14, 2025)
                        temporal_context=temporal_context  # 🕐 TEMPORAL (Nov 15, 2025)
                    )

                    # Combine emitted phrases into single emission text
                    if emitted_phrases:
                        emission_text = ' '.join([phrase.text for phrase in emitted_phrases])
                        emission_confidence = sum([phrase.confidence for phrase in emitted_phrases]) / len(emitted_phrases)
                        emission_path = emitted_phrases[0].strategy  # Primary strategy used
                    else:
                        emission_text = None
                        emission_confidence = 0.0
                        emission_path = 'none'

                    emission_nexus_count = len(nexuses)
                    zone_name = 'unknown'
                    zone_id = 0

            except Exception as e:
                # Emission generation failed, continue without it
                print(f"   ⚠️  Emission generation failed: {e}")
                emission_text = None
                emission_confidence = 0.0
                emission_path = 'error'

        # Phase 2 COMPLETE - all 11 organs now operational!

        # Phase 5 family assignment (if available)
        phase5_family_id = None
        if self.phase5_learning:
            try:
                # 🌀 DAE 3.0 LEGACY INTEGRATION: Transformation-based learning (November 15, 2025)

                # Build INITIAL felt-state (defaults - Phase 1 path doesn't have V0 convergence history)
                initial_felt_state = {
                    'v0_initial': 1.0,
                    'organ_coherences': {
                        'LISTENING': 0.5, 'EMPATHY': 0.5, 'WISDOM': 0.5,
                        'AUTHENTICITY': 0.5, 'PRESENCE': 0.5, 'BOND': 0.5,
                        'SANS': 0.5, 'NDAM': 0.5, 'RNX': 0.5, 'EO': 0.5, 'CARD': 0.5
                    },
                    'polyvagal_state': 'ventral',
                    'zone': 1,
                    'satisfaction': 0.5,
                    'urgency': 0.0
                }

                # Build FINAL felt-state from processed results
                # 🚨 CRITICAL FIX (Nov 16): Compute zone from BOND mean_self_distance
                # BOND doesn't have a .zone attribute, it has mean_self_distance
                bond_result = organ_results.get('BOND')
                if bond_result and hasattr(bond_result, 'mean_self_distance'):
                    bond_self_dist = bond_result.mean_self_distance
                else:
                    bond_self_dist = 0.5

                # Convert BOND self_distance to SELF Matrix zone (1-5)
                # Zone mapping follows DAE 3.0 SELF Matrix conventions
                if bond_self_dist > 0.8:
                    computed_zone = 5  # Collapse/shutdown (far from SELF)
                elif bond_self_dist > 0.6:
                    computed_zone = 4  # Protective parts
                elif bond_self_dist > 0.4:
                    computed_zone = 3  # Manager parts
                elif bond_self_dist > 0.2:
                    computed_zone = 2  # Firefighter parts
                else:
                    computed_zone = 1  # SELF (connected, low distance)

                # 🚨 CRITICAL FIX (Nov 16): NDAM has mean_urgency, not urgency attribute
                ndam_result = organ_results.get('NDAM')
                if ndam_result and hasattr(ndam_result, 'mean_urgency'):
                    ndam_urgency = ndam_result.mean_urgency
                else:
                    ndam_urgency = 0.0

                final_felt_state = {
                    'v0_initial': v0_initial if 'v0_initial' in locals() else 1.0,
                    'v0_final': v0_final if 'v0_final' in locals() else 0.5,
                    'convergence_cycles': convergence_cycles if 'convergence_cycles' in locals() else 3.0,
                    'organ_coherences': {
                        organ_name: getattr(organ_results.get(organ_name), 'coherence', 0.5)
                        for organ_name in ['LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY',
                                          'PRESENCE', 'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD']
                    },
                    'polyvagal_state': getattr(organ_results.get('EO'), 'polyvagal_state', 'ventral') if organ_results.get('EO') else 'ventral',
                    'zone': computed_zone,  # 🚨 FIX: Use computed zone from BOND self_distance
                    'satisfaction_final': satisfaction_final,
                    'urgency': ndam_urgency,  # 🚨 FIX: Use NDAM's mean_urgency attribute
                    'emission_path': emission_path if 'emission_path' in locals() else 'fusion',
                    'kairos_detected': kairos_detected if 'kairos_detected' in locals() else False,
                    'nexus_count': len(nexuses) if 'nexuses' in locals() else 0
                }

                # Call transformation-based learning (DAE 3.0 approach)
                learning_result = self.phase5_learning.learn_from_conversation_transformation(
                    initial_felt_state=initial_felt_state,
                    final_felt_state=final_felt_state,
                    emission_text=emission_text if emission_text else '',
                    user_message=text,
                    conversation_id=context.get('conversation_id', 'unknown') if context else 'unknown'
                )

                if learning_result:
                    phase5_family_id = learning_result.get('family_id')

                    # Log family assignment for visibility
                    if phase5_family_id:
                        family_sim = learning_result.get('similarity', 0.0)
                        is_new = learning_result.get('is_new_family', False)
                        sat_improvement = learning_result.get('satisfaction_improvement', 0.0)
                        action = "CREATED" if is_new else "JOINED"
                        print(f"   🌀 Phase 5: {action} {phase5_family_id} (sim: {family_sim:.3f}, Δsat: {sat_improvement:+.3f})")
            except Exception as e:
                print(f"   ⚠️  Phase 5 learning failed: {e}")
                import traceback
                traceback.print_exc()
                phase5_family_id = None

        # BOND self_distance (trauma activation level) - FROM REAL BOND ORGAN!
        # Extract from BOND organ processing result (Phase 1 integration)
        bond_result = organ_results.get('BOND')
        bond_self_distance = getattr(bond_result, 'mean_self_distance', 0.0) if bond_result else 0.0

        # RNX temporal state (conversation rhythm) - FROM REAL RNX ORGAN!
        # Extract from RNX organ processing result (Phase 2 integration)
        rnx_result = organ_results.get('RNX')
        rnx_temporal_state = getattr(rnx_result, 'temporal_state', 'concrescent') if rnx_result else 'concrescent'
        rnx_volatility = getattr(rnx_result, 'volatility', 0.0) if rnx_result else 0.0

        # EO polyvagal state (safety/threat detection) - FROM REAL EO ORGAN!
        # Extract from EO organ processing result (Phase 2 integration)
        eo_result = organ_results.get('EO')
        eo_polyvagal_state = getattr(eo_result, 'polyvagal_state', 'mixed_state') if eo_result else 'mixed_state'
        eo_state_confidence = getattr(eo_result, 'state_confidence', 0.5) if eo_result else 0.5
        eo_self_distance_modifier = getattr(eo_result, 'self_distance_modifier', 0.5) if eo_result else 0.5

        # CARD response scaling (response calibration) - FROM REAL CARD ORGAN!
        # Extract from CARD organ processing result (Phase 2 integration)
        card_result = organ_results.get('CARD')
        card_recommended_scale = getattr(card_result, 'recommended_scale', 'moderate') if card_result else 'moderate'
        card_length_target = getattr(card_result, 'length_target', 300) if card_result else 300
        card_detail_level = getattr(card_result, 'detail_level', 0.5) if card_result else 0.5

        # Build felt states structure
        felt_states = {
            'text_occasions': self._occasions_to_dict(occasions),
            'organ_coherences': organ_coherences,
            'satisfaction_final': satisfaction_final,
            'v0_energy': {
                'initial_energy': initial_energy,
                'final_energy': final_energy,
                'energy_descent_rate': energy_descent_rate
            },
            'convergence_cycles': convergence_cycles,
            'convergence_reason': convergence_reason,
            'kairos_cycle_index': kairos_cycle_index,
            'phase5_family_id': phase5_family_id,
            'bond_self_distance': bond_self_distance,
            'rnx_temporal_state': rnx_temporal_state,  # Phase 2: temporal rhythm
            'rnx_volatility': rnx_volatility,          # Phase 2: conversation volatility
            'eo_polyvagal_state': eo_polyvagal_state,  # Phase 2: polyvagal detection
            'eo_state_confidence': eo_state_confidence,  # Phase 2: polyvagal confidence
            'eo_self_distance_modifier': eo_self_distance_modifier,  # Phase 2: EO→BOND correlation
            'card_recommended_scale': card_recommended_scale,  # Phase 2: response scaling
            'card_length_target': card_length_target,  # Phase 2: response length
            'card_detail_level': card_detail_level,    # Phase 2: detail level
            # 🆕 LURE ATTRACTOR FIELDS: Whiteheadian process tracking (November 13, 2025)
            'eo_lure': getattr(organ_results.get('EO'), 'lure', 0.0),
            'eo_lure_field': getattr(organ_results.get('EO'), 'lure_field', {}),
            'ndam_lure': getattr(organ_results.get('NDAM'), 'lure', 0.0),
            'ndam_salience_field': getattr(organ_results.get('NDAM'), 'salience_field', {}),
            'rnx_lure': getattr(organ_results.get('RNX'), 'lure', 0.0),
            'rnx_temporal_field': getattr(organ_results.get('RNX'), 'temporal_field', {}),
            # 🆕 CONVERSATIONAL LURE FIELDS: (Phase B, November 13, 2025)
            'empathy_lure': getattr(organ_results.get('EMPATHY'), 'lure', 0.0),
            'empathy_emotional_lure_field': getattr(organ_results.get('EMPATHY'), 'emotional_lure_field', {}),
            'wisdom_lure': getattr(organ_results.get('WISDOM'), 'lure', 0.0),
            'wisdom_pattern_lure_field': getattr(organ_results.get('WISDOM'), 'pattern_lure_field', {}),
            'authenticity_lure': getattr(organ_results.get('AUTHENTICITY'), 'lure', 0.0),
            'authenticity_vulnerability_lure_field': getattr(organ_results.get('AUTHENTICITY'), 'vulnerability_lure_field', {}),
            'lure_contribution_to_v0': (
                getattr(organ_results.get('EO'), 'lure', 0.0) * 0.20 +
                getattr(organ_results.get('NDAM'), 'lure', 0.0) * 0.20 +
                getattr(organ_results.get('RNX'), 'lure', 0.0) * 0.15 +
                getattr(organ_results.get('EMPATHY'), 'lure', 0.0) * 0.20 +
                getattr(organ_results.get('WISDOM'), 'lure', 0.0) * 0.15 +
                getattr(organ_results.get('AUTHENTICITY'), 'lure', 0.0) * 0.10
            ),  # Total lure pull in V0 descent (6 organs)
            # 🆕 PHASE C2: Composite lure signature for emission (November 13, 2025)
            'lure_signature_used_in_emission': (
                self.emission_generator.lure_selector.get_lure_signature_for_tsk(organ_results)
                if self.emission_generator and hasattr(self.emission_generator, 'lure_selector') else None
            ),
            'mean_coherence': mean_coherence,
            # Emission generation results (11-organ dual-path)
            'emission_text': emission_text,            # Generated emission text (or None)
            'emission_confidence': emission_confidence,  # Emission confidence [0,1]
            'emission_path': emission_path,            # 'intersection', 'direct', or 'none'
            'emission_nexus_count': emission_nexus_count  # Number of nexuses formed
        }

        # 🆕 PERSONA LAYER: Modulate emission with companion personality (November 12, 2025)
        if self.persona_layer and emission_text:
            try:
                # Get user profile
                user_id = context.get('user_id', None)
                user_profile = self.user_profile_manager.get_or_create_profile(user_id) if self.user_profile_manager else None

                # Get SELF Matrix zone from BOND self-distance
                zone = 1  # Default: Zone 1 (SELF)
                if bond_self_distance > 0.7:
                    zone = 5  # Collapse/shutdown
                elif bond_self_distance > 0.5:
                    zone = 4  # Protective
                elif bond_self_distance > 0.35:
                    zone = 3  # Manager
                elif bond_self_distance > 0.2:
                    zone = 2  # Firefighter

                # Build template context from organ felt states
                template_context = TemplateContext(
                    zone=zone,
                    ndam_urgency=getattr(organ_results.get('NDAM'), 'mean_urgency', 0.0) if organ_results.get('NDAM') else 0.0,  # 🚨 FIX
                    polyvagal_state=eo_polyvagal_state,
                    confidence=emission_confidence,
                    v0_energy=final_energy,
                    kairos_detected=False,  # Single cycle doesn't detect kairos
                    organ_coherences=organ_coherences,
                    active_meta_atoms=[],  # No meta-atoms in Phase 1
                    transduction_pathway=None,  # No transduction in Phase 1
                    user_input=text,
                    response_length=user_profile.response_length_preference if user_profile else "moderate",
                    humor_tolerance=user_profile.humor_tolerance if user_profile else 0.5,
                    small_talk_openness=user_profile.small_talk_openness if user_profile else 0.5,
                    llm_usage_consent=user_profile.llm_usage_consent if user_profile else False
                )

                # Modulate emission
                modulation_result = self.persona_layer.modulate_emission(
                    base_emission=emission_text,
                    context=template_context,
                    user_profile=user_profile.__dict__ if user_profile else None,
                    conversation_history=None  # TODO: Fetch from user_profile_manager
                )

                # Update emission_text with modulated version
                original_emission = emission_text
                # PersonaLayer returns 'emission', not 'modulated_emission'
                emission_text = modulation_result.get('modulated_emission') or modulation_result.get('emission', emission_text)
                felt_states['emission_text'] = emission_text

                # Store persona layer metadata
                felt_states['persona_layer_applied'] = True
                felt_states['persona_templates_used'] = modulation_result.get('templates_used', [])
                felt_states['persona_query_type'] = modulation_result.get('query_type')
                felt_states['persona_llm_queried'] = modulation_result.get('llm_queried', False)

            except Exception as e:
                import traceback
                print(f"   ⚠️  Persona layer modulation failed: {e}")
                traceback.print_exc()
                # Continue with unmodulated emission
                felt_states['persona_layer_applied'] = False

        # Build TSK record (if enabled)
        tsk_record = {}
        if enable_tsk_recording:
            tsk_record = {
                'timestamp': datetime.now().isoformat(),
                'conversation_id': context.get('conversation_id', 'unknown'),
                'grid_type': context.get('training_phase', 'unknown').upper(),
                'felt_states': felt_states,
                'context': context
            }

        # 🚨 REMOVED (Nov 19, 2025): Learning block moved to process_text() line ~1445
        # This method (_process_single_cycle) is only used for Phase 1 (backward compat)
        # Training uses Phase 2 (_multi_cycle_convergence), so learning here never executed
        # Learning must happen AFTER routing decision where both paths rejoin

        return {
            'mode': 'processing_complete',
            'felt_states': felt_states,
            'tsk_record': tsk_record,
            'organ_results': organ_results,  # Raw organ results for debugging
            # Emission data at top level for backward compatibility
            'emission_text': emission_text,
            'emission_confidence': emission_confidence,
            'emission_path': emission_path,
            'emission_nexus_count': emission_nexus_count,
            # 🌀 Zone info (Phase 1.5c: Zone 5 tracking)
            'zone': zone_name,
            'zone_id': zone_id,
            # 🚨 Nov 18, 2025: Return entity prehension result for testing/validation
            'entity_prehension': entity_prehension_result if entity_prehension_result else {}
        }

    def process_text_with_phase3b_context(
        self,
        text: str,
        user_id: Optional[str] = None,
        username: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Process text with automatic Phase 3B context extraction.

        This is a convenience wrapper around process_text() that automatically:
        1. Extracts entities with word_occasions using EntityNeighborPrehension
        2. Builds Phase 3B context (word_occasions, nexus_entities, gate_results)
        3. Calls process_text() with the extended context

        This ensures all 5 Phase 3B epoch learning trackers receive proper context data:
        - WordOccasionTracker: word-level organ activation patterns
        - CycleConvergenceTracker: multi-cycle convergence optimization
        - GateCascadeQualityTracker: 4-gate cascade quality monitoring
        - NexusVsLLMDecisionTracker: NEXUS vs LLM decision tracking
        - NeighborWordContextTracker: neighbor word → organ boost learning

        Args:
            text: Input text to process
            user_id: Optional user ID for context
            username: Optional username for context
            **kwargs: Additional arguments passed to process_text()
                     (enable_phase2, enable_tsk_recording, user_satisfaction, etc.)

        Returns:
            Same dict as process_text(), with extended context passed to trackers

        Example:
            >>> result = wrapper.process_text_with_phase3b_context(
            ...     "My daughter Emma is worried",
            ...     user_id="epoch_1_training",
            ...     username="training_user",
            ...     enable_phase2=True,
            ...     enable_tsk_recording=True,
            ...     user_satisfaction=0.8
            ... )
        """
        # Get or create context
        context = kwargs.get('context', {})

        # Phase 3B: Extract entities with word_occasions
        if hasattr(self, 'entity_neighbor_prehension') and self.entity_neighbor_prehension:
            try:
                import time

                # Extract entities with word_occasions (Phase 3B)
                nexus_start = time.time()
                extraction_result = self.entity_neighbor_prehension.extract_entities(
                    text,
                    return_word_occasions=True
                )

                # Unpack result (could be tuple or just list)
                if isinstance(extraction_result, tuple) and len(extraction_result) == 2:
                    nexus_entities, word_occasions = extraction_result
                else:
                    # Backward compatibility: no word_occasions returned
                    nexus_entities = extraction_result
                    word_occasions = []

                nexus_time_ms = (time.time() - nexus_start) * 1000.0

                # Compute NEXUS confidence (max across all entities)
                nexus_confidence = max(
                    [e.get('confidence_score', 0.0) for e in nexus_entities],
                    default=0.0
                )

                # Extend context with Phase 3B data
                context['word_occasions'] = word_occasions
                context['nexus_entities'] = nexus_entities
                context['nexus_confidence'] = nexus_confidence
                context['extraction_time_ms'] = nexus_time_ms
                context['nexus_extraction_used'] = nexus_confidence >= 0.7

            except Exception as e:
                print(f"⚠️  Phase 3B context extension failed: {e}")
                import traceback
                traceback.print_exc()
                # Continue with empty Phase 3B context
                context['word_occasions'] = []
                context['nexus_entities'] = []
                context['nexus_extraction_used'] = False
        else:
            # No entity_neighbor_prehension available, use empty context
            context['word_occasions'] = []
            context['nexus_entities'] = []
            context['nexus_extraction_used'] = False

        # Add user context if provided
        if user_id:
            context['user_id'] = user_id
        if username:
            context['username'] = username

        # Call original process_text with extended context
        # 🌀 Phase 3B Fix #4 (Nov 18, 2025): Pass user_id/username as separate parameters
        # These must be passed BOTH in context dict AND as parameters for entity extraction
        kwargs['context'] = context
        return self.process_text(
            text,
            user_id=user_id,
            username=username,
            **kwargs
        )

    def _create_text_occasions(self, text: str, context: Optional[Dict] = None) -> List[TextOccasion]:
        """
        Create TextOccasions from input text (Whiteheadian actual occasions).

        Args:
            text: Input text string
            context: Optional context dict containing stored_entities, username, etc.

        Returns:
            List of TextOccasion objects (words/phrases with positions)
        """
        # Simple tokenization: split on whitespace and punctuation
        # In full organism, this would be more sophisticated (semantic chunking)
        words = text.split()

        occasions = []
        position = 0
        for word in words:
            # Create dummy embedding (384-dim zeros) for epoch training
            # In full organism, this would be actual semantic embeddings
            dummy_embedding = np.zeros(384)

            # Use proper hierarchical chunk_id format (doc_para_sent_chunk)
            # Expected by TextOccasion._parse_chunk_id() method
            occasion = TextOccasion(
                chunk_id=f"doc_0_para_0_sent_0_chunk_{position}",
                position=position,
                text=word,
                embedding=dummy_embedding
            )
            occasions.append(occasion)
            position += 1

        # 🌀 Nov 14, 2025: Entity-aware enrichment (Phase 1.2)
        # Enrich occasions with entity context for organism prehension
        if context and 'stored_entities' in context:
            stored_entities = context['stored_entities']

            for occasion in occasions:
                # Add stored entities to occasion (felt context, not symbolic lookup)
                occasion.known_entities = stored_entities

                # Detect entity references in THIS occasion's text
                entity_refs = self._detect_entity_references(occasion.text, stored_entities)
                occasion.entity_references = entity_refs['references']
                occasion.entity_match_confidence = entity_refs['confidences']

        return occasions

    def _detect_entity_references(self, text: str, stored_entities: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect entity references in text using simple felt-based matching (DAE 3.0 compliant).

        NOT symbolic AI pattern matching - just simple case-insensitive substring presence.
        Organisms learn entity patterns through felt prehension, not symbolic rules.

        Args:
            text: Occasion text (single word/phrase)
            stored_entities: Known entities from memory

        Returns:
            Dict with 'references' list and 'confidences' dict
        """
        references = []
        confidences = {}

        if not stored_entities:
            return {'references': references, 'confidences': confidences}

        text_lower = text.lower()

        # Simple felt-based detection: check if entity name appears in text
        # Start with highest confidence entity types

        # User name (highest priority)
        if 'user_name' in stored_entities:
            name = stored_entities['user_name']
            if name and name.lower() in text_lower:
                references.append(name)
                confidences[name] = 0.95  # High confidence for exact name match

        # Family members
        if 'family_members' in stored_entities:
            for member in stored_entities['family_members']:
                name = member.get('name', '')
                if name and name.lower() in text_lower:
                    references.append(name)
                    confidences[name] = 0.85  # High confidence for family

        # Friends
        if 'friends' in stored_entities:
            for friend in stored_entities['friends']:
                name = friend.get('name', '')
                if name and name.lower() in text_lower:
                    references.append(name)
                    confidences[name] = 0.80  # Medium-high for friends

        # Preferences (lower confidence - more abstract)
        if 'preferences' in stored_entities:
            for pref_key, pref_value in stored_entities['preferences'].items():
                if isinstance(pref_value, str) and pref_value.lower() in text_lower:
                    references.append(pref_value)
                    confidences[pref_value] = 0.60  # Lower for preferences

        return {'references': references, 'confidences': confidences}

    def _occasions_to_dict(self, occasions: List[TextOccasion]) -> List[Dict[str, Any]]:
        """
        Convert TextOccasion objects to dictionary format for JSON serialization.

        Args:
            occasions: List of TextOccasion objects

        Returns:
            List of dictionaries with occasion data
        """
        return [
            {
                'chunk_id': occ.chunk_id,
                'text': occ.text,
                'position': occ.position
            }
            for occ in occasions
        ]

    def _create_temporal_context(self) -> Dict[str, Any]:
        """
        Create rich temporal context for organism awareness.

        🕐 TEMPORAL AWARENESS: November 15, 2025
        Makes organism aware of current time/date during processing.

        Returns:
            Dictionary with temporal context:
            {
                'timestamp': '2025-11-15T20:30:45.123456',
                'date': '2025-11-15',
                'time': '20:30:45',
                'hour': 20,
                'minute': 30,
                'time_of_day': 'evening',  # morning/afternoon/evening/night
                'day_of_week': 'Friday',
                'day_of_week_num': 4,  # 0=Monday, 6=Sunday
                'is_weekend': False,
                'is_weekday': True,
                'is_morning': False,
                'is_afternoon': False,
                'is_evening': True,
                'is_night': False,
                'is_work_hours': False
            }
        """
        now = datetime.now()

        hour = now.hour

        # Categorize time of day
        if 5 <= hour < 12:
            time_of_day = "morning"
            is_morning = True
            is_afternoon = is_evening = is_night = False
        elif 12 <= hour < 17:
            time_of_day = "afternoon"
            is_afternoon = True
            is_morning = is_evening = is_night = False
        elif 17 <= hour < 21:
            time_of_day = "evening"
            is_evening = True
            is_morning = is_afternoon = is_night = False
        else:
            time_of_day = "night"
            is_night = True
            is_morning = is_afternoon = is_evening = False

        # Day of week info
        day_of_week_num = now.weekday()  # 0=Monday, 6=Sunday
        is_weekend = day_of_week_num >= 5
        is_weekday = day_of_week_num < 5

        # Work hours (9am-5pm on weekdays)
        is_work_hours = (9 <= hour < 17) and is_weekday

        return {
            'timestamp': now.isoformat(),
            'date': now.strftime('%Y-%m-%d'),
            'time': now.strftime('%H:%M:%S'),
            'hour': hour,
            'minute': now.minute,

            # Categorical time
            'time_of_day': time_of_day,
            'day_of_week': now.strftime('%A'),
            'day_of_week_num': day_of_week_num,
            'is_weekend': is_weekend,
            'is_weekday': is_weekday,

            # Time-specific flags
            'is_morning': is_morning,
            'is_afternoon': is_afternoon,
            'is_evening': is_evening,
            'is_night': is_night,
            'is_work_hours': is_work_hours
        }

    def _multi_cycle_convergence(
        self,
        text: str,
        context: Dict[str, Any],
        enable_tsk_recording: bool,
        initial_felt_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Phase 2 processing path: Multi-cycle V0 convergence with Kairos detection.

        Implements Whiteheadian process philosophy:
        - ConversationalOccasions (tokens as experiencing subjects)
        - Felt affordances accumulate DURING prehension
        - V0 energy descends through cycles
        - Kairos moment detection gates emission
        - Mature propositions POST-convergence
        """
        print("\n🌀 Phase 2: Multi-cycle V0 convergence")

        # Create ConversationalOccasions (tokens as experiencing subjects)
        occasions = self._create_conversational_occasions(text)
        print(f"   Created {len(occasions)} conversational occasions")

        # Multi-cycle convergence (2-4 cycles expected)
        max_cycles = 5
        convergence_threshold = 0.1  # ΔE < 0.1
        kairos_detected = False
        kairos_cycle = None

        # 🆕 Transduction trajectory tracking (November 12, 2025)
        transduction_trajectory = []  # Track nexus evolution across cycles
        prev_transduction_state = None

        # Define meta-atom names for salience evaluation
        meta_atom_names = {'trauma_aware', 'safety_restoration', 'window_of_tolerance',
                          'compassion_safety', 'fierce_holding', 'relational_attunement',
                          'temporal_grounding', 'kairos_emergence', 'coherence_integration', 'somatic_wisdom'}

        # 🛡️ Phase 1.5H: Heckling intelligence assessment (Nov 14, 2025)
        heckling_assessment = None

        for cycle in range(1, max_cycles + 1):
            print(f"\n   Cycle {cycle}:")

            # Process all organs for this cycle
            # 🌀 Nov 14, 2025: Pass context for entity-aware enrichment
            organ_results = self._process_organs_with_v0(occasions, cycle, context=context)

            # 🛡️ CYCLE 1 ONLY: Assess for crisis/heckling (Phase 1.5H - Nov 14, 2025)
            if cycle == 1 and self.heckling_intel:
                try:
                    # Extract NDAM urgency and EO polyvagal state from first cycle
                    ndam_result = organ_results.get('NDAM')
                    ndam_urgency = getattr(ndam_result, 'mean_urgency', 0.0) if ndam_result else 0.0

                    eo_result = organ_results.get('EO')
                    polyvagal_state = getattr(eo_result, 'polyvagal_state', 'mixed_state') if eo_result else 'mixed_state'

                    # Get user rapport from context (if available from superject)
                    user_rapport = context.get('user_rapport', 0.5)

                    # Assess for crisis vs heckling
                    heckling_assessment = self.heckling_intel.assess(
                        text=text,
                        ndam_urgency=ndam_urgency,
                        polyvagal_state=polyvagal_state,
                        user_rapport=user_rapport
                    )

                    # Enhance NDAM urgency if heckling detected
                    if heckling_assessment.is_heckling:
                        original_urgency = ndam_urgency
                        ndam_urgency = enhance_ndam_with_heckling(ndam_urgency, heckling_assessment)

                        # Update NDAM result with enhanced urgency
                        if ndam_result and hasattr(ndam_result, 'mean_urgency'):
                            ndam_result.mean_urgency = ndam_urgency
                            print(f"   🛡️  Heckling detected: {heckling_assessment.intent.value}")
                            print(f"      NDAM urgency adjusted: {original_urgency:.2f} → {ndam_urgency:.2f}")
                            print(f"      Safe for banter: {heckling_assessment.safe_for_banter}")

                    if heckling_assessment.is_genuine_crisis:
                        print(f"   ⚠️  GENUINE CRISIS DETECTED - Grounding prioritized")
                        print(f"      Crisis indicators: {', '.join(heckling_assessment.crisis_indicators[:3])}")

                except Exception as e:
                    print(f"   ⚠️  Heckling assessment failed: {e}")
                    heckling_assessment = None

            # Store felt affordances in occasions
            for occasion in occasions:
                organ_coherences = {
                    organ: getattr(result, 'coherence', 0.0)
                    for organ, result in organ_results.items()
                }

                # Add felt affordances from this cycle
                for organ_name, result in organ_results.items():
                    atom_activations = getattr(result, 'atom_activations', {})
                    lure = getattr(result, 'lure', 0.5)

                    for atom, activation in atom_activations.items():
                        # Filter NaN/Inf
                        if not (np.isnan(activation) or np.isinf(activation)):
                            occasion.add_felt_affordance(
                                atom=atom,
                                organ_name=organ_name,
                                confidence=activation,
                                lure_intensity=lure
                            )

                # V0 energy descent (🆕 with lure contribution from EO/NDAM/RNX)
                occasion.descend_v0_energy(organ_coherences, organ_results)

                # 🌀 Phase 2 (Nov 15, 2025): Calculate field coherence using DAE 3.0 std formula
                # Measures organ harmony: coherence = 1 - std([organ_outputs])
                # Pass organ_results dict containing coherence/confidence values
                field_coherence = occasion._calculate_field_coherence(organ_results)
                occasion.field_coherence = field_coherence
                occasion.field_coherence_history.append(field_coherence)

                # 🆕 SALIENCE: Evaluate salience and set subjective aim
                if self.salience_model:
                    # Extract meta-atom activations for salience evaluation
                    meta_atoms = {}
                    for organ_name, result in organ_results.items():
                        atom_activations = getattr(result, 'atom_activations', {})
                        for atom, activation in atom_activations.items():
                            # Only include meta-atoms (10 bridge atoms)
                            if atom in meta_atom_names:
                                if atom not in meta_atoms:
                                    meta_atoms[atom] = activation
                                else:
                                    # Take max if multiple organs activate same meta-atom
                                    meta_atoms[atom] = max(meta_atoms[atom], activation)

                    # 🆕 Extract organ insights for salience evaluation
                    # BOND: IFS parts and SELF-distance
                    bond_result = organ_results.get('BOND')
                    bond_self_distance_base = getattr(bond_result, 'mean_self_distance', 0.5) if bond_result else 0.5
                    bond_dominant_part = getattr(bond_result, 'dominant_part', None) if bond_result else None

                    # EO: Polyvagal state
                    eo_result = organ_results.get('EO')
                    eo_polyvagal_state = getattr(eo_result, 'polyvagal_state', 'mixed_state') if eo_result else 'mixed_state'
                    eo_state_confidence = getattr(eo_result, 'state_confidence', 0.5) if eo_result else 0.5

                    # 🆕 FIX 3: MODULATE SELF-distance with polyvagal state (SELF_MATRIX formula)
                    # From DAE_GOV_SELF_MATRIX_MATHEMATICAL_ADDENDUM.md:
                    # d_SELF = base_distance + polyvagal_modifier
                    polyvagal_modifiers = {
                        "ventral_vagal": -0.10,   # Safe & Social → pulls toward SELF
                        "sympathetic": +0.15,     # Fight/Flight → pushes toward urgency
                        "dorsal_vagal": +0.30,    # Shutdown → pushes toward collapse
                        "mixed_state": 0.0        # No modulation (fallback)
                    }

                    polyvagal_modifier = polyvagal_modifiers.get(eo_polyvagal_state, 0.0)
                    bond_self_distance = max(0.0, min(1.0, bond_self_distance_base + polyvagal_modifier))  # Clamp [0,1]

                    # NDAM: Crisis urgency
                    ndam_result = organ_results.get('NDAM')
                    ndam_urgency_level = getattr(ndam_result, 'mean_urgency', 0.0) if ndam_result else 0.0  # 🚨 FIX: Use mean_urgency, not urgency_level
                    ndam_dominant_urgency = getattr(ndam_result, 'dominant_urgency_type', None) if ndam_result else None  # 🚨 FIX: dominant_urgency_type

                    # RNX: Temporal state
                    rnx_result = organ_results.get('RNX')
                    rnx_temporal_state = getattr(rnx_result, 'temporal_state', 'concrescent') if rnx_result else 'concrescent'
                    rnx_volatility = getattr(rnx_result, 'volatility', 0.0) if rnx_result else 0.0

                    # CARD: Response scaling
                    card_result = organ_results.get('CARD')
                    card_recommended_scale = getattr(card_result, 'recommended_scale', 'moderate') if card_result else 'moderate'

                    # Build prehension dict for salience evaluation
                    prehension = {
                        "organ_coherences": organ_coherences,
                        "meta_atoms": meta_atoms,
                        "nexuses": [],  # Will be filled post-convergence
                        "v0_energy": occasion.v0_energy,
                        "cycle": cycle,
                        "kairos_detected": False,  # Not checked yet
                        "satisfaction": occasion.satisfaction,
                        "v0_energy_prev": occasion._prev_v0_energy,
                        "satisfaction_prev": occasion._prev_satisfaction,
                        "text": text,

                        # 🆕 FIX 1: Pass organ insights to salience
                        "bond_self_distance": bond_self_distance,
                        "bond_dominant_part": bond_dominant_part,
                        "eo_polyvagal_state": eo_polyvagal_state,
                        "eo_state_confidence": eo_state_confidence,
                        "ndam_urgency_level": ndam_urgency_level,
                        "ndam_dominant_urgency": ndam_dominant_urgency,
                        "rnx_temporal_state": rnx_temporal_state,
                        "rnx_volatility": rnx_volatility,
                        "card_recommended_scale": card_recommended_scale
                    }

                    # Evaluate salience
                    salience_results = self.salience_model.evaluate(prehension)

                    # Set subjective aim from salience
                    occasion.set_subjective_aim(
                        lure_direction=salience_results['morphogenetic_guidance'],
                        intensity=salience_results['morphogenetic_pressure'],
                        ethical_weight=salience_results['process_terms']['ethical_salience_field'],
                        morphogenetic_guidance=salience_results['morphogenetic_guidance']
                    )

                    # 🆕 FIX: Extract trauma markers for per-cycle transduction recording
                    salience_trauma_markers = salience_results.get('trauma_markers', {})
                else:
                    # Ensure variable is defined even if salience model not active
                    salience_trauma_markers = {}

                # Check Kairos
                if occasion.detect_kairos():
                    kairos_detected = True
                    kairos_cycle = cycle

            # Check convergence (compute mean values first)
            mean_energy = np.mean([occ.v0_energy for occ in occasions])
            mean_satisfaction = np.mean([occ.satisfaction for occ in occasions])
            mean_energy_change = np.mean([
                abs(occ.v0_energy - occ._prev_v0_energy)
                for occ in occasions
            ])

            print(f"      V0 energy: {mean_energy:.3f}")
            print(f"      Satisfaction: {mean_satisfaction:.3f}")
            print(f"      Energy change: {mean_energy_change:.3f}")
            print(f"      Kairos: {kairos_detected}")

            # 🆕 MULTI-CYCLE TRANSDUCTION: Record per-cycle state (November 16, 2025)
            if self.transduction_evaluator and TRANSDUCTION_AVAILABLE:
                try:
                    # Classify nexus type from current cycle's V0 energy + organ insights
                    cycle_nexus_type, cycle_nexus_category = classify_nexus_type_from_v0(
                        v0_energy=mean_energy,
                        satisfaction=mean_satisfaction,
                        bond_self_distance=bond_self_distance,
                        ndam_urgency_level=ndam_urgency_level,
                        eo_polyvagal_state=eo_polyvagal_state
                    )

                    # Compute transductive vocabulary for this cycle
                    cycle_transductive_vocab = compute_transductive_vocabulary(
                        salience_metrics=salience_trauma_markers,
                        organ_activations=organ_coherences,
                        satisfaction=mean_satisfaction,
                        v0_energy=mean_energy
                    )

                    # Simplified per-cycle state (rhythm_coherence and mutual_satisfaction computed post-loop)
                    # Use placeholder values, they'll be overwritten in final state
                    cycle_rhythm_coherence = getattr(organ_results.get('RNX'), 'coherence', 0.5)
                    cycle_relational_available = check_relational_field_available(
                        bond_self_distance,
                        eo_polyvagal_state,
                        organ_coherences.get('EMPATHY', 0.5)
                    )

                    # Create per-cycle transduction state
                    cycle_transduction_state = NexusTransductionState(
                        current_type=cycle_nexus_type,
                        current_category=cycle_nexus_category,
                        cycle_num=cycle,
                        v0_energy=mean_energy,
                        satisfaction=mean_satisfaction,
                        mutual_satisfaction=mean_satisfaction * 0.8,  # Proxy until full compute
                        rhythm_coherence=cycle_rhythm_coherence,
                        field_resonance=0.5,  # Placeholder, nexus not yet formed
                        signal_inflation=cycle_transductive_vocab['signal_inflation'],
                        salience_drift=cycle_transductive_vocab['salience_drift'],
                        prehensive_overload=cycle_transductive_vocab['prehensive_overload'],
                        coherence_leakage=cycle_transductive_vocab['coherence_leakage'],
                        relational_field_available=cycle_relational_available,
                        protective_field_active=(bond_self_distance > 0.4),
                        bond_self_distance=bond_self_distance,
                        ndam_urgency_level=ndam_urgency_level,
                        eo_polyvagal_state=eo_polyvagal_state,
                        rnx_temporal_coherence=cycle_rhythm_coherence
                    )

                    # Append to trajectory (multi-cycle recording!)
                    transduction_trajectory.append(cycle_transduction_state)

                except Exception as e:
                    print(f"      ⚠️ Per-cycle transduction recording failed: {e}")

            if mean_energy_change < convergence_threshold or kairos_detected:
                convergence_reason = 'kairos' if kairos_detected else 'satisfaction'
                print(f"   ✓ Convergence at cycle {cycle} ({convergence_reason})")
                break

        # 🆕 DAE 3.0: Update organ coupling (Fractal Level 3) - November 12, 2025
        if self.organ_coupling_learner and organ_results:
            self.organ_coupling_learner.update_coupling(
                organ_results=organ_results,
                satisfaction=mean_satisfaction,
                verbose=False  # Set to True to see coupling updates
            )

        # Mature propositions POST-CONVERGENCE
        print("\n   Maturing propositions...")
        for occasion in occasions:
            occasion.mature_propositions_from_affordances()

        total_propositions = sum(len(occ.mature_propositions) for occ in occasions)
        print(f"   ✓ {total_propositions} mature propositions created")

        # Build semantic fields from mature propositions
        semantic_fields = self._build_semantic_fields_from_propositions(occasions)
        print(f"   ✓ {len(semantic_fields)} semantic fields created")

        # 🔍 DEBUG: Show meta-atoms in semantic fields
        meta_atom_names = {'trauma_aware', 'safety_restoration', 'window_of_tolerance',
                          'compassion_safety', 'fierce_holding', 'relational_attunement',
                          'temporal_grounding', 'kairos_emergence', 'coherence_integration', 'somatic_wisdom'}
        for organ, field in semantic_fields.items():
            organ_meta_atoms = {atom: val for atom, val in field.atom_activations.items() if atom in meta_atom_names}
            if organ_meta_atoms:
                print(f"      {organ} meta-atoms: {organ_meta_atoms}")

        # 🆕 PHASE 3: Activate meta-atoms based on organ results (November 12, 2025)
        meta_atom_activations = []
        if self.meta_atom_activator and organ_results:
            print(f"\n   🧬 Activating meta-atoms...")

            # 🌀 Phase 2 (Nov 15, 2025): Get field coherence from converged occasion
            # Use mean field coherence across all cycles for nexus modulation
            mean_field_coherence = 0.0
            if occasions:
                field_coherences = [occ.field_coherence for occ in occasions if hasattr(occ, 'field_coherence')]
                if field_coherences:
                    mean_field_coherence = sum(field_coherences) / len(field_coherences)

            meta_atom_activations = self.meta_atom_activator.activate_meta_atoms(
                organ_results=organ_results,
                verbose=True,
                field_coherence=mean_field_coherence
            )

            # Add meta-atom activations to semantic fields for nexus composition
            if meta_atom_activations:
                # Convert dict to list, add meta-atoms
                semantic_fields_list = list(semantic_fields.values())
                semantic_fields_with_meta = self.meta_atom_activator.add_meta_atoms_to_semantic_fields(
                    semantic_fields=semantic_fields_list,
                    meta_atom_activations=meta_atom_activations
                )

                # The returned list has: [original fields...] + [meta-atom fields...]
                # Extract just the newly added meta-atom fields
                original_count = len(semantic_fields_list)
                for i, meta_field in enumerate(semantic_fields_with_meta[original_count:]):
                    # Use meta-atom field's organ_name as key (already prefixed with META_)
                    semantic_fields[meta_field.organ_name] = meta_field

                print(f"   ✓ {len(meta_atom_activations)} meta-atoms activated and added to semantic fields")

        # 🆕 SALIENCE: Extract trauma markers and morphogenetic guidance BEFORE emission
        salience_trauma_markers = {}
        salience_morphogenetic_guidance = None
        if self.salience_model and len(self.salience_model.salience_history) > 0:
            final_salience = self.salience_model.salience_history[-1]
            salience_trauma_markers = final_salience.get('trauma_markers', {})
            salience_morphogenetic_guidance = final_salience.get('morphogenetic_guidance', None)

        # Compose nexuses first (needed for both reconstruction and transduction)
        nexuses = []
        if self.nexus_composer:
            nexuses = self.nexus_composer.compose_nexuses(semantic_fields)
            print(f"   ✓ {len(nexuses)} nexuses formed")

        # 🆕 RECONSTRUCTION PIPELINE (November 12, 2025) - Phase 2 Integration
        # Use reconstruction pipeline if available (wires all components with SELF governance)
        emission_text = None
        emission_confidence = 0.0
        emission_path = 'none'
        emission_nexus_count = len(nexuses)

        # 🆕 PHASE C2: Set organ_results for lure-informed phrase selection (November 13, 2025)
        if self.emission_generator and hasattr(self.emission_generator, 'set_organ_results'):
            self.emission_generator.set_organ_results(organ_results)

        if self.reconstruction_pipeline:
            print(f"\n   🌀 Using Reconstruction Pipeline (Authentic Voice)")

            # Extract NDAM urgency and EO polyvagal state from final cycle
            ndam_result_final = organ_results.get('NDAM')
            eo_result_final = organ_results.get('EO')

            ndam_urgency_final = getattr(ndam_result_final, 'mean_urgency', 0.0) if ndam_result_final else 0.0
            eo_polyvagal_final = getattr(eo_result_final, 'polyvagal_state', 'mixed_state') if eo_result_final else 'mixed_state'

            # Build felt state for reconstruction
            felt_state_for_reconstruction = {
                'organ_coherences': organ_coherences,
                'semantic_fields': semantic_fields,
                'v0_energy': mean_energy,
                'satisfaction': mean_satisfaction,
                'convergence_cycles': cycle,
                'transduction_state': transduction_trajectory[0] if transduction_trajectory else None,
                'eo_polyvagal_state': eo_polyvagal_final,
                'ndam_urgency': ndam_urgency_final,
                'kairos_detected': kairos_detected,
                'salience_trauma_markers': salience_trauma_markers,  # 🆕 SALIENCE
                # 🌀 PHASE LLM1: Felt-guided LLM parameters (Nov 13, 2025)
                'user_input': text,
                'organ_results': organ_results,
                'memory_context': None  # TODO: Add memory context from hybrid LLM
            }

            # Call reconstruction pipeline
            reconstruction_result = self.reconstruction_pipeline.reconstruct_emission(
                felt_state=felt_state_for_reconstruction,
                context=context
            )

            # Extract results
            emission_text = reconstruction_result['emission_text']
            emission_confidence = reconstruction_result['confidence']
            emission_path = reconstruction_result['strategy']
            emission_nexus_count = reconstruction_result['nexuses_used']

            print(f"   ✅ Reconstruction complete:")
            print(f"      Strategy: {emission_path}")
            print(f"      Confidence: {emission_confidence:.3f}")
            print(f"      Zone: {reconstruction_result['zone']} (Zone {reconstruction_result['zone_id']})")
            print(f"      Safe: {reconstruction_result['safe']}")

        else:
            # FALLBACK: Direct emission generation (backward compatible)
            print(f"\n   ⚠️  Using direct emission (reconstruction pipeline unavailable)")

            # 🆕 PHASE 2: Generate emission with V0 guidance and Kairos awareness
            # 🆕 SALIENCE: Pass trauma markers for intensity modulation
            if self.emission_generator and nexuses:
                    num_emissions = min(3, max(1, len(nexuses)))

                    # Use V0-guided emission generator with trauma-aware modulation
                    emitted_phrases, emission_path = self.emission_generator.generate_v0_guided_emissions(
                        nexuses=nexuses,
                        v0_energy=mean_energy,
                        kairos_detected=kairos_detected,
                        num_emissions=num_emissions,
                        prefer_variety=True,
                        trauma_markers=salience_trauma_markers  # 🆕 SALIENCE
                    )

                    if emitted_phrases:
                        emission_text = ' '.join([phrase.text for phrase in emitted_phrases])
                        emission_confidence = sum([phrase.confidence for phrase in emitted_phrases]) / len(emitted_phrases)

        # Build felt states
        mean_energy = np.mean([occ.v0_energy for occ in occasions])
        mean_satisfaction = np.mean([occ.satisfaction for occ in occasions])

        # Extract organ coherences from final cycle
        organ_coherences = {}
        for organ_name, result in organ_results.items():
            coherence = getattr(result, 'coherence', 0.0)
            organ_coherences[organ_name] = coherence

        # 🔧 FIX: Extract BOND self_distance and polyvagal-modulated version from final cycle
        bond_result_final = organ_results.get('BOND')
        bond_self_distance_base_final = getattr(bond_result_final, 'mean_self_distance', 0.5) if bond_result_final else 0.5

        eo_result_final = organ_results.get('EO')
        eo_polyvagal_final = getattr(eo_result_final, 'polyvagal_state', 'mixed_state') if eo_result_final else 'mixed_state'

        # Apply polyvagal modulation (same as in cycle loop)
        polyvagal_modifiers = {
            "ventral_vagal": -0.10,
            "sympathetic": +0.15,
            "dorsal_vagal": +0.30,
            "mixed_state": 0.0
        }
        polyvagal_modifier_final = polyvagal_modifiers.get(eo_polyvagal_final, 0.0)
        bond_self_distance_modulated_final = max(0.0, min(1.0, bond_self_distance_base_final + polyvagal_modifier_final))

        # 🆕 TRANSDUCTION: Create transduction state POST-convergence (November 12, 2025)
        if self.transduction_evaluator and TRANSDUCTION_AVAILABLE and nexuses:
            # Take dominant nexus (highest coherence)
            dominant_nexus = max(nexuses, key=lambda n: n.coherence)

            # Extract final organ insights
            organ_insights = {
                'bond_self_distance': bond_self_distance_modulated_final,
                'ndam_urgency_level': getattr(organ_results.get('NDAM'), 'mean_urgency', 0.0),  # 🚨 FIX
                'eo_polyvagal_state': eo_polyvagal_final,
                'rnx_temporal_coherence': getattr(organ_results.get('RNX'), 'coherence', 0.5),
                'empathy_coherence': getattr(organ_results.get('EMPATHY'), 'coherence', 0.5)
            }

            # Compute rhythm coherence
            rhythm_coherence = compute_rhythm_coherence(
                organ_results,
                rnx_temporal_coherence=organ_insights['rnx_temporal_coherence']
            )

            # Compute mutual satisfaction
            mutual_satisfaction = compute_mutual_satisfaction(
                organ_results,
                nexus_coherence=dominant_nexus.coherence,
                rhythm_coherence=rhythm_coherence
            )

            # Check relational field availability
            relational_field_available = check_relational_field_available(
                bond_self_distance_modulated_final,
                eo_polyvagal_final,
                organ_insights['empathy_coherence']
            )

            # Compute transductive vocabulary
            transductive_vocab = compute_transductive_vocabulary(
                salience_metrics=salience_trauma_markers,
                organ_activations=organ_coherences,
                satisfaction=mean_satisfaction,
                v0_energy=mean_energy
            )

            # Classify nexus type from V0 energy + organ insights
            nexus_type, nexus_category = classify_nexus_type_from_v0(
                v0_energy=mean_energy,
                satisfaction=mean_satisfaction,
                bond_self_distance=bond_self_distance_modulated_final,
                ndam_urgency_level=organ_insights['ndam_urgency_level'],
                eo_polyvagal_state=eo_polyvagal_final
            )

            # Create transduction state
            transduction_state = NexusTransductionState(
                current_type=nexus_type,
                current_category=nexus_category,
                cycle_num=cycle,
                v0_energy=mean_energy,
                satisfaction=mean_satisfaction,
                mutual_satisfaction=mutual_satisfaction,
                rhythm_coherence=rhythm_coherence,
                field_resonance=dominant_nexus.coherence,
                signal_inflation=transductive_vocab['signal_inflation'],
                salience_drift=transductive_vocab['salience_drift'],
                prehensive_overload=transductive_vocab['prehensive_overload'],
                coherence_leakage=transductive_vocab['coherence_leakage'],
                relational_field_available=relational_field_available,
                protective_field_active=(bond_self_distance_modulated_final > 0.4),
                bond_self_distance=bond_self_distance_modulated_final,
                ndam_urgency_level=organ_insights['ndam_urgency_level'],
                eo_polyvagal_state=eo_polyvagal_final,
                rnx_temporal_coherence=organ_insights['rnx_temporal_coherence']
            )

            # Evaluate transduction pathways
            transduction_state.available_paths = self.transduction_evaluator.evaluate_pathways(
                current_nexus_type=nexus_type,
                v0_energy=mean_energy,
                satisfaction=mean_satisfaction,
                mutual_satisfaction=mutual_satisfaction,
                rhythm_coherence=rhythm_coherence,
                relational_field_available=relational_field_available,
                organ_insights=organ_insights
            )

            # Select highest probability path
            transduction_state.select_highest_probability_path()

            # Store in trajectory (single final state for now)
            transduction_trajectory.append(transduction_state)

        felt_states = {
            'text_occasions': [occ.get_summary() for occ in occasions],
            'organ_coherences': organ_coherences,
            'satisfaction_final': mean_satisfaction,
            'v0_energy': {
                'initial_energy': 1.0,
                'final_energy': mean_energy,
                'energy_descent_rate': 1.0 - mean_energy
            },
            'v0_energy_initial': 1.0,  # Flatten for maturity test
            'v0_energy_final': mean_energy,
            'convergence_cycles': cycle,
            'convergence_reason': convergence_reason,
            'kairos_cycle_index': kairos_cycle,
            'kairos_detected': kairos_detected,
            'phase5_family_id': None,
            'bond_self_distance_base': bond_self_distance_base_final,  # 🆕 Base (keyword-based)
            'bond_self_distance': bond_self_distance_modulated_final,   # 🆕 Modulated (with polyvagal)
            'BOND_self_distance': bond_self_distance_modulated_final,  # Test-compatible key
            'NDAM_urgency_level': getattr(organ_results.get('NDAM'), 'mean_urgency', 0.0),  # 🚨 FIX: Test-compatible key
            'urgency': getattr(organ_results.get('NDAM'), 'mean_urgency', 0.0),  # 🚨 CRITICAL: Training script uses this key
            'EO_polyvagal_state': getattr(organ_results.get('EO'), 'polyvagal_state', 'mixed_state'),  # Test-compatible key
            'rnx_temporal_state': getattr(organ_results.get('RNX'), 'temporal_state', 'concrescent'),
            'eo_polyvagal_state': getattr(organ_results.get('EO'), 'polyvagal_state', 'mixed_state'),
            'card_recommended_scale': getattr(organ_results.get('CARD'), 'recommended_scale', 'moderate'),
            # 🆕 PHASE 1.6: Organ activations for transductive aggregation (Nov 14, 2025)
            'organ_activations': {
                organ_name: getattr(result, 'mean_activation', getattr(result, 'coherence', 0.0))
                for organ_name, result in organ_results.items()
            },
            # 🆕 LURE ATTRACTOR FIELDS: Whiteheadian process tracking (November 13, 2025)
            'eo_lure': getattr(organ_results.get('EO'), 'lure', 0.0),
            'eo_lure_field': getattr(organ_results.get('EO'), 'lure_field', {}),
            'ndam_lure': getattr(organ_results.get('NDAM'), 'lure', 0.0),
            'ndam_salience_field': getattr(organ_results.get('NDAM'), 'salience_field', {}),
            'rnx_lure': getattr(organ_results.get('RNX'), 'lure', 0.0),
            'rnx_temporal_field': getattr(organ_results.get('RNX'), 'temporal_field', {}),
            # 🆕 CONVERSATIONAL LURE FIELDS: (Phase B, November 13, 2025)
            'empathy_lure': getattr(organ_results.get('EMPATHY'), 'lure', 0.0),
            'empathy_emotional_lure_field': getattr(organ_results.get('EMPATHY'), 'emotional_lure_field', {}),
            'wisdom_lure': getattr(organ_results.get('WISDOM'), 'lure', 0.0),
            'wisdom_pattern_lure_field': getattr(organ_results.get('WISDOM'), 'pattern_lure_field', {}),
            'authenticity_lure': getattr(organ_results.get('AUTHENTICITY'), 'lure', 0.0),
            'authenticity_vulnerability_lure_field': getattr(organ_results.get('AUTHENTICITY'), 'vulnerability_lure_field', {}),
            'lure_contribution_to_v0': (
                getattr(organ_results.get('EO'), 'lure', 0.0) * 0.20 +
                getattr(organ_results.get('NDAM'), 'lure', 0.0) * 0.20 +
                getattr(organ_results.get('RNX'), 'lure', 0.0) * 0.15 +
                getattr(organ_results.get('EMPATHY'), 'lure', 0.0) * 0.20 +
                getattr(organ_results.get('WISDOM'), 'lure', 0.0) * 0.15 +
                getattr(organ_results.get('AUTHENTICITY'), 'lure', 0.0) * 0.10
            ),  # Total lure pull in V0 descent (6 organs)
            # 🆕 PHASE C2: Composite lure signature for emission (November 13, 2025)
            'lure_signature_used_in_emission': (
                self.emission_generator.lure_selector.get_lure_signature_for_tsk(organ_results)
                if self.emission_generator and hasattr(self.emission_generator, 'lure_selector') else None
            ),
            'mean_coherence': np.mean(list(organ_coherences.values())),
            'emission_text': emission_text,
            'emission_confidence': emission_confidence,
            'emission_path': emission_path,
            'emission_nexus_count': emission_nexus_count,
            # 🆕 SALIENCE: Trauma-aware monitoring and morphogenetic pressure
            'salience_trauma_markers': salience_trauma_markers,
            'salience_morphogenetic_guidance': salience_morphogenetic_guidance,
            # 🆕 TRANSDUCTION: Nexus evolution trajectory (November 12, 2025)
            'transduction_trajectory': [state.to_dict() for state in transduction_trajectory] if transduction_trajectory else [],
            'transduction_enabled': bool(self.transduction_evaluator and TRANSDUCTION_AVAILABLE),
            # 🆕 PHASE 1.6: Transduction data for aggregation (Nov 14, 2025)
            'transduction_data': {
                'nexus_types': [state.current_type for state in transduction_trajectory] if transduction_trajectory else [],
                'primary_pathway': transduction_trajectory[-1].transition_mechanism if transduction_trajectory and transduction_trajectory[-1].transition_mechanism else None,
                'healing_score': 0.0,  # TODO: Extract from trajectory analyzer when available
                'nexus_count': len(nexuses) if nexuses else 0
            } if transduction_trajectory else {}
        }

        # 🔧 Add individual organ coherence fields for maturity test compatibility
        for organ_name, coherence_value in organ_coherences.items():
            felt_states[f'{organ_name}_coherence'] = coherence_value

        # Build TSK record
        tsk_record = {}
        if enable_tsk_recording:
            tsk_record_id = f"tsk_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            tsk_record = {
                'record_id': tsk_record_id,
                'timestamp': datetime.now().isoformat(),
                'conversation_id': context.get('conversation_id', 'unknown'),
                'grid_type': context.get('training_phase', 'unknown').upper(),
                'felt_states': felt_states,
                'context': context
            }

            # 🛡️ Phase 1.5H: Add heckling data to TSK (Nov 14, 2025)
            if heckling_assessment:
                tsk_record['heckling_assessment'] = {
                    'is_genuine_crisis': heckling_assessment.is_genuine_crisis,
                    'crisis_indicators': heckling_assessment.crisis_indicators,
                    'is_heckling': heckling_assessment.is_heckling,
                    'heckling_score': heckling_assessment.heckling_score,
                    'intent': heckling_assessment.intent.value,
                    'safe_for_banter': heckling_assessment.safe_for_banter,
                    'recommended_zone': heckling_assessment.recommended_zone,
                    'response_strategy': heckling_assessment.response_strategy,
                    'provocation_type': heckling_assessment.provocation_type,
                    'ndam_urgency': heckling_assessment.ndam_urgency,
                    'relational_safety': heckling_assessment.relational_safety,
                    'polyvagal_state': heckling_assessment.polyvagal_state
                }
                felt_states['heckling_assessment'] = tsk_record['heckling_assessment']

            # Add TSK record ID to felt_states for maturity test
            felt_states['tsk_record_id'] = tsk_record_id

        print(f"\n✅ Phase 2 complete: {cycle} cycles, {emission_nexus_count} nexuses, confidence={emission_confidence:.2f}\n")

        # 🆕 PERSONA LAYER: Modulate emission with companion personality (November 12, 2025)
        if self.persona_layer and emission_text:
            try:
                # Get user profile
                user_id = context.get('user_id', None)
                user_profile = self.user_profile_manager.get_or_create_profile(user_id) if self.user_profile_manager else None

                # Get SELF Matrix zone from BOND self-distance
                zone = 1  # Default: Zone 1 (SELF)
                if bond_self_distance_modulated_final > 0.7:
                    zone = 5  # Collapse/shutdown
                elif bond_self_distance_modulated_final > 0.5:
                    zone = 4  # Protective
                elif bond_self_distance_modulated_final > 0.35:
                    zone = 3  # Manager
                elif bond_self_distance_modulated_final > 0.2:
                    zone = 2  # Firefighter

                # Build template context from organ felt states
                template_context = TemplateContext(
                    zone=zone,
                    ndam_urgency=getattr(organ_results.get('NDAM'), 'mean_urgency', 0.0),  # 🚨 FIX
                    polyvagal_state=getattr(organ_results.get('EO'), 'polyvagal_state', 'mixed_state'),
                    confidence=emission_confidence,
                    v0_energy=mean_energy,
                    kairos_detected=kairos_detected,
                    organ_coherences=organ_coherences,
                    active_meta_atoms=[],  # TODO: Extract from meta-atom activator
                    transduction_pathway=None,  # TODO: Extract from transduction state
                    user_input=text,
                    response_length=user_profile.response_length_preference if user_profile else "moderate",
                    humor_tolerance=user_profile.humor_tolerance if user_profile else 0.5,
                    small_talk_openness=user_profile.small_talk_openness if user_profile else 0.5,
                    llm_usage_consent=user_profile.llm_usage_consent if user_profile else False
                )

                # Modulate emission
                modulation_result = self.persona_layer.modulate_emission(
                    base_emission=emission_text,
                    context=template_context,
                    user_profile=user_profile.__dict__ if user_profile else None,
                    conversation_history=None  # TODO: Fetch from user_profile_manager
                )

                # Update emission_text with modulated version
                original_emission = emission_text
                # PersonaLayer returns 'emission', not 'modulated_emission'
                emission_text = modulation_result.get('modulated_emission') or modulation_result.get('emission', emission_text)
                felt_states['emission_text'] = emission_text

                # Store persona layer metadata
                felt_states['persona_layer_applied'] = True
                felt_states['persona_templates_used'] = modulation_result.get('templates_used', [])
                felt_states['persona_query_type'] = modulation_result.get('query_type')
                felt_states['persona_llm_queried'] = modulation_result.get('llm_queried', False)

            except Exception as e:
                import traceback
                print(f"   ⚠️  Persona layer modulation failed: {e}")
                traceback.print_exc()
                # Continue with unmodulated emission
                felt_states['persona_layer_applied'] = False

        # 🆕 DAE 3.0: Update family V0 target (Fractal Level 4) - November 12, 2025
        if self.family_v0_learner and self.phase5_learning:
            try:
                # Get family assignment from Phase 5
                family_id = self.phase5_learning.get_current_family_id()
                if family_id:
                    # Compute mean R-matrix coupling for gradient-based organ weights
                    mean_r_coupling = 0.0
                    if self.organ_coupling_learner:
                        # Get mean coupling strength from R-matrix (excluding diagonal)
                        synergy_report = self.organ_coupling_learner.get_synergy_report()
                        mean_r_coupling = synergy_report.get('mean_coupling', 0.0)

                    self.family_v0_learner.update_family_v0(
                        family_id=family_id,
                        v0_final=mean_energy,
                        satisfaction=mean_satisfaction,
                        convergence_cycles=cycle,
                        organ_coherences=organ_coherences,
                        r_matrix_coupling=mean_r_coupling,  # For gradient-based weights
                        verbose=False  # Set to True to see V0 target + gradient updates
                    )
                    self.family_v0_learner.save()
            except Exception as e:
                pass  # Silently continue if family learning fails

        # 🆕 DAE 3.0: Save learned R-matrix (Fractal Level 3) - November 12, 2025
        if self.organ_coupling_learner:
            self.organ_coupling_learner.save()

        # 🌀 DAE 3.0 LEGACY INTEGRATION: Transformation-based learning (November 15, 2025)
        # Learn from INPUT→OUTPUT transformation, not single state (DAE 3.0 proven approach)
        if self.phase5_learning and self.phase5_learning.enable_learning:
            try:
                # Build FINAL felt-state from processed results
                final_felt_state = {
                    'v0_initial': 1.0,  # From initial state
                    'v0_final': mean_energy,  # Final V0 energy after convergence
                    'convergence_cycles': cycle,  # Number of cycles to convergence
                    'organ_coherences': {
                        organ_name: organ_coherences.get(organ_name, 0.5)
                        for organ_name in ['LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY',
                                          'PRESENCE', 'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD']
                    },
                    'polyvagal_state': getattr(organ_results.get('EO'), 'polyvagal_state', 'ventral'),
                    'zone': felt_states.get('bond_zone', 1),
                    'satisfaction_final': mean_satisfaction,
                    'urgency': getattr(organ_results.get('NDAM'), 'mean_urgency', 0.0),  # 🚨 CRITICAL FIX
                    'emission_path': emission_path,
                    'kairos_detected': kairos_detected,
                    'nexus_count': len(nexuses)
                }

                # Convert transduction_trajectory objects to dicts for Phase 5
                transduction_trajectory_dicts = []
                if 'transduction_trajectory' in dir() and transduction_trajectory:
                    for state in transduction_trajectory:
                        if hasattr(state, '__dict__'):
                            state_dict = {
                                'current_type': getattr(state, 'current_type', 'Relational'),
                                'current_category': getattr(state, 'current_category', 'PSYCHE'),
                                'domain': getattr(state, 'get_nexus_domain', lambda: 'PSYCHE')(),
                                'cycle_num': getattr(state, 'cycle_num', 1),
                                'v0_energy': getattr(state, 'v0_energy', 0.5),
                                'satisfaction': getattr(state, 'satisfaction', 0.5),
                                'mutual_satisfaction': getattr(state, 'mutual_satisfaction', 0.5),
                                'rhythm_coherence': getattr(state, 'rhythm_coherence', 0.5),
                                'field_resonance': getattr(state, 'field_resonance', 0.5),
                                'signal_inflation': getattr(state, 'signal_inflation', 0.0),
                                'salience_drift': getattr(state, 'salience_drift', 0.0),
                                'prehensive_overload': getattr(state, 'prehensive_overload', 0.0),
                                'coherence_leakage': getattr(state, 'coherence_leakage', 0.0),
                                'next_type': getattr(state, 'next_type', None),
                                'transition_mechanism': getattr(state, 'transition_mechanism', 'maintain'),
                                'transition_probability': getattr(state, 'transition_probability', 0.0),
                                'bond_self_distance': getattr(state, 'bond_self_distance', 0.5),
                                'ndam_urgency_level': getattr(state, 'ndam_urgency_level', 0.0),
                                'eo_polyvagal_state': getattr(state, 'eo_polyvagal_state', 'mixed'),
                                'rnx_temporal_coherence': getattr(state, 'rnx_temporal_coherence', 0.5),
                            }
                            transduction_trajectory_dicts.append(state_dict)

                # Compute constraint deltas (initial vs final)
                constraint_deltas = {}
                if transduction_trajectory_dicts:
                    first_state = transduction_trajectory_dicts[0]
                    last_state = transduction_trajectory_dicts[-1]
                    constraint_deltas = {
                        'bond_self_distance': last_state['bond_self_distance'] - first_state['bond_self_distance'],
                        'ndam_urgency': last_state['ndam_urgency_level'] - first_state['ndam_urgency_level'],
                        'sans_coherence': last_state['rhythm_coherence'] - first_state['rhythm_coherence'],
                        'eo_temporal': last_state['rnx_temporal_coherence'] - first_state['rnx_temporal_coherence']
                    }

                # Call transformation-based learning (DAE 3.0 approach with 57D RNX/TSK)
                learning_result = self.phase5_learning.learn_from_conversation_transformation(
                    initial_felt_state=initial_felt_state,
                    final_felt_state=final_felt_state,
                    emission_text=emission_text if emission_text else '',
                    user_message=text,
                    conversation_id=context.get('conversation_id', 'unknown') if context else 'unknown',
                    transduction_trajectory=transduction_trajectory_dicts if transduction_trajectory_dicts else None,
                    constraint_deltas=constraint_deltas if constraint_deltas else None
                )

                if learning_result:
                    phase5_family_id = learning_result.get('family_id')

                    # Log family assignment for visibility
                    if phase5_family_id:
                        family_sim = learning_result.get('similarity', 0.0)
                        is_new = learning_result.get('is_new_family', False)
                        sat_improvement = learning_result.get('satisfaction_improvement', 0.0)
                        action = "CREATED" if is_new else "JOINED"
                        print(f"   🌀 Phase 5: {action} {phase5_family_id} (sim: {family_sim:.3f}, Δsat: {sat_improvement:+.3f})")

                        # Store in felt_states for return value
                        felt_states['phase5_family_id'] = phase5_family_id
                        felt_states['phase5_similarity'] = family_sim
                        felt_states['phase5_is_new'] = is_new
            except Exception as e:
                print(f"   ⚠️  Phase 5 learning failed: {e}")
                import traceback
                traceback.print_exc()

        # 🌀 POST-EMISSION: Create and store TSK (Transductive Summary Kernel - November 16, 2025)
        # This enables transformation-based epoch learning with 57D signatures
        # NOTE: Use "is not None" because TSKRecorder has __len__ method that returns 0 when empty
        if self.tsk_recorder is not None and TSK_RECORDER_AVAILABLE:
            try:
                print(f"   🔄 Creating TSK...")
                # Create initial state (default before processing)
                tsk_initial_state = self.tsk_recorder.create_initial_state()

                # Build final felt states from processing results
                # 🚨 CRITICAL FIX (Nov 16): Use ACTUAL organ result keys, not generic defaults!
                # Compute zone from BOND self-distance (matches SELF Matrix zones)
                bond_self_dist = felt_states.get('bond_self_distance', felt_states.get('BOND_self_distance', 0.5))
                if bond_self_dist > 0.8:
                    computed_zone = 5  # Collapse/shutdown
                elif bond_self_dist > 0.6:
                    computed_zone = 4  # Protective
                elif bond_self_dist > 0.4:
                    computed_zone = 3  # Manager
                elif bond_self_dist > 0.2:
                    computed_zone = 2  # Firefighter
                else:
                    computed_zone = 1  # SELF (connected)

                tsk_final_states = {
                    'v0_energy': felt_states.get('v0_energy_final', 0.5),
                    'organ_coherences': felt_states.get('organ_coherences', {}),
                    # Use ACTUAL organ detection results - keys must match TSK recorder expectations!
                    'eo_polyvagal_state': felt_states.get('eo_polyvagal_state', felt_states.get('EO_polyvagal_state', 'ventral_vagal')),
                    'zone': computed_zone,  # Compute from BOND self-distance
                    'NDAM_urgency_level': felt_states.get('NDAM_urgency_level', felt_states.get('ndam_urgency_level', 0.0)),
                    'satisfaction': felt_states.get('satisfaction_final', 0.5),
                    'emission_path': emission_path,
                    'confidence': emission_confidence,
                    'nexus_type': felt_states.get('nexus_type', 'Relational'),
                    'transduction_enabled': felt_states.get('transduction_enabled', False),
                    'bond_constraint': felt_states.get('BOND_self_distance', felt_states.get('bond_self_distance', 0.0)),
                    'ndam_urgency': felt_states.get('urgency', felt_states.get('NDAM_urgency_level', 0.0)),  # 🚨 FIX: Try 'urgency' first
                    'sans_coherence': felt_states.get('SANS_coherence', 0.0),
                    'eo_polyvagal': felt_states.get('EO_coherence', 0.5),
                }

                # Get transduction trajectory from felt_states (already converted to dicts)
                tsk_transduction_trajectory = felt_states.get('transduction_trajectory', [])

                # Create TSK from INITIAL → FINAL transformation
                conversation_id = context.get('conversation_id', 'unknown') if context else 'unknown'
                tsk = self.tsk_recorder.create_tsk_from_processing(
                    conversation_id=conversation_id,
                    user_input=text,
                    initial_state=tsk_initial_state,
                    final_felt_states=tsk_final_states,
                    transduction_trajectory=tsk_transduction_trajectory,
                    response_text=emission_text if emission_text else ''
                )

                # Store TSK in result for external consumption (e.g., TransductiveEpochCoordinator)
                felt_states['tsk'] = tsk
                felt_states['tsk_transformation_signature'] = tsk.transformation_signature

                # Optionally store persistently if epoch_id provided in context
                if context and context.get('tsk_recording', False):
                    epoch_id = context.get('epoch_id', None)
                    self.tsk_recorder.store_tsk(tsk, epoch_id=epoch_id)

            except Exception as e:
                print(f"   ⚠️  TSK recording failed: {e}")
                import traceback
                traceback.print_exc()

        # 📊 Phase 1.6: Record occasion for Transductive Self-Governance (Nov 14, 2025)
        # DAE learns from PATTERNS across users, not from individuals
        if self.transductive_monitor and tsk_record:
            try:
                # Get user hash (for counting unique users only, discarded after aggregation)
                user_id = context.get('user_id', None)
                user_hash = hashlib.sha256(str(user_id).encode()).hexdigest() if user_id else None

                # Record occasion (buffered until k≥10 for k-anonymity)
                self.transductive_monitor.record_occasion(tsk_record, user_hash)
            except Exception as e:
                pass  # Silently continue if transductive monitoring fails

        # 🌀 LLM BRIDGE: Store current emission for next-turn feedback - November 18, 2025 (Phase 1)
        if self.feedback_handler and emission_text:
            session_id = context.get('conversation_id', 'default_session')

            # Store emission data for feedback assessment on next turn
            self.last_emission_data[session_id] = {
                'emission': emission_text,
                'metadata': {
                    'emission_confidence': emission_confidence,
                    'emission_path': emission_path,
                    'active_organs': list(organ_results.keys()) if organ_results else [],
                    'felt_state': {
                        'polyvagal_state': felt_states.get('polyvagal_state'),
                        'urgency': felt_states.get('satisfaction_final'),
                        'zone': felt_states.get('zone_id')
                    },
                    'nexus_signature': felt_states.get('nexus_signature'),
                    'turn': context.get('turn_number', 0)
                }
            }

        # 🌀 LLM BRIDGE: Add current turn to history - November 18, 2025 (Phase 2)
        if self.turn_history and emission_text:
            session_id = context.get('conversation_id', 'default_session')

            try:
                self.turn_history.add_turn(
                    session_id=session_id,
                    user_input=text,
                    organism_emission=emission_text,
                    emission_metadata={
                        'emission_confidence': emission_confidence,
                        'emission_path': emission_path,
                        'polyvagal_state': felt_states.get('polyvagal_state'),
                        'urgency': felt_states.get('satisfaction_final'),
                        'zone': felt_states.get('zone_id'),
                        'satisfaction': felt_states.get('satisfaction_final')
                    }
                )
            except Exception as e:
                print(f"⚠️  Turn history recording failed: {e}")

        return {
            'mode': 'processing_complete',
            'felt_states': felt_states,
            'tsk_record': tsk_record,
            'organ_results': organ_results,
            # Emission data at top level for backward compatibility
            'emission_text': emission_text,
            'emission_confidence': emission_confidence,
            'emission_path': emission_path,
            'emission_nexus_count': emission_nexus_count,
            # 🌀 Wave training integration (Nov 15, 2025): Return occasions for metric tracking
            'occasions': occasions,  # V0 convergence occasions with wave training metadata
            'nexuses': nexuses,  # Formed nexuses
            'strategy': emission_path  # Emission strategy for backward compat
        }

    def _create_conversational_occasions(self, text: str) -> List[ConversationalOccasion]:
        """Create ConversationalOccasion objects for each token."""
        words = text.split()
        occasions = []

        for position, word in enumerate(words):
            embedding = np.zeros(384)  # Placeholder embedding
            occasion = ConversationalOccasion(
                datum=word,
                position=position,
                embedding=embedding
            )
            occasions.append(occasion)

        return occasions

    def _process_organs_with_v0(
        self,
        occasions: List[ConversationalOccasion],
        cycle: int,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Process all 11 organs for current cycle."""
        # Convert ConversationalOccasions to TextOccasions for organ processing
        text_occasions = []
        for occ in occasions:
            text_occ = TextOccasion(
                chunk_id=f"doc_0_para_0_sent_0_chunk_{occ.position}",
                position=occ.position,
                text=occ.datum,
                embedding=occ.embedding
            )
            text_occasions.append(text_occ)

        # 🌀 Nov 14, 2025: Entity-aware enrichment for Phase 2 (multi-cycle)
        if context and 'stored_entities' in context:
            stored_entities = context['stored_entities']

            for text_occ in text_occasions:
                # Add stored entities to occasion (felt context)
                text_occ.known_entities = stored_entities

                # Detect entity references in THIS occasion's text
                entity_refs = self._detect_entity_references(text_occ.text, stored_entities)
                text_occ.entity_references = entity_refs['references']
                text_occ.entity_match_confidence = entity_refs['confidences']

        # 🌀 Nov 14, 2025: Build entity context for all organs (Phase 2.1)
        # 🌀 Nov 15, 2025: Extract user_id for NEXUS organ
        # ✅ FIX (Nov 16): Use correct context keys for Phase 2
        user_id = context.get('user_id', 'default_user') if context else 'default_user'

        entity_context = {
            'entity_prehension': context.get('entity_prehension', {}) if context else {},
            'organ_context_enrichment': context.get('organ_context_enrichment', {}) if context else {},
            'temporal': context.get('temporal', {}) if context else {},
            'username': context.get('username') if context else None
        }

        # 🔍 DEBUG (Nov 16): Log what entity_context contains for NEXUS
        entity_prehension = entity_context.get('entity_prehension', {})
        if cycle == 1:  # Only log first cycle to avoid spam
            print(f"   🔍 DEBUG Phase2 Cycle {cycle}: entity_prehension keys = {list(entity_prehension.keys())}")
            if 'entity_memory_available' in entity_prehension:
                print(f"   🔍 DEBUG Phase2 Cycle {cycle}: entity_memory_available = {entity_prehension['entity_memory_available']}")
                print(f"   🔍 DEBUG Phase2 Cycle {cycle}: mentioned_entities count = {len(entity_prehension.get('mentioned_entities', []))}")

        # Process through all 12 organs (5 conversational + 6 trauma + 1 memory)
        # 🌀 Nov 14, 2025: Pass entity_context to all organs
        # 🌀 Nov 15, 2025: Added NEXUS (12th organ) for Neo4j memory prehension
        organ_results = {
            'LISTENING': self.listening.process_text_occasions(text_occasions, cycle=cycle, context=entity_context),
            'EMPATHY': self.empathy.process_text_occasions(text_occasions, cycle=cycle, context=entity_context),
            'WISDOM': self.wisdom.process_text_occasions(text_occasions, cycle=cycle, context=entity_context),
            'AUTHENTICITY': self.authenticity.process_text_occasions(text_occasions, cycle=cycle, context=entity_context),
            'PRESENCE': self.presence.process_text_occasions(text_occasions, cycle=cycle, context=entity_context),
            'BOND': self.bond.process_text_occasions(text_occasions, cycle=cycle, context=entity_context),
            'SANS': self.sans.process_text_occasions(text_occasions, cycle=cycle, context=entity_context),
            'NDAM': self.ndam.process_text_occasions(text_occasions, cycle=cycle, context=entity_context),
            'RNX': self.rnx.process_text_occasions(text_occasions, cycle=cycle, context=entity_context),
            'EO': self.eo.process_text_occasions(text_occasions, cycle=cycle, context=entity_context),
            # 🌀 12th organ: NEXUS (Neo4j entity memory - Nov 15, 2025 - Quick Win #9)
            'NEXUS': self.nexus.process_text_occasions(text_occasions, cycle=cycle, context={**entity_context, 'user_id': user_id}),
        }

        # CARD needs EXTENDED context (entity data + organ signals for response scaling)
        eo_result = organ_results.get('EO')
        ndam_result = organ_results.get('NDAM')
        bond_result = organ_results.get('BOND')
        rnx_result = organ_results.get('RNX')

        card_context = {
            # Entity context (Nov 14, 2025) - ✅ FIX (Nov 16): Use correct keys
            'entity_prehension': entity_context.get('entity_prehension', {}),
            'organ_context_enrichment': entity_context.get('organ_context_enrichment', {}),
            'temporal': entity_context.get('temporal', {}),
            'username': entity_context.get('username'),
            # Organ signal context (existing)
            'polyvagal_state': getattr(eo_result, 'polyvagal_state', 'mixed_state') if eo_result else 'mixed_state',
            'urgency': getattr(ndam_result, 'mean_urgency', 0.5) if ndam_result else 0.5,
            'self_distance': getattr(bond_result, 'mean_self_distance', 0.5) if bond_result else 0.5,
            'temporal_state': getattr(rnx_result, 'temporal_state', 'concrescent') if rnx_result else 'concrescent'
        }

        organ_results['CARD'] = self.card.process_text_occasions(text_occasions, cycle=cycle, context=card_context)

        return organ_results

    def _build_semantic_fields_from_propositions(
        self,
        occasions: List[ConversationalOccasion]
    ) -> Dict[str, Any]:
        """Build semantic fields from mature propositions."""
        from persona_layer.semantic_field_extractor import SemanticField
        from collections import defaultdict

        # Aggregate propositions by organ
        organ_fields = defaultdict(lambda: {'atoms': {}, 'count': 0})

        for occasion in occasions:
            for prop in occasion.mature_propositions:
                for organ in prop.organ_sources:
                    organ_fields[organ]['atoms'][prop.atom] = \
                        organ_fields[organ]['atoms'].get(prop.atom, 0.0) + prop.confidence
                    organ_fields[organ]['count'] += 1

        # Normalize and create SemanticField objects
        semantic_fields = {}
        for organ, data in organ_fields.items():
            if data['count'] > 0:
                atom_activations = {
                    atom: activation / data['count']
                    for atom, activation in data['atoms'].items()
                }

                # Filter NaN/Inf
                atom_activations = {
                    atom: activation
                    for atom, activation in atom_activations.items()
                    if not (np.isnan(activation) or np.isinf(activation))
                }

                if atom_activations:
                    semantic_fields[organ] = SemanticField(
                        organ_name=organ,
                        coherence=0.5,  # Placeholder
                        lure=0.5,
                        atom_activations=atom_activations,
                        pattern_count=data['count']
                    )

        return semantic_fields


def test_organism_wrapper():
    """
    Test conversational organism wrapper with sample text.
    """
    print("\n" + "="*70)
    print("🧪 TESTING CONVERSATIONAL ORGANISM WRAPPER")
    print("="*70 + "\n")

    # Initialize wrapper
    wrapper = ConversationalOrganismWrapper()

    # Test INPUT text (organizational distress)
    input_text = "Our team is completely burned out. People are working 60-hour weeks, missing deadlines anyway, and making careless mistakes. I don't know how to help them recover."

    print("📘 Processing INPUT text:")
    print(f"   Text: \"{input_text[:80]}...\"")
    print()

    input_result = wrapper.process_text(
        text=input_text,
        context={
            'conversation_id': 'test_001_epoch1_INPUT',
            'epoch_num': 1,
            'training_phase': 'input',
            'self_distance': 0.85,  # High trauma activation (burnout)
            'polyvagal_state': 'dorsal_vagal'  # Shutdown state
        },
        enable_tsk_recording=True
    )

    felt_states = input_result['felt_states']

    print("✅ INPUT processing complete:")
    print(f"   Text occasions: {len(felt_states['text_occasions'])}")
    print(f"   Mean coherence: {felt_states['mean_coherence']:.3f}")
    print(f"   Final satisfaction: {felt_states['satisfaction_final']:.3f}")
    print(f"   V0 final energy: {felt_states['v0_energy']['final_energy']:.3f}")
    print(f"   Convergence cycles: {felt_states['convergence_cycles']}")
    print(f"   Convergence reason: {felt_states['convergence_reason']}")
    print(f"   BOND self_distance: {felt_states['bond_self_distance']:.3f}")
    print()

    print("   Organ coherences:")
    for organ, coherence in felt_states['organ_coherences'].items():
        print(f"     {organ:15s}: {coherence:.3f}")
    print()

    # Test OUTPUT text (therapeutic response)
    output_text = "Let's take a moment to ground together. I hear the exhaustion in your words. This level of depletion isn't sustainable. When a team is burning out, it's a sign the system needs adjustment, not that people need to try harder. Let's explore what boundaries might help protect your team's wellbeing and create space for recovery."

    print("📗 Processing OUTPUT text:")
    print(f"   Text: \"{output_text[:80]}...\"")
    print()

    output_result = wrapper.process_text(
        text=output_text,
        context={
            'conversation_id': 'test_001_epoch1_OUTPUT',
            'epoch_num': 1,
            'training_phase': 'output',
            'self_distance': 0.25,  # Lower trauma activation (therapeutic holding)
            'polyvagal_state': 'ventral_vagal'  # Safe/connected state
        },
        enable_tsk_recording=True
    )

    felt_states = output_result['felt_states']

    print("✅ OUTPUT processing complete:")
    print(f"   Text occasions: {len(felt_states['text_occasions'])}")
    print(f"   Mean coherence: {felt_states['mean_coherence']:.3f}")
    print(f"   Final satisfaction: {felt_states['satisfaction_final']:.3f}")
    print(f"   V0 final energy: {felt_states['v0_energy']['final_energy']:.3f}")
    print(f"   Convergence cycles: {felt_states['convergence_cycles']}")
    print(f"   Convergence reason: {felt_states['convergence_reason']}")
    print(f"   BOND self_distance: {felt_states['bond_self_distance']:.3f}")
    print()

    print("   Organ coherences:")
    for organ, coherence in felt_states['organ_coherences'].items():
        print(f"     {organ:15s}: {coherence:.3f}")
    print()

    # Compare INPUT vs OUTPUT (expected pattern for learning)
    print("🔬 INPUT→OUTPUT Comparison (Expected Learning Pattern):")
    print("="*70)

    input_felt = input_result['felt_states']
    output_felt = output_result['felt_states']

    print(f"   V0 Energy:      {input_felt['v0_energy']['final_energy']:.3f} → {output_felt['v0_energy']['final_energy']:.3f}")
    print(f"                   (OUTPUT should be lower, showing resolution)")
    print()

    print(f"   Satisfaction:   {input_felt['satisfaction_final']:.3f} → {output_felt['satisfaction_final']:.3f}")
    print(f"                   (OUTPUT should be higher, showing therapeutic success)")
    print()

    print(f"   Self-distance:  {input_felt['bond_self_distance']:.3f} → {output_felt['bond_self_distance']:.3f}")
    print(f"                   (OUTPUT should be lower, showing trauma deactivation)")
    print()

    print("   Organ shifts (INPUT → OUTPUT):")
    for organ in input_felt['organ_coherences'].keys():
        input_coh = input_felt['organ_coherences'][organ]
        output_coh = output_felt['organ_coherences'][organ]
        delta = output_coh - input_coh
        print(f"     {organ:15s}: {input_coh:.3f} → {output_coh:.3f} (Δ {delta:+.3f})")

    print()
    print("="*70)
    print("✅ Organism wrapper test complete!")
    print("="*70 + "\n")


if __name__ == '__main__':
    test_organism_wrapper()
