#!/usr/bin/env python3
"""
Test Non-Normalized Signature Discrimination
=============================================

The key insight from the 65D test: L2 normalization collapses information.
This test compares:
1. Raw (non-normalized) signatures using Euclidean distance
2. Cosine similarity on normalized signatures

Hypothesis: Raw signatures with Euclidean distance will show better family
discrimination because:
- Magnitude carries information (crisis = high urgency values)
- Agreement dimensions have different scales than coherences
- Absolute distances matter, not just angles

Date: November 16, 2025
"""

import numpy as np
from persona_layer.organ_signature_extractor import OrganSignatureExtractor


def create_crisis_felt_state():
    """Crisis: High NDAM, sympathetic, high urgency, organ disagreement."""
    return {
        'v0_initial': 1.0,
        'satisfaction': 0.3,
        'zone': 4,
        'urgency': 0.85,
        'organ_coherences': {
            'LISTENING': 0.45, 'EMPATHY': 0.42, 'WISDOM': 0.50,
            'AUTHENTICITY': 0.48, 'PRESENCE': 0.35, 'BOND': 0.60,
            'SANS': 0.40, 'NDAM': 0.95, 'RNX': 0.55, 'EO': 0.88, 'CARD': 0.72
        },
        'polyvagal_state': 'sympathetic'
    }, {
        'v0_final': 0.5,
        'satisfaction_final': 0.55,
        'zone': 3,
        'urgency': 0.65,
        'convergence_cycles': 4,
        'kairos_detected': False,
        'organ_coherences': {
            'LISTENING': 0.52, 'EMPATHY': 0.48, 'WISDOM': 0.55,
            'AUTHENTICITY': 0.50, 'PRESENCE': 0.42, 'BOND': 0.65,
            'SANS': 0.45, 'NDAM': 0.82, 'RNX': 0.60, 'EO': 0.78, 'CARD': 0.68
        },
        'polyvagal_state': 'sympathetic'
    }


def create_safety_felt_state():
    """Safety: Low NDAM, ventral, low urgency, high organ agreement."""
    return {
        'v0_initial': 0.8,
        'satisfaction': 0.6,
        'zone': 2,
        'urgency': 0.1,
        'organ_coherences': {
            'LISTENING': 0.82, 'EMPATHY': 0.85, 'WISDOM': 0.78,
            'AUTHENTICITY': 0.80, 'PRESENCE': 0.88, 'BOND': 0.75,
            'SANS': 0.83, 'NDAM': 0.25, 'RNX': 0.79, 'EO': 0.92, 'CARD': 0.76
        },
        'polyvagal_state': 'ventral'
    }, {
        'v0_final': 0.2,
        'satisfaction_final': 0.85,
        'zone': 1,
        'urgency': 0.0,
        'convergence_cycles': 2,
        'kairos_detected': True,
        'organ_coherences': {
            'LISTENING': 0.88, 'EMPATHY': 0.90, 'WISDOM': 0.85,
            'AUTHENTICITY': 0.87, 'PRESENCE': 0.92, 'BOND': 0.80,
            'SANS': 0.88, 'NDAM': 0.15, 'RNX': 0.84, 'EO': 0.95, 'CARD': 0.82
        },
        'polyvagal_state': 'ventral'
    }


def create_ambivalence_felt_state():
    """Ambivalence: Mixed state, high organ disagreement."""
    return {
        'v0_initial': 0.9,
        'satisfaction': 0.4,
        'zone': 3,
        'urgency': 0.45,
        'organ_coherences': {
            'LISTENING': 0.45, 'EMPATHY': 0.85, 'WISDOM': 0.35,
            'AUTHENTICITY': 0.90, 'PRESENCE': 0.30, 'BOND': 0.80,
            'SANS': 0.40, 'NDAM': 0.55, 'RNX': 0.25, 'EO': 0.60, 'CARD': 0.50
        },
        'polyvagal_state': 'mixed_state'
    }, {
        'v0_final': 0.4,
        'satisfaction_final': 0.65,
        'zone': 2,
        'urgency': 0.35,
        'convergence_cycles': 4,
        'kairos_detected': False,
        'organ_coherences': {
            'LISTENING': 0.52, 'EMPATHY': 0.82, 'WISDOM': 0.42,
            'AUTHENTICITY': 0.85, 'PRESENCE': 0.38, 'BOND': 0.75,
            'SANS': 0.48, 'NDAM': 0.45, 'RNX': 0.32, 'EO': 0.65, 'CARD': 0.55
        },
        'polyvagal_state': 'mixed_state'
    }


