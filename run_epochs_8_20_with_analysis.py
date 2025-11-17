#!/usr/bin/env python3
"""
Run Epochs 8-20 with corrected metrics and mathematical correlation analysis.
Created: November 16, 2025
"""

import sys
import os
import subprocess
import time
import json
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple

# Set PYTHONPATH
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

# Force unbuffered output
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)

print("="*80, flush=True)
print("🌀 EPOCHS 8-20 TRAINING WITH MATHEMATICAL CORRELATION ANALYSIS", flush=True)
print("="*80, flush=True)

# Configuration
EPOCHS_TO_RUN = list(range(8, 21))  # 8-20 inclusive
TRAINING_SCRIPT = "training/entity_memory_epoch_training.py"
RESULTS_DIR = "results/epochs"
ANALYSIS_OUTPUT = "results/epochs/epochs_8_20_correlation_analysis.json"

# Ensure results directory exists
os.makedirs(RESULTS_DIR, exist_ok=True)

# Storage for all epoch results
all_epochs_data = []

print(f"\n📊 Running {len(EPOCHS_TO_RUN)} epochs (8-20)...")
print(f"   Training script: {TRAINING_SCRIPT}")
print(f"   Results directory: {RESULTS_DIR}")
print(f"   Analysis output: {ANALYSIS_OUTPUT}\n")

# Run each epoch
for epoch_num in EPOCHS_TO_RUN:
    print(f"\n{'='*80}", flush=True)
    print(f"🌀 EPOCH {epoch_num}", flush=True)
    print(f"{'='*80}", flush=True)

    log_file = f"/tmp/entity_memory_epoch_{epoch_num}.log"
    result_file = f"{RESULTS_DIR}/entity_memory_epoch_1_results.json"  # ✅ FIX (Nov 17): Always use epoch 1 results (training script always writes there)

    print(f"   Log: {log_file}", flush=True)
    print(f"   Running training...", flush=True)

    start_time = time.time()

    # Run training
    result = subprocess.run(
        ["python3", TRAINING_SCRIPT],
        capture_output=True,
        text=True
    )

    elapsed_time = time.time() - start_time

    if result.returncode != 0:
        print(f"   ❌ ERROR in Epoch {epoch_num}:")
        print(result.stderr[:500])
        continue

    print(f"   ✅ Complete ({elapsed_time:.1f}s)")

    # Load results and save epoch-specific copy
    if os.path.exists(result_file):
        with open(result_file, 'r') as f:
            epoch_data = json.load(f)
            epoch_data['epoch_num'] = epoch_num
            epoch_data['elapsed_time'] = elapsed_time
            all_epochs_data.append(epoch_data)

        # Save epoch-specific copy for record-keeping
        epoch_specific_file = f"{RESULTS_DIR}/entity_memory_epoch_{epoch_num}_results.json"
        with open(epoch_specific_file, 'w') as f:
            json.dump(epoch_data, f, indent=2)

        # Print quick metrics
        metrics = epoch_data.get('metrics', {})
        entity_recall = metrics.get('entity_recall_accuracy', [])
        nexus_formation = metrics.get('nexus_formation_rate', [])

        if entity_recall:
            print(f"   📊 Entity recall: {np.mean(entity_recall)*100:.1f}% (avg)")
        if nexus_formation:
            print(f"   📊 NEXUS formation: {np.mean(nexus_formation)*100:.1f}% (avg)")
    else:
        print(f"   ⚠️  Results file not found: {result_file}")

print(f"\n{'='*80}")
print("📈 MATHEMATICAL CORRELATION ANALYSIS")
print(f"{'='*80}\n")

if len(all_epochs_data) < 3:
    print("❌ Not enough epochs completed for correlation analysis (need ≥3)")
    sys.exit(1)

# Extract time series data
epochs = []
entity_recall_means = []
entity_memory_available_rates = []
nexus_formation_rates = []
entity_tracker_update_rates = []
emission_correctness_means = []
confidence_means = []
v0_final_means = []
cycles_means = []
processing_time_means = []

for epoch_data in all_epochs_data:
    epoch_num = epoch_data.get('epoch_num', 0)
    metrics = epoch_data.get('metrics', {})

    epochs.append(epoch_num)

    # Entity memory metrics
    entity_recall = metrics.get('entity_recall_accuracy', [])
    entity_recall_means.append(np.mean(entity_recall) if entity_recall else 0.0)

    nexus_formation = metrics.get('nexus_formation_rate', [])
    nexus_formation_rates.append(np.mean(nexus_formation) if nexus_formation else 0.0)

    emission_correctness = metrics.get('emission_correctness', [])
    emission_correctness_means.append(np.mean(emission_correctness) if emission_correctness else 0.0)

    # General metrics
    confidence = metrics.get('confidence_history', [])
    confidence_means.append(np.mean(confidence) if confidence else 0.0)

    v0_final = metrics.get('v0_final_history', [])
    v0_final_means.append(np.mean(v0_final) if v0_final else 0.0)

    cycles = metrics.get('cycle_history', [])
    cycles_means.append(np.mean(cycles) if cycles else 0.0)

    processing_time = metrics.get('processing_time_history', [])
    processing_time_means.append(np.mean(processing_time) if processing_time else 0.0)

