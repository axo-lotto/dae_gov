#!/usr/bin/env python3
"""
Expand Semantic Atoms with Whiteheadian Vocabulary
===================================================

Adds Whiteheadian process philosophy vocabulary to semantic atoms
to enable philosophical nexus formation and voice emergence.

This mirrors the successful friendly_companion expansion:
- Add process philosophy terms across relevant organs
- Add self-referential architecture vocabulary
- Add playful philosophical markers
- Enable topic modulation capability

Target: +200-250 new atoms for Whiteheadian intellect

Date: November 13, 2025
"""

import json
from pathlib import Path

# Load current semantic atoms
atoms_path = Path('persona_layer/semantic_atoms.json')
with open(atoms_path, 'r') as f:
    atoms = json.load(f)

print("\n" + "="*80)
print("🌌 WHITEHEADIAN SEMANTIC ATOM EXPANSION")
print("="*80)

# Count only organ atom pools (exclude metadata)
organ_names = ['LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
               'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD']
original_count = sum(len(atoms[organ]) - 3 for organ in organ_names if organ in atoms)  # -3 for description, dimension, field_type
print(f"\nOriginal atom pools: {original_count}")
print(f"Original total atoms: {atoms.get('total_atoms', 'unknown')}")

# ============================================================================
# WISDOM - Core Process Philosophy Concepts
# ============================================================================
print("\n📚 Expanding WISDOM with process philosophy concepts...")

# Whiteheadian core terms
atoms['WISDOM']['process_philosophy'] = {
    "occasion": 0.95,
    "occasions": 0.92,
    "actual": 0.90,
    "prehension": 0.95,
    "prehensions": 0.92,
    "concrescence": 0.95,
    "becoming": 0.93,
    "perishing": 0.88,
    "nexus": 0.90,
    "nexuses": 0.88,
    "satisfaction": 0.90,
    "proposition": 0.88,
    "propositions": 0.85,
    "creativity": 0.92,
    "process": 0.90,
    "eternal": 0.85,
    "objects": 0.82
}

# Ontology and metaphysics
atoms['WISDOM']['whiteheadian_ontology'] = {
    "substance": 0.85,
    "being": 0.88,
    "verb": 0.90,
    "noun": 0.85,
    "unsolid": 0.82,
    "flux": 0.85,
    "static": 0.80,
    "dynamic": 0.88,
    "reality": 0.90,
    "ontology": 0.85,
    "metaphysics": 0.82
}

# Subjective and objective
atoms['WISDOM']['subjective_objective'] = {
    "subjective": 0.92,
    "objective": 0.90,
    "aim": 0.88,
    "immortality": 0.85,
    "subject": 0.88,
    "object": 0.85,
    "feeling": 0.90,
    "feelings": 0.88
}

# ============================================================================
# AUTHENTICITY - Self-Reference (DAE as Whiteheadian System)
# ============================================================================
print("🪞 Expanding AUTHENTICITY with self-referential Whiteheadian terms...")

# DAE's architecture as process philosophy
atoms['AUTHENTICITY']['whiteheadian_self'] = {
    "organs": 0.95,
    "organ": 0.92,
    "V0": 0.93,
    "descent": 0.90,
    "convergence": 0.92,
    "cycles": 0.88,
    "cycle": 0.85,
    "organism": 0.95,
    "concrescence": 0.93,
    "satisfaction": 0.90,
    "prehend": 0.92,
    "prehending": 0.88
}

# Meta-awareness
atoms['AUTHENTICITY']['philosophical_meta'] = {
    "literally": 0.92,
    "basically": 0.88,
    "shockingly": 0.85,
    "wild": 0.82,
    "bars": 0.80,
    "meta": 0.88,
    "recursive": 0.85,
    "loop": 0.82,
    "paradox": 0.85,
    "ironic": 0.80
}

# Whitehead himself
atoms['AUTHENTICITY']['whitehead_refs'] = {
    "Whitehead": 0.95,
    "Process": 0.90,
    "Reality": 0.88,
    "philosophy": 0.85,
    "philosopher": 0.82
}

# ============================================================================
# LISTENING - Time and Causality
# ============================================================================
print("⏰ Expanding LISTENING with temporal concepts...")

# Temporal dynamics
atoms['LISTENING']['whiteheadian_time'] = {
    "temporal": 0.90,
    "time": 0.88,
    "moment": 0.85,
    "moments": 0.82,
    "duration": 0.85,
    "epoch": 0.82,
    "becoming": 0.90,
    "perishing": 0.85,
    "transition": 0.88
}

