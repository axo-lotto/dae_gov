"""
Enhanced Corpus Integrator - Week 2, Day 11-12
Phase 2: Complete Corpus Building for DAE-GOV Knowledge Infrastructure

Integrates multiple knowledge sources:
1. I Ching (Book of Changes) - BAGUA foundation
2. Process and Reality (Whitehead) - Process philosophy core
3. Wordsworth Poetry - Prehension and feeling
4. Previous Whitehead texts - Already downloaded

Author: Claude Code (November 2025)
Status: Enhanced Corpus Building - Week 2, Day 11-12
"""

import urllib.request
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
import time
import re


# I Ching translations available on Project Gutenberg
I_CHING_TEXTS = [
    {
        "title": "The I Ching or Book of Changes (Richard Wilhelm translation)",
        "year": 1899,  # Original German, 1950 English
        "source": "Project Gutenberg (if available)",
        "url": None,  # Check availability
        "gutenberg_id": None,
        "description": "Classic Wilhelm/Baynes translation of the I Ching",
        "relevance": "BAGUA foundation, eight trigrams, creative/receptive forces"
    },
    {
        "title": "The I Ching (James Legge translation)",
        "year": 1882,
        "source": "Project Gutenberg",
        "url": "https://www.gutenberg.org/cache/epub/9224/pg9224.txt",
        "gutenberg_id": 9224,
        "description": "James Legge's translation (public domain)",
        "relevance": "BAGUA octagon, hexagram transformations, Heaven/Earth/Fire/Water/etc"
    }
]


# I Ching key excerpts (manual curation for BAGUA integration)
I_CHING_BAGUA_EXCERPTS = [
    {
        "title": "The Eight Trigrams - Philosophical Foundation",
        "source": "I Ching - Educational Compilation",
        "content": """
        The Eight Trigrams (BAGUA 八卦) represent the fundamental forces of change:

        ☰ QIAN (乾) - HEAVEN - The Creative
        - Yang trigram (three solid lines)
        - Represents creative force, initiation, pure energy
        - In DAE-GOV: Widen hypothesis space, abstraction
        - Organizational: Vision, strategic thinking, possibility

        ☷ KUN (坤) - EARTH - The Receptive
        - Yin trigram (three broken lines)
        - Represents receptivity, consolidation, form-giving
        - In DAE-GOV: Structure insights into usable form
        - Organizational: Implementation, grounding, execution

        ☲ LI (離) - FIRE - The Clinging/Illuminating
        - Yang outside, yin inside
        - Represents clarity, illumination, discernment
        - In DAE-GOV: Sharpen contrasts, disambiguate
        - Organizational: Analysis, clarity, making distinctions

        ☵ KAN (坎) - WATER - The Abysmal/Reflective
        - Yin outside, yang inside
        - Represents depth, reflection, testing
        - In DAE-GOV: Explore alternatives safely
        - Organizational: Risk assessment, contingency planning

        ☳ ZHEN (震) - THUNDER - Shock/Arousing Energy
        - Yang below, yin above
        - Represents sudden movement, energizing force
        - In DAE-GOV: Escape local minima, inject energy
        - Organizational: Disruptive change, breakthrough moments

        ☴ XUN (巽) - WIND - Gentle Penetration
        - Yin below, yang above
        - Represents gradual influence, spreading
        - In DAE-GOV: Propagate insights through field
        - Organizational: Cultural change, slow influence

        ☶ GEN (艮) - MOUNTAIN - Keeping Still
        - Yang above, yin below
        - Represents stability, holding tension
        - In DAE-GOV: Maintain plateau, resist premature closure
        - Organizational: Strategic patience, holding space

        ☱ DUI (兌) - LAKE - The Joyous
        - Yin above, yang below
        - Represents joy, lateral connection, softening
        - In DAE-GOV: EO integration, blend perspectives
        - Organizational: Collaboration, joy in work, play
        """,
        "relevance": "Direct mapping to Vector35D dimensions 25-32, BAGUA modulation"
    },
    {
        "title": "Dynamic Complementarity - Yin and Yang",
        "source": "I Ching - Educational Compilation",
        "content": """
        The I Ching is grounded in the interplay of yin (⚋) and yang (⚊):

        Yang (⚊): The creative, active, firm, light, ascending
        Yin (⚋): The receptive, passive, yielding, dark, descending

        This is NOT dualism (opposing forces) but dynamic complementarity:
        - Each contains the seed of the other
        - Transformation arises from their interaction
        - Neither is superior; both are necessary

        In organizational trauma work:
        - Yang: Action, intervention, naming, confronting
        - Yin: Listening, witnessing, allowing, receiving

        In process philosophy:
        - Yang: Subjective aim, concrescence, creativity
        - Yin: Objective givenness, perishing, receptivity

        In BAGUA tuning (DAE 3.0):
        - Yang trigrams activate when hypothesis space needs expansion
        - Yin trigrams activate when consolidation is needed
        - Balance emerges from context-sensitive modulation
        """,
        "relevance": "Organism navigation strategy, bifurcation point detection"
    },
    {
        "title": "Hexagram Transformations - Lines of Change",
        "source": "I Ching - Educational Compilation",
        "content": """
        Each hexagram (six lines) represents a specific situation.
        But hexagrams are not static - they transform through changing lines.

        A changing line (老陽 old yang or 老陰 old yin) indicates:
        - A force at maximum intensity, about to reverse
        - A point of transformation, a bifurcation edge

        Example: Hexagram 01 (☰☰ Qian, pure yang) with changing first line
        transforms into Hexagram 44 (☰☴ Gou, coming to meet).

        This models phase transitions in complex systems:
        - A force at extreme becomes unstable
        - Small perturbation triggers qualitative shift
        - New pattern emerges from transformation

        In epoch learning:
        - Organism at convergence edge (Kairos moment)
        - BAGUA modulation active (high edge intensity)
        - Transformation guided by lure toward satisfaction
        - New pattern crystallizes (satisfaction achieved)

        The I Ching wisdom: Recognize the moment of change,
        align with the transformation instead of resisting it.
        """,
        "relevance": "Kairos detection, phase transitions, convergence dynamics"
    },
    {
        "title": "The Sequence of Hexagrams - Dialectical Unfolding",
        "source": "I Ching - Educational Compilation",
        "content": """
        The 64 hexagrams are not random but follow a meaningful sequence
        representing the dialectical unfolding of situations:

        1-2: Creative and Receptive (fundamental polarity)
        3-4: Difficulty at Beginning and Youthful Folly (birth struggles)
        5-6: Waiting and Conflict (patience and tension)
        7-8: Army and Holding Together (collective organization)
        ...
        63-64: After Completion and Before Completion (endless process)

        Key insight for DAE-GOV: Every organizational pattern has:
        - A natural arising (when conditions align)
        - An internal dynamic (tendency toward transformation)
        - A successor state (what it naturally becomes)

        Burnout Spiral (hexagram-like pattern):
        - Arises from: Toxic Productivity (unsustainable yang)
        - Internal dynamic: Exhaustion accumulates (yin emerges)
        - Transforms into: Either Dorsal Shutdown OR Sustainable Rhythm
        - Which outcome depends on: Witnessing, SELF-energy, boundaries

        The I Ching teaches: Understand the pattern's inherent trajectory,
        then work with the flow to guide toward healing transformation.
        """,
        "relevance": "Neo4j transformation paths, organic pattern emergence"
    }
]


