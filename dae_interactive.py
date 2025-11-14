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

        # Step 1: Process through organism (11 organs)
        result = self.organism.process_text(
            user_input,
            context=context,
            enable_tsk_recording=self.enable_tsk_recording,
            enable_phase2=self.enable_phase2,
            user_id=self.user['user_id'],  # 🌀 Phase 1.6: User identity (Nov 14, 2025)
            username=self.user['username']  # 🌀 Phase 1.6: Username for personalization (Nov 14, 2025)
        )

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

    def _extract_organ_signature(self, organ_results: dict) -> dict:
        """Extract 57D organ signature from organ results."""
        signature = {}
        for organ_name, organ_result in organ_results.items():
            if hasattr(organ_result, 'atom_activations'):
                signature[organ_name] = organ_result.atom_activations
            elif isinstance(organ_result, dict) and 'atom_activations' in organ_result:
                signature[organ_name] = organ_result['atom_activations']
        return signature

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

                # Handle empty input
                if not user_input:
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
                    else:
                        print(f"❌ Unknown command: {user_input}")
                        print("   Type /help for available commands")
                        continue

                # Process through organism
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
