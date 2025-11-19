#!/bin/bash
# Adaptive Documentation Organization Script
# Uses existing docs/ structure + adds missing categories
# Date: November 19, 2025

set -e

ROOT="/Users/daedalea/Desktop/DAE_HYPHAE_1"
cd "$ROOT"

echo "🗂️  Adaptive Documentation Organization"
echo "   Using existing docs/ structure..."
echo ""

# Create missing subdirectories within existing categories
mkdir -p docs/architecture/{core,learning,entity}
mkdir -p docs/analysis/{assessments,diagnostics,investigations}
mkdir -p docs/phases/{phase1,phase2,phase3,weekly_updates}
mkdir -p docs/training/{epochs,validation,strategies}
mkdir -p docs/roadmaps/{strategic,llm_independence}
mkdir -p docs/sessions/{2025-11-15,2025-11-16,2025-11-17,2025-11-18,2025-11-19}

# Use existing: enhancements/, implementation/, interactive_logs/, misc/, archive/

echo "📁 Moving files by category..."
echo ""

# ===== ARCHITECTURE FILES =====
echo "  → Architecture (core systems)..."
mv NEXUS_*.md docs/architecture/core/ 2>/dev/null || true
mv DUAL_MEMORY_*.md docs/architecture/core/ 2>/dev/null || true
mv TRANSDUCTIVE_*.md docs/architecture/core/ 2>/dev/null || true
mv *_12_ORGAN_*.md docs/architecture/core/ 2>/dev/null || true

echo "  → Architecture (learning systems)..."
mv TSK_*.md RNX_*.md 57D_RNX_*.md docs/architecture/learning/ 2>/dev/null || true
mv *_FRACTAL_*.md COMPLETE_FRACTAL_*.md docs/architecture/learning/ 2>/dev/null || true
mv LEARNING_*.md *_LEARNING_*.md docs/architecture/learning/ 2>/dev/null || true

echo "  → Architecture (entity systems)..."
mv ENTITY_NEIGHBOR_*.md docs/architecture/entity/ 2>/dev/null || true
mv ENTITY_EXTRACTION_*.md docs/architecture/entity/ 2>/dev/null || true
mv ENTITY_MEMORY_*.md docs/architecture/entity/ 2>/dev/null || true
mv ENTITY_INTERFACE_*.md docs/architecture/entity/ 2>/dev/null || true
mv ENTITY_CONTINUITY_*.md docs/architecture/entity/ 2>/dev/null || true
mv ENTITY_STORAGE_*.md docs/architecture/entity/ 2>/dev/null || true

# ===== ANALYSIS FILES =====
echo "  → Analysis (assessments)..."
mv *_ASSESSMENT_*.md docs/analysis/assessments/ 2>/dev/null || true
mv *_AUDIT_*.md docs/analysis/assessments/ 2>/dev/null || true
mv ARCHITECTURAL_ASSESSMENT_*.md docs/analysis/assessments/ 2>/dev/null || true
mv DAE3_*.md DAE_*.md docs/analysis/assessments/ 2>/dev/null || true

echo "  → Analysis (diagnostics)..."
mv *_DIAGNOSIS_*.md docs/analysis/diagnostics/ 2>/dev/null || true
mv *_ROOT_CAUSE_*.md docs/analysis/diagnostics/ 2>/dev/null || true
mv DIAGNOSTIC_*.md docs/analysis/diagnostics/ 2>/dev/null || true
mv CRISIS_*.md docs/analysis/diagnostics/ 2>/dev/null || true

echo "  → Analysis (investigations)..."
mv *_ANALYSIS_*.md docs/analysis/investigations/ 2>/dev/null || true
mv ANALYSIS_*.md docs/analysis/investigations/ 2>/dev/null || true
mv *_INVESTIGATION_*.md docs/analysis/investigations/ 2>/dev/null || true

# ===== PHASE FILES =====
echo "  → Phases..."
mv PHASE1_*.md docs/phases/phase1/ 2>/dev/null || true
mv PHASE2_*.md docs/phases/phase2/ 2>/dev/null || true
mv PHASE3_*.md PHASE3B_*.md docs/phases/phase3/ 2>/dev/null || true
mv WEEK*_*.md docs/phases/weekly_updates/ 2>/dev/null || true

# ===== TRAINING FILES =====
echo "  → Training (epochs)..."
mv EPOCH_*.md *_EPOCH*_*.md docs/training/epochs/ 2>/dev/null || true
mv WAVE_TRAINING_*.md docs/training/epochs/ 2>/dev/null || true

echo "  → Training (validation)..."
mv *_VALIDATION_*.md docs/training/validation/ 2>/dev/null || true
mv *_TESTING_*.md docs/training/validation/ 2>/dev/null || true
mv *_VERIFIED_*.md docs/training/validation/ 2>/dev/null || true