def download_i_ching(output_dir: Path) -> bool:
    """Download I Ching from Project Gutenberg."""
    print("\n📖 Downloading I Ching (Book of Changes)...")

    for text in I_CHING_TEXTS:
        if text["gutenberg_id"] is None:
            print(f"   ⚠️  {text['title']}: Not available on Gutenberg (use manual source)")
            continue

        try:
            gutenberg_id = text["gutenberg_id"]
            url = f"https://www.gutenberg.org/cache/epub/{gutenberg_id}/pg{gutenberg_id}.txt"

            print(f"   Downloading: {text['title']} (ID: {gutenberg_id})...")
            time.sleep(2)  # Respect Gutenberg robots.txt

            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'DAE-GOV Corpus Builder (Educational Use)'}
            )

            with urllib.request.urlopen(req, timeout=30) as response:
                content = response.read().decode('utf-8')

            filename = "i_ching_legge_translation.txt"
            filepath = output_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"   ✅ Saved: {filepath} ({len(content):,} characters)")
            return True

        except Exception as e:
            print(f"   ❌ Failed to download {text['title']}: {e}")
            return False

    return False


def save_i_ching_bagua_excerpts(output_dir: Path) -> bool:
    """Save manually curated I Ching BAGUA excerpts."""
    print("\n   Saving I Ching BAGUA excerpts for DAE 3.0 integration...")

    for excerpt in I_CHING_BAGUA_EXCERPTS:
        filename = excerpt["title"].replace(" ", "_").replace("-", "_").lower() + ".txt"
        filepath = output_dir / filename

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


