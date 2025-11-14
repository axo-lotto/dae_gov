#!/bin/bash
# DAE_HYPHAE_1 Markdown Reorganization Script
# Date: November 12, 2025
# Organizes 106 .md files from root into docs/ subdirectories

set -e  # Exit on error

BASE_DIR="/Users/daedalea/Desktop/DAE_HYPHAE_1"
cd "$BASE_DIR"

echo "======================================"
echo "DAE_HYPHAE_1 DOCUMENTATION REORGANIZATION"
echo "======================================"
echo ""
echo "This will move 106 .md files into organized docs/ structure"
echo "Backup recommended before proceeding!"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 1
fi

echo ""
echo "Starting reorganization..."
echo ""

# ====================================
# ARCHITECTURE (18 files)
# ====================================
echo "[1/6] Moving architecture docs..."

mv "DAE_HYPHAE_1_EMISSION_ARCHITECTURE.md" "docs/architecture/" 2>/dev/null || echo "  ⚠️  DAE_HYPHAE_1_EMISSION_ARCHITECTURE.md not found"
mv "BACKPROPAGATION_SELF_FEEDING_LOOP_ARCHITECTURE.md" "docs/architecture/" 2>/dev/null || true
mv "TEXT_NATIVE_ARCHITECTURE_ADDENDUM.md" "docs/architecture/" 2>/dev/null || true
mv "DAE_GOV_KNOWLEDGE_ARCHITECTURE_NOV7_2025.md" "docs/architecture/" 2>/dev/null || true
mv "DAE_GOV_PERSONA_LAYER_ARCHITECTURE_ADDENDUM.md" "docs/architecture/" 2>/dev/null || true
mv "TSK_CONVERSATIONAL_EPOCH_ARCHITECTURE_NOV11_2025.md" "docs/architecture/" 2>/dev/null || true
mv "MULTI_TIER_MEMORY_ARCHITECTURE.md" "docs/architecture/" 2>/dev/null || true
mv "COMMUNICATION_PROTOCOLS.md" "docs/architecture/" 2>/dev/null || true
mv "14_NEXUS_DESIGN.md" "docs/architecture/" 2>/dev/null || true
mv "EMISSION_DUAL_PATH_INTEGRATION_REFINED.md" "docs/architecture/" 2>/dev/null || true
mv "EMISSION_11_ORGAN_INTEGRATION_PLAN.md" "docs/architecture/" 2>/dev/null || true
mv "MYCELIUM_FELT_INTEGRATION_README.md" "docs/architecture/" 2>/dev/null || true
mv "MYCELIUM_TRACES_README.md" "docs/architecture/" 2>/dev/null || true
mv "TRANSDUCTIVE_NEXUS_INTEGRATION_ADDENDUM_NOV12_2025.md" "docs/architecture/" 2>/dev/null || true
mv "SELF_MATRIX.MD" "docs/architecture/" 2>/dev/null || true
mv "SELF_MATRIX_EMISSION_GOVERNANCE_NOV12_2025.md" "docs/architecture/" 2>/dev/null || true
mv "VECTOR_SIGNATURE_INTEGRATION_STRATEGY.md" "docs/architecture/" 2>/dev/null || true
mv "SAFETY_ALIGNMENT_POLICY.md" "docs/architecture/" 2>/dev/null || true

echo "  ✅ Architecture docs moved"

# ====================================
# PHASES (22 files)
# ====================================
echo "[2/6] Moving phase reports..."

