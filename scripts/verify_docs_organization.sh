#!/bin/bash
# DAE_HYPHAE_1 Documentation Verification Script
# Date: November 12, 2025
# Verifies documentation reorganization completed successfully

set -e

BASE_DIR="/Users/daedalea/Desktop/DAE_HYPHAE_1"
cd "$BASE_DIR"

echo "======================================"
echo "DOCUMENTATION VERIFICATION"
echo "======================================"
echo ""

# Expected counts
EXPECTED_ARCHITECTURE=18
EXPECTED_PHASES=22
EXPECTED_IMPLEMENTATION=15
EXPECTED_ANALYSIS=19
EXPECTED_ROADMAPS=12
EXPECTED_ARCHIVE=20
EXPECTED_ROOT=8

# Actual counts
ACTUAL_ARCHITECTURE=$(ls -1 docs/architecture/*.md 2>/dev/null | wc -l)
ACTUAL_PHASES=$(ls -1 docs/phases/*.md 2>/dev/null | wc -l)
ACTUAL_IMPLEMENTATION=$(ls -1 docs/implementation/*.md 2>/dev/null | wc -l)
ACTUAL_ANALYSIS=$(ls -1 docs/analysis/*.md 2>/dev/null | wc -l)
ACTUAL_ROADMAPS=$(ls -1 docs/roadmaps/*.md 2>/dev/null | wc -l)
ACTUAL_ARCHIVE=$(ls -1 docs/archive/*.md 2>/dev/null | wc -l)
ACTUAL_ROOT=$(ls -1 *.md 2>/dev/null | wc -l)

echo "📊 File Counts:"
echo ""
echo "  Architecture:     $ACTUAL_ARCHITECTURE / $EXPECTED_ARCHITECTURE expected"
echo "  Phases:           $ACTUAL_PHASES / $EXPECTED_PHASES expected"
echo "  Implementation:   $ACTUAL_IMPLEMENTATION / $EXPECTED_IMPLEMENTATION expected"
echo "  Analysis:         $ACTUAL_ANALYSIS / $EXPECTED_ANALYSIS expected"
echo "  Roadmaps:         $ACTUAL_ROADMAPS / $EXPECTED_ROADMAPS expected"
echo "  Archive:          $ACTUAL_ARCHIVE / $EXPECTED_ARCHIVE expected"
echo "  Root (kept):      $ACTUAL_ROOT / $EXPECTED_ROOT expected"
echo ""

# Check for success
TOTAL_EXPECTED=114
TOTAL_MOVED=106
TOTAL_ACTUAL=$((ACTUAL_ARCHITECTURE + ACTUAL_PHASES + ACTUAL_IMPLEMENTATION + ACTUAL_ANALYSIS + ACTUAL_ROADMAPS + ACTUAL_ARCHIVE + ACTUAL_ROOT))

echo "📈 Total Files: $TOTAL_ACTUAL / $TOTAL_EXPECTED expected"
echo ""

# Essential files in root check
echo "✅ Essential Files in Root:"
for file in CLAUDE.md README.md QUICK_REFERENCE.md REORGANIZATION_COMPLETE_NOV12_2025.md; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (MISSING)"
    fi
done
echo ""

# Verify directories exist
echo "📁 Directory Structure:"
for dir in docs/architecture docs/phases docs/implementation docs/analysis docs/roadmaps docs/archive; do
    if [ -d "$dir" ]; then
        echo "  ✅ $dir"
    else
        echo "  ❌ $dir (MISSING)"
    fi
done
echo ""

# Check if any old files remain in root that shouldn't
echo "⚠️  Potential Stragglers in Root:"
STRAGGLERS=$(ls -1 *.md 2>/dev/null | grep -vE "^(CLAUDE|README|QUICK_REFERENCE|REORGANIZATION_COMPLETE_NOV12_2025|CHANGELOG|CONTRIBUTING|STATUS|LICENSE)" || true)
if [ -z "$STRAGGLERS" ]; then
    echo "  ✅ No unexpected files in root"
else
    echo "$STRAGGLERS" | while read file; do
        echo "  ⚠️  $file (should this be in docs/?)"
    done
fi
echo ""

# Overall status
echo "======================================"
if [ $TOTAL_ACTUAL -eq $TOTAL_EXPECTED ]; then
    echo "✅ VERIFICATION PASSED"
    echo "All files accounted for!"
else
    echo "⚠️  VERIFICATION INCOMPLETE"
    echo "Expected $TOTAL_EXPECTED files, found $TOTAL_ACTUAL"
fi
echo "======================================"
echo ""
