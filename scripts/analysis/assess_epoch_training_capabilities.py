"""
Assess Current Epoch Training Capabilities
===========================================

Analyzes the hybrid organism's learning architecture to understand:
1. What the R-matrix learns (organ couplings)
2. What families learn (conversation patterns)
3. How training pairs are processed
4. Where emoji/glyph patterns can be integrated

Date: November 13, 2025
"""

import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

import json
from pathlib import Path

print("=" * 80)
print("EPOCH TRAINING CAPABILITIES ASSESSMENT")
print("=" * 80)

# ==============================================================================
# 1. R-MATRIX LEARNING (Organ Couplings)
# ==============================================================================
print("\n" + "=" * 80)
print("1. R-MATRIX LEARNING (Conversational Hebbian Memory)")
print("=" * 80)

hebbian_path = Path("persona_layer/conversational_hebbian_memory.json")
if hebbian_path.exists():
    with open(hebbian_path) as f:
        hebbian_memory = json.load(f)

    print(f"\n📊 R-Matrix Structure:")
    r_matrix = hebbian_memory.get('R_matrix', {})
    print(f"   Organs tracked: {len(r_matrix)}")

    # Sample coupling
    if r_matrix:
        first_organ = list(r_matrix.keys())[0]
        couplings = r_matrix[first_organ]
        print(f"\n   Example: {first_organ} couplings:")
        for organ, strength in list(couplings.items())[:5]:
            print(f"      {organ}: {strength:.3f}")

    # Metadata
    metadata = hebbian_memory.get('metadata', {})
    print(f"\n📈 Learning Stats:")
    print(f"   Total updates: {metadata.get('total_updates', 0)}")
    print(f"   Last updated: {metadata.get('last_updated', 'unknown')}")

    print(f"\n💡 What R-matrix learns:")
    print(f"   - Which organs co-activate in conversations")
    print(f"   - Coupling strengths between all 11 organs")
    print(f"   - Pattern: When EMPATHY fires, does BOND also fire?")

    print(f"\n🔗 Emoji/Glyph Integration Point:")
    print(f"   → Could learn: Which organs → which emoji families")
    print(f"   → Example: EMPATHY high + BOND high → 🫂 emoji preference")
    print(f"   → Example: PRESENCE high + WISDOM high → 🧘 🦉 pattern")

else:
    print("   ⚠️  R-matrix file not found")

# ==============================================================================
# 2. FAMILY LEARNING (Conversation Patterns)
# ==============================================================================
print("\n" + "=" * 80)
print("2. FAMILY LEARNING (Organic Families)")
print("=" * 80)

families_path = Path("persona_layer/organic_families.json")
if families_path.exists():
    with open(families_path) as f:
        families_data = json.load(f)

    families = families_data.get('families', {})
    print(f"\n📊 Family Structure:")
    print(f"   Total families: {len(families)}")

    for i, (family_id, family) in enumerate(list(families.items())[:2], 1):  # Show first 2
        print(f"\n   Family {i}:")
        print(f"      ID: {family_id}")
        print(f"      Members: {len(family.get('members', []))}")
        print(f"      Maturity: {family.get('maturity_level', 0)}")

        # Signature
        signature = family.get('signature', {})
        if signature:
            print(f"      Signature: {len(signature)} organs")
            top_organs = sorted(signature.items(), key=lambda x: x[1], reverse=True)[:3]
            for organ, weight in top_organs:
                print(f"         {organ}: {weight:.3f}")

    print(f"\n💡 What Families learn:")
    print(f"   - 57D organ signature patterns (which organs active)")
    print(f"   - V0 target energy (optimal convergence point)")
    print(f"   - Conversation style per family")

    print(f"\n🔗 Emoji/Glyph Integration Point:")
    print(f"   → Could learn: Family-specific emoji rhythms")
    print(f"   → Example: Family A prefers 🌸 warmth, Family B prefers ⚡ directness")
    print(f"   → Could track: Glyph emergence success per family")

else:
    print("   ⚠️  Families file not found")

# ==============================================================================
# 3. TRAINING PAIRS STRUCTURE
# ==============================================================================
print("\n" + "=" * 80)
print("3. TRAINING PAIRS STRUCTURE")
print("=" * 80)

training_path = Path("knowledge_base/conversational_training_pairs.json")
if training_path.exists():
    with open(training_path) as f:
        training_data = json.load(f)

    print(f"\n📊 Training Data:")
    print(f"   Categories: {len(training_data.get('categories', []))}")

    total_pairs = sum(len(cat['pairs']) for cat in training_data.get('categories', []))
    print(f"   Total pairs: {total_pairs}")

    # Show sample pair
    if training_data.get('categories'):
        sample_cat = training_data['categories'][0]
        print(f"\n   Example category: {sample_cat.get('name', 'unknown')}")
        if sample_cat.get('pairs'):
            pair = sample_cat['pairs'][0]
            print(f"      User: {pair.get('user_input', '')[:60]}...")
            print(f"      Expected: {pair.get('dae_response', '')[:60]}...")

            # Check for existing fields
            print(f"\n   Current fields in pair:")
            for key in pair.keys():
                print(f"      - {key}")

    print(f"\n💡 What Training Pairs provide:")
    print(f"   - User input examples")
    print(f"   - Expected DAE responses")
    print(f"   - Category labels (burnout, trauma, etc.)")

    print(f"\n🔗 Emoji/Glyph Integration Point:")
    print(f"   → Could add: 'target_emoji' field")
    print(f"   → Could add: 'avoid_emoji' field")
    print(f"   → Could add: 'kairos_eligible' flag")
    print(f"   → Could add: 'expected_polyvagal_state' field")
    print(f"   → Training would learn: Right emoji for right moment")

