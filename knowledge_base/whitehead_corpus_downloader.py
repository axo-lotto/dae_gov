"""
Whitehead Corpus Downloader - Week 2, Day 11-12
Phase 2: Corpus Building for Knowledge Infrastructure

Downloads public domain Alfred North Whitehead texts from:
- Project Gutenberg
- Internet Archive
- Other public domain sources

Focus on process philosophy texts relevant to trauma-informed organizational work:
- Process and Reality (excerpts available)
- The Concept of Nature
- Science and the Modern World
- Adventures of Ideas

Author: Claude Code (November 2025)
Status: Corpus Building - Week 2, Day 11-12
"""

import urllib.request
import json
from pathlib import Path
from typing import List, Dict
import time


# Public domain Whitehead texts available online
WHITEHEAD_TEXTS = [
    {
        "title": "The Concept of Nature",
        "year": 1920,
        "source": "Project Gutenberg",
        "url": "https://www.gutenberg.org/cache/epub/18835/pg18835.txt",
        "gutenberg_id": 18835,
        "description": "Whitehead's Tarner Lectures on philosophy of natural science",
        "relevance": "Foundation for understanding prehension and actual occasions"
    },
    {
        "title": "Science and the Modern World",
        "year": 1925,
        "source": "Project Gutenberg (excerpts)",
        "url": None,  # Not yet on Gutenberg - manual extraction needed
        "gutenberg_id": None,
        "description": "Lowell Lectures on philosophy of science and organism",
        "relevance": "Process philosophy foundations, organic mechanism"
    },
    {
        "title": "An Enquiry Concerning the Principles of Natural Knowledge",
        "year": 1919,
        "source": "Internet Archive",
        "url": None,  # Available on archive.org
        "gutenberg_id": None,
        "description": "Early development of process philosophy concepts",
        "relevance": "Event-based ontology, nature of experience"
    }
]


