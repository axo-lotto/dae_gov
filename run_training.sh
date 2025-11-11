#!/bin/bash
# Quick start training script for DAE_HYPHAE_1

set -e

echo "🌀 DAE HYPHAE_0 Training"
echo "========================"

# Set PYTHONPATH
export PYTHONPATH="/Users/daedalea/Desktop/DAE_HYPHAE_1:$PYTHONPATH"

# Run training
echo "Starting Epoch 1: ARC 1.0 (400 tasks)"
python3 training/train_arc1.py

echo ""
echo "✅ Training complete. Check data/organism_state.json for results."
