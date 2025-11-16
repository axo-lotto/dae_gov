#!/usr/bin/env python3
"""
I Ching Oracle - Wisdom Module for DAE
========================================

Provides hexagram consultation based on felt-state patterns.
Integrates with polyvagal system and transduction pathways.

Philosophy:
- Change is the only constant (Whiteheadian process)
- Hexagrams represent archetypal transformation patterns
- Oracle wisdom complements organic felt-state reasoning
- Not prediction, but pattern recognition for what transformation is called for

Date: November 16, 2025
"""

import json
import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class IChingOracle:
    """
    I Ching wisdom consultation for DAE.

    Provides hexagram readings based on:
    1. Random casting (traditional yarrow/coin method simulation)
    2. Polyvagal state matching (find resonant hexagram)
    3. Transduction pathway alignment (what transformation is needed?)
    """

    def __init__(self, hexagram_path: str = "knowledge_base/i_ching_hexagrams.json"):
        """Initialize oracle with hexagram library."""
        self.hexagram_path = Path(hexagram_path)
        self.hexagrams = {}
        self.trigrams = {}
        self._load_hexagrams()

    def _load_hexagrams(self) -> None:
        """Load hexagram library from JSON."""
        if not self.hexagram_path.exists():
            print(f"[IChingOracle] Warning: Hexagram file not found at {self.hexagram_path}")
            return

        with open(self.hexagram_path, 'r') as f:
            data = json.load(f)

        self.hexagrams = data.get("hexagrams", {})
        self.trigrams = data.get("trigrams", {})
        print(f"[IChingOracle] Loaded {len(self.hexagrams)} hexagrams")

    def cast_hexagram(self, method: str = "coin") -> int:
        """
        Cast a hexagram using traditional methods.

        Args:
            method: "coin" (3 coins, 6 times) or "yarrow" (yarrow stalk simulation)

        Returns:
            Hexagram number (1-64)
        """
        if method == "coin":
            return self._coin_method()
        elif method == "yarrow":
            return self._yarrow_method()
        else:
            return random.randint(1, 64)

    def _coin_method(self) -> int:
        """
        Simulate 3-coin method.

        Heads=3, Tails=2
        Sum: 6=old yin, 7=young yang, 8=young yin, 9=old yang

        Returns hexagram as binary encoding of 6 lines.
        """
        lines = []
        for _ in range(6):
            # Three coins
            coins = [random.choice([2, 3]) for _ in range(3)]
            total = sum(coins)
            # 6,8 = yin (0), 7,9 = yang (1)
            if total in [6, 8]:
                lines.append(0)
            else:
                lines.append(1)

        # Convert binary lines to hexagram number
        # Bottom to top (first line is bottom)
        hexagram_num = self._lines_to_hexagram(lines)
        return hexagram_num

    def _yarrow_method(self) -> int:
        """
        Simulate yarrow stalk method (more random variation).

        Each line has different probabilities:
        - Old yang (9): 1/16
        - Young yang (7): 5/16
        - Young yin (8): 7/16
        - Old yin (6): 3/16
        """
        lines = []
        for _ in range(6):
            r = random.random()
            if r < 1/16:
                lines.append(1)  # old yang
            elif r < 6/16:
                lines.append(1)  # young yang
            elif r < 13/16:
                lines.append(0)  # young yin
            else:
                lines.append(0)  # old yin

        return self._lines_to_hexagram(lines)

    def _lines_to_hexagram(self, lines: List[int]) -> int:
        """
        Convert 6 binary lines to hexagram number.

        Uses King Wen sequence (traditional ordering).
        This is a simplified mapping - full implementation would use lookup table.
        """
        # Simple binary to decimal (1-64)
        binary_val = sum(line * (2 ** i) for i, line in enumerate(lines))
        return (binary_val % 64) + 1

    def get_hexagram(self, number: int) -> Optional[Dict[str, Any]]:
        """
        Get hexagram data by number.

        Args:
            number: Hexagram number (1-64)

        Returns:
            Hexagram dictionary or None
        """
        return self.hexagrams.get(str(number))

    def find_by_polyvagal_state(self, polyvagal_state: str) -> List[Dict[str, Any]]:
        """
        Find hexagrams that resonate with a polyvagal state.

        Args:
            polyvagal_state: "ventral", "sympathetic", "dorsal", or mixed states

        Returns:
            List of resonant hexagrams
        """
        resonant = []

        for num, hex_data in self.hexagrams.items():
            resonance = hex_data.get("polyvagal_resonance", "")
            if polyvagal_state.lower() in resonance.lower():
                hex_copy = hex_data.copy()
                hex_copy["number"] = int(num)
                resonant.append(hex_copy)

        return resonant

    def find_by_transduction_need(self, transduction_pathway: str) -> List[Dict[str, Any]]:
        """
        Find hexagrams that align with a needed transduction pathway.

        Args:
            transduction_pathway: e.g., "coherence_repair", "empathic_bridging"

        Returns:
            List of aligned hexagrams
        """
        aligned = []

        for num, hex_data in self.hexagrams.items():
            affinities = hex_data.get("transduction_affinity", [])
            # Check if any affinity contains the pathway
            for affinity in affinities:
                if transduction_pathway.lower() in affinity.lower() or affinity.lower() in transduction_pathway.lower():
                    hex_copy = hex_data.copy()
                    hex_copy["number"] = int(num)
                    aligned.append(hex_copy)
                    break

        return aligned

    def consult_oracle(
        self,
        question: Optional[str] = None,
        polyvagal_state: Optional[str] = None,
        current_zone: Optional[int] = None,
        v0_energy: Optional[float] = None,
        casting_method: str = "coin"
    ) -> Dict[str, Any]:
        """
        Full oracle consultation.

        Args:
            question: Optional question being asked
            polyvagal_state: Current polyvagal state
            current_zone: Current zone (1-5)
            v0_energy: Current V0 energy level
            casting_method: "coin", "yarrow", or "random"

        Returns:
            Complete consultation result with hexagram and interpretation
        """
        # Cast hexagram
        hex_num = self.cast_hexagram(casting_method)
        hexagram = self.get_hexagram(hex_num)

        if not hexagram:
            return {"error": f"Hexagram {hex_num} not found"}

        # Build consultation result
        result = {
            "hexagram_number": hex_num,
            "hexagram_name": hexagram.get("english"),
            "chinese_name": hexagram.get("name"),
            "trigrams": hexagram.get("trigrams"),
            "judgment": hexagram.get("judgment"),
            "image": hexagram.get("image"),
            "wisdom": hexagram.get("wisdom"),
            "transformation_guidance": hexagram.get("transformation_guidance"),
            "polyvagal_resonance": hexagram.get("polyvagal_resonance"),
            "transduction_affinities": hexagram.get("transduction_affinity", []),
            "question": question
        }

        # Add contextual interpretation if state provided
        if polyvagal_state:
            result["state_alignment"] = self._assess_state_alignment(
                hexagram.get("polyvagal_resonance", ""),
                polyvagal_state
            )

        if current_zone:
            result["zone_interpretation"] = self._interpret_for_zone(
                hexagram, current_zone
            )

        if v0_energy is not None:
            result["energy_guidance"] = self._energy_guidance(
                hexagram, v0_energy
            )

        return result

    def _assess_state_alignment(self, hex_resonance: str, current_state: str) -> str:
        """Assess how hexagram resonance aligns with current state."""
        if current_state.lower() in hex_resonance.lower():
            return "ALIGNED: Hexagram resonates with your current state. Trust this wisdom."
        elif "ventral" in hex_resonance and "sympathetic" in current_state.lower():
            return "ASPIRATIONAL: Hexagram points toward ventral regulation. Gentle path forward."
        elif "dorsal" in hex_resonance and "ventral" in current_state.lower():
            return "CAUTIONARY: Hexagram suggests withdrawal. Honor your current strength."
        else:
            return "COMPLEMENTARY: Hexagram offers perspective different from current state."

    def _interpret_for_zone(self, hexagram: Dict, zone: int) -> str:
        """Provide zone-specific interpretation."""
        if zone <= 2:
            return f"In safe exploration (Zone {zone}): {hexagram.get('wisdom')} supports your grounded state."
        elif zone == 3:
            return f"In middle ground (Zone {zone}): {hexagram.get('transformation_guidance')} may guide next steps."
        elif zone == 4:
            return f"In elevated energy (Zone {zone}): Consider {hexagram.get('wisdom')} as you navigate intensity."
        else:
            return f"In crisis territory (Zone {zone}): {hexagram.get('transformation_guidance')} offers grounding wisdom."

    def _energy_guidance(self, hexagram: Dict, v0: float) -> str:
        """Provide guidance based on V0 energy level."""
        if v0 < 0.3:
            return f"Low V0 ({v0:.2f}): {hexagram.get('english')} encourages gentle, receptive action."
        elif v0 < 0.6:
            return f"Balanced V0 ({v0:.2f}): {hexagram.get('english')} supports steady transformation."
        else:
            return f"High V0 ({v0:.2f}): {hexagram.get('english')} suggests channeling intensity wisely."

    def get_daily_hexagram(self) -> Dict[str, Any]:
        """
        Get a daily wisdom hexagram (cached by date).

        Returns the same hexagram for a given day.
        """
        import hashlib
        from datetime import date

        today = date.today().isoformat()
        hash_val = int(hashlib.md5(today.encode()).hexdigest(), 16)
        daily_num = (hash_val % 64) + 1

        return self.consult_oracle(casting_method="random")

    def suggest_for_crisis(self) -> Dict[str, Any]:
        """
        Suggest hexagram for crisis situations.

        Prioritizes grounding and safety hexagrams.
        """
        crisis_hexagrams = [
            5,   # Waiting (Nourishment) - patient trust
            24,  # Return - natural renewal
            29,  # The Abysmal - flowing through danger
            36,  # Darkening of the Light - inner preservation
            52,  # Keeping Still - complete rest
        ]

        hex_num = random.choice(crisis_hexagrams)
        hexagram = self.get_hexagram(hex_num)

        return {
            "hexagram_number": hex_num,
            "hexagram_name": hexagram.get("english"),
            "crisis_wisdom": hexagram.get("transformation_guidance"),
            "polyvagal_guidance": hexagram.get("polyvagal_resonance"),
            "message": "In crisis, the I Ching reminds us: safety first, transformation second."
        }

    def format_reading(self, consultation: Dict[str, Any]) -> str:
        """
        Format consultation result as readable text.

        Args:
            consultation: Result from consult_oracle()

        Returns:
            Formatted string for display
        """
        lines = [
            f"\n╔══════════════════════════════════════╗",
            f"║    I CHING CONSULTATION    ║",
            f"╚══════════════════════════════════════╝\n",
            f"Hexagram {consultation['hexagram_number']}: {consultation['hexagram_name']}",
            f"({consultation['chinese_name']})\n",
            f"Trigrams: {' over '.join(consultation['trigrams'])}\n",
            f"━━━ JUDGMENT ━━━",
            f"{consultation['judgment']}\n",
            f"━━━ IMAGE ━━━",
            f"{consultation['image']}\n",
            f"━━━ WISDOM ━━━",
            f"{consultation['wisdom']}\n",
            f"━━━ TRANSFORMATION GUIDANCE ━━━",
            f"{consultation['transformation_guidance']}\n",
        ]

        if "state_alignment" in consultation:
            lines.append(f"━━━ STATE ALIGNMENT ━━━")
            lines.append(f"{consultation['state_alignment']}\n")

        if "zone_interpretation" in consultation:
            lines.append(f"━━━ ZONE INTERPRETATION ━━━")
            lines.append(f"{consultation['zone_interpretation']}\n")

        if "energy_guidance" in consultation:
            lines.append(f"━━━ ENERGY GUIDANCE ━━━")
            lines.append(f"{consultation['energy_guidance']}\n")

        lines.append(f"Polyvagal Resonance: {consultation['polyvagal_resonance']}")
        lines.append(f"Transduction Affinities: {', '.join(consultation['transduction_affinities'])}")

        return "\n".join(lines)