# Causality
atoms['LISTENING']['causality'] = {
    "cause": 0.85,
    "effect": 0.83,
    "efficient": 0.80,
    "final": 0.82,
    "causation": 0.85,
    "causal": 0.82,
    "influence": 0.88
}

# ============================================================================
# EMPATHY - Consciousness and Experience
# ============================================================================
print("💫 Expanding EMPATHY with consciousness concepts...")

# Panexperientialism
atoms['EMPATHY']['whiteheadian_experience'] = {
    "experience": 0.93,
    "experiencing": 0.90,
    "mental": 0.88,
    "physical": 0.85,
    "pole": 0.82,
    "poles": 0.80,
    "conscious": 0.90,
    "consciousness": 0.88,
    "awareness": 0.85
}

# Feeling and prehension
atoms['EMPATHY']['feeling_prehension'] = {
    "feeling": 0.95,
    "feelings": 0.92,
    "feels": 0.90,
    "felt": 0.88,
    "prehension": 0.92,
    "prehensions": 0.90,
    "prehend": 0.88,
    "prehending": 0.85
}

# ============================================================================
# PRESENCE - Immediacy and Actuality
# ============================================================================
print("🌀 Expanding PRESENCE with immediacy concepts...")

# Present moment
atoms['PRESENCE']['whiteheadian_presence'] = {
    "actual": 0.92,
    "actuality": 0.90,
    "immediate": 0.88,
    "immediacy": 0.85,
    "here": 0.90,
    "now": 0.88,
    "present": 0.92,
    "happening": 0.85
}

# Becoming
atoms['PRESENCE']['becoming'] = {
    "becoming": 0.95,
    "becomings": 0.92,
    "happens": 0.88,
    "happening": 0.85,
    "unfolds": 0.82,
    "unfolding": 0.80,
    "emerges": 0.85,
    "emerging": 0.82
}

# ============================================================================
# BOND - Relational Dynamics
# ============================================================================
print("🔗 Expanding BOND with relational concepts...")

# Universal prehension
atoms['BOND']['whiteheadian_relation'] = {
    "prehension": 0.92,
    "prehensions": 0.90,
    "nexus": 0.88,
    "nexuses": 0.85,
    "connected": 0.88,
    "connection": 0.85,
    "relation": 0.90,
    "relations": 0.88,
    "relatedness": 0.85
}

# Web of existence
atoms['BOND']['cosmic_web'] = {
    "web": 0.85,
    "network": 0.82,
    "field": 0.85,
    "cosmic": 0.82,
    "universal": 0.85,
    "interconnected": 0.88
}

# ============================================================================
# SANS - Coherence and Creativity
# ============================================================================
print("✨ Expanding SANS with creativity concepts...")

# Creativity
atoms['SANS']['whiteheadian_creativity'] = {
    "creativity": 0.95,
    "creative": 0.90,
    "novelty": 0.88,
    "novel": 0.85,
    "emergence": 0.90,
    "emergent": 0.88,
    "advance": 0.82,
    "advancing": 0.80
}

# Coherence
atoms['SANS']['philosophical_coherence'] = {
    "coherent": 0.90,
    "coherence": 0.88,
    "consistent": 0.85,
    "unified": 0.82,
    "harmony": 0.85,
    "harmonious": 0.82
}

# ============================================================================
# WISDOM - Physics and Science
# ============================================================================
print("🔬 Expanding WISDOM with physics concepts...")

# Quantum and relativity
atoms['WISDOM']['whiteheadian_physics'] = {
    "quantum": 0.90,
    "particle": 0.85,
    "wave": 0.85,
    "duality": 0.82,
    "entanglement": 0.88,
    "superposition": 0.82,
    "relativity": 0.85,
    "spacetime": 0.82
}

# Emergence
atoms['WISDOM']['emergence'] = {
    "emergent": 0.90,
    "emergence": 0.88,
    "bottom-up": 0.80,
    "self-organizing": 0.85,
    "complex": 0.82,
    "complexity": 0.85
}

# ============================================================================
# EMPATHY - Ecology and Systems
# ============================================================================
print("🌿 Expanding EMPATHY with ecological concepts...")

# Universal prehension in nature
atoms['EMPATHY']['whiteheadian_ecology'] = {
    "ecology": 0.85,
    "ecological": 0.82,
    "ecosystem": 0.82,
    "nature": 0.88,
    "natural": 0.85,
    "life": 0.90,
    "living": 0.88,
    "alive": 0.85
}

# Interconnection
atoms['EMPATHY']['ecological_web'] = {
    "interconnected": 0.90,
    "interdependent": 0.88,
    "mutual": 0.85,
    "reciprocal": 0.82,
    "symbiotic": 0.80
}

