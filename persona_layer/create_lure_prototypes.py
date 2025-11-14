#!/usr/bin/env python3
"""
Create Lure Prototype Embeddings - Phase C3.1
==============================================

Generates semantic embeddings for 21 lure dimensions:
- EMPATHY: 7 emotional prototypes
- WISDOM: 7 cognitive/pattern prototypes
- AUTHENTICITY: 7 relational/vulnerability prototypes

Uses SANS organ's sentence transformer model for consistency.

Date: November 13, 2025
Phase: C3.1
"""

import sys
import json
import numpy as np
from pathlib import Path

sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.embedding_coordinator import EmbeddingCoordinator


# Define prototype texts for each lure dimension
LURE_PROTOTYPES = {
    "empathy_emotional": {
        "joy": [
            "I feel delighted and energized",
            "There's brightness and aliveness here",
            "Something joyful is emerging",
            "I sense celebration and vitality",
            "This feels uplifting and warm"
        ],
        "grief": [
            "I feel deep sadness and loss",
            "There's profound sorrow here",
            "Something precious is mourned",
            "I sense heaviness and longing",
            "This feels tender and aching"
        ],
        "fear": [
            "I feel anxious and uncertain",
            "There's danger and threat here",
            "Something scary is present",
            "I sense worry and apprehension",
            "This feels unsafe and alarming"
        ],
        "anger": [
            "I feel frustrated and protective",
            "There's injustice and boundary violation here",
            "Something is not okay",
            "I sense fierce energy and rage",
            "This feels wrong and activating"
        ],
        "compassion": [
            "I feel warmth toward suffering",
            "There's kindness and care here",
            "Something tender is held",
            "I sense empathy and understanding",
            "This feels gentle and accepting"
        ],
        "shame": [
            "I feel exposed and defective",
            "There's unworthiness and hiding here",
            "Something shameful is revealed",
            "I sense wrongness in myself",
            "This feels unbearable and small"
        ],
        "neutral": [
            "I notice what's present",
            "There's observation and awareness here",
            "Something is simply here",
            "I sense clarity and witness",
            "This feels balanced and observing"
        ]
    },

    "wisdom_pattern": {
        "systems": [
            "I see how parts interconnect",
            "There are patterns and relationships here",
            "Something systemic is visible",
            "I sense the whole system dynamics",
            "This reveals interconnection and complexity"
        ],
        "meta": [
            "I notice I'm noticing",
            "There's a stepping back to see the whole",
            "Something recursive is happening",
            "I sense awareness of awareness",
            "This feels like meta-perspective emerging"
        ],
        "temporal": [
            "I see patterns across time",
            "There's a rhythm and sequence here",
            "Something evolves and changes",
            "I sense timing and unfolding",
            "This reveals temporal dynamics"
        ],
        "paradox": [
            "I hold both and neither",
            "There's contradiction that makes sense",
            "Something contains opposites",
            "I sense both/and complexity",
            "This feels paradoxical and true"
        ],
        "embodied": [
            "I feel this in my body",
            "There's somatic knowing here",
            "Something is sensed physically",
            "I sense bodily wisdom",
            "This feels viscerally true"
        ],
        "relational": [
            "I see the between-ness",
            "There's connection and relating here",
            "Something emerges in relationship",
            "I sense the field between us",
            "This reveals relational dynamics"
        ],
        "integrative": [
            "I see how it all comes together",
            "There's synthesis and wholeness here",
            "Something coherent emerges",
            "I sense integration and unity",
            "This feels like pieces finding their place"
        ]
    },

    "authenticity_vulnerability": {
        "vulnerable": [
            "I feel exposed and open",
            "There's tender truth here",
            "Something undefended is shared",
            "I sense rawness and honesty",
            "This feels unguarded and real"
        ],
        "honest": [
            "I speak the truth",
            "There's clarity and directness here",
            "Something genuine is named",
            "I sense congruence and realness",
            "This feels truthful and aligned"
        ],
        "guarded": [
            "I protect what's tender",
            "There's careful holding here",
            "Something defended is present",
            "I sense protective distance",
            "This feels boundaried and cautious"
        ],
        "performative": [
            "I show what's expected",
            "There's presentation and facade here",
            "Something crafted is displayed",
            "I sense image management",
            "This feels strategic and polished"
        ],
        "emergent": [
            "I'm becoming something new",
            "There's unfolding and discovery here",
            "Something is being born",
            "I sense newness arriving",
            "This feels like emergence and growth"
        ],
        "receptive": [
            "I'm open to what comes",
            "There's willingness and allowing here",
            "Something is being received",
            "I sense openness and acceptance",
            "This feels welcoming and spacious"
        ],
        "boundaried": [
            "I know what's mine and not mine",
            "There's clear limits and edges here",
            "Something is differentiated",
            "I sense healthy boundaries",
            "This feels clear and contained"
        ]
    },

    "listening_inquiry": {
        "temporal_inquiry": [
            "What happened before this? When did it begin?",
            "How has this unfolded over time?",
            "What comes next in the sequence?",
            "I'm curious about the timeline here",
            "Tell me more about the when of this"
        ],
        "core_exploration": [
            "What's beneath the surface of this?",
            "What deeper layer wants attention?",
            "I sense something core is here",
            "What's at the heart of this?",
            "There's a deeper truth underneath"
        ],
        "witnessing_presence": [
            "I see you, I hear you completely",
            "You are witnessed in this moment",
            "I'm fully here with what you're sharing",
            "Your experience is received and held",
            "I'm present to all of this"
        ],
        "pattern_mapping": [
            "This connects to what you shared earlier",
            "I notice a pattern emerging here",
            "These pieces relate in this way",
            "There's a through-line I'm tracking",
            "I see how these fit together"
        ],
        "silence_holding": [
            "I'm comfortable in this silence with you",
            "There's spacious quiet here",
            "No need to fill the space",
            "Silence can speak volumes",
            "I'm listening to what's unspoken"
        ],
        "clarifying_inquiry": [
            "Help me understand this better",
            "Can you say more about that?",
            "What do you mean by that?",
            "I want to make sure I'm following",
            "Tell me more so I can understand"
        ],
        "tracking_continuity": [
            "You mentioned earlier that...",
            "Coming back to what you said before",
            "I'm tracking what you shared about...",
            "This relates to the thread we started",
            "I'm holding the continuity here"
        ]
    },

    "presence_embodiment": {
        "embodied_awareness": [
            "I feel this in my body right now",
            "There's sensation and aliveness here",
            "My body is sensing something",
            "I notice physical feelings arising",
            "This lives in somatic experience"
        ],
        "grounded_holding": [
            "I feel rooted and stable here",
            "There's solid ground beneath",
            "Anchored presence is available",
            "Grounded and centered in this",
            "Foundation is strong and steady"
        ],
        "spacious_allowing": [
            "There's room for all of this",
            "Nothing needs to be fixed or changed",
            "I can hold space for whatever arises",
            "Everything is welcome here",
            "Spacious acceptance is present"
        ],
        "attuned_resonance": [
            "I feel into your energetic state",
            "Matching the felt sense here",
            "Attuned to the subtle field",
            "I'm resonating with your energy",
            "Calibrated to your frequency"
        ],
        "somatic_noticing": [
            "I notice sensations in my chest",
            "There's tightness in my throat",
            "My body is giving me information",
            "Attending to physical signals",
            "Body-level awareness is active"
        ],
        "centered_stillness": [
            "I'm in the still point within",
            "Calm center amidst the movement",
            "Quiet inner stability is here",
            "Centered in the eye of the storm",
            "Still and present at the core"
        ],
        "integrated_wholeness": [
            "All parts of me are welcome",
            "Nothing needs to be excluded",
            "Integrated and whole in this moment",
            "Unity within multiplicity",
            "Complete and undivided presence"
        ]
    },

    "bond_parts": {
        "manager_control": [
            "We need to plan this carefully and stay organized",
            "Let's implement proper protocols to prevent issues",
            "I'm managing this situation by controlling outcomes",
            "Structure and order will keep us safe",
            "Planning ahead prevents problems later"
        ],
        "firefighter_numbing": [
            "I can't deal with this right now, need distraction",
            "Overwhelmed and needing to escape or numb out",
            "The pressure is unbearable, shut it down",
            "Crisis mode activated, react immediately",
            "Can't think, just need to make it stop"
        ],
        "exile_pain": [
            "I feel worthless and deeply flawed inside",
            "There's tender young pain that feels unbearable",
            "Shame and hurt from long ago surfaces",
            "I'm unlovable and will be abandoned",
            "This wound is so old and so tender"
        ],
        "self_energy": [
            "I'm curious and calm about what's emerging",
            "There's compassion and clarity present here",
            "I can be with all parts without judgment",
            "Confident and connected to inner wisdom",
            "Creative and courageous exploration happening"
        ],
        "protector_activation": [
            "Parts are working hard to keep me safe",
            "Protective strategies are engaged strongly",
            "Defenses are up and active right now",
            "Something is guarding against the pain",
            "Protection systems are fully online"
        ],
        "blending_identification": [
            "I am this anger, completely fused with it",
            "Lost in this part, can't see anything else",
            "Totally identified with this reaction",
            "No distance from this feeling at all",
            "This part has completely taken over"
        ],
        "unburdening_release": [
            "Old roles are falling away naturally",
            "Something is being released and healed",
            "Parts are letting go of burdens they carried",
            "Transformation is happening, lightness emerging",
            "The heavy weight is lifting, freedom coming"
        ]
    },

    "sans_coherence": {
        "semantic_drift": [
            "The meaning has shifted subtly from before",
            "Words no longer match the original intent",
            "Something has drifted away from coherence",
            "The sense has changed without me noticing",
            "Meaning is slipping and losing alignment"
        ],
        "contradiction_detected": [
            "These two things contradict each other",
            "Something doesn't add up logically here",
            "Inconsistency is present between statements",
            "These ideas cannot both be true together",
            "There's a logical conflict emerging"
        ],
        "alignment_strong": [
            "Everything coheres and fits together perfectly",
            "Strong consistency across all elements",
            "All parts align and reinforce each other",
            "Clear coherence throughout the system",
            "Everything makes sense and holds together"
        ],
        "repair_needed": [
            "Something needs reconnection and integration",
            "A gap needs bridging to restore coherence",
            "Repair work is called for here",
            "Disconnection needs healing attention",
            "Integration is required to restore flow"
        ],
        "fragmentation": [
            "Pieces are scattered with no connection",
            "Everything feels disconnected and separate",
            "No through-line or unity is visible",
            "Fragmented with no coherent whole",
            "Broken into isolated parts"
        ],
        "coherent_narrative": [
            "The story holds together from start to finish",
            "A clear through-line connects everything",
            "Narrative coherence is strong and clear",
            "Everything fits into a unified story",
            "The account is consistent and complete"
        ],
        "bridging_gaps": [
            "Connecting separated meanings together",
            "Finding links between disconnected parts",
            "Building bridges across the divide",
            "Creating connections where gaps existed",
            "Weaving together what was separate"
        ]
    },

    "ndam_urgency": {
        "crisis_imminent": [
            "Immediate danger present right now",
            "Crisis is happening in this very moment",
            "Urgent threat requiring instant response",
            "Right now urgency, cannot wait",
            "Emergency unfolding at this instant"
        ],
        "safety_concern": [
            "Worried about safety and potential harm",
            "Concern for wellbeing and security",
            "Something feels unsafe and risky",
            "Safety is uncertain and concerning",
            "Risk of harm is present here"
        ],
        "escalating_intensity": [
            "Things are building and getting worse",
            "Intensity is rising toward crisis",
            "Escalation is happening progressively",
            "Moving toward a breaking point",
            "Situation is intensifying dangerously"
        ],
        "stability_present": [
            "Grounded and not in crisis right now",
            "Safety is present, no immediate threat",
            "Stable and secure in this moment",
            "Everything is okay and manageable",
            "No urgency, things are safe enough"
        ],
        "harm_risk": [
            "Risk of self-harm is present",
            "Danger of hurting self or others",
            "Harmful actions are possible",
            "Risk of injury or damage exists",
            "Potential for harm is real here"
        ],
        "deescalating": [
            "Coming down from high activation",
            "Intensity is decreasing and settling",
            "Finding ground after escalation",
            "Crisis is passing and calming",
            "Returning to baseline and safety"
        ],
        "resource_assessment": [
            "What support is available right now?",
            "Who can help in this situation?",
            "Assessing resources and options",
            "What tools or help do I have?",
            "Evaluating available support systems"
        ]
    },

    "rnx_temporal": {
        "chronic_pattern": [
            "This has been happening for a very long time",
            "Longstanding pattern repeating over years",
            "Chronic issue that persists endlessly",
            "This is a very old, established pattern",
            "Been dealing with this for ages now"
        ],
        "acute_event": [
            "This just happened very recently",
            "New development that just occurred",
            "Acute situation that arose suddenly",
            "Something that just started happening",
            "Recent and new event unfolding"
        ],
        "cyclical_rhythm": [
            "This comes and goes in cycles",
            "Repeating rhythm that returns regularly",
            "Cyclical pattern with ups and downs",
            "This happens periodically in waves",
            "Rhythmic cycle that keeps returning"
        ],
        "developmental_phase": [
            "This is a transition and growth point",
            "Developmental stage of transformation",
            "Growing edge and evolutionary moment",
            "Phase of development and maturation",
            "Transitional period of becoming"
        ],
        "stuck_repetition": [
            "Same thing over and over with no change",
            "Stuck in repetitive loop going nowhere",
            "No movement, just endless repetition",
            "Groundhog day feeling, nothing shifts",
            "Trapped in pattern with no evolution"
        ],
        "momentum_building": [
            "Change is happening, things are shifting",
            "Momentum is building toward transformation",
            "Movement is occurring progressively",
            "Things are evolving and developing",
            "Forward motion is gaining strength"
        ],
        "temporal_coherence": [
            "Past, present, and future all connect",
            "Coherent thread through time is visible",
            "Timeline makes sense as unified whole",
            "Temporal integration across all time",
            "History and future link meaningfully"
        ]
    },

    "eo_polyvagal": {
        "ventral_vagal_safe": [
            "I feel safe and socially connected",
            "Engaged and comfortable with others",
            "Relaxed openness and social ease",
            "Safe connection and warm presence",
            "Calm, social, and feeling secure"
        ],
        "sympathetic_fight": [
            "Activated with fighting energy and anger",
            "Aggressive and ready for confrontation",
            "Fight response is fully engaged",
            "Mobilized to push back and defend",
            "Fierce activation and combative energy"
        ],
        "sympathetic_flight": [
            "Anxious and needing to escape quickly",
            "Flight response activated strongly",
            "Panic and need to get away now",
            "Running energy, can't stay here",
            "Fleeing from threat and danger"
        ],
        "dorsal_freeze": [
            "Shut down and frozen in place",
            "Immobilized and unable to move",
            "Collapsed into freeze response",
            "Stuck and numb, can't respond",
            "Complete shutdown and paralysis"
        ],
        "dorsal_dissociation": [
            "Disconnected and floating away",
            "Not here, spaced out completely",
            "Dissociated from body and present",
            "Unreal feeling, watching from outside",
            "Gone away, not in my body anymore"
        ],
        "mixed_state": [
            "Multiple nervous system states active together",
            "Both fight and freeze happening at once",
            "Mixed activation with conflicting signals",
            "Stuck between states, can't settle",
            "Simultaneous opposing responses present"
        ],
        "state_transition": [
            "Moving between nervous system states",
            "Shifting from one state to another",
            "Transition happening in activation",
            "State is changing and reorganizing",
            "Moving through polyvagal hierarchy"
        ]
    },

    "card_scale": {
        "minimal_holding": [
            "Just a brief word is enough",
            "Simple and short response needed",
            "Minimal presence, nothing elaborate",
            "Just enough, no more required",
            "Brief holding is sufficient here"
        ],
        "moderate_presence": [
            "Balanced response with medium depth",
            "Moderate engagement and exploration",
            "Neither too brief nor too extensive",
            "Middle level of presence and depth",
            "Proportional moderate response"
        ],
        "comprehensive_depth": [
            "Full exploration and deep engagement",
            "Comprehensive presence with full depth",
            "Extensive holding and thorough response",
            "Deep dive into all dimensions",
            "Complete and expansive presence"
        ],
        "silence_appropriate": [
            "No words needed, just presence",
            "Silence speaks more than words",
            "Quiet holding is what's called for",
            "Words would diminish this moment",
            "Presence without language is right"
        ],
        "crisis_brevity": [
            "Brief and grounding for overwhelm",
            "Short to prevent overload in crisis",
            "Minimal words when capacity is low",
            "Condensed for high activation state",
            "Grounding brevity for overwhelm"
        ],
        "developmental_expansive": [
            "Room for growth and exploration",
            "Expansive space for development",
            "Generous holding for emergence",
            "Developmental openness and room",
            "Growth-supporting spaciousness"
        ],
        "tracking_proportional": [
            "Response matches the need exactly",
            "Right-sized to the situation",
            "Proportional to what's present",
            "Calibrated matching of scale",
            "Neither too much nor too little"
        ]
    }
}


