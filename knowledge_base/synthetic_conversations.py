"""
Synthetic Trauma-Informed Conversation Examples - Week 2, Day 8-10
Phase 2: Corpus Building for Knowledge Infrastructure

Generates 30 diverse trauma-informed organizational conversation examples
covering key concepts: burnout, toxic productivity, psychological safety,
polyvagal states, IFS parts, witnessing, boundaries, and SELF-distance.

These conversations provide training data for:
- FAISS semantic memory (pattern recognition)
- Hebbian learning (co-activation patterns)
- Neo4j graph traversal (concept relationships)

Author: Claude Code (November 2025)
Status: Corpus Building - Week 2, Day 8-10
"""

import json
from pathlib import Path
from typing import List, Dict

# Synthetic trauma-informed conversation examples
SYNTHETIC_CONVERSATIONS = [
    # Burnout & Exhaustion Scenarios (1-5)
    {
        "id": "burnout_001",
        "category": "burnout_spiral",
        "polyvagal_state": "dorsal_vagal",
        "dominant_part": "exile",
        "self_distance": 0.85,
        "conversation": """
        Our team is completely burned out. People are working 60-hour weeks,
        missing deadlines anyway, and making careless mistakes. Nobody has
        energy left. We're in a constant state of exhaustion and overwhelm.
        Leadership keeps pushing for more without acknowledging the toll this
        is taking. Several people have mentioned wanting to quit. The culture
        feels toxic and unsustainable.
        """
    },
    {
        "id": "burnout_002",
        "category": "burnout_spiral",
        "polyvagal_state": "sympathetic",
        "dominant_part": "firefighter",
        "self_distance": 0.78,
        "conversation": """
        I can't keep this pace. Every morning I wake up with anxiety about
        the mountain of tasks ahead. My manager keeps adding more to my plate
        without removing anything. I'm working weekends just to stay afloat.
        I feel like I'm failing at everything. The stress is affecting my
        health and my relationships outside work. Something has to change.
        """
    },
    {
        "id": "burnout_003",
        "category": "burnout_spiral",
        "polyvagal_state": "dorsal_vagal",
        "dominant_part": "exile",
        "self_distance": 0.92,
        "conversation": """
        We've lost three senior engineers this quarter to burnout. The pattern
        is always the same: someone starts missing meetings, their work quality
        drops, they become withdrawn, and then they give two weeks notice.
        Management's response is to redistribute their work to the remaining
        team, which just accelerates the burnout cycle. We're in a death spiral
        and nobody's addressing the root cause.
        """
    },
    {
        "id": "burnout_004",
        "category": "burnout_spiral",
        "polyvagal_state": "sympathetic",
        "dominant_part": "manager",
        "self_distance": 0.81,
        "conversation": """
        I've been pushing through exhaustion for months, telling myself I can
        handle it. But my body is screaming at me to stop. I'm getting
        tension headaches, sleeping poorly, and snapping at my colleagues.
        I know I'm not performing well, but I'm too overwhelmed to figure out
        how to get out of this hole. I feel trapped.
        """
    },
    {
        "id": "burnout_005",
        "category": "burnout_spiral",
        "polyvagal_state": "dorsal_vagal",
        "dominant_part": "exile",
        "self_distance": 0.88,
        "conversation": """
        The burnout in our organization has reached crisis levels. People are
        emotionally flat, going through the motions. There's no creativity,
        no innovation, no joy in the work. We're all just trying to survive
        until Friday. Leadership talks about "resilience" and "grit," but
        what we actually need is rest and realistic expectations.
        """
    },

    # Toxic Productivity Scenarios (6-10)
    {
        "id": "toxic_prod_001",
        "category": "toxic_productivity",
        "polyvagal_state": "sympathetic",
        "dominant_part": "manager",
        "self_distance": 0.73,
        "conversation": """
        Our company culture valorizes overwork. People brag about pulling
        all-nighters and working through weekends. If you leave at 5pm, you're
        seen as not committed. There's constant competition to be the most
        productive, the most available, the most sacrificing. It's exhausting
        and destructive, but nobody wants to be the first to slow down.
        """
    },
    {
        "id": "toxic_prod_002",
        "category": "toxic_productivity",
        "polyvagal_state": "sympathetic",
        "dominant_part": "manager",
        "self_distance": 0.76,
        "conversation": """
        We measure everything: lines of code, tickets closed, hours logged.
        But all this quantification has made us lose sight of actual value.
        People game the metrics instead of doing meaningful work. The obsession
        with productivity numbers is making us less effective, not more. We're
        optimizing the wrong things.
        """
    },
    {
        "id": "toxic_prod_003",
        "category": "toxic_productivity",
        "polyvagal_state": "sympathetic",
        "dominant_part": "firefighter",
        "self_distance": 0.79,
        "conversation": """
        My manager expects immediate responses to Slack messages, even at 10pm.
        There's an unspoken rule that we're always on call, always available.
        Boundaries are seen as weakness. The phrase "work-life balance" is
        treated like a joke. This isn't sustainable, but everyone's afraid to
        push back because they'll be seen as not a team player.
        """
    },
    {
        "id": "toxic_prod_004",
        "category": "toxic_productivity",
        "polyvagal_state": "sympathetic",
        "dominant_part": "manager",
        "self_distance": 0.71,
        "conversation": """
        We have a "hustle culture" that glorifies suffering. People wear their
        exhaustion as a badge of honor. Taking a mental health day is frowned
        upon. Using your full vacation time makes you look weak. The message
        is clear: your worth is measured by your willingness to sacrifice your
        wellbeing for the company.
        """
    },
    {
        "id": "toxic_prod_005",
        "category": "toxic_productivity",
        "polyvagal_state": "sympathetic",
        "dominant_part": "manager",
        "self_distance": 0.74,
        "conversation": """
        Every meeting ends with more action items than we started with. We're
        in constant execution mode with no time for reflection or strategic
        thinking. The pace is relentless. If you're not visibly busy, you're
        suspect. Rest is equated with laziness. This performative productivity
        is destroying our capacity for actual innovation.
        """
    },

    # Psychological Safety & Trust (11-15)
    {
        "id": "psych_safety_001",
        "category": "psychological_safety",
        "polyvagal_state": "ventral_vagal",
        "dominant_part": "self",
        "self_distance": 0.15,
        "conversation": """
        Our team has built real psychological safety. People can admit mistakes
        without fear of punishment. We challenge each other's ideas respectfully.
        When someone's struggling, we adjust the workload as a team. There's
        genuine trust and vulnerability. This foundation lets us take creative
        risks and learn from failures.
        """
    },
    {
        "id": "psych_safety_002",
        "category": "psychological_safety",
        "polyvagal_state": "ventral_vagal",
        "dominant_part": "self",
        "self_distance": 0.22,
        "conversation": """
        In our retrospectives, people actually tell the truth about what's not
        working. Leadership listens without getting defensive. We've created
        space for difficult conversations. When there's conflict, we work
        through it instead of avoiding it. The safety to be honest has made
        us so much more effective.
        """
    },
    {
        "id": "psych_safety_003",
        "category": "psychological_safety",
        "polyvagal_state": "ventral_vagal",
        "dominant_part": "self",
        "self_distance": 0.18,
        "conversation": """
        We recently implemented "fail forward" sessions where people share
        projects that didn't work out and what they learned. At first people
        were nervous, but now it's one of our most valuable practices. The
        vulnerability has built deep trust. We're learning faster because
        we're not hiding our mistakes.
        """
    },
    {
        "id": "psych_safety_004",
        "category": "psychological_safety",
        "polyvagal_state": "sympathetic",
        "dominant_part": "manager",
        "self_distance": 0.68,
        "conversation": """
        We claim to have psychological safety, but the reality is different.
        People are afraid to speak up in meetings because dissenters get
        marginalized. Mistakes are punished, not learned from. The culture
        rewards conformity and punishes honesty. We're missing out on valuable
        perspectives because people don't feel safe to share them.
        """
    },
    {
        "id": "psych_safety_005",
        "category": "psychological_safety",
        "polyvagal_state": "ventral_vagal",
        "dominant_part": "self",
        "self_distance": 0.21,
        "conversation": """
        Our manager explicitly invites dissenting opinions and thanks people
        for raising concerns. She models vulnerability by sharing her own
        uncertainties. The team knows that being honest won't hurt their career.
        This safety has unlocked so much creativity and problem-solving capacity
        that was hidden when people were playing it safe.
        """
    },

    # Witnessing & Holding Space (16-20)
    {
        "id": "witnessing_001",
        "category": "witnessing_presence",
        "polyvagal_state": "ventral_vagal",
        "dominant_part": "self",
        "self_distance": 0.12,
        "conversation": """
        In our one-on-ones, my manager really sees me. Not just my productivity,
        but my whole experience. When I shared that I was struggling with the
        workload, she didn't immediately try to fix it or minimize it. She
        just listened and validated what I was feeling. That witnessing gave
        me the space to figure out what I needed.
        """
    },
    {
        "id": "witnessing_002",
        "category": "witnessing_presence",
        "polyvagal_state": "ventral_vagal",
        "dominant_part": "self",
        "self_distance": 0.19,
        "conversation": """
        We've started doing "check-ins" at the beginning of meetings where
        people can share how they're actually doing. It's not performative;
        there's genuine space for presence. Sometimes someone will say they're
        having a hard day and we'll adjust the agenda. This practice of
        witnessing each other has deepened our connection as a team.
        """
    },
    {
        "id": "witnessing_003",
        "category": "witnessing_presence",
        "polyvagal_state": "ventral_vagal",
        "dominant_part": "self",
        "self_distance": 0.14,
        "conversation": """
        When our project failed, our director didn't rush to blame or problem-solve.
        She held space for the team to process the disappointment and frustration.
        That witnessing of our grief about the failure was incredibly healing.
        It allowed us to move forward without carrying resentment or shame.
        """
    },
    {
        "id": "witnessing_004",
        "category": "witnessing_presence",
        "polyvagal_state": "sympathetic",
        "dominant_part": "firefighter",
        "self_distance": 0.72,
        "conversation": """
        Nobody really listens here. In meetings, people are waiting for their
        turn to talk, not actually hearing each other. When someone shares a
        struggle, the response is immediate advice or fixing, not presence.
        There's no space for being witnessed. It's all about moving fast and
        getting things done, with no room for the human experience.
        """
    },
    {
        "id": "witnessing_005",
        "category": "witnessing_presence",
        "polyvagal_state": "ventral_vagal",
        "dominant_part": "self",
        "self_distance": 0.16,
        "conversation": """
        Our team coach taught us to practice "non-fixing presence." When
        someone shares a challenge, we first just witness it without jumping
        to solutions. This simple practice has transformed our relationships.
        People feel truly seen and heard. Paradoxically, being witnessed often
        leads to better solutions than immediate fixing ever did.
        """
    },

    # Boundaries & Sustainable Rhythm (21-25)
    {
        "id": "boundaries_001",
        "category": "sustainable_rhythm",
        "polyvagal_state": "ventral_vagal",
        "dominant_part": "self",
        "self_distance": 0.23,
        "conversation": """
        I've learned to set clear boundaries around my work hours. I don't
        check email after 6pm or on weekends. At first I was nervous about
        pushback, but my team has actually respected these boundaries. Modeling
        sustainable work has given others permission to do the same. We're all
        more effective with these limits in place.
        """
    },
    {
        "id": "boundaries_002",
        "category": "sustainable_rhythm",
        "polyvagal_state": "ventral_vagal",
        "dominant_part": "self",
        "self_distance": 0.28,
        "conversation": """
        Our team explicitly discusses capacity in our planning sessions. We
        say no to projects that would overextend us. We build in buffer time
        for the unexpected. This sustainable pacing means we actually finish
        what we commit to, and we finish it well. The boundaries have made us
        more reliable, not less.
        """
    },
    {
        "id": "boundaries_003",
        "category": "sustainable_rhythm",
        "polyvagal_state": "ventral_vagal",
        "dominant_part": "self",
        "self_distance": 0.19,
        "conversation": """
        We implemented a team agreement: no meetings before 10am or after 4pm,
        and Fridays are meeting-free for deep work. These boundaries have given
        everyone space to think and recharge. Productivity has actually increased
        because we're working with our natural rhythms instead of against them.
        """
    },
    {
        "id": "boundaries_004",
        "category": "sustainable_rhythm",
        "polyvagal_state": "sympathetic",
        "dominant_part": "manager",
        "self_distance": 0.67,
        "conversation": """
        I want to set boundaries, but I'm afraid of the consequences. My
        manager makes comments about people who "aren't committed enough."
        There's pressure to always be available, always say yes. I know I need
        limits for my health, but I'm scared that boundaries will hurt my
        career advancement here.
        """
    },
    {
        "id": "boundaries_005",
        "category": "sustainable_rhythm",
        "polyvagal_state": "ventral_vagal",
        "dominant_part": "self",
        "self_distance": 0.24,
        "conversation": """
        Our organization finally recognized that sustainable pace is better
        than crunch time. We mandate that people take their full vacation.
        We actively monitor for signs of overwork. Leadership models boundaries
        by not sending late-night emails. This culture shift has reduced
        turnover and increased innovation.
        """
    },

    # Scapegoating & Shadow Dynamics (26-30)
    {
        "id": "scapegoat_001",
        "category": "scapegoat_dynamics",
        "polyvagal_state": "dorsal_vagal",
        "dominant_part": "exile",
        "self_distance": 0.89,
        "conversation": """
        Whenever something goes wrong in our department, blame falls on the
        same person. She's become the scapegoat for systemic failures. Instead
        of examining our broken processes, we point to her as the problem. It's
        easier to have someone to blame than to face the uncomfortable truth
        about our organizational dysfunction.
        """
    },
    {
        "id": "scapegoat_002",
        "category": "scapegoat_dynamics",
        "polyvagal_state": "sympathetic",
        "dominant_part": "exile",
        "self_distance": 0.83,
        "conversation": """
        I've become the person everyone blames when projects fail. It doesn't
        matter that the real issues are unrealistic timelines and poor planning.
        There's something about me that makes me an easy target. I'm carrying
        the shadow of the whole organization. The isolation is crushing, and
        I don't know how to break out of this role.
        """
    },
    {
        "id": "scapegoat_003",
        "category": "scapegoat_dynamics",
        "polyvagal_state": "sympathetic",
        "dominant_part": "firefighter",
        "self_distance": 0.76,
        "conversation": """
        Our team has an unspoken agreement: when things go wrong, we blame the
        QA department. It's a collective shadow we're not willing to look at.
        The scapegoating protects us from examining our own contribution to
        failures, but it's destroying trust and collaboration across departments.
        """
    },
    {
        "id": "scapegoat_004",
        "category": "scapegoat_dynamics",
        "polyvagal_state": "ventral_vagal",
        "dominant_part": "self",
        "self_distance": 0.31,
        "conversation": """
        We caught ourselves scapegoating and decided to interrupt the pattern.
        Now when something fails, we do a blameless postmortem focused on
        systems, not individuals. It was uncomfortable at first to face our
        collective responsibility, but this practice has ended the scapegoating
        cycle and made us much more effective as a team.
        """
    },
    {
        "id": "scapegoat_005",
        "category": "scapegoat_dynamics",
        "polyvagal_state": "dorsal_vagal",
        "dominant_part": "exile",
        "self_distance": 0.91,
        "conversation": """
        The organizational shadow gets projected onto our remote workers. When
        communication breaks down or deadlines slip, management blames "remote
        work culture" instead of addressing actual systemic issues. The remote
        team carries all the organization's anxiety about control and visibility.
        It's a scapegoating dynamic that's destroying morale and trust.
        """
    },
]