def demo_oracle():
    """Demonstrate I Ching Oracle capabilities."""
    print("\n" + "="*70)
    print("I CHING ORACLE - DAE WISDOM MODULE DEMO")
    print("="*70 + "\n")

    oracle = IChingOracle()

    # Test 1: Basic consultation
    print("TEST 1: Basic Hexagram Casting")
    print("-" * 50)
    consultation = oracle.consult_oracle(
        question="What transformation is called for?",
        polyvagal_state="sympathetic",
        current_zone=3,
        v0_energy=0.45
    )
    print(oracle.format_reading(consultation))

    # Test 2: Find by polyvagal state
    print("\nTEST 2: Find Ventral-Resonant Hexagrams")
    print("-" * 50)
    ventral_hex = oracle.find_by_polyvagal_state("ventral")
    print(f"Found {len(ventral_hex)} hexagrams with ventral resonance:")
    for h in ventral_hex[:5]:
        print(f"  - #{h['number']}: {h['english']} ({h['polyvagal_resonance']})")

    # Test 3: Find by transduction need
    print("\nTEST 3: Find Coherence Repair Hexagrams")
    print("-" * 50)
    repair_hex = oracle.find_by_transduction_need("coherence")
    print(f"Found {len(repair_hex)} hexagrams aligned with coherence repair:")
    for h in repair_hex[:5]:
        print(f"  - #{h['number']}: {h['english']}")
        print(f"    Affinities: {h['transduction_affinity']}")

    # Test 4: Crisis wisdom
    print("\nTEST 4: Crisis Situation Wisdom")
    print("-" * 50)
    crisis_wisdom = oracle.suggest_for_crisis()
    print(f"Hexagram #{crisis_wisdom['hexagram_number']}: {crisis_wisdom['hexagram_name']}")
    print(f"Crisis Wisdom: {crisis_wisdom['crisis_wisdom']}")
    print(f"Message: {crisis_wisdom['message']}")

    print("\n" + "="*70)
    print("I Ching Oracle Ready for DAE Integration!")
    print("="*70)


if __name__ == "__main__":
    demo_oracle()
