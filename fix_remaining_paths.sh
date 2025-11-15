#!/bin/bash
# Fix all remaining hardcoded paths in persona_layer

echo "Fixing remaining hardcoded paths..."

# Fix hebbian memory paths (state/active/)
find persona_layer -name "*.py" -type f -exec sed -i '' \
  's|"persona_layer/conversational_hebbian_memory.json"|"persona_layer/state/active/conversational_hebbian_memory.json"|g' {} \;

find persona_layer -name "*.py" -type f -exec sed -i '' \
  's|Path("persona_layer/conversational_hebbian_memory.json")|Path("persona_layer/state/active/conversational_hebbian_memory.json")|g' {} \;

# Fix transduction phrase paths (config/transduction/)
find persona_layer -name "*.py" -type f -exec sed -i '' \
  's|"persona_layer/transduction_mechanism_phrases.json"|"persona_layer/config/transduction/transduction_mechanism_phrases.json"|g' {} \;

find persona_layer -name "*.py" -type f -exec sed -i '' \
  's|"persona_layer/transduction_mechanism_phrases_with_lure_tags.json"|"persona_layer/config/transduction/transduction_mechanism_phrases_with_lure_tags.json"|g' {} \;

echo "✅ Path fixes applied"
