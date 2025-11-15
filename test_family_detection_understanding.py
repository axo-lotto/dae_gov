#!/usr/bin/env python3
"""
Test Family Detection & Understanding from Lengthy User Stories

Purpose: Assess if DAE organism can:
1. Understand what user is saying (semantic comprehension)
2. Detect appropriate family membership for conversations
3. Tag/cluster similar patterns over time
4. Generate emissions that demonstrate understanding

This will inform if epoch training is necessary to improve family formation.
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper


# Test Stories: Lengthy, realistic user inputs across different themes
TEST_STORIES = [
    {
        "id": "burnout_1",
        "expected_family": "burnout_spiral",
        "story": """I've been working 70-hour weeks for the past 6 months and I can't remember
        the last time I felt actually rested. My manager keeps saying "just one more sprint" but
        it never ends. I wake up at 3am thinking about deadlines, my stomach is constantly tight,
        and yesterday I snapped at my partner over something stupid. I know I should set boundaries
        but every time I try, there's this voice in my head saying "if you don't deliver, they'll
        replace you." I feel like I'm running on fumes and I don't even know who I am anymore
        outside of work. The weird part is, I used to love this job. Now I just feel numb."""
    },
    {
        "id": "burnout_2",
        "expected_family": "burnout_spiral",
        "story": """It's been three weeks since I took a real day off. Even on weekends I'm checking
        Slack, responding to emails, fixing "urgent" bugs that could wait until Monday. My team
        depends on me - or at least that's what I tell myself. But honestly? I think I'm just
        terrified of what happens if I stop. Last night I had this dream where I was drowning in
        code and no one could hear me calling for help. I'm exhausted, but I can't seem to let go."""
    },
    {
        "id": "scapegoat_1",
        "expected_family": "scapegoat_dynamics",
        "story": """In every meeting, it somehow becomes my fault. The design wasn't clear? My fault
        for not asking. The API changed? My fault for not predicting it. The timeline was unrealistic?
        My fault for not pushing back harder. I've noticed this pattern - whenever something goes
        wrong, all eyes turn to me. And the thing is, I've started to internalize it. Maybe I AM
        the problem. Maybe if I just worked harder, anticipated more, spoke up louder... but I
        already work 60 hours a week. I already triple-check everything. I already send detailed
        updates. It's never enough. I feel like I'm carrying the emotional weight of the entire
        team's anxiety, and it's crushing me."""
    },
    {
        "id": "safe_connection_1",
        "expected_family": "psychological_safety",
        "story": """Something shifted in our standup today. I admitted I was stuck on a problem and
        didn't know the answer - something I've been terrified to say in past jobs. And instead of
        judgment, three people immediately offered to pair with me. One person said "oh thank god,
        I thought I was the only one who found that confusing." It was this moment of collective
        exhale. We ended up having this really honest conversation about what's hard right now,
        and it didn't feel performative or scary. It felt... human? I realized I've been holding
        my breath for months, waiting for the other shoe to drop, but maybe it won't here."""
    },
    {
        "id": "safe_connection_2",
        "expected_family": "psychological_safety",
        "story": """My manager did something today that I've never experienced before. In our 1:1,
        she asked "how are you, actually?" and then just... waited. Really waited. Didn't fill the
        silence, didn't rush me, didn't make it about project updates. So I told her the truth -
        that I've been struggling with imposter syndrome, that I'm afraid I'm not good enough.
        And she didn't try to fix me or reassure me with platitudes. She just said "yeah, that
        sounds really hard. What would help?" It was the first time I felt like I could be a whole
        person at work, not just a productivity unit."""
    },
    {
        "id": "sustainable_rhythm_1",
        "expected_family": "sustainable_rhythm",
        "story": """I've been experimenting with something new: actually taking my lunch break. Like,
        away from my desk, outside if possible, phone on silent. At first it felt wrong, almost
        rebellious. But I've noticed that when I come back, I'm sharper. Problems that felt
        impossible at 11am suddenly have obvious solutions at 1:30pm. My manager mentioned she's
        noticed the quality of my work has improved. I think I've been confusing "busy" with
        "productive" for years. Turns out rest isn't laziness - it's part of the work."""
    },
    {
        "id": "toxic_productivity_1",
        "expected_family": "toxic_productivity",
        "story": """I track everything. Steps, calories, work hours, lines of code, emails sent,
        tasks completed. I have a spreadsheet where I log my daily productivity score. If I don't
        hit my targets, I feel this visceral sense of failure. Even when I'm "relaxing," I'm
        optimizing - productivity podcasts while cooking, language learning app while walking,
        always maximizing every minute. My therapist asked me when I last did something just for
        joy, not for self-improvement. I couldn't answer. I think I've turned myself into a
        perpetual optimization machine and I don't know how to stop."""
    },
    {
        "id": "witnessing_presence_1",
        "expected_family": "witnessing_presence",
        "story": """I told my best friend about the anxiety I've been carrying, and she didn't try
        to fix it. She didn't offer solutions or tell me it would be okay. She just said "that
        sounds really heavy" and sat with me. We were quiet for a while, and in that silence,
        something loosened in my chest. I realized how rare that is - to not be rushed toward
        resolution, to not have to perform being "better" already. Just being witnessed, exactly
        as I am, messy and confused and hurting. It was more healing than any advice could have been."""
    },
    {
        "id": "parts_conflict_1",
        "expected_family": "parts_multiplicity",  # New family we should detect
        "story": """There's this war happening inside me. Part of me desperately wants to quit my
        job and travel, just disappear for six months and figure out who I am. But another part
        is terrified - what about the mortgage? What about my career trajectory? And then there's
        this third voice that's just exhausted by the whole debate, wanting everyone to shut up
        so I can just sleep. Sometimes I feel like I'm three different people trapped in one body,
        all wanting different things, all convinced they know what's best. It's exhausting being
        a committee instead of a person."""
    },
    {
        "id": "somatic_signal_1",
        "expected_family": "body_wisdom",  # New family we should detect
        "story": """My jaw has been clenched for two weeks straight. I only notice when someone
        points it out or when I wake up with a headache. It's like my body is screaming something
        my mind won't acknowledge. Every time I think about going to that team meeting, my stomach
        tightens. When I see my manager's name in my inbox, my shoulders creep up toward my ears.
        My body knows something I'm not letting myself consciously admit. I've been so focused on
        being "professional" and "rational" that I've been ignoring these signals for months. But
        they're getting louder."""
    }
]


