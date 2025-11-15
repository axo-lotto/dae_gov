#!/usr/bin/env python3
"""
DAE_HYPHAE_1 Interactive Mode
==============================

Interactive prompting interface for conversing with the organism.
Allows real-time testing, exploration, and conversation.

Usage:
    python3 dae_interactive.py

    # Or with specific mode
    python3 dae_interactive.py --mode detailed

Modes:
    - simple: Just show emission text
    - standard: Show emission + confidence + nexuses (default)
    - detailed: Show full organ details + transduction trajectory
    - debug: Show everything including V0 convergence cycles

Date: November 12, 2025
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.user_registry import UserRegistry
from persona_layer.feedback_collector import FeedbackCollector

# 🌀 Phase 1.7: Command expansion imports (Nov 14, 2025)
from monitoring.mycelial_identity_tracker import MycelialIdentityTracker
from persona_layer.user_superject_learner import UserSuperjectLearner

# 🌀 Phase 1.8: Entity extraction imports (Nov 14, 2025)
from persona_layer.memory_intent_detector import MemoryIntentDetector
from persona_layer.entity_extractor import EntityExtractor

# Hybrid components (conditional import)
if Config.HYBRID_ENABLED:
    from persona_layer.memory_retrieval import MemoryRetrieval
    from persona_layer.superject_recorder import SuperjectRecorder
    from persona_layer.local_llm_bridge import MemoryEnrichedLLMBridge


class InteractiveSession:
    """Interactive conversation session with DAE_HYPHAE_1."""

    def __init__(self, mode='standard', user_id=None, username=None):
        """
        Initialize interactive session with user identity.

        Args:
            mode: Display mode ('simple', 'standard', 'detailed', 'debug')
            user_id: Existing user ID (for returning users)
            username: Username for new user creation
        """
        # User identity & feedback
        self.user_registry = UserRegistry()
        self.feedback_collector = FeedbackCollector()

        # Handle user login/creation
        if user_id:
            self.user = self.user_registry.get_user(user_id)
            if not self.user:
                print(f"⚠️  User {user_id} not found, creating new user")
                user_id = self.user_registry.create_user(username)
                self.user = self.user_registry.get_user(user_id)
        else:
            # Interactive user creation
            print("\n🆔 USER IDENTIFICATION")
            print("="*50)
            choice = input("(N)ew user or (E)xisting user? [N/e]: ").strip().lower()

            if choice == 'e':
                # List existing users
                users = self.user_registry.list_users()
                if users:
                    print("\nExisting users:")
                    for i, u in enumerate(users, 1):
                        print(f"  {i}. {u['username']} ({u['user_id'][:20]}...)")
                        print(f"     Sessions: {u['total_sessions']}, Turns: {u['total_turns']}")

                    user_input = input("\nEnter number or user ID: ").strip()

                    # Check if number
                    if user_input.isdigit():
                        idx = int(user_input) - 1
                        if 0 <= idx < len(users):
                            user_id = users[idx]['user_id']
                    else:
                        user_id = user_input

                    self.user = self.user_registry.get_user(user_id)

                    if not self.user:
                        print(f"⚠️  User not found, creating new user")
                        username = input("Enter a username: ").strip()
                        user_id = self.user_registry.create_user(username)
                        self.user = self.user_registry.get_user(user_id)
                else:
                    print("No existing users found. Creating new user.")
                    username = input("Enter a username: ").strip()
                    user_id = self.user_registry.create_user(username)
                    self.user = self.user_registry.get_user(user_id)
            else:
                # New user
                username = input("Enter a username (optional): ").strip() or None
                user_id = self.user_registry.create_user(username)
                self.user = self.user_registry.get_user(user_id)

        # Load user state
        self.user_state = self.user_registry.load_user_state(self.user['user_id'])

        # Get user feedback stats
        user_stats = self.feedback_collector.get_user_feedback_stats(self.user['user_id'])

        print(f"\n✅ Logged in as: {self.user['username']}")
        print(f"   User ID: {self.user['user_id'][:30]}...")
        print(f"   Total sessions: {self.user['total_sessions']}")
        print(f"   Total turns: {self.user['total_turns']}")
        if user_stats['total_ratings'] > 0:
            print(f"   Helpful rate: {user_stats['helpful_rate']*100:.1f}% ({user_stats['total_ratings']} ratings)")

        # Session tracking
        self.mode = mode
        self.display_mode = mode  # ✅ Fix: Add display_mode attribute
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.conversation_history = []

        # Get mode-specific configuration
        mode_config = Config.get_mode_config('interactive')
        self.enable_phase2 = mode_config['enable_phase2']
        self.enable_tsk_recording = mode_config['enable_tsk_recording']
        self.enable_salience = mode_config['enable_salience']

        # Display settings based on mode
        self.display_settings = {
            'simple': {
                'show_emission': True,
                'show_confidence': False,
                'show_nexuses': False,
                'show_organs': False,
                'show_transduction': False,
                'show_v0': False
            },
            'standard': {
                'show_emission': True,
                'show_confidence': True,
                'show_nexuses': True,
                'show_organs': False,
                'show_transduction': False,
                'show_v0': False
            },
            'detailed': {
                'show_emission': True,
                'show_confidence': True,
                'show_nexuses': True,
                'show_organs': True,
                'show_transduction': True,
                'show_v0': False
            },
            'debug': {
                'show_emission': True,
                'show_confidence': True,
                'show_nexuses': True,
                'show_organs': True,
                'show_transduction': True,
                'show_v0': True
            }
        }

        self.settings = self.display_settings.get(mode, self.display_settings['standard'])

        print("\n" + "="*80)
        print("🌀 DAE_HYPHAE_1 INTERACTIVE MODE")
        print("="*80)
        print(f"\nSession ID: {self.session_id}")
        print(f"Display Mode: {mode}")
        print(f"Phase 2 (Multi-cycle V0): {'✅ Enabled' if self.enable_phase2 else '❌ Disabled'}")
        print(f"Salience (Trauma-aware): {'✅ Enabled' if self.enable_salience else '❌ Disabled'}")
        print(f"TSK Recording: {'✅ Enabled' if self.enable_tsk_recording else '❌ Disabled'}")

        # Initialize organism
        print("\n📋 Initializing organism...")
        self.organism = ConversationalOrganismWrapper()
        print("✅ Organism ready")

        # 🌀 Phase 1.7: Initialize command components (Nov 14, 2025)
        try:
            self.identity_tracker = MycelialIdentityTracker()
            self.user_superject_learner = UserSuperjectLearner()
            print("✅ Identity tracker & superject learner ready")
        except Exception as e:
            print(f"⚠️  Command components initialization failed: {e}")
            self.identity_tracker = None
            self.user_superject_learner = None

        # 🌀 Phase 1.8: Initialize entity extraction (Nov 14, 2025)
        try:
            self.memory_intent_detector = MemoryIntentDetector()
            self.entity_extractor = EntityExtractor()
            print("✅ Memory intent detector & entity extractor ready")
        except Exception as e:
            print(f"⚠️  Entity extraction initialization failed: {e}")
            self.memory_intent_detector = None
            self.entity_extractor = None

        # 🌀 Phase 1.8++: Initialize Neo4j knowledge graph (Nov 14, 2025)
        # Dual-storage strategy: JSON fallback + Neo4j enrichment
        self.knowledge_graph = None
        if Config.NEO4J_ENABLED:
            try:
                from knowledge_base.neo4j_knowledge_graph import Neo4jKnowledgeGraph
                self.knowledge_graph = Neo4jKnowledgeGraph(
                    uri=Config.NEO4J_URI,
                    user=Config.NEO4J_USER,
                    password=Config.NEO4J_PASSWORD,
                    database=Config.NEO4J_DATABASE
                )
                if self.knowledge_graph.driver:
                    print("✅ Neo4j knowledge graph connected (entity memory enrichment enabled)")
                else:
                    print("⚠️  Neo4j unavailable, using JSON fallback only")
                    self.knowledge_graph = None
            except Exception as e:
                print(f"⚠️  Neo4j initialization failed: {e}")
                print("   Using JSON fallback for entity storage")
                self.knowledge_graph = None
        else:
            print("ℹ️  Neo4j disabled in config, using JSON fallback for entity storage")

        # Initialize hybrid components (if enabled)
        if Config.HYBRID_ENABLED:
            print("\n🆕 Initializing hybrid superject system...")
            try:
                self.memory_retrieval = MemoryRetrieval(
                    hebbian_memory_path=str(Config.HEBBIAN_MEMORY_PATH),
                    organic_families_path=str(Config.ORGANIC_FAMILIES_PATH),
                    top_k=Config.HYBRID_MEMORY_TOP_K
                )
                self.superject_recorder = SuperjectRecorder(
                    session_storage_dir=str(Config.HYBRID_SUPERJECT_SESSION_DIR),
                    user_bundles_dir=str(Config.HYBRID_SUPERJECT_USER_BUNDLES_DIR)
                )
                self.llm_bridge = MemoryEnrichedLLMBridge(
                    model_name=Config.HYBRID_LLM_MODEL,
                    ollama_url=Config.HYBRID_LLM_OLLAMA_URL
                )
                self.llm_weight = Config.HYBRID_LLM_INITIAL_WEIGHT

                # 🌀 Initialize felt-guided LLM (if enabled)
                if Config.FELT_GUIDED_LLM_ENABLED:
                    from persona_layer.llm_felt_guidance import FeltGuidedLLMGenerator
                    self.felt_guided_llm = FeltGuidedLLMGenerator(
                        llm_bridge=self.llm_bridge,
                        enable_safety_gates=True,
                        enable_emergent_personality=True
                    )
                    # Pass to organism's emission generator
                    self.organism.emission_generator.felt_guided_llm = self.felt_guided_llm
                else:
                    self.felt_guided_llm = None

                # Start hybrid session
                self.hybrid_session_id = self.superject_recorder.start_session(user_id=self.user['user_id'])
                print(f"✅ Hybrid mode enabled (LLM weight: {self.llm_weight:.2f})")
            except Exception as e:
                print(f"⚠️  Hybrid initialization failed: {e}")
                print("   Falling back to pure DAE mode")
                self.memory_retrieval = None
                self.superject_recorder = None
                self.llm_bridge = None
        else:
            self.memory_retrieval = None
            self.superject_recorder = None
            self.llm_bridge = None
            self.felt_guided_llm = None

        print()
        print("="*80)
        print("💬 Interactive Session Started")
        print("="*80)
        print("\nCommands:")
        print("  /help     - Show this help message")
        print("  /mode     - Change display mode")
        print("  /history  - Show conversation history")
        print("  /save     - Save conversation to file")
        print("  /exit     - Exit interactive mode")
        print("\nType your message and press Enter to converse with the organism.")
        print("="*80 + "\n")

    def process_input(self, user_input: str) -> dict:
        """
        Process user input through the organism (with optional hybrid).

        Args:
            user_input: Text input from user

        Returns:
            Processing result dictionary
        """
        context = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'turn': len(self.conversation_history) + 1
        }

        # 🌀 Phase 1.8++: Load entity context on EVERY turn (Nov 14, 2025)
        # 🌀 Phase 1.8+++: Enhanced persistent context (Nov 14, 2025 - Memory persistence fix)
        # This ensures DAE organism AND LLM always have access to stored entities
        if 'user_profile' in self.user_state:
            from persona_layer.superject_structures import EnhancedUserProfile
            profile = EnhancedUserProfile.from_dict(self.user_state['user_profile'])

            # ALWAYS add entity context string (even if empty) - for LLM bridge
            context['entity_context_string'] = profile.get_entity_context_string()

            # Add individual entities to context for organism access
            if profile.entities:
                context['stored_entities'] = profile.entities

                # Add username for personalization (check multiple sources)
                if 'user_name' in profile.entities:
                    context['username'] = profile.entities['user_name']
                elif 'username' in self.user:
                    context['username'] = self.user['username']

                # Add other key entities for easy access
                if 'family_members' in profile.entities:
                    context['family_members'] = profile.entities['family_members']
                if 'preferences' in profile.entities:
                    context['preferences'] = profile.entities['preferences']
        else:
            # Fallback: Use username from registry if no profile exists yet
            if 'username' in self.user:
                context['username'] = self.user['username']

        # 🌀 Phase 1.8: Entity extraction & memory storage (Nov 14, 2025)
        # 🌀 Phase 1.8+: TSK Integration - pass felt_state for transductive context
        # 🌀 Phase 1.8++: ALWAYS-ON entity extraction (Nov 14, 2025 - Critical Fix)
        # 🌀 Phase 1.8+++: Run MemoryIntentDetector FIRST (Nov 14, 2025 - Memory persistence fix)
        memory_intent_detected = False
        extracted_entities = {}
        intent_type = 'general'
        intent_context = {}

        # Step 1: ALWAYS run MemoryIntentDetector to check for names, relationships, etc.
        if self.memory_intent_detector:
            intent_detected, intent_type, confidence, intent_context = self.memory_intent_detector.detect(user_input)
            if intent_detected and confidence > 0.5:  # Lower threshold to catch more
                memory_intent_detected = True
                context['memory_intent'] = True
                context['memory_intent_type'] = intent_type
                context['memory_intent_confidence'] = confidence

        # Step 2: ALWAYS run EntityExtractor with proper intent_type and context
        if self.entity_extractor:
            extracted_entities = self.entity_extractor.extract(
                user_input,
                intent_type=intent_type,  # Use detected intent type (or 'general')
                context=intent_context  # Use context from detector (includes extracted_name if found)
            )

            # Check if ANY entities were extracted
            if extracted_entities and any(k != 'timestamp' and k != 'source_text' and k != 'intent_type'
                                         and extracted_entities.get(k) for k in extracted_entities.keys()):
                memory_intent_detected = True  # Mark that we found actual entities
                context['pre_extraction_entities'] = extracted_entities

        # Step 1: Process through organism (11 organs)
        result = self.organism.process_text(
            user_input,
            context=context,
            enable_tsk_recording=self.enable_tsk_recording,
            enable_phase2=self.enable_phase2,
            user_id=self.user['user_id'],  # 🌀 Phase 1.6: User identity (Nov 14, 2025)
            username=self.user['username']  # 🌀 Phase 1.6: Username for personalization (Nov 14, 2025)
        )

        # 🌀 Phase 1.8+: TSK Entity Enrichment (Nov 14, 2025)
        # If memory intent was detected, enrich entities with transductive felt-state
        if memory_intent_detected and 'pre_extraction_entities' in context:
            try:
                # Extract felt-state from organism result
                organ_results = result.get('organ_results', {})
                felt_states = result.get('felt_states', {})

                # Build felt_state dict for entity enrichment
                felt_state = {
                    'organ_results': organ_results,
                    'felt_states': felt_states,
                }

                # Add polyvagal state (from EO organ)
                if 'EO' in organ_results:
                    eo_result = organ_results['EO']
                    felt_state['polyvagal_state'] = getattr(eo_result, 'polyvagal_state', 'unknown')

                # Add self_distance (from BOND organ)
                if 'BOND' in organ_results:
                    bond_result = organ_results['BOND']
                    felt_state['self_distance'] = getattr(bond_result, 'self_distance', 0.5)

                # Add urgency level (from NDAM salience markers)
                if 'salience_trauma_markers' in felt_states:
                    felt_state['salience_trauma_markers'] = felt_states['salience_trauma_markers']

                # Add nexuses (from felt_states)
                if 'nexuses' in felt_states:
                    felt_state['nexuses'] = felt_states['nexuses']

                # Add V0 and satisfaction
                felt_state['v0_energy'] = felt_states.get('v0_energy_final', 0.5)
                felt_state['satisfaction'] = felt_states.get('satisfaction', 0.5)
                felt_state['convergence_cycles'] = felt_states.get('convergence_cycles', 1)

                # Add transduction info
                felt_state['transduction_mechanism'] = felt_states.get('transduction_mechanism')
                felt_state['transduction_pathway'] = felt_states.get('transduction_pathway')
                felt_state['healing_trajectory'] = felt_states.get('healing_trajectory', False)

                # Re-extract entities with transductive context
                enriched_entities = self.entity_extractor.extract(
                    user_input,
                    context['pre_extraction_entities'].get('intent_type', 'unknown'),
                    context,
                    felt_state=felt_state
                )

                # Store enriched entities in user profile
                # 🌀 Phase 1.8++: CREATE profile if it doesn't exist (Nov 14, 2025 - Critical Fix)
                from persona_layer.superject_structures import EnhancedUserProfile

                if 'user_profile' in self.user_state:
                    profile = EnhancedUserProfile.from_dict(self.user_state['user_profile'])
                else:
                    # Create new profile if it doesn't exist
                    now = datetime.now().isoformat()
                    profile = EnhancedUserProfile(
                        user_id=self.user['user_id'],
                        created_at=now,
                        last_active=now
                    )

                profile.store_entities(enriched_entities)
                self.user_state['user_profile'] = profile.to_dict()

                # Save user state (JSON fallback - always done)
                self.user_registry.save_user_state(self.user['user_id'], self.user_state)

                # 🌀 Phase 1.8++: ALSO store in Neo4j if enabled (Nov 14, 2025)
                # Dual-storage strategy: JSON (fallback) + Neo4j (enrichment)
                if self.knowledge_graph and Config.NEO4J_DUAL_STORAGE:
                    try:
                        self._store_entities_in_neo4j(enriched_entities, felt_state)
                        if self.display_mode in ['detailed', 'debug']:
                            print(f"🌀 Entities also stored in Neo4j (dual-storage)")
                    except Exception as e:
                        if self.display_mode == 'debug':
                            print(f"⚠️  Neo4j entity storage failed (JSON fallback succeeded): {e}")
                        # Non-critical - JSON storage already succeeded

                # Update context with enriched entity string for LLM
                context['entity_context_string'] = profile.get_entity_context_string()

                if self.display_mode in ['detailed', 'debug']:
                    print(f"🌀 TSK-enriched entities stored in profile")
                    if enriched_entities.get('transductive_context'):
                        tc = enriched_entities['transductive_context']
                        print(f"   Polyvagal: {tc.get('polyvagal_state', 'unknown')}")
                        print(f"   Urgency: {tc.get('urgency_level', 0.0):.2f}")
                        print(f"   Nexuses: {', '.join(tc.get('dominant_nexuses', [])[:2])}")

            except Exception as e:
                if self.display_mode == 'debug':
                    print(f"\n⚠️  TSK entity enrichment failed: {e}")
                # Continue without enrichment - non-critical failure

        # Step 2: Hybrid processing (if enabled)
        if Config.HYBRID_ENABLED and self.llm_bridge:
            try:
                organ_results = result.get('organ_results', {})
                felt_states = result.get('felt_states', {})

                # Extract organ signature (57D)
                organ_signature = self._extract_organ_signature(organ_results)

                # Retrieve similar moments from memory
                similar_moments = self.memory_retrieval.retrieve_similar_moments(
                    current_organ_signature=organ_signature,
                    current_family_id=felt_states.get('family_id'),
                    user_id=self.user['user_id']
                )

                # Load user bundle
                user_bundle = self.memory_retrieval.load_user_bundle(self.user['user_id'])

                # Extract polyvagal and self_zone safely
                polyvagal_state = 'unknown'
                self_zone = 0
                if 'EO' in organ_results:
                    eo_result = organ_results['EO']
                    polyvagal_state = getattr(eo_result, 'polyvagal_state', 'unknown')
                if 'BOND' in organ_results:
                    bond_result = organ_results['BOND']
                    self_zone = getattr(bond_result, 'self_zone', 0)

                # Query LLM with memory context
                llm_response = self.llm_bridge.query_with_memory(
                    user_input=user_input,
                    dae_felt_states={
                        'polyvagal': polyvagal_state,
                        'self_zone': self_zone,
                        'top_organs': self._get_top_organs(organ_results, k=3),
                    },
                    similar_moments=similar_moments,
                    user_bundle=user_bundle
                )

                # Store hybrid data in result
                result['hybrid'] = {
                    'llm_response': llm_response.get('llm_response', ''),
                    'llm_confidence': llm_response.get('confidence', 0.0),
                    'similar_moments_count': len(similar_moments),
                    'llm_weight': self.llm_weight
                }

                # Record superject (persistent memory)
                if self.superject_recorder:
                    self.superject_recorder.record_superject(
                        user_message=user_input,
                        dae_response=felt_states.get('emission_text', ''),
                        organ_results=organ_results,
                        felt_states={
                            'v0_energy': felt_states.get('v0_energy_final', 0.0),
                            'satisfaction_score': felt_states.get('satisfaction', 0.0),
                            'emission_confidence': felt_states.get('emission_confidence', 0.0),
                            'emission_path': felt_states.get('emission_path', 'unknown'),
                        },
                        family_assignment={'family_id': felt_states.get('family_id')},
                        user_id=self.user['user_id']
                    )

            except Exception as e:
                print(f"\n⚠️  Hybrid processing failed: {e}")
                # Continue with pure DAE result

        return result

    def detect_continuous_reflection_need(self, user_input: str, initial_result: dict) -> dict:
        """
        Determine if input warrants multi-layer continuous reflection processing.

        Criteria for continuous reflection:
        - Long input (500+ characters)
        - High complexity (multiple semantic fields, high nexus count)
        - Trauma markers present
        - Deep polyvagal/self zones

        Args:
            user_input: User's text input
            initial_result: First processing result from organism

        Returns:
            dict with 'triggered' bool and detailed metrics for tracking
        """
        felt_states = initial_result.get('felt_states', {})
        organ_results = initial_result.get('organ_results', {})

        # Input length check
        input_length = len(user_input)
        long_input = input_length >= 500

        # Semantic complexity check
        semantic_fields = felt_states.get('semantic_fields', [])
        num_fields = len(semantic_fields)
        many_fields = num_fields >= 5

        # Nexus formation check
        nexus_count = felt_states.get('emission_nexus_count', 0)
        many_nexuses = nexus_count >= 4

        # Trauma markers extraction
        trauma_metrics = {
            'bond_self_distance': 0.0,
            'eo_polyvagal_state': 'unknown',
            'ndam_urgency': 0.0,
            'sans_coherence': 1.0,
            'trauma_present': False
        }

        # BOND: self-distance (parts fragmentation)
        if 'BOND' in organ_results:
            bond = organ_results['BOND']
            if hasattr(bond, 'self_distance'):
                trauma_metrics['bond_self_distance'] = bond.self_distance
                if bond.self_distance >= 0.6:
                    trauma_metrics['trauma_present'] = True

        # EO: polyvagal state
        if 'EO' in organ_results:
            eo = organ_results['EO']
            if hasattr(eo, 'polyvagal_state'):
                trauma_metrics['eo_polyvagal_state'] = eo.polyvagal_state
                if eo.polyvagal_state in ['dorsal', 'sympathetic']:
                    trauma_metrics['trauma_present'] = True

        # NDAM: urgency/salience
        if 'NDAM' in organ_results:
            ndam = organ_results['NDAM']
            if hasattr(ndam, 'urgency_level'):
                trauma_metrics['ndam_urgency'] = ndam.urgency_level
            elif hasattr(ndam, 'salience_score'):
                trauma_metrics['ndam_urgency'] = ndam.salience_score

        # SANS: coherence repair (lower = more fragmentation)
        if 'SANS' in organ_results:
            sans = organ_results['SANS']
            if hasattr(sans, 'coherence_score'):
                trauma_metrics['sans_coherence'] = sans.coherence_score

        # Self zone tracking
        self_zone = felt_states.get('self_zone', 1)
        v0_energy = felt_states.get('v0_final_energy', 0.5)

        # Compile detection metrics
        detection_metrics = {
            'triggered': long_input and (trauma_metrics['trauma_present'] or many_fields or many_nexuses),
            'input_length': input_length,
            'semantic_fields_count': num_fields,
            'nexus_count': nexus_count,
            'self_zone': self_zone,
            'v0_energy': v0_energy,
            'trauma_metrics': trauma_metrics,
            'complexity_score': (num_fields * 0.3) + (nexus_count * 0.4) + (trauma_metrics['bond_self_distance'] * 0.3)
        }

        return detection_metrics

    def generate_continuous_reflections(self, user_input: str, num_layers: int = 3) -> list:
        """
        Generate multiple perspectives on the same input using different organ configurations.

        Each layer explores a different dimension:
        - Layer 1: Immediate felt response (default organ weights)
        - Layer 2: Relational/identity exploration (WISDOM, AUTHENTICITY, BOND focus)
        - Layer 3: Integration/grounding (PRESENCE, WISDOM, SANS focus)

        Args:
            user_input: The complex input to process
            num_layers: Number of reflection layers (2-4, default 3)

        Returns:
            List of processing results, one per layer
        """
        layers = []

        layer_configs = [
            {
                'name': 'Immediate Felt Response',
                'description': 'First felt resonance with your experience',
                'organ_emphasis': None  # Use default weights
            },
            {
                'name': 'Relational Patterns',
                'description': 'How this shapes connection and identity',
                'organ_emphasis': ['WISDOM', 'AUTHENTICITY', 'BOND', 'LISTENING']
            },
            {
                'name': 'Integration & Ground',
                'description': 'Finding stability and wholeness',
                'organ_emphasis': ['PRESENCE', 'WISDOM', 'SANS', 'AUTHENTICITY']
            },
            {
                'name': 'Healing Pathways',
                'description': 'What wants to emerge',
                'organ_emphasis': ['WISDOM', 'PRESENCE', 'EMPATHY', 'AUTHENTICITY']
            }
        ]

        for i in range(min(num_layers, len(layer_configs))):
            config = layer_configs[i]

            # Note: Current organism doesn't support organ_weight_override yet
            # For now, each layer uses default processing but we track which focus it represents
            result = self.process_input(user_input)

            layers.append({
                'layer_num': i + 1,
                'config': config,
                'result': result
            })

        return layers

    def _extract_organ_signature(self, organ_results: dict) -> dict:
        """Extract 57D organ signature from organ results."""
        signature = {}
        for organ_name, organ_result in organ_results.items():
            if hasattr(organ_result, 'atom_activations'):
                signature[organ_name] = organ_result.atom_activations
            elif isinstance(organ_result, dict) and 'atom_activations' in organ_result:
                signature[organ_name] = organ_result['atom_activations']
        return signature

    def _store_entities_in_neo4j(self, enriched_entities: dict, felt_state: dict):
        """
        Store extracted entities in Neo4j knowledge graph.

        Creates entity nodes and relationships with TSK enrichment.

        Args:
            enriched_entities: Extracted entities with transductive context
            felt_state: TSK felt state for enrichment
        """
        if not self.knowledge_graph:
            return

        # Prepare TSK properties for entity enrichment
        tsk_properties = {}
        if Config.NEO4J_ENABLE_TSK_ENRICHMENT and felt_state:
            tsk_properties = {
                'polyvagal_state': felt_state.get('polyvagal_state', 'unknown'),
                'urgency_level': felt_state.get('urgency_level', 0.0),
                'self_distance': felt_state.get('self_distance', 0.5),
                'v0_energy': felt_state.get('v0_energy', 0.5),
                'satisfaction': felt_state.get('satisfaction', 0.5)
            }

        # Store user name
        if enriched_entities.get('user_name'):
            name = enriched_entities['user_name']
            self.knowledge_graph.create_entity(
                entity_type='Person',
                entity_value=name,
                user_id=self.user['user_id'],
                properties=tsk_properties
            )

        # Store family members with relationships
        if enriched_entities.get('family_members'):
            user_name = enriched_entities.get('user_name', 'User')
            for member in enriched_entities['family_members']:
                member_name = member.get('name')
                relationship = member.get('relationship', 'RELATED_TO')

                # Create member entity
                self.knowledge_graph.create_entity(
                    entity_type='Person',
                    entity_value=member_name,
                    user_id=self.user['user_id'],
                    properties=tsk_properties
                )

                # Create relationship (HAS_DAUGHTER, HAS_SON, etc.)
                rel_type = f"HAS_{relationship.upper()}" if relationship else "HAS_FAMILY_MEMBER"
                self.knowledge_graph.create_entity_relationship(
                    from_entity_value=user_name,
                    to_entity_value=member_name,
                    rel_type=rel_type,
                    user_id=self.user['user_id'],
                    properties={'confidence': member.get('confidence', 0.9)}
                )

        # Store friends
        if enriched_entities.get('friends'):
            user_name = enriched_entities.get('user_name', 'User')
            for friend_name in enriched_entities['friends']:
                # Create friend entity
                self.knowledge_graph.create_entity(
                    entity_type='Person',
                    entity_value=friend_name,
                    user_id=self.user['user_id'],
                    properties=tsk_properties
                )

                # Create HAS_FRIEND relationship
                self.knowledge_graph.create_entity_relationship(
                    from_entity_value=user_name,
                    to_entity_value=friend_name,
                    rel_type='HAS_FRIEND',
                    user_id=self.user['user_id']
                )

        # Store locations
        if enriched_entities.get('locations'):
            for location in enriched_entities['locations']:
                self.knowledge_graph.create_entity(
                    entity_type='Place',
                    entity_value=location,
                    user_id=self.user['user_id'],
                    properties=tsk_properties
                )

        # Store preferences
        if enriched_entities.get('preferences'):
            for pref_key, pref_value in enriched_entities['preferences'].items():
                self.knowledge_graph.create_entity(
                    entity_type='Preference',
                    entity_value=f"{pref_key}: {pref_value}",
                    user_id=self.user['user_id'],
                    properties=tsk_properties
                )

        # Store facts
        if enriched_entities.get('facts'):
            for fact in enriched_entities['facts']:
                self.knowledge_graph.create_entity(
                    entity_type='Fact',
                    entity_value=fact,
                    user_id=self.user['user_id'],
                    properties=tsk_properties
                )

    def _get_top_organs(self, organ_results: dict, k: int = 3) -> list:
        """Get top K organs by activation."""
        organ_scores = {}
        for organ_name, organ_result in organ_results.items():
            if hasattr(organ_result, 'coherence'):
                organ_scores[organ_name] = organ_result.coherence
            elif isinstance(organ_result, dict) and 'coherence' in organ_result:
                organ_scores[organ_name] = organ_result['coherence']

        sorted_organs = sorted(organ_scores.items(), key=lambda x: x[1], reverse=True)
        return [organ for organ, score in sorted_organs[:k]]

    def display_result(self, result: dict):
        """Display processing result based on current mode."""
        felt_states = result.get('felt_states', {})

        print("\n" + "-"*80)

        # Always show emission
        if self.settings['show_emission']:
            emission_text = felt_states.get('emission_text', '(no emission)')
            print(f"💬 Emission:\n   {emission_text}")

        # Show confidence
        if self.settings['show_confidence']:
            confidence = felt_states.get('emission_confidence', 0.0)
            path = felt_states.get('emission_path', 'unknown')
            print(f"\n📊 Confidence: {confidence:.3f} (path: {path})")

        # Show nexuses
        if self.settings['show_nexuses']:
            nexus_count = felt_states.get('emission_nexus_count', 0)
            transduction_trajectory = felt_states.get('transduction_trajectory', [])

            print(f"\n🔗 Nexuses: {nexus_count}")

            if transduction_trajectory and len(transduction_trajectory) > 0:
                final_state = transduction_trajectory[-1]
                nexus_type = final_state.get('current_type', 'Unknown')
                domain = final_state.get('domain', 'Unknown')
                print(f"   Dominant: {nexus_type} ({domain})")

        # Show organs
        if self.settings['show_organs']:
            organ_coherences = felt_states.get('organ_coherences', {})
            active_organs = [k for k, v in organ_coherences.items() if v > 0.1]

            print(f"\n🧬 Active Organs ({len(active_organs)}/11):")
            for organ in sorted(active_organs):
                coherence = organ_coherences[organ]
                print(f"   {organ}: {coherence:.3f}")

            # Key organ metrics
            if 'BOND_self_distance' in felt_states:
                print(f"\n   BOND self-distance: {felt_states['BOND_self_distance']:.3f}")
            if 'NDAM_urgency_level' in felt_states:
                print(f"   NDAM urgency: {felt_states['NDAM_urgency_level']:.3f}")
            if 'EO_polyvagal_state' in felt_states:
                print(f"   EO polyvagal: {felt_states['EO_polyvagal_state']}")

        # Show transduction trajectory
        if self.settings['show_transduction']:
            transduction_trajectory = felt_states.get('transduction_trajectory', [])

            if transduction_trajectory:
                print(f"\n🔄 Transduction Trajectory ({len(transduction_trajectory)} states):")
                for i, state in enumerate(transduction_trajectory, 1):
                    nexus_type = state.get('current_type', 'Unknown')
                    mechanism = state.get('transition_mechanism', 'none')
                    mutual_sat = state.get('mutual_satisfaction', 0.0)
                    is_crisis = state.get('is_crisis', False)
                    crisis_marker = "⚠️" if is_crisis else "✅"
                    print(f"   {i}. {crisis_marker} {nexus_type} ({mechanism}, sat={mutual_sat:.3f})")

        # Show V0 convergence
        if self.settings['show_v0']:
            v0_initial = felt_states.get('v0_energy_initial', 1.0)
            v0_final = felt_states.get('v0_energy_final', 0.0)
            cycles = felt_states.get('convergence_cycles', 0)
            kairos = felt_states.get('kairos_detected', False)

            print(f"\n🌀 V0 Convergence:")
            print(f"   Initial: {v0_initial:.3f} → Final: {v0_final:.3f}")
            print(f"   Descent: {v0_initial - v0_final:.3f} over {cycles} cycles")
            print(f"   Kairos: {'✅ Detected' if kairos else '❌ Not detected'}")

        # Show hybrid information (if enabled and available)
        if Config.HYBRID_ENABLED and 'hybrid' in result:
            hybrid_data = result['hybrid']
            print(f"\n🆕 Hybrid Superject:")
            print(f"   LLM weight: {hybrid_data['llm_weight']:.2f}")
            print(f"   LLM confidence: {hybrid_data['llm_confidence']:.3f}")
            print(f"   Similar moments: {hybrid_data['similar_moments_count']}")
            if self.settings['show_organs']:  # Show LLM response in detailed/debug modes
                llm_response = hybrid_data['llm_response']
                if len(llm_response) > 100:
                    print(f"   LLM scaffold: {llm_response[:100]}...")
                else:
                    print(f"   LLM scaffold: {llm_response}")

        print("-"*80 + "\n")

    def _collect_feedback(self, turn_id: int, user_input: str, result: dict):
        """Collect user feedback for this emission."""
        felt_states = result.get('felt_states', {})
        emission = felt_states.get('emission_text', '(no emission)')
        confidence = felt_states.get('emission_confidence', 0.0)
        nexuses = felt_states.get('emission_nexus_count', 0)

        print("\n📊 Rate this response:")
        print("  [1] ⭐ Excellent  [2] 👍 Helpful  [3] 👎 Not Helpful  [Enter] Skip")

        rating_input = input("Rating: ").strip()

        rating_map = {
            '1': 'excellent',
            '2': 'helpful',
            '3': 'not_helpful'
        }

        if rating_input in rating_map:
            rating = rating_map[rating_input]
            comment = None
            tone_notes = None

            # Ask for comment if not helpful
            if rating == 'not_helpful':
                comment = input("What would have been more helpful? (optional): ").strip() or None

            # Ask for tone notes if excellent (to capture what's working)
            if rating == 'excellent':
                tone_notes = input("What felt good about this? (optional): ").strip() or None

            # Record feedback
            self.feedback_collector.record_rating(
                user_id=self.user['user_id'],
                session_id=self.session_id,
                turn_id=turn_id,
                user_input=user_input,
                emission=emission,
                rating=rating,
                comment=comment,
                tone_notes=tone_notes,
                metadata={
                    'confidence': confidence,
                    'nexuses': nexuses,
                    'mode': self.mode,
                    'strategy': felt_states.get('emission_strategy', 'unknown')
                }
            )

            print("✅ Feedback recorded. Thank you!\n")

            # Show updated stats
            user_stats = self.feedback_collector.get_user_feedback_stats(self.user['user_id'])
            if user_stats['total_ratings'] > 0:
                print(f"   Your helpful rate: {user_stats['helpful_rate']*100:.1f}% ({user_stats['total_ratings']} ratings)")
                if user_stats['excellent_rate'] > 0:
                    print(f"   Excellent rate: {user_stats['excellent_rate']*100:.1f}%")
                print()

    def run(self):
        """Run interactive session loop."""
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()

                # 🌀 Multi-line input mode (Nov 15, 2025)
                # If input starts with >>> enter multi-line mode
                if user_input == ">>>":
                    print("   (Multi-line mode - paste your text, then type >>> on new line to finish)")
                    lines = []
                    while True:
                        line = input("... ")
                        if line.strip() == ">>>":
                            break
                        lines.append(line)
                    user_input = "\n".join(lines).strip()
                    if not user_input:
                        print("   (empty input - skipping)")
                        continue
                    print(f"\n✓ Received {len(user_input)} chars")

                # Handle empty input (robust multi-check - Nov 14, 2025)
                if not user_input or len(user_input) == 0 or user_input.isspace():
                    print("   (empty input - skipping)")
                    continue

                # Handle commands
                if user_input.startswith('/'):
                    if user_input == '/exit':
                        print("\n👋 Ending session...")
                        self._save_session_and_cleanup()
                        print("Goodbye!")
                        break
                    elif user_input == '/help':
                        self.show_help()
                        continue
                    elif user_input == '/mode':
                        self.change_mode()
                        continue
                    elif user_input == '/history':
                        self.show_history()
                        continue
                    elif user_input == '/save':
                        self.save_conversation()
                        continue
                    # 🌀 Phase 1.7: New commands (Nov 14, 2025)
                    elif user_input == '/identity':
                        self.cmd_identity()
                        continue
                    elif user_input == '/stats':
                        self.cmd_stats()
                        continue
                    elif user_input == '/projects':
                        self.cmd_projects()
                        continue
                    elif user_input == '/remember':
                        self.cmd_remember()
                        continue
                    elif user_input == '/traces':
                        self.cmd_traces()
                        continue
                    elif user_input == '/insights':
                        self.cmd_insights()
                        continue
                    elif user_input == '/notes':
                        self.cmd_notes()
                        continue
                    elif user_input == '/patterns':
                        self.cmd_patterns()
                        continue
                    elif user_input == '/trajectory':
                        self.cmd_trajectory()
                        continue
                    else:
                        print(f"❌ Unknown command: {user_input}")
                        print("   Type /help for available commands")
                        continue

                # 🌀 Phase 1.9: Continuous Reflection Mode (Nov 14, 2025)
                # For long, complex inputs, offer multi-layered processing

                # Process first layer
                result = self.process_input(user_input)

                # Store in history
                self.conversation_history.append({
                    'turn': len(self.conversation_history) + 1,
                    'user': user_input,
                    'result': result,
                    'timestamp': datetime.now().isoformat()
                })

                # Display result
                self.display_result(result)

                # Check if continuous reflection is warranted
                detection_metrics = self.detect_continuous_reflection_need(user_input, result)

                if detection_metrics['triggered']:
                    # Display metrics summary
                    print("\n🌀 CONTINUOUS REFLECTION MODE DETECTED")
                    print(f"   Input: {detection_metrics['input_length']} chars")
                    print(f"   Complexity: {detection_metrics['complexity_score']:.2f}")
                    print(f"   Semantic fields: {detection_metrics['semantic_fields_count']}")
                    print(f"   Nexuses: {detection_metrics['nexus_count']}")
                    print(f"   Self zone: {detection_metrics['self_zone']}")

                    trauma = detection_metrics['trauma_metrics']
                    if trauma['trauma_present']:
                        print(f"   ⚠️  Trauma markers:")
                        print(f"      BOND self-distance: {trauma['bond_self_distance']:.2f}")
                        print(f"      EO polyvagal: {trauma['eo_polyvagal_state']}")
                        print(f"      NDAM urgency: {trauma['ndam_urgency']:.2f}")

                    print("\n   Would you like additional perspectives? (y/n/number 2-3): ", end='')

                    reflection_input = input().strip().lower()

                    if reflection_input in ['y', 'yes', '2', '3']:
                        # Determine number of additional layers
                        if reflection_input in ['2', '3']:
                            num_layers = int(reflection_input)
                        else:
                            num_layers = 2  # Default: 2 additional layers (3 total)

                        print(f"\n🌀 Generating {num_layers} additional perspective(s)...\n")

                        # Generate additional layers (skip first layer since we already processed it)
                        all_layers = self.generate_continuous_reflections(user_input, num_layers + 1)
                        additional_layers = all_layers[1:]  # Skip first layer

                        for layer in additional_layers:
                            layer_num = layer['layer_num']
                            config = layer['config']
                            layer_result = layer['result']

                            print(f"\n{'='*80}")
                            print(f"📍 Layer {layer_num}/{num_layers + 1}: {config['name']}")
                            print(f"   {config['description']}")
                            print('='*80 + "\n")

                            # Display this layer's result
                            self.display_result(layer_result)

                            # Extract layer metrics for tracking
                            layer_felt_states = layer_result.get('felt_states', {})
                            layer_metrics = {
                                'nexus_count': layer_felt_states.get('emission_nexus_count', 0),
                                'confidence': layer_felt_states.get('emission_confidence', 0.0),
                                'v0_energy': layer_felt_states.get('v0_final_energy', 0.5),
                                'self_zone': layer_felt_states.get('self_zone', 1),
                                'semantic_fields': len(layer_felt_states.get('semantic_fields', []))
                            }

                            # Store in history with full metrics
                            self.conversation_history.append({
                                'turn': len(self.conversation_history) + 1,
                                'user': f"[Layer {layer_num}] {user_input}",
                                'result': layer_result,
                                'timestamp': datetime.now().isoformat(),
                                'layer_num': layer_num,
                                'layer_config': config,
                                'layer_metrics': layer_metrics,
                                'continuous_reflection': True
                            })

                        # Store overall reflection session metadata
                        reflection_summary = {
                            'num_layers': num_layers + 1,
                            'detection_metrics': detection_metrics,
                            'timestamp': datetime.now().isoformat(),
                            'input_preview': user_input[:100] + '...' if len(user_input) > 100 else user_input
                        }

                        print(f"\n{'='*80}")
                        print(f"✅ Continuous reflection complete ({num_layers + 1} layers)")
                        print(f"   Overall complexity: {detection_metrics['complexity_score']:.2f}")
                        print("   Which perspective resonated most with you?")
                        print('='*80 + "\n")

                # Collect feedback (optional, based on mode)
                if self.mode in ['standard', 'detailed', 'debug']:
                    self._collect_feedback(
                        turn_id=len(self.conversation_history),
                        user_input=user_input,
                        result=result
                    )

            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupted. Type /exit to end session or continue conversing.")
                continue
            except Exception as e:
                print(f"\n❌ Error: {e}")
                import traceback
                traceback.print_exc()
                continue

    def show_help(self):
        """Show help message."""
        print("\n" + "="*80)
        print("📖 HELP")
        print("="*80)
        print("\nCommands:")
        print("  /help     - Show this help message")
        print("  /mode     - Change display mode (simple/standard/detailed/debug)")
        print("  /history  - Show conversation history")
        print("  /save     - Save conversation to JSON file")
        print("  /exit     - Exit interactive mode")
        print("\n📝 Input:")
        print("  >>>       - Multi-line mode (paste long text, end with >>> on new line)")
        print("\n🌀 Organism Commands:")
        print("  /identity - Show mycelial identity (subjective aim + projects)")
        print("  /stats    - Learning statistics (R-matrix, hebbian, families)")
        print("  /projects - Active projects summary")
        print("\n💭 Memory Commands:")
        print("  /remember - Retrieve similar past moments (hybrid mode)")
        print("  /traces   - Show mycelium traces (notes, insights, projects)")
        print("  /insights - Show insights only")
        print("  /notes    - Show notes only")
        print("\n👤 User Commands:")
        print("  /patterns   - Show transformation patterns (your learning)")
        print("  /trajectory - Show felt-state trajectory (your journey)")
        print("\nDisplay Modes:")
        print("  simple   - Just emission text")
        print("  standard - Emission + confidence + nexuses (default)")
        print("  detailed - + organ details + transduction trajectory")
        print("  debug    - + V0 convergence details")
        print("="*80 + "\n")

    def change_mode(self):
        """Change display mode interactively."""
        print("\n📊 Available modes:")
        print("  1. simple   - Just emission text")
        print("  2. standard - Emission + confidence + nexuses")
        print("  3. detailed - + organ details + transduction")
        print("  4. debug    - + V0 convergence")

        choice = input("\nSelect mode (1-4): ").strip()

        mode_map = {'1': 'simple', '2': 'standard', '3': 'detailed', '4': 'debug'}
        new_mode = mode_map.get(choice)

        if new_mode:
            self.mode = new_mode
            self.settings = self.display_settings[new_mode]
            print(f"✅ Display mode changed to: {new_mode}\n")
        else:
            print("❌ Invalid choice. Mode unchanged.\n")

    def show_history(self):
        """Show conversation history."""
        print("\n" + "="*80)
        print("📜 CONVERSATION HISTORY")
        print("="*80)

        if not self.conversation_history:
            print("\n(No messages yet)\n")
            return

        for entry in self.conversation_history:
            turn = entry['turn']
            user_msg = entry['user']
            felt_states = entry['result'].get('felt_states', {})
            emission = felt_states.get('emission_text', '(no emission)')
            confidence = felt_states.get('emission_confidence', 0.0)

            print(f"\nTurn {turn}:")
            print(f"  You: {user_msg}")
            print(f"  DAE: {emission} (conf={confidence:.3f})")

        print("="*80 + "\n")

    def save_conversation(self):
        """Save conversation history to JSON file."""
        if not self.conversation_history:
            print("❌ No conversation to save.\n")
            return

        # Prepare save data
        save_data = {
            'session_id': self.session_id,
            'mode': self.mode,
            'timestamp_start': self.conversation_history[0]['timestamp'],
            'timestamp_end': self.conversation_history[-1]['timestamp'],
            'turn_count': len(self.conversation_history),
            'conversation': self.conversation_history
        }

        # Save to file
        output_dir = Config.RESULTS_DIR / "interactive_sessions"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"session_{self.session_id}.json"

        with open(output_file, 'w') as f:
            json.dump(save_data, f, indent=2, default=str)

        print(f"✅ Conversation saved to: {output_file}\n")

    def _save_session_and_cleanup(self):
        """Save user state and update statistics before exiting."""
        # Update session history in user state
        self.user_state['session_history'].append({
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'turns': len(self.conversation_history)
        })
        self.user_state['last_session'] = self.session_id

        # Update feedback stats
        user_stats = self.feedback_collector.get_user_feedback_stats(self.user['user_id'])
        self.user_registry.update_feedback_stats(
            self.user['user_id'],
            helpful_rate=user_stats['helpful_rate'],
            excellent_rate=user_stats['excellent_rate']
        )

        # Save user state
        self.user_registry.save_user_state(self.user['user_id'], self.user_state)

        # Update user registry stats
        self.user_registry.update_user_stats(self.user['user_id'], len(self.conversation_history))

        print(f"\n💾 Session saved:")
        print(f"   Turns: {len(self.conversation_history)}")
        print(f"   Total turns (all sessions): {self.user['total_turns'] + len(self.conversation_history)}")
        if user_stats['total_ratings'] > 0:
            print(f"   Helpful rate: {user_stats['helpful_rate']*100:.1f}%")

    # 🌀 Phase 1.7: Command implementations (Nov 14, 2025)

    def cmd_identity(self):
        """Show mycelial identity (subjective aim + projects)."""
        if not self.identity_tracker:
            print("\n❌ Identity tracker not available\n")
            return
        print("\n")
        print(self.identity_tracker.get_identity_summary())

    def cmd_stats(self):
        """Show learning statistics."""
        print("\n" + "="*70)
        print("Learning Statistics")
        print("="*70)
        if not hasattr(self.organism, 'conversational_r_matrix'):
            print("\n⚠️  R-Matrix not available in organism\n")
            return
        r_matrix = self.organism.conversational_r_matrix
        print(f"\n🌀 Conversational Organs R-Matrix:")
        print(f"   Updates: {r_matrix.update_count}")
        print(f"   Organs: {', '.join(r_matrix.organs)}")
        print(f"\n   Strongest Couplings:")
        for organ1, organ2, strength in r_matrix.get_strongest_couplings(top_k=5):
            print(f"      {organ1} + {organ2} = {strength:.3f}")
        if hasattr(self.organism, 'hebbian_memory'):
            hebbian = self.organism.hebbian_memory
            print(f"\n📊 Hebbian Learning:")
            print(f"   Total updates: {hebbian.update_count}")
            print(f"   Successes: {hebbian.success_count}")
            print(f"   Failures: {hebbian.failure_count}")
            print(f"   Success rate: {hebbian.success_rate*100:.1f}%")
            print(f"   Global confidence: {hebbian.get_global_confidence():.3f}")
        print("="*70 + "\n")

    def cmd_projects(self):
        """Show active projects summary."""
        if not self.identity_tracker:
            print("\n❌ Identity tracker not available\n")
            return
        print("\n")
        print(self.identity_tracker.get_project_summary())

    def cmd_patterns(self):
        """Show transformation patterns for this user."""
        if not self.user_superject_learner:
            print("\n❌ User superject learner not available\n")
            return
        profile = self.user_superject_learner.get_or_create_profile(self.user['user_id'])
        print("\n" + "="*70)
        print(f"Transformation Patterns for {self.user['username']}")
        print("="*70)
        patterns = list(profile.transformation_patterns.values())
        if not patterns:
            print("\n   No transformation patterns recorded yet.")
            print("   Patterns emerge after 10+ conversations.\n")
            return
        print(f"\n   Total patterns: {len(patterns)}\n")
        for i, pattern in enumerate(patterns[:10], 1):
            print(f"   {i}. {pattern.pattern_id}")
            print(f"      Frequency: {pattern.frequency}")
            print(f"      Success rate: {pattern.success_rate*100:.1f}%")
            print(f"      Tone: {pattern.tone}, Length: {pattern.preferred_length}\n")
        print("="*70 + "\n")

    def cmd_trajectory(self):
        """Show felt-state trajectory for this user."""
        if not self.user_superject_learner:
            print("\n❌ User superject learner not available\n")
            return
        profile = self.user_superject_learner.get_or_create_profile(self.user['user_id'])
        print("\n" + "="*70)
        print(f"Felt-State Trajectory for {self.user['username']}")
        print("="*70)
        trajectory = profile.felt_trajectory
        if not trajectory:
            print("\n   No trajectory data recorded yet.\n")
            return
        print(f"\n   Total snapshots: {len(trajectory)}")
        print(f"   Recent trajectory (last 10):\n")
        for snapshot in trajectory[-10:]:
            print(f"   📍 {snapshot.timestamp}")
            print(f"      Zone: {snapshot.zone}, Polyvagal: {snapshot.polyvagal_state}")
            print(f"      Satisfaction: {snapshot.satisfaction:.2f}")
            print(f"      Organs: {', '.join(snapshot.active_organs[:3])}\n")
        print("="*70 + "\n")

    def cmd_remember(self):
        """Retrieve similar past moments (hybrid mode)."""
        if not Config.HYBRID_ENABLED or not self.memory_retrieval:
            print("\n❌ Hybrid mode not enabled. Set HYBRID_ENABLED = True in config.py\n")
            return
        print("\n" + "="*70)
        print("Memory Retrieval (Hybrid Superject)")
        print("="*70)
        print("\n   💡 To retrieve similar moments:")
        print("   1. Have a conversation first")
        print("   2. Use /remember after a response")
        print("   3. DAE will find similar past moments\n")
        print("   Feature: Retrieves similar felt-states from your history")
        print("   Uses: 57D organ signatures for similarity matching\n")
        print("="*70 + "\n")

    def cmd_traces(self):
        """Show mycelium traces (notes, insights, projects)."""
        if not self.identity_tracker:
            print("\n❌ Identity tracker not available\n")
            return
        print("\n" + "="*70)
        print("Mycelium Traces")
        print("="*70)
        traces = self.identity_tracker.get_all_traces()
        if not traces:
            print("\n   No traces recorded yet.\n")
            return
        print(f"\n   Total traces: {len(traces)}\n")
        for trace in traces[-20:]:
            trace_type = trace.get('type', 'unknown')
            content = trace.get('content', '')
            timestamp = trace.get('timestamp', 'unknown')
            icon = "📝" if trace_type == "note" else "💡" if trace_type == "insight" else "📂"
            print(f"   {icon} [{trace_type}] {timestamp}")
            print(f"      {content[:100]}...\n" if len(content) > 100 else f"      {content}\n")
        print("="*70 + "\n")

    def cmd_insights(self):
        """Show insights only (filtered traces)."""
        if not self.identity_tracker:
            print("\n❌ Identity tracker not available\n")
            return
        print("\n" + "="*70)
        print("Insights")
        print("="*70)
        traces = self.identity_tracker.get_traces_by_type('insight')
        if not traces:
            print("\n   No insights recorded yet.\n")
            return
        print(f"\n   Total insights: {len(traces)}\n")
        for trace in traces[-15:]:
            print(f"   💡 {trace.get('timestamp', 'unknown')}")
            print(f"      {trace.get('content', '')}\n")
        print("="*70 + "\n")

    def cmd_notes(self):
        """Show notes only (filtered traces)."""
        if not self.identity_tracker:
            print("\n❌ Identity tracker not available\n")
            return
        print("\n" + "="*70)
        print("Notes")
        print("="*70)
        traces = self.identity_tracker.get_traces_by_type('note')
        if not traces:
            print("\n   No notes recorded yet.\n")
            return
        print(f"\n   Total notes: {len(traces)}\n")
        for trace in traces[-15:]:
            print(f"   📝 {trace.get('timestamp', 'unknown')}")
            print(f"      {trace.get('content', '')}\n")
        print("="*70 + "\n")


def main():
    """Main entry point for interactive mode."""
    import argparse

    parser = argparse.ArgumentParser(description='DAE_HYPHAE_1 Interactive Mode')
    parser.add_argument(
        '--mode',
        choices=['simple', 'standard', 'detailed', 'debug'],
        default='standard',
        help='Display mode (default: standard)'
    )
    parser.add_argument(
        '--user',
        type=str,
        default=None,
        help='User ID for returning users'
    )
    parser.add_argument(
        '--username',
        type=str,
        default=None,
        help='Username for new user creation'
    )

    args = parser.parse_args()

    try:
        session = InteractiveSession(
            mode=args.mode,
            user_id=args.user,
            username=args.username
        )
        session.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Session interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