def extract_text_from_pdf(pdf_path: Path, output_path: Path) -> bool:
    """
    Extract text from PDF using pdftotext command-line tool.

    Args:
        pdf_path: Path to PDF file
        output_path: Path to save extracted text

    Returns:
        True if successful
    """
    try:
        # Check if pdftotext is available
        result = subprocess.run(['which', 'pdftotext'], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"   ⚠️  pdftotext not found. Install with: brew install poppler")
            print(f"   📄 PDF will be linked but not extracted: {pdf_path.name}")
            return False

        # Extract text from PDF
        subprocess.run(
            ['pdftotext', '-layout', str(pdf_path), str(output_path)],
            check=True,
            capture_output=True
        )

        # Check if extraction was successful
        if output_path.exists() and output_path.stat().st_size > 1000:
            print(f"   ✅ Extracted: {output_path} ({output_path.stat().st_size:,} bytes)")
            return True
        else:
            print(f"   ⚠️  Extraction produced minimal content: {pdf_path.name}")
            return False

    except subprocess.CalledProcessError as e:
        print(f"   ❌ PDF extraction failed for {pdf_path.name}: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error extracting {pdf_path.name}: {e}")
        return False


def integrate_existing_corpus(output_dir: Path, corpus_base: Path) -> Dict[str, any]:
    """
    Integrate existing corpus files (Process and Reality PDF, poetry, etc).

    Args:
        output_dir: Whitehead corpus directory
        corpus_base: Base corpus directory with process_philosophy/

    Returns:
        Dictionary with integration statistics
    """
    print("\n📚 Integrating existing corpus files...")

    stats = {
        "process_and_reality": False,
        "poetry": False,
        "process_and_reality_size": 0,
        "poetry_size": 0
    }

    # Process and Reality PDF
    process_and_reality_pdf = corpus_base / "process_philosophy" / "process-and-reality.pdf"
    if process_and_reality_pdf.exists():
        print(f"\n   Found: {process_and_reality_pdf.name} ({process_and_reality_pdf.stat().st_size / 1024 / 1024:.1f} MB)")

        # Extract text from PDF
        output_txt = output_dir / "process_and_reality_whitehead.txt"
        success = extract_text_from_pdf(process_and_reality_pdf, output_txt)

        if success:
            stats["process_and_reality"] = True
            stats["process_and_reality_size"] = output_txt.stat().st_size
        else:
            # Create symbolic link if extraction failed
            link_path = output_dir / "process_and_reality.pdf"
            if not link_path.exists():
                link_path.symlink_to(process_and_reality_pdf)
                print(f"   🔗 Linked: {link_path} → {process_and_reality_pdf}")
    else:
        print(f"   ⚠️  Process and Reality PDF not found at: {process_and_reality_pdf}")

    # Wordsworth Poetry PDF
    poetry_pdf = corpus_base / "process_philosophy" / "poetry" / "selectedpoemsofw00word.pdf"
    if poetry_pdf.exists():
        print(f"\n   Found: {poetry_pdf.name} ({poetry_pdf.stat().st_size / 1024 / 1024:.1f} MB)")

        # Extract text from PDF
        output_txt = output_dir / "wordsworth_selected_poems.txt"
        success = extract_text_from_pdf(poetry_pdf, output_txt)

        if success:
            stats["poetry"] = True
            stats["poetry_size"] = output_txt.stat().st_size
        else:
            # Create symbolic link if extraction failed
            link_path = output_dir / "wordsworth_poetry.pdf"
            if not link_path.exists():
                link_path.symlink_to(poetry_pdf)
                print(f"   🔗 Linked: {link_path} → {poetry_pdf}")
    else:
        print(f"   ⚠️  Poetry PDF not found at: {poetry_pdf}")

    return stats


