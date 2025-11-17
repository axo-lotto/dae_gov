"""
Comprehensive TSK Data Analysis
================================

Analyzes 150 TSK files to characterize:
1. Zone transformation patterns (initial_zone → final_zone)
2. Polyvagal state transitions
3. Urgency distributions
4. Nexus type patterns with context
5. V0 convergence characteristics
6. Transformation signature statistics

Date: November 17, 2025
Purpose: Identify development areas before LLM-free training
"""

import json
import sys
from pathlib import Path
from collections import defaultdict, Counter
import numpy as np

def analyze_tsk_files():
    """
    Comprehensive analysis of all TSK files.

    Corrects for nested structure:
    - Zone/polyvagal/urgency in tsk.initial_*/final_* fields
    - Transformation signatures in tsk.transformation_signature
    - Transduction trajectory in felt_states.transduction_trajectory
    """

    print("=" * 80)
    print("🔍 COMPREHENSIVE TSK DATA ANALYSIS")
    print("=" * 80)

    tsk_dir = Path("results/tsk_logs")

    if not tsk_dir.exists():
        print(f"\n❌ TSK directory not found: {tsk_dir}")
        return

    # Find all TSK JSON files
    tsk_files = list(tsk_dir.rglob("*_tsk.json"))

    print(f"\n📊 Found {len(tsk_files)} TSK files")

    # Analysis accumulators
    zone_transitions = []  # (initial, final) tuples
    polyvagal_transitions = []  # (initial, final) tuples
    urgency_initial = []
    urgency_final = []
    urgency_deltas = []
    nexus_types = []
    nexus_by_zone = defaultdict(list)  # zone → nexus types
    nexus_by_polyvagal = defaultdict(list)  # polyvagal → nexus types
    v0_initial = []
    v0_final = []
    v0_descent = []
    convergence_cycles = []
    satisfaction_initial = []
    satisfaction_final = []
    satisfaction_deltas = []
    kairos_detected_count = 0
    transformation_signatures = []  # 57D arrays

    missing_fields = defaultdict(int)
    files_processed = 0

    print(f"\n🔄 Processing TSK files...")

    for tsk_file in tsk_files:
        try:
            with open(tsk_file, 'r') as f:
                data = json.load(f)

            felt_states = data.get('felt_states', {})
            tsk = felt_states.get('tsk', {})

            # Zone transitions (from tsk.initial_zone, tsk.final_zone)
            initial_zone = tsk.get('initial_zone')
            final_zone = tsk.get('final_zone')
            if initial_zone is not None and final_zone is not None:
                zone_transitions.append((initial_zone, final_zone))
            else:
                missing_fields['zone'] += 1

            # Polyvagal transitions (from tsk.initial_polyvagal_state, tsk.final_polyvagal_state)
            initial_polyvagal = tsk.get('initial_polyvagal_state')
            final_polyvagal = tsk.get('final_polyvagal_state')
            if initial_polyvagal is not None and final_polyvagal is not None:
                polyvagal_transitions.append((initial_polyvagal, final_polyvagal))
            else:
                missing_fields['polyvagal'] += 1

            # Urgency (from tsk.initial_urgency, tsk.final_urgency)
            initial_urg = tsk.get('initial_urgency')
            final_urg = tsk.get('final_urgency')
            if initial_urg is not None:
                urgency_initial.append(initial_urg)
            if final_urg is not None:
                urgency_final.append(final_urg)
            if initial_urg is not None and final_urg is not None:
                urgency_deltas.append(final_urg - initial_urg)
            else:
                missing_fields['urgency'] += 1

            # Transformation signature (from tsk.transformation_signature)
            sig = tsk.get('transformation_signature')
            if sig is not None and len(sig) == 57:
                transformation_signatures.append(sig)
            else:
                missing_fields['signature'] += 1

            # V0 energy (from felt_states top level)
            v0_init = felt_states.get('v0_energy_initial')
            v0_fin = felt_states.get('v0_energy_final')
            if v0_init is not None:
                v0_initial.append(v0_init)
            if v0_fin is not None:
                v0_final.append(v0_fin)
            if v0_init is not None and v0_fin is not None:
                v0_descent.append(v0_init - v0_fin)

            # Convergence cycles
            cycles = felt_states.get('convergence_cycles')
            if cycles is not None:
                convergence_cycles.append(cycles)

            # Satisfaction
            sat_init = felt_states.get('satisfaction_initial')
            sat_fin = felt_states.get('satisfaction_final')
            if sat_init is not None:
                satisfaction_initial.append(sat_init)
            if sat_fin is not None:
                satisfaction_final.append(sat_fin)
            if sat_init is not None and sat_fin is not None:
                satisfaction_deltas.append(sat_fin - sat_init)

            # Kairos detection
            kairos = felt_states.get('kairos_detected', False)
            if kairos:
                kairos_detected_count += 1

            # Nexus types from transduction trajectory
            trajectory = felt_states.get('transduction_trajectory', [])
            for step in trajectory:
                nexus_type = step.get('current_type')
                if nexus_type:
                    nexus_types.append(nexus_type)

                    # Associate with zone/polyvagal
                    if final_zone is not None:
                        nexus_by_zone[final_zone].append(nexus_type)
                    if final_polyvagal is not None:
                        nexus_by_polyvagal[final_polyvagal].append(nexus_type)

            files_processed += 1

        except Exception as e:
            print(f"   ⚠️  Error processing {tsk_file.name}: {e}")
            continue

    print(f"\n✅ Processed {files_processed}/{len(tsk_files)} files successfully")

    if missing_fields:
        print(f"\n⚠️  Missing Fields:")
        for field, count in missing_fields.items():
            print(f"   {field}: {count}/{files_processed} files ({100*count/files_processed:.1f}%)")

    # =============================================================================
    # ANALYSIS RESULTS
    # =============================================================================

    print("\n" + "=" * 80)
    print("📊 ZONE TRANSFORMATION PATTERNS")
    print("=" * 80)

    if zone_transitions:
        zone_counter = Counter(zone_transitions)
        print(f"\nTotal zone transitions: {len(zone_transitions)}")
        print(f"\nTop 10 zone transitions:")
        for (z_init, z_fin), count in zone_counter.most_common(10):
            pct = 100 * count / len(zone_transitions)
            print(f"   Zone {z_init} → Zone {z_fin}: {count} ({pct:.1f}%)")

        # Stability vs transformation
        stable = sum(1 for z_init, z_fin in zone_transitions if z_init == z_fin)
        transformed = len(zone_transitions) - stable
        print(f"\n   Stable (same zone): {stable} ({100*stable/len(zone_transitions):.1f}%)")
        print(f"   Transformed (zone change): {transformed} ({100*transformed/len(zone_transitions):.1f}%)")

    print("\n" + "=" * 80)
    print("🧠 POLYVAGAL STATE TRANSITIONS")
    print("=" * 80)

    if polyvagal_transitions:
        poly_counter = Counter(polyvagal_transitions)
        print(f"\nTotal polyvagal transitions: {len(polyvagal_transitions)}")
        print(f"\nTop 10 polyvagal transitions:")
        for (p_init, p_fin), count in poly_counter.most_common(10):
            pct = 100 * count / len(polyvagal_transitions)
            print(f"   {p_init} → {p_fin}: {count} ({pct:.1f}%)")

        # Stability vs transformation
        stable = sum(1 for p_init, p_fin in polyvagal_transitions if p_init == p_fin)
        transformed = len(polyvagal_transitions) - stable
        print(f"\n   Stable (same state): {stable} ({100*stable/len(polyvagal_transitions):.1f}%)")
        print(f"   Transformed (state change): {transformed} ({100*transformed/len(polyvagal_transitions):.1f}%)")

    print("\n" + "=" * 80)
    print("⚡ URGENCY DISTRIBUTIONS")
    print("=" * 80)

    if urgency_initial:
        print(f"\nInitial Urgency (n={len(urgency_initial)}):")
        print(f"   Mean: {np.mean(urgency_initial):.3f}")
        print(f"   Std:  {np.std(urgency_initial):.3f}")
        print(f"   Min:  {np.min(urgency_initial):.3f}")
        print(f"   Max:  {np.max(urgency_initial):.3f}")

    if urgency_final:
        print(f"\nFinal Urgency (n={len(urgency_final)}):")
        print(f"   Mean: {np.mean(urgency_final):.3f}")
        print(f"   Std:  {np.std(urgency_final):.3f}")
        print(f"   Min:  {np.min(urgency_final):.3f}")
        print(f"   Max:  {np.max(urgency_final):.3f}")

    if urgency_deltas:
        print(f"\nUrgency Deltas (final - initial, n={len(urgency_deltas)}):")
        print(f"   Mean: {np.mean(urgency_deltas):.3f}")
        print(f"   Std:  {np.std(urgency_deltas):.3f}")

        increased = sum(1 for d in urgency_deltas if d > 0.05)
        decreased = sum(1 for d in urgency_deltas if d < -0.05)
        stable = len(urgency_deltas) - increased - decreased
        print(f"\n   Increased (Δ > 0.05): {increased} ({100*increased/len(urgency_deltas):.1f}%)")
        print(f"   Decreased (Δ < -0.05): {decreased} ({100*decreased/len(urgency_deltas):.1f}%)")
        print(f"   Stable (-0.05 ≤ Δ ≤ 0.05): {stable} ({100*stable/len(urgency_deltas):.1f}%)")

    print("\n" + "=" * 80)
    print("🔗 NEXUS TYPE PATTERNS")
    print("=" * 80)

    if nexus_types:
        nexus_counter = Counter(nexus_types)
        print(f"\nTotal nexus occurrences: {len(nexus_types)}")
        print(f"Unique nexus types: {len(nexus_counter)}")
        print(f"\nNexus type distribution:")
        for nexus_type, count in nexus_counter.most_common():
            pct = 100 * count / len(nexus_types)
            print(f"   {nexus_type}: {count} ({pct:.1f}%)")

    print("\n" + "=" * 80)
    print("🌀 NEXUS BY ZONE (Contextual Patterns)")
    print("=" * 80)

    for zone in sorted(nexus_by_zone.keys()):
        zone_nexuses = nexus_by_zone[zone]
        zone_counter = Counter(zone_nexuses)
        print(f"\nZone {zone} (n={len(zone_nexuses)}):")
        for nexus_type, count in zone_counter.most_common(5):
            pct = 100 * count / len(zone_nexuses)
            print(f"   {nexus_type}: {count} ({pct:.1f}%)")

    print("\n" + "=" * 80)
    print("🧠 NEXUS BY POLYVAGAL STATE")
    print("=" * 80)

    for state in sorted(nexus_by_polyvagal.keys()):
        state_nexuses = nexus_by_polyvagal[state]
        state_counter = Counter(state_nexuses)
        print(f"\n{state} (n={len(state_nexuses)}):")
        for nexus_type, count in state_counter.most_common(5):
            pct = 100 * count / len(state_nexuses)
            print(f"   {nexus_type}: {count} ({pct:.1f}%)")

    print("\n" + "=" * 80)
    print("⚡ V0 ENERGY CONVERGENCE")
    print("=" * 80)

    if v0_initial:
        print(f"\nInitial V0 (n={len(v0_initial)}):")
        print(f"   Mean: {np.mean(v0_initial):.3f}")
        print(f"   Std:  {np.std(v0_initial):.3f}")

    if v0_final:
        print(f"\nFinal V0 (n={len(v0_final)}):")
        print(f"   Mean: {np.mean(v0_final):.3f}")
        print(f"   Std:  {np.std(v0_final):.3f}")

    if v0_descent:
        print(f"\nV0 Descent (initial - final, n={len(v0_descent)}):")
        print(f"   Mean: {np.mean(v0_descent):.3f}")
        print(f"   Std:  {np.std(v0_descent):.3f}")
        print(f"   Min:  {np.min(v0_descent):.3f}")
        print(f"   Max:  {np.max(v0_descent):.3f}")

    if convergence_cycles:
        print(f"\nConvergence Cycles (n={len(convergence_cycles)}):")
        print(f"   Mean: {np.mean(convergence_cycles):.3f}")
        print(f"   Std:  {np.std(convergence_cycles):.3f}")
        cycle_counter = Counter(convergence_cycles)
        for cycles, count in sorted(cycle_counter.items()):
            pct = 100 * count / len(convergence_cycles)
            print(f"   {cycles} cycles: {count} ({pct:.1f}%)")

    print(f"\nKairos Detection:")
    print(f"   Detected: {kairos_detected_count}/{files_processed} ({100*kairos_detected_count/files_processed:.1f}%)")

    print("\n" + "=" * 80)
    print("😊 SATISFACTION EVOLUTION")
    print("=" * 80)

    if satisfaction_initial:
        print(f"\nInitial Satisfaction (n={len(satisfaction_initial)}):")
        print(f"   Mean: {np.mean(satisfaction_initial):.3f}")
        print(f"   Std:  {np.std(satisfaction_initial):.3f}")

    if satisfaction_final:
        print(f"\nFinal Satisfaction (n={len(satisfaction_final)}):")
        print(f"   Mean: {np.mean(satisfaction_final):.3f}")
        print(f"   Std:  {np.std(satisfaction_final):.3f}")

    if satisfaction_deltas:
        print(f"\nSatisfaction Deltas (final - initial, n={len(satisfaction_deltas)}):")
        print(f"   Mean: {np.mean(satisfaction_deltas):.3f}")
        print(f"   Std:  {np.std(satisfaction_deltas):.3f}")

        improved = sum(1 for d in satisfaction_deltas if d > 0.05)
        worsened = sum(1 for d in satisfaction_deltas if d < -0.05)
        stable = len(satisfaction_deltas) - improved - worsened
        print(f"\n   Improved (Δ > 0.05): {improved} ({100*improved/len(satisfaction_deltas):.1f}%)")
        print(f"   Worsened (Δ < -0.05): {worsened} ({100*worsened/len(satisfaction_deltas):.1f}%)")
        print(f"   Stable (-0.05 ≤ Δ ≤ 0.05): {stable} ({100*stable/len(satisfaction_deltas):.1f}%)")

    print("\n" + "=" * 80)
    print("🧬 57D TRANSFORMATION SIGNATURES")
    print("=" * 80)

    if transformation_signatures:
        print(f"\nSignatures collected: {len(transformation_signatures)}")

        # Compute statistics per dimension
        sig_array = np.array(transformation_signatures)

        print(f"\nSignature statistics:")
        print(f"   Mean magnitude: {np.mean(np.linalg.norm(sig_array, axis=1)):.3f}")
        print(f"   Std magnitude:  {np.std(np.linalg.norm(sig_array, axis=1)):.3f}")

        # Non-zero dimensions
        non_zero_per_sig = np.count_nonzero(sig_array, axis=1)
        print(f"\n   Mean non-zero dimensions: {np.mean(non_zero_per_sig):.1f}/57")
        print(f"   Std non-zero dimensions:  {np.std(non_zero_per_sig):.1f}")

        # Dimensions that are consistently non-zero
        non_zero_freq = np.count_nonzero(sig_array, axis=0)
        active_dims = np.sum(non_zero_freq > 0.5 * len(transformation_signatures))
        print(f"\n   Consistently active dimensions (>50% of sigs): {active_dims}/57")

    print("\n" + "=" * 80)
    print("✅ COMPREHENSIVE TSK ANALYSIS COMPLETE")
    print("=" * 80)

    return {
        'files_processed': files_processed,
        'zone_transitions': zone_transitions,
        'polyvagal_transitions': polyvagal_transitions,
        'urgency_deltas': urgency_deltas,
        'nexus_types': nexus_types,
        'nexus_by_zone': dict(nexus_by_zone),
        'nexus_by_polyvagal': dict(nexus_by_polyvagal),
        'v0_descent': v0_descent,
        'satisfaction_deltas': satisfaction_deltas,
        'kairos_detected_count': kairos_detected_count,
        'transformation_signatures': transformation_signatures
    }


if __name__ == '__main__':
    try:
        results = analyze_tsk_files()
        print(f"\n✅ Analysis complete!")
        print(f"   Files processed: {results['files_processed']}")
    except Exception as e:
        print(f"\n❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
