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

# 🌀 Whiteheadian Entity Ontology Integration (Nov 17, 2025)
from knowledge_base.entity_ontology_validator import get_default_validator
from persona_layer.entity_horizon import EntityHorizon
from persona_layer.entity_salience_tracker import EntitySalienceTracker
from persona_layer.felt_satisfaction_inference import get_default_inferencer

# 🌀 Phase 1.7: Command expansion imports (Nov 14, 2025)
from monitoring.mycelial_identity_tracker import MycelialIdentityTracker
from persona_layer.user_superject_learner import UserSuperjectLearner

# 🌀 Phase 1.8: Entity extraction imports (Nov 14, 2025)
from persona_layer.memory_intent_detector import MemoryIntentDetector
from persona_layer.entity_extractor import EntityExtractor

# 🌀 Phase 3: Transductive felt entity filtering imports (Nov 18, 2025 - Dual Memory Phase 3 Refactor)
from persona_layer.transductive_felt_entity_filter import get_transductive_felt_entity_filter
from persona_layer.satisfaction_fingerprinting import SatisfactionFingerprintClassifier

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
                            self.user = self.user_registry.get_user(user_id)
                        else:
                            print(f"⚠️  Invalid selection: {user_input} (must be 1-{len(users)})")
                            self.user = None
                    else:
                        # Treat as user_id string
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

        # 🌀 Phase 1 Entity Continuity: Conversation history buffer (Nov 17, 2025)
        self.max_history_turns = 10  # Keep last 10 turns for entity continuity

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

        # 🌀 Phase 3B: Initialize NEXUS-first entity extraction (Nov 18, 2025)
        # Neighbor prehension + 4-gate cascade + multi-word detection
        try:
            from persona_layer.entity_neighbor_prehension import EntityNeighborPrehension
            # Will initialize entity_organ_tracker later (after wrapper is ready)
            self.entity_neighbor_prehension = EntityNeighborPrehension(entity_tracker=None)
            print("✅ NEXUS-first entity extraction ready (neighbor prehension + 4-gate cascade)")
        except Exception as e:
            print(f"⚠️  NEXUS entity extraction initialization failed: {e}")
            self.entity_neighbor_prehension = None

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

        # 🌀 Whiteheadian Entity Ontology Infrastructure (Nov 17, 2025)
        # Initialize entity validation, horizon, and salience tracking
        print("\n🌀 Initializing Whiteheadian entity continuity...")
        try:
            # Entity ontology validator (stopwords, categories, process philosophy)
            self.entity_validator = get_default_validator()

            # Entity horizon (morpheable 100-500 based on field coherence)
            self.entity_horizon = EntityHorizon()

            # 🌀 Phase 3: Transductive felt entity filter (Nov 18, 2025 - Dual Memory Phase 3 Refactor)
            # 4-layer filtering: BOND IFS Gate → SELF Matrix → Salience + Temporal Decay → Satisfaction + Regime
            self.transductive_felt_filter = get_transductive_felt_entity_filter(
                enable_layer0=True,  # BOND IFS parts gate
                enable_layer1=True,  # SELF Matrix zone gating
                enable_layer2=False,  # Salience + temporal decay (disabled for now - needs full prehension)
                enable_layer3=False   # Satisfaction fingerprinting (disabled for now - needs trace)
            )
            self.satisfaction_classifier = SatisfactionFingerprintClassifier()
            print("✅ Transductive felt entity filter initialized (Phase 3 - 4-layer architecture)")
            print("   • Layer 0: BOND IFS Parts Gate (120+ keywords)")
            print("   • Layer 1: SELF Matrix Zone Gating (5 zones)")
            print("   • Layer 2: Salience + Temporal Decay (disabled pending prehension)")
            print("   • Layer 3: Satisfaction + Regime (disabled pending trace)")

            # Entity salience tracker (3-tier EMA decay)
            self.entity_salience_tracker = EntitySalienceTracker(
                storage_path=f"persona_layer/state/entity_salience_{self.user['user_id']}.json",
                staleness_threshold=300  # 300 turns without mention
            )

            # Felt-satisfaction inferencer (non-invasive urgency from organism)
            self.satisfaction_inferencer = get_default_inferencer()

            # Entity continuity ready
            print(f"✅ Whiteheadian entity continuity ready")
            print(f"   • Validator: {len(self.entity_validator.stopwords)} stopwords blacklist")
            print(f"   • Horizon: Adaptive 100-500 entities (field-coherence gated)")
            print(f"   • Salience: 3-tier EMA decay (Local/Family/Global)")
            print(f"   • Satisfaction: Non-invasive felt-state inference")
        except Exception as e:
            print(f"⚠️  Whiteheadian entity continuity initialization failed: {e}")
            print("   Falling back to basic entity extraction")
            self.entity_validator = None
            self.entity_horizon = None
            self.entity_salience_tracker = None
            self.satisfaction_inferencer = None

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
                    # Pass to organism's emission generator (if it exists)
                    if self.organism and hasattr(self.organism, 'emission_generator') and self.organism.emission_generator:
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
                self.felt_guided_llm = None
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
        print("  /refresh  - Reload organism learning state (Whiteheadian prehension)")
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

        # 🌀 Phase 1 Entity Continuity Fix: Neo4j Pre-Querying (Nov 17, 2025)
        # PULL entity context BEFORE pattern matching to enable pronoun resolution
        # and implicit entity references ("she" → Emma, "our project" → DAEDALEA)
        # 🌀 Phase 1 Performance: Parallel Query Execution (Nov 17, 2025)
        # Execute 3 strategies in parallel for 2× speedup
        neo4j_entities = []

        if self.knowledge_graph and self.knowledge_graph.driver:
            try:
                from concurrent.futures import ThreadPoolExecutor, as_completed

                # Execute queries in parallel (2× speedup)
                with ThreadPoolExecutor(max_workers=3) as executor:
                    # Strategy 1: Get entities from recent conversation history (last 60 minutes)
                    future_recent = executor.submit(
                        self.knowledge_graph.get_recent_entities,
                        user_id=self.user['user_id'],
                        limit=20,
                        time_window_minutes=60
                    )

                    # Strategy 2: Fuzzy match current input against stored entities
                    future_fuzzy = executor.submit(
                        self.knowledge_graph.fuzzy_match_entities,
                        text=user_input,
                        user_id=self.user['user_id'],
                        threshold=0.6
                    )

                    # Strategy 3: Get entities from last N turns of THIS session (local, instant)
                    session_entities = self.get_recent_session_entities(n_turns=5)

                    # Collect results with timeout protection (500ms each)
                    recent_entities = future_recent.result(timeout=0.5)
                    fuzzy_entities = future_fuzzy.result(timeout=0.5)

                # Combine all sources
                neo4j_entities = recent_entities + fuzzy_entities + session_entities

                # Deduplicate by (name, type) tuple
                seen = set()
                unique_entities = []
                for entity in neo4j_entities:
                    key = (entity.get('name', entity.get('entity_value')), entity.get('type', entity.get('entity_type')))
                    if key not in seen and key[0]:  # Ensure name exists
                        seen.add(key)
                        unique_entities.append(entity)

                neo4j_entities = unique_entities

                if self.mode in ['detailed', 'debug'] and neo4j_entities:
                    print(f"   🔍 Neo4j pre-query found {len(neo4j_entities)} entities:")
                    for e in neo4j_entities[:5]:  # Show first 5
                        source = e.get('source', 'unknown')
                        print(f"      • {e.get('name', e.get('entity_value'))} ({e.get('type', e.get('entity_type'))}) [{source}]")

            except Exception as e:
                if self.mode in ['detailed', 'debug']:
                    error_type = "timeout" if "timeout" in str(e).lower() else "error"
                    print(f"   ⚠️ Neo4j pre-query {error_type}: {e}")
                neo4j_entities = []

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

        # Step 2: Try NEXUS-first entity extraction (Phase 3B - Nov 18, 2025)
        # Falls back to LLM EntityExtractor if NEXUS confidence is low
        nexus_entities = []
        word_occasions = []  # Phase 3B: For epoch learning trackers
        nexus_extraction_attempted = False

        if hasattr(self, 'entity_neighbor_prehension'):
            try:
                import time
                nexus_extraction_attempted = True

                # Time NEXUS extraction (for NexusVsLLMDecisionTracker)
                nexus_start = time.time()
                nexus_entities, word_occasions = self.entity_neighbor_prehension.extract_entities(
                    user_input,
                    return_word_occasions=True  # Phase 3B: Get word_occasions for trackers
                )
                nexus_time_ms = (time.time() - nexus_start) * 1000.0

                # Compute NEXUS confidence (max confidence across all entities)
                nexus_confidence = max([e.get('confidence_score', 0.0) for e in nexus_entities], default=0.0)

                # Store word_occasions in context for trackers (Phase 3B - Nov 18, 2025)
                context['word_occasions'] = word_occasions

                # Check if we got high-confidence entities from NEXUS
                high_confidence_nexus = [
                    e for e in nexus_entities
                    if e.get('confidence_score', 0.0) >= 0.7
                ]

                if high_confidence_nexus:
                    # Use NEXUS entities (LLM-free extraction!)
                    memory_intent_detected = True
                    context['pre_extraction_entities_nexus'] = high_confidence_nexus
                    context['nexus_extraction_used'] = True

                    # Store NEXUS metadata for NexusVsLLMDecisionTracker (Phase 3B)
                    context['nexus_confidence'] = nexus_confidence
                    context['nexus_entities'] = nexus_entities
                    context['extraction_time_ms'] = nexus_time_ms

                    # Convert to extracted_entities format for compatibility
                    extracted_entities = {
                        'timestamp': context.get('timestamp'),
                        'source_text': user_input,
                        'intent_type': intent_type
                    }

                    # Populate entity fields based on type
                    for entity in high_confidence_nexus:
                        entity_value = entity.get('entity_value')
                        entity_type = entity.get('entity_type')

                        if entity_type == 'Person':
                            if 'family_members' not in extracted_entities:
                                extracted_entities['family_members'] = []
                            extracted_entities['family_members'].append(entity_value)
                        elif entity_type == 'Place':
                            if 'places' not in extracted_entities:
                                extracted_entities['places'] = []
                            extracted_entities['places'].append(entity_value)
                        # Add more type mappings as needed

            except Exception as e:
                print(f"⚠️  NEXUS entity extraction failed: {e}")
                import traceback
                traceback.print_exc()
                nexus_extraction_attempted = False

        # Fallback to LLM EntityExtractor if NEXUS didn't provide high-confidence entities
        if not nexus_entities or not any(e.get('confidence_score', 0.0) >= 0.7 for e in nexus_entities):
            if self.entity_extractor:
                import time

                # Time LLM extraction (for comparison)
                llm_start = time.time()
                extracted_entities = self.entity_extractor.extract(
                    user_input,
                    intent_type=intent_type,  # Use detected intent type (or 'general')
                    context=intent_context  # Use context from detector (includes extracted_name if found)
                )
                llm_time_ms = (time.time() - llm_start) * 1000.0

                context['nexus_extraction_used'] = False

                # Store LLM metadata for NexusVsLLMDecisionTracker (Phase 3B)
                context['nexus_confidence'] = max([e.get('confidence_score', 0.0) for e in nexus_entities], default=0.0) if nexus_entities else 0.0
                context['nexus_entities'] = nexus_entities
                context['llm_entities'] = extracted_entities
                context['extraction_time_ms'] = llm_time_ms

                # Check if ANY entities were extracted
                if extracted_entities and any(k != 'timestamp' and k != 'source_text' and k != 'intent_type'
                                             and extracted_entities.get(k) for k in extracted_entities.keys()):
                    memory_intent_detected = True  # Mark that we found actual entities
                    context['pre_extraction_entities'] = extracted_entities

                # 🌀 Quick Win #7: Convert extracted entities to list format for entity-organ tracker
                # entity-organ tracker expects List[Dict[entity_value, entity_type]]
                extracted_entities_list = []
                for key, value in extracted_entities.items():
                    if key not in ['timestamp', 'source_text', 'intent_type'] and value:
                        # Infer entity type from key
                        entity_type = 'Unknown'
                        if key in ['user_name', 'name']:
                            entity_type = 'Person'
                        elif key in ['family_members', 'relationships']:
                            entity_type = 'Person'
                        elif key in ['preferences', 'likes', 'dislikes']:
                            entity_type = 'Preference'
                        elif key in ['facts', 'information']:
                            entity_type = 'Fact'
                        elif key in ['places', 'locations']:
                            entity_type = 'Place'

                        # Handle list values (like family_members)
                        if isinstance(value, list):
                            for item in value:
                                if isinstance(item, str):
                                    extracted_entities_list.append({
                                        'entity_value': item,
                                        'entity_type': entity_type
                                    })
                        elif isinstance(value, str):
                            extracted_entities_list.append({
                                'entity_value': value,
                                'entity_type': entity_type
                            })

                if extracted_entities_list:
                    # 🌀 Phase 3: OLD felt entity filter (DISABLED - Nov 18, 2025)
                    # Replaced by transductive felt entity filter POST-organism processing
                    # See lines ~770-810 for new 4-layer transductive filtering
                    context['current_turn_entities'] = extracted_entities_list

        # 🌀 Phase 1 Entity Continuity Fix: Merge Neo4j entities with pattern-matched (Nov 17, 2025)
        # Populate current_turn_entities even if pattern matching failed (enables "she" → Emma resolution)
        if 'current_turn_entities' not in context:
            context['current_turn_entities'] = []

        # Add Neo4j pre-queried entities
        for neo4j_entity in neo4j_entities:
            # Convert to expected format if needed
            entity_dict = {
                'entity_value': neo4j_entity.get('name', neo4j_entity.get('entity_value')),
                'entity_type': neo4j_entity.get('type', neo4j_entity.get('entity_type', 'Entity')),
                'source': neo4j_entity.get('source', 'neo4j'),
                'properties': neo4j_entity.get('properties', {})
            }

            # Check for duplicates before adding
            is_duplicate = False
            for existing in context['current_turn_entities']:
                if (existing.get('entity_value') == entity_dict['entity_value'] and
                    existing.get('entity_type') == entity_dict['entity_type']):
                    is_duplicate = True
                    break

            if not is_duplicate:
                context['current_turn_entities'].append(entity_dict)

        if self.mode in ['detailed', 'debug'] and context['current_turn_entities']:
            print(f"   📋 Total entities for organism: {len(context['current_turn_entities'])}")
            pattern_matched = sum(1 for e in context['current_turn_entities'] if e.get('source') not in ['neo4j', 'recent_query', 'fuzzy_match', 'session'])
            neo4j_sourced = len(context['current_turn_entities']) - pattern_matched
            if pattern_matched > 0:
                print(f"      • Pattern-matched: {pattern_matched}")
            if neo4j_sourced > 0:
                print(f"      • Neo4j/Session: {neo4j_sourced}")

        # 🌀 Nov 17, 2025: Populate entity_prehension for NEXUS organ
        # Convert current_turn_entities to entity_prehension format that NEXUS expects
        if context.get('current_turn_entities'):
            mentioned_entities = [
                {
                    'name': entity['entity_value'],
                    'type': entity.get('entity_type', 'person'),
                    'relationship': entity.get('relationship'),
                    'source': entity.get('source', 'explicit')
                }
                for entity in context['current_turn_entities']
            ]

            context['entity_prehension'] = {
                'entity_memory_available': len(mentioned_entities) > 0,
                'mentioned_entities': mentioned_entities,
                'user_name': self.user.get('username', 'User')
            }

        # 🌀 Phase 1.9: Load user's learned satisfaction baseline from superject (Nov 17, 2025)
        # This enables personalized wave protocols, humor calibration, and tone adaptation post-training
        user_satisfaction_baseline = None
        if self.user_superject_learner:
            try:
                user_superject = self.user_superject_learner.load_superject(self.user['user_id'])
                if user_superject and user_superject.turn_count >= 5:
                    # Only use learned baseline after 5+ turns (ensures enough data)
                    user_satisfaction_baseline = user_superject.satisfaction_baseline
                    if Config.INTERACTIVE_SHOW_SUPERJECT_LOAD and self.mode in ['detailed', 'debug']:
                        print(f"   📈 Using learned satisfaction baseline: {user_satisfaction_baseline:.3f} (from {user_superject.turn_count} turns)")
            except Exception as e:
                # Graceful degradation - if superject load fails, continue without it
                if self.mode in ['detailed', 'debug']:
                    print(f"   ⚠️  Superject load failed: {e}")

        # Step 1: Process through organism (12 organs)
        result = self.organism.process_text(
            user_input,
            context=context,
            enable_tsk_recording=self.enable_tsk_recording,
            enable_phase2=self.enable_phase2,
            user_id=self.user['user_id'],  # 🌀 Phase 1.6: User identity (Nov 14, 2025)
            username=self.user['username'],  # 🌀 Phase 1.6: Username for personalization (Nov 14, 2025)
            user_satisfaction=user_satisfaction_baseline  # 🌀 Phase 1.9: Personalized wave protocols (Nov 17, 2025)
        )

        # 🌀 Felt-Satisfaction Inference (Nov 17, 2025)
        # Infer mutual satisfaction from organism's felt-state (non-invasive)
        # Used to compute urgency_context for entity salience boosting
        urgency_context = 0.0  # Default neutral
        field_coherence = 0.5  # Default for horizon computation

        if self.satisfaction_inferencer:
            try:
                # Extract felt-state metrics from organism result
                felt_states = result.get('felt_states', {})
                organ_results = result.get('organ_results', {})

                # Compute field coherence (already in result, or compute from organs)
                field_coherence = felt_states.get('field_coherence', 0.5)
                if field_coherence == 0.0 and organ_results:
                    # Fallback: compute from organ coherences if available
                    coherences = [
                        getattr(organ_results.get(organ_name), 'coherence', 0.5)
                        for organ_name in organ_results.keys()
                    ]
                    if coherences:
                        import numpy as np
                        field_coherence = max(0.0, 1.0 - np.std(coherences))

                # Extract V0 energy descent
                v0_initial = felt_states.get('v0_energy_initial', 1.0)
                v0_final = felt_states.get('v0_energy_final', 0.5)

                # Kairos detection
                kairos_detected = felt_states.get('kairos_detected', False)

                # Emission quality
                emission_confidence = felt_states.get('emission_confidence', 0.5)
                emission_path = felt_states.get('emission_path', 'felt_guided_llm')

                # Active organs count
                active_organs = len(organ_results) if organ_results else 12

                # Infer satisfaction from felt-state
                satisfaction_metrics = self.satisfaction_inferencer.infer_satisfaction(
                    field_coherence=field_coherence,
                    v0_initial=v0_initial,
                    v0_final=v0_final,
                    kairos_detected=kairos_detected,
                    emission_confidence=emission_confidence,
                    emission_path=emission_path,
                    active_organs=active_organs
                )

                # Extract urgency context (inverse of satisfaction)
                urgency_context = self.satisfaction_inferencer.get_urgency_context(
                    satisfaction_metrics.inferred_satisfaction
                )

                # Store in result for visibility
                result['inferred_satisfaction'] = satisfaction_metrics.inferred_satisfaction
                result['satisfaction_tier'] = satisfaction_metrics.satisfaction_tier
                result['urgency_context'] = urgency_context

                if self.mode in ['detailed', 'debug']:
                    print(f"\n🌀 Felt-Satisfaction Inference:")
                    print(f"   Inferred satisfaction: {satisfaction_metrics.inferred_satisfaction:.3f}")
                    print(f"   Satisfaction tier: {satisfaction_metrics.satisfaction_tier}")
                    print(f"   Urgency context: {urgency_context:.3f} (for entity salience)")
                    print(f"   Field coherence: {field_coherence:.3f}")

            except Exception as e:
                if self.mode == 'debug':
                    print(f"⚠️  Felt-satisfaction inference failed: {e}")
                # Continue with default urgency

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

                # 🌀 Phase 3: Apply transductive felt entity filter (Nov 18, 2025 - Dual Memory Phase 3 Refactor)
                # 4-layer filtering: BOND IFS Gate → SELF Matrix → Salience + Temporal Decay → Satisfaction + Regime
                if hasattr(self, 'transductive_felt_filter') and self.transductive_felt_filter and enriched_entities:
                    pre_filter_count = len(enriched_entities)

                    # Get BOND result and zone from felt_state
                    bond_result = organ_results.get('BOND') if organ_results else None

                    # Derive zone from BOND self_distance using SELF Matrix classification
                    zone = None
                    if bond_result and hasattr(bond_result, 'self_distance'):
                        # Use SELF Matrix to classify zone
                        from persona_layer.self_matrix_governance import SELFZoneState
                        self_distance = bond_result.self_distance

                        # Map self_distance to zone (SELF Matrix boundaries)
                        if self_distance < 0.15:
                            zone_id = 1  # Core SELF Orbit
                        elif self_distance < 0.25:
                            zone_id = 2  # Inner Relational
                        elif self_distance < 0.35:
                            zone_id = 3  # Symbolic Threshold
                        elif self_distance < 0.60:
                            zone_id = 4  # Shadow/Compost
                        else:
                            zone_id = 5  # Exile/Collapse

                        # Create zone state object
                        zone_names = {
                            1: "Core SELF Orbit",
                            2: "Inner Relational",
                            3: "Symbolic Threshold",
                            4: "Shadow/Compost",
                            5: "Exile/Collapse"
                        }
                        therapeutic_stances = {
                            1: "Full exploration",
                            2: "Relational depth",
                            3: "Caution advised",
                            4: "Protective stance",
                            5: "Crisis containment"
                        }

                        zone = SELFZoneState(
                            zone_id=zone_id,
                            zone_name=zone_names.get(zone_id, "Unknown"),
                            therapeutic_stance=therapeutic_stances.get(zone_id, "Unknown")
                        )

                    # Convert enriched_entities to candidate_entities format
                    candidate_entities = []
                    for entity in enriched_entities:
                        candidate_entities.append({
                            'value': entity.get('value', entity.get('entity_value', '')),
                            'entity_type': entity.get('type', entity.get('entity_type', 'Unknown')),
                            'confidence_score': entity.get('confidence', 0.5)
                        })

                    # Filter entities transductively
                    filtered_entities, filter_metadata = self.transductive_felt_filter.filter_entities_transductively(
                        candidate_entities=candidate_entities,
                        bond_result=bond_result,
                        zone=zone,
                        prehension=None,  # Disabled for now - requires full prehension object
                        satisfaction_trace=[]  # Disabled for now - requires satisfaction trace
                    )

                    # Convert back to enriched_entities format
                    enriched_entities = []
                    for entity in filtered_entities:
                        enriched_entities.append({
                            'value': entity['value'],
                            'type': entity['entity_type'],
                            'confidence': entity.get('confidence_score', 0.5)
                        })

                    # Show filtering results
                    if self.display_mode in ['detailed', 'debug'] and pre_filter_count != len(enriched_entities):
                        filter_rate = filter_metadata.get('filter_rate', 0.0)
                        print(f"\n🌀 Transductive Felt Filter:")
                        print(f"   {pre_filter_count} → {len(enriched_entities)} entities ({filter_rate:.1%} filtered)")
                        print(f"   Zone: {zone.zone_name if zone else 'Unknown'}")

                        # Show layer contributions
                        if 'layer0_filtered' in filter_metadata and filter_metadata['layer0_filtered'] > 0:
                            print(f"   Layer 0 (BOND IFS): {filter_metadata['layer0_filtered']} filtered")
                        if 'layer1_filtered' in filter_metadata and filter_metadata['layer1_filtered'] > 0:
                            print(f"   Layer 1 (SELF Matrix): {filter_metadata['layer1_filtered']} filtered")

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

                # 🌀 Whiteheadian Entity Ontology Integration (Nov 17, 2025)
                # Process: Extract → Validate → Horizon → Salience → Neo4j
                if self.entity_validator and self.entity_horizon and self.entity_salience_tracker:
                    try:
                        # Step 1: Convert enriched entities to validation format
                        entities_to_validate = self._convert_to_validation_format(enriched_entities)

                        # Step 2: VALIDATE against Whiteheadian ontology
                        valid_entities, rejected_entities = self.entity_validator.validate_entities(entities_to_validate)

                        if self.display_mode in ['detailed', 'debug']:
                            print(f"\n🌀 Whiteheadian Entity Validation:")
                            print(f"   Valid entities: {len(valid_entities)}/{len(entities_to_validate)}")
                            if rejected_entities:
                                rejection_reasons = {}
                                for ent in rejected_entities:
                                    reason = ent.get('rejection_reason', 'unknown')
                                    rejection_reasons[reason] = rejection_reasons.get(reason, 0) + 1
                                print(f"   Rejected: {len(rejected_entities)} (stopwords={rejection_reasons.get('Stopword', 0)}, capitalization={rejection_reasons.get('Invalid capitalization', 0)})")

                        # Step 3: Compute adaptive HORIZON size (100-500 based on coherence)
                        horizon_size = self.entity_horizon.compute_horizon_size(field_coherence)

                        # Step 4: Update SALIENCE with urgency context
                        self.entity_salience_tracker.update_salience(
                            valid_entities,
                            context['turn'],
                            urgency_context=urgency_context
                        )

                        # Step 5: Get morpheable entity set (horizon-bounded + salience-ranked)
                        entities_in_horizon = self.entity_horizon.get_entities_in_horizon(
                            self.entity_salience_tracker,
                            horizon_size,
                            include_staleness_pruning=True
                        )

                        if self.display_mode in ['detailed', 'debug']:
                            print(f"   Horizon size: {horizon_size} entities (coherence={field_coherence:.3f})")
                            print(f"   Entities in horizon: {len(entities_in_horizon)}")
                            if valid_entities:
                                top_entity = max(valid_entities, key=lambda e: e.get('salience_base', 0.5))
                                print(f"   Top entity: {top_entity.get('entity_value')} ({top_entity.get('ontology_category')}, salience={top_entity.get('salience_base'):.2f})")

                        # Step 5.5: PERSIST salience state to JSON (fallback robustness)
                        # Ensures organism memory persists even if Neo4j unavailable
                        try:
                            self.entity_salience_tracker.save_state()
                            if self.display_mode == 'debug':
                                print(f"   💾 Entity salience state persisted to JSON")
                        except Exception as e:
                            if self.display_mode == 'debug':
                                print(f"   ⚠️  Salience state persistence failed: {e}")

                        # Step 6: Store VALIDATED entities in Neo4j (if enabled)
                        if self.knowledge_graph and Config.NEO4J_DUAL_STORAGE:
                            try:
                                self._store_validated_entities_in_neo4j(
                                    valid_entities,
                                    felt_state,
                                    context['turn']
                                )
                                if self.display_mode in ['detailed', 'debug']:
                                    print(f"   ✅ Validated entities stored in Neo4j (ontology-aware)")
                            except Exception as e:
                                if self.display_mode == 'debug':
                                    print(f"   ⚠️  Neo4j storage failed: {e}")
                                # Non-critical - entity tracking still works

                    except Exception as e:
                        if self.display_mode == 'debug':
                            print(f"\n⚠️  Whiteheadian entity processing failed: {e}")
                        # Fallback to original storage if validation fails
                        if self.knowledge_graph and Config.NEO4J_DUAL_STORAGE:
                            try:
                                self._store_entities_in_neo4j(enriched_entities, felt_state, context['turn'])
                            except:
                                pass

                # 🌀 Fallback: Original entity storage (if Whiteheadian disabled)
                elif self.knowledge_graph and Config.NEO4J_DUAL_STORAGE:
                    try:
                        self._store_entities_in_neo4j(enriched_entities, felt_state, context['turn'])
                        if self.display_mode in ['detailed', 'debug']:
                            print(f"🌀 Entities stored in Neo4j (original method, turn {context['turn']})")
                    except Exception as e:
                        if self.display_mode == 'debug':
                            print(f"⚠️  Neo4j entity storage failed: {e}")
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

        # 🌀 Phase 1 Entity Continuity: Add to conversation history (Nov 17, 2025)
        # Store this turn for pronoun resolution and entity continuity
        try:
            emission_text = result.get('emission', '')
            entities_for_history = context.get('current_turn_entities', [])
            self.add_to_history(user_input, emission_text, entities_for_history)
        except Exception as e:
            if self.mode == 'debug':
                print(f"⚠️  Failed to add turn to history: {e}")
            # Non-critical - continue without history

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

    def _reconnect_neo4j(self) -> bool:
        """
        Attempt to reconnect to Neo4j after connection loss.

        Returns:
            bool: True if reconnection successful, False otherwise
        """
        if not Config.NEO4J_ENABLED:
            return False

        try:
            from knowledge_base.neo4j_knowledge_graph import Neo4jKnowledgeGraph
            print("   🔄 Attempting Neo4j reconnection...")
            self.knowledge_graph = Neo4jKnowledgeGraph(
                uri=Config.NEO4J_URI,
                user=Config.NEO4J_USER,
                password=Config.NEO4J_PASSWORD,
                database=Config.NEO4J_DATABASE
            )
            if self.knowledge_graph.driver:
                print("   ✅ Neo4j reconnected successfully")
                return True
            else:
                print("   ⚠️  Neo4j reconnection failed - using JSON fallback")
                self.knowledge_graph = None
                return False
        except Exception as e:
            print(f"   ⚠️  Neo4j reconnection error: {e}")
            self.knowledge_graph = None
            return False

    def _convert_to_validation_format(self, enriched_entities: dict) -> list:
        """
        Convert enriched_entities dict to list format for EntityOntologyValidator.

        Args:
            enriched_entities: Dict with keys like 'family_members', 'friends', 'locations', etc.

        Returns:
            List of entity dicts with entity_type, entity_value, and properties
        """
        entities = []

        # User name (Person)
        if enriched_entities.get('user_name'):
            entities.append({
                'entity_type': 'Person',
                'entity_value': enriched_entities['user_name'],
                'properties': {}
            })

        # Family members (Person with relationship)
        if enriched_entities.get('family_members'):
            for member in enriched_entities['family_members']:
                entities.append({
                    'entity_type': 'Person',
                    'entity_value': member.get('name'),
                    'relationship': member.get('relationship', 'family'),  # daughter, son, etc.
                    'properties': {
                        'relationship': member.get('relationship'),
                        'confidence': member.get('confidence', 0.9)
                    }
                })

        # Friends (Person with social relationship)
        if enriched_entities.get('friends'):
            for friend_name in enriched_entities['friends']:
                entities.append({
                    'entity_type': 'Person',
                    'entity_value': friend_name,
                    'relationship': 'friend',
                    'properties': {'relationship': 'friend'}
                })

        # Locations (Place)
        if enriched_entities.get('locations'):
            for location in enriched_entities['locations']:
                entities.append({
                    'entity_type': 'Place',
                    'entity_value': location,
                    'properties': {}
                })

        # Preferences (Preference)
        if enriched_entities.get('preferences'):
            for pref_key, pref_value in enriched_entities['preferences'].items():
                entities.append({
                    'entity_type': 'Preference',
                    'entity_value': f"{pref_key}: {pref_value}",
                    'preference_type': pref_key,  # likes, dislikes, interests
                    'properties': {'type': pref_key}
                })

        # Facts (Concept - factual knowledge)
        if enriched_entities.get('facts'):
            for fact in enriched_entities['facts']:
                entities.append({
                    'entity_type': 'Concept',
                    'entity_value': fact,
                    'properties': {}
                })

        return entities

    def _store_validated_entities_in_neo4j(
        self,
        valid_entities: list,
        felt_state: dict,
        current_turn: int = None
    ):
        """
        Store VALIDATED entities in Neo4j with ontology-aware properties.

        Args:
            valid_entities: List of entities that passed EntityOntologyValidator
            felt_state: TSK felt state for enrichment
            current_turn: Turn number for horizon tracking
        """
        if not self.knowledge_graph:
            return

        # Prepare TSK properties
        tsk_properties = {}
        if Config.NEO4J_ENABLE_TSK_ENRICHMENT and felt_state:
            tsk_properties = {
                'polyvagal_state': felt_state.get('polyvagal_state', 'unknown'),
                'urgency_level': felt_state.get('urgency_level', 0.0),
                'self_distance': felt_state.get('self_distance', 0.5),
                'v0_energy': felt_state.get('v0_energy', 0.5),
                'satisfaction': felt_state.get('satisfaction', 0.5)
            }

        # Wrap with retry logic
        max_retries = 2
        for attempt in range(max_retries):
            try:
                for entity in valid_entities:
                    # Merge TSK + ontology properties
                    properties = {**tsk_properties}
                    properties.update({
                        'ontology_category': entity.get('ontology_category'),
                        'process_mapping': entity.get('process_mapping'),
                        'salience_base': entity.get('salience_base', 0.5)
                    })

                    # Add entity-specific properties
                    if entity.get('properties'):
                        properties.update(entity['properties'])

                    # Create entity node
                    self.knowledge_graph.create_entity(
                        entity_type=entity['entity_type'],
                        entity_value=entity['entity_value'],
                        user_id=self.user['user_id'],
                        properties=properties,
                        current_turn=current_turn
                    )

                    # Create relationships (Person entities only)
                    if entity['entity_type'] == 'Person' and entity.get('relationship'):
                        relationship = entity['relationship']
                        # Try to create relationship to user (if user_name exists)
                        # This is a simplification - full implementation would track user entity
                        rel_type = f"HAS_{relationship.upper()}"
                        # Note: Relationship creation requires from_entity_value
                        # This is handled by the knowledge graph's entity linking

                # Success - break retry loop
                break

            except Exception as e:
                error_msg = str(e).lower()
                is_connection_error = any(err in error_msg for err in [
                    'connection reset', 'service unavailable', 'connection refused',
                    'connection closed', 'socket', 'timeout', 'reconnect'
                ])

                if is_connection_error and attempt < max_retries - 1:
                    if self._reconnect_neo4j():
                        continue
                    else:
                        break
                else:
                    raise  # Re-raise for outer exception handler

    def _store_entities_in_neo4j(self, enriched_entities: dict, felt_state: dict, current_turn: int = None):
        """
        Store extracted entities in Neo4j knowledge graph.

        Creates entity nodes and relationships with TSK enrichment and turn tracking.
        Includes automatic reconnection on connection failures.

        Args:
            enriched_entities: Extracted entities with transductive context
            felt_state: TSK felt state for enrichment
            current_turn: Turn number for morpheable horizon tracking (Nov 17, 2025)
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

        # Wrap all Neo4j operations with retry logic for connection resilience
        max_retries = 2
        for attempt in range(max_retries):
            try:
                # Store user name
                if enriched_entities.get('user_name'):
                    name = enriched_entities['user_name']
                    self.knowledge_graph.create_entity(
                        entity_type='Person',
                        entity_value=name,
                        user_id=self.user['user_id'],
                        properties=tsk_properties,
                        current_turn=current_turn
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
                            properties=tsk_properties,
                            current_turn=current_turn
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
                            properties=tsk_properties,
                            current_turn=current_turn
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
                            properties=tsk_properties,
                            current_turn=current_turn
                        )

                # Store preferences
                if enriched_entities.get('preferences'):
                    for pref_key, pref_value in enriched_entities['preferences'].items():
                        self.knowledge_graph.create_entity(
                            entity_type='Preference',
                            entity_value=f"{pref_key}: {pref_value}",
                            user_id=self.user['user_id'],
                            properties=tsk_properties,
                            current_turn=current_turn
                        )

                # Store facts
                if enriched_entities.get('facts'):
                    for fact in enriched_entities['facts']:
                        self.knowledge_graph.create_entity(
                            entity_type='Fact',
                            entity_value=fact,
                            user_id=self.user['user_id'],
                            properties=tsk_properties,
                            current_turn=current_turn
                        )

                # Success - break out of retry loop
                break

            except Exception as e:
                error_msg = str(e).lower()
                is_connection_error = any(err in error_msg for err in [
                    'connection reset', 'service unavailable', 'connection refused',
                    'connection closed', 'socket', 'timeout', 'reconnect'
                ])

                if is_connection_error and attempt < max_retries - 1:
                    print(f"   ⚠️  Neo4j connection error: {e}")
                    if self._reconnect_neo4j():
                        print(f"   🔄 Retrying entity storage (attempt {attempt + 2}/{max_retries})")
                        continue
                    else:
                        print("   ⚠️  Neo4j reconnection failed, entities not stored in graph")
                        break
                else:
                    print(f"   ⚠️  Neo4j entity storage error: {e}")
                    break

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

            print(f"\n🧬 Active Organs ({len(active_organs)}/12):  🌀 12th organ: NEXUS")
            for organ in sorted(active_organs):
                coherence = organ_coherences[organ]
                emoji = "🌀" if organ == "NEXUS" else "  "
                print(f"   {emoji} {organ}: {coherence:.3f}")

            # Key organ metrics
            if 'BOND_self_distance' in felt_states:
                print(f"\n   BOND self-distance: {felt_states['BOND_self_distance']:.3f}")
            if 'NDAM_urgency_level' in felt_states:
                print(f"   NDAM urgency: {felt_states['NDAM_urgency_level']:.3f}")
            if 'EO_polyvagal_state' in felt_states:
                print(f"   EO polyvagal: {felt_states['EO_polyvagal_state']}")
            if 'NEXUS' in organ_coherences and organ_coherences['NEXUS'] > 0.3:
                print(f"   🌀 NEXUS coherence: {organ_coherences['NEXUS']:.3f} (entity-memory activated!)")

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

        # 🌀 Nov 17, 2025: Add satisfaction prompt (0.0-1.0 for quality boost activation)
        satisfaction_score = None

        if rating_input in rating_map:
            rating = rating_map[rating_input]

            # Prompt for numerical satisfaction score (0.0-1.0)
            print("\n💧 Satisfaction score (optional - enables Hebbian learning):")
            print("  How satisfied are you with this response? (0.0-1.0)")
            print("  [0.0 = Not at all] [0.5 = Somewhat] [1.0 = Very satisfied] [Enter] Skip")
            satisfaction_input = input("Satisfaction (0.0-1.0): ").strip()

            if satisfaction_input:
                try:
                    satisfaction_score = float(satisfaction_input)
                    # Clamp to [0.0, 1.0] range
                    satisfaction_score = max(0.0, min(1.0, satisfaction_score))
                    print(f"   ✅ Satisfaction recorded: {satisfaction_score:.2f}")
                except ValueError:
                    print("   ⚠️  Invalid number, skipping satisfaction score")
                    satisfaction_score = None
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
                    'strategy': felt_states.get('emission_strategy', 'unknown'),
                    'satisfaction_score': satisfaction_score  # 🌀 Nov 17, 2025: Real-time quality boost
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
                    elif user_input == '/refresh':
                        # ✅ NOV 17: Reload organism learning state (Whiteheadian prehension)
                        print("\n🔄 Reloading organism learning state from disk...")
                        try:
                            self.organism.reload_learning_state()
                            print("✅ Organism state refreshed!")
                            print("   - R-matrix couplings reloaded")
                            print("   - Hebbian memory updated")
                            print("   - Organ confidence refreshed")
                            print("   - Entity-organ associations updated")
                            print("   - Organic families synchronized")
                            print("\n   Each occasion now prehends all past occasions (including recent training)")
                        except Exception as e:
                            print(f"⚠️  Reload failed: {e}")
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
                    # 🌀 Phase 2.0: Entity management commands (Nov 16, 2025)
                    elif user_input.startswith('/entities'):
                        # Parse optional filter argument
                        parts = user_input.split(maxsplit=1)
                        filter_arg = parts[1] if len(parts) > 1 else None
                        self.cmd_entities(filter_arg)
                        continue
                    elif user_input.startswith('/entity add'):
                        # Parse entity add command
                        parts = user_input.split()[2:]  # Skip '/entity add'
                        self.cmd_entity_add(*parts)
                        continue
                    elif user_input.startswith('/entity link'):
                        # Parse entity link command
                        parts = user_input.split()[2:]  # Skip '/entity link'
                        self.cmd_entity_link(*parts)
                        continue
                    elif user_input.startswith('/graph'):
                        # Parse graph command
                        parts = user_input.split()[1:]  # Skip '/graph'
                        self.cmd_graph(*parts)
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
        print("\n🧠 Entity Memory Commands (NEW - Nov 16, 2025):")
        print("  /entities           - List all stored entities")
        print("  /entities person    - Filter by type (person/place/preference/fact)")
        print("  /entities Emma      - Show specific entity details")
        print("  /entity add person \"Name\" relationship=\"daughter\" age=8")
        print("  /entity link \"Emma\" \"Lily\" siblings")
        print("  /graph Emma         - Show entity relationship graph")
        print("  /graph Emma 2       - Show 2-hop connections")
        print("  /graph stats        - Neo4j graph statistics")
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

    # 🌀 Phase 2.0: Entity Management Commands (Nov 16, 2025)
    # Quick Win #10: Interactive entity interface for Neo4j knowledge graph

    def cmd_entities(self, filter_arg=None):
        """
        List all entities for current user with optional filtering.

        Usage:
            /entities              - Show all entities
            /entities person       - Filter by type (person, place, preference, fact)
            /entities Emma         - Show details for specific entity
        """
        print("\n" + "="*70)
        print(f"Entity Memory for {self.user['username']}")
        print("="*70)

        # Dual-storage approach: Try Neo4j first, fall back to JSON
        entities = []
        storage_source = "JSON"

        if self.knowledge_graph:
            try:
                # Try Neo4j retrieval
                if filter_arg and filter_arg.lower() in ['person', 'place', 'preference', 'fact']:
                    # Filter by type
                    entities = self.knowledge_graph.get_user_entities(
                        self.user['user_id'],
                        entity_type=filter_arg.capitalize()
                    )
                elif filter_arg:
                    # Show specific entity detail
                    self._show_entity_detail(filter_arg)
                    return
                else:
                    # Show all entities
                    entities = self.knowledge_graph.get_user_entities(self.user['user_id'])
                storage_source = "Neo4j"
            except Exception as e:
                print(f"⚠️  Neo4j query failed: {e}")
                print("   Falling back to JSON storage...\n")

        # Fallback to JSON if Neo4j unavailable or failed
        if not entities:
            entities = self._get_json_entities(filter_arg)
            storage_source = "JSON"

        if not entities:
            print(f"\n   No entities stored yet.")
            print(f"   Entities are learned from conversations or added manually.")
            print(f"\n   Try: /entity add person \"YourName\"")
            print("="*70 + "\n")
            return

        # Display entities
        print(f"\nSource: {storage_source} | Count: {len(entities)}\n")
        self._display_entity_table(entities)
        print("="*70 + "\n")

    def _get_json_entities(self, filter_arg=None):
        """Retrieve entities from JSON user profile (fallback)."""
        entities = []
        if 'user_profile' in self.user_state:
            from persona_layer.superject_structures import EnhancedUserProfile
            profile = EnhancedUserProfile.from_dict(self.user_state['user_profile'])

            # Extract entities from profile
            if profile.entities:
                # User name
                if 'user_name' in profile.entities:
                    entities.append({
                        'name': profile.entities['user_name'],
                        'type': 'Person',
                        'properties': {'relationship': 'self'},
                        'mention_count': 0
                    })

                # Family members
                if 'family_members' in profile.entities:
                    for member in profile.entities['family_members']:
                        if isinstance(member, dict):
                            entities.append({
                                'name': member.get('name', 'Unknown'),
                                'type': 'Person',
                                'properties': member,
                                'mention_count': 0
                            })

                # Other entities
                for key, value in profile.entities.items():
                    if key not in ['user_name', 'family_members'] and value:
                        if isinstance(value, list):
                            for item in value:
                                entities.append({
                                    'name': str(item),
                                    'type': 'Fact',
                                    'properties': {},
                                    'mention_count': 0
                                })

        # Filter if requested
        if filter_arg and filter_arg.lower() in ['person', 'place', 'preference', 'fact']:
            entities = [e for e in entities if e['type'].lower() == filter_arg.lower()]

        return entities

    def _display_entity_table(self, entities):
        """Display entities in formatted table."""
        # Group by type
        by_type = {}
        for e in entities:
            # Handle both Neo4j (entity_types list) and JSON (type string)
            if 'entity_types' in e:
                # Neo4j returns labels as list, filter out 'Entity' base label
                types = [t for t in e['entity_types'] if t != 'Entity']
                entity_type = types[0] if types else 'Unknown'
            else:
                entity_type = e.get('type', 'Unknown')

            if entity_type not in by_type:
                by_type[entity_type] = []
            by_type[entity_type].append(e)

        # Display grouped
        for entity_type, entity_list in sorted(by_type.items()):
            print(f"\n📁 {entity_type} ({len(entity_list)})")
            print("   " + "-"*66)

            for e in entity_list:
                # Handle both Neo4j (entity_value) and JSON (name) fields
                name = e.get('name', e.get('entity_value', e.get('value', 'Unknown')))

                # For Neo4j, properties are stored directly on entity node
                # For JSON, properties are in 'properties' dict
                if 'properties' in e:
                    props = e.get('properties', {})
                else:
                    # Neo4j: all fields are properties
                    props = e

                # Build property string
                prop_parts = []
                if 'relationship' in props:
                    prop_parts.append(f"rel:{props['relationship']}")
                if 'polyvagal_state' in props:
                    prop_parts.append(f"polyvagal:{props['polyvagal_state']}")
                if 'safety_score' in props and isinstance(props['safety_score'], (int, float)):
                    prop_parts.append(f"safety:{props['safety_score']:.2f}")
                if 'age' in props:
                    prop_parts.append(f"age:{props['age']}")
                if 'location' in props:
                    prop_parts.append(f"location:{props['location']}")

                prop_str = " | ".join(prop_parts) if prop_parts else "no metadata"
                mention_count = e.get('mention_count', e.get('mentions', 0))

                print(f"   🔹 {name:<20} {prop_str:<30} ({mention_count} mentions)")

    def _show_entity_detail(self, entity_name):
        """Show detailed view of entity with relationships."""
        print("\n" + "="*70)
        print(f"Entity Detail: {entity_name}")
        print("="*70)

        if not self.knowledge_graph:
            print("\n⚠️  Neo4j not connected. Detailed view requires Neo4j.")
            print("   Showing JSON data only:\n")
            # Show from JSON
            entities = self._get_json_entities()
            matching = [e for e in entities if e.get('name', '').lower() == entity_name.lower()]
            if matching:
                entity = matching[0]
                print(f"   Name: {entity.get('name')}")
                print(f"   Type: {entity.get('type')}")
                print(f"   Properties: {entity.get('properties', {})}")
            else:
                print(f"   Entity not found: {entity_name}")
            print("="*70 + "\n")
            return

        try:
            # Get entity relationships from Neo4j
            rels = self.knowledge_graph.get_entity_relationships(
                entity_value=entity_name,
                user_id=self.user['user_id'],
                max_depth=1
            )

            if not rels:
                print(f"\n⚠️  No entity found: {entity_name}\n")
                print("="*70 + "\n")
                return

            # Show relationships
            print(f"\n📊 Relationships:")
            print("   " + "-"*66)
            for rel in rels:
                from_entity = rel.get('from', 'Unknown')
                to_entity = rel.get('to', 'Unknown')
                rel_type = rel.get('type', 'RELATED_TO')
                print(f"   {from_entity} --[{rel_type}]--> {to_entity}")

            # Show properties if available
            # TODO: Query entity node properties from Neo4j
            print(f"\n💾 Stored Properties:")
            print("   " + "-"*66)
            print("   (Property retrieval coming in next update)")

            print("="*70 + "\n")

        except Exception as e:
            print(f"\n⚠️  Error retrieving entity: {e}\n")
            print("="*70 + "\n")

    def cmd_entity_add(self, *args):
        """
        Manually add an entity to memory.

        Usage:
            /entity add person "Name" relationship="daughter" age=8
            /entity add place "Location"
            /entity add preference "likes coffee"
            /entity add fact "Works at Google"
        """
        if len(args) < 2:
            print("\n❌ Usage: /entity add <type> <name> [properties...]")
            print("   Example: /entity add person \"Emma\" relationship=\"daughter\" age=8\n")
            return

        entity_type = args[0].capitalize()
        entity_name = args[1].strip('"')

        # Parse properties (key=value format)
        properties = {}
        for arg in args[2:]:
            if '=' in arg:
                key, value = arg.split('=', 1)
                # Try to parse as number
                try:
                    value = float(value)
                    if value.is_integer():
                        value = int(value)
                except:
                    value = value.strip('"')
                properties[key] = value

        print(f"\n🔹 Adding entity: {entity_name} ({entity_type})")
        if properties:
            print(f"   Properties: {properties}")

        # Add to Neo4j if available
        neo4j_success = False
        if self.knowledge_graph:
            try:
                self.knowledge_graph.create_entity(
                    entity_type=entity_type,
                    entity_value=entity_name,
                    user_id=self.user['user_id'],
                    properties=properties
                )
                print(f"   ✅ Added to Neo4j")
                neo4j_success = True
            except Exception as e:
                print(f"   ⚠️  Neo4j add failed: {e}")

        # Also add to JSON (dual storage)
        from persona_layer.superject_structures import EnhancedUserProfile
        if 'user_profile' in self.user_state:
            profile = EnhancedUserProfile.from_dict(self.user_state['user_profile'])
        else:
            now = datetime.now().isoformat()
            profile = EnhancedUserProfile(
                user_id=self.user['user_id'],
                created_at=now,
                last_active=now
            )

        # Store in profile using correct format for entity prehension
        # CRITICAL: Use 'relationships' field so pre_emission_entity_prehension can find them
        entities_to_store = {}

        if entity_type == 'Person':
            if 'relationships' not in profile.entities:
                profile.entities['relationships'] = []
            profile.entities['relationships'].append({
                'name': entity_name,
                'type': 'person',
                **properties
            })
            entities_to_store['relationships'] = profile.entities['relationships']
        else:
            # For non-person entities, store in mentioned_names
            if 'mentioned_names' not in profile.entities:
                profile.entities['mentioned_names'] = []
            if entity_name not in profile.entities['mentioned_names']:
                profile.entities['mentioned_names'].append(entity_name)
            entities_to_store['mentioned_names'] = profile.entities['mentioned_names']

        # Use store_entities method for proper persistence
        profile.store_entities(entities_to_store)

        # Save via UserSuperjectLearner for consistency
        if self.user_superject_learner:
            self.user_superject_learner.save_profile(profile)

        print(f"   ✅ Added to JSON profile (format: {'relationships' if entity_type == 'Person' else 'mentioned_names'})\n")

    def cmd_entity_link(self, *args):
        """
        Create relationship between two entities.

        Usage:
            /entity link "Emma" "Lily" siblings
            /entity link "Emiliano" "Emma" HAS_DAUGHTER
        """
        if len(args) < 3:
            print("\n❌ Usage: /entity link <from_entity> <to_entity> <relationship_type>")
            print("   Example: /entity link \"Emma\" \"Lily\" siblings\n")
            return

        from_entity = args[0].strip('"')
        to_entity = args[1].strip('"')
        rel_type = args[2].upper().replace(' ', '_')

        if not self.knowledge_graph:
            print("\n⚠️  Neo4j not connected. Entity relationships require Neo4j.\n")
            return

        print(f"\n🔗 Creating relationship:")
        print(f"   {from_entity} --[{rel_type}]--> {to_entity}")

        try:
            self.knowledge_graph.create_entity_relationship(
                from_entity_value=from_entity,
                to_entity_value=to_entity,
                rel_type=rel_type,
                user_id=self.user['user_id'],
                properties={'manually_created': True}
            )
            print(f"   ✅ Relationship created in Neo4j\n")
        except Exception as e:
            print(f"   ❌ Failed: {e}\n")

    def cmd_graph(self, *args):
        """
        Visualize entity relationship graph.

        Usage:
            /graph Emma              # Show Emma's relationships (1-hop)
            /graph Emma 2            # Show 2-hop connections
            /graph stats             # Show graph statistics
        """
        if not args:
            print("\n❌ Usage: /graph <entity_name> [depth] or /graph stats\n")
            return

        if args[0] == 'stats':
            self._show_graph_stats()
            return

        entity_name = args[0].strip('"')
        depth = int(args[1]) if len(args) > 1 else 1

        if not self.knowledge_graph:
            print("\n⚠️  Neo4j not connected. Graph visualization requires Neo4j.\n")
            return

        print(f"\n🌐 Relationship Graph for: {entity_name} (depth: {depth})")
        print("="*70)

        try:
            rels = self.knowledge_graph.get_entity_relationships(
                entity_value=entity_name,
                user_id=self.user['user_id'],
                max_depth=depth
            )

            if not rels:
                print(f"\n   No relationships found for: {entity_name}\n")
                print("="*70 + "\n")
                return

            # ASCII graph visualization
            self._render_ascii_graph(entity_name, rels)
            print("="*70 + "\n")

        except Exception as e:
            print(f"\n⚠️  Error: {e}\n")
            print("="*70 + "\n")

    def _show_graph_stats(self):
        """Show Neo4j graph statistics."""
        if not self.knowledge_graph:
            print("\n⚠️  Neo4j not connected.\n")
            return

        print("\n" + "="*70)
        print("Neo4j Knowledge Graph Statistics")
        print("="*70)

        try:
            stats = self.knowledge_graph.get_stats()

            print(f"\n📊 Overall:")
            print(f"   Total entity nodes: {stats.get('entity_count', 0)}")
            print(f"   Total relationships: {stats.get('relationship_count', 0)}")

            print(f"\n👤 Your Entities:")
            user_entities = self.knowledge_graph.get_user_entities(self.user['user_id'])
            print(f"   Entities stored: {len(user_entities)}")

            # Count by type
            by_type = {}
            for e in user_entities:
                entity_type = e.get('type', 'Unknown')
                by_type[entity_type] = by_type.get(entity_type, 0) + 1

            for entity_type, count in sorted(by_type.items()):
                print(f"   - {entity_type}: {count}")

            print("="*70 + "\n")

        except Exception as e:
            print(f"\n⚠️  Error: {e}\n")
            print("="*70 + "\n")

    def _render_ascii_graph(self, center, relationships):
        """
        Render entity graph as ASCII art.

        Example:
            Emma
            ├── [HAS_SIBLING] --> Lily
            ├── [HAS_FATHER] --> Emiliano
            └── [MENTIONED_WITH] --> School
        """
        print(f"\n   {center}")
        for i, rel in enumerate(relationships):
            is_last = (i == len(relationships) - 1)
            prefix = "   └──" if is_last else "   ├──"
            rel_type = rel.get('type', 'RELATED_TO')
            to_entity = rel.get('to', 'Unknown')
            print(f"{prefix} [{rel_type}] --> {to_entity}")

    def add_to_history(self, user_input, emission, entities):
        """
        Add turn to conversation history buffer.

        Maintains a sliding window of last N turns for entity continuity.

        Args:
            user_input: User's input text
            emission: DAE's response text
            entities: List of entities detected/mentioned in this turn
        """
        self.conversation_history.append({
            'turn_num': len(self.conversation_history) + 1,
            'user_input': user_input,
            'emission': emission,
            'entities': entities,
            'timestamp': datetime.now().isoformat()
        })

        # Keep only last N turns
        if len(self.conversation_history) > self.max_history_turns:
            self.conversation_history.pop(0)

    def get_recent_session_entities(self, n_turns=5):
        """
        Get all entities mentioned in last N turns of this session.

        Used for pronoun resolution and implicit entity references.

        Args:
            n_turns: Number of recent turns to extract entities from

        Returns:
            List of entity dicts with name, type, properties, source
        """
        recent_entities = []

        for turn in self.conversation_history[-n_turns:]:
            if turn.get('entities'):
                for entity in turn['entities']:
                    recent_entities.append({
                        'name': entity.get('entity_value'),
                        'type': entity.get('entity_type', 'Entity'),
                        'properties': entity.get('properties', {}),
                        'source': 'session'
                    })

        return recent_entities


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
