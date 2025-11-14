#!/bin/bash
# Monitor friendly companion training progress

LOG_FILE="/tmp/friendly_companion_training.log"

echo "=== Training Progress Monitor ==="
echo ""

# Check if training is running
if ps -p 84323 > /dev/null 2>&1; then
    echo "✅ Training process running (PID: 84323)"
else
    echo "⚠️  Training process not found (may have completed)"
fi

echo ""
echo "=== Recent Progress ==="
tail -50 "$LOG_FILE" 2>/dev/null || echo "Log not available yet"

echo ""
echo "=== Epoch Summary ==="
grep -E "EPOCH [0-9]+ TRAINING|Mean confidence|Mean nexuses|Mean V0|COMPLETE" "$LOG_FILE" 2>/dev/null || echo "No epoch data yet"
