#!/usr/bin/env python3
"""
Comprehensive Entity Context Flow Diagnostic
Traces entity context through entire processing pipeline.

November 14, 2025 - Entity Integration Debugging
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
import json


def test_stage_1_occasion_enrichment():
    """Stage 1: Verify TextOccasions get enriched with entity context."""
    print("=" * 80)
    print("STAGE 1: TextOccasion Entity Enrichment")
    print("=" * 80)

    organism = ConversationalOrganismWrapper()

    context = {
        'stored_entities': {
            'user_name': 'Alice',
            'family_members': [{'name': 'Bob', 'relation': 'brother'}],
            'friends': [],
            'preferences': {'color': 'blue'}
        },
        'username': 'test_user'
    }

    # Test 1: Text containing entity name
    text1 = "Hello, my name is Alice"
    occasions1 = organism._create_text_occasions(text1, context=context)

    print(f"\n✓ Test 1: Text CONTAINS entity name")
    print(f"  Input: \"{text1}\"")
    print(f"  Occasions created: {len(occasions1)}")

    # Check if any occasion has entity_references
    alice_detected = any('Alice' in occ.entity_references for occ in occasions1)
    print(f"  Entity 'Alice' detected in references: {alice_detected}")

    for i, occ in enumerate(occasions1):
        if occ.entity_references:
            print(f"  Occasion {i} (\"{occ.text}\"): {occ.entity_references}")

    # Test 2: Text NOT containing entity name
    text2 = "What is my name?"
    occasions2 = organism._create_text_occasions(text2, context=context)

    print(f"\n✓ Test 2: Text DOES NOT contain entity name")
    print(f"  Input: \"{text2}\"")
    print(f"  Occasions created: {len(occasions2)}")

    # All should have known_entities even if no references
    all_have_known = all(occ.known_entities.get('user_name') == 'Alice' for occ in occasions2)
    print(f"  All occasions have known_entities['user_name']='Alice': {all_have_known}")

    any_references = any(occ.entity_references for occ in occasions2)
    print(f"  Any occasions have entity_references: {any_references}")

    return alice_detected and all_have_known


def test_stage_2_organism_wrapper_context_passing():
    """Stage 2: Verify organism wrapper passes context to reconstruction pipeline."""
    print("\n" + "=" * 80)
    print("STAGE 2: Organism Wrapper → Reconstruction Pipeline")
    print("=" * 80)

    # We need to inspect the actual call chain
    # Check if organ_reconstruction_pipeline receives entity context

    from persona_layer.organ_reconstruction_pipeline import OrganReconstructionPipeline
    import inspect

    # Check generate_reconstruction_emission signature
    sig = inspect.signature(OrganReconstructionPipeline.generate_reconstruction_emission)
    params = list(sig.parameters.keys())

    print(f"\n✓ OrganReconstructionPipeline.generate_reconstruction_emission() parameters:")
    for i, param in enumerate(params, 1):
        print(f"  {i}. {param}")

    has_entity_param = 'entity_context' in params or 'context' in params or 'stored_entities' in params
    print(f"\n  Has entity-related parameter: {has_entity_param}")

    return has_entity_param


def test_stage_3_emission_generator():
    """Stage 3: Verify emission generator methods accept entity context."""
    print("\n" + "=" * 80)
    print("STAGE 3: Emission Generator Entity Context Support")
    print("=" * 80)

    from persona_layer.emission_generator import EmissionGenerator
    import inspect

    methods_to_check = [
        'generate_v0_guided_emissions',
        '_generate_felt_guided_llm_single',
        '_generate_felt_guided_llm_fallback'
    ]

    results = {}

    for method_name in methods_to_check:
        if hasattr(EmissionGenerator, method_name):
            method = getattr(EmissionGenerator, method_name)
            sig = inspect.signature(method)
            params = list(sig.parameters.keys())

            has_entity = any('entity' in p.lower() for p in params)

            print(f"\n✓ {method_name}:")
            print(f"  Has entity parameter: {has_entity}")

            if has_entity:
                entity_params = [p for p in params if 'entity' in p.lower()]
                print(f"  Entity parameters: {entity_params}")

            results[method_name] = has_entity
        else:
            print(f"\n✗ {method_name}: NOT FOUND")
            results[method_name] = False

    return results


def test_stage_4_felt_guided_llm():
    """Stage 4: Verify FeltGuidedLLMGenerator receives entity context."""
    print("\n" + "=" * 80)
    print("STAGE 4: FeltGuidedLLMGenerator Entity Context Support")
    print("=" * 80)

    from persona_layer.felt_guided_llm_generator import FeltGuidedLLMGenerator
    import inspect

    sig = inspect.signature(FeltGuidedLLMGenerator.generate_from_felt_state)
    params = list(sig.parameters.keys())

    print(f"\n✓ FeltGuidedLLMGenerator.generate_from_felt_state() parameters:")
    for i, param in enumerate(params, 1):
        print(f"  {i}. {param}")

    has_entity = 'entity_context_string' in params
    print(f"\n  Has 'entity_context_string' parameter: {has_entity}")

    return has_entity


def test_stage_5_end_to_end_trace():
    """Stage 5: End-to-end trace with debug output."""
    print("\n" + "=" * 80)
    print("STAGE 5: End-to-End Entity Context Trace")
    print("=" * 80)

    # Patch to add debug output
    print("\n🔍 Tracing entity context through process_text()...")

    organism = ConversationalOrganismWrapper()

    context = {
        'stored_entities': {
            'user_name': 'Alice',
            'family_members': [],
            'friends': [],
            'preferences': {}
        },
        'username': 'test_user'
    }

    text = "What is my name?"

    print(f"\n📥 Input: \"{text}\"")
    print(f"📦 Context: user_name = {context['stored_entities']['user_name']}")

    # Process
    result = organism.process_text(
        text=text,
        context=context,
        enable_tsk_recording=False
    )

    print(f"\n📤 Emission: \"{result['emission_text'][:100]}...\"")

    # Check if emission mentions Alice
    mentions_alice = 'alice' in result['emission_text'].lower()
    print(f"\n✅ Emission mentions 'Alice': {mentions_alice}")

    return mentions_alice


def main():
    """Run all diagnostic stages."""
    print("\n🔍 COMPREHENSIVE ENTITY CONTEXT FLOW DIAGNOSTIC")
    print("November 14, 2025")
    print("\n")

    results = {}

    # Stage 1
    results['stage1_occasion_enrichment'] = test_stage_1_occasion_enrichment()

    # Stage 2
    results['stage2_wrapper_to_pipeline'] = test_stage_2_organism_wrapper_context_passing()

    # Stage 3
    results['stage3_emission_generator'] = test_stage_3_emission_generator()

    # Stage 4
    results['stage4_felt_guided_llm'] = test_stage_4_felt_guided_llm()

    # Stage 5
    results['stage5_end_to_end'] = test_stage_5_end_to_end_trace()

    # Summary
    print("\n" + "=" * 80)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 80)

    print(f"\n✅ Stage 1: TextOccasion Enrichment: {results['stage1_occasion_enrichment']}")
    print(f"{'✅' if results['stage2_wrapper_to_pipeline'] else '❌'} Stage 2: Wrapper → Pipeline: {results['stage2_wrapper_to_pipeline']}")

    stage3 = results['stage3_emission_generator']
    print(f"\n   Stage 3: Emission Generator Methods:")
    for method, has_entity in stage3.items():
        status = '✅' if has_entity else '❌'
        print(f"   {status} {method}: {has_entity}")

    print(f"\n✅ Stage 4: FeltGuidedLLMGenerator: {results['stage4_felt_guided_llm']}")
    print(f"{'✅' if results['stage5_end_to_end'] else '❌'} Stage 5: End-to-End Name Recall: {results['stage5_end_to_end']}")

    # Diagnosis
    print("\n" + "=" * 80)
    print("DIAGNOSIS")
    print("=" * 80)

    if not results['stage5_end_to_end']:
        print("\n❌ ISSUE IDENTIFIED: Entity context not reaching LLM")
        print("\nLikely causes:")

        if not stage3['generate_v0_guided_emissions']:
            print("  1. generate_v0_guided_emissions() missing entity parameter")

        if stage3['_generate_felt_guided_llm_single'] and not stage3['generate_v0_guided_emissions']:
            print("  2. Entity parameter exists in _generate_felt_guided_llm_single() but")
            print("     not passed from generate_v0_guided_emissions()")

        if not results['stage2_wrapper_to_pipeline']:
            print("  3. OrganReconstructionPipeline not receiving entity context")

        print("\n🔧 RECOMMENDED FIXES:")
        print("  1. Add entity_context parameter to generate_v0_guided_emissions()")
        print("  2. Pass entity_context through reconstruction pipeline")
        print("  3. Build entity_context_string from stored_entities")
    else:
        print("\n✅ ALL SYSTEMS OPERATIONAL: Entity context flowing to LLM!")

    return results


if __name__ == '__main__':
    results = main()

    # Exit code based on end-to-end test
    sys.exit(0 if results['stage5_end_to_end'] else 1)
