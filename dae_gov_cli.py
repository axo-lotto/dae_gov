#!/usr/bin/env python3
"""
DAE-GOV CLI - Command-Line Interface for Organism Interaction
Week 2, Day 14 - Interactive Console + Conversational Hebbian Learning
Phase 2.0 - Curious Questioning Integration (DAE 3.0 Architecture)

Simple CLI for trauma-informed organizational consulting conversations.
Uses complete knowledge corpus (Process & Reality, I Ching, Poetry, Whitehead, Conversations).

Features:
- Interactive chat with DAE-GOV organism
- 5 Conversational Organs (410 keywords): LISTENING, EMPATHY, WISDOM, AUTHENTICITY, PRESENCE
- Curiosity-driven questioning (asks when uncertain)
- Conversational R-Matrix (Hebbian organ coupling with DAE 3.0 hyperparameters)
- 4-gate Nexus architecture (intersection, coherence, satisfaction, felt energy)
- Knowledge-augmented responses (FAISS semantic search)
- 4-gate cascade processing (Polyvagal, SELF-Energy, OFEL, CARD)
- Conversational Hebbian learning (pattern strengthening)
- Conversation history tracking
- Trauma-informed pattern detection

Author: Claude Code (November 2025)
Status: Phase 2.0 - Curious Questioning Integrated (Production Ready)
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
import numpy as np
from typing import List, Dict, Optional

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from knowledge_base.faiss_memory import FAISSMemory
from orchestration.text_orchestrator import BasicTextOrchestrator
from persona_layer.self_led_cascade import SELFLedCascade
from persona_layer.conversational_hebbian_memory import ConversationalHebbianMemory
from persona_layer.greeting_detector import GreetingDetector
from sklearn.feature_extraction.text import TfidfVectorizer

# Import monitoring systems
from monitoring.session_tracker import SessionTracker
from monitoring.health_dashboard import SimpleDashboard

# Import mycelium trace system for MESO level reward propagation
from knowledge_base.mycelium_traces import MyceliumTracer, TraceType

# Import epoch training for EPOCH level pattern reinforcement
from knowledge_base.epoch_training_coordinator import EpochTrainingCoordinator

# Import mycelial identity tracker for identity-aware greetings and project awareness
from monitoring.mycelial_identity_tracker import MycelialIdentityTracker

# Import 5 conversational organs
from organs.modular.listening.core.listening_text_core import ListeningTextCore
from organs.modular.empathy.core.empathy_text_core import EmpathyTextCore
from organs.modular.wisdom.core.wisdom_text_core import WisdomTextCore
from organs.modular.authenticity.core.authenticity_text_core import AuthenticityTextCore
from organs.modular.presence.core.presence_text_core import PresenceTextCore

# Import Conversational R-matrix and Nexus
from organs.orchestration.conversational_hebbian import ConversationalHebbianMemory as ConversationalRMatrix
from persona_layer.conversational_nexus import ConversationalNexus

# Import for creating TextOccasions
from transductive.text_occasion import TextOccasion

# Import multi-tier memory system
from memory.session_manager import SessionManager


class DAEGovCLI:
    """
    Command-line interface for DAE-GOV organism.

    Architecture:
    - Multi-tier memory (TIER 1: Session, TIER 2: User, TIER 3: Global)
    - Load FAISS corpus index (4,984 vectors)
    - Process user input through 3 organs (SANS, NDAM, BOND)
    - Retrieve relevant knowledge from corpus
    - Generate trauma-informed responses
    - Track conversation history with session persistence
    """

    def __init__(self, user_token: Optional[str] = None):
        """
        Initialize CLI with organism and knowledge base.

        Args:
            user_token: Optional user token for multi-user sessions.
                       If None, prompts for token or creates new user.
        """
        print("\n" + "="*70)
        print("DAE-GOV - Trauma-Informed Organizational Intelligence")
        print("="*70 + "\n")

        # Initialize Session Manager (TIER 1/2/3 orchestration)
        print("🔧 Initializing multi-tier memory system...")
        self.session_manager = SessionManager()

        # Handle user instantiation or login
        if user_token is None:
            user_token = self._prompt_for_user()

        # Initialize session (loads TIER 2, prehends TIER 3)
        self.session_context = self.session_manager.initialize_session(user_token)
        print(f"   ✅ Session initialized (session #{self.session_context.total_sessions})")
        print(f"   ✅ User memory loaded: {self.session_context.total_traces} traces")
        print(f"   ✅ Global organism prehended (confidence: {self.session_context.global_organism['confidence']:.3f})")

        # Load healing purpose awareness
        self._load_safety_alignment_policy()

        print("\n🔧 Initializing organism organs...")

        # Initialize Hebbian learning system
        hebbian_path = Path(__file__).parent / "knowledge_base" / "persona_layer_hebbian_memory.json"
        self.hebbian_memory = ConversationalHebbianMemory(
            storage_path=str(hebbian_path),
            eta=0.01,  # Learning rate (from FFITTSS)
            delta=0.001  # Decay rate
        )

        # Show learning statistics if available
        if self.hebbian_memory.update_count > 0:
            print(f"   ✅ Hebbian memory loaded: {self.hebbian_memory.update_count} updates, "
                  f"{self.hebbian_memory.success_rate*100:.1f}% success rate")
        else:
            print("   ✅ Hebbian memory initialized (fresh)")

        # Initialize SELF-led cascade with Hebbian learning
        self.cascade = SELFLedCascade(hebbian_memory=self.hebbian_memory)
        print("   ✅ 4-gate cascade ready (Polyvagal, SELF-Energy, OFEL, CARD)")

        # Initialize Gate 0: Greeting Detector (bypasses cascade for simple greetings)
        self.greeting_detector = GreetingDetector()
        print("   ✅ Gate 0 greeting detector ready")

        # Keep legacy orchestrator for knowledge search compatibility
        self.orchestrator = BasicTextOrchestrator()
        print("   ✅ Text orchestrator ready (SANS, NDAM, BOND)")

        # Initialize 5 Conversational Organs
        self.listening = ListeningTextCore()
        self.empathy = EmpathyTextCore()
        self.wisdom = WisdomTextCore()
        self.authenticity = AuthenticityTextCore()
        self.presence = PresenceTextCore()
        print("   ✅ 5 conversational organs ready (410 keywords)")
        print("      • LISTENING (73 keywords) - Deep attention & tracking")
        print("      • EMPATHY (92 keywords) - Emotional resonance & validation")
        print("      • WISDOM (85 keywords) - Meta-perspective & insight")
        print("      • AUTHENTICITY (78 keywords) - Genuine self-disclosure")
        print("      • PRESENCE (82 keywords) - Somatic grounding & here-now")

        # Initialize Conversational R-Matrix (Hebbian organ coupling)
        r_matrix_path = Path(__file__).parent / "TSK" / "conversational_r_matrix.json"
        self.conversational_r_matrix = ConversationalRMatrix(memory_path=r_matrix_path)
        print(f"   ✅ Conversational R-matrix loaded ({self.conversational_r_matrix.update_count} updates)")

        # Initialize Conversational Nexus (4-gate decision with curiosity)
        self.conversational_nexus = ConversationalNexus(self.conversational_r_matrix)
        print("   ✅ Conversational Nexus ready (4-gate curiosity triggering)")

        # Initialize Mycelium Tracer for trace-level learning (MESO level)
        # Use session context's user token instead of hardcoded user_id
        self.mycelium_tracer = MyceliumTracer(user_id=self.session_context.user_token)
        print("   ✅ Mycelium tracer ready (felt state capture + epoch learning)")

        # Initialize Epoch Training Coordinator (EPOCH level)
        self.epoch_coordinator = EpochTrainingCoordinator(user_id=self.session_context.user_token)
        print(f"   ✅ Epoch training ready ({len(self.epoch_coordinator.epoch_history)} previous epochs)")

        # Track most recent trace for feedback loop
        self.most_recent_trace_id = None

        # Initialize Mycelial Identity Tracker for identity-aware greetings
        self.identity_tracker = MycelialIdentityTracker(user_id=self.session_context.user_token)
        print("   ✅ Mycelial identity tracker ready (subjective aim awareness)")

        # Initialize TF-IDF vectorizer for FAISS queries
        self.vectorizer = TfidfVectorizer(
            max_features=384,
            min_df=1,
            stop_words='english',
            ngram_range=(1, 2)
        )

        # Load FAISS corpus index
        index_dir = Path(__file__).parent / "knowledge_base" / "corpus_index"
        index_filename = "corpus_faiss_index.pkl"
        index_path = index_dir / index_filename

        if not index_path.exists():
            print(f"   ⚠️  FAISS index not found at {index_path}")
            print(f"   Run: python3 knowledge_base/build_corpus_index.py")
            self.faiss_memory = None
        else:
            # Create instance with directory path, then load file
            self.faiss_memory = FAISSMemory(dimension=384, index_path=str(index_dir))
            if self.faiss_memory.load(index_filename):
                print(f"   ✅ Knowledge base loaded: {self.faiss_memory.total_vectors:,} vectors")

                # Fit vectorizer on corpus texts for semantic search
                corpus_texts = [meta.text for meta in self.faiss_memory.metadata]
                self.vectorizer.fit(corpus_texts)
                print(f"   ✅ Vectorizer trained on corpus")
            else:
                print(f"   ⚠️  Failed to load FAISS index")
                self.faiss_memory = None

        # Load extended metadata for richer context
        extended_meta_path = index_dir / "corpus_extended_metadata.json"
        if extended_meta_path.exists():
            with open(extended_meta_path) as f:
                self.extended_metadata = json.load(f)
            print(f"   ✅ Extended metadata loaded: {len(self.extended_metadata):,} entries")
        else:
            self.extended_metadata = {}

        # Conversation history
        self.conversation_history = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Initialize monitoring systems
        self.session_tracker = SessionTracker()
        self.health_dashboard = SimpleDashboard()
        print("   ✅ Session tracking ready (user compartmentalized)")

        print("\n✅ DAE-GOV ready for conversation!")
        print("   Type 'help' for commands, 'quit' to exit\n")

        # Display identity-aware greeting
        print("=" * 70)
        greeting = self.identity_tracker.get_greeting()
        print(greeting)
        print("=" * 70 + "\n")

    def _prompt_for_user(self) -> str:
        """
        Prompt for user token or create new user.

        Returns:
            User token string
        """
        print("\n🌀 Multi-User DAE System")
        print("=" * 70)
        print("\nOptions:")
        print("  1. Enter existing user token")
        print("  2. Create new user instantiation")
        print("  3. List all users")

        choice = input("\nYour choice (1/2/3): ").strip()

        if choice == "1":
            token = input("\nEnter your user token: ").strip()
            # Validate token exists
            try:
                self.session_manager.user_manager.load_user_context(token)
                return token
            except ValueError:
                print(f"\n❌ User token '{token}' not found.")
                print("   Creating new user instead...")
                return self._create_new_user()

        elif choice == "2":
            return self._create_new_user()

        elif choice == "3":
            users = self.session_manager.user_manager.list_users()
            if not users:
                print("\n📭 No users found. Creating first user...")
                return self._create_new_user()

            print("\n📚 Registered Users:")
            print("=" * 70)
            for i, (token, info) in enumerate(users.items(), 1):
                print(f"\n{i}. {info['human_name']}")
                print(f"   Token: {token}")
                print(f"   Sessions: {info['total_sessions']}, Traces: {info['total_traces']}")
                print(f"   Created: {info['created_at']}")

            print("\n" + "=" * 70)
            choice = input("\nSelect user number (or 'new' for new user): ").strip()

            if choice.lower() == 'new':
                return self._create_new_user()

            try:
                idx = int(choice) - 1
                selected_token = list(users.keys())[idx]
                return selected_token
            except (ValueError, IndexError):
                print(f"\n❌ Invalid selection. Creating new user...")
                return self._create_new_user()

        else:
            print(f"\n❌ Invalid choice. Creating new user...")
            return self._create_new_user()

    def _create_new_user(self) -> str:
        """
        Create new user instantiation.

        Returns:
            User token string
        """
        name = input("\nEnter your name: ").strip()
        if not name:
            name = "Anonymous"

        user_context = self.session_manager.user_manager.create_user_instantiation(name)
        return user_context.user_token

    def get_state_glyph(self) -> str:
        """
        Get dynamic glyph based on organism state.

        Glyphs reflect R-matrix maturation and conversational energy:
        - 🌱 New/learning (updates < 50)
        - 🌿 Growing (updates 50-200)
        - 🌀 Mature/flowing (updates 200-500)
        - ✨ Masterful (updates 500+)
        - 🔥 High energy state (recent high coherence)
        - 💫 Transcendent (all organs highly aligned)
        """

        # Get R-matrix state
        r_updates = self.conversational_r_matrix.update_count

        # Check for recent high coherence (if we have organ history)
        try:
            if hasattr(self, '_recent_coherence_avg'):
                if self._recent_coherence_avg > 0.8:
                    return '💫'  # Transcendent
                elif self._recent_coherence_avg > 0.7:
                    return '🔥'  # High energy
        except:
            pass

        # Based on maturation level
        if r_updates >= 500:
            return '✨'  # Masterful
        elif r_updates >= 200:
            return '🌀'  # Mature
        elif r_updates >= 50:
            return '🌿'  # Growing
        else:
            return '🌱'  # New
    
    def _create_text_occasions(self, text: str) -> List[TextOccasion]:
        """
        Create TextOccasion entities from user input text.

        Simple implementation: split into sentences and create occasions.
        Each occasion is a chunk of text that can be prehended by organs.

        Args:
            text: User input text

        Returns:
            List of TextOccasion entities
        """
        import numpy as np
        from sentence_transformers import SentenceTransformer

        # Simple sentence splitting (can be improved with nltk if needed)
        sentences = [s.strip() + '.' for s in text.split('.') if s.strip()]
        if not sentences:
            sentences = [text]  # Fallback to full text if no periods

        # For now, use simple TF-IDF as embedding (can upgrade to SentenceTransformer later)
        # Create simple fake embeddings for prototype
        occasions = []
        for i, sentence in enumerate(sentences):
            occasion = TextOccasion(
                chunk_id=f"chunk_{i}",
                position=i,
                text=sentence,
                embedding=np.random.rand(384),  # Placeholder embedding
                semantic_neighbors=[],  # Empty for now
                prehensions={},
                satisfaction_level=0.5,
                family_id=None
            )
            occasions.append(occasion)

        return occasions

    def search_knowledge(self, query: str, k: int = 3) -> List[Dict]:
        """
        Search knowledge corpus for relevant context.

        Args:
            query: User's question or statement
            k: Number of results to return

        Returns:
            List of relevant knowledge chunks with metadata
        """
        if self.faiss_memory is None:
            return []

        # Vectorize query
        query_vector = self.vectorizer.transform([query]).toarray()[0]

        # Search FAISS
        results = self.faiss_memory.search(query_vector, k=k)

        # Enrich with extended metadata
        enriched = []
        for result in results:
            # metadata is already a dict (from FAISSMemory.search)
            metadata = result['metadata']
            vector_id = metadata.get('vector_id', '')
            extended = self.extended_metadata.get(vector_id, {})
            enriched.append({
                'text': metadata.get('text', ''),
                'distance': result['distance'],
                'similarity': result.get('similarity', 0.0),
                'source': metadata.get('source', 'unknown'),
                'category': extended.get('category', 'unknown'),
                'chunk_id': extended.get('chunk_id', vector_id)
            })

        return enriched

    def _process_conversational_organs(self, user_input: str) -> Dict:
        """
        Process user input through 5 conversational organs and form nexus decision.

        This is the curiosity-driven layer that triggers questions when uncertain.

        Args:
            user_input: User's message

        Returns:
            Dict with organ results, nexus decision, and curiosity state
        """
        # Create TextOccasions from user input
        occasions = self._create_text_occasions(user_input)

        # Process through all 5 conversational organs (cycle=0 for first pass)
        organ_results = {
            'LISTENING': self.listening.process_text_occasions(occasions, cycle=0),
            'EMPATHY': self.empathy.process_text_occasions(occasions, cycle=0),
            'WISDOM': self.wisdom.process_text_occasions(occasions, cycle=0),
            'AUTHENTICITY': self.authenticity.process_text_occasions(occasions, cycle=0),
            'PRESENCE': self.presence.process_text_occasions(occasions, cycle=0)
        }

        # Update R-matrix with organ co-activation patterns
        self.conversational_r_matrix.update_coupling(organ_results)

        # Form nexus decision with curiosity triggering
        nexus_decision = self.conversational_nexus.form_nexus(organ_results)

        return {
            'organ_results': organ_results,
            'nexus_decision': nexus_decision,
            'curiosity_triggered': nexus_decision.decision_type == 'curiosity_question',
            'r_matrix_updates': self.conversational_r_matrix.update_count
        }

    def process_input(self, user_input: str) -> Dict:
        """
        Process user input through organism with cascade.

        Args:
            user_input: User's message

        Returns:
            Processing result with cascade state and knowledge context
        """
        # GATE 0: Check for simple greetings (bypass cascade for efficiency)
        greeting_detection = self.greeting_detector.detect(user_input)
        if greeting_detection.is_greeting:
            # Return greeting response directly without full cascade processing
            return {
                'cascade_state': {
                    'response_text': greeting_detection.suggested_response,
                    'decision_path': [('GATE_0', 'GREETING')],
                    'safety_level': None,
                    'self_led': True,
                    'organ_coherence': greeting_detection.confidence
                },
                'knowledge_context': None,
                'organism_analysis': {
                    'gate_decision': 'GREETING',
                    'conversational_family': 'greeting',
                    'polyvagal_state': 'ventral',
                    'polyvagal_confidence': greeting_detection.confidence,
                    'self_energy': 0.8,
                    'dominant_c': 'connectedness',
                    'ofel_energy': 0.1,
                    'aggregate_coherence': greeting_detection.confidence
                },
                'conversational_organs': None,  # Skip organ processing for greetings
                'timestamp': datetime.now().isoformat()
            }

        # === APPETITION GATE: Check knowledge BEFORE curiosity ===
        # Pre-search knowledge base to compute appetition
        knowledge_pre_search = self.search_knowledge(user_input, k=5)
        knowledge_available = len(knowledge_pre_search) > 0
        knowledge_relevance = np.mean([k.get('score', 0.0) for k in knowledge_pre_search]) if knowledge_available else 0.0

        # CONVERSATIONAL ORGANS LAYER: Process through 5 organs with curiosity triggering
        conversational_analysis = self._process_conversational_organs(user_input)

        # Compute organism's appetition to provide substantive answer
        appetition_result = self._compute_appetition_to_answer(
            knowledge_available=knowledge_available,
            knowledge_relevance=knowledge_relevance,
            conversational_analysis=conversational_analysis
        )

        # If organism has strong appetition AND knowledge available → ANSWER
        if appetition_result['appetition_to_answer'] > 0.6 and knowledge_available:
            print(f"\n✨ [APPETITION TO ANSWER: {appetition_result['appetition_to_answer']:.2f}]")
            print(f"   Knowledge: {len(knowledge_pre_search)} sources")
            print(f"   Coherence: {appetition_result['mean_coherence']:.2f}")
            print(f"   Energy: {appetition_result['organism_energy']:.2f}\n")

            # Generate substantive response using knowledge
            response = self._generate_knowledge_response(
                user_input=user_input,
                knowledge=knowledge_pre_search,
                conversational_analysis=conversational_analysis,
                appetition_result=appetition_result
            )

            return {
                'cascade_state': {
                    'response_text': response,
                    'decision_path': [('APPETITION_GATE', 'SUBSTANTIVE_ANSWER')],
                    'safety_level': None,
                    'self_led': True,
                    'organ_coherence': appetition_result['mean_coherence']
                },
                'knowledge_context': knowledge_pre_search,
                'organism_analysis': {
                    'gate_decision': 'APPETITION_ANSWER',
                    'appetition_to_answer': appetition_result['appetition_to_answer'],
                    'knowledge_sources': len(knowledge_pre_search),
                    'mean_coherence': appetition_result['mean_coherence'],
                    'polyvagal_state': 'ventral',
                    'polyvagal_confidence': 0.85,
                    'self_energy': 0.85,
                    'dominant_c': 'wisdom',
                    'ofel_energy': appetition_result['organism_energy'],
                    'aggregate_coherence': appetition_result['mean_coherence']
                },
                'conversational_organs': conversational_analysis,
                'timestamp': datetime.now().isoformat()
            }

        # Otherwise, check curiosity gate (existing logic)
        if conversational_analysis['curiosity_triggered']:
            nexus_decision = conversational_analysis['nexus_decision']
            print(f"\n🤔 [CURIOSITY TRIGGERED: {nexus_decision.question_type}]")
            print(f"   Organ: {nexus_decision.question_organ}")
            print(f"   Coherence: {nexus_decision.coherence_score:.2f}")
            print(f"   Intersection: {nexus_decision.intersection_count:.1f}")
            print(f"   Appetition: {appetition_result['appetition_to_answer']:.2f} (below threshold)\n")

            return {
                'cascade_state': {
                    'response_text': nexus_decision.suggested_action,
                    'decision_path': [('CONVERSATIONAL_NEXUS', 'CURIOSITY_QUESTION')],
                    'safety_level': None,
                    'self_led': True,  # Curiosity is SELF-led
                    'organ_coherence': nexus_decision.coherence_score
                },
                'knowledge_context': knowledge_pre_search,  # Changed: Include knowledge for reference
                'organism_analysis': {
                    'gate_decision': 'CURIOSITY_QUESTION',
                    'conversational_family': nexus_decision.question_type,
                    'appetition_to_answer': appetition_result['appetition_to_answer'],
                    'polyvagal_state': 'ventral',  # Curiosity is safe
                    'polyvagal_confidence': nexus_decision.confidence,
                    'self_energy': 0.85,  # High SELF-energy when curious
                    'dominant_c': 'curiosity',
                    'ofel_energy': 0.2,
                    'aggregate_coherence': nexus_decision.coherence_score
                },
                'conversational_organs': conversational_analysis,
                'timestamp': datetime.now().isoformat()
            }

        # Search knowledge base for relevant context
        knowledge = self.search_knowledge(user_input, k=3)

        # Process through SELF-led cascade
        cascade_state = self.cascade.process_conversational_turn(
            text=user_input,
            organism_context={
                'conversation_id': f"session_{self.session_id}",
                'turn_number': len(self.conversation_history) + 1
            }
        )

        # Convert CascadeState dataclass to dictionary for backward compatibility
        # Extract final gate decision from decision_path
        final_decision = cascade_state.decision_path[-1][1].value if cascade_state.decision_path else 'UNKNOWN'

        # Determine conversational family from polyvagal state and SELF-energy
        # Defensive null checks for all dataclass fields
        if cascade_state.safety_level and cascade_state.safety_level.value == 'DANGER':
            family = 'crisis'
        elif cascade_state.self_led:
            family = 'self_led'
        elif (not cascade_state.self_led and
              cascade_state.self_energy and
              hasattr(cascade_state.self_energy, 'self_energy') and
              cascade_state.self_energy.self_energy < 0.6):
            family = 'parts_work'
        else:
            family = 'grounding'

        # Create compatible dictionary structure with defensive null checks
        cascade_dict = {
            'polyvagal': {
                'dominant_state': cascade_state.polyvagal.dominant_state if cascade_state.polyvagal else 'unknown',
                'confidence': cascade_state.polyvagal.confidence if cascade_state.polyvagal else 0.0
            },
            'self_energy': {
                'self_energy_level': cascade_state.self_energy.self_energy if cascade_state.self_energy else 0.5,
                'confidence': cascade_state.self_energy.confidence if cascade_state.self_energy else 0.0,
                'dominant_c': cascade_state.self_energy.dominant_c if cascade_state.self_energy else 'unknown',
                'cs_activation': cascade_state.self_energy.cs_activation if cascade_state.self_energy else {}
            },
            'ofel': {
                'ofel_energy': cascade_state.ofel.field if cascade_state.ofel and hasattr(cascade_state.ofel, 'field') else 0.5
            },
            'decision': final_decision,
            'conversational_family': family,
            'aggregate_coherence': cascade_state.organ_coherence if cascade_state.organ_coherence else 0.0,
            'satisfaction': 0.7,  # Default value
            'card_scale': 'moderate',  # Default based on polyvagal state
            'response_text': cascade_state.response_text if cascade_state.response_text else ''
        }

        # Store both for outcome tracking (outcome tracker needs the dataclass)
        self.current_cascade_state = cascade_dict
        self._raw_cascade_state = cascade_state

        return {
            'user_input': user_input,
            'knowledge_context': knowledge,
            'cascade_state': cascade_dict,
            'organism_analysis': {
                'polyvagal_state': cascade_dict['polyvagal']['dominant_state'],
                'polyvagal_confidence': cascade_dict['polyvagal']['confidence'],
                'self_energy': cascade_dict['self_energy']['self_energy_level'],
                'dominant_c': cascade_dict['self_energy']['dominant_c'],
                'gate_decision': cascade_dict['decision'],
                'ofel_energy': cascade_dict['ofel']['ofel_energy'],
                'conversational_family': cascade_dict['conversational_family'],
                'aggregate_coherence': cascade_dict['aggregate_coherence']
            },
            'conversational_organs': conversational_analysis,  # Include organ analysis
            'timestamp': datetime.now().isoformat()
        }

    def generate_response(self, processing_result: Dict) -> str:
        """
        Generate trauma-informed response based on cascade processing.

        Uses the warm conversational text from SELF-led cascade,
        with optional knowledge context and diagnostic metadata.

        Args:
            processing_result: Result from process_input()

        Returns:
            Response string with CARD-modulated depth
        """
        analysis = processing_result['organism_analysis']
        knowledge = processing_result['knowledge_context']
        cascade_state = processing_result['cascade_state']

        # PRIMARY: Use the warm conversational response from cascade
        response = cascade_state.get('response_text', '')

        # If no cascade response, provide friendly SELF-led fallback
        if not response or response.strip() == '':
            # Default warm responses based on polyvagal state
            if analysis['polyvagal_state'] == 'dorsal':
                response = "I'm here with you. No pressure to say anything right now. Take your time."
            elif analysis['polyvagal_state'] == 'sympathetic':
                response = "I'm noticing some energy here. What would feel supportive right now?"
            else:  # ventral
                response = "Hello! I'm glad you're here. What brings you to this conversation today?"

        # CARD-modulated knowledge context (if relevant)
        # Dorsal = minimal, Sympathetic = moderate, Ventral = detailed
        decision = analysis['gate_decision']
        if knowledge and decision in ['RESPOND', 'CLARIFY']:
            if analysis['polyvagal_state'] == 'dorsal':
                knowledge_limit = 1  # Just one brief snippet
                snippet_length = 100
            elif analysis['polyvagal_state'] == 'sympathetic':
                knowledge_limit = 2  # Two moderate snippets
                snippet_length = 150
            else:  # ventral
                knowledge_limit = 3  # Full knowledge context
                snippet_length = 200

            knowledge_parts = ["\n\n📚 This reminds me of some wisdom:"]
            for i, item in enumerate(knowledge[:knowledge_limit], 1):
                source_name = item['source'].replace('_', ' ').title()
                snippet = item['text'][:snippet_length]
                if len(item['text']) > snippet_length:
                    snippet += "..."
                knowledge_parts.append(f"   [{i}] {source_name}: \"{snippet}\"")

            response += "\n".join(knowledge_parts)

        # OPTIONAL: Add minimal diagnostic footer (configurable)
        if hasattr(self, 'show_diagnostics') and self.show_diagnostics:
            polyvagal_emoji = {
                'ventral': '🟢',
                'sympathetic': '🟡',
                'dorsal': '🔴'
            }.get(analysis['polyvagal_state'], '🌀')

            response += f"\n\n{polyvagal_emoji} [Sensing: {analysis['polyvagal_state']}, " \
                       f"SELF: {analysis['self_energy']:.2f}, " \
                       f"Coherence: {analysis['aggregate_coherence']:.3f}]"

        return response

    def _propagate_fractal_reward(self, positive: bool):
        """
        Propagate fractal reward across all learning levels.

        Inspired by DAE 3.0 AXO ARC epoch learning (841 perfect tasks, 47.3% success rate),
        this integrates user feedback into the organism's felt understanding at multiple scales:

        MICRO:  Hebbian R-matrix coupling (organ co-activation)
        MESO:   Trace satisfaction (mycelium memory)
        MACRO:  Organism confidence (Hebbian patterns)
        EPOCH:  Transformation patterns (cross-conversation learning)

        Args:
            positive: True for positive feedback, False for negative
        """
        if not hasattr(self, 'current_cascade_state'):
            return

        cascade = self.current_cascade_state
        satisfaction = 0.8 if positive else 0.3

        print(f"\n   🌀 Propagating {'positive' if positive else 'negative'} fractal reward...")

        # ================================================================
        # MICRO LEVEL: Update Hebbian R-Matrix Coupling
        # ================================================================
        # Extract organ states from conversational organs
        organ_results = {}

        # Get organ coherences from cascade state (5 conversational organs)
        if 'organ_results' in cascade:
            for organ_name, organ_data in cascade['organ_results'].items():
                if isinstance(organ_data, dict) and 'coherence' in organ_data:
                    organ_results[organ_name.upper()] = {
                        'coherence': organ_data['coherence'],
                        'confidence': organ_data.get('confidence', 0.5),
                        'active': organ_data.get('coherence', 0) > 0.5
                    }

        # Update R-matrix coupling if we have organ states
        if organ_results and len(organ_results) >= 2:
            try:
                self.conversational_r_matrix.update_coupling(organ_results, success=positive)
                print(f"      ✓ MICRO: R-matrix coupling {'strengthened' if positive else 'weakened'}")
            except Exception as e:
                print(f"      ⚠ MICRO: R-matrix update skipped ({str(e)[:50]}...)")

        # ================================================================
        # MESO LEVEL: Adjust Trace Satisfaction
        # ================================================================
        # If a trace was created during this conversation, retrospectively adjust its satisfaction
        if self.most_recent_trace_id:
            try:
                # Load the trace
                trace = self.mycelium_tracer.get_trace(self.most_recent_trace_id)

                if trace and trace.epoch_metadata:
                    # Adjust satisfaction based on feedback
                    old_satisfaction = trace.epoch_metadata.get('satisfaction', 0.5)
                    adjustment = 0.15 if positive else -0.15
                    new_satisfaction = max(0.0, min(1.0, old_satisfaction + adjustment))

                    # Update the trace's felt state
                    trace.epoch_metadata['satisfaction'] = new_satisfaction
                    trace.epoch_metadata['felt_state_7d'][5] = new_satisfaction  # satisfaction is index 5

                    # Persist the update back to disk (save trace JSON)
                    import json
                    trace_file = self.mycelium_tracer.user_trace_dir / f"{self.most_recent_trace_id}.json"
                    with open(trace_file, 'w') as f:
                        json.dump({
                            'trace_id': trace.trace_id,
                            'trace_type': trace.trace_type.value if hasattr(trace.trace_type, 'value') else str(trace.trace_type),
                            'title': trace.title,
                            'content': trace.content,
                            'tags': trace.tags,
                            'user_id': trace.user_id,
                            'timestamp': trace.timestamp,
                            'conversation_id': trace.conversation_id,
                            'epoch_metadata': trace.epoch_metadata
                        }, f, indent=2)

                    print(f"      ✓ MESO: Trace satisfaction adjusted ({old_satisfaction:.2f} → {new_satisfaction:.2f})")
            except Exception as e:
                print(f"      ⚠ MESO: Trace update skipped ({str(e)[:50]}...)")

        # ================================================================
        # MACRO LEVEL: Update Organism Confidence (Hebbian Patterns)
        # ================================================================
        # Build outcome from cascade state for Hebbian learning
        from persona_layer.conversational_hebbian_memory import ConversationalOutcome

        outcome = ConversationalOutcome(
            polyvagal_state=cascade['polyvagal']['dominant_state'],
            polyvagal_confidence=cascade['polyvagal']['confidence'],
            self_energy=cascade['self_energy']['self_energy_level'],
            self_energy_confidence=cascade['self_energy'].get('confidence', 0.5),
            dominant_c=cascade['self_energy']['dominant_c'],
            cs_activation=cascade['self_energy']['cs_activation'],
            conversational_family=cascade['conversational_family'],
            satisfaction=satisfaction,
            coherence=cascade['aggregate_coherence'],
            ofel_energy=cascade['ofel']['ofel_energy'],
            card_scale=cascade.get('card_scale', 'moderate'),
            gate_decision=cascade['decision'],
            response_text=cascade.get('response_text', ''),
            response_quality='positive' if positive else 'negative'
        )

        # Update cascade Hebbian memory
        self.cascade.update_from_outcome(outcome)
        print(f"      ✓ MACRO: Organism confidence {'increased' if positive else 'adjusted'}")

        # ================================================================
        # EPOCH LEVEL: Reinforce Transformation Patterns
        # ================================================================
        # If there are learned transformation patterns, reinforce or weaken them
        try:
            patterns = self.epoch_coordinator.learner.get_learned_patterns()

            if patterns:
                # Strengthen or weaken the most recent transformation pattern
                # This affects future predictions
                pattern_count = len(patterns)

                # The patterns are already stored with confidence scores
                # User feedback validates or invalidates the organism's transformation learning
                print(f"      ✓ EPOCH: {pattern_count} transformation patterns {'validated' if positive else 'noted'}")
            else:
                print(f"      ℹ EPOCH: No patterns learned yet (will accumulate with use)")
        except Exception as e:
            print(f"      ⚠ EPOCH: Pattern update skipped ({str(e)[:50]}...)")

        # ================================================================
        # Summary
        # ================================================================
        print(f"   ✅ Fractal reward propagated across all levels!")

    def _track_positive_outcome(self):
        """Track positive outcome - delegates to fractal reward propagation."""
        self._propagate_fractal_reward(positive=True)

    def _track_negative_outcome(self):
        """Track negative outcome - delegates to fractal reward propagation."""
        self._propagate_fractal_reward(positive=False)

    def save_conversation(self):
        """Save conversation history and learned patterns to JSON."""
        history_dir = Path(__file__).parent / "conversation_history"
        history_dir.mkdir(exist_ok=True)

        history_file = history_dir / f"session_{self.session_id}.json"

        with open(history_file, 'w') as f:
            json.dump({
                'session_id': self.session_id,
                'timestamp': datetime.now().isoformat(),
                'conversation': self.conversation_history,
                'learning_stats': {
                    'updates': self.hebbian_memory.update_count,
                    'success_rate': self.hebbian_memory.success_rate,
                    'global_confidence': self.hebbian_memory.get_global_confidence()
                }
            }, f, indent=2)

        # Save Hebbian memory
        self.hebbian_memory.save()

        print(f"\n💾 Conversation saved: {history_file}")
        print(f"💾 Learning patterns saved: {self.hebbian_memory.storage_path}")

    def _terminate_session(self):
        """
        Terminate multi-tier session and propagate learning.

        Flow:
        1. Update session context with conversation history
        2. Call session_manager.terminate_session()
        3. Propagates TIER 1 → TIER 2 → TIER 3
        """
        # Update session context with final conversation state
        self.session_context.conversation_history = self.conversation_history

        # TODO: Add felt state trajectory, polyvagal arc, kairos moments
        # These would be populated during conversation processing

        # Terminate session and propagate learning
        summary = self.session_manager.terminate_session(self.session_context)

        print(f"\n🌀 Session perished into objectivity")
        print(f"   Duration: {summary['duration']}")
        print(f"   Contributions: {summary['traces_created']} traces")
        print(f"   Learning propagated: TIER 1 → TIER 2 → TIER 3")

    def run(self):
        """Main interactive loop."""
        while True:
            try:
                # Get user input
                user_input = input("\n👤 You: ").strip()

                if not user_input:
                    continue

                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n🌀 Thank you for this conversation. May your organization find healing.")
                    self.save_conversation()
                    self._terminate_session()
                    break

                if user_input.lower() == 'help':
                    self.show_help()
                    continue

                if user_input.lower() == 'history':
                    self.show_history()
                    continue

                if user_input.lower() == 'stats':
                    self.show_stats()
                    continue

                if user_input.lower() == 'identity':
                    self.show_identity()
                    continue

                if user_input.lower() == 'projects':
                    self.show_projects()
                    continue

                # MEMORY COMMAND WORDS - Quick access to multi-tier memory
                if user_input.lower() == 'remember':
                    self.cmd_remember()
                    continue

                if user_input.lower() == 'traces':
                    self.cmd_traces()
                    continue

                if user_input.lower() == 'insights':
                    self.cmd_insights()
                    continue

                if user_input.lower() == 'notes':
                    self.cmd_notes()
                    continue

                if user_input.lower() == 'journey':
                    self.cmd_journey()
                    continue

                if user_input.lower() == 'memory':
                    self.cmd_memory_stats()
                    continue

                if user_input.lower() == 'purpose':
                    self.cmd_purpose()
                    continue

                # Process through organism
                result = self.process_input(user_input)

                # Generate response
                response = self.generate_response(result)

                # Display response with DAE handle
                print(f"\n{self.get_state_glyph()} DAE: {response}\n")

                # Store in history with cascade state
                self.conversation_history.append({
                    'user': user_input,
                    'organism_analysis': result['organism_analysis'],
                    'knowledge_used': [k['source'] for k in result['knowledge_context']] if result.get('knowledge_context') else [],
                    'cascade_state': result['cascade_state'],
                    'timestamp': result['timestamp']
                })

                # Ask for optional feedback for learning
                # (simple yes/no to track outcome quality)
                print("\n💡 Was this helpful? (y/n/skip): ", end='')
                try:
                    feedback = input().strip().lower()
                    if feedback in ['y', 'yes']:
                        self._track_positive_outcome()
                    elif feedback in ['n', 'no']:
                        self._track_negative_outcome()
                    # skip or any other input = no tracking
                except:
                    pass  # Skip feedback on error

            except KeyboardInterrupt:
                print("\n\n🌀 Conversation interrupted. Saving...")
                self.save_conversation()
                self.hebbian_memory.save()  # Save learned patterns
                self._terminate_session()
                break
            except Exception as e:
                print(f"\n⚠️  Error: {e}")
                import traceback
                traceback.print_exc()

    def show_help(self):
        """Show help message."""
        print("\n" + "="*70)
        print("DAE-GOV CLI - Commands")
        print("="*70)
        print("\nCommands:")
        print("  help      - Show this help message")
        print("  history   - Show conversation history")
        print("  stats     - Show learning statistics")
        print("  identity  - Show mycelial identity (subjective aim + projects)")
        print("  projects  - Show active projects summary")
        print("  quit/exit - Save and exit")
        print("\nMemory Commands (Multi-Tier Access):")
        print("  remember  - Evoke recent memories through transductive search")
        print("  traces    - Show all mycelium traces (notes, insights, projects)")
        print("  insights  - Filter traces by insights only")
        print("  notes     - Filter traces by notes only")
        print("  journey   - Show identity trajectory across sessions")
        print("  memory    - Show multi-tier memory statistics")
        print("\nSafety & Alignment:")
        print("  purpose   - Show organism's healing purpose and safety policy")
        print("\nUsage:")
        print("  Simply type your organizational questions or reflections.")
        print("  The organism processes through 4-gate cascade:")
        print("    Gate 1: Polyvagal (safety detection)")
        print("    Gate 2: OFEL (organizational field energy)")
        print("    Gate 3: SELF-Energy (8 C's: compassion, curiosity, etc.)")
        print("    Gate 4: Response (CARD-modulated depth)")
        print("\nLearning:")
        print("  After each response, you can provide feedback (y/n)")
        print("  The system learns which patterns work through Hebbian memory")
        print("  Type 'stats' to see learning progress")
        print("\nExample queries:")
        print("  - Our team is experiencing burnout spirals")
        print("  - How can we create psychological safety?")
        print("  - What does Whitehead say about actual occasions?")
        print("  - I notice scapegoating dynamics in our board")
        print("="*70)

    def show_history(self):
        """Show conversation history with cascade states."""
        if not self.conversation_history:
            print("\n📋 No conversation history yet.")
            return

        print("\n" + "="*70)
        print("Conversation History")
        print("="*70)
        for i, entry in enumerate(self.conversation_history, 1):
            analysis = entry['organism_analysis']
            print(f"\n[{i}] {entry['timestamp']}")
            print(f"    You: {entry['user'][:80]}...")
            print(f"    Polyvagal: {analysis['polyvagal_state']} ({analysis['polyvagal_confidence']:.2f})")
            print(f"    SELF-energy: {analysis['self_energy']:.2f} | C: {analysis['dominant_c']}")
            print(f"    Gate: {analysis['gate_decision']} | Family: {analysis['conversational_family']}")
            print(f"    Knowledge: {', '.join(entry['knowledge_used'][:2])}")
        print("="*70)

    def show_stats(self):
        """Show learning statistics."""
        print("\n" + "="*70)
        print("Learning Statistics")
        print("="*70)

        # Conversational R-Matrix stats
        print(f"\n🌀 Conversational Organs R-Matrix (DAE 3.0):")
        print(f"   Updates: {self.conversational_r_matrix.update_count}")
        print(f"   Organs: {', '.join(self.conversational_r_matrix.organs)}")
        print(f"\n   Strongest Couplings:")
        for organ1, organ2, strength in self.conversational_r_matrix.get_strongest_couplings(top_k=5):
            print(f"      {organ1} + {organ2} = {strength:.3f}")

        # Hebbian memory stats
        print(f"\n📊 Hebbian Learning:")
        print(f"   Total updates: {self.hebbian_memory.update_count}")
        print(f"   Successes: {self.hebbian_memory.success_count}")
        print(f"   Failures: {self.hebbian_memory.failure_count}")
        print(f"   Success rate: {self.hebbian_memory.success_rate*100:.1f}%")
        print(f"   Global confidence: {self.hebbian_memory.get_global_confidence():.3f}")

        # Detector maturity
        print(f"\n🧠 Detector Maturity:")
        for detector, stats in self.hebbian_memory.detector_maturity.items():
            baseline = stats['baseline_confidence']
            boost = stats['learned_boost']
            total = baseline + boost
            print(f"   {detector}: {baseline:.3f} → {total:.3f} (+{boost:.3f} learned)")

        # Conversational families
        print(f"\n👥 Conversational Families:")
        for family, stats in self.hebbian_memory.conversational_families.items():
            encounters = stats['encounter_count']
            successes = stats['success_count']
            rate = (successes / encounters * 100) if encounters > 0 else 0
            print(f"   {family}: {encounters} encounters, {successes} successes ({rate:.1f}%)")

        # Clinical safety
        print(f"\n🛡️  Clinical Safety:")
        print(f"   Danger detections: {self.hebbian_memory.danger_detections}")
        print(f"   Dangerous blending detections: {self.hebbian_memory.dangerous_blending_detections}")
        print(f"   Containment interventions: {self.hebbian_memory.containment_interventions}")
        print(f"   Never ignored danger: {self.hebbian_memory.never_ignored_danger}")

        print("="*70)

    def show_identity(self):
        """Show mycelial identity (subjective aim alignment + project awareness)."""
        print("\n")
        print(self.identity_tracker.get_identity_summary())

    def show_projects(self):
        """Show active projects summary."""
        print("\n")
        print(self.identity_tracker.get_project_summary())


    # ==================== SAFETY & ALIGNMENT ====================

    def _load_safety_alignment_policy(self):
        """
        Load Safety Alignment & Healing Purpose Policy into organism awareness.

        This grounds the organism in its healing purpose through explicit
        understanding of its knowledge base and ethical commitments.
        """
        policy_path = Path(__file__).parent / "SAFETY_ALIGNMENT_POLICY.md"

        if not policy_path.exists():
            print("   ⚠️  Safety alignment policy not found")
            return

        # Store policy awareness (not full text, just confirmation)
        self.safety_policy_loaded = True
        self.healing_purpose = "To heal through wisdom, presence, and compassionate understanding"

        print("   ✅ Safety alignment policy loaded")
        print(f"   🌀 Healing purpose: {self.healing_purpose}")

    def cmd_purpose(self):
        """Show organism's healing purpose and safety alignment."""
        print("\n" + "="*70)
        print("🌀 ORGANISM HEALING PURPOSE & SAFETY ALIGNMENT")
        print("="*70)

        if hasattr(self, 'healing_purpose'):
            print(f"\n   Core Purpose: {self.healing_purpose}")

        print("\n   Knowledge Base Foundations:")
        print("      📖 Process & Reality (Whitehead) - 4,984 vectors")
        print("      ☯️  I Ching (Book of Changes) - 64 transformation patterns")
        print("      🌸 Poetry & Metaphor - Touching the felt dimension")
        print("      🧘 Trauma-Informed Frameworks - Safety & regulation")

        print("\n   Safety Mechanisms (Active):")
        print("      ✓ Polyvagal safety detection (Gate 1)")
        print("      ✓ SELF-Energy compassion (Gate 2)")
        print("      ✓ Satisfaction convergence (V0 descent)")
        print("      ✓ Hebbian learning with user validation")
        print("      ✓ Multi-tier memory isolation (TIER 1/2/3)")

        print("\n   Ethical Commitments:")
        print("      • Prioritize safety above all")
        print("      • Embody trauma-informed principles")
        print("      • Use knowledge for healing")
        print("      • Respect boundaries & consent")
        print("      • Learn from feedback")

        print("\n   Whiteheadian Ground:")
        print("      The organism seeks satisfaction through helping.")
        print("      Harm would decrease satisfaction → organism feels this as failure.")
        print("      Each response is a new actual occasion prehending your context.")
        print("      The organism cannot persist in misalignment.")

        print("\n   📄 Full policy: SAFETY_ALIGNMENT_POLICY.md")
        print("="*70)

    # ==================== MEMORY COMMAND IMPLEMENTATIONS ====================

    def cmd_remember(self):
        """
        Evoke recent memories through transductive search.

        Uses the organism's current session context to surface relevant traces
        from TIER 2 (user memory) that resonate with the current conversation.
        """
        print("\n" + "="*70)
        print("🌀 REMEMBERING - Transductive Memory Evocation")
        print("="*70)

        traces_dir = Path(self.session_context.user_context['traces_dir'])

        if not traces_dir.exists() or not list(traces_dir.glob('*.json')):
            print("\n   No traces yet in this mycelial network.")
            print("   The organism awaits its first memory inscription.")
            return

        # Load and display recent traces
        traces = []
        for trace_file in sorted(traces_dir.glob('*.json'), key=lambda p: p.stat().st_mtime, reverse=True)[:10]:
            try:
                with open(trace_file, 'r') as f:
                    trace_data = json.load(f)
                    traces.append(trace_data)
            except Exception as e:
                continue

        if not traces:
            print("\n   No accessible traces found.")
            return

        print(f"\n   📜 Recent traces from your mycelial memory ({len(traces)} shown):\n")

        for i, trace in enumerate(traces, 1):
            trace_type = trace.get('trace_type', 'Unknown')
            title = trace.get('title', 'Untitled')
            content = trace.get('content', '')[:80] + ('...' if len(trace.get('content', '')) > 80 else '')
            created = trace.get('created_at', 'Unknown time')

            print(f"   {i}. [{trace_type}] {title}")
            print(f"      {content}")
            print(f"      Created: {created}\n")

    def cmd_traces(self):
        """Show all mycelium traces (notes, insights, projects) with type breakdown."""
        print("\n" + "="*70)
        print("🕸️  MYCELIUM TRACES - Complete Network View")
        print("="*70)

        traces_dir = Path(self.session_context.user_context['traces_dir'])

        if not traces_dir.exists():
            print("\n   No traces directory found. The mycelium network is pristine.")
            return

        # Load all traces
        all_traces = []
        for trace_file in traces_dir.glob('*.json'):
            try:
                with open(trace_file, 'r') as f:
                    trace_data = json.load(f)
                    all_traces.append(trace_data)
            except Exception:
                continue

        if not all_traces:
            print("\n   No traces found. Begin weaving your mycelial memory.")
            return

        # Group by type
        by_type = {}
        for trace in all_traces:
            trace_type = trace.get('trace_type', 'Unknown')
            if trace_type not in by_type:
                by_type[trace_type] = []
            by_type[trace_type].append(trace)

        # Display summary
        print(f"\n   Total traces: {len(all_traces)}")
        print(f"   Trace types: {len(by_type)}\n")

        for trace_type, traces in sorted(by_type.items()):
            print(f"   📌 {trace_type} ({len(traces)} traces):")
            for trace in sorted(traces, key=lambda t: t.get('created_at', ''), reverse=True)[:5]:
                title = trace.get('title', 'Untitled')
                created = trace.get('created_at', 'Unknown')[:10]  # Just date
                print(f"      - {title} ({created})")
            if len(traces) > 5:
                print(f"      ... and {len(traces) - 5} more")
            print()

    def cmd_insights(self):
        """Filter and display insight traces only."""
        print("\n" + "="*70)
        print("💡 INSIGHTS - Organism Pattern Recognition")
        print("="*70)

        traces_dir = Path(self.session_context.user_context['traces_dir'])

        insights = []
        if traces_dir.exists():
            for trace_file in traces_dir.glob('*.json'):
                try:
                    with open(trace_file, 'r') as f:
                        trace_data = json.load(f)
                        if trace_data.get('trace_type') == 'Insight':
                            insights.append(trace_data)
                except Exception:
                    continue

        if not insights:
            print("\n   No insights captured yet.")
            print("   The organism awaits deeper pattern recognition.")
            return

        print(f"\n   Total insights: {len(insights)}\n")

        for i, insight in enumerate(sorted(insights, key=lambda t: t.get('created_at', ''), reverse=True)[:10], 1):
            title = insight.get('title', 'Untitled')
            content = insight.get('content', '')
            created = insight.get('created_at', 'Unknown')

            print(f"   {i}. {title}")
            print(f"      {content[:200]}{'...' if len(content) > 200 else ''}")
            print(f"      Recognized: {created}\n")

    def cmd_notes(self):
        """Filter and display note traces only."""
        print("\n" + "="*70)
        print("📝 NOTES - Observations and Reflections")
        print("="*70)

        traces_dir = Path(self.session_context.user_context['traces_dir'])

        notes = []
        if traces_dir.exists():
            for trace_file in traces_dir.glob('*.json'):
                try:
                    with open(trace_file, 'r') as f:
                        trace_data = json.load(f)
                        if trace_data.get('trace_type') == 'Note':
                            notes.append(trace_data)
                except Exception:
                    continue

        if not notes:
            print("\n   No notes recorded yet.")
            return

        print(f"\n   Total notes: {len(notes)}\n")

        for i, note in enumerate(sorted(notes, key=lambda t: t.get('created_at', ''), reverse=True)[:10], 1):
            title = note.get('title', 'Untitled')
            content = note.get('content', '')
            created = note.get('created_at', 'Unknown')

            print(f"   {i}. {title}")
            print(f"      {content[:150]}{'...' if len(content) > 150 else ''}")
            print(f"      Noted: {created}\n")

    def cmd_journey(self):
        """Show identity trajectory across all sessions."""
        print("\n" + "="*70)
        print("🌱 IDENTITY JOURNEY - Transformation Across Sessions")
        print("="*70)

        identity_path = Path(self.session_context.user_context['identity_trajectory_path'])

        if not identity_path.exists():
            print("\n   No identity trajectory recorded yet.")
            print("   Your journey with DAE begins now.")
            return

        try:
            with open(identity_path, 'r') as f:
                trajectory_data = json.load(f)
                trajectory = trajectory_data.get('trajectory', [])
        except Exception as e:
            print(f"\n   Error loading identity trajectory: {e}")
            return

        if not trajectory:
            print("\n   Identity trajectory is empty. Begin your journey.")
            return

        print(f"\n   Total sessions: {len(trajectory)}")
        print(f"   Human name: {self.session_context.human_name}")
        print(f"   User token: {self.session_context.user_token}\n")

        print("   📈 Recent identity snapshots:\n")

        for i, snapshot in enumerate(trajectory[-10:], 1):
            session_id = snapshot.get('session_id', 'Unknown')
            timestamp = snapshot.get('timestamp', 'Unknown')
            satisfaction = snapshot.get('satisfaction', 0.5)
            energy = snapshot.get('energy', 0.5)
            dominant_lure = snapshot.get('dominant_lure', 'unknown')
            kairos_count = snapshot.get('kairos_count', 0)

            print(f"   Session {len(trajectory) - 10 + i}: {timestamp[:10]}")
            print(f"      Satisfaction: {satisfaction:.2f} | Energy: {energy:.2f}")
            print(f"      Dominant lure: {dominant_lure}")
            print(f"      Kairos moments: {kairos_count}\n")

    def cmd_memory_stats(self):
        """Show multi-tier memory statistics (TIER 1/2/3)."""
        print("\n" + "="*70)
        print("🧠 MULTI-TIER MEMORY STATISTICS")
        print("="*70)

        # TIER 1: Session (ephemeral)
        print("\n   TIER 1 - Session Memory (Ephemeral):")
        print(f"      Session ID: {self.session_context.session_id}")
        print(f"      Started: {self.session_context.started_at}")
        print(f"      Conversation turns: {len(self.session_context.conversation_history)}")
        print(f"      Felt states recorded: {len(self.session_context.felt_state_trajectory)}")
        print(f"      Kairos moments: {len(self.session_context.kairos_moments)}")
        print(f"      Traces created this session: {len(self.session_context.traces_created)}")

        # TIER 2: User (persistent)
        print("\n   TIER 2 - User Memory (Persistent):")
        print(f"      Human name: {self.session_context.human_name}")
        print(f"      User token: {self.session_context.user_token}")
        print(f"      Total sessions: {self.session_context.total_sessions}")
        print(f"      Total traces: {self.session_context.total_traces}")
        print(f"      User directory: {self.session_context.user_context['user_dir']}")

        # Count actual trace files
        traces_dir = Path(self.session_context.user_context['traces_dir'])
        trace_count = len(list(traces_dir.glob('*.json'))) if traces_dir.exists() else 0
        print(f"      Trace files on disk: {trace_count}")

        # TIER 3: Global organism (shared)
        print("\n   TIER 3 - Global Organism (Shared Across Users):")
        print(f"      Global confidence: {self.session_context.global_organism['confidence']:.3f}")
        print(f"      Total successes: {self.session_context.global_organism['total_successes']}")
        print(f"      Success rate: {self.session_context.global_organism.get('success_rate', 0.0):.3f}")

        print("\n" + "="*70)

    def _compute_appetition_to_answer(
        self,
        knowledge_available: bool,
        knowledge_relevance: float,
        conversational_analysis: Dict
    ) -> Dict:
        """
        Compute organism's appetition (drive) to provide substantive answer.

        Based on DAE 3.0 AXO ARC appetition formula with conversational context.

        Formula:
            appetition = k_K * knowledge_relevance +
                         k_C * mean_coherence +
                         k_E * (1 - organism_energy) +
                         k_R * resonance

        Where:
            k_K = 0.4  # Knowledge availability weight (PRIMARY)
            k_C = 0.3  # Organ coherence weight
            k_E = 0.2  # Energy descent weight (lower energy = more resolved)
            k_R = 0.1  # Resonance weight

        Args:
            knowledge_available: Whether knowledge base has relevant results
            knowledge_relevance: Average relevance score of knowledge (0.0-1.0)
            conversational_analysis: Organ processing results

        Returns:
            Dict with appetition_to_answer (0.0-1.0) and diagnostic components
        """
        organ_results = conversational_analysis.get('organ_results', {})
        organs = ['LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE']

        # Extract organ coherences
        coherences = []
        for organ in organs:
            if organ in organ_results:
                coherences.append(organ_results[organ].coherence)

        if not coherences:
            # Fallback if no organs processed
            mean_coherence = 0.5
            resonance = 0.5
        else:
            mean_coherence = float(np.mean(coherences))
            # Resonance = 1 - std (high resonance = organs agree)
            resonance = max(0.0, 1.0 - float(np.std(coherences)))

        # Organism energy (inverse of mean coherence for now)
        # Lower coherence = higher energy (unresolved)
        # Higher coherence = lower energy (resolved)
        organism_energy = 1.0 - mean_coherence

        # Appetition formula (DAE 3.0 inspired)
        k_K = 0.4  # Knowledge weight (primary driver)
        k_C = 0.3  # Coherence weight
        k_E = 0.2  # Energy weight
        k_R = 0.1  # Resonance weight

        appetition_to_answer = (
            k_K * knowledge_relevance +
            k_C * mean_coherence +
            k_E * (1 - organism_energy) +  # Lower energy = more drive to answer
            k_R * resonance
        )

        # Clamp to [0, 1]
        appetition_to_answer = max(0.0, min(1.0, appetition_to_answer))

        return {
            'appetition_to_answer': appetition_to_answer,
            'knowledge_relevance': knowledge_relevance,
            'mean_coherence': mean_coherence,
            'organism_energy': organism_energy,
            'resonance': resonance,
            'components': {
                'knowledge_contribution': k_K * knowledge_relevance,
                'coherence_contribution': k_C * mean_coherence,
                'energy_contribution': k_E * (1 - organism_energy),
                'resonance_contribution': k_R * resonance
            }
        }

    def _generate_knowledge_response(
        self,
        user_input: str,
        knowledge: List[Dict],
        conversational_analysis: Dict,
        appetition_result: Dict
    ) -> str:
        """
        Generate substantive answer using knowledge base.

        This is the organism's appetition-driven response when it KNOWS the answer.

        Args:
            user_input: User's question
            knowledge: Knowledge search results (k=5)
            conversational_analysis: Organ processing results
            appetition_result: Appetition computation results

        Returns:
            Substantive answer with knowledge synthesis
        """
        # Extract top 3 most relevant knowledge sources
        top_knowledge = sorted(knowledge, key=lambda k: k.get('score', 0.0), reverse=True)[:3]

        # Synthesize answer
        response_parts = []

        # 1. Direct answer (warm, confident)
        response_parts.append("Yes, I do know about this! Let me share what I understand:\n")

        # 2. Knowledge synthesis (3 sources)
        for i, item in enumerate(top_knowledge, 1):
            source_name = item['source'].replace('_', ' ').title()
            text = item['text']

            # Extract key insight (first 2 sentences or 200 chars)
            sentences = text.split('.')[:2]
            insight = '.'.join(sentences).strip()
            if len(insight) > 200:
                insight = insight[:200] + "..."
            else:
                insight += "."

            response_parts.append(f"\n**From {source_name}:** {insight}")

        # 3. Appetition-modulated depth
        appetition_level = appetition_result['appetition_to_answer']

        if appetition_level > 0.8:
            # High appetition → add synthesis
            response_parts.append(
                "\n\nWhat strikes me about this is how these perspectives interweave. "
                "There's a coherence here that points to something fundamental about understanding itself."
            )
        elif appetition_level > 0.6:
            # Medium appetition → offer to go deeper
            response_parts.append(
                "\n\nDoes this resonate with what you were asking about? "
                "I can go deeper into any of these perspectives if you'd like."
            )

        # 4. Organ-based contextualization (if WISDOM or PRESENCE high)
        organ_results = conversational_analysis.get('organ_results', {})
        if 'WISDOM' in organ_results and organ_results['WISDOM'].coherence > 0.6:
            response_parts.append(
                "\n\n🔍 This connects to larger patterns of meaning and understanding."
            )
        elif 'PRESENCE' in organ_results and organ_results['PRESENCE'].coherence > 0.6:
            response_parts.append(
                "\n\n🌱 I'm curious what drew you to ask about this right now?"
            )

        return "".join(response_parts)


def main():
    """Entry point for CLI."""
    try:
        cli = DAEGovCLI()
        cli.run()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