def save_synthetic_conversations(output_path: str = None) -> Dict[str, any]:
    """
    Save synthetic conversations to JSON file.

    Args:
        output_path: Path to save JSON file (default: knowledge_base/synthetic_conversations.json)

    Returns:
        Dictionary with statistics about the saved conversations
    """
    if output_path is None:
        output_path = Path(__file__).parent / "synthetic_conversations.json"
    else:
        output_path = Path(output_path)

    # Ensure directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Calculate statistics
    stats = {
        "total_conversations": len(SYNTHETIC_CONVERSATIONS),
        "categories": {},
        "polyvagal_states": {},
        "dominant_parts": {},
        "mean_self_distance": 0.0,
        "conversations_by_id": {}
    }

    total_self_distance = 0.0

    for conv in SYNTHETIC_CONVERSATIONS:
        # Category counts
        category = conv["category"]
        stats["categories"][category] = stats["categories"].get(category, 0) + 1

        # Polyvagal state counts
        state = conv["polyvagal_state"]
        stats["polyvagal_states"][state] = stats["polyvagal_states"].get(state, 0) + 1

        # Dominant part counts
        part = conv["dominant_part"]
        stats["dominant_parts"][part] = stats["dominant_parts"].get(part, 0) + 1

        # Self-distance accumulation
        total_self_distance += conv["self_distance"]

        # Store by ID
        stats["conversations_by_id"][conv["id"]] = {
            "category": category,
            "polyvagal_state": state,
            "dominant_part": part,
            "self_distance": conv["self_distance"],
            "text_length": len(conv["conversation"].strip())
        }

    stats["mean_self_distance"] = total_self_distance / len(SYNTHETIC_CONVERSATIONS)

    # Save conversations
    with open(output_path, 'w') as f:
        json.dump({
            "metadata": {
                "description": "Synthetic trauma-informed organizational conversation examples",
                "created": "2025-11-10",
                "purpose": "Training data for DAE-GOV knowledge infrastructure",
                "version": "1.0"
            },
            "statistics": stats,
            "conversations": SYNTHETIC_CONVERSATIONS
        }, f, indent=2)

    print(f"\n✅ Saved {len(SYNTHETIC_CONVERSATIONS)} synthetic conversations to {output_path}")
    return stats


