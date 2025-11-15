#!/bin/bash
# Fix organic_families.json path in all persona_layer modules

echo "Fixing organic_families.json paths..."

# Fix in memory_retrieval.py
sed -i '' 's|"persona_layer/organic_families.json"|"persona_layer/state/active/organic_families.json"|g' persona_layer/memory_retrieval.py

# Fix in conversational_organism_wrapper.py
sed -i '' 's|Path("persona_layer/organic_families.json")|Path("persona_layer/state/active/organic_families.json")|g' persona_layer/conversational_organism_wrapper.py

# Fix in organic_conversational_families.py
sed -i '' "s|'persona_layer/organic_families.json'|'persona_layer/state/active/organic_families.json'|g" persona_layer/organic_conversational_families.py

echo "✅ organic_families.json path fixes applied"

# Verify the changes
echo ""
echo "Verifying new paths..."
grep -n "organic_families.json" persona_layer/memory_retrieval.py persona_layer/conversational_organism_wrapper.py persona_layer/organic_conversational_families.py
