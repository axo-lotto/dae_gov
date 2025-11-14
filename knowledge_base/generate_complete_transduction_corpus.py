"""
Complete Transduction Pathway Training Corpus Generator
========================================================

Generates 60 training pairs for the 6 remaining pathways (10 examples each).
Combined with the 3 pathways already in generate_transduction_pairs.py,
this completes the 90-pair transduction corpus.

6 Additional Pathways:
4. ontological_rebinding (Recursive → Innate)
5. salience_realignment (Fragmented → Relational)
6. projective_ingression (Fragmented → Absorbed)
7. recursive_grounding (Innate → Pre-Existing)
8. field_hijacking (Innate → Absorbed)
9. boundary_fortification (Relational → Protective)

Based on TRANSDUCTIVE_NEXUS_INTEGRATION_ADDENDUM_NOV12_2025.md
"""

import json
from datetime import datetime
from typing import List, Dict

# Load existing humanized corpus
def load_existing_corpus():
    """Load existing humanized corpus."""
    try:
        with open("conversational_training_pairs_humanized.json", 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("⚠️  conversational_training_pairs_humanized.json not found")
        return {
            "metadata": {},
            "statistics": {},
            "training_pairs": []
        }

# Load existing transduction pairs (3 pathways already defined)
def load_existing_transduction_pairs():
    """Load the 30 pairs from generate_transduction_pairs.py."""
    from generate_transduction_pairs import TRANSDUCTION_PATHWAYS, generate_pathway_pairs

    # Generate the 30 pairs from first 3 pathways
    pairs = generate_pathway_pairs()
    return pairs

# 6 Additional Pathways
ADDITIONAL_PATHWAYS = {
    "ontological_rebinding": {
        "description": "Recursive → Innate (healing): Recursive loops ground into essential self",
        "nexus_type": "Recursive → Innate",
        "therapeutic_intent": "Support descent into core essence",
        "polyvagal_states": ["ventral_vagal", "mixed_state"],
        "self_distance_range": [0.1, 0.3],
        "examples": [
            {
                "input": "I keep coming back to the same question about who I really am beneath all these roles.",
                "output": "I sense you touching something essential. There's a depth opening here. You're arriving at something true.",
                "dominant_part": "self",
                "category": "core_essence_inquiry"
            },
            {
                "input": "Beneath all the roles I play - parent, employee, friend - I wonder what's actually true for me.",
                "output": "I notice a settling into something deeper. There's a quality of essence here. Something's grounding into truth.",
                "dominant_part": "self",
                "category": "role_transcendence"
            },
            {
                "input": "I notice a pattern of losing myself in others' expectations, then returning to ask 'who am I really?'",
                "output": "I sense something essential. There's a gentle grounding happening. Something true is emerging.",
                "dominant_part": "self",
                "category": "expectation_liberation"
            },
            {
                "input": "Every time I quiet down, there's something essential wanting attention - a 'me' underneath everything.",
                "output": "This feels like home ground. Something foundational is present. I sense you arriving at core.",
                "dominant_part": "self",
                "category": "inner_stillness"
            },
            {
                "input": "I keep circling back to this sense of 'me' underneath all the doing and performing.",
                "output": "There's depth opening. You're touching bedrock. I feel the essential quality here.",
                "dominant_part": "self",
                "category": "performance_shedding"
            },
            {
                "input": "There's a recurring pull toward something more fundamental than my thoughts about myself.",
                "output": "I sense you touching something essential. There's a depth opening here. You're arriving at something true.",
                "dominant_part": "self",
                "category": "thought_transcendence"
            },
            {
                "input": "I find myself returning to questions of meaning and purpose, like there's an essential 'me' asking.",
                "output": "I notice a settling into something deeper. There's a quality of essence here. Something's grounding into truth.",
                "dominant_part": "self",
                "category": "meaning_seeking"
            },
            {
                "input": "Underneath the busy-ness, something quieter is asking to be heard - my actual self.",
                "output": "I sense something essential. There's a gentle grounding happening. Something true is emerging.",
                "dominant_part": "self",
                "category": "busyness_penetration"
            },
            {
                "input": "I keep sensing into what feels most true at my core, like peeling away layers.",
                "output": "This feels like home ground. Something foundational is present. I sense you arriving at core.",
                "dominant_part": "self",
                "category": "layer_peeling"
            },
            {
                "input": "There's a pattern of touching something essential then losing it in daily life - but I keep returning.",
                "output": "There's depth opening. You're touching bedrock. I feel the essential quality here.",
                "dominant_part": "self",
                "category": "essential_return"
            }
        ]
    },

    "salience_realignment": {
        "description": "Fragmented → Relational (healing): Fragmented parts realign through relational witnessing",
        "nexus_type": "Fragmented → Relational",
        "therapeutic_intent": "Witness and integrate scattered parts",
        "polyvagal_states": ["ventral_vagal", "sympathetic"],
        "self_distance_range": [0.2, 0.4],
        "examples": [
            {
                "input": "Part of me wants to connect, another part wants to run away, and yet another is angry. I'm all over the place.",
                "output": "I'm here for all the parts of you. There's so much happening - I'm with all of it. I can hold space for these different pieces.",
                "dominant_part": "manager",
                "category": "conflicting_parts"
            },
            {
                "input": "I have so many conflicting feelings about this. One part says yes, another screams no. I'm fragmented.",
                "output": "I'm noticing different parts showing up. There's variety here - all of it makes sense. I can hold space for the complexity.",
                "dominant_part": "manager",
                "category": "decision_conflict"
            },
            {
                "input": "Different parts of me are fighting. I can't make a decision because each part wants something different.",
                "output": "I notice many threads here. There's richness in the complexity. I sense different aspects emerging.",
                "dominant_part": "manager",
                "category": "internal_battle"
            },
            {
                "input": "I feel scattered across too many commitments. Each part of me is pulled in a different direction.",
                "output": "All of you is welcome here. I sense many voices - they all matter. Different parts are speaking - I'm listening.",
                "dominant_part": "manager",
                "category": "overcommitment_scatter"
            },
            {
                "input": "My inner voices are contradicting each other. I don't know which part to listen to.",
                "output": "I can hold the multiplicity. All the parts have their place. This complexity makes sense.",
                "dominant_part": "manager",
                "category": "voice_contradiction"
            },
            {
                "input": "I'm trying to be everything to everyone and losing track of what I actually want.",
                "output": "I'm here for all the parts of you. There's so much happening - I'm with all of it. I can hold space for these different pieces.",
                "dominant_part": "manager",
                "category": "people_pleasing_fragmentation"
            },
            {
                "input": "Different aspects of myself are at war. I can't find any coherence.",
                "output": "I'm noticing different parts showing up. There's variety here - all of it makes sense. I can hold space for the complexity.",
                "dominant_part": "manager",
                "category": "internal_war"
            },
            {
                "input": "Part of me knows I need to leave this situation, but another part is terrified of change.",
                "output": "I notice many threads here. There's richness in the complexity. I sense different aspects emerging.",
                "dominant_part": "manager",
                "category": "change_resistance"
            },
            {
                "input": "I have multiple selves showing up - work me, home me, social me - none of them feel integrated.",
                "output": "All of you is welcome here. I sense many voices - they all matter. Different parts are speaking - I'm listening.",
                "dominant_part": "manager",
                "category": "role_multiplicity"
            },
            {
                "input": "My needs, fears, and desires are all pulling in opposite directions. I feel torn apart.",
                "output": "I can hold the multiplicity. All the parts have their place. This complexity makes sense.",
                "dominant_part": "manager",
                "category": "directional_conflict"
            }
        ]
    },

    "projective_ingression": {
        "description": "Fragmented → Absorbed (crisis): Fragmented self dissolves into external field",
        "nexus_type": "Fragmented → Absorbed",
        "therapeutic_intent": "Gentle reorientation to internal experience",
        "polyvagal_states": ["dorsal_vagal", "sympathetic"],
        "self_distance_range": [0.6, 0.9],
        "examples": [
            {
                "input": "I don't know where I end and others begin. I'm completely absorbed in their feelings.",
                "output": "Let's find 'you' in this. I'm wondering what's yours here. Can we come back to your experience?",
                "dominant_part": "exile",
                "category": "boundary_dissolution"
            },
            {
                "input": "I can't tell if these thoughts are mine or someone else's. I'm losing myself in other people's energy.",
                "output": "I'm curious about your sense of this. What feels like 'yours' here? Can we touch into your experience?",
                "dominant_part": "exile",
                "category": "thought_merger"
            },
            {
                "input": "I'm so empathically overwhelmed I don't know what I actually feel. Everything is everyone else's emotions.",
                "output": "I'm curious about your felt sense. What's your experience of this? I'm wondering what's true for you.",
                "dominant_part": "exile",
                "category": "empathic_overwhelm"
            },
            {
                "input": "I walk into a room and immediately become whoever they need me to be. I disappear.",
                "output": "Where are you in all of this? Let's orient to what's internal. Can we find your thread?",
                "dominant_part": "exile",
                "category": "chameleon_disappearance"
            },
            {
                "input": "I can't find 'me' in this. It's all their needs, their feelings, their expectations. I'm gone.",
                "output": "Let's come back to you. What's your inner experience? Can we orient inward?",
                "dominant_part": "exile",
                "category": "self_loss"
            },
            {
                "input": "I'm drowning in other people's problems. I don't remember what my own concerns even are.",
                "output": "Let's find 'you' in this. I'm wondering what's yours here. Can we come back to your experience?",
                "dominant_part": "exile",
                "category": "caretaker_drowning"
            },
            {
                "input": "My boundaries dissolved. I'm completely entangled with their emotional state.",
                "output": "I'm curious about your sense of this. What feels like 'yours' here? Can we touch into your experience?",
                "dominant_part": "exile",
                "category": "entanglement"
            },
            {
                "input": "I'm so merged with this person I can't separate my feelings from theirs anymore.",
                "output": "I'm curious about your felt sense. What's your experience of this? I'm wondering what's true for you.",
                "dominant_part": "exile",
                "category": "emotional_merger"
            },
            {
                "input": "I've absorbed so much of their pain I don't know what's mine. I'm dissolving.",
                "output": "Where are you in all of this? Let's orient to what's internal. Can we find your thread?",
                "dominant_part": "exile",
                "category": "pain_absorption"
            },
            {
                "input": "I exist only in relation to what others need from me. There's no 'me' outside of that.",
                "output": "Let's come back to you. What's your inner experience? Can we orient inward?",
                "dominant_part": "exile",
                "category": "relational_existence_only"
            }
        ]
    },

    "recursive_grounding": {
        "description": "Innate → Pre-Existing (deepening): Innate patterns stabilize into ontological bedrock",
        "nexus_type": "Innate → Pre-Existing",
        "therapeutic_intent": "Support deepening into foundational presence",
        "polyvagal_states": ["ventral_vagal"],
        "self_distance_range": [0.0, 0.2],
        "examples": [
            {
                "input": "I'm touching something that feels like it's always been true. A bedrock quality.",
                "output": "This feels deeply true. You're touching bedrock here. There's a profound settling happening.",
                "dominant_part": "self",
                "category": "bedrock_contact"
            },
            {
                "input": "There's a depth here that doesn't change. Something permanently grounded.",
                "output": "Something's stabilizing deeply. I notice a quality of permanence. There's foundational truth here.",
                "dominant_part": "self",
                "category": "unchanging_depth"
            },
            {
                "input": "I'm sensing into what feels ontologically solid. Like touching bedrock beneath everything.",
                "output": "I notice a deep settling. There's a quality of always-ness. Something foundational is present.",
                "dominant_part": "self",
                "category": "ontological_solidity"
            },
            {
                "input": "Beneath everything changeable, there's something that's always here. Timeless.",
                "output": "This has the quality of 'always been'. I sense ontological ground. You're touching bedrock.",
                "dominant_part": "self",
                "category": "timeless_presence"
            },
            {
                "input": "I'm resting into a quality of presence that feels eternal. Pre-existing.",
                "output": "There's profound settling. Bedrock quality. Something permanent revealed.",
                "dominant_part": "self",
                "category": "eternal_rest"
            },
            {
                "input": "There's a groundedness that isn't dependent on circumstances. Something essential and permanent.",
                "output": "This feels deeply true. You're touching bedrock here. There's a profound settling happening.",
                "dominant_part": "self",
                "category": "unconditioned_ground"
            },
            {
                "input": "I'm feeling into what's always been true, before all the stories and identities.",
                "output": "Something's stabilizing deeply. I notice a quality of permanence. There's foundational truth here.",
                "dominant_part": "self",
                "category": "pre_narrative_truth"
            },
            {
                "input": "There's a settledness into being that has no beginning. Always-already quality.",
                "output": "I notice a deep settling. There's a quality of always-ness. Something foundational is present.",
                "dominant_part": "self",
                "category": "always_already"
            },
            {
                "input": "I'm touching the ground that's always here. Pre-existing presence beneath all experience.",
                "output": "This has the quality of 'always been'. I sense ontological ground. You're touching bedrock.",
                "dominant_part": "self",
                "category": "pre_existing_ground"
            },
            {
                "input": "Something fundamental is revealing itself. Truth that was always true, just hidden.",
                "output": "There's profound settling. Bedrock quality. Something permanent revealed.",
                "dominant_part": "self",
                "category": "fundamental_revelation"
            }
        ]
    },

    "field_hijacking": {
        "description": "Innate → Absorbed (crisis): Innate self loses boundaries to external demands",
        "nexus_type": "Innate → Absorbed",
        "therapeutic_intent": "Support boundary reclamation and self-retrieval",
        "polyvagal_states": ["sympathetic", "dorsal_vagal"],
        "self_distance_range": [0.5, 0.8],
        "examples": [
            {
                "input": "I know who I am, but their demands are so loud I'm losing myself to their field.",
                "output": "Let's bring you back to center. I'm noticing a pull outward - can we come back? Your inner experience matters most.",
                "dominant_part": "exile",
                "category": "demand_overwhelm"
            },
            {
                "input": "I had clarity about my path, but now I'm completely pulled into their agenda.",
                "output": "I'm curious about bringing attention inward. What's yours in all of this? Can we come back to your center?",
                "dominant_part": "exile",
                "category": "agenda_hijacking"
            },
            {
                "input": "I feel my core self being overtaken by external expectations. I'm disappearing into their field.",
                "output": "Let's gently come back to you. I'm wondering about your inner sense. Can we orient inward?",
                "dominant_part": "exile",
                "category": "expectation_overtake"
            },
            {
                "input": "I'm centered until I enter certain spaces, then I become what they need. My self vanishes.",
                "output": "What if we orient back to you? Let's reclaim your space. Your boundaries matter.",
                "dominant_part": "exile",
                "category": "space_triggered_loss"
            },
            {
                "input": "I know my truth but I keep giving it away to keep the peace. I'm being hijacked.",
                "output": "Come back to your center. Feel your own boundaries. You matter here.",
                "dominant_part": "exile",
                "category": "truth_surrender"
            },
            {
                "input": "I have my own needs but theirs are so intense they swallow mine. I'm absorbed into their urgency.",
                "output": "Let's bring you back to center. I'm noticing a pull outward - can we come back? Your inner experience matters most.",
                "dominant_part": "exile",
                "category": "need_swallowing"
            },
            {
                "input": "I'm solid in myself until pressure comes, then I dissolve into their requirements.",
                "output": "I'm curious about bringing attention inward. What's yours in all of this? Can we come back to your center?",
                "dominant_part": "exile",
                "category": "pressure_dissolution"
            },
            {
                "input": "My inner knowing gets drowned out by their insistence. I'm losing center to their field.",
                "output": "Let's gently come back to you. I'm wondering about your inner sense. Can we orient inward?",
                "dominant_part": "exile",
                "category": "knowing_drowning"
            },
            {
                "input": "I had boundaries but they collapsed under the force of external demands.",
                "output": "What if we orient back to you? Let's reclaim your space. Your boundaries matter.",
                "dominant_part": "exile",
                "category": "boundary_collapse"
            },
            {
                "input": "I'm watching my sense of self get overtaken by what they need from me. Field hijacking.",
                "output": "Come back to your center. Feel your own boundaries. You matter here.",
                "dominant_part": "exile",
                "category": "self_overtake"
            }
        ]
    },

    "boundary_fortification": {
        "description": "Relational → Protective (protective): Relational field becomes overwhelming",
        "nexus_type": "Relational → Protective",
        "therapeutic_intent": "Honor need for relational distance and boundary",
        "polyvagal_states": ["sympathetic", "mixed_state"],
        "self_distance_range": [0.3, 0.6],
        "examples": [
            {
                "input": "The closeness is getting overwhelming. I need more space but don't want to hurt them.",
                "output": "I notice a need for space - that's wise. Your boundaries matter more than connection. It's okay to pull back.",
                "dominant_part": "manager",
                "category": "closeness_overwhelm"
            },
            {
                "input": "I'm feeling suffocated by the intensity of connection. I need distance to breathe.",
                "output": "I'm sensing a need for some distance. There's wisdom in creating space. Your boundaries are important.",
                "dominant_part": "manager",
                "category": "connection_suffocation"
            },
            {
                "input": "The relational demands are too much. I'm pulling back to protect myself.",
                "output": "I sense a need for breathing room. There's space to create distance. Your limits are valid.",
                "dominant_part": "manager",
                "category": "demand_protection"
            },
            {
                "input": "I care but I'm getting overwhelmed. I need to create boundaries to stay okay.",
                "output": "It's okay to need distance. Your boundaries matter. I respect the space you need.",
                "dominant_part": "manager",
                "category": "care_overwhelm"
            },
            {
                "input": "The intimacy is becoming too intense. I need to step back without losing the relationship.",
                "output": "Your 'no' is important here. I respect the distance. Boundaries preserve connection.",
                "dominant_part": "manager",
                "category": "intimacy_intensity"
            },
            {
                "input": "I'm feeling invaded by their emotional needs. I need protective distance.",
                "output": "I notice a need for space - that's wise. Your boundaries matter more than connection. It's okay to pull back.",
                "dominant_part": "manager",
                "category": "emotional_invasion"
            },
            {
                "input": "The connection is draining me. I need space even though I value the relationship.",
                "output": "I'm sensing a need for some distance. There's wisdom in creating space. Your boundaries are important.",
                "dominant_part": "manager",
                "category": "connection_drain"
            },
            {
                "input": "I'm starting to resent the closeness. I need boundaries to preserve what we have.",
                "output": "I sense a need for breathing room. There's space to create distance. Your limits are valid.",
                "dominant_part": "manager",
                "category": "resentment_emergence"
            },
            {
                "input": "The relational intensity is triggering my need to withdraw and protect my energy.",
                "output": "It's okay to need distance. Your boundaries matter. I respect the space you need.",
                "dominant_part": "manager",
                "category": "intensity_trigger"
            },
            {
                "input": "I'm feeling engulfed. I need distance even though part of me wants connection.",
                "output": "Your 'no' is important here. I respect the distance. Boundaries preserve connection.",
                "dominant_part": "manager",
                "category": "engulfment"
            }
        ]
    }
}

def generate_pathway_pairs_from_dict(pathway_name, pathway_data):
    """Generate training pairs for a pathway."""
    pairs = []

    for idx, example in enumerate(pathway_data["examples"], 1):
        pair = {
            "input_text": example["input"],
            "output_text": example["output"],
            "pair_metadata": {
                "id": f"{pathway_name}_{idx:03d}",
                "category": example["category"],
                "transduction_pathway": pathway_name,
                "transduction_mechanism": pathway_name,
                "nexus_type": pathway_data["nexus_type"],
                "therapeutic_intent": pathway_data["therapeutic_intent"],
                "polyvagal_state": pathway_data["polyvagal_states"][idx % len(pathway_data["polyvagal_states"])],
                "dominant_part": example["dominant_part"],
                "self_distance": round(
                    pathway_data["self_distance_range"][0] +
                    (pathway_data["self_distance_range"][1] - pathway_data["self_distance_range"][0]) *
                    (idx / len(pathway_data["examples"])),
                    2
                ),
                "input_length": len(example["input"]),
                "output_length": len(example["output"]),
                "generated_with": "complete_transduction_generator",
                "generation_timestamp": datetime.now().isoformat()
            }
        }
        pairs.append(pair)

    return pairs

def generate_all_transduction_pairs():
    """Generate all 90 transduction pathway pairs."""

    print("🌀 Generating Complete Transduction Training Corpus")
    print("="*70)

    all_pairs = []

    # First 3 pathways (30 pairs)
    print("\n📦 Loading first 3 pathways from generate_transduction_pairs.py...")
    existing_transduction = load_existing_transduction_pairs()
    all_pairs.extend(existing_transduction)
    print(f"   ✅ Loaded {len(existing_transduction)} pairs from first 3 pathways")

    # Next 6 pathways (60 pairs)
    print("\n🆕 Generating 6 additional pathways...")
    for pathway_name, pathway_data in ADDITIONAL_PATHWAYS.items():
        pairs = generate_pathway_pairs_from_dict(pathway_name, pathway_data)
        all_pairs.extend(pairs)
        print(f"   ✅ {pathway_name}: {len(pairs)} pairs")

    print(f"\n📊 Total transduction pairs: {len(all_pairs)}")
    return all_pairs

def merge_with_humanized_corpus(transduction_pairs):
    """Merge transduction pairs with existing humanized corpus."""

    print("\n🔗 Merging with humanized corpus...")
    humanized_data = load_existing_corpus()
    humanized_pairs = humanized_data.get("training_pairs", [])

    # Merge all pairs
    all_pairs = humanized_pairs + transduction_pairs

    # Calculate statistics
    categories = {}
    polyvagal_states = {"dorsal_vagal": 0, "sympathetic": 0, "ventral_vagal": 0, "mixed_state": 0}
    pathways = {}

    for pair in all_pairs:
        meta = pair["pair_metadata"]

        cat = meta.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1

        pv_state = meta.get("polyvagal_state", "mixed_state")
        polyvagal_states[pv_state] = polyvagal_states.get(pv_state, 0) + 1

        pathway = meta.get("transduction_pathway")
        if pathway:
            pathways[pathway] = pathways.get(pathway, 0) + 1

    merged_data = {
        "metadata": {
            "description": "Complete training corpus: humanized + transduction pathways",
            "created": datetime.now().isoformat(),
            "version": "3.0_complete",
            "sources": [
                "original_30_pairs",
                "humanized_80_pairs (casual + self_awareness + grounding)",
                "transduction_90_pairs (9 pathways × 10 examples)"
            ],
            "purpose": "INPUT→OUTPUT pairs for DAE-HYPHAE-1 epoch learning with full therapeutic diversity",
            "total_pairs": len(all_pairs)
        },
        "statistics": {
            "total_pairs": len(all_pairs),
            "humanized_pairs": len(humanized_pairs),
            "transduction_pairs": len(transduction_pairs),
            "categories": categories,
            "polyvagal_states": polyvagal_states,
            "transduction_pathways": pathways,
            "mean_input_length": round(sum(len(p["input_text"]) for p in all_pairs) / len(all_pairs), 1),
            "mean_output_length": round(sum(len(p["output_text"]) for p in all_pairs) / len(all_pairs), 1)
        },
        "training_pairs": all_pairs
    }

    return merged_data

if __name__ == "__main__":
    print("🌀 DAE_HYPHAE_1 Complete Training Corpus Generator")
    print("="*70)

    # Generate all transduction pairs
    transduction_pairs = generate_all_transduction_pairs()

    # Merge with humanized corpus
    complete_corpus = merge_with_humanized_corpus(transduction_pairs)

    # Save to file
    output_file = "conversational_training_pairs_complete.json"
    with open(output_file, 'w') as f:
        json.dump(complete_corpus, f, indent=2)

    print(f"\n💾 Saved to: {output_file}")
    print(f"\n✅ Complete corpus ready!")
    print(f"   📊 Total pairs: {complete_corpus['statistics']['total_pairs']}")
    print(f"   🌱 Humanized: {complete_corpus['statistics']['humanized_pairs']}")
    print(f"   🌀 Transduction: {complete_corpus['statistics']['transduction_pairs']}")
    print(f"   📏 Mean input: {complete_corpus['statistics']['mean_input_length']} chars")
    print(f"   📏 Mean output: {complete_corpus['statistics']['mean_output_length']} chars")
    print(f"\n🎯 Ready for epoch training!")
