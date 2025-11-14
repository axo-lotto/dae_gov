"""
Universal Test Utilities for DAE_HYPHAE_1
==========================================

Provides correct extraction methods for organism results across all test suites.

Key Fix: Organs return `.coherence` and `.lure` attributes (Whiteheadian process),
not `.satisfaction` (which is the final converged state).

Author: DAE_HYPHAE_1
Date: November 13, 2025
Phase: A1 (Test Infrastructure Fix)
"""

import numpy as np
from typing import Dict, List, Optional, Set

# Standard 11-organ order
ORGAN_ORDER = [
    'LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',  # Conversational (5)
    'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD'  # Trauma/context-aware (6)
]


# ============================================================================
# Organ Extraction Utilities
# ============================================================================

def extract_organ_coherences(result: Dict) -> Dict[str, float]:
    """
    Extract organ coherences from organism result.

    Args:
        result: Organism processing result dict

    Returns:
        Dict mapping organ_name → coherence (0.0-1.0)
    """
    organ_results = result.get('organ_results', {})
    coherences = {}

    for organ_name in ORGAN_ORDER:
        organ_result = organ_results.get(organ_name)
        if organ_result and hasattr(organ_result, 'coherence'):
            coherences[organ_name] = organ_result.coherence
        else:
            coherences[organ_name] = 0.0

    return coherences


def extract_organ_lures(result: Dict) -> Dict[str, float]:
    """
    Extract organ lures (Whiteheadian attractors) from organism result.

    Args:
        result: Organism processing result dict

    Returns:
        Dict mapping organ_name → lure (0.0-1.0)
    """
    organ_results = result.get('organ_results', {})
    lures = {}

    for organ_name in ORGAN_ORDER:
        organ_result = organ_results.get(organ_name)
        if organ_result and hasattr(organ_result, 'lure'):
            lures[organ_name] = organ_result.lure
        else:
            lures[organ_name] = 0.0

    return lures


def extract_organ_vector(result: Dict, use_lure: bool = False) -> np.ndarray:
    """
    Extract organ coherences (or lures) as 11D vector.

    Args:
        result: Organism processing result dict
        use_lure: If True, extract lures instead of coherences

    Returns:
        11D numpy array of organ values
    """
    if use_lure:
        values = extract_organ_lures(result)
    else:
        values = extract_organ_coherences(result)

    return np.array([values[organ] for organ in ORGAN_ORDER])


def count_active_organs(result: Dict, threshold: float = 0.01, use_lure: bool = False) -> int:
    """
    Count organs with coherence (or lure) above threshold.

    Args:
        result: Organism processing result dict
        threshold: Minimum value to consider "active"
        use_lure: If True, count by lure instead of coherence

    Returns:
        Number of active organs (0-11)
    """
    if use_lure:
        values = extract_organ_lures(result)
    else:
        values = extract_organ_coherences(result)

    return sum(1 for v in values.values() if v > threshold)


# ============================================================================
# Emission Extraction Utilities
# ============================================================================

def extract_emission_text(result: Dict) -> str:
    """
    Extract emission text from result.

    Args:
        result: Organism processing result dict

    Returns:
        Emission text string (may be empty)
    """
    return result.get('emission_text', '')


def extract_emission_confidence(result: Dict) -> float:
    """
    Extract emission confidence.

    Args:
        result: Organism processing result dict

    Returns:
        Confidence score (0.0-1.0)
    """
    return result.get('emission_confidence', 0.0)


def extract_emission_strategy(result: Dict) -> str:
    """
    Extract emission strategy/path.

    Args:
        result: Organism processing result dict

    Returns:
        Strategy name ('direct', 'fusion', 'hebbian_fallback', etc.)
    """
    # Primary location: result['emission_path']
    strategy = result.get('emission_path')

    # Fallback: felt_states['emission_strategy']
    if not strategy:
        felt_states = result.get('felt_states', {})
        strategy = felt_states.get('emission_strategy')

    return strategy or 'unknown'