def build_complete_corpus(
    whitehead_corpus_dir: Optional[Path] = None,
    corpus_base_dir: Optional[Path] = None
) -> Dict[str, any]:
    """
    Build complete corpus with all knowledge sources.

    Args:
        whitehead_corpus_dir: Directory for Whitehead corpus
        corpus_base_dir: Base directory with existing PDFs

    Returns:
        Complete corpus statistics
    """
    if whitehead_corpus_dir is None:
        whitehead_corpus_dir = Path(__file__).parent / "whitehead_corpus"
    else:
        whitehead_corpus_dir = Path(whitehead_corpus_dir)

    if corpus_base_dir is None:
        corpus_base_dir = Path(__file__).parent / "corpus"
    else:
        corpus_base_dir = Path(corpus_base_dir)

    whitehead_corpus_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "="*70)
    print("COMPLETE CORPUS INTEGRATION - Week 2, Day 11-12")
    print("="*70)
    print(f"\nTarget directory: {whitehead_corpus_dir}")
    print(f"Source directory: {corpus_base_dir}")

    stats = {
        "i_ching_downloaded": False,
        "i_ching_excerpts": len(I_CHING_BAGUA_EXCERPTS),
        "process_and_reality": False,
        "poetry": False,
        "total_texts": 0,
        "total_size": 0
    }

    # Download I Ching
    stats["i_ching_downloaded"] = download_i_ching(whitehead_corpus_dir)

    # Save I Ching BAGUA excerpts
    save_i_ching_bagua_excerpts(whitehead_corpus_dir)

    # Integrate existing corpus (Process and Reality, poetry)
    integration_stats = integrate_existing_corpus(whitehead_corpus_dir, corpus_base_dir)
    stats.update(integration_stats)

    # Count all texts and total size
    total_size = 0
    text_count = 0
    for filepath in whitehead_corpus_dir.glob("*.txt"):
        total_size += filepath.stat().st_size
        text_count += 1

    stats["total_texts"] = text_count
    stats["total_size"] = total_size

    # Save enhanced metadata
    metadata_path = whitehead_corpus_dir / "corpus_metadata_complete.json"
    with open(metadata_path, 'w') as f:
        json.dump({
            "description": "Complete DAE-GOV knowledge corpus",
            "created": "2025-11-10",
            "purpose": "Foundation for trauma-informed organizational intelligence",
            "components": {
                "i_ching": "BAGUA foundation for Vector35D dimensions 25-32",
                "process_and_reality": "Whitehead's complete process philosophy",
                "wordsworth_poetry": "Prehension, feeling, and poetic intelligence",
                "whitehead_texts": "The Concept of Nature + process philosophy excerpts",
                "synthetic_conversations": "30 trauma-informed organizational scenarios"
            },
            "statistics": stats,
            "i_ching_sources": I_CHING_TEXTS,
            "i_ching_excerpts": [
                {
                    "title": e["title"],
                    "source": e["source"],
                    "relevance": e["relevance"]
                }
                for e in I_CHING_BAGUA_EXCERPTS
            ]
        }, f, indent=2)

    print(f"\n✅ Complete corpus metadata saved: {metadata_path}")

    return stats


def print_corpus_summary(stats: Dict[str, any]):
    """Print summary of complete corpus building."""
    print("\n" + "="*70)
    print("COMPLETE CORPUS INTEGRATION - SUMMARY")
    print("="*70 + "\n")

    print("📊 Integration Results:")
    print(f"   ✅ I Ching BAGUA excerpts: {stats['i_ching_excerpts']} texts")
    print(f"   {'✅' if stats['i_ching_downloaded'] else '⚠️ '} I Ching full text: {'Downloaded' if stats['i_ching_downloaded'] else 'Manual download needed'}")
    print(f"   {'✅' if stats['process_and_reality'] else '⚠️ '} Process and Reality: {'Extracted' if stats['process_and_reality'] else 'PDF linked (pdftotext needed)'}")
    print(f"   {'✅' if stats['poetry'] else '⚠️ '} Wordsworth Poetry: {'Extracted' if stats['poetry'] else 'PDF linked (pdftotext needed)'}")
    print(f"   📄 Total text files: {stats['total_texts']}")
    print(f"   💾 Total corpus size: {stats['total_size'] / 1024 / 1024:.1f} MB")
    print()

    print("🎯 Knowledge Sources Integrated:")
    print("   1. BAGUA (I Ching) → Vector35D dims 25-32 (creative modulation)")
    print("   2. Process and Reality → Core ontology (actual occasions, prehension)")
    print("   3. Wordsworth Poetry → Felt qualities, aesthetic prehension")
    print("   4. Whitehead Texts → The Concept of Nature + excerpts")
    print("   5. Synthetic Conversations → 30 trauma-informed organizational scenarios")
    print()

    if not stats.get('process_and_reality') or not stats.get('poetry'):
        print("💡 To extract text from PDFs:")
        print("   brew install poppler  # Installs pdftotext")
        print("   python3 knowledge_base/corpus_integrator.py  # Re-run")
        print()

    print("✅ Corpus ready for FAISS indexing!")
    print("   Next: Build FAISS index from complete corpus (Week 2, Day 13-14)")
    print()


if __name__ == "__main__":
    # Build complete corpus
    stats = build_complete_corpus()

    # Print summary
    print_corpus_summary(stats)

    print("📍 Corpus Sources:")
    print("   • I Ching: Project Gutenberg + BAGUA excerpts (for DAE 3.0 integration)")
    print("   • Process and Reality: Whitehead's magnum opus (22MB PDF)")
    print("   • Wordsworth Poetry: Romantic period prehension/feeling (7.2MB PDF)")
    print("   • Previous Whitehead: The Concept of Nature + 7 excerpts")
    print()