def create_lure_prototypes(output_path: str = "persona_layer/lure_prototypes.json"):
    """
    Create lure prototype embeddings using SANS organ.

    For each lure dimension, we:
    1. Take 5 prototype sentences
    2. Generate embeddings using SANS sentence transformer
    3. Average embeddings to create prototype vector
    4. Store in JSON for later use
    """
    print("="*80)
    print("🌀 CREATING LURE PROTOTYPE EMBEDDINGS (Phase C3.1)")
    print("="*80)

    # Initialize embedding coordinator (singleton, centralized)
    print("\n📦 Initializing embedding coordinator...")
    coordinator = EmbeddingCoordinator()
    print("✅ Coordinator ready (will lazy-load model on first embed)")

    # Storage for all prototypes
    prototypes_data = {
        "description": "Lure prototype embeddings for embedding-based lure computation",
        "version": "1.0.0",
        "date_created": "2025-11-13",
        "embedding_model": "all-MiniLM-L6-v2",
        "embedding_dim": 384,
        "prototypes": {}
    }

    # Generate embeddings for each category
    for category, dimensions in LURE_PROTOTYPES.items():
        print(f"\n📊 Processing {category}...")
        prototypes_data["prototypes"][category] = {}

        for dimension, texts in dimensions.items():
            print(f"   Generating prototype for '{dimension}'...")

            # Get embeddings for all prototype texts using coordinator
            embeddings = coordinator.embed_batch(texts, use_cache=False)

            if embeddings is not None and len(embeddings) > 0:
                # Average embeddings to create prototype
                prototype_embedding = np.mean(embeddings, axis=0)

                # Normalize
                norm = np.linalg.norm(prototype_embedding)
                if norm > 0:
                    prototype_embedding = prototype_embedding / norm

                # Store as list (JSON serializable)
                prototypes_data["prototypes"][category][dimension] = {
                    "embedding": prototype_embedding.tolist(),
                    "prototype_texts": texts
                }

                print(f"      ✅ {dimension}: {len(embeddings)} texts → 384D embedding")
            else:
                print(f"      ❌ {dimension}: Failed to generate embeddings")

    # Save to JSON
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(prototypes_data, f, indent=2)

    print(f"\n✅ Lure prototypes saved to: {output_path}")

    # Summary
    total_prototypes = sum(
        len(dims) for dims in prototypes_data["prototypes"].values()
    )
    print(f"\n📊 SUMMARY:")
    print(f"   Total prototypes: {total_prototypes}")
    print(f"   EMPATHY emotional: {len(prototypes_data['prototypes']['empathy_emotional'])}")
    print(f"   WISDOM pattern: {len(prototypes_data['prototypes']['wisdom_pattern'])}")
    print(f"   AUTHENTICITY vulnerability: {len(prototypes_data['prototypes']['authenticity_vulnerability'])}")
    if 'listening_inquiry' in prototypes_data['prototypes']:
        print(f"   LISTENING inquiry: {len(prototypes_data['prototypes']['listening_inquiry'])}")
    if 'presence_embodiment' in prototypes_data['prototypes']:
        print(f"   PRESENCE embodiment: {len(prototypes_data['prototypes']['presence_embodiment'])}")
    if 'bond_parts' in prototypes_data['prototypes']:
        print(f"   BOND parts: {len(prototypes_data['prototypes']['bond_parts'])}")
    if 'sans_coherence' in prototypes_data['prototypes']:
        print(f"   SANS coherence: {len(prototypes_data['prototypes']['sans_coherence'])}")
    if 'ndam_urgency' in prototypes_data['prototypes']:
        print(f"   NDAM urgency: {len(prototypes_data['prototypes']['ndam_urgency'])}")
    if 'rnx_temporal' in prototypes_data['prototypes']:
        print(f"   RNX temporal: {len(prototypes_data['prototypes']['rnx_temporal'])}")
    if 'eo_polyvagal' in prototypes_data['prototypes']:
        print(f"   EO polyvagal: {len(prototypes_data['prototypes']['eo_polyvagal'])}")
    if 'card_scale' in prototypes_data['prototypes']:
        print(f"   CARD scale: {len(prototypes_data['prototypes']['card_scale'])}")
    print(f"   Embedding dimension: 384D")

    print("\n" + "="*80)
    print("✅ Phase C3 COMPLETE: ALL 11 ORGANS Lure Prototypes Created (77 total)")
    print("="*80 + "\n")

    return prototypes_data


if __name__ == '__main__':
    create_lure_prototypes()