def extract_nexus_count(result: Dict) -> int:
    """
    Extract number of nexuses formed.

    Args:
        result: Organism processing result dict

    Returns:
        Number of nexuses (≥0)
    """
    # Primary location: result['emission_nexus_count']
    nexus_count = result.get('emission_nexus_count')

    if nexus_count is not None:
        return int(nexus_count)

    # Fallback: count from felt_states
    felt_states = result.get('felt_states', {})
    nexuses = felt_states.get('nexuses', [])

    if isinstance(nexuses, list):
        return len(nexuses)

    return 0


# ============================================================================
# Convergence Extraction Utilities
# ============================================================================

def extract_convergence_cycles(result: Dict) -> int:
    """
    Extract number of convergence cycles.

    Args:
        result: Organism processing result dict

    Returns:
        Number of cycles (≥0)
    """
    felt_states = result.get('felt_states', {})
    return int(felt_states.get('convergence_cycles', 0))


def extract_v0_descent(result: Dict) -> float:
    """
    Extract V0 energy descent (initial - final).

    Args:
        result: Organism processing result dict

    Returns:
        V0 descent amount (0.0-1.0)
    """
    felt_states = result.get('felt_states', {})
    v0_initial = felt_states.get('v0_energy_initial', 1.0)
    v0_final = felt_states.get('v0_energy_final', 0.0)
    return v0_initial - v0_final


def extract_final_satisfaction(result: Dict) -> float:
    """
    Extract final satisfaction after convergence.

    Note: This is the organism-level satisfaction (after concrescence),
    NOT per-organ (which use coherence/lure).

    Args:
        result: Organism processing result dict

    Returns:
        Final satisfaction (0.0-1.0)
    """
    felt_states = result.get('felt_states', {})
    return float(felt_states.get('satisfaction_final', 0.0))


def extract_kairos_detected(result: Dict) -> bool:
    """
    Extract whether Kairos (opportune moment) was detected.

    Args:
        result: Organism processing result dict

    Returns:
        True if Kairos detected
    """
    felt_states = result.get('felt_states', {})
    return bool(felt_states.get('kairos_detected', False))


# ============================================================================
# Semantic Field Extraction Utilities
# ============================================================================

def extract_semantic_fields(result: Dict) -> List[Dict]:
    """
    Extract semantic fields from result.

    Args:
        result: Organism processing result dict

    Returns:
        List of semantic field dicts
    """
    felt_states = result.get('felt_states', {})
    semantic_fields = felt_states.get('semantic_fields', [])

    if isinstance(semantic_fields, list):
        return semantic_fields

    return []


def extract_atom_activations(result: Dict) -> Dict[str, float]:
    """
    Extract all atom activations from semantic fields.

    Args:
        result: Organism processing result dict

    Returns:
        Dict mapping atom_name → activation strength
    """
    semantic_fields = extract_semantic_fields(result)
    atom_activations = {}

    for field in semantic_fields:
        if isinstance(field, dict):
            atoms = field.get('atoms', [])
            for atom in atoms:
                if isinstance(atom, dict):
                    atom_name = atom.get('atom_name')
                    activation = atom.get('activation', 0.0)
                    if atom_name:
                        # Aggregate multiple activations (max)
                        if atom_name in atom_activations:
                            atom_activations[atom_name] = max(atom_activations[atom_name], activation)
                        else:
                            atom_activations[atom_name] = activation

    return atom_activations


def extract_meta_atom_activations(result: Dict) -> Set[str]:
    """
    Extract activated meta-atoms from semantic fields.

    Args:
        result: Organism processing result dict

    Returns:
        Set of meta-atom names that were activated
    """
    semantic_fields = extract_semantic_fields(result)
    meta_atoms = set()

    for field in semantic_fields:
        if isinstance(field, dict):
            field_meta_atoms = field.get('meta_atoms', {})
            if isinstance(field_meta_atoms, dict):
                meta_atoms.update(field_meta_atoms.keys())

    # Also check felt_states
    felt_states = result.get('felt_states', {})
    meta_atoms_list = felt_states.get('meta_atoms_activated', [])
    if isinstance(meta_atoms_list, list):
        meta_atoms.update(meta_atoms_list)

    return meta_atoms


