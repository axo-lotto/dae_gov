"""
Add Semantic Names to Organic Conversational Families
November 13, 2025

Analyzes organ activation patterns in families and generates semantic names.
Based on DAE 3.0 family emergence patterns.
"""

import json
import numpy as np
from pathlib import Path
from collections import Counter

def analyze_family_signature(family_data):
    """Analyze family's organ activation signature to generate semantic name."""

    organ_activations = family_data['organ_activation_means']
    dominant_organs = family_data['dominant_organs']
    member_count = family_data['member_count']
    mean_satisfaction = family_data['mean_satisfaction']

    # Get member conversation IDs to analyze categories
    members = family_data['member_conversations']

    # Extract categories from conversation IDs (e.g., "arc_0200_sustainable_rhythm_ex1" → "sustainable_rhythm")
    categories = []
    for conv_id in members:
        parts = conv_id.split('_')
        if len(parts) >= 3:
            # Conversation IDs format: arc_NNNN_category_ex1
            category = '_'.join(parts[2:-1])  # Everything between number and ex1
            categories.append(category)

    category_distribution = Counter(categories)
    primary_category = category_distribution.most_common(1)[0] if category_distribution else ("unknown", 0)

    # Analyze organ activation pattern
    # Sort organs by activation strength
    sorted_organs = sorted(organ_activations.items(), key=lambda x: x[1], reverse=True)
    top_3_organs = [org[0] for org in sorted_organs[:3]]

    # Generate semantic name based on patterns
    semantic_name, semantic_description = generate_semantic_name(
        top_3_organs,
        category_distribution,
        mean_satisfaction,
        member_count
    )

    return {
        'semantic_name': semantic_name,
        'semantic_description': semantic_description,
        'category_distribution': dict(category_distribution),
        'primary_category': primary_category[0],
        'primary_category_count': primary_category[1],
        'top_3_organs': top_3_organs,
        'organ_activation_profile': {org: round(act, 3) for org, act in sorted_organs}
    }

def generate_semantic_name(top_organs, category_dist, mean_satisfaction, member_count):
    """
    Generate semantic name and description based on family characteristics.

    Naming strategy:
    - Top organ determines primary modality
    - Secondary organs determine nuance
    - Category distribution provides context
    - Satisfaction indicates effectiveness
    """

    # Organ semantic mappings
    organ_semantics = {
        'SANS': 'coherence_repair',
        'CARD': 'response_scaling',
        'PRESENCE': 'embodied_grounding',
        'LISTENING': 'deep_attunement',
        'EMPATHY': 'compassionate_holding',
        'WISDOM': 'pattern_recognition',
        'AUTHENTICITY': 'vulnerable_truth',
        'BOND': 'parts_integration',
        'NDAM': 'crisis_navigation',
        'RNX': 'temporal_rhythm',
        'EO': 'nervous_system_regulation'
    }

    # Get semantic tags for top 3 organs
    primary_tag = organ_semantics.get(top_organs[0], 'unknown')
    secondary_tag = organ_semantics.get(top_organs[1], 'unknown') if len(top_organs) > 1 else None
    tertiary_tag = organ_semantics.get(top_organs[2], 'unknown') if len(top_organs) > 2 else None

    # Get dominant conversation category
    if category_dist:
        primary_category = category_dist.most_common(1)[0][0]
        category_pct = (category_dist.most_common(1)[0][1] / sum(category_dist.values())) * 100
    else:
        primary_category = "general"
        category_pct = 100

    # Generate name based on pattern
    # Pattern: [primary_modality]_[context]

    # Map categories to semantic contexts
    category_contexts = {
        'sustainable_rhythm': 'sustainable_pacing',
        'psychological_safety': 'safety_cultivation',
        'witnessing_presence': 'witnessing_companionship',
        'burnout_spiral': 'burnout_recovery',
        'toxic_productivity': 'productivity_healing',
        'scapegoat_dynamics': 'scapegoat_repair'
    }

    context = category_contexts.get(primary_category, primary_category.replace('_', '_'))

    # Combine primary organ with context
    semantic_name = f"{primary_tag}_{context}"

    # Generate description
    description_parts = []

    # Primary characteristic
    organ_descriptions = {
        'SANS': 'Emphasizes semantic coherence and meaning repair',
        'CARD': 'Focuses on calibrated response scaling',
        'PRESENCE': 'Centered on embodied, grounded holding',
        'LISTENING': 'Characterized by deep relational attunement',
        'EMPATHY': 'Defined by compassionate, resonant presence',
        'WISDOM': 'Distinguished by pattern recognition and synthesis',
        'AUTHENTICITY': 'Marked by vulnerable truth-telling',
        'BOND': 'Oriented toward parts integration (IFS)',
        'NDAM': 'Specialized in crisis navigation',
        'RNX': 'Attuned to temporal rhythms and pacing',
        'EO': 'Grounded in nervous system regulation (polyvagal)'
    }

    description_parts.append(organ_descriptions.get(top_organs[0], 'Primary modality'))

    # Add secondary characteristic if present
    if secondary_tag:
        secondary_descriptions = {
            'coherence_repair': 'with semantic coherence support',
            'response_scaling': 'with response calibration',
            'embodied_grounding': 'with somatic grounding',
            'deep_attunement': 'with relational depth',
            'compassionate_holding': 'with compassionate resonance',
            'pattern_recognition': 'with pattern synthesis',
            'vulnerable_truth': 'with authentic disclosure',
            'parts_integration': 'with IFS integration',
            'crisis_navigation': 'with crisis awareness',
            'temporal_rhythm': 'with temporal attunement',
            'nervous_system_regulation': 'with nervous system awareness'
        }
        description_parts.append(secondary_descriptions.get(secondary_tag, f'and {secondary_tag}'))

    # Add context
    context_descriptions = {
        'sustainable_pacing': 'around sustainable rhythm and pacing',
        'safety_cultivation': 'focused on psychological safety',
        'witnessing_companionship': 'providing witnessing presence',
        'burnout_recovery': 'supporting burnout recovery',
        'productivity_healing': 'healing toxic productivity patterns',
        'scapegoat_repair': 'addressing scapegoat dynamics'
    }

    description_parts.append(context_descriptions.get(context, f'in {context} contexts'))

    # Add statistics
    description_parts.append(f"({member_count} conversations, satisfaction={mean_satisfaction:.2f})")

    semantic_description = '. '.join(description_parts) + '.'

    # Add category distribution if diverse
    if len(category_dist) > 1:
        top_3_categories = category_dist.most_common(3)
        cat_summary = ', '.join([f"{cat}({count})" for cat, count in top_3_categories])
        semantic_description += f" Mix: {cat_summary}."

    return semantic_name, semantic_description