mv "PHASE_1_COMPLETE_PROGRESS_NOV11_2025.md" "docs/phases/" 2>/dev/null || true
mv "PHASE_1_IMPLEMENTATION_STATUS.md" "docs/phases/" 2>/dev/null || true
mv "PHASE_1_FIXES_COMPLETE_NOV12_2025.md" "docs/phases/" 2>/dev/null || true
mv "PHASE_2_FELT_AFFORDANCES_DESIGN.md" "docs/phases/" 2>/dev/null || true
mv "PHASE_2_QUICK_START.md" "docs/phases/" 2>/dev/null || true
mv "PHASE_2_ARCHITECTURE_CONFLICT_ANALYSIS.md" "docs/phases/" 2>/dev/null || true
mv "PHASE_2_IMPLEMENTATION_SESSION1_NOV11_2025.md" "docs/phases/" 2>/dev/null || true
mv "PHASE_2_SESSION2_COMPLETE_NOV11_2025.md" "docs/phases/" 2>/dev/null || true
mv "PHASE_2_SESSION3_11_ORGAN_COMPLETE_NOV11_2025.md" "docs/phases/" 2>/dev/null || true
mv "PHASE_2_COMPLETE_ASSESSMENT_NOV11_2025.md" "docs/phases/" 2>/dev/null || true
mv "PHASE_2_COMPREHENSIVE_TEST_RESULTS.md" "docs/phases/" 2>/dev/null || true
mv "PHASE_5_INTEGRATION_COMPLETE_NOV11_2025.md" "docs/phases/" 2>/dev/null || true
mv "PHASE_5_ORGANIC_LEARNING_IMPLEMENTATION_SUMMARY.md" "docs/phases/" 2>/dev/null || true
mv "EMISSION_PIPELINE_COMPLETE_NOV11_2025.md" "docs/phases/" 2>/dev/null || true
mv "EMISSION_ARCHITECTURE_SESSION_NOV11_2025.md" "docs/phases/" 2>/dev/null || true
mv "SELF_FEEDING_LOOP_PHASE_1_COMPLETE.md" "docs/phases/" 2>/dev/null || true
mv "HEALTH_MONITORING_SYSTEM_COMPLETE_NOV11_2025.md" "docs/phases/" 2>/dev/null || true
mv "CONVERSATIONAL_EPOCH_IMPLEMENTATION_PROGRESS_NOV11_2025.md" "docs/phases/" 2>/dev/null || true
mv "TRANSDUCTIVE_INTEGRATION_COMPLETE_NOV12_2025.md" "docs/phases/" 2>/dev/null || true
mv "TRANSDUCTIVE_NEXUS_COMPLETE_NOV12_2025.md" "docs/phases/" 2>/dev/null || true
mv "IMPLEMENTATION_SUMMARY_NOV11_2025.md" "docs/phases/" 2>/dev/null || true
mv "EPOCH_1_PHASE1_FIXES_COMPARISON_NOV12_2025.md" "docs/phases/" 2>/dev/null || true

echo "  ✅ Phase reports moved"

# ====================================
# IMPLEMENTATION (15 files)
# ====================================
echo "[3/6] Moving implementation guides..."

mv "OPTION_A_ENTITY_NATIVE_REDESIGN_ROADMAP.md" "docs/implementation/" 2>/dev/null || true
mv "CONVERSATIONAL_GRAMMAR_LEARNING_V2_ORGANIC_NOV11_2025.md" "docs/implementation/" 2>/dev/null || true
mv "CONVERSATIONAL_EPOCH_TRAINING_READINESS_NOV11_2025.md" "docs/implementation/" 2>/dev/null || true
mv "CONVERSATIONAL_ORGAN_INTEGRATION_STRATEGY_NOV11_2025.md" "docs/implementation/" 2>/dev/null || true
mv "DAE_GOV_CONVERSATIONAL_EPOCH_TRAINING_DESIGN.md" "docs/implementation/" 2>/dev/null || true
mv "THERAPEUTIC_EPOCH_LEARNING_STRATEGY.md" "docs/implementation/" 2>/dev/null || true
mv "POETIC_SPONTANEITY_EPOCH_LEARNING_ADDENDUM.md" "docs/implementation/" 2>/dev/null || true
mv "CONVERSATIONAL_GRAMMAR_LEARNING_PROPOSAL_NOV11_2025.md" "docs/implementation/" 2>/dev/null || true
mv "ORGAN_INTEGRATION_ADDENDUM_45D_FELT_NOV11_2025.md" "docs/implementation/" 2>/dev/null || true
mv "INTERSECTION_EMISSION_WORD_EMERGENCE_STRATEGY.md" "docs/implementation/" 2>/dev/null || true
mv "HYBRID_SELECTION_EMISSION_STRATEGY.md" "docs/implementation/" 2>/dev/null || true
mv "TEMPLATE_EXPANSION_NOV11_2025.md" "docs/implementation/" 2>/dev/null || true
mv "SYSTEM_TUNABLE_PARAMETERS.md" "docs/implementation/" 2>/dev/null || true
mv "NEO4J_SETUP_INSTRUCTIONS.md" "docs/implementation/" 2>/dev/null || true
mv "PRODUCTION_DEPLOYMENT_STATUS.md" "docs/implementation/" 2>/dev/null || true

