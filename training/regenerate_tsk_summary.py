#!/usr/bin/env python3
"""
Regenerate TSK Summary from Existing TSK Logs
Created: November 17, 2025

Post-processes TSK logs to create aggregated summary.
"""

import sys
import json
from pathlib import Path

def regenerate_tsk_summary(epoch_num: int):
    """Regenerate TSK summary from individual TSK files."""

    tsk_logs_dir = Path(f"results/tsk_logs/epoch_{epoch_num}")
    output_file = Path(f"results/epochs/epoch_{epoch_num}/tsk_summary.json")

    if not tsk_logs_dir.exists():
        print(f"❌ TSK logs directory not found: {tsk_logs_dir}")
        return False

    tsk_files = sorted(tsk_logs_dir.glob("*.json"))
    if not tsk_files:
        print(f"❌ No TSK files found in {tsk_logs_dir}")
        return False

    print(f"📊 Processing {len(tsk_files)} TSK files from Epoch {epoch_num}...")

    tsk_summary = {
        'epoch': epoch_num,
        'total_pairs': len(tsk_files),
        'zone_transitions': [],
        'polyvagal_trajectories': [],
        'kairos_detections': 0,
        'organ_signature_evolution': [],
        'transformation_pathways': []
    }

    for tsk_file in tsk_files:
        try:
            with open(tsk_file, 'r') as f:
                tsk_data = json.load(f)

            # Extract TSK from felt_states
            felt_states_tsk = tsk_data.get('felt_states', {}).get('tsk', {})
            if not felt_states_tsk:
                print(f"   ⚠️  No TSK in {tsk_file.name}")
                continue

            pair_id = tsk_file.stem.replace('_tsk', '')

            # Zone transitions
            initial_zone = felt_states_tsk.get('initial_zone')
            final_zone = felt_states_tsk.get('final_zone')
            if initial_zone is not None and final_zone is not None:
                tsk_summary['zone_transitions'].append({
                    'from': initial_zone,
                    'to': final_zone,
                    'pair_id': pair_id
                })

            # Polyvagal trajectory
            initial_pv = felt_states_tsk.get('initial_polyvagal_state')
            final_pv = felt_states_tsk.get('final_polyvagal_state')
            if initial_pv and final_pv:
                tsk_summary['polyvagal_trajectories'].append({
                    'from': initial_pv,
                    'to': final_pv,
                    'pair_id': pair_id
                })

            # Kairos detection
            if felt_states_tsk.get('kairos_detected', False):
                tsk_summary['kairos_detections'] += 1

            # Organ signature evolution
            tsk_summary['organ_signature_evolution'].append({
                'pair_id': pair_id,
                'initial': felt_states_tsk.get('initial_organ_coherences', {}),
                'final': felt_states_tsk.get('final_organ_coherences', {}),
                'v0_descent': felt_states_tsk.get('initial_v0_energy', 1.0) - felt_states_tsk.get('final_v0_energy', 0.5)
            })

            # Transformation pathways
            tsk_summary['transformation_pathways'].append({
                'pair_id': pair_id,
                'emission_path': felt_states_tsk.get('emission_path', 'unknown'),
                'nexus_count': felt_states_tsk.get('nexus_count', 0),
                'cycles': felt_states_tsk.get('convergence_cycles', 1)
            })

        except Exception as e:
            print(f"   ❌ Error processing {tsk_file.name}: {e}")
            continue

    # Save summary
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(tsk_summary, f, indent=2)

    print(f"\n✅ TSK Summary saved: {output_file}")
    print(f"   Zone transitions: {len(tsk_summary['zone_transitions'])}")
    print(f"   Polyvagal trajectories: {len(tsk_summary['polyvagal_trajectories'])}")
    print(f"   Kairos detections: {tsk_summary['kairos_detections']}")
    print(f"   Organ evolutions: {len(tsk_summary['organ_signature_evolution'])}")
    print(f"   Transformation pathways: {len(tsk_summary['transformation_pathways'])}")

    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 regenerate_tsk_summary.py <epoch_num>")
        sys.exit(1)

    epoch_num = int(sys.argv[1])
    success = regenerate_tsk_summary(epoch_num)
    sys.exit(0 if success else 1)