def get_conversations_by_category(category: str) -> List[Dict]:
    """Get all conversations for a specific category."""
    return [c for c in SYNTHETIC_CONVERSATIONS if c["category"] == category]


def get_conversations_by_polyvagal_state(state: str) -> List[Dict]:
    """Get all conversations for a specific polyvagal state."""
    return [c for c in SYNTHETIC_CONVERSATIONS if c["polyvagal_state"] == state]


def get_conversations_by_self_distance(min_distance: float, max_distance: float) -> List[Dict]:
    """Get conversations within a SELF-distance range."""
    return [
        c for c in SYNTHETIC_CONVERSATIONS
        if min_distance <= c["self_distance"] <= max_distance
    ]


if __name__ == "__main__":
    print("\n" + "="*70)
    print("SYNTHETIC CONVERSATIONS GENERATOR - Week 2, Day 8-10")
    print("="*70 + "\n")

    # Save conversations
    stats = save_synthetic_conversations()

    # Print statistics
    print("\n📊 Conversation Statistics:")
    print(f"   Total conversations: {stats['total_conversations']}")
    print(f"   Mean SELF-distance: {stats['mean_self_distance']:.3f}")
    print()

    print("📂 By Category:")
    for category, count in sorted(stats["categories"].items()):
        print(f"   {category}: {count}")
    print()

    print("🧠 By Polyvagal State:")
    for state, count in sorted(stats["polyvagal_states"].items()):
        print(f"   {state}: {count}")
    print()

    print("👥 By Dominant Part:")
    for part, count in sorted(stats["dominant_parts"].items()):
        print(f"   {part}: {count}")
    print()

    print("✅ Synthetic conversations ready for FAISS indexing!")
    print("   Next: Download public domain Whitehead texts (Week 2, Day 11-12)")
    print()