# Convert to numpy arrays
epochs = np.array(epochs)
entity_recall_means = np.array(entity_recall_means)
nexus_formation_rates = np.array(nexus_formation_rates)
emission_correctness_means = np.array(emission_correctness_means)
confidence_means = np.array(confidence_means)
v0_final_means = np.array(v0_final_means)
cycles_means = np.array(cycles_means)
processing_time_means = np.array(processing_time_means)

print("📊 Time Series Summary:")
print(f"   Epochs analyzed: {len(epochs)}")
print(f"   Range: Epoch {epochs[0]} to Epoch {epochs[-1]}\n")

# 1. ENTITY RECALL ACCURACY TRENDS
print("1️⃣  ENTITY RECALL ACCURACY ANALYSIS")
print("   " + "-"*70)

if np.std(entity_recall_means) > 0.001:  # Non-zero variance
    # Linear trend
    slope, intercept, r_value, p_value, std_err = stats.linregress(epochs, entity_recall_means)
    print(f"   Linear Trend:")
    print(f"      Slope: {slope:.6f} (change per epoch)")
    print(f"      R²: {r_value**2:.4f}")
    print(f"      p-value: {p_value:.4f} {'✅ Significant' if p_value < 0.05 else '❌ Not significant'}")
    print(f"      Predicted Epoch 20: {slope * 20 + intercept:.4f}")

    # Mean and variance
    print(f"   Statistics:")
    print(f"      Mean: {np.mean(entity_recall_means):.4f}")
    print(f"      Std Dev: {np.std(entity_recall_means):.4f}")
    print(f"      Min: {np.min(entity_recall_means):.4f} (Epoch {epochs[np.argmin(entity_recall_means)]})")
    print(f"      Max: {np.max(entity_recall_means):.4f} (Epoch {epochs[np.argmax(entity_recall_means)]})")
else:
    print(f"   No variance detected (all values ≈ {entity_recall_means[0]:.4f})")

print()

# 2. NEXUS FORMATION TRENDS
print("2️⃣  NEXUS DIFFERENTIATION ANALYSIS")
print("   " + "-"*70)

if np.std(nexus_formation_rates) > 0.001:
    slope, intercept, r_value, p_value, std_err = stats.linregress(epochs, nexus_formation_rates)
    print(f"   Linear Trend:")
    print(f"      Slope: {slope:.6f} (change per epoch)")
    print(f"      R²: {r_value**2:.4f}")
    print(f"      p-value: {p_value:.4f} {'✅ Significant' if p_value < 0.05 else '❌ Not significant'}")
    print(f"      Predicted Epoch 20: {slope * 20 + intercept:.4f}")

    print(f"   Statistics:")
    print(f"      Mean: {np.mean(nexus_formation_rates):.4f}")
    print(f"      Std Dev: {np.std(nexus_formation_rates):.4f}")
    print(f"      Min: {np.min(nexus_formation_rates):.4f} (Epoch {epochs[np.argmin(nexus_formation_rates)]})")
    print(f"      Max: {np.max(nexus_formation_rates):.4f} (Epoch {epochs[np.argmax(nexus_formation_rates)]})")
else:
    print(f"   No variance detected (all values ≈ {nexus_formation_rates[0]:.4f})")

print()

# 3. CORRELATIONS BETWEEN ENTITY METRICS AND GENERAL METRICS
print("3️⃣  CROSS-METRIC CORRELATIONS")
print("   " + "-"*70)

correlations = []

# Entity recall vs Confidence
if np.std(entity_recall_means) > 0.001 and np.std(confidence_means) > 0.001:
    corr, p_val = stats.pearsonr(entity_recall_means, confidence_means)
    correlations.append(("Entity Recall vs Confidence", corr, p_val))
    print(f"   Entity Recall ↔ Confidence:")
    print(f"      Correlation: {corr:.4f} {'✅ Significant' if p_val < 0.05 else '❌ Not significant'}")
    print(f"      p-value: {p_val:.4f}")

# Entity recall vs V0 final
if np.std(entity_recall_means) > 0.001 and np.std(v0_final_means) > 0.001:
    corr, p_val = stats.pearsonr(entity_recall_means, v0_final_means)
    correlations.append(("Entity Recall vs V0 Final", corr, p_val))
    print(f"   Entity Recall ↔ V0 Final:")
    print(f"      Correlation: {corr:.4f} {'✅ Significant' if p_val < 0.05 else '❌ Not significant'}")
    print(f"      p-value: {p_val:.4f}")

# NEXUS formation vs Cycles
if np.std(nexus_formation_rates) > 0.001 and np.std(cycles_means) > 0.001:
    corr, p_val = stats.pearsonr(nexus_formation_rates, cycles_means)
    correlations.append(("NEXUS Formation vs Cycles", corr, p_val))
    print(f"   NEXUS Formation ↔ Convergence Cycles:")
    print(f"      Correlation: {corr:.4f} {'✅ Significant' if p_val < 0.05 else '❌ Not significant'}")
    print(f"      p-value: {p_val:.4f}")