echo "  ✅ Implementation guides moved"

# ====================================
# ANALYSIS (19 files)
# ====================================
echo "[4/6] Moving analysis reports..."

mv "APPETITION_MISALIGNMENT_ANALYSIS_NOV11_2025.md" "docs/analysis/" 2>/dev/null || true
mv "APPETITION_SCORE_BUG_FIX_NOV11_2025.md" "docs/analysis/" 2>/dev/null || true
mv "APPETITION_FIX_IMPLEMENTATION_NOV11_2025.md" "docs/analysis/" 2>/dev/null || true
mv "LEARNING_SYSTEM_DIAGNOSTIC_NOV11_2025.md" "docs/analysis/" 2>/dev/null || true
mv "HEALTH_MONITOR_DIAGNOSTIC_NOV11_2025.md" "docs/analysis/" 2>/dev/null || true
mv "CONVERSATIONAL_HEALTH_MONITORING_NOV11_2025.md" "docs/analysis/" 2>/dev/null || true
mv "TRAINING_READINESS_AUDIT_NOV11_2025.md" "docs/analysis/" 2>/dev/null || true
mv "TRAINING_READINESS_ASSESSMENT_WITH_SALIENCE_NOV12_2025.md" "docs/analysis/" 2>/dev/null || true
mv "PLACEHOLDER_AUDIT_SUMMARY_NOV11_2025.md" "docs/analysis/" 2>/dev/null || true
mv "EPOCH_1_TRAINING_ANALYSIS_NOV12_2025.md" "docs/analysis/" 2>/dev/null || true
mv "MATHEMATICAL_CORRELATIONS_VALIDATION_NOV12_2025.md" "docs/analysis/" 2>/dev/null || true
mv "SALIENCE_SELF_ORGAN_INTEGRATION_ANALYSIS_NOV12_2025.md" "docs/analysis/" 2>/dev/null || true
mv "SELF_MATRIX_INTEGRATION_GAP_ANALYSIS_NOV12_2025.md" "docs/analysis/" 2>/dev/null || true
mv "SYSTEM_MATURITY_ASSESSMENT_REPORT_NOV12_2025.md" "docs/analysis/" 2>/dev/null || true
mv "TEST_INFRASTRUCTURE_AUDIT_REPORT.md" "docs/analysis/" 2>/dev/null || true
mv "TEST_INFRASTRUCTURE_AUDIT_VISUAL_SUMMARY.md" "docs/analysis/" 2>/dev/null || true
mv "SAFETY_ASSESSMENT_NOV11_2025.md" "docs/analysis/" 2>/dev/null || true
mv "SYSTEM_STATUS_NOV_11_2025.md" "docs/analysis/" 2>/dev/null || true
mv "API_FIXES_COMPLETE_NOV12_2025.md" "docs/analysis/" 2>/dev/null || true

echo "  ✅ Analysis reports moved"

# ====================================
# ROADMAPS (12 files)
# ====================================
echo "[5/6] Moving roadmap docs..."

mv "TEXT_NATIVE_DEVELOPMENT_ROADMAP.md" "docs/roadmaps/" 2>/dev/null || true
mv "EMISSION_IMPLEMENTATION_ROADMAP_ADAPTED.md" "docs/roadmaps/" 2>/dev/null || true
mv "KNOWLEDGE_INTEGRATION_ROADMAP.md" "docs/roadmaps/" 2>/dev/null || true
mv "FFITTSS_DAE_GOV_INTEGRATION_ROADMAP.md" "docs/roadmaps/" 2>/dev/null || true
mv "NEXUS_14_TYPE_INTEGRATION_ROADMAP_NOV12_2025.md" "docs/roadmaps/" 2>/dev/null || true
mv "SALIENCE_MODEL_INTEGRATION_PLAN.md" "docs/roadmaps/" 2>/dev/null || true
mv "DAE_GOV_IMPLEMENTATION_STRATEGY.md" "docs/roadmaps/" 2>/dev/null || true
mv "DAE_GOV_ENHANCEMENT_PROPOSAL_NOV11_2025.md" "docs/roadmaps/" 2>/dev/null || true
mv "RECONSTRUCTION_EMISSION_DEBT.md" "docs/roadmaps/" 2>/dev/null || true
mv "IMIGRATION_STATUS.md" "docs/roadmaps/" 2>/dev/null || true
mv "CPU_ASSESSMENT_TO_APP.md" "docs/roadmaps/" 2>/dev/null || true
mv "UI_Pythongame.md" "docs/roadmaps/" 2>/dev/null || true

