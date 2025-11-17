#!/bin/bash
# Run Epochs 10-20 Sequentially with TSK Logging
# Created: November 17, 2025 05:20 AM CET

echo "🌀 Starting Epochs 10-20 Training (11 epochs total)"
echo "📊 Estimated time: ~2 hours (10 min/epoch)"
echo "================================"

for epoch in {10..20}; do
  echo ""
  echo "🚀 Starting Epoch $epoch ($(date '+%H:%M:%S'))"

  # Run epoch training
  python3 -u training/entity_memory_epoch_training_with_tsk.py $epoch > /tmp/epoch_${epoch}_with_tsk.log 2>&1

  # Check exit status
  if [ $? -eq 0 ]; then
    echo "✅ Epoch $epoch COMPLETE"

    # Count TSK files created
    tsk_count=$(ls results/tsk_logs/epoch_${epoch}/*.json 2>/dev/null | wc -l)
    echo "   📊 TSK files created: $tsk_count"

    # Check if summary exists
    if [ -f "results/epochs/epoch_${epoch}/tsk_summary.json" ]; then
      echo "   ✅ TSK summary created"
    else
      echo "   ⚠️  TSK summary missing - may need regeneration"
    fi
  else
    echo "❌ Epoch $epoch FAILED (exit code $?)"
    echo "   Check log: /tmp/epoch_${epoch}_with_tsk.log"
    exit 1
  fi
done

echo ""
echo "================================"
echo "🎉 ALL EPOCHS COMPLETE (10-20)"
echo "📊 Total TSK files created: $(ls results/tsk_logs/epoch_*/**.json 2>/dev/null | wc -l)"
echo "💾 Total storage: $(du -sh results/tsk_logs/ | cut -f1)"
echo "⏱️  Finished at: $(date '+%Y-%m-%d %H:%M:%S')"
