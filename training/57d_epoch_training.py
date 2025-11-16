#!/usr/bin/env python3
"""
57D RNX/TSK Epoch Training - Multi-Family Emergence Validation
===============================================================
Tests the new 57D transformation signatures to verify:
1. Signatures are consistently 57D
2. Multiple families emerge (expect 3-8 from diverse inputs)
3. Nexus type transitions differentiate families
"""
import sys
import json
from datetime import datetime
import io

# Add project to path
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

# Suppress initialization output
old_stdout = sys.stdout
sys.stdout = io.StringIO()

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
organism = ConversationalOrganismWrapper()

sys.stdout = old_stdout

print('='*70)
print('57D RNX/TSK EPOCH TRAINING - MULTI-FAMILY EMERGENCE')
print('='*70)
print(f'Start time: {datetime.now().strftime("%H:%M:%S")}')

# Diverse therapeutic input patterns designed to trigger different nexus transitions
training_inputs = [
    # HIGH URGENCY / CRISIS (Urgency → Relational)
    ('I am absolutely panicking and cant breathe', 'urgency_crisis'),
    ('Everything is falling apart right now I need help immediately', 'urgency_escalation'),
    ('I feel like Im going to lose control', 'urgency_control_loss'),

    # RELATIONAL / CONNECTION (Relational → Innate)
    ('I feel really understood when you listen like this', 'relational_connection'),
    ('This space feels safe enough to be vulnerable', 'relational_safety'),
    ('Thank you for holding space for me', 'relational_gratitude'),

    # PROTECTIVE / BOUNDARIES (Protective → Innate)
    ('I need to set some boundaries around this conversation', 'protective_boundary'),
    ('Part of me wants to protect myself from getting hurt again', 'protective_parts'),
    ('I notice a wall going up when we talk about this', 'protective_wall'),

    # RECURSIVE / LOOPING (Looped → Relational)
    ('I keep going over the same thoughts again and again', 'recursive_rumination'),
    ('Im stuck in this pattern and cant break free', 'recursive_stuck'),
    ('Every time I try to move forward I end up back here', 'recursive_return'),

    # DISSOCIATIVE / FRAGMENTED (Dissociative → Innate)
    ('I feel disconnected from my body right now', 'dissociative_body'),
    ('Part of me feels far away from this conversation', 'dissociative_distant'),
    ('I notice Im spacing out when things get intense', 'dissociative_spacing'),

    # PARADOX / CONTRAST (Paradox → Relational)
    ('I want connection but Im also terrified of it', 'paradox_connection'),
    ('I need help but I also dont want to be a burden', 'paradox_help'),
    ('I feel strong but also completely broken', 'paradox_strength'),

    # ABSORBED / SYSTEMIC (Absorbed → Protective)
    ('The system is designed to keep me down', 'absorbed_systemic'),
    ('Society has failed people like me', 'absorbed_society'),
    ('I feel crushed by expectations from all sides', 'absorbed_pressure'),
]

results = []
families_seen = set()

print(f'\nProcessing {len(training_inputs)} diverse therapeutic inputs...')
print('-'*70)

for i, (text, pattern_name) in enumerate(training_inputs):
    # Suppress processing output
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    result = organism.process_text(text, context={'enable_transduction': True})

    sys.stdout = old_stdout

    felt_states = result.get('felt_states', {})
    family_id = felt_states.get('phase5_family_id', 'NONE')
    families_seen.add(family_id)

    emission = result.get('emission_text', '')[:60] + '...'
    confidence = result.get('emission_confidence', 0.0)

    results.append({
        'input': pattern_name,
        'family': family_id,
        'confidence': confidence,
        'emission': emission
    })

    # Progress indicator
    if (i + 1) % 7 == 0:
        print(f'   Processed {i+1}/{len(training_inputs)} inputs, {len(families_seen)} unique families so far')

print(f'\n✅ Processing complete!')
print('-'*70)

# Analyze results
filtered_families = sorted([f for f in families_seen if f != 'NONE'])
print(f'\n📊 TRAINING RESULTS:')
print(f'   Total inputs processed: {len(training_inputs)}')
print(f'   Unique families formed: {len(families_seen)}')
print(f'   Families: {filtered_families}')

# Load final family data
with open('persona_layer/organic_families.json', 'r') as f:
    fam_data = json.load(f)

total_families = len(fam_data['families'])
print(f'\n📐 57D SIGNATURE VERIFICATION:')
print(f'   Total families stored: {total_families}')

all_57d = True
for fam_id, fam_info in fam_data['families'].items():
    centroid_dim = len(fam_info.get('centroid', []))
    member_count = fam_info.get('conversation_count', 0)
    mean_sat = fam_info.get('mean_satisfaction', 0.0)
    print(f'   {fam_id}:')
    print(f'      Centroid: {centroid_dim}D')
    print(f'      Members: {member_count}')
    print(f'      Mean satisfaction: {mean_sat:.3f}')
    if centroid_dim != 57:
        all_57d = False

if all_57d and total_families > 0:
    print(f'\n✅ ALL FAMILIES HAVE 57D CENTROIDS!')
else:
    print(f'\n⚠️  Dimension verification failed or no families formed')

# Check family assignment distribution
family_counts = {}
for r in results:
    fam = r['family']
    family_counts[fam] = family_counts.get(fam, 0) + 1

print(f'\n📈 FAMILY ASSIGNMENT DISTRIBUTION:')
for fam, count in sorted(family_counts.items(), key=lambda x: x[1], reverse=True):
    bar = '█' * count
    print(f'   {fam}: {count} assignments {bar}')

# Success metrics
if total_families >= 3:
    print(f'\n✅ MULTI-FAMILY EMERGENCE SUCCESS!')
    print(f'   Expected 3-8 families from diverse inputs, got {total_families}')
    print(f'   57D RNX/TSK signatures enabling differentiation')
elif total_families >= 1:
    print(f'\n⚠️  Only {total_families} family formed')
    print(f'   May need more training epochs or lower similarity threshold')
else:
    print(f'\n❌ No families formed - check learning threshold and satisfaction scores')

# Save results
results_data = {
    'timestamp': datetime.now().isoformat(),
    'total_inputs': len(training_inputs),
    'total_families': total_families,
    'families': list(fam_data['families'].keys()),
    'all_57d': all_57d,
    'family_distribution': family_counts,
    'results': results
}

with open('results/57d_epoch_training_results.json', 'w') as f:
    json.dump(results_data, f, indent=2)

print(f'\nResults saved to: results/57d_epoch_training_results.json')
print(f'End time: {datetime.now().strftime("%H:%M:%S")}')
print('='*70)
