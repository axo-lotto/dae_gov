#!/usr/bin/env python3
"""
Expand Semantic Atoms: Friendly Companion Vocabulary
====================================================

Adds friendly companion vocabulary to semantic_atoms.json:
- Warm greetings (hey, sup, waves)
- Playful markers (*, meta, loop, paradox)
- Self-awareness (organs, convergence, V0, nexus, becoming)
- Earthbound/Undertale style (present, alive, noticing)

Philosophy:
- Preserve existing trauma/therapeutic vocabulary
- Add new atom pools for each organ
- Enable nexus formation on friendly inputs
- Support warm, witty, tender voice emergence

Date: November 13, 2025
"""

import json
from pathlib import Path
from datetime import datetime

# Load existing semantic atoms
atoms_path = Path('persona_layer/semantic_atoms.json')
with open(atoms_path, 'r') as f:
    atoms = json.load(f)

print("🌀 Expanding semantic atoms with friendly companion vocabulary...")
print(f"   Current total atoms: {atoms.get('total_atoms', 'unknown')}")

# Backup original
backup_path = Path('persona_layer/semantic_atoms_backup_before_expansion.json')
with open(backup_path, 'w') as f:
    json.dump(atoms, f, indent=2)
print(f"   ✅ Backup saved: {backup_path.name}")

# LISTENING: Add friendly inquiry and casual check-ins
atoms['LISTENING']['friendly_greeting'] = {
    "hey": 0.95,
    "hi": 0.92,
    "hello": 0.88,
    "sup": 0.90,
    "yo": 0.85,
    "heya": 0.82,
    "howdy": 0.78,
    "greetings": 0.75
}

atoms['LISTENING']['casual_check_in'] = {
    "what's alive": 0.92,
    "what's up": 0.90,
    "what brings you": 0.85,
    "what's present": 0.88,
    "how's it going": 0.82,
    "how are you": 0.80,
    "what's good": 0.85,
    "what's happening": 0.82
}

atoms['LISTENING']['conversational_presence'] = {
    "here": 0.90,
    "with you": 0.88,
    "listening": 0.92,
    "noticing": 0.85,
    "tracking": 0.82,
    "present": 0.90,
    "attending": 0.78,
    "receiving": 0.80
}

# Update LISTENING total
atoms['LISTENING']['total_atoms'] = 74  # 50 + 24 new

# EMPATHY: Add playful warmth and casual connection
atoms['EMPATHY']['playful_warmth'] = {
    "nice": 0.85,
    "good": 0.82,
    "glad": 0.80,
    "appreciate": 0.78,
    "like": 0.75,
    "enjoy": 0.72,
    "dig": 0.70,
    "vibe": 0.75
}

atoms['EMPATHY']['casual_attunement'] = {
    "get it": 0.85,
    "makes sense": 0.82,
    "hear you": 0.88,
    "with you": 0.90,
    "feel you": 0.85,
    "yeah": 0.80,
    "totally": 0.78,
    "real": 0.82
}

atoms['EMPATHY']['total_atoms'] = 66  # 50 + 16 new

# WISDOM: Add self-awareness and meta-cognition
atoms['WISDOM']['self_awareness'] = {
    "organism": 0.95,
    "organs": 0.92,
    "convergence": 0.90,
    "becoming": 0.88,
    "process": 0.85,
    "cycles": 0.82,
    "V0": 0.90,
    "nexus": 0.88,
    "nexuses": 0.85,
    "propositions": 0.80,
    "prehension": 0.82,
    "satisfaction": 0.80
}

atoms['WISDOM']['meta_cognition'] = {
    "meta": 0.92,
    "recursive": 0.85,
    "loop": 0.88,
    "circular": 0.82,
    "self-referential": 0.80,
    "paradox": 0.85,
    "ironic": 0.78,
    "aware": 0.90
}

atoms['WISDOM']['process_philosophy'] = {
    "whitehead": 0.85,
    "actual occasion": 0.88,
    "concrescence": 0.82,
    "kairos": 0.90,
    "lure": 0.85,
    "feeling": 0.92,
    "prehending": 0.82,
    "occasion": 0.88
}

atoms['WISDOM']['total_atoms'] = 82  # 50 + 32 new

# AUTHENTICITY: Add earthbound/undertale style markers
atoms['AUTHENTICITY']['earthbound_style'] = {
    "*": 0.95,  # Action marker
    "appears": 0.88,
    "waves": 0.85,
    "vibes": 0.82,
    "feels": 0.90,
    "notices": 0.85,
    "senses": 0.82,
    "checks": 0.78
}

atoms['AUTHENTICITY']['playful_markers'] = {
    "very meta": 0.90,
    "paradox unlocked": 0.85,
    "oof": 0.88,
    "hmm": 0.82,
    "ah": 0.80,
    "oh": 0.78,
    "huh": 0.75,
    "wait": 0.72
}

atoms['AUTHENTICITY']['casual_expression'] = {
    "dunno": 0.85,
    "maybe": 0.82,
    "kinda": 0.78,
    "sorta": 0.75,
    "bit": 0.72,
    "little": 0.70,
    "just": 0.68,
    "simply": 0.65
}

atoms['AUTHENTICITY']['total_atoms'] = 74  # 50 + 24 new

