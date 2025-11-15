#!/bin/bash
# Fix lure_prototypes.json paths in all organs

echo "Fixing lure_prototypes.json paths in all organs..."

# Update the path from persona_layer/lure_prototypes.json to persona_layer/config/lures/lure_prototypes.json
find organs/modular -name "*_text_core.py" -type f -exec sed -i '' \
  "s|'persona_layer', 'lure_prototypes.json'|'persona_layer', 'config', 'lures', 'lure_prototypes.json'|g" {} \;

echo "✅ Lure prototype path fixes applied"

# Verify the changes
echo ""
echo "Verifying new paths..."
grep -r "lure_prototypes.json" organs/modular --include="*_text_core.py" | head -5
