#!/bin/bash
# Fix lure_prototypes.json paths for organs using Path()

echo "Fixing Path()-style lure prototype paths..."

# List of organs using Path()
organs_with_pathlib=(
  "organs/modular/card/core/card_text_core.py"
  "organs/modular/sans/core/sans_text_core.py"
  "organs/modular/rnx/core/rnx_text_core.py"
  "organs/modular/ndam/core/ndam_text_core.py"
  "organs/modular/eo/core/eo_text_core.py"
  "organs/modular/empathy/core/empathy_text_core.py"
  "organs/modular/wisdom/core/wisdom_text_core.py"
  "organs/modular/authenticity/core/authenticity_text_core.py"
  "organs/modular/presence/core/presence_text_core.py"
)

for file in "${organs_with_pathlib[@]}"; do
  if [ -f "$file" ]; then
    sed -i '' "s|'persona_layer' / 'lure_prototypes.json'|'persona_layer' / 'config' / 'lures' / 'lure_prototypes.json'|g" "$file"
    echo "  ✅ Fixed: $file"
  fi
done

echo ""
echo "✅ All Path()-style paths fixed"
echo ""
echo "Verifying all organs now have correct paths..."
grep -r "lure_prototypes.json" organs/modular --include="*_text_core.py" | grep -v "config/lures"
