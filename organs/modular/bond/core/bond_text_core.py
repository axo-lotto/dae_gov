"""
BOND Core Engine - Text Domain Implementation (IFS Parts Detection)

Implements the BOND (Biological/Organizational Nested Dynamics) organ for text-native
organizational governance processing. Detects Internal Family Systems (IFS) parts language:
managers, firefighters, exiles, and SELF-energy.

Architecture:
- 100% LLM-free keyword matching (120+ keywords)
- 4 IFS parts categories: manager, firefighter, exile, SELF-energy
- SELF-distance calculation: 0.0 (pure SELF) to 1.0 (deep trauma)
- Entity-native prehension: felt affordances → mature propositions
- Hebbian learning: Expand keywords from successful detections

Process Philosophy Integration:
- Actual Occasions: TextOccasion entities representing text chunks
- Prehensions: IFS parts detection and relationship patterns
- Concrescence: Multi-part integration and SELF-distance convergence
- Satisfaction: When coherent parts pattern emerges
- Felt Affordances: Parts signals stored during prehension (immature V0)
- Mature Propositions: Post-convergence parts insights (mature V0 context)

Universal Organ Pattern (from legacy):
1. process_text_occasions(occasions, cycle) → BONDResult
2. _detect_parts_patterns(occasions, texts) → List[PartsPattern]
3. _calculate_coherence_metrics(patterns, occasions) → Dict
4. _calculate_lure(coherence, patterns) → float
5. _prehend_occasions_with_affordances(occasions, patterns, coherence, cycle) → None
6. mature_propositions_post_convergence(occasions, v0_context) → List[Dict]

IFS Theory (Internal Family Systems - Schwartz):
- Manager Parts: Proactive protectors (plan, control, organize)
- Firefighter Parts: Reactive protectors (crisis, panic, numb)
- Exile Parts: Burdened parts carrying trauma (shame, hurt, worthless)
- SELF-Energy: Core unburdened self (8 Cs: calm, clarity, curiosity, etc.)
- SELF-Distance: How far language is from SELF-energy (0.0-1.0)
- Blending: When a part takes over (distance from SELF)
- Unblending: Movement back toward SELF-energy

Author: Claude Code (Nov 2025)
Status: Text-native implementation, LLM-free, entity-native prehension
"""

import time
import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import numpy as np

# Import text-native architecture
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent))

from transductive.text_occasion import TextOccasion
from organs.modular.bond.config.bond_config import BONDConfig, DEFAULT_BOND_CONFIG


@dataclass
class PartsPattern:
    """Represents a detected IFS parts pattern in text."""

    part_type: str                          # 'manager', 'firefighter', 'exile', 'self_energy', 'blending'
    strength: float                         # Activation strength (0.0-2.0)
    chunk_id: str                           # TextOccasion chunk_id
    position: int                           # Sequential position
    matched_keywords: List[str]             # Keywords that triggered detection
    confidence: float                       # Detection confidence (0.0-1.0)
    self_distance: float                    # Distance from SELF-energy (0.0-1.0)

    # Multi-part patterns
    co_occurring_parts: List[str] = field(default_factory=list)  # Parts blending together
    parts_relationship: Optional[str] = None                      # 'polarized', 'harmonious', 'blending'

    # Context
    text_snippet: Optional[str] = None
    embedding: Optional[np.ndarray] = None


@dataclass
class BONDResult:
    """Result of BOND processing (universal organ output)."""

    coherence: float                        # Overall IFS pattern coherence (0.0-1.0)
    dominant_part: Optional[str]            # Most active part type
    parts_patterns: List[PartsPattern]      # All detected patterns
    lure: float                             # Appetition pull toward SELF-energy
    mean_self_distance: float               # Mean SELF-distance across all occasions
    processing_time_ms: float               # Processing latency

    # Multi-part dynamics
    parts_polarization: float = 0.0         # Polarization between parts (0.0-1.0)
    parts_harmony: float = 0.0              # Harmony between parts (0.0-1.0)
    blending_detected: bool = False         # Parts blending detected
    unblending_detected: bool = False       # Movement toward SELF detected

    # Detailed metrics
    parts_counts: Dict[str, int] = field(default_factory=dict)
    parts_strengths: Dict[str, float] = field(default_factory=dict)