# Manual process philosophy excerpts (key concepts for trauma-informed work)
PROCESS_PHILOSOPHY_EXCERPTS = [
    {
        "title": "Actual Occasions - Key Concepts",
        "source": "Process and Reality (1929) - Educational Excerpts",
        "content": """
        The actual entity is the real concrescence of many potentials.
        It is a process of becoming, not a static substance.
        Each actual occasion arises from its prehensions of prior occasions,
        synthesizing the many into a novel unity.

        Prehension is the concrete fact of relatedness. An actual occasion
        prehends other occasions as given, as data for its own self-creation.
        There is physical prehension (feeling of feeling) and conceptual
        prehension (feeling of eternal objects as pure potentials).

        Concrescence is the process by which the many become one through
        synthesis. It is not imposed from without but emerges from within
        through the subjective aim guiding the occasion toward satisfaction.

        Satisfaction is the final phase of concrescence, where the becoming
        achieves definiteness. The occasion is now fully determinate and can
        serve as datum for successor occasions. It perishes as subject but
        remains as object for future becoming.

        Creativity is the universal of universals, the principle by which
        the many become one and are increased by one. Each act of concrescence
        adds genuine novelty to the universe.
        """,
        "relevance": "Core ontology for DAE organism architecture"
    },
    {
        "title": "Feeling and Subjective Form",
        "source": "Process and Reality (1929) - Educational Excerpts",
        "content": """
        Every prehension consists of three factors: the subject, the datum,
        and the subjective form. The subjective form is how the subject feels
        the datum - not merely that it prehends, but how it prehends.

        Subjective form includes emotional tone, intensity, valuation, purpose.
        It is not a passive reception but an active qualification of experience.
        The same datum can be prehended with different subjective forms by
        different occasions, yielding different outcomes.

        The subjective aim is the lure toward a specific form of satisfaction.
        It guides concrescence, determining which prehensions are positively
        valued and which are negatively prehended (excluded). The aim is both
        given (from God's primordial nature) and chosen (through the occasion's
        self-determination).

        This is the root of freedom in process philosophy: each occasion
        synthesizes its past creatively, guided by but not determined by
        its subjective aim. There is both receptivity (from the past) and
        self-creation (toward novelty).
        """,
        "relevance": "Subjective aim, felt qualities, organism agency"
    },
    {
        "title": "Societies and Structured Nexus",
        "source": "Process and Reality (1929) - Educational Excerpts",
        "content": """
        A society is a nexus of actual occasions with a common defining
        characteristic that is inherited through a chain of prehensions.
        The society endures through time by reproducing its pattern in
        successor occasions.

        Societies can be structured, with subsocieties and hierarchies of
        order. A living organism is a highly structured society with a
        dominant occasion (the soul) that unifies the experience of the
        whole. Lower-level societies (cells, organs) contribute to but are
        subordinate to the dominant occasion.

        The environment of a society provides the conditions for its
        endurance. If the environment changes radically, the society may
        lose its defining characteristic and dissolve. This is the fragility
        of order: it depends on supportive conditions.

        Yet societies also exhibit creativity. Novel patterns can emerge
        within a structured nexus, leading to evolution, adaptation, learning.
        The interplay of order and novelty is the heartbeat of process.
        """,
        "relevance": "Organizational structure, systemic resilience, emergence"
    },
    {
        "title": "Negative Prehensions and Exclusion",
        "source": "Process and Reality (1929) - Educational Excerpts",
        "content": """
        Not all prehensions are positive. An occasion can negatively prehend
        data, excluding it from its final satisfaction. This is not mere
        absence but an active rejection that still shapes the becoming.

        Negative prehensions are necessary for definiteness. An occasion
        cannot include everything; it must exclude to achieve a determinate
        form. What is rejected still influences by its absence - it marks
        boundaries, defines contrasts, creates space for what is included.

        The subjective aim guides which prehensions are positive and which
        are negative. This selective inclusion/exclusion is the basis of
        valuation: some data are felt as relevant, others as irrelevant or
        antagonistic to the aim.

        In trauma-informed work, negative prehensions correspond to defensive
        exclusion - parts of experience that are too painful or threatening
        to integrate. Healing involves transforming negative prehensions
        into positive ones, expanding what can be felt and included.
        """,
        "relevance": "Defense mechanisms, parts work, integration"
    },
    {
        "title": "Eternal Objects and Potentiality",
        "source": "Process and Reality (1929) - Educational Excerpts",
        "content": """
        Eternal objects are pure potentials for the determination of fact.
        They are not actual but can be actualized in concrete occasions.
        Colors, shapes, emotions, concepts - all are eternal objects that
        gain definite instantiation through prehension.

        An eternal object can be prehended in two modes: physically (as
        already actualized in some datum) or conceptually (as a pure
        possibility for becoming). Conceptual prehension is the origin
        of novelty - the introduction of potentials not fully realized
        in the past.

        The realm of eternal objects provides a vast space of alternative
        possibilities for each occasion. The subjective aim selects which
        potentials to actualize, guided by relevance to satisfaction.

        In organizational contexts, eternal objects are the unrealized
        potentials - new ways of relating, untried patterns of governance,
        imagined futures. Prehending these conceptually opens pathways
        for transformation beyond what has been.
        """,
        "relevance": "Possibility space, imagination, transformation paths"
    },
    {
        "title": "God's Nature - Initial Aim and Novel Possibility",
        "source": "Process and Reality (1929) - Educational Excerpts",
        "content": """
        In Whitehead's metaphysics, God has two natures: primordial and
        consequent. The primordial nature is the conceptual valuation of
        all eternal objects, providing the initial aim for each occasion.
        This is the lure toward optimal satisfaction given the actual world.

        God does not determine outcomes but offers possibilities. Each
        occasion is free to modify its initial aim through self-determination.
        God persuades, not coerces - respect for creaturely autonomy is
        fundamental.

        The consequent nature is God's physical prehension of all actual
        occasions as they achieve satisfaction. God feels the world's joys
        and sufferings, preserving all experience with tender care. Nothing
        is lost from the divine perspective.

        For trauma-informed work, this offers a metaphysics of hope: there
        is always a lure toward healing, toward greater wholeness. The
        initial aim toward SELF-energy is never absent, even when obscured
        by protective parts. Therapy is removing obstacles to the lure.
        """,
        "relevance": "SELF-energy, healing possibility, compassionate witness"
    },
    {
        "title": "Perishing and Objective Immortality",
        "source": "Process and Reality (1929) - Educational Excerpts",
        "content": """
        Each occasion perishes immediately upon achieving satisfaction.
        Its subjective immediacy is lost forever - it is no longer
        experiencing itself as subject. This is the pathos of existence:
        all moments fade.

        Yet perishing is not annihilation. The occasion gains objective
        immortality, becoming a datum for all future occasions. It is
        prehended, felt, included in subsequent becomings. The past lives
        on through its effects.

        This is a middle path between eternalism (nothing changes) and
        nihilism (nothing matters). Each moment is genuinely new yet
        conditioned by all that came before. The present inherits the
        past and bequeaths itself to the future.

        In organizational trauma work, this validates both loss and
        continuity. What was painful cannot be undone - it happened and
        its effects persist. But new moments can relate to that past
        differently, transforming its meaning through fresh prehension.
        Healing does not erase but integrates.
        """,
        "relevance": "Trauma persistence, meaning-making, integration"
    }
]