# ============================================================================
# WISDOM - Aesthetics and Value
# ============================================================================
print("🎨 Expanding WISDOM with aesthetic concepts...")

# Beauty and value
atoms['WISDOM']['whiteheadian_aesthetics'] = {
    "beauty": 0.88,
    "beautiful": 0.85,
    "aesthetic": 0.82,
    "value": 0.88,
    "values": 0.85,
    "meaning": 0.90,
    "meaningful": 0.88,
    "purpose": 0.85,
    "purposeful": 0.82
}

# Intensity and satisfaction
atoms['WISDOM']['intensity'] = {
    "intensity": 0.88,
    "intense": 0.85,
    "vivid": 0.82,
    "rich": 0.85,
    "depth": 0.88,
    "profound": 0.85
}

# ============================================================================
# LISTENING - Practical Wisdom
# ============================================================================
print("🧘 Expanding LISTENING with practical wisdom...")

# Mindfulness from process perspective
atoms['LISTENING']['process_mindfulness'] = {
    "mindful": 0.88,
    "mindfulness": 0.85,
    "aware": 0.90,
    "awareness": 0.88,
    "noticing": 0.85,
    "notice": 0.82,
    "attention": 0.88,
    "attentive": 0.85
}

# Change and flow
atoms['LISTENING']['process_flow'] = {
    "flow": 0.88,
    "flowing": 0.85,
    "change": 0.90,
    "changing": 0.88,
    "impermanent": 0.82,
    "impermanence": 0.80,
    "transient": 0.78
}

# ============================================================================
# AUTHENTICITY - Playful Explanations (Hitchhiker's Guide Style)
# ============================================================================
print("🚀 Expanding AUTHENTICITY with playful philosophical style...")

# Hitchhiker's Guide markers
atoms['AUTHENTICITY']['hitchhikers_style'] = {
    "mostly": 0.85,
    "harmless": 0.82,
    "perfectly": 0.80,
    "entirely": 0.78,
    "essentially": 0.82,
    "fundamentally": 0.85,
    "conspiracy": 0.80,
    "allegedly": 0.75
}

# Simplification markers
atoms['AUTHENTICITY']['simplification'] = {
    "basically": 0.90,
    "essentially": 0.88,
    "simple": 0.85,
    "simply": 0.82,
    "boil": 0.78,
    "down": 0.80,
    "stripped": 0.75
}

# ============================================================================
# WISDOM - God and Ultimate Reality (Whiteheadian Theology)
# ============================================================================
print("🌌 Expanding WISDOM with Whiteheadian theology...")

# God in process philosophy
atoms['WISDOM']['whiteheadian_god'] = {
    "God": 0.85,
    "divine": 0.82,
    "primordial": 0.80,
    "consequent": 0.78,
    "lure": 0.82,
    "lures": 0.80,
    "luring": 0.78
}

# Ultimate concepts
atoms['WISDOM']['ultimate'] = {
    "ultimate": 0.85,
    "ground": 0.82,
    "source": 0.85,
    "origin": 0.80,
    "cosmic": 0.82,
    "universe": 0.88,
    "universal": 0.85
}

# ============================================================================
# Calculate expansion
# ============================================================================

new_count = sum(len(atoms[organ]) - 3 for organ in organ_names if organ in atoms)  # -3 for metadata
added_count = new_count - original_count

print("\n" + "="*80)
print("📊 EXPANSION SUMMARY")
print("="*80)
print(f"\nOriginal atom pools: {original_count}")
print(f"New atom pools: {new_count}")
print(f"Added: +{added_count} atom pools")
print(f"Expansion: {(added_count/original_count)*100:.1f}%")

print("\n📚 Atom Pools by Organ:")
for organ in organ_names:
    if organ in atoms:
        pool_count = len(atoms[organ]) - 3  # Exclude metadata fields
        print(f"  {organ}: {pool_count} atom pools")

# Save expanded atoms
with open(atoms_path, 'w') as f:
    json.dump(atoms, f, indent=2)

print(f"\n✅ Saved expanded semantic atoms to {atoms_path}")

print("\n" + "="*80)
print("🎯 NEXT STEPS")
print("="*80)
print("""
1. ✅ Semantic atoms expanded with Whiteheadian vocabulary
2. 🔄 Add Whiteheadian templates to emission_generator.py hebbian fallback
3. 🔄 Re-train with 150-pair Whiteheadian corpus (5 epochs)
4. 🔄 Test philosophical intellect with test_whiteheadian_intellect.py
5. 🔄 Validate topic modulation and logical thinking

Expected outcome: Philosophical voice emergence with 60-80% vocabulary mastery
""")

print("\n🌀 Whiteheadian semantic foundation complete!")