def create_collapse_felt_state():
    """Collapse: Dorsal, low activation, organ shutdown."""
    return {
        'v0_initial': 0.7,
        'satisfaction': 0.35,
        'zone': 5,
        'urgency': 0.2,
        'organ_coherences': {
            'LISTENING': 0.25, 'EMPATHY': 0.30, 'WISDOM': 0.28,
            'AUTHENTICITY': 0.22, 'PRESENCE': 0.15, 'BOND': 0.35,
            'SANS': 0.32, 'NDAM': 0.40, 'RNX': 0.20, 'EO': 0.45, 'CARD': 0.38
        },
        'polyvagal_state': 'dorsal'
    }, {
        'v0_final': 0.6,
        'satisfaction_final': 0.45,
        'zone': 4,
        'urgency': 0.25,
        'convergence_cycles': 3,
        'kairos_detected': False,
        'organ_coherences': {
            'LISTENING': 0.32, 'EMPATHY': 0.35, 'WISDOM': 0.30,
            'AUTHENTICITY': 0.28, 'PRESENCE': 0.22, 'BOND': 0.40,
            'SANS': 0.38, 'NDAM': 0.35, 'RNX': 0.25, 'EO': 0.50, 'CARD': 0.42
        },
        'polyvagal_state': 'dorsal'
    }


def extract_raw_65d_signature(extractor, initial, final):
    """Extract 65D signature WITHOUT L2 normalization."""
    from persona_layer.organ_agreement_metrics import OrganAgreementComputer

    # Get base 57D (normalized)
    base_sig = extractor.extract_transformation_signature_57d(initial, final)

    # Build raw 65D (denormalize base and add agreement)
    sig = np.zeros(65)

    # V0 Energy Transformation (raw values)
    sig[0] = initial.get('v0_initial', 1.0)
    sig[1] = final.get('v0_final', 0.5)
    sig[2] = sig[0] - sig[1]  # Descent magnitude
    sig[3] = abs(sig[2]) / max(sig[0], 1e-6)
    sig[4] = final.get('convergence_cycles', 3.0) - 3.0
    sig[5] = 1.0 if final.get('kairos_detected', False) else 0.0

    # Organ coherence shifts (raw)
    initial_organs = initial.get('organ_coherences', {})
    final_organs = final.get('organ_coherences', {})
    organ_names = ['LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
                   'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD']
    for i, organ in enumerate(organ_names):
        sig[6 + i] = final_organs.get(organ, 0.5) - initial_organs.get(organ, 0.5)

    # Polyvagal (one-hot)
    final_poly = final.get('polyvagal_state', 'ventral')
    if final_poly in ['ventral', 'ventral_vagal']:
        sig[17:20] = [1.0, 0.0, 0.0]
    elif final_poly == 'sympathetic':
        sig[17:20] = [0.0, 1.0, 0.0]
    elif final_poly in ['dorsal', 'dorsal_vagal']:
        sig[17:20] = [0.0, 0.0, 1.0]
    else:
        sig[17:20] = [0.33, 0.33, 0.33]

    # Zone transformation (amplified)
    initial_zone = initial.get('zone', 1)
    final_zone = final.get('zone', 1)
    zone_amp = 2.0
    sig[20] = zone_amp * (initial_zone - 1) / 4.0
    sig[21] = zone_amp * (final_zone - 1) / 4.0
    sig[22] = zone_amp * (final_zone - initial_zone) / 4.0

    # Satisfaction evolution
    sig[23] = initial.get('satisfaction', 0.5)
    sig[24] = final.get('satisfaction_final', 0.5)
    sig[25] = sig[24] - sig[23]
    sig[26] = abs(sig[25])
    sig[27] = 1.0 if sig[25] > 0.05 else 0.0
    sig[28] = final.get('satisfaction_variance', 0.0)

    # Convergence characteristics
    sig[29] = (final.get('convergence_cycles', 3.0) - 1.0) / 4.0
    sig[30] = final.get('convergence_speedup', 1.0)
    sig[31] = final.get('v0_descent_stability', 0.5)
    sig[32] = final.get('nexus_count', 5.0) / 15.0

    # Urgency shift (amplified)
    urgency_amp = 2.0
    sig[33] = urgency_amp * initial.get('urgency', 0.0)
    sig[34] = urgency_amp * final.get('urgency', 0.0)

    # Emission path (raw 0/1)
    emission_path = final.get('emission_path', 'fusion')
    if emission_path == 'direct':
        sig[35:38] = [1.0, 0.0, 0.0]
    elif emission_path == 'fusion':
        sig[35:38] = [0.0, 1.0, 0.0]
    elif emission_path == 'kairos':
        sig[35:38] = [0.0, 0.0, 1.0]
    else:
        sig[35:38] = [0.0, 0.0, 0.0]

    # Pad remaining base dimensions with zeros (transduction data not available)
    sig[38:57] = 0.0

    # Organ Agreement Metrics (RAW, not normalized!)
    computer = OrganAgreementComputer()
    agreement_state = computer.compute_full_agreement_state(final_organs)

    sig[57] = agreement_state.pairwise_agreement
    sig[58] = agreement_state.organ_entropy
    sig[59] = agreement_state.nexus_coherence
    sig[60] = agreement_state.multiplicity_index
    sig[61] = agreement_state.mean_coherence
    sig[62] = agreement_state.std_coherence
    sig[63] = agreement_state.max_disagreement
    sig[64] = 1.0 - agreement_state.std_coherence

    return sig


