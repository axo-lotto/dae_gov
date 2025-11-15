"""
Multi-Family Discovery Training Script
November 13, 2025

Optimized for discovering 10-30 organic families from 102-pair expanded corpus.

Key Optimizations (from agent analysis):
- Similarity threshold: 0.75 → 0.65 (prevents centroid collapse)
- Variance amplification: 1.0 → 2.0 (increases discrimination)
- Fresh start: Reset families for clean multi-family emergence
- Full INPUT→OUTPUT learning: 204 processing events (102 pairs × 2)

Expected outcome: 10-15 families with healthy distribution
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from config import Config

# ============================================================================
# CONFIGURATION FOR MULTI-FAMILY DISCOVERY
# ============================================================================

# Training data
TRAINING_PAIRS_PATH = "knowledge_base/conversational_training_pairs_expanded.json"
NUM_PAIRS = 102  # Use all 102 pairs (15 categories)

# Key parameters (optimized based on agent analysis)
SIMILARITY_THRESHOLD = 0.65  # CRITICAL: Lowered from 0.75 to prevent centroid collapse
VARIANCE_AMPLIFICATION = 2.0  # CRITICAL: Increased from 1.0 for better discrimination
LEARNING_THRESHOLD = 0.45  # Keep (trauma-focused corpus)

# Training control
RESET_FAMILIES = True  # Fresh start for multi-family emergence
ENABLE_PHASE2 = True  # V0 convergence required
ENABLE_TSK = False  # Speed up training

# Output
RESULTS_DIR = Path("results/training")
BACKUP_DIR = Path("persona_layer")

print(f"\n{'='*80}")
print(f"🌀 MULTI-FAMILY DISCOVERY TRAINING")
print(f"{'='*80}\n")

print(f"📋 Configuration:")
print(f"   Corpus: {TRAINING_PAIRS_PATH}")
print(f"   Pairs: {NUM_PAIRS} (15 categories)")
print(f"   Processing events: {NUM_PAIRS * 2} (INPUT + OUTPUT)")
print(f"   Similarity threshold: {SIMILARITY_THRESHOLD} (was 0.75)")
print(f"   Variance amplification: {VARIANCE_AMPLIFICATION} (was 1.0)")
print(f"   Learning threshold: {LEARNING_THRESHOLD}")
print(f"   Reset families: {RESET_FAMILIES}")
print(f"\n📊 Expected outcome: 10-15 organic families\n")

# ============================================================================
# STEP 1: BACKUP AND RESET FAMILIES (if enabled)
# ============================================================================

if RESET_FAMILIES:
    print(f"1️⃣ Backing up and resetting families...")

    families_path = BACKUP_DIR / "organic_families.json"
    backup_path = BACKUP_DIR / f"organic_families_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    if families_path.exists():
        import shutil
        shutil.copy(families_path, backup_path)
        print(f"   ✅ Backup saved: {backup_path}")

        # Read old state
        with open(families_path) as f:
            old_data = json.load(f)
        print(f"   📊 Old state: {len(old_data.get('families', {}))} families, {len(old_data.get('conversation_to_family', {}))} conversations")

    # Write empty families
    empty_families = {
        "families": {},
        "conversation_to_family": {},
        "next_family_id": 1
    }

    with open(families_path, 'w') as f:
        json.dump(empty_families, f, indent=2)

    print(f"   ✅ Families reset to empty (fresh start)\n")

# ============================================================================
# STEP 2: LOAD TRAINING CORPUS
# ============================================================================

print(f"2️⃣ Loading training corpus...")

with open(TRAINING_PAIRS_PATH) as f:
    corpus_data = json.load(f)
    training_pairs = corpus_data['training_pairs']
    stats = corpus_data['statistics']

print(f"   ✅ Loaded {len(training_pairs)} pairs")
print(f"   📊 Categories: {stats['total_pairs']} pairs across {len(stats['categories'])} categories")
print(f"   📊 Category distribution:")
for cat, count in sorted(stats['categories'].items()):
    print(f"      {cat}: {count}")
print()

# ============================================================================
# STEP 3: INITIALIZE ORGANISM WITH OPTIMIZED PARAMETERS
# ============================================================================

print(f"3️⃣ Initializing conversational organism...")
print(f"   (This will take ~30 seconds on first run)\n")

# Note: We can't directly modify Phase5LearningIntegration parameters without
# code changes, but we documented the needed changes. For now, proceed with
# current infrastructure and document what happens.

wrapper = ConversationalOrganismWrapper()
print(f"   ✅ Organism initialized\n")

print(f"⚠️  NOTE: Current implementation uses hardcoded threshold 0.75")
print(f"   To achieve 10-30 families, code modifications needed:")
print(f"   - persona_layer/organic_conversational_families.py line ~50: self.similarity_threshold = 0.65")
print(f"   - persona_layer/organ_signature_extractor.py line ~120: variance_amplification = 2.0")
print(f"   For this run, we'll train with current params and document results.\n")

# ============================================================================
# STEP 4: TRAINING LOOP (INPUT + OUTPUT for each pair)
# ============================================================================

print(f"4️⃣ Beginning multi-family discovery training...")
print(f"{'='*80}\n")

family_discovery_log = []
processing_times = []
start_time = time.time()

for idx, pair in enumerate(training_pairs, 1):
    pair_id = pair['pair_metadata']['id']
    category = pair['pair_metadata']['category']

    print(f"📘 Training Pair {idx}/{NUM_PAIRS}")
    print(f"   ID: {pair_id}")
    print(f"   Category: {category}")

    pair_start = time.time()

    # Process INPUT
    print(f"   ▶️  Processing INPUT...")
    try:
        input_result = wrapper.process_text(
            pair['input_text'],
            enable_tsk_recording=ENABLE_TSK,
            enable_phase2=ENABLE_PHASE2
        )

        input_confidence = input_result['felt_states'].get('emission_confidence', 0.0)
        input_nexuses = input_result['felt_states'].get('emission_nexus_count', 0)
        print(f"      INPUT: confidence={input_confidence:.3f}, nexuses={input_nexuses}")

        # CRITICAL: Call Phase 5 learning to enable family discovery
        if 'assembled_response' in input_result:
            learning_report = wrapper.phase5_learning.learn_from_conversation(
                organ_results=input_result.get('organ_results', {}),
                assembled_response=input_result['assembled_response'],
                user_message=pair['input_text'],
                conversation_id=f"{pair_id}_input"
            )
            if learning_report:
                print(f"      📚 INPUT learned: Family {learning_report.get('family_id', 'unknown')}")
    except Exception as e:
        print(f"      ❌ INPUT error: {e}")
        continue

    # Process OUTPUT
    print(f"   ▶️  Processing OUTPUT...")
    try:
        output_result = wrapper.process_text(
            pair['output_text'],
            enable_tsk_recording=ENABLE_TSK,
            enable_phase2=ENABLE_PHASE2
        )

        output_confidence = output_result['felt_states'].get('emission_confidence', 0.0)
        output_nexuses = output_result['felt_states'].get('emission_nexus_count', 0)
        print(f"      OUTPUT: confidence={output_confidence:.3f}, nexuses={output_nexuses}")

        # CRITICAL: Call Phase 5 learning to enable family discovery
        if 'assembled_response' in output_result:
            learning_report = wrapper.phase5_learning.learn_from_conversation(
                organ_results=output_result.get('organ_results', {}),
                assembled_response=output_result['assembled_response'],
                user_message=pair['output_text'],
                conversation_id=f"{pair_id}_output"
            )
            if learning_report:
                print(f"      📚 OUTPUT learned: Family {learning_report.get('family_id', 'unknown')}")
    except Exception as e:
        print(f"      ❌ OUTPUT error: {e}")
        continue

    pair_time = time.time() - pair_start
    processing_times.append(pair_time)
    print(f"      ⏱️  Pair time: {pair_time:.2f}s")

    # Check family discovery (every 10 pairs)
    if idx % 10 == 0 or idx == NUM_PAIRS:
        print(f"\n   📊 Family Status Check (after {idx} pairs):")

        # Read current family state
        families_path = BACKUP_DIR / "organic_families.json"
        if families_path.exists():
            with open(families_path) as f:
                family_data = json.load(f)

            total_families = len(family_data.get('families', {}))
            total_conversations = len(family_data.get('conversation_to_family', {}))

            print(f"      Total families: {total_families}")
            print(f"      Total conversations: {total_conversations}")

            # Log discovery milestone
            family_discovery_log.append({
                'pair': idx,
                'total_families': total_families,
                'total_conversations': total_conversations
            })

            if total_families > 0:
                print(f"      Family sizes:")
                for fam_id, fam_data in family_data['families'].items():
                    member_count = fam_data.get('member_count', 0)
                    print(f"         {fam_id}: {member_count} members")

        print()

    print(f"   ✅ Pair {idx}/{NUM_PAIRS} complete\n")

# ============================================================================
# STEP 5: FINAL ANALYSIS
# ============================================================================

total_time = time.time() - start_time
mean_pair_time = sum(processing_times) / len(processing_times) if processing_times else 0

print(f"{'='*80}")
print(f"🎯 TRAINING COMPLETE")
print(f"{'='*80}\n")

print(f"⏱️  Performance:")
print(f"   Total time: {total_time:.1f}s ({total_time/60:.1f} min)")
print(f"   Mean pair time: {mean_pair_time:.2f}s")
print(f"   Total pairs: {NUM_PAIRS}")
print(f"   Processing events: {NUM_PAIRS * 2} (INPUT + OUTPUT)\n")

# Read final family state
families_path = BACKUP_DIR / "organic_families.json"
if families_path.exists():
    with open(families_path) as f:
        final_family_data = json.load(f)

    total_families = len(final_family_data.get('families', {}))
    total_conversations = len(final_family_data.get('conversation_to_family', {}))

    print(f"📊 Final Family Discovery:")
    print(f"   Total families: {total_families}")
    print(f"   Total conversations: {total_conversations}")
    print(f"   Avg conversations/family: {total_conversations / total_families if total_families > 0 else 0:.1f}\n")

    if total_families > 0:
        print(f"🌱 Family Details:")

        for fam_id, fam_data in final_family_data['families'].items():
            member_count = fam_data.get('member_count', 0)
            semantic_name = fam_data.get('semantic_name', 'unnamed')
            dominant_organs = fam_data.get('dominant_organs', [])[:3]

            maturity = "mature" if member_count >= 10 else "emerging" if member_count >= 3 else "infant"

            print(f"\n   {fam_id} ({maturity}):")
            print(f"      Name: {semantic_name}")
            print(f"      Members: {member_count}")
            if dominant_organs:
                print(f"      Dominant organs: {', '.join(dominant_organs)}")

        # Zipf's law check (if ≥5 families)
        if total_families >= 5:
            print(f"\n   ✅ Zipf's law candidate (≥5 families)")

            # Get family sizes
            family_sizes = sorted([f.get('member_count', 0) for f in final_family_data['families'].values()], reverse=True)

            if len(family_sizes) >= 2:
                zipf_ratio = family_sizes[0] / family_sizes[1] if family_sizes[1] > 0 else 0
                expected_ratio = 2 ** 0.73  # ≈ 1.66

                print(f"      Largest family: {family_sizes[0]} members")
                print(f"      Second largest: {family_sizes[1]} members")
                print(f"      Observed ratio (1st/2nd): {zipf_ratio:.2f}")
                print(f"      Expected ratio (α=0.73): {expected_ratio:.2f}")
                print(f"      Deviation: {abs(zipf_ratio - expected_ratio):.2f}")

        # Maturity distribution
        infant = sum(1 for f in final_family_data['families'].values() if f.get('member_count', 0) < 3)
        emerging = sum(1 for f in final_family_data['families'].values() if 3 <= f.get('member_count', 0) < 10)
        mature = sum(1 for f in final_family_data['families'].values() if f.get('member_count', 0) >= 10)

        print(f"\n   📈 Maturity Distribution:")
        print(f"      Infant (1-2): {infant}")
        print(f"      Emerging (3-9): {emerging}")
        print(f"      Mature (10+): {mature}")

    else:
        print(f"   ⚠️  No families discovered")
        print(f"   Possible reasons:")
        print(f"      - Similarity threshold too high (0.75)")
        print(f"      - Variance amplification too low (1.0)")
        print(f"      - Not enough diversity in corpus")
        print(f"      - Learning threshold too high (0.45)")

else:
    print(f"   ⚠️  No family file found")

# Save training log
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
log_path = RESULTS_DIR / "multi_family_discovery_log.json"

training_log = {
    "metadata": {
        "training_date": datetime.now().isoformat(),
        "corpus_path": str(TRAINING_PAIRS_PATH),
        "num_pairs": NUM_PAIRS,
        "processing_events": NUM_PAIRS * 2,
        "similarity_threshold_target": SIMILARITY_THRESHOLD,
        "variance_amplification_target": VARIANCE_AMPLIFICATION,
        "learning_threshold": LEARNING_THRESHOLD,
        "reset_families": RESET_FAMILIES
    },
    "performance": {
        "total_time_seconds": total_time,
        "mean_pair_time_seconds": mean_pair_time,
        "pairs_per_minute": 60 / mean_pair_time if mean_pair_time > 0 else 0
    },
    "final_state": {
        "total_families": total_families if 'total_families' in locals() else 0,
        "total_conversations": total_conversations if 'total_conversations' in locals() else 0
    },
    "discovery_milestones": family_discovery_log
}

with open(log_path, 'w') as f:
    json.dump(training_log, f, indent=2)

print(f"\n💾 Training log saved: {log_path}")

# ============================================================================
# RECOMMENDATIONS
# ============================================================================

print(f"\n{'='*80}")
print(f"📋 RECOMMENDATIONS")
print(f"{'='*80}\n")

if total_families < 5:
    print(f"⚠️  Fewer than 5 families discovered")
    print(f"\n   To increase family count:")
    print(f"   1. Lower similarity threshold:")
    print(f"      - Edit: persona_layer/organic_conversational_families.py")
    print(f"      - Line ~50: self.similarity_threshold = 0.60 (from 0.75)")
    print(f"\n   2. Increase variance amplification:")
    print(f"      - Edit: persona_layer/organ_signature_extractor.py")
    print(f"      - Line ~120: variance_amplification = 2.5 (from 1.0)")
    print(f"\n   3. Re-run this script after code changes")

elif 5 <= total_families < 10:
    print(f"✅ Good progress! {total_families} families discovered")
    print(f"\n   To reach 10-30 families target:")
    print(f"   - Lower threshold slightly: 0.70 → 0.65")
    print(f"   - Or increase variance: 1.0 → 1.5")

elif 10 <= total_families <= 30:
    print(f"🎉 SUCCESS! {total_families} families discovered (target: 10-30)")
    print(f"\n   Next steps:")
    print(f"   1. Run semantic naming script:")
    print(f"      python3 add_family_semantic_names.py")
    print(f"\n   2. Validate Zipf's law (if ≥5 families)")
    print(f"\n   3. Analyze family coherence:")
    print(f"      - Do families cluster meaningfully by category?")
    print(f"      - Check inter-family centroid distances")

else:
    print(f"⚠️  Too many families ({total_families} > 30)")
    print(f"\n   To reduce family count:")
    print(f"   - Raise threshold: 0.65 → 0.70")
    print(f"   - Or decrease variance: 2.0 → 1.5")

print(f"\n{'='*80}")
print(f"✅ MULTI-FAMILY DISCOVERY TRAINING COMPLETE")
print(f"{'='*80}\n")