echo "  ✅ Roadmap docs moved"

# ====================================
# ARCHIVE (20 files)
# ====================================
echo "[6/6] Moving archive docs..."

mv "ANALYSIS_FINAL_SUMMARY.md" "docs/archive/" 2>/dev/null || true
mv "ANALYSIS_INDEX.md" "docs/archive/" 2>/dev/null || true
mv "ACCURACY_VERIFICATION_AND_SYSTEM_BREAKDOWN.md" "docs/archive/" 2>/dev/null || true
mv "ORGAN_ACTIVATION_STATUS.md" "docs/archive/" 2>/dev/null || true
mv "GROUND_TRUTH_VALIDATION.md" "docs/archive/" 2>/dev/null || true
mv "REPORT_DATA_SOURCE_INVESTIGATION.md" "docs/archive/" 2>/dev/null || true
mv "DAE_HYPHAE_0_TEMPLATE_ANALYSIS.md" "docs/archive/" 2>/dev/null || true
mv "COMPETITIVE_ANALYSIS_ARC_PRIZE.md" "docs/archive/" 2>/dev/null || true
mv "INVESTIGATION_SUMMARY.md" "docs/archive/" 2>/dev/null || true
mv "INVESTIGATION_INDEX.md" "docs/archive/" 2>/dev/null || true
mv "INVESTIGATION_COMPLETION_REPORT.md" "docs/archive/" 2>/dev/null || true
mv "DESIGN_DOCUMENT_SUMMARY.md" "docs/archive/" 2>/dev/null || true
mv "DOCUMENTATION_INDEX.md" "docs/archive/" 2>/dev/null || true
mv "README_EPOCH_TRAINING_DESIGN.md" "docs/archive/" 2>/dev/null || true
mv "RESPONSE_ENRICHMENT_ANALYSIS.md" "docs/archive/" 2>/dev/null || true
mv "DAE_GOV_DISCONNECT_ANALYSIS.md" "docs/archive/" 2>/dev/null || true
mv "DAE_GOV_FLOW_TRACE_VISUAL.md" "docs/archive/" 2>/dev/null || true
mv "SYSTEM_STATUS_AND_FORWARD_PATH.md" "docs/archive/" 2>/dev/null || true
mv "MATHEMATICAL_EXPLANATION_TRANSDUCTION_AND_TSK.md" "docs/archive/" 2>/dev/null || true
mv "DAE_GOV_SELF_MATRIX_MATHEMATICAL_ADDENDUM.md" "docs/archive/" 2>/dev/null || true
mv "TRANSDUCTIVE_ASSETS_ASSESSMENT.md" "docs/archive/" 2>/dev/null || true

echo "  ✅ Archive docs moved"

echo ""
echo "======================================"
echo "✅ REORGANIZATION COMPLETE"
echo "======================================"
echo ""
echo "Summary:"
echo "  - Architecture:     18 files → docs/architecture/"
echo "  - Phases:           22 files → docs/phases/"
echo "  - Implementation:   15 files → docs/implementation/"
echo "  - Analysis:         19 files → docs/analysis/"
echo "  - Roadmaps:         12 files → docs/roadmaps/"
echo "  - Archive:          20 files → docs/archive/"
echo "  - Root (kept):       8 files (CLAUDE.md, README.md, etc.)"
echo ""
echo "Files in root now:"
ls -1 *.md 2>/dev/null | wc -l
echo ""
echo "Run verification script to check results:"
echo "  bash scripts/verify_docs_organization.sh"
echo ""