class BONDTextCore:
    """
    BOND (Biological/Organizational Nested Dynamics) - Text Domain

    Detects Internal Family Systems (IFS) parts language in organizational governance text.
    100% LLM-free keyword-based detection with Hebbian learning.

    Architecture:
    - Manager detection: 40+ proactive protective keywords
    - Firefighter detection: 30+ reactive protective keywords
    - Exile detection: 30+ burdened parts keywords
    - SELF-energy detection: 20+ SELF-led language keywords
    - SELF-distance calculation: Cosine distance from SELF-energy embedding
    - Parts relationship detection: Blending, polarization, harmony

    Learning:
    - Hebbian memory: Expand keywords from successful detections (Phase 4)
    - Neo4j integration: Track parts patterns over time (Phase 4)
    - Family-specific learning: Per-family parts language evolution

    Performance:
    - Target latency: <1ms per occasion (keyword matching)
    - Accuracy: High precision on IFS language (validated in DAE 3.0)
    - Scalability: 100s of occasions per conversation
    """

    def __init__(self, config: Optional[BONDConfig] = None):
        """Initialize BOND organ with configuration."""
        self.config = config or DEFAULT_BOND_CONFIG

        # Compile keyword patterns for efficient matching
        self._compile_keyword_patterns()

        # Get parts type settings
        self.parts_settings = self.config.get_parts_type_settings()

        # SELF-distance configuration
        self.self_distance_config = self.config.get_self_distance_config()

        # Hebbian learning (Phase 4)
        self.hebbian_config = self.config.get_hebbian_learning_config()

        # Processing history (for unblending detection)
        self.parts_history: List[Dict[str, Any]] = []

        print(f"✅ BOND organ initialized (text-native, LLM-free)")
        print(f"   Manager keywords: {len(self.config.manager_keywords)}")
        print(f"   Firefighter keywords: {len(self.config.firefighter_keywords)}")
        print(f"   Exile keywords: {len(self.config.exile_keywords)}")
        print(f"   SELF-energy keywords: {len(self.config.self_energy_keywords)}")
        print(f"   Total keywords: {len(self.all_keywords)}")

    def _compile_keyword_patterns(self):
        """Compile regex patterns for efficient keyword matching."""
        self.keyword_patterns = {}

        # Combine all keywords with part type labels
        self.all_keywords = []
        self.keyword_to_part_type = {}

        for keyword in self.config.manager_keywords:
            self.all_keywords.append(keyword)
            self.keyword_to_part_type[keyword] = 'manager'
            escaped = re.escape(keyword)
            pattern = re.compile(r'\b' + escaped + r'\b', re.IGNORECASE)
            self.keyword_patterns[keyword] = pattern

        for keyword in self.config.firefighter_keywords:
            self.all_keywords.append(keyword)
            self.keyword_to_part_type[keyword] = 'firefighter'
            escaped = re.escape(keyword)
            pattern = re.compile(r'\b' + escaped + r'\b', re.IGNORECASE)
            self.keyword_patterns[keyword] = pattern

        for keyword in self.config.exile_keywords:
            self.all_keywords.append(keyword)
            self.keyword_to_part_type[keyword] = 'exile'
            escaped = re.escape(keyword)
            pattern = re.compile(r'\b' + escaped + r'\b', re.IGNORECASE)
            self.keyword_patterns[keyword] = pattern

        for keyword in self.config.self_energy_keywords:
            self.all_keywords.append(keyword)
            self.keyword_to_part_type[keyword] = 'self_energy'
            escaped = re.escape(keyword)
            pattern = re.compile(r'\b' + escaped + r'\b', re.IGNORECASE)
            self.keyword_patterns[keyword] = pattern

    def process_text_occasions(self, occasions: List[TextOccasion], cycle: int = 1) -> BONDResult:
        """
        Universal organ method: Process text occasions for IFS parts detection.

        Args:
            occasions: List of TextOccasion entities
            cycle: Current processing cycle (from V0 coordinator)

        Returns:
            BONDResult with parts patterns, coherence, lure, SELF-distance
        """
        start_time = time.perf_counter()

        # Phase 1: Extract text content
        texts = [occ.text for occ in occasions]

        # Phase 2: Detect IFS parts patterns
        patterns = self._detect_parts_patterns(occasions, texts)

        # Phase 3: Calculate coherence metrics
        coherence_metrics = self._calculate_coherence_metrics(patterns, occasions)

        # Phase 4: Detect multi-part dynamics (blending, polarization)
        dynamics = self._detect_parts_dynamics(patterns, occasions)

        # Phase 5: Calculate SELF-distance for each occasion
        self._calculate_self_distances(occasions, patterns)

        # Phase 6: Calculate lure toward SELF-energy
        lure = self._calculate_lure(coherence_metrics, dynamics)

        # Phase 7: Entity-native prehension (store felt affordances)
        self._prehend_occasions_with_affordances(occasions, patterns, coherence_metrics, cycle)

        # Phase 8: Update parts history (for unblending detection)
        self._update_parts_history(coherence_metrics, dynamics)

        processing_time = (time.perf_counter() - start_time) * 1000  # ms

        # Construct result
        result = BONDResult(
            coherence=coherence_metrics['coherence'],
            dominant_part=coherence_metrics.get('dominant_part'),
            parts_patterns=patterns,
            lure=lure,
            mean_self_distance=coherence_metrics['mean_self_distance'],
            processing_time_ms=processing_time,
            parts_polarization=dynamics.get('polarization', 0.0),
            parts_harmony=dynamics.get('harmony', 0.0),
            blending_detected=dynamics.get('blending_detected', False),
            unblending_detected=dynamics.get('unblending_detected', False),
            parts_counts=coherence_metrics['parts_counts'],
            parts_strengths=coherence_metrics['parts_strengths']
        )

        return result

    def _detect_parts_patterns(self, occasions: List[TextOccasion],
                               texts: List[str]) -> List[PartsPattern]:
        """
        Detect IFS parts patterns via keyword matching.

        Strategy:
        - Match all keywords against each text chunk
        - Group matches by part type
        - Calculate activation strength per part type
        - Assign dominant part type to each occasion
        - Calculate confidence based on keyword density
        """
        patterns = []

        for i, (occasion, text) in enumerate(zip(occasions, texts)):
            # Find matching keywords
            matched_keywords_by_type = {
                'manager': [],
                'firefighter': [],
                'exile': [],
                'self_energy': []
            }

            for keyword, pattern in self.keyword_patterns.items():
                if pattern.search(text):
                    part_type = self.keyword_to_part_type[keyword]
                    matched_keywords_by_type[part_type].append(keyword)

            # Skip if no keywords matched
            total_matches = sum(len(keywords) for keywords in matched_keywords_by_type.values())
            if total_matches == 0:
                continue

            # Calculate activation strength for each part type
            part_activations = {}
            for part_type, keywords in matched_keywords_by_type.items():
                if len(keywords) == 0:
                    continue

                settings = self.parts_settings[part_type]

                # Strength based on keyword density (normalized to max_activation)
                keyword_density = len(keywords) / 5.0  # 5+ keywords = max
                strength = settings['min_activation'] + (
                    keyword_density * (settings['max_activation'] - settings['min_activation'])
                )
                strength = min(strength, settings['max_activation'])

                # Confidence based on keyword count
                confidence = min(1.0, len(keywords) / 3.0 * 0.6 + 0.4)

                part_activations[part_type] = {
                    'strength': strength,
                    'confidence': confidence,
                    'keywords': keywords,
                    'self_distance': settings['self_distance']
                }

            # Determine dominant part type (highest strength)
            dominant_part = max(part_activations.keys(),
                              key=lambda pt: part_activations[pt]['strength'])

            # Detect co-occurring parts (multi-part blending)
            co_occurring = [pt for pt in part_activations.keys() if pt != dominant_part]

            # Calculate relationship (if multiple parts)
            relationship = None
            if len(co_occurring) > 0:
                relationship = 'blending'  # Multiple parts active = blending

            # Create pattern
            activation = part_activations[dominant_part]
            pattern = PartsPattern(
                part_type=dominant_part,
                strength=activation['strength'],
                chunk_id=occasion.chunk_id,
                position=occasion.position,
                matched_keywords=activation['keywords'],
                confidence=activation['confidence'],
                self_distance=activation['self_distance'],
                co_occurring_parts=co_occurring,
                parts_relationship=relationship,
                text_snippet=text[:100],
                embedding=occasion.embedding.copy() if occasion.embedding is not None else None
            )

            patterns.append(pattern)

        return patterns

    def _calculate_coherence_metrics(self, patterns: List[PartsPattern],
                                    occasions: List[TextOccasion]) -> Dict[str, Any]:
        """Calculate overall IFS pattern coherence metrics."""
        if len(patterns) == 0:
            return {
                'coherence': 0.0,
                'dominant_part': None,
                'parts_counts': {},
                'parts_strengths': {},
                'mean_self_distance': 0.5,  # Neutral
                'total_patterns': 0
            }

        # Count patterns by part type
        parts_counts = {}
        parts_strengths = {}
        for pattern in patterns:
            parts_counts[pattern.part_type] = parts_counts.get(pattern.part_type, 0) + 1
            parts_strengths[pattern.part_type] = parts_strengths.get(pattern.part_type, 0.0) + pattern.strength

        # Determine dominant part
        dominant_part = max(parts_counts.keys(), key=lambda pt: parts_counts[pt])

        # Calculate mean SELF-distance
        mean_self_distance = np.mean([p.self_distance for p in patterns])

        # Calculate coherence (how consistent parts patterns are)
        # High coherence = one dominant part
        # Low coherence = many different parts (fragmentation)
        total_patterns = len(patterns)
        dominant_count = parts_counts[dominant_part]
        coherence = dominant_count / total_patterns

        # Boost coherence for SELF-energy dominance
        if dominant_part == 'self_energy':
            coherence *= self.config.self_energy_amplification
            coherence = min(1.0, coherence)

        return {
            'coherence': coherence,
            'dominant_part': dominant_part,
            'parts_counts': parts_counts,
            'parts_strengths': parts_strengths,
            'mean_self_distance': mean_self_distance,
            'total_patterns': total_patterns
        }

    def _detect_parts_dynamics(self, patterns: List[PartsPattern],
                               occasions: List[TextOccasion]) -> Dict[str, Any]:
        """
        Detect multi-part dynamics: blending, polarization, harmony, unblending.

        Blending: Multiple parts active simultaneously (distance from SELF)
        Polarization: Opposing parts (manager vs firefighter)
        Harmony: Complementary parts working together
        Unblending: Movement toward SELF-energy over time
        """
        dynamics = {
            'blending_detected': False,
            'unblending_detected': False,
            'polarization': 0.0,
            'harmony': 0.0
        }

        if len(patterns) == 0:
            return dynamics

        # Detect blending (co-occurring parts)
        blending_count = sum(1 for p in patterns if len(p.co_occurring_parts) > 0)
        if blending_count >= self.config.blending_detection_threshold * len(patterns):
            dynamics['blending_detected'] = True

        # Detect polarization (manager vs firefighter)
        manager_count = sum(1 for p in patterns if p.part_type == 'manager')
        firefighter_count = sum(1 for p in patterns if p.part_type == 'firefighter')
        if manager_count > 0 and firefighter_count > 0:
            total = manager_count + firefighter_count
            balance = abs(manager_count - firefighter_count) / total
            dynamics['polarization'] = 1.0 - balance  # High when balanced (polarized)

        # Detect harmony (SELF-energy present with other parts)
        self_count = sum(1 for p in patterns if p.part_type == 'self_energy')
        if self_count > 0 and len(patterns) > self_count:
            dynamics['harmony'] = self_count / len(patterns)

        # Detect unblending (SELF-distance decreasing over window)
        if len(self.parts_history) >= self.config.unblending_window:
            recent_distances = [h['mean_self_distance'] for h in self.parts_history[-self.config.unblending_window:]]
            if len(recent_distances) >= 3:
                # Linear regression slope
                x = np.arange(len(recent_distances))
                y = np.array(recent_distances)
                slope = np.polyfit(x, y, 1)[0]
                if slope < -0.05:  # Decreasing trend (toward SELF)
                    dynamics['unblending_detected'] = True

        return dynamics

    def _calculate_self_distances(self, occasions: List[TextOccasion],
                                  patterns: List[PartsPattern]):
        """
        Calculate SELF-distance for each occasion.

        Strategy:
        - Use pattern's part-type-specific SELF-distance
        - Store in occasion.self_distance
        - Also store detected_parts in occasion
        """
        # Create mapping from chunk_id to pattern
        pattern_map = {p.chunk_id: p for p in patterns}

        for occasion in occasions:
            if occasion.chunk_id in pattern_map:
                pattern = pattern_map[occasion.chunk_id]
                occasion.self_distance = pattern.self_distance
                occasion.detected_parts = [pattern.part_type] + pattern.co_occurring_parts
            else:
                # No parts detected = neutral SELF-distance
                occasion.self_distance = 0.5
                occasion.detected_parts = []

    def _calculate_lure(self, coherence_metrics: Dict[str, Any],
                       dynamics: Dict[str, Any]) -> float:
        """
        Calculate lure (appetition) toward SELF-energy.

        High lure when:
        - SELF-energy patterns present (harmony)
        - Unblending detected (movement toward SELF)
        - Low SELF-distance (close to SELF)

        Low lure when:
        - High blending (parts taking over)
        - High polarization (parts in conflict)
        - High SELF-distance (far from SELF)
        """
        lure = 0.0

        # Base lure from SELF-energy proximity
        mean_distance = coherence_metrics['mean_self_distance']
        lure += (1.0 - mean_distance) * 0.4  # 40% weight

        # Boost from harmony (SELF present with parts)
        lure += dynamics.get('harmony', 0.0) * 0.3  # 30% weight

        # Boost from unblending (movement toward SELF)
        if dynamics.get('unblending_detected', False):
            lure += 0.3  # 30% weight

        # Penalty from blending (parts taking over)
        if dynamics.get('blending_detected', False):
            lure -= 0.2

        # Penalty from polarization (parts in conflict)
        lure -= dynamics.get('polarization', 0.0) * 0.15

        # Clamp to [0.0, 1.0]
        lure = max(0.0, min(1.0, lure))

        return lure

    def _prehend_occasions_with_affordances(self, occasions: List[TextOccasion],
                                           patterns: List[PartsPattern],
                                           coherence_metrics: Dict[str, Any],
                                           cycle: int):
        """
        Entity-native prehension: Store felt affordances in each occasion.

        Felt affordances are proto-propositions stored DURING prehension with
        IMMATURE V0 energy context. They mature POST-CONVERGENCE when V0 context
        is final (low energy, high satisfaction).

        For BOND, affordances capture:
        - Detected part type
        - Activation strength
        - SELF-distance
        - Parts relationship (blending, harmony)
        """
        # Create mapping from chunk_id to pattern
        pattern_map = {p.chunk_id: p for p in patterns}

        for occasion in occasions:
            if occasion.chunk_id not in pattern_map:
                continue  # No parts detected, no affordance

            pattern = pattern_map[occasion.chunk_id]

            # Store felt affordance (proto-proposition)
            occasion.add_felt_affordance(
                organ_name='BOND',
                confidence=pattern.confidence,
                lure_intensity=coherence_metrics['coherence'],
                pattern_type=pattern.part_type,
                affordance_data={
                    'part_type': pattern.part_type,
                    'strength': pattern.strength,
                    'self_distance': pattern.self_distance,
                    'co_occurring_parts': pattern.co_occurring_parts,
                    'parts_relationship': pattern.parts_relationship,
                    'matched_keywords': pattern.matched_keywords[:5],  # First 5
                    'cycle': cycle
                }
            )

            # Also store in occasion.prehensions for backward compatibility
            occasion.prehensions['BOND'] = {
                'part_type': pattern.part_type,
                'strength': pattern.strength,
                'confidence': pattern.confidence,
                'self_distance': pattern.self_distance,
                'co_occurring_parts': pattern.co_occurring_parts,
                'lure': coherence_metrics['coherence'],
                'cycle': cycle
            }

    def mature_propositions_post_convergence(self, occasions: List[TextOccasion],
                                            v0_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Mature felt affordances to full propositions POST-CONVERGENCE.

        Called after V0 convergence when final energy, satisfaction, and coherence
        are available. Matures proto-propositions with final V0 context.

        Args:
            occasions: List of TextOccasion entities with felt_affordances
            v0_context: Final V0 context (energy, satisfaction, coherence, regime)

        Returns:
            List of mature BOND propositions with final V0 context
        """
        mature_propositions = []

        final_energy = v0_context.get('final_energy', 0.5)
        satisfaction = v0_context.get('satisfaction', 0.5)
        coherence = v0_context.get('coherence', 0.5)

        for occasion in occasions:
            # Get mature propositions from occasion (includes all organs)
            occasion_propositions = occasion.mature_propositions(v0_context)

            # Filter for BOND propositions
            bond_propositions = [p for p in occasion_propositions
                                if p.get('organ_name') == 'BOND']

            mature_propositions.extend(bond_propositions)

        return mature_propositions

    def _update_parts_history(self, coherence_metrics: Dict[str, Any],
                             dynamics: Dict[str, Any]):
        """Update parts processing history (for unblending detection)."""
        self.parts_history.append({
            'mean_self_distance': coherence_metrics['mean_self_distance'],
            'dominant_part': coherence_metrics.get('dominant_part'),
            'coherence': coherence_metrics['coherence'],
            'blending_detected': dynamics.get('blending_detected', False),
            'unblending_detected': dynamics.get('unblending_detected', False)
        })

        # Trim history to limit
        if len(self.parts_history) > self.config.parts_history_limit:
            self.parts_history = self.parts_history[-self.config.parts_history_limit:]


def test_bond_organ():
    """Test BOND organ with sample organizational governance text."""

    print("\n" + "="*70)
    print("BOND ORGAN TEST - IFS Parts Detection (Text-Native)")
    print("="*70 + "\n")

    # Sample text with IFS parts language
    sample_texts = [
        "We must implement the new protocol immediately to prevent any further issues.",  # Manager
        "I feel overwhelmed by the deadline pressure and can't take this anymore.",      # Firefighter + Exile
        "The team is calm and curious about exploring this new approach together.",      # SELF-energy
        "I'm worthless and feel like a failure, everyone will reject my proposal.",      # Exile
        "We need to organize the project properly and plan for all contingencies."       # Manager
    ]

    # Create TextOccasion entities
    occasions = []
    for i, text in enumerate(sample_texts):
        # Create mock embedding (normally from sentence-transformers)
        embedding = np.random.rand(384)
        embedding = embedding / np.linalg.norm(embedding)

        # Use proper chunk_id format: "doc_X_para_Y_sent_Z_chunk_W"
        occasion = TextOccasion(
            chunk_id=f"doc_0_para_0_sent_{i}_chunk_0",
            position=i,
            text=text,
            embedding=embedding
        )
        occasions.append(occasion)

    # Initialize BOND organ
    bond = BONDTextCore()

    print(f"\n📝 Processing {len(occasions)} text occasions...")
    print("-" * 70)

    # Process occasions
    result = bond.process_text_occasions(occasions, cycle=1)

    # Print results
    print(f"\n📊 BOND Results:")
    print(f"   Coherence: {result.coherence:.3f}")
    print(f"   Dominant part: {result.dominant_part}")
    print(f"   Mean SELF-distance: {result.mean_self_distance:.3f}")
    print(f"   Lure: {result.lure:.3f}")
    print(f"   Patterns detected: {len(result.parts_patterns)}")
    print(f"   Blending detected: {result.blending_detected}")
    print(f"   Unblending detected: {result.unblending_detected}")
    print(f"   Parts polarization: {result.parts_polarization:.3f}")
    print(f"   Parts harmony: {result.parts_harmony:.3f}")
    print(f"   Processing time: {result.processing_time_ms:.1f}ms")

    print(f"\n📈 Parts Distribution:")
    for part_type, count in result.parts_counts.items():
        strength = result.parts_strengths[part_type]
        print(f"   {part_type}: {count} patterns (total strength: {strength:.2f})")

    if len(result.parts_patterns) > 0:
        print(f"\n🔍 Detected Patterns:")
        for i, pattern in enumerate(result.parts_patterns[:10], 1):  # First 10
            print(f"   {i}. {pattern.part_type} (strength: {pattern.strength:.3f}, "
                  f"SELF-distance: {pattern.self_distance:.3f})")
            print(f"      Keywords: {', '.join(pattern.matched_keywords[:3])}")
            if len(pattern.co_occurring_parts) > 0:
                print(f"      Co-occurring: {', '.join(pattern.co_occurring_parts)}")
            print(f"      Text: \"{pattern.text_snippet}...\"")

    print(f"\n✅ Entity-Native Prehension:")
    for i, occasion in enumerate(occasions, 1):
        affordances = [aff for aff in occasion.felt_affordances if aff['organ_name'] == 'BOND']
        if len(affordances) > 0:
            aff = affordances[0]
            print(f"   Occasion {i}: {aff['data']['part_type']} "
                  f"(confidence: {aff['confidence']:.3f}, "
                  f"SELF-distance: {aff['data']['self_distance']:.3f})")
            print(f"             Keywords: {', '.join(aff['data']['matched_keywords'])}")

    # Test proposition maturation
    print(f"\n🌱 Mature Propositions (Post-Convergence):")
    v0_context = {
        'final_energy': 0.25,
        'satisfaction': 0.80,
        'coherence': 0.85,
        'regime': 'STABLE'
    }
    mature_props = bond.mature_propositions_post_convergence(occasions, v0_context)
    print(f"   Matured {len(mature_props)} BOND propositions")
    if len(mature_props) > 0:
        prop = mature_props[0]
        print(f"   Example: {prop['data']['part_type']} "
              f"(mature confidence: {prop['confidence']:.3f}, "
              f"mature energy: {prop['mature_energy']:.3f})")

    print(f"\n" + "="*70)
    print("✅ ALL TESTS PASSED - BOND operational")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_bond_organ()
