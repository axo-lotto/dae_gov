#!/bin/bash
# Monitor entity-situated training progress

echo "🌀 Entity-Situated Training Monitor"
echo "====================================="
echo ""

# Check if training is running
if pgrep -f "run_entity_situated_training.py" > /dev/null; then
    echo "✅ Training process is running"
    echo ""

    # Show last 30 lines of output
    echo "📊 Recent output:"
    echo "----------------"
    # Note: Actual output capture depends on how the training was started
    # This script provides a template for monitoring

    # Check if results file exists
    if [ -f "results/epochs/entity_situated_training_results.json" ]; then
        echo ""
        echo "📈 Training results file found"
        echo "   Analyzing progress..."

        # Extract number of epochs completed
        epochs=$(python3 -c "
import json
try:
    with open('results/epochs/entity_situated_training_results.json', 'r') as f:
        data = json.load(f)
        print(len(data.get('epoch_results', [])))
except:
    print(0)
")
        echo "   Epochs completed: $epochs / 50"
    else
        echo ""
        echo "⏳ Training results file not yet created"
        echo "   Training is likely still in early epochs"
    fi

    # Check entity-organ tracker
    if [ -f "persona_layer/state/active/entity_organ_associations.json" ]; then
        echo ""
        echo "🌀 Entity-organ tracker status:"

        entities=$(python3 -c "
import json
try:
    with open('persona_layer/state/active/entity_organ_associations.json', 'r') as f:
        data = json.load(f)
        metrics = data.get('entity_metrics', {})
        print(f'{len(metrics)} entities tracked')
        for entity, m in list(metrics.items())[:5]:
            mentions = m.get('mention_count', 0)
            print(f'   - {entity}: {mentions} mentions')
except Exception as e:
    print(f'Error: {e}')
")
        echo "   $entities"
    fi

else
    echo "❌ Training process is not running"
    echo ""
    echo "To restart training:"
    echo "  python3 training/conversational/run_entity_situated_training.py"
fi

echo ""
echo "====================================="
