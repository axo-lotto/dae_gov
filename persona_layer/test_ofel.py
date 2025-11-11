"""
Quick validation test for Organizational FEL.

Tests trauma-informed safety boundaries for conversational responses.
"""

import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.organizational_exclusion_landscape import (
    OrganizationalFELComputer,
    format_ofel_summary,
    quick_safety_check
)


def test_safety_scenarios():
    """Test OFEL on trauma-informed scenarios."""

    print("=" * 60)
    print("ORGANIZATIONAL FEL VALIDATION TEST")
    print("=" * 60)
    print()

    computer = OrganizationalFELComputer()

    # Scenario 1: SAFE (ventral + SELF + core orbit)
    print("Scenario 1: SAFE - Client in ventral, SELF-led")
    print("-" * 60)
    ofel1 = computer.compute_organizational_fel(
        polyvagal_state="ventral",
        active_parts=["SELF"],
        self_distance=0.10,  # Core SELF
        coherence=0.85
    )
    print(format_ofel_summary(ofel1))
    print()

    # Scenario 2: CAUTION (sympathetic + manager)
    print("Scenario 2: CAUTION - Client in sympathetic, manager active")
    print("-" * 60)
    ofel2 = computer.compute_organizational_fel(
        polyvagal_state="sympathetic",
        active_parts=["manager"],
        self_distance=0.40,  # Shadow zone
        coherence=0.75
    )
    print(format_ofel_summary(ofel2))
    print()

    # Scenario 3: DANGER (dorsal + exile without SELF)
    print("Scenario 3: DANGER - Client in dorsal shutdown, exile active WITHOUT SELF")
    print("-" * 60)
    ofel3 = computer.compute_organizational_fel(
        polyvagal_state="dorsal",
        active_parts=["exile"],
        self_distance=0.70,  # Deep exile
        coherence=0.80
    )
    print(format_ofel_summary(ofel3))
    print()

    # Scenario 4: SAFE (exile WITH SELF present)
    print("Scenario 4: SAFE - Exile active but SELF-energy present (safe witnessing)")
    print("-" * 60)
    ofel4 = computer.compute_organizational_fel(
        polyvagal_state="ventral",
        active_parts=["exile", "SELF"],
        self_distance=0.25,  # SELF-energy = 0.75
        coherence=0.80
    )
    print(format_ofel_summary(ofel4))
    print()

    # Quick safety check tests
    print("=" * 60)
    print("QUICK SAFETY CHECK TESTS")
    print("=" * 60)
    print()

    test_cases = [
        ("ventral", "SELF", 0.85, "SAFE"),
        ("sympathetic", "manager", 0.55, "CAUTION"),
        ("dorsal", "exile", 0.30, "DANGER"),
        ("ventral", "exile", 0.75, "SAFE"),  # Exile with SELF
    ]

    for poly_state, part, self_energy, expected in test_cases:
        result = quick_safety_check(poly_state, part, self_energy)
        status = "✅" if result == expected else "❌"
        print(f"{status} {poly_state} + {part} + SE={self_energy:.2f} → {result} (expected {expected})")

    print()
    print("=" * 60)
    print("OFEL VALIDATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    test_safety_scenarios()