# Entity recall vs Emission correctness
if np.std(entity_recall_means) > 0.001 and np.std(emission_correctness_means) > 0.001:
    corr, p_val = stats.pearsonr(entity_recall_means, emission_correctness_means)
    correlations.append(("Entity Recall vs Emission Correctness", corr, p_val))
    print(f"   Entity Recall ↔ Emission Correctness:")
    print(f"      Correlation: {corr:.4f} {'✅ Significant' if p_val < 0.05 else '❌ Not significant'}")
    print(f"      p-value: {p_val:.4f}")

print()

# 4. LEARNING VELOCITY ANALYSIS
print("4️⃣  LEARNING VELOCITY (Rate of Change)")
print("   " + "-"*70)

if len(epochs) >= 5:
    # Compute rolling derivatives (velocity)
    entity_recall_velocity = np.diff(entity_recall_means)
    nexus_formation_velocity = np.diff(nexus_formation_rates)

    print(f"   Entity Recall Velocity:")
    print(f"      Mean change per epoch: {np.mean(entity_recall_velocity):.6f}")
    print(f"      Acceleration (2nd derivative): {np.mean(np.diff(entity_recall_velocity)):.6f}")

    print(f"   NEXUS Formation Velocity:")
    print(f"      Mean change per epoch: {np.mean(nexus_formation_velocity):.6f}")
    print(f"      Acceleration (2nd derivative): {np.mean(np.diff(nexus_formation_velocity)):.6f}")
else:
    print("   Not enough epochs for velocity analysis (need ≥5)")

print()

# 5. SAVE ANALYSIS RESULTS
analysis_results = {
    "epochs_analyzed": epochs.tolist(),
    "time_series": {
        "entity_recall_means": entity_recall_means.tolist(),
        "nexus_formation_rates": nexus_formation_rates.tolist(),
        "emission_correctness_means": emission_correctness_means.tolist(),
        "confidence_means": confidence_means.tolist(),
        "v0_final_means": v0_final_means.tolist(),
        "cycles_means": cycles_means.tolist(),
        "processing_time_means": processing_time_means.tolist()
    },
    "linear_trends": {},
    "correlations": {},
    "learning_velocity": {}
}

# Add linear trends if variance exists
if np.std(entity_recall_means) > 0.001:
    slope, intercept, r_value, p_value, std_err = stats.linregress(epochs, entity_recall_means)
    analysis_results["linear_trends"]["entity_recall"] = {
        "slope": float(slope),
        "intercept": float(intercept),
        "r_squared": float(r_value**2),
        "p_value": float(p_value),
        "predicted_epoch_20": float(slope * 20 + intercept)
    }

if np.std(nexus_formation_rates) > 0.001:
    slope, intercept, r_value, p_value, std_err = stats.linregress(epochs, nexus_formation_rates)
    analysis_results["linear_trends"]["nexus_formation"] = {
        "slope": float(slope),
        "intercept": float(intercept),
        "r_squared": float(r_value**2),
        "p_value": float(p_value),
        "predicted_epoch_20": float(slope * 20 + intercept)
    }

# Add correlations
for name, corr, p_val in correlations:
    analysis_results["correlations"][name] = {
        "correlation": float(corr),
        "p_value": float(p_val),
        "significant": bool(p_val < 0.05)
    }

# Add velocity if enough data
if len(epochs) >= 5:
    analysis_results["learning_velocity"]["entity_recall"] = {
        "mean_velocity": float(np.mean(entity_recall_velocity)),
        "acceleration": float(np.mean(np.diff(entity_recall_velocity)))
    }
    analysis_results["learning_velocity"]["nexus_formation"] = {
        "mean_velocity": float(np.mean(nexus_formation_velocity)),
        "acceleration": float(np.mean(np.diff(nexus_formation_velocity)))
    }

# Save to JSON
with open(ANALYSIS_OUTPUT, 'w') as f:
    json.dump(analysis_results, f, indent=2)

print(f"💾 Analysis saved to: {ANALYSIS_OUTPUT}")

print(f"\n{'='*80}")
print("✅ EPOCHS 8-20 TRAINING & ANALYSIS COMPLETE")
print(f"{'='*80}\n")

print("📊 Summary:")
print(f"   Epochs completed: {len(all_epochs_data)}/{len(EPOCHS_TO_RUN)}")
print(f"   Analysis output: {ANALYSIS_OUTPUT}")
print(f"   Entity recall trend: {'Improving' if np.std(entity_recall_means) > 0.001 and np.mean(entity_recall_velocity) > 0 else 'Stable'}")
print(f"   NEXUS formation trend: {'Improving' if np.std(nexus_formation_rates) > 0.001 and np.mean(nexus_formation_velocity) > 0 else 'Stable'}")