echo "  → Training (strategies)..."
mv TRAINING_*.md *_TRAINING_*.md docs/training/strategies/ 2>/dev/null || true
mv COMPREHENSIVE_TRAINING_*.md docs/training/strategies/ 2>/dev/null || true
mv *_TRAINING_CONFIG_*.md docs/training/strategies/ 2>/dev/null || true

# ===== SESSION FILES =====
echo "  → Sessions..."
mv SESSION_NOV15_*.md docs/sessions/2025-11-15/ 2>/dev/null || true
mv SESSION_NOV16_*.md docs/sessions/2025-11-16/ 2>/dev/null || true
mv SESSION_NOV17_*.md docs/sessions/2025-11-17/ 2>/dev/null || true
mv SESSION_NOV18_*.md docs/sessions/2025-11-18/ 2>/dev/null || true
mv SESSION_NOV19_*.md docs/sessions/2025-11-19/ 2>/dev/null || true
mv SESSION_SUMMARY_*.md docs/sessions/ 2>/dev/null || true

# ===== ROADMAP FILES =====
echo "  → Roadmaps (strategic)..."
mv STRATEGIC_*.md docs/roadmaps/strategic/ 2>/dev/null || true
mv *_ROADMAP_*.md docs/roadmaps/strategic/ 2>/dev/null || true
mv COMPREHENSIVE_LEARNING_CORPUS_*.md docs/roadmaps/strategic/ 2>/dev/null || true
mv COMPREHENSIVE_MEMORY_*.md docs/roadmaps/strategic/ 2>/dev/null || true
mv COMPANION_INTELLIGENCE_*.md docs/roadmaps/strategic/ 2>/dev/null || true

echo "  → Roadmaps (LLM independence)..."
mv LLM_DEPENDENCY_*.md docs/roadmaps/llm_independence/ 2>/dev/null || true
mv LLM_FREE_*.md docs/roadmaps/llm_independence/ 2>/dev/null || true
mv LLM_BRIDGE_*.md docs/roadmaps/llm_independence/ 2>/dev/null || true
mv UNIFIED_LLM_*.md docs/roadmaps/llm_independence/ 2>/dev/null || true

# ===== IMPLEMENTATION FILES (use existing docs/implementation/) =====
echo "  → Implementation..."
mv *_IMPLEMENTATION_*.md docs/implementation/ 2>/dev/null || true
mv *_COMPLETE_*.md docs/implementation/ 2>/dev/null || true
mv *_INTEGRATION_*.md docs/implementation/ 2>/dev/null || true

# ===== ENHANCEMENTS (use existing docs/enhancements/) =====
echo "  → Enhancements..."
mv *_ENHANCEMENT_*.md docs/enhancements/ 2>/dev/null || true
mv ADDENDUM_*.md docs/enhancements/ 2>/dev/null || true

# ===== PROPOSALS & QUICK FIXES =====
echo "  → Proposals & Quick Fixes..."
mv *_PROPOSAL_*.md docs/misc/ 2>/dev/null || true
mv *_PLAN_*.md docs/misc/ 2>/dev/null || true
mv QUICK_*.md docs/misc/ 2>/dev/null || true
mv FIX_*.md EMERGENCY_*.md BREAKTHROUGH_*.md docs/misc/ 2>/dev/null || true

# ===== GUIDES & REFERENCES =====
echo "  → Guides & References..."
mv *_GUIDE*.md docs/misc/ 2>/dev/null || true
mv *_REFERENCE*.md docs/misc/ 2>/dev/null || true

# ===== REMAINING FILES → archive =====
echo "  → Archiving remaining files..."
mv *.md docs/archive/ 2>/dev/null || true

# ===== RESTORE ESSENTIAL FILES TO ROOT =====
echo "  → Restoring essential files to root..."
mv docs/archive/CLAUDE.md . 2>/dev/null || true
mv docs/archive/README.md . 2>/dev/null || true
mv docs/archive/DEVELOPMENT_GUIDE.md . 2>/dev/null || true
mv docs/archive/COMPREHENSIVE_PROJECT_ORGANIZATION_PROPOSAL_NOV19_2025.md . 2>/dev/null || true

echo ""
echo "✅ Documentation organized!"
echo ""
echo "📊 Summary:"
echo "   Root .md files remaining: $(ls -1 *.md 2>/dev/null | wc -l | tr -d ' ')"
echo "   Files in docs/: $(find docs -name '*.md' | wc -l | tr -d ' ')"
echo ""
echo "📋 Review these directories for any mis-categorized files:"
echo "   - docs/misc/ (catch-all for miscellaneous)"
echo "   - docs/archive/ (files that didn't match patterns)"
echo ""