else:
    print("   ⚠️  Training pairs file not found")

# ==============================================================================
# 4. TRAINING PROCESSORS (How Learning Happens)
# ==============================================================================
print("\n" + "=" * 80)
print("4. TRAINING PROCESSORS (Learning Mechanisms)")
print("=" * 80)

processors = [
    ("conversational_training_pair_processor.py", "Processes training pairs"),
    ("organ_coupling_learner.py", "Updates R-matrix from conversations"),
    ("family_v0_learner.py", "Learns V0 targets per family"),
    ("conversational_cluster_learning.py", "Forms new families from patterns")
]

print(f"\n📊 Learning Components:")
for filename, description in processors:
    filepath = Path("persona_layer") / filename
    exists = "✅" if filepath.exists() else "❌"
    print(f"   {exists} {filename}")
    print(f"      Purpose: {description}")

print(f"\n💡 Learning Flow:")
print(f"   1. User input → Organism processes → Emission generated")
print(f"   2. Compare emission to training target")
print(f"   3. Update R-matrix (organ couplings)")
print(f"   4. Update family patterns (if family match)")
print(f"   5. Form new families (if novel pattern)")

print(f"\n🔗 Emoji/Glyph Integration Points:")
print(f"   → In pair processor: Evaluate emoji appropriateness")
print(f"   → In R-matrix: Learn organ→emoji associations")
print(f"   → In families: Learn family emoji rhythms")
print(f"   → New metric: Emoji match score (did right emoji emerge?)")

# ==============================================================================
# 5. INTEGRATION RECOMMENDATIONS
# ==============================================================================
print("\n" + "=" * 80)
print("5. INTEGRATION RECOMMENDATIONS")
print("=" * 80)

print(f"\n📋 Where to Add Emoji/Glyph Learning:")
print(f"\n   1. TRAINING PAIRS:")
print(f"      - Add 'target_emoji' field")
print(f"      - Add 'target_glyph' field (for kairos moments)")
print(f"      - Add 'polyvagal_emoji_family' field")
print(f"\n   2. R-MATRIX:")
print(f"      - Add 'organ_emoji_associations' dict")
print(f"      - Track: EMPATHY+BOND → 🫂 success rate")
print(f"      - Track: PRESENCE+WISDOM → 🧘 success rate")
print(f"\n   3. FAMILIES:")
print(f"      - Add 'emoji_rhythm' to family signature")
print(f"      - Track: Which emojis work best for this family")
print(f"      - Track: Glyph emergence timing per family")
print(f"\n   4. NEW COMPONENT:")
print(f"      - emoji_felt_library.json (80+ mappings)")
print(f"      - glyph_felt_library.json (20+ glyphs)")
print(f"      - emoji_post_processor.py (action text → emoji)")
print(f"      - emoji_learning_metrics.py (evaluate emoji appropriateness)")

# ==============================================================================
# 6. SUMMARY
# ==============================================================================
print("\n" + "=" * 80)
print("SUMMARY: Current Learning Capabilities")
print("=" * 80)

print(f"\n✅ What the system CAN learn now:")
print(f"   - Organ coupling patterns (R-matrix)")
print(f"   - Conversation family signatures (57D)")
print(f"   - V0 convergence targets per family")
print(f"   - Response patterns from training pairs")

print(f"\n🔜 What we NEED to add for emoji/glyph learning:")
print(f"   - Emoji felt library (organ → emoji mappings)")
print(f"   - Glyph kairos library (meta-atom → glyph)")
print(f"   - Training pair emoji targets")
print(f"   - Emoji evaluation metrics")
print(f"   - Post-processor for action text → emoji")

print(f"\n🎯 Recommended Implementation Order:")
print(f"   1. Create emoji_felt_library.json (Phase 1.5a)")
print(f"   2. Integrate emoji guidance in LLM prompt (Phase 1.5b)")
print(f"   3. Add emoji post-processor (Phase 1.5b)")
print(f"   4. Test emoji generation (Phase 1.5c)")
print(f"   5. Add emoji fields to training pairs (Phase 1.5d)")
print(f"   6. Run baseline training with emoji feedback (Phase 1.5d)")
print(f"   7. Implement kairos glyph emergence (Phase 2)")

print("\n" + "=" * 80)
print("Assessment Complete!")
print("=" * 80)