def main():
    """Main function to add semantic names to families."""
    print("\n" + "="*70)
    print("🌀 ADDING SEMANTIC NAMES TO ORGANIC FAMILIES")
    print("="*70 + "\n")

    families_path = Path("persona_layer/organic_families.json")

    # Load families
    print("📂 Loading organic families...")
    with open(families_path) as f:
        data = json.load(f)

    families = data.get('families', {})
    total_families = len(families)

    print(f"   ✅ Loaded {total_families} families\n")

    # Analyze and name each family
    updates = []

    for family_id, family_data in families.items():
        print(f"🔍 Analyzing {family_id}...")
        print(f"   Members: {family_data['member_count']}")
        print(f"   Dominant organs: {', '.join(family_data['dominant_organs'])}")
        print(f"   Current name: {family_data.get('semantic_name', 'None')}")

        # Analyze family
        analysis = analyze_family_signature(family_data)

        # Update family data
        family_data['semantic_name'] = analysis['semantic_name']
        family_data['semantic_description'] = analysis['semantic_description']
        family_data['category_distribution'] = analysis['category_distribution']
        family_data['primary_category'] = analysis['primary_category']

        print(f"   ✅ New name: {analysis['semantic_name']}")
        print(f"   Description: {analysis['semantic_description'][:80]}...")
        print(f"   Primary category: {analysis['primary_category']} ({analysis['primary_category_count']} conversations)")
        print(f"   Top 3 organs: {', '.join(analysis['top_3_organs'])}")
        print()

        updates.append({
            'family_id': family_id,
            'semantic_name': analysis['semantic_name'],
            'primary_category': analysis['primary_category'],
            'member_count': family_data['member_count']
        })

    # Save updated families
    print("💾 Saving updated families...")
    data['last_updated'] = data.get('last_updated', '')  # Preserve last_updated

    with open(families_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"   ✅ Saved to {families_path}\n")

    # Summary
    print("="*70)
    print("✅ SEMANTIC NAMING COMPLETE")
    print("="*70 + "\n")

    print(f"📊 Summary:")
    print(f"   Total families: {total_families}")
    print(f"   Families named: {len(updates)}")

    if updates:
        print(f"\n   Family Names:")
        for update in updates:
            print(f"   - {update['family_id']}: {update['semantic_name']}")
            print(f"     ({update['member_count']} conversations, primary: {update['primary_category']})")

    print(f"\n🎯 Next Steps:")
    print(f"   1. Review family names in persona_layer/organic_families.json")
    print(f"   2. Run baseline training to accumulate more conversations")
    print(f"   3. Monitor family growth and emergence of new families")
    print(f"   4. Create family analytics dashboard (future)\n")

if __name__ == "__main__":
    main()