def test_family_detection_and_understanding():
    """
    Run lengthy user stories through DAE and assess:
    1. Emission quality (does it demonstrate understanding?)
    2. Nexus formation (what patterns detected?)
    3. Family clustering (are similar stories grouped?)
    4. Organ participation (which organs activate?)
    """

    print("=" * 80)
    print("🌀 FAMILY DETECTION & UNDERSTANDING TEST")
    print("=" * 80)
    print()
    print("Testing DAE's ability to:")
    print("  1. Understand lengthy, realistic user stories")
    print("  2. Detect appropriate family membership")
    print("  3. Generate emissions demonstrating comprehension")
    print("  4. Cluster similar patterns over time")
    print()
    print("=" * 80)
    print()

    # Initialize organism
    organism = ConversationalOrganismWrapper()

    results = []

    for i, test_case in enumerate(TEST_STORIES, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}/{len(TEST_STORIES)}: {test_case['id']}")
        print(f"Expected Family: {test_case['expected_family']}")
        print(f"{'='*80}\n")

        print(f"📖 User Story ({len(test_case['story'])} chars):")
        print(f"   {test_case['story'][:150]}...")
        print()

        # Process through organism
        try:
            result = organism.process_text(
                text=test_case['story'],
                user_id="test_family_detection",
                enable_phase2=True  # Enable multi-cycle V0 convergence
            )

            # Extract key metrics
            emission = result.get('emission', '')
            confidence = result.get('emission_confidence', 0.0)
            nexuses = result.get('dominant_nexuses', [])
            organ_results = result.get('organ_results', {})
            v0_trace = result.get('v0_trace', {})

            # Count active organs
            active_organs = sum(1 for organ, data in organ_results.items()
                              if hasattr(data, 'activation') and data.activation > 0.3)

            # Get V0 descent
            final_v0 = v0_trace.get('final_v0', 0.0)
            initial_v0 = v0_trace.get('initial_v0', 0.0)
            v0_descent = initial_v0 - final_v0

            # Display results
            print(f"✅ PROCESSING SUCCESSFUL")
            print(f"   Confidence: {confidence:.3f}")
            print(f"   V0 Descent: {v0_descent:.3f}")
            print(f"   Active Organs: {active_organs}/11")
            print()

            print(f"🔗 Nexuses Detected ({len(nexuses)}):")
            for nex in nexuses[:5]:  # Top 5
                print(f"   - {nex['name']}: {nex['activation']:.3f}")
            print()

            print(f"💬 Emission Generated ({len(emission)} chars):")
            # Show first 300 chars
            preview = emission[:300] + "..." if len(emission) > 300 else emission
            print(f"   {preview}")
            print()

            # Assess understanding quality
            understanding_score = assess_understanding_quality(
                user_story=test_case['story'],
                emission=emission,
                nexuses=nexuses,
                confidence=confidence
            )

            print(f"📊 Understanding Score: {understanding_score:.2f}/10")
            print()

            # Store result
            results.append({
                'test_id': test_case['id'],
                'expected_family': test_case['expected_family'],
                'story_length': len(test_case['story']),
                'emission_length': len(emission),
                'confidence': confidence,
                'v0_descent': v0_descent,
                'active_organs': active_organs,
                'nexuses': nexuses[:5],
                'understanding_score': understanding_score,
                'emission_preview': emission[:500]
            })

        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()

            results.append({
                'test_id': test_case['id'],
                'expected_family': test_case['expected_family'],
                'error': str(e)
            })

    # Summary analysis
    print("\n" + "="*80)
    print("📊 SUMMARY ANALYSIS")
    print("="*80 + "\n")

    successful_tests = [r for r in results if 'error' not in r]

    if successful_tests:
        avg_confidence = sum(r['confidence'] for r in successful_tests) / len(successful_tests)
        avg_v0_descent = sum(r['v0_descent'] for r in successful_tests) / len(successful_tests)
        avg_active_organs = sum(r['active_organs'] for r in successful_tests) / len(successful_tests)
        avg_understanding = sum(r['understanding_score'] for r in successful_tests) / len(successful_tests)

        print(f"Tests Completed: {len(successful_tests)}/{len(TEST_STORIES)}")
        print(f"Average Confidence: {avg_confidence:.3f}")
        print(f"Average V0 Descent: {avg_v0_descent:.3f}")
        print(f"Average Active Organs: {avg_active_organs:.1f}/11")
        print(f"Average Understanding Score: {avg_understanding:.2f}/10")
        print()

        # Family clustering assessment
        print("🏠 FAMILY CLUSTERING ASSESSMENT:")
        print()

        # Check if similar themes got similar nexuses
        family_nexuses = {}
        for r in successful_tests:
            family = r['expected_family']
            if family not in family_nexuses:
                family_nexuses[family] = []
            family_nexuses[family].append([n['name'] for n in r['nexuses']])

        for family, nexus_lists in family_nexuses.items():
            print(f"  {family}:")
            if len(nexus_lists) > 1:
                # Check overlap between stories in same family
                common_nexuses = set(nexus_lists[0])
                for nex_list in nexus_lists[1:]:
                    common_nexuses &= set(nex_list)

                if common_nexuses:
                    print(f"    ✅ Common nexuses: {', '.join(list(common_nexuses)[:3])}")
                else:
                    print(f"    ⚠️  No common nexuses detected")
            else:
                print(f"    ℹ️  Only one story in family")
            print()

        # Recommendation
        print("="*80)
        print("🎯 EPOCH TRAINING RECOMMENDATION:")
        print("="*80)
        print()

        if avg_understanding < 6.0:
            print("❌ EPOCH TRAINING HIGHLY RECOMMENDED")
            print("   - Understanding score below threshold (< 6.0)")
            print("   - Organism may not be comprehending user stories effectively")
            print("   - Family formation likely inaccurate")
        elif avg_understanding < 7.5:
            print("⚠️  EPOCH TRAINING RECOMMENDED")
            print("   - Understanding score moderate (6.0-7.5)")
            print("   - Organism shows partial comprehension")
            print("   - Family clustering could be improved")
        else:
            print("✅ EPOCH TRAINING OPTIONAL")
            print("   - Understanding score good (> 7.5)")
            print("   - Organism demonstrates solid comprehension")
            print("   - Family formation appears functional")

        print()
        print(f"Confidence: {avg_confidence:.3f} ({'Low' if avg_confidence < 0.5 else 'Good'})")
        print(f"V0 Descent: {avg_v0_descent:.3f} ({'Low' if avg_v0_descent < 0.5 else 'Good'})")
        print(f"Organ Activation: {avg_active_organs:.1f}/11 ({'Low' if avg_active_organs < 8 else 'Good'})")

    else:
        print("❌ NO SUCCESSFUL TESTS - SYSTEM MAY BE BROKEN")

    # Save detailed results
    output_path = Path("results/family_detection_test_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump({
            'summary': {
                'total_tests': len(TEST_STORIES),
                'successful_tests': len(successful_tests),
                'avg_confidence': avg_confidence if successful_tests else 0,
                'avg_v0_descent': avg_v0_descent if successful_tests else 0,
                'avg_active_organs': avg_active_organs if successful_tests else 0,
                'avg_understanding_score': avg_understanding if successful_tests else 0,
                'epoch_training_needed': avg_understanding < 7.5 if successful_tests else True
            },
            'detailed_results': results
        }, f, indent=2)

    print()
    print(f"📁 Detailed results saved to: {output_path}")
    print()


