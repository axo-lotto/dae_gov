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

# 🌀 Import Session Turn Manager (USER:SESSION:TURN Hierarchy - November 16, 2025)
try:
    from persona_layer.session_turn_manager import SessionTurnManager
    SESSION_TURN_MANAGER_AVAILABLE = True
except ImportError as e:
    SESSION_TURN_MANAGER_AVAILABLE = False
    print(f"⚠️  Session turn manager not available: {e}")


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
                    learning_threshold=0.55,
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

        # Initialize emission generation (if available)
        if EMISSION_AVAILABLE:
            try:
                print("   Loading emission generation components...")
                self.semantic_extractor = SemanticFieldExtractor(
                    semantic_atoms_path="persona_layer/semantic_atoms.json"
                )
                self.nexus_composer = NexusIntersectionComposer(
                    r_matrix_path="persona_layer/state/active/conversational_hebbian_memory.json",
                    intersection_threshold=0.005  # 🌀 NOV 14: Lowered 0.01→0.005 for better nexus formation
                )

                # Import emission thresholds from config (Nov 13, 2025 - fixes organic emission bottleneck)
                from config import Config

                # 🌀 PHASE LLM1: Initialize felt-guided LLM generator (Nov 13, 2025)
                felt_guided_llm = None
                if Config.FELT_GUIDED_LLM_ENABLED and Config.LOCAL_LLM_ENABLED:
                    try:
                        from persona_layer.local_llm_bridge import LocalLLMBridge
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
                    hebbian_memory_path="persona_layer/state/active/conversational_hebbian_memory.json",
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
                    phase5_learning=self.phase5_learning,
                    hebbian_memory_path="persona_layer/state/active/conversational_hebbian_memory.json"
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
                from config import Config
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

        print("="*70)
        print("✅ 11-organ conversational organism initialized (Phase 2 COMPLETE!)\n")

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

        context = context or {}

        # 🕐 TEMPORAL AWARENESS: Add time/date context - November 15, 2025
        context['temporal'] = self._create_temporal_context()

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
            result = self._process_single_cycle(text, context, enable_tsk_recording)

        # 🌀 Nov 14, 2025: Open-ended entity extraction (LLM-based, not hardcoded)
        if user_id and self.superject_learner:
            try:
                # Get current user profile
                user_profile = self.superject_learner.get_or_create_profile(user_id)
                current_entities = user_profile.entities if user_profile else {}

                # Extract entities using LLM (open-ended discovery)
                new_entities = self.superject_learner.extract_entities_llm(
                    user_input=text,
                    current_entities=current_entities
                )

                # Store newly extracted entities
                if new_entities and user_profile:
                    user_profile.store_entities(new_entities)
                    self.superject_learner.save_profile(user_profile)

                    # Show extraction feedback
                    if 'memories' in new_entities:
                        num_memories = len(new_entities['memories'])
                        print(f"      📝 Extracted {num_memories} new memories")

            except Exception as e:
                print(f"      ⚠️  Entity extraction failed: {e}")

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
                        v0_energy=fs.get('v0_energy', {}).get('final_energy', 0.5),
                        v0_initial=fs.get('v0_energy', {}).get('initial_energy', 1.0),
                        v0_descent_rate=fs.get('v0_energy', {}).get('energy_descent_rate', 0.0),
                        convergence_cycles=fs.get('convergence_cycles', 1),
                        convergence_reason=fs.get('convergence_reason', 'single_pass'),
                        organ_activations=fs.get('organ_coherences', {}),
                        zone=fs.get('zone', 3),
                        polyvagal_state=fs.get('eo_polyvagal_state', 'unknown'),
                        satisfaction=fs.get('satisfaction_final', 0.5)
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
        if self.entity_organ_tracker and context.get('current_turn_entities'):
            try:
                # Extract entities from current turn (passed from dae_interactive.py)
                # Format: List[{'entity_value': 'Emma', 'entity_type': 'Person'}, ...]
                extracted_entities = context.get('current_turn_entities', [])
                organ_results = result.get('organ_results', {})

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
            except Exception as e:
                print(f"⚠️  Entity-organ tracking update failed: {e}")

        return result

    def _process_single_cycle(
        self,
        text: str,
        context: Dict[str, Any],
        enable_tsk_recording: bool
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
        user_id = context.get('user_id', 'default_user')

        entity_context = {
            'stored_entities': context.get('stored_entities', {}),
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
            # Entity context (Nov 14, 2025)
            'stored_entities': entity_context['stored_entities'],
            'username': entity_context['username'],
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

                    emitted_phrases = self.emission_generator.generate_emissions(
                        nexuses=nexuses,
                        num_emissions=num_emissions,
                        prefer_variety=True,
                        user_input=text,  # 🌀 For felt-guided LLM
                        organ_results=organ_results,  # 🌀 For felt-guided LLM
                        v0_energy=final_energy,  # 🌀 For felt-guided LLM
                        satisfaction=satisfaction_final,  # 🌀 For felt-guided LLM
                        memory_context=None,  # 🌀 TODO: Pass from dae_interactive if hybrid enabled
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
                    ndam_urgency=getattr(organ_results.get('NDAM'), 'urgency_level', 0.0) if organ_results.get('NDAM') else 0.0,
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
            'zone_id': zone_id
        }

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
                    ndam_urgency_level = getattr(ndam_result, 'urgency_level', 0.0) if ndam_result else 0.0
                    ndam_dominant_urgency = getattr(ndam_result, 'dominant_urgency', None) if ndam_result else None

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
                'ndam_urgency_level': getattr(organ_results.get('NDAM'), 'urgency_level', 0.0),
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
            'NDAM_urgency_level': getattr(organ_results.get('NDAM'), 'urgency_level', 0.0),  # Test-compatible key
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
                    ndam_urgency=getattr(organ_results.get('NDAM'), 'urgency_level', 0.0),
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
                    'urgency': getattr(organ_results.get('NDAM'), 'urgency_level', 0.0),
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
                    'ndam_urgency': felt_states.get('NDAM_urgency_level', 0.0),
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
        user_id = context.get('user_id', 'default_user') if context else 'default_user'

        entity_context = {
            'stored_entities': context.get('stored_entities', {}) if context else {},
            'username': context.get('username') if context else None
        }

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
            # Entity context (Nov 14, 2025)
            'stored_entities': entity_context['stored_entities'],
            'username': entity_context['username'],
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