# ============================================================================
# Comparison Utilities
# ============================================================================

def compute_organ_similarity(result_a: Dict, result_b: Dict) -> float:
    """
    Compute cosine similarity between organ coherence vectors.

    Args:
        result_a: First organism result
        result_b: Second organism result

    Returns:
        Cosine similarity (0.0-1.0)
    """
    vector_a = extract_organ_vector(result_a)
    vector_b = extract_organ_vector(result_b)

    # Cosine similarity
    if np.linalg.norm(vector_a) == 0 or np.linalg.norm(vector_b) == 0:
        return 0.0

    similarity = np.dot(vector_a, vector_b) / (np.linalg.norm(vector_a) * np.linalg.norm(vector_b))

    return float(max(0.0, min(1.0, similarity)))  # Clamp to [0, 1]


def compute_emission_similarity(emission_a: str, emission_b: str) -> float:
    """
    Compute similarity between two emissions (simple word overlap).

    Args:
        emission_a: First emission text
        emission_b: Second emission text

    Returns:
        Jaccard similarity (0.0-1.0)
    """
    if not emission_a or not emission_b:
        return 0.0

    # Simple word-based Jaccard similarity
    words_a = set(emission_a.lower().split())
    words_b = set(emission_b.lower().split())

    if not words_a or not words_b:
        return 0.0

    intersection = len(words_a & words_b)
    union = len(words_a | words_b)

    return intersection / union if union > 0 else 0.0


# ============================================================================
# Validation Utilities
# ============================================================================

def validate_result_structure(result: Dict) -> bool:
    """
    Validate that organism result has expected structure.

    Args:
        result: Organism processing result dict

    Returns:
        True if structure is valid
    """
    required_keys = ['organ_results', 'felt_states', 'emission_text']

    for key in required_keys:
        if key not in result:
            return False

    # Validate organ_results is dict
    if not isinstance(result.get('organ_results'), dict):
        return False

    # Validate felt_states is dict
    if not isinstance(result.get('felt_states'), dict):
        return False

    return True


def get_debug_summary(result: Dict) -> str:
    """
    Get human-readable summary of result for debugging.

    Args:
        result: Organism processing result dict

    Returns:
        Multi-line summary string
    """
    lines = []
    lines.append("=== ORGANISM RESULT SUMMARY ===")

    # Organs
    active_count = count_active_organs(result)
    lines.append(f"Active organs: {active_count}/11")

    coherences = extract_organ_coherences(result)
    top_organs = sorted(coherences.items(), key=lambda x: x[1], reverse=True)[:3]
    lines.append(f"Top organs: {', '.join(f'{o}={c:.2f}' for o, c in top_organs)}")

    # Convergence
    cycles = extract_convergence_cycles(result)
    v0_descent = extract_v0_descent(result)
    satisfaction = extract_final_satisfaction(result)
    lines.append(f"Convergence: {cycles} cycles, V0 descent={v0_descent:.3f}, satisfaction={satisfaction:.3f}")

    # Emission
    emission = extract_emission_text(result)
    confidence = extract_emission_confidence(result)
    strategy = extract_emission_strategy(result)
    lines.append(f"Emission: {len(emission)} chars, confidence={confidence:.3f}, strategy={strategy}")

    # Nexuses
    nexus_count = extract_nexus_count(result)
    meta_atoms = extract_meta_atom_activations(result)
    lines.append(f"Nexuses: {nexus_count}, Meta-atoms: {len(meta_atoms)}")

    return "\n".join(lines)
