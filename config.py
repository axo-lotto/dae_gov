#!/usr/bin/env python3
"""
DAE_HYPHAE_1 Configuration
==========================

Centralized configuration for all paths, parameters, and settings.
This replaces hard-coded paths throughout the codebase.

Usage:
    from config import Config

    # Access paths
    semantic_atoms_path = Config.SEMANTIC_ATOMS_PATH

    # Access parameters
    max_cycles = Config.V0_MAX_CYCLES

Date: November 12, 2025
"""

from pathlib import Path

class Config:
    """Centralized configuration for DAE_HYPHAE_1 system."""

    # ============================================================================
    # BASE PATHS
    # ============================================================================

    PROJECT_ROOT = Path(__file__).parent

    # Core directories
    PERSONA_LAYER_DIR = PROJECT_ROOT / "persona_layer"
    ORGANS_DIR = PROJECT_ROOT / "organs" / "modular"
    KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "knowledge_base"
    TSK_DIR = PROJECT_ROOT / "TSK"
    SESSIONS_DIR = PROJECT_ROOT / "sessions"
    BUNDLE_DIR = PROJECT_ROOT / "Bundle"
    MONITORING_DIR = PROJECT_ROOT / "monitoring"

    # New organized directories
    TESTS_DIR = PROJECT_ROOT / "tests"
    TRAINING_DIR = PROJECT_ROOT / "training"
    DOCS_DIR = PROJECT_ROOT / "docs"
    SCRIPTS_DIR = PROJECT_ROOT / "scripts"
    RESULTS_DIR = PROJECT_ROOT / "results"

    # ============================================================================
    # PERSONA LAYER PATHS (Core Processing)
    # ============================================================================

    # Template libraries (Phase 1: Bootstrap)
    PERSONALITY_TEMPLATES_PATH = PERSONA_LAYER_DIR / "personality_templates.json"
    SMALL_TALK_TEMPLATES_PATH = PERSONA_LAYER_DIR / "small_talk_templates.json"
    HUMOR_TEMPLATES_PATH = PERSONA_LAYER_DIR / "humor_templates.json"
    RELATIONSHIP_TEMPLATES_PATH = PERSONA_LAYER_DIR / "relationship_templates.json"
    RESPONSE_STYLE_TEMPLATES_PATH = PERSONA_LAYER_DIR / "response_style_templates.json"
    LLM_AUGMENTATION_PROMPTS_PATH = PERSONA_LAYER_DIR / "llm_augmentation_prompts.json"

    # User profiles and conversations (Levels 8-9)
    USER_PROFILES_DIR = PERSONA_LAYER_DIR / "user_profiles"
    DEFAULT_USER_ID = "default_user"

    # Shared learning (cross-user patterns)
    TEMPLATE_USAGE_STATS_PATH = PERSONA_LAYER_DIR / "template_usage_stats.json"
    FAMILY_TEMPLATE_PREFERENCES_PATH = PERSONA_LAYER_DIR / "family_template_preferences.json"
    META_TEMPLATES_PATH = PERSONA_LAYER_DIR / "meta_templates.json"  # Phase 3

    # Semantic space
    SEMANTIC_ATOMS_PATH = PERSONA_LAYER_DIR / "semantic_atoms.json"
    SHARED_META_ATOMS_PATH = PERSONA_LAYER_DIR / "shared_meta_atoms.json"

    # Memory & learning
    HEBBIAN_MEMORY_PATH = PERSONA_LAYER_DIR / "conversational_hebbian_memory.json"
    ORGANIC_FAMILIES_PATH = PERSONA_LAYER_DIR / "organic_families.json"
    CLUSTER_DATABASE_PATH = PERSONA_LAYER_DIR / "conversational_clusters.json"

    # Emission generation
    META_ATOM_PHRASE_LIBRARY_PATH = PERSONA_LAYER_DIR / "emission_generation" / "meta_atom_phrase_library.json"
    TRANSDUCTION_MECHANISM_PHRASES_PATH = PERSONA_LAYER_DIR / "transduction_mechanism_phrases.json"

    # ============================================================================
    # KNOWLEDGE BASE PATHS (Training Data)
    # ============================================================================

    CONVERSATIONAL_TRAINING_PAIRS_PATH = KNOWLEDGE_BASE_DIR / "conversational_training_pairs.json"
    STRUCTURE_TRAINING_PAIRS_PATH = KNOWLEDGE_BASE_DIR / "structure_training_pairs.py"

    # ============================================================================
    # TSK & MONITORING PATHS (Learning Records)
    # ============================================================================

    GLOBAL_ORGANISM_STATE_PATH = TSK_DIR / "global_organism_state.json"
    CONVERSATIONAL_HEBBIAN_MEMORY_TSK_PATH = TSK_DIR / "conversational_hebbian_memory.json"
    MYCELIAL_IDENTITY_PATH = MONITORING_DIR / "mycelial_identity.json"

    # ============================================================================
    # RESULTS & OUTPUT PATHS
    # ============================================================================

    # Training results
    BASELINE_TRAINING_RESULTS_PATH = RESULTS_DIR / "epochs" / "baseline_training_results.json"
    EPOCH_RESULTS_DIR = RESULTS_DIR / "epochs"

    # Validation results
    VALIDATION_RESULTS_DIR = RESULTS_DIR / "validation"
    SYSTEM_MATURITY_REPORT_PATH = VALIDATION_RESULTS_DIR / "system_maturity_report.json"

    # Visualization
    VISUALIZATION_DIR = RESULTS_DIR / "visualization"

    # ============================================================================
    # PHASE 2: V0 CONVERGENCE PARAMETERS
    # ============================================================================

    # Multi-cycle convergence
    V0_MAX_CYCLES = 5
    V0_CONVERGENCE_THRESHOLD = 0.1
    V0_SATISFACTION_THRESHOLD = 0.9

    # Kairos detection (tuned Nov 13, 2025 - widened further for better detection)
    KAIROS_WINDOW_MIN = 0.15  # Was 0.20 - lowered to catch rapid descent through window
    KAIROS_WINDOW_MAX = 0.75  # Was 0.70 - raised to catch slower cycles

    # V0 descent formula coefficients
    V0_ALPHA = 0.40  # Satisfaction weight
    V0_BETA = 0.25   # Energy change weight
    V0_GAMMA = 0.15  # Agreement weight
    V0_DELTA = 0.10  # Resonance weight
    V0_ZETA = 0.10   # Intensity weight

    # ============================================================================
    # SALIENCE MODEL PARAMETERS (Trauma-Aware)
    # ============================================================================

    # Trauma detection thresholds
    SALIENCE_TRAUMA_INFLATION_THRESHOLD = 0.75
    SALIENCE_TRAUMA_TEMPORAL_THRESHOLD = 0.70
    SALIENCE_SAFETY_GRADIENT_LOW = 0.50

    # Morphogenetic pressure
    SALIENCE_MORPHOGENETIC_PRESSURE_THRESHOLD = 0.60

    # ============================================================================
    # META-ATOM PARAMETERS (10 Bridge Atoms)
    # ============================================================================

    META_ATOM_ACTIVATION_THRESHOLD = 0.30
    META_ATOM_COUNT = 10

    # Meta-atom categories
    META_ATOM_CATEGORIES = {
        'trauma_aware': ['trauma_aware', 'safety_restoration', 'window_of_tolerance'],
        'compassion': ['compassion_safety', 'fierce_holding', 'relational_attunement'],
        'temporal': ['temporal_grounding', 'kairos_emergence'],
        'integration': ['coherence_integration', 'somatic_wisdom']
    }

    # ============================================================================
    # EMISSION GENERATION PARAMETERS
    # ============================================================================

    # Emission path thresholds (tuned Nov 13, 2025 - final adjustment for actual ΔC values)
    EMISSION_DIRECT_THRESHOLD = 0.48  # Was 0.50 - lowered to catch ΔC~0.4997 (displays as 0.500)
    EMISSION_FUSION_THRESHOLD = 0.42  # Was 0.45 - lowered proportionally
    EMISSION_META_ATOM_DIRECT_THRESHOLD = 0.30  # Meta-atom direct threshold

    # 🆕 Regime-Based Confidence Modulation (Enhancement #1 - November 13, 2025)
    # Adaptive confidence modulation based on satisfaction regime (adapted from FFITTSS)
    CONFIDENCE_MODULATION_BY_REGIME = {
        'INITIALIZING': 0.80,   # Conservative - system warming up
        'EXPLORING': 0.90,      # Slight caution - active search
        'CONVERGING': 1.00,     # Neutral - approaching target
        'STABLE': 1.15,         # Boost - found good region ⭐ SWEET SPOT
        'COMMITTED': 1.10,      # Slight boost - sustained success
        'PLATEAUED': 0.85       # Pull back - escape local minimum
    }

    # Learning rate modulation by regime (for Phase 5 organic learning)
    LEARNING_RATE_BY_REGIME = {
        'INITIALIZING': 0.05,   # Very cautious
        'EXPLORING': 0.10,      # Moderate exploration
        'CONVERGING': 0.15,     # Faster learning
        'STABLE': 0.08,         # Maintain stability
        'COMMITTED': 0.03,      # Very slow - don't disrupt success
        'PLATEAUED': 0.20       # Aggressive - need to escape
    }

    # 🔧 R-Matrix Learning Rate (Fixed Nov 13, 2025)
    # Reduced from 0.05 to 0.005 (10× slower) to prevent saturation
    # See: R_MATRIX_SATURATION_FIX_COMPLETE_NOV13_2025.md
    R_MATRIX_LEARNING_RATE = 0.005  # CRITICAL: Do not increase above 0.01

    # Transduction confidence bases
    TRANSDUCTION_CONFIDENCE_HEALING = 0.70
    TRANSDUCTION_CONFIDENCE_PROTECTIVE = 0.60
    TRANSDUCTION_CONFIDENCE_CRISIS = 0.50

    # Kairos boost
    EMISSION_KAIROS_BOOST_MULTIPLIER = 1.5

    # ============================================================================
    # ORGAN PARAMETERS
    # ============================================================================

    # BOND (IFS)
    BOND_SELF_ENERGY_THRESHOLD = 0.6

    # SANS (Coherence Repair)
    SANS_SIMILARITY_THRESHOLD = 0.7
    SANS_EMBEDDING_DIM = 384

    # NDAM (Urgency Detection)
    NDAM_URGENCY_THRESHOLD = 0.75
    NDAM_ESCALATION_WINDOW = 5

    # RNX (Temporal Dynamics)
    RNX_CRISIS_TEMPORAL_THRESHOLD = 0.7
    RNX_RESTORATIVE_TEMPORAL_THRESHOLD = 0.6

    # EO (Polyvagal)
    EO_VENTRAL_VAGAL_THRESHOLD = 0.6
    EO_SYMPATHETIC_THRESHOLD = 0.7
    EO_DORSAL_VAGAL_THRESHOLD = 0.8

    # CARD (Scaling)
    CARD_MINIMAL_SCALE_THRESHOLD = 0.3
    CARD_MODERATE_SCALE_THRESHOLD = 0.6

    # ============================================================================
    # HEBBIAN LEARNING PARAMETERS
    # ============================================================================

    HEBBIAN_LEARNING_RATE = 0.1
    HEBBIAN_DECAY_RATE = 0.01
    HEBBIAN_R_MATRIX_SIZE = 11  # 11 organs

    # ============================================================================
    # PHASE 5: ORGANIC LEARNING PARAMETERS
    # ============================================================================

    ORGANIC_SIMILARITY_THRESHOLD = 0.75
    ORGANIC_FAMILY_MATURITY_COUNT = 3
    ORGANIC_SIGNATURE_DIM = 57  # 11 organs × 5 stats + 2 V0 metrics

    # ============================================================================
    # TRANSDUCTION PARAMETERS (14 Nexus Types, 9 Primary Pathways)
    # ============================================================================

    TRANSDUCTION_NEXUS_TYPES = 14
    TRANSDUCTION_PRIMARY_PATHWAYS = 9
    TRANSDUCTION_MECHANISM_COUNT = 15

    # Mutual satisfaction thresholds
    TRANSDUCTION_MUTUAL_SATISFACTION_HIGH = 0.7
    TRANSDUCTION_MUTUAL_SATISFACTION_LOW = 0.4

    # Rhythm coherence thresholds
    TRANSDUCTION_RHYTHM_COHERENCE_HIGH = 0.6
    TRANSDUCTION_RHYTHM_COHERENCE_LOW = 0.3

    # ============================================================================
    # TRAINING PARAMETERS
    # ============================================================================

    # Baseline training
    BASELINE_TRAINING_NUM_PAIRS = 30
    BASELINE_TRAINING_ENABLE_PHASE2 = True
    BASELINE_TRAINING_ENABLE_SALIENCE = True

    # Epoch training
    EPOCH_1_ITERATIONS = 10
    EPOCH_2_ITERATIONS = 20
    EPOCH_3_ITERATIONS = 30
    EPOCH_4_ITERATIONS = 40
    EPOCH_5_ITERATIONS = 50

    # ============================================================================
    # VALIDATION & TESTING PARAMETERS
    # ============================================================================

    # System maturity thresholds
    MATURITY_MIN_ACTIVE_ORGANS = 8
    MATURITY_MIN_EMISSION_CONFIDENCE = 0.3
    MATURITY_MAX_PROCESSING_TIME = 5.0  # seconds
    MATURITY_MIN_CONVERGENCE_CYCLES = 2

    # Quick validation
    QUICK_VALIDATE_TIMEOUT = 30  # seconds
    QUICK_VALIDATE_TEST_INPUTS = [
        "I'm feeling overwhelmed right now.",
        "This conversation feels really safe.",
        "I need some space."
    ]

    # ============================================================================
    # INTERACTIVE MODE PARAMETERS (NEW)
    # ============================================================================

    # Interactive prompting settings
    INTERACTIVE_ENABLE_PHASE2 = True
    INTERACTIVE_ENABLE_TSK_RECORDING = False  # Don't record interactive sessions by default
    INTERACTIVE_ENABLE_SALIENCE = True
    INTERACTIVE_SHOW_ORGAN_DETAILS = True
    INTERACTIVE_SHOW_TRANSDUCTION_TRAJECTORY = True
    INTERACTIVE_SHOW_V0_CONVERGENCE = True

    # Interactive output formatting
    INTERACTIVE_MAX_EMISSION_DISPLAY = 500  # characters
    INTERACTIVE_SHOW_CONFIDENCE = True
    INTERACTIVE_SHOW_NEXUSES = True

    # ============================================================================
    # MODE DETECTION
    # ============================================================================

    @classmethod
    def get_mode_config(cls, mode: str) -> dict:
        """
        Get configuration for specific mode of operation.

        Args:
            mode: 'training', 'validation', 'interactive', or 'production'

        Returns:
            Dictionary with mode-specific configuration
        """
        mode_configs = {
            'training': {
                'enable_phase2': True,
                'enable_tsk_recording': True,
                'enable_salience': True,
                'verbose': True
            },
            'validation': {
                'enable_phase2': True,
                'enable_tsk_recording': True,
                'enable_salience': True,
                'verbose': True
            },
            'interactive': {
                'enable_phase2': cls.INTERACTIVE_ENABLE_PHASE2,
                'enable_tsk_recording': cls.INTERACTIVE_ENABLE_TSK_RECORDING,
                'enable_salience': cls.INTERACTIVE_ENABLE_SALIENCE,
                'verbose': cls.INTERACTIVE_SHOW_ORGAN_DETAILS
            },
            'production': {
                'enable_phase2': True,
                'enable_tsk_recording': True,
                'enable_salience': True,
                'verbose': False
            }
        }

        return mode_configs.get(mode, mode_configs['production'])

    # ============================================================================
    # HELPER METHODS
    # ============================================================================

    @classmethod
    def ensure_directories(cls):
        """Create all necessary directories if they don't exist."""
        directories = [
            cls.PERSONA_LAYER_DIR,
            cls.KNOWLEDGE_BASE_DIR,
            cls.TSK_DIR,
            cls.SESSIONS_DIR,
            cls.BUNDLE_DIR,
            cls.MONITORING_DIR,
            cls.TESTS_DIR,
            cls.TRAINING_DIR,
            cls.DOCS_DIR,
            cls.SCRIPTS_DIR,
            cls.RESULTS_DIR,
            cls.EPOCH_RESULTS_DIR,
            cls.VALIDATION_RESULTS_DIR,
            cls.VISUALIZATION_DIR
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def validate_paths(cls) -> dict:
        """
        Validate that all critical paths exist.

        Returns:
            Dictionary with validation results
        """
        critical_files = {
            'semantic_atoms': cls.SEMANTIC_ATOMS_PATH,
            'training_pairs': cls.CONVERSATIONAL_TRAINING_PAIRS_PATH,
        }

        results = {}
        for name, path in critical_files.items():
            results[name] = path.exists()

        return results

    @classmethod
    def get_epoch_results_path(cls, epoch: int) -> Path:
        """Get results path for specific epoch."""
        return cls.EPOCH_RESULTS_DIR / f"epoch_{epoch}_results.json"

    @classmethod
    def get_session_dir(cls, user_id: str, session_id: str) -> Path:
        """Get session directory for specific user and session."""
        return cls.SESSIONS_DIR / f"session_{user_id}_{session_id}"

    # ============================================================================
    # PERSONA LAYER CONFIGURATION (LEVELS 8-10)
    # ============================================================================

    # Global toggles
    PERSONA_LAYER_ENABLED = True  # Set False to disable entire companion system

    # User profile defaults
    DEFAULT_RESPONSE_LENGTH = "moderate"  # "minimal", "moderate", "comprehensive"
    DEFAULT_HUMOR_TOLERANCE = 0.5  # 0.0 (serious only) to 1.0 (playful welcomed)
    DEFAULT_SMALL_TALK_OPENNESS = 0.5  # 0.0 (direct only) to 1.0 (casual welcomed)
    USER_PROFILE_AUTO_SAVE = True

    # Template selection behavior
    TEMPLATE_CONFIDENCE_THRESHOLD = 0.4  # Use templates only if confidence > this
    TEMPLATE_RANDOM_SELECTION = False  # True = random, False = weighted by success

    # ============================================================================
    # LOCAL LLM CONFIGURATION (OPTIONAL - DEFAULT: DISABLED)
    # ============================================================================

    # ⭐ PRIMARY TOGGLE - Set to False for 100% template-only operation
    LOCAL_LLM_ENABLED = True  # ENABLED for felt-guided LLM (Nov 13, 2025)

    # LLM Backend settings (only relevant if LOCAL_LLM_ENABLED = True)
    LOCAL_LLM_BACKEND = "ollama"  # "ollama", "lmstudio", "gpt4all"
    LOCAL_LLM_MODEL = "llama3.2:3b"
    LOCAL_LLM_ENDPOINT = "http://localhost:11434/api/generate"
    LOCAL_LLM_MAX_TOKENS = 150
    LOCAL_LLM_TEMPERATURE = 0.7
    LOCAL_LLM_TIMEOUT = 30  # seconds (Nov 13, 2025 - increased for felt-guided LLM)

    # When to query LLM (only if enabled)
    LLM_QUERY_FOR_FACTUAL = True  # Use LLM for factual questions
    LLM_QUERY_FOR_CREATIVE = True  # Use LLM for creative/metaphor tasks
    LLM_QUERY_FOR_SMALL_TALK = False  # Templates sufficient for small talk
    LLM_QUERY_MIN_CONFIDENCE = 0.3  # Only query if DAE confidence < this

    # Safety: NEVER query LLM in these conditions (even if enabled)
    LLM_NEVER_IN_ZONES = [4, 5]  # Protective/collapse zones
    LLM_NEVER_IF_NDAM_ABOVE = 0.7  # Crisis threshold
    LLM_NEVER_FOR_THERAPEUTIC = True  # Therapeutic core always DAE-only

    # ============================================================================
    # HYBRID SUPERJECT CONFIGURATION (WEEK 1 - NOV 13, 2025)
    # ============================================================================

    # 🆕 PRIMARY HYBRID TOGGLE - Memory-enriched LLM scaffolding with progressive weaning
    HYBRID_ENABLED = True  # ACTIVATED FOR TESTING (opt-in experimental feature)

    # 🌀 FELT-GUIDED LLM TOGGLE - Unlimited felt intelligence (Nov 13, 2025)
    FELT_GUIDED_LLM_ENABLED = True  # Replaces hebbian fallback with unlimited LLM (Option B)

    # LLM Integration (Ollama with memory context)
    HYBRID_LLM_MODEL = "llama3.2:3b"
    HYBRID_LLM_OLLAMA_URL = "http://localhost:11434"
    HYBRID_LLM_RESPONSE_MODE = "full_response"  # 'full_response', 'guidance', 'validation'
    HYBRID_LLM_MAX_TOKENS = 500
    HYBRID_LLM_TEMPERATURE = 0.7
    HYBRID_LLM_TIMEOUT = 30  # seconds (longer than basic LLM - includes memory retrieval)

    # Progressive LLM Weaning (Month 0 → Month 12)
    HYBRID_LLM_INITIAL_WEIGHT = 0.80  # Month 0: 80% LLM scaffolding
    HYBRID_LLM_FINAL_WEIGHT = 0.05    # Month 12: 5% LLM (95% autonomous)
    HYBRID_LLM_WEANING_RATE = 0.24    # Exponential decay: w(t) = 0.80·e^(-0.24·t) + 0.05

    # Hybrid V0 Energy Coefficients (adjusted from pure DAE to include LLM term)
    V0_ALPHA_HYBRID = 0.35     # Satisfaction (reduced from 0.40 to make room for LLM)
    V0_BETA_HYBRID = 0.25      # Delta energy (unchanged)
    V0_GAMMA_HYBRID = 0.12     # Appetition (reduced from 0.15)
    V0_DELTA_HYBRID = 0.10     # Relevance (unchanged)
    V0_ZETA_HYBRID = 0.10      # Complexity (unchanged)
    V0_ETA_HYBRID = 0.08       # LLM uncertainty (NEW - decays to 0.01 over 12 months)

    # Memory Retrieval (Prehensive Recall)
    HYBRID_MEMORY_TOP_K = 5              # Retrieve top 5 similar past moments
    HYBRID_MEMORY_RECENCY_WEIGHT = 0.2   # Weight for recent conversations
    HYBRID_MEMORY_FAMILY_BONUS = 0.15    # Bonus for same organic family
    HYBRID_MEMORY_HEBBIAN_BONUS = 0.1    # Bonus for hebbian R-matrix alignment

    # Superject Recording (Persistent Conversational Datum)
    HYBRID_SUPERJECT_SESSION_LOGGING = True  # Save session transcripts
    HYBRID_SUPERJECT_SESSION_DIR = SESSIONS_DIR
    HYBRID_SUPERJECT_USER_BUNDLES_DIR = BUNDLE_DIR

    # LLM Activation Cache (Optional - for organ activation augmentation)
    HYBRID_LLM_ACTIVATION_CACHE_PATH = PERSONA_LAYER_DIR / "llm_activation_cache_local.json"
    HYBRID_LLM_ACTIVATION_CACHE_ENABLED = True  # Use cached activations if available

    # Safety & Fallback
    HYBRID_FALLBACK_TO_ORGAN = True   # If LLM fails, use pure organ emission
    HYBRID_REQUIRE_OLLAMA = False     # If True, error if Ollama not running; if False, graceful fallback

    # Adaptive Weaning (Auto-adjust based on performance)
    HYBRID_ADAPTIVE_WEANING_ENABLED = True  # Auto-reduce LLM weight if organ performance exceeds
    HYBRID_ADAPTIVE_THRESHOLD = 0.10        # Organ must outperform LLM by this much to trigger weaning
    HYBRID_ADAPTIVE_ADJUSTMENT = 0.05       # Amount to adjust LLM weight per trigger

    @classmethod
    def get_hybrid_config(cls):
        """Get all hybrid-related configuration as a dict."""
        return {
            'enabled': cls.HYBRID_ENABLED,
            'llm': {
                'model': cls.HYBRID_LLM_MODEL,
                'url': cls.HYBRID_LLM_OLLAMA_URL,
                'response_mode': cls.HYBRID_LLM_RESPONSE_MODE,
                'max_tokens': cls.HYBRID_LLM_MAX_TOKENS,
                'temperature': cls.HYBRID_LLM_TEMPERATURE,
                'timeout': cls.HYBRID_LLM_TIMEOUT,
            },
            'weaning': {
                'initial_weight': cls.HYBRID_LLM_INITIAL_WEIGHT,
                'final_weight': cls.HYBRID_LLM_FINAL_WEIGHT,
                'weaning_rate': cls.HYBRID_LLM_WEANING_RATE,
            },
            'v0_coefficients': {
                'alpha': cls.V0_ALPHA_HYBRID,
                'beta': cls.V0_BETA_HYBRID,
                'gamma': cls.V0_GAMMA_HYBRID,
                'delta': cls.V0_DELTA_HYBRID,
                'zeta': cls.V0_ZETA_HYBRID,
                'eta': cls.V0_ETA_HYBRID,
            },
            'memory_retrieval': {
                'top_k': cls.HYBRID_MEMORY_TOP_K,
                'recency_weight': cls.HYBRID_MEMORY_RECENCY_WEIGHT,
                'family_bonus': cls.HYBRID_MEMORY_FAMILY_BONUS,
                'hebbian_bonus': cls.HYBRID_MEMORY_HEBBIAN_BONUS,
            },
            'superject': {
                'session_logging': cls.HYBRID_SUPERJECT_SESSION_LOGGING,
                'session_dir': str(cls.HYBRID_SUPERJECT_SESSION_DIR),
                'user_bundles_dir': str(cls.HYBRID_SUPERJECT_USER_BUNDLES_DIR),
            },
            'safety': {
                'fallback_to_organ': cls.HYBRID_FALLBACK_TO_ORGAN,
                'require_ollama': cls.HYBRID_REQUIRE_OLLAMA,
            },
            'adaptive_weaning': {
                'enabled': cls.HYBRID_ADAPTIVE_WEANING_ENABLED,
                'threshold': cls.HYBRID_ADAPTIVE_THRESHOLD,
                'adjustment': cls.HYBRID_ADAPTIVE_ADJUSTMENT,
            }
        }


# ============================================================================
# MODULE-LEVEL EXPORTS
# ============================================================================

# Export Config class as default
__all__ = ['Config']

# Quick access to common paths (for backward compatibility during migration)
PROJECT_ROOT = Config.PROJECT_ROOT
SEMANTIC_ATOMS_PATH = Config.SEMANTIC_ATOMS_PATH
HEBBIAN_MEMORY_PATH = Config.HEBBIAN_MEMORY_PATH
CONVERSATIONAL_TRAINING_PAIRS_PATH = Config.CONVERSATIONAL_TRAINING_PAIRS_PATH