def assess_understanding_quality(user_story, emission, nexuses, confidence):
    """
    Heuristic assessment of whether DAE understood the user story.

    Score 0-10 based on:
    - Emission relevance to story themes
    - Appropriate nexus detection
    - Confidence level
    - Emission length/depth
    """
    score = 0.0

    # 1. Confidence baseline (0-2 points)
    if confidence > 0.7:
        score += 2.0
    elif confidence > 0.5:
        score += 1.5
    elif confidence > 0.3:
        score += 1.0

    # 2. Emission substance (0-2 points)
    if len(emission) > 200:
        score += 2.0
    elif len(emission) > 100:
        score += 1.5
    elif len(emission) > 50:
        score += 1.0

    # 3. Nexus relevance (0-3 points)
    # Check if detected nexuses make sense for story content
    story_lower = user_story.lower()

    relevant_nexus_patterns = {
        'overwhelm': ['crisis', 'urgency', 'survival', 'breaking'],
        'boundary': ['self_protection', 'boundary', 'limits'],
        'safe': ['healing', 'trust', 'presence', 'safety'],
        'exhaust': ['crisis', 'depletion', 'survival'],
        'parts': ['parts', 'multiplicity', 'conflict'],
        'body': ['embodied', 'somatic', 'body']
    }

    nexus_names = [n['name'].lower() for n in nexuses[:5]]

    relevance_count = 0
    for keyword, expected_nexuses in relevant_nexus_patterns.items():
        if keyword in story_lower:
            if any(exp in ' '.join(nexus_names) for exp in expected_nexuses):
                relevance_count += 1

    score += min(3.0, relevance_count * 0.75)

    # 4. Emission thematic alignment (0-3 points)
    # Check if emission mirrors themes from story
    emission_lower = emission.lower()

    theme_keywords = {
        'burnout': ['exhaust', 'burn', 'overwhelm', 'rest', 'boundary'],
        'scapegoat': ['blame', 'fault', 'burden', 'weight', 'carrying'],
        'safe': ['safe', 'trust', 'hold', 'witness', 'space'],
        'rhythm': ['pace', 'rhythm', 'rest', 'sustainable', 'breath'],
        'parts': ['part', 'parts', 'voice', 'conflict', 'society'],
        'body': ['body', 'somatic', 'feel', 'sensation', 'jaw', 'chest']
    }

    theme_match_count = 0
    for theme, keywords in theme_keywords.items():
        story_has_theme = any(kw in story_lower for kw in keywords)
        emission_reflects_theme = any(kw in emission_lower for kw in keywords)

        if story_has_theme and emission_reflects_theme:
            theme_match_count += 1

    score += min(3.0, theme_match_count * 0.6)

    return min(10.0, score)


if __name__ == "__main__":
    test_family_detection_and_understanding()