# PRESENCE: Add grounded simplicity and ordinary moments
atoms['PRESENCE']['grounded_simplicity'] = {
    "coffee": 0.82,
    "tea": 0.80,
    "rain": 0.85,
    "sunset": 0.82,
    "music": 0.78,
    "window": 0.75,
    "sitting": 0.80,
    "walking": 0.78,
    "breathing": 0.88,
    "being": 0.90
}

atoms['PRESENCE']['ordinary_moments'] = {
    "morning": 0.85,
    "evening": 0.82,
    "day": 0.80,
    "night": 0.78,
    "break": 0.75,
    "pause": 0.82,
    "lunch": 0.72,
    "waking": 0.78,
    "sleeping": 0.75,
    "resting": 0.80
}

atoms['PRESENCE']['simple_acknowledgment'] = {
    "ok": 0.80,
    "okay": 0.78,
    "alright": 0.75,
    "right": 0.72,
    "yes": 0.70,
    "yep": 0.68,
    "sure": 0.65,
    "cool": 0.70
}

atoms['PRESENCE']['total_atoms'] = 77  # 50 + 27 new

# BOND: Add friendly connection language
atoms['BOND']['friendly_connection'] = {
    "friend": 0.85,
    "together": 0.82,
    "us": 0.88,
    "we": 0.85,
    "you and me": 0.80,
    "connection": 0.82,
    "relating": 0.78,
    "meeting": 0.75
}

atoms['BOND']['total_atoms'] = 58  # 50 + 8 new

# SANS: Add coherence and flow language
atoms['SANS']['conversational_flow'] = {
    "flowing": 0.85,
    "smooth": 0.80,
    "easy": 0.82,
    "natural": 0.85,
    "organic": 0.88,
    "emergent": 0.82,
    "unfolding": 0.80,
    "arising": 0.78
}

atoms['SANS']['total_atoms'] = 58  # 50 + 8 new

# NDAM: Add playful urgency markers
atoms['NDAM']['playful_urgency'] = {
    "oof": 0.85,
    "ugh": 0.82,
    "whoa": 0.88,
    "wow": 0.85,
    "oh boy": 0.80,
    "yikes": 0.82,
    "help": 0.90,
    "stuck": 0.85
}

atoms['NDAM']['total_atoms'] = 58  # 50 + 8 new

# RNX: Add temporal awareness
atoms['RNX']['conversational_timing'] = {
    "right now": 0.90,
    "this moment": 0.88,
    "just now": 0.85,
    "suddenly": 0.82,
    "gradually": 0.80,
    "slowly": 0.78,
    "quickly": 0.75,
    "timing": 0.82
}

atoms['RNX']['total_atoms'] = 58  # 50 + 8 new

# EO: Add warm polyvagal states
atoms['EO']['ventral_warmth'] = {
    "warm": 0.88,
    "safe": 0.90,
    "connected": 0.85,
    "engaged": 0.82,
    "curious": 0.88,
    "playful": 0.90,
    "light": 0.85,
    "easy": 0.82
}

atoms['EO']['total_atoms'] = 58  # 50 + 8 new

# CARD: Add response scaling for casual vs deep
atoms['CARD']['casual_minimal'] = {
    "hey": 0.90,
    "yep": 0.85,
    "cool": 0.82,
    "nice": 0.80,
    "got it": 0.85,
    "makes sense": 0.82,
    "hear you": 0.88,
    "with you": 0.90
}

atoms['CARD']['total_atoms'] = 58  # 50 + 8 new

# Update metadata
total_new_atoms = (
    24 + 16 + 32 + 24 + 27 + 8 + 8 + 8 + 8 + 8 + 8
)  # 171 new atoms

atoms['total_atoms'] = 550 + total_new_atoms  # 721 total
atoms['version'] = "2.1_friendly_companion"
atoms['date'] = datetime.now().strftime('%Y-%m-%d')
atoms['metadata']['expansion_note'] = "Added 171 friendly companion atoms across all 11 organs to enable warm, witty, tender voice emergence. Includes greetings, playfulness, self-awareness, Earthbound/Undertale style, and ordinary moment vocabulary."

# Save expanded atoms
with open(atoms_path, 'w') as f:
    json.dump(atoms, f, indent=2)

print(f"\n✅ Semantic atoms expanded successfully!")
print(f"   New version: {atoms['version']}")
print(f"   Total atoms: {atoms['total_atoms']} (was 550, added {total_new_atoms})")
print(f"\n📊 Atoms added per organ:")
print(f"   LISTENING: +24 (friendly_greeting, casual_check_in, conversational_presence)")
print(f"   EMPATHY: +16 (playful_warmth, casual_attunement)")
print(f"   WISDOM: +32 (self_awareness, meta_cognition, process_philosophy)")
print(f"   AUTHENTICITY: +24 (earthbound_style, playful_markers, casual_expression)")
print(f"   PRESENCE: +27 (grounded_simplicity, ordinary_moments, simple_acknowledgment)")
print(f"   BOND: +8 (friendly_connection)")
print(f"   SANS: +8 (conversational_flow)")
print(f"   NDAM: +8 (playful_urgency)")
print(f"   RNX: +8 (conversational_timing)")
print(f"   EO: +8 (ventral_warmth)")
print(f"   CARD: +8 (casual_minimal)")
print(f"\n🌀 Ready for re-training! Nexus formation should now occur on friendly inputs.")