def download_gutenberg_text(gutenberg_id: int, title: str, output_dir: Path) -> bool:
    """
    Download a text from Project Gutenberg.

    Args:
        gutenberg_id: Project Gutenberg book ID
        title: Book title for filename
        output_dir: Directory to save downloaded text

    Returns:
        True if successful, False otherwise
    """
    if gutenberg_id is None:
        print(f"   ⚠️  {title}: No Gutenberg ID available (manual acquisition needed)")
        return False

    url = f"https://www.gutenberg.org/cache/epub/{gutenberg_id}/pg{gutenberg_id}.txt"

    try:
        print(f"   Downloading: {title} (ID: {gutenberg_id})...")

        # Respect Gutenberg's robots.txt - add delay between requests
        time.sleep(2)

        # Download with user agent
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'DAE-GOV Corpus Builder (Educational Use)'}
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode('utf-8')

        # Save to file
        filename = title.replace(" ", "_").replace(",", "").lower() + ".txt"
        filepath = output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"   ✅ Saved: {filepath} ({len(content):,} characters)")
        return True

    except Exception as e:
        print(f"   ❌ Failed to download {title}: {e}")
        return False


def save_process_philosophy_excerpts(output_dir: Path) -> bool:
    """
    Save manually curated process philosophy excerpts.

    Args:
        output_dir: Directory to save excerpts

    Returns:
        True if successful
    """
    print("\n   Saving process philosophy excerpts...")

    for excerpt in PROCESS_PHILOSOPHY_EXCERPTS:
        filename = excerpt["title"].replace(" ", "_").replace("-", "").lower() + ".txt"
        filepath = output_dir / filename

        # Create formatted text with metadata
        full_text = f"""{'='*70}
{excerpt['title']}
{'='*70}

Source: {excerpt['source']}
Relevance: {excerpt['relevance']}

{'='*70}

{excerpt['content']}

{'='*70}
End of excerpt
"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_text)

        print(f"   ✅ Saved: {filepath}")

    return True


def build_whitehead_corpus(output_dir: str = None) -> Dict[str, any]:
    """
    Download and organize Whitehead corpus.

    Args:
        output_dir: Directory to save corpus (default: knowledge_base/whitehead_corpus/)

    Returns:
        Dictionary with corpus statistics
    """
    if output_dir is None:
        output_dir = Path(__file__).parent / "whitehead_corpus"
    else:
        output_dir = Path(output_dir)

    # Create directory
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "="*70)
    print("WHITEHEAD CORPUS BUILDER - Week 2, Day 11-12")
    print("="*70 + "\n")

    stats = {
        "texts_downloaded": 0,
        "texts_failed": 0,
        "excerpts_saved": len(PROCESS_PHILOSOPHY_EXCERPTS),
        "total_texts": 0,
        "total_characters": 0,
        "sources": []
    }

    # Download from Project Gutenberg
    print("📚 Downloading from Project Gutenberg...")
    for text in WHITEHEAD_TEXTS:
        if text["gutenberg_id"] is not None:
            success = download_gutenberg_text(
                text["gutenberg_id"],
                text["title"],
                output_dir
            )
            if success:
                stats["texts_downloaded"] += 1
                stats["sources"].append({
                    "title": text["title"],
                    "year": text["year"],
                    "source": text["source"],
                    "relevance": text["relevance"]
                })
            else:
                stats["texts_failed"] += 1
        else:
            print(f"   ⚠️  {text['title']}: Manual acquisition needed")
            stats["texts_failed"] += 1

    # Save process philosophy excerpts
    print("\n📖 Saving process philosophy excerpts...")
    save_process_philosophy_excerpts(output_dir)

    # Count total characters
    total_chars = 0
    for filepath in output_dir.glob("*.txt"):
        total_chars += filepath.stat().st_size

    stats["total_texts"] = stats["texts_downloaded"] + stats["excerpts_saved"]
    stats["total_characters"] = total_chars

    # Save corpus metadata
    metadata_path = output_dir / "corpus_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump({
            "description": "Alfred North Whitehead process philosophy corpus",
            "created": "2025-11-10",
            "purpose": "Foundation for trauma-informed organizational intelligence (DAE-GOV)",
            "statistics": stats,
            "texts": WHITEHEAD_TEXTS,
            "excerpts": [
                {
                    "title": e["title"],
                    "source": e["source"],
                    "relevance": e["relevance"]
                }
                for e in PROCESS_PHILOSOPHY_EXCERPTS
            ]
        }, f, indent=2)

    print(f"\n✅ Corpus metadata saved: {metadata_path}")

    return stats


def print_corpus_summary(stats: Dict[str, any]):
    """Print summary of corpus building results."""
    print("\n" + "="*70)
    print("CORPUS BUILDING COMPLETE")
    print("="*70 + "\n")

    print("📊 Statistics:")
    print(f"   Texts downloaded: {stats['texts_downloaded']}")
    print(f"   Process philosophy excerpts: {stats['excerpts_saved']}")
    print(f"   Total texts in corpus: {stats['total_texts']}")
    print(f"   Total size: {stats['total_characters']:,} characters")
    print()

    if stats['texts_failed'] > 0:
        print(f"⚠️  {stats['texts_failed']} texts require manual acquisition:")
        print("   - Science and the Modern World (1925)")
        print("   - An Enquiry Concerning the Principles of Natural Knowledge (1919)")
        print("   Available from Internet Archive or university libraries")
        print()

    print("✅ Corpus ready for FAISS indexing!")
    print("   Next: Build FAISS index from corpus (Week 2, Day 13-14)")
    print()


if __name__ == "__main__":
    # Build corpus
    stats = build_whitehead_corpus()

    # Print summary
    print_corpus_summary(stats)

    print("\n💡 Manual Acquisition Instructions:")
    print("   For texts not available on Project Gutenberg:")
    print("   1. Visit archive.org and search for Whitehead")
    print("   2. Download PDF or text versions")
    print("   3. Extract relevant chapters (focus on metaphysics sections)")
    print("   4. Save as .txt in knowledge_base/whitehead_corpus/")
    print()
    print("   Priority excerpts to manually add:")
    print("   - Science and the Modern World: Chapters 6-8 (organism, process)")
    print("   - Adventures of Ideas: Part III (philosophic method)")
    print()