def euclidean_distance(a, b):
    """Compute Euclidean distance between two vectors."""
    return np.linalg.norm(a - b)


def cosine_similarity(a, b):
    """Compute cosine similarity."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def main():
    print("=" * 80)
    print("NON-NORMALIZED SIGNATURE DISCRIMINATION TEST")
    print("Comparing Euclidean distance on raw signatures vs cosine similarity")
    print("=" * 80)

    extractor = OrganSignatureExtractor()

    categories = {
        'crisis': create_crisis_felt_state(),
        'safety': create_safety_felt_state(),
        'ambivalence': create_ambivalence_felt_state(),
        'collapse': create_collapse_felt_state()
    }

    # Extract signatures
    raw_signatures = {}
    normalized_signatures = {}

    for name, (initial, final) in categories.items():
        raw_signatures[name] = extract_raw_65d_signature(extractor, initial, final)
        normalized_signatures[name] = extractor.extract_transformation_signature_65d(initial, final)

    category_names = list(categories.keys())

    print("\n" + "=" * 80)
    print("EUCLIDEAN DISTANCES (raw signatures) - HIGHER = MORE SEPARATED")
    print("=" * 80)

    distances_raw = {}
    for i, name1 in enumerate(category_names):
        for name2 in category_names[i+1:]:
            dist = euclidean_distance(raw_signatures[name1], raw_signatures[name2])
            key = f"{name1} vs {name2}"
            distances_raw[key] = dist
            print(f"  {key:30s}: {dist:.4f}")

    print("\n" + "=" * 80)
    print("COSINE SIMILARITY (normalized signatures) - LOWER = MORE SEPARATED")
    print("=" * 80)

    similarities_norm = {}
    for i, name1 in enumerate(category_names):
        for name2 in category_names[i+1:]:
            sim = cosine_similarity(normalized_signatures[name1], normalized_signatures[name2])
            key = f"{name1} vs {name2}"
            similarities_norm[key] = sim
            print(f"  {key:30s}: {sim:.4f}")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    mean_dist = np.mean(list(distances_raw.values()))
    std_dist = np.std(list(distances_raw.values()))
    mean_sim = np.mean(list(similarities_norm.values()))
    std_sim = np.std(list(similarities_norm.values()))

    print(f"\nRaw Euclidean Distances:")
    print(f"  Mean: {mean_dist:.4f}")
    print(f"  Std:  {std_dist:.4f}")
    print(f"  Min:  {min(distances_raw.values()):.4f}")
    print(f"  Max:  {max(distances_raw.values()):.4f}")

    print(f"\nNormalized Cosine Similarities:")
    print(f"  Mean: {mean_sim:.4f}")
    print(f"  Std:  {std_sim:.4f}")
    print(f"  Min:  {min(similarities_norm.values()):.4f}")
    print(f"  Max:  {max(similarities_norm.values()):.4f}")

    # Recommendation
    print("\n" + "=" * 80)
    print("RECOMMENDATION FOR MULTI-FAMILY EMERGENCE")
    print("=" * 80)

    if std_dist > 0.5:
        print("✅ RAW EUCLIDEAN DISTANCES show GOOD separation!")
        print(f"   Std = {std_dist:.4f} > 0.5")
        print("")
        print("RECOMMENDED CHANGES:")
        print("1. Modify organic_conversational_families.py to use Euclidean distance:")
        print("   ```python")
        print("   distance = np.linalg.norm(signature - centroid)")
        print("   # Create new family if distance > threshold (e.g., 2.0)")
        print("   ```")
        print("")
        print("2. Remove L2 normalization from signature extraction")
        print("3. Set distance threshold based on observed separation:")
        print(f"   Suggested threshold: {mean_dist * 0.5:.4f} (half of mean distance)")
    else:
        print("⚠️ Raw distances still show limited separation")
        print("Consider alternative approaches:")
        print("- Weighted dimensions (emphasize polyvagal, urgency)")
        print("- Categorical encoding only (no continuous values)")
        print("- Hierarchical clustering instead of centroid-based")

    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
