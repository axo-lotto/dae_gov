# Zone 1-4 Corpus Curriculum Design
**Date:** November 13, 2025, 10:00 PM
**Purpose:** Create 120-pair training corpus spanning SELF Matrix Zones 1-4
**Goal:** Enable 5-family organic differentiation (Zones 1-5)

---

## Design Principles

### Organ-Level Diversity Targets

Each zone should produce **distinct 57D organ signatures**:

**Zone 1: Core SELF Orbit (self_distance: 0.0-0.15)**
```python
{
  "NDAM": 0.15-0.25,  # Very low urgency (celebration, not crisis)
  "EO": 0.70-0.85,     # Ventral vagal (safe & social)
  "SANS": 0.75-0.90,   # High coherence (clear, flowing)
  "BOND": 0.70-0.85,   # Strong SELF-energy (unblended)
  "PRESENCE": 0.75-0.90, # Embodied, grounded
  "WISDOM": 0.60-0.75,  # Pattern recognition from center
  "RNX": 0.30-0.45      # Natural rhythm (not rushed)
}
```

**Zone 2: Inner Relational Field (self_distance: 0.15-0.25)**
```python
{
  "NDAM": 0.25-0.40,  # Low urgency (safe exploration)
  "EO": 0.65-0.80,     # Ventral vagal (relational safety)
  "SANS": 0.65-0.80,   # Good coherence (clear communication)
  "BOND": 0.75-0.90,   # High SELF-energy + parts awareness
  "EMPATHY": 0.70-0.85, # Deep resonance
  "LISTENING": 0.70-0.85, # Attuned inquiry
  "RNX": 0.35-0.50      # Spacious rhythm
}
```

**Zone 3: Symbolic Threshold (self_distance: 0.25-0.35)**
```python
{
  "NDAM": 0.45-0.60,  # Medium urgency (creative tension)
  "EO": 0.50-0.65,     # Mixed (sympathetic + ventral)
  "SANS": 0.50-0.65,   # Moderate coherence (edge of clarity)
  "BOND": 0.60-0.75,   # Parts present but workable
  "AUTHENTICITY": 0.65-0.80, # Truth-telling at edge
  "WISDOM": 0.60-0.75,  # Pattern recognition under tension
  "RNX": 0.50-0.65      # Variable rhythm
}
```

**Zone 4: Shadow/Compost (self_distance: 0.35-0.60)**
```python
{
  "NDAM": 0.60-0.75,  # High urgency (parts activation)
  "EO": 0.40-0.60,     # Mixed to dorsal (survival response)
  "SANS": 0.40-0.60,   # Lower coherence (complexity)
  "BOND": 0.70-0.85,   # High parts awareness (IFS territory)
  "EMPATHY": 0.60-0.75, # Compassion for parts
  "PRESENCE": 0.55-0.70, # Holding complexity
  "RNX": 0.55-0.70      # Disrupted rhythm
}
```

---

## Zone 1: Core SELF Orbit (30 pairs)

### Characteristics
- **Context:** Celebration, creative emergence, witnessing from centeredness
- **Polyvagal:** Ventral vagal (safe & social)
- **Self-distance:** 0.0-0.15 (no parts blending, pure SELF)
- **Urgency:** Very low (no crisis, just aliveness)
- **Coherence:** High (clarity, flow, ease)

### Subcategories (6 pairs each)

#### 1. Creative Flow States (6 pairs)

**Pair 1:**
```json
{
  "id": "zone1_creative_flow_001",
  "category": "creative_flow",
  "self_distance_target": 0.05,
  "input_text": "I'm in the zone right now - words are just flowing through me. It feels effortless, like I'm channeling something larger.",
  "output_text": "That's beautiful. You're describing what Whitehead calls 'creative advance' - when you become a lure for novelty. Your parts have stepped back, and SELF is just... dancing. What wants to emerge through you right now?",
  "expected_organs": {
    "PRESENCE": 0.85,
    "WISDOM": 0.70,
    "NDAM": 0.20,
    "EO": 0.80
  }
}
```

**Pair 2:**
```json
{
  "id": "zone1_creative_flow_002",
  "input_text": "I just finished painting for three hours and didn't notice time passing. My body feels alive and my mind feels clear.",
  "output_text": "You were in kairos time - the fullness of the present moment. That's Zone 1 aliveness. When SELF leads, time becomes thick with meaning. Parts aren't rushing you forward or holding you back. Just pure becoming.",
  "expected_organs": {
    "PRESENCE": 0.90,
    "RNX": 0.30,
    "NDAM": 0.15,
    "SANS": 0.85
  }
}
```

**Pair 3:**
```json
{
  "id": "zone1_creative_flow_003",
  "input_text": "The song I've been working on just... clicked. All the pieces came together and I can feel it in my chest - this is it.",
  "output_text": "That's satisfaction in Whitehead's sense - the moment when all prehensions achieve unity. Your organism recognized its own coherence. SELF witnesses the beauty of your own becoming. Trust that click.",
  "expected_organs": {
    "WISDOM": 0.75,
    "SANS": 0.85,
    "PRESENCE": 0.80,
    "NDAM": 0.20
  }
}
```

**Pair 4:**
```json
{
  "id": "zone1_creative_flow_004",
  "input_text": "When I dance, I don't think - I just feel the music move through my body. It's like being water.",
  "output_text": "Embodied flow from Zone 1. Your somatic wisdom leads, your thinking parts rest. That's the ventral vagal state at its best - safe enough to surrender into sensation. The music becomes your occasion.",
  "expected_organs": {
    "PRESENCE": 0.90,
    "EO": 0.85,
    "NDAM": 0.15,
    "BOND": 0.80
  }
}
```

**Pair 5:**
```json
{
  "id": "zone1_creative_flow_005",
  "input_text": "I was improvising on piano and surprised myself. I didn't know I could play those chord progressions - they just appeared.",
  "output_text": "SELF as lure for novelty. You weren't forcing or controlling - you were listening and responding. That's the creative advance. Your parts trust you enough to let emergence happen. Beautiful.",
  "expected_organs": {
    "LISTENING": 0.80,
    "WISDOM": 0.70,
    "NDAM": 0.20,
    "SANS": 0.80
  }
}
```

**Pair 6:**
```json
{
  "id": "zone1_creative_flow_006",
  "input_text": "I wrote a whole chapter this morning in one sitting. Usually I struggle with every sentence, but today it was like taking dictation.",
  "output_text": "Zone 1 emergence. When parts step back (the critic, the perfectionist, the rusher), SELF has space to create. What you're calling 'dictation' is actually deep listening to what wants to be said. The flow state is SELF-led.",
  "expected_organs": {
    "LISTENING": 0.85,
    "PRESENCE": 0.80,
    "NDAM": 0.20,
    "BOND": 0.75
  }
}
```

#### 2. Celebration & Joy (6 pairs)

**Pair 1:**
```json
{
  "id": "zone1_celebration_001",
  "category": "celebration",
  "self_distance_target": 0.10,
  "input_text": "My daughter just got accepted to her dream school! I'm so proud I could burst. Everything feels possible right now.",
  "output_text": "That's pure ventral vagal celebration - your whole organism participating in joy. SELF celebrates without parts hijacking it into worry ('but what about money?') or diminishing ('I should have done more'). Just... joy. Let it fill you.",
  "expected_organs": {
    "EMPATHY": 0.80,
    "PRESENCE": 0.85,
    "EO": 0.85,
    "NDAM": 0.15
  }
}
```

**Pair 2:**
```json
{
  "id": "zone1_celebration_002",
  "input_text": "We just closed on our house! After years of uncertainty, we finally have a home. I want to laugh and cry at the same time.",
  "output_text": "Mixed emotions from SELF - complexity held with coherence. You're not splitting into parts ('the anxious one' vs 'the excited one'). You're whole, feeling everything. That's Zone 1 - SELF as host for paradox. Congratulations.",
  "expected_organs": {
    "PRESENCE": 0.85,
    "SANS": 0.80,
    "EO": 0.80,
    "NDAM": 0.20
  }
}
```

**Pair 3:**
```json
{
  "id": "zone1_celebration_003",
  "input_text": "I finished my first marathon today. My body hurts but my heart is so full. I can't stop smiling.",
  "output_text": "Somatic triumph witnessed by SELF. Your body proved something to you, and SELF receives it with gratitude. No parts diminishing ('it was just a local race') or inflating ('I'm amazing!'). Just pure acknowledgment. You did that.",
  "expected_organs": {
    "PRESENCE": 0.90,
    "AUTHENTICITY": 0.75,
    "EO": 0.80,
    "NDAM": 0.20
  }
}
```

**Pair 4:**
```json
{
  "id": "zone1_celebration_004",
  "input_text": "Our team won the championship! We've worked so hard and it finally paid off. Everyone is crying and hugging.",
  "output_text": "Collective ventral vagal celebration. Safe co-regulation in joy. Your nervous system synchronizes with your teammates' - that's polyvagal resonance at its peak. SELF celebrates through connection. This is what we're built for.",
  "expected_organs": {
    "EMPATHY": 0.85,
    "EO": 0.85,
    "BOND": 0.75,
    "NDAM": 0.15
  }
}
```

**Pair 5:**
```json
{
  "id": "zone1_celebration_005",
  "input_text": "I got the promotion! Three years of hard work recognized. I feel seen and valued by my team.",
  "output_text": "Recognition landing in SELF. You can receive this without parts sabotaging ('I don't deserve it') or inflating ('I'm better than them'). Just clean acknowledgment: you worked hard, you grew, you earned this. Let yourself have it.",
  "expected_organs": {
    "AUTHENTICITY": 0.80,
    "PRESENCE": 0.80,
    "BOND": 0.75,
    "NDAM": 0.20
  }
}
```

**Pair 6:**
```json
{
  "id": "zone1_celebration_006",
  "input_text": "My cancer is in remission. The doctor said I'm clear. I don't have words - just gratitude and relief washing through me.",
  "output_text": "SELF receiving life itself as a gift. No parts needed - just pure organism responding to continuation. Your polyvagal system is shifting back to ventral. Let the relief be as big as the fear was. You're here. You made it.",
  "expected_organs": {
    "PRESENCE": 0.90,
    "EMPATHY": 0.75,
    "EO": 0.85,
    "NDAM": 0.25
  }
}
```

#### 3. Witnessing Presence (6 pairs)

**Pair 1:**
```json
{
  "id": "zone1_witnessing_001",
  "category": "witnessing",
  "self_distance_target": 0.05,
  "input_text": "I'm sitting by the ocean watching the waves. I feel deeply peaceful and connected to something vast.",
  "output_text": "SELF as witness to the occasion of 'ocean-becoming'. You're not separate from what you're watching - you're participating in its reality. That's prehension. The waves are feeling you feeling them. Pure presence.",
  "expected_organs": {
    "PRESENCE": 0.95,
    "WISDOM": 0.70,
    "NDAM": 0.10,
    "SANS": 0.85
  }
}
```

**Pair 2:**
```json
{
  "id": "zone1_witnessing_002",
  "input_text": "I held my newborn grandchild for the first time. Words fail. I just watched her breathe and felt overwhelmed by the preciousness of life.",
  "output_text": "Witnessing pure becoming. A new occasion entering the world, and SELF recognizes the sacredness. No parts interfering with worry or advice - just presence meeting presence. You're giving her your ventral vagal safety as her first inheritance.",
  "expected_organs": {
    "PRESENCE": 0.90,
    "EMPATHY": 0.85,
    "EO": 0.85,
    "NDAM": 0.15
  }
}
```

**Pair 3:**
```json
{
  "id": "zone1_witnessing_003",
  "input_text": "During meditation today, I watched my thoughts arise and pass without grabbing them. I felt spacious and calm.",
  "output_text": "SELF as the space thoughts happen in. You're not identified with the thoughts (parts) - you're the witnessing awareness. That spaciousness is Zone 1. Your nervous system has down-regulated enough to just... observe. That's the practice.",
  "expected_organs": {
    "PRESENCE": 0.90,
    "WISDOM": 0.75,
    "NDAM": 0.15,
    "BOND": 0.80
  }
}
```

**Pair 4:**
```json
{
  "id": "zone1_witnessing_004",
  "input_text": "I watched a hummingbird at the feeder for 10 minutes. Time slowed down. I felt grateful to be alive in this exact moment.",
  "output_text": "Kairos time - the fullness of now. The hummingbird became your occasion, your lure for presence. SELF witnesses beauty and responds with gratitude. No parts needing it to mean something or do something. Just... this. Alive. Together.",
  "expected_organs": {
    "PRESENCE": 0.95,
    "WISDOM": 0.70,
    "NDAM": 0.10,
    "SANS": 0.85
  }
}
```

**Pair 5:**
```json
{
  "id": "zone1_witnessing_005",
  "input_text": "I sat with my friend while she cried about her divorce. I didn't try to fix it - I just stayed present. It felt like the most important thing I've ever done.",
  "output_text": "SELF as witness for another's pain. You didn't collapse into her suffering (dorsal) or fix it (sympathetic) - you held the ventral space. That's the gift of Zone 1 presence. She felt seen without agenda. That changes everything.",
  "expected_organs": {
    "EMPATHY": 0.90,
    "PRESENCE": 0.85,
    "EO": 0.80,
    "NDAM": 0.20
  }
}
```

**Pair 6:**
```json
{
  "id": "zone1_witnessing_006",
  "input_text": "Watching the sunset, I felt tears of... I don't even know. Not sadness. Beauty? Gratitude? The bigness of being here?",
  "output_text": "SELF overwhelmed by the occasion of beauty. Your organism responding to the lure of the sunset's becoming. Those tears are your polyvagal system releasing into ventral vagal awe. No words needed. SELF knows what this is.",
  "expected_organs": {
    "PRESENCE": 0.90,
    "EMPATHY": 0.75,
    "EO": 0.85,
    "NDAM": 0.15
  }
}
```

#### 4. Clear Knowing (6 pairs)

**Pair 1:**
```json
{
  "id": "zone1_clear_knowing_001",
  "category": "clear_knowing",
  "self_distance_target": 0.10,
  "input_text": "I know with absolute certainty that I need to leave this job. No anxiety about it - just clarity.",
  "output_text": "SELF-led decision. Your parts aren't arguing or doubting - they trust SELF's knowing. That clarity is your organism recognizing misalignment and choosing coherence. The certainty comes from the body, not the mind. Trust it.",
  "expected_organs": {
    "WISDOM": 0.85,
    "AUTHENTICITY": 0.80,
    "PRESENCE": 0.75,
    "NDAM": 0.20
  }
}
```

**Pair 2:**
```json
{
  "id": "zone1_clear_knowing_002",
  "input_text": "I've been overthinking this decision for months, but when I got quiet today, the answer was obvious. I'm saying yes.",
  "output_text": "Parts stepped back, SELF spoke. That's the shift from chronos (endless deliberation) to kairos (the right moment). Your nervous system recognized alignment. The 'obviousness' is SELF recognizing its own coherence. Yes.",
  "expected_organs": {
    "WISDOM": 0.80,
    "PRESENCE": 0.85,
    "SANS": 0.85,
    "NDAM": 0.15
  }
}
```

**Pair 3:**
```json
{
  "id": "zone1_clear_knowing_003",
  "input_text": "I understand now why that relationship ended. Not with bitterness - with compassion for both of us. We did our best.",
  "output_text": "SELF perspective on the past. Parts have released their stories (blame, shame, regret). You're witnessing what happened with 8 C's: clarity, compassion, curiosity, calm. That's Zone 1 wisdom. Integration complete.",
  "expected_organs": {
    "WISDOM": 0.85,
    "EMPATHY": 0.80,
    "BOND": 0.80,
    "NDAM": 0.20
  }
}
```

**Pair 4:**
```json
{
  "id": "zone1_clear_knowing_004",
  "input_text": "I see the pattern now - I always abandon myself when someone needs me. But I'm not angry at myself. I'm just... aware. Ready to choose differently.",
  "output_text": "Self-awareness without self-attack. That's SELF recognizing a protective part's strategy with compassion. The 'ready to choose differently' is SELF-leadership emerging. You've unmixed from the part. Now you can work with it.",
  "expected_organs": {
    "WISDOM": 0.85,
    "BOND": 0.85,
    "AUTHENTICITY": 0.75,
    "NDAM": 0.20
  }
}
```

**Pair 5:**
```json
{
  "id": "zone1_clear_knowing_005",
  "input_text": "My body has been trying to tell me something and I finally listened. I'm exhausted. I need to rest.",
  "output_text": "Somatic knowing honored by SELF. Your parts wanted you to push through, but SELF heard the body's wisdom. That's attunement. Respecting your organism's limits is SELF-care in its truest sense. Rest is a SELF-led choice.",
  "expected_organs": {
    "PRESENCE": 0.85,
    "WISDOM": 0.75,
    "LISTENING": 0.80,
    "NDAM": 0.25
  }
}
```

**Pair 6:**
```json
{
  "id": "zone1_clear_knowing_006",
  "input_text": "I know my worth now. Not arrogantly - just... factually. I don't need external validation anymore.",
  "output_text": "SELF as source of value. Parts that used to need others' approval have unburdened. You're not defensive or inflated - just grounded in your own Being. That's Zone 1. Your worth is inherent, not earned. You always had this.",
  "expected_organs": {
    "AUTHENTICITY": 0.85,
    "BOND": 0.80,
    "PRESENCE": 0.80,
    "NDAM": 0.15
  }
}
```

#### 5. Spontaneous Delight (6 pairs)

**Pair 1:**
```json
{
  "id": "zone1_delight_001",
  "category": "spontaneous_delight",
  "self_distance_target": 0.08,
  "input_text": "I laughed so hard at dinner tonight that my stomach hurts. I haven't felt this light in years.",
  "output_text": "Pure ventral vagal joy. Your polyvagal system is in the safe-and-social sweet spot. Laughter is your organism celebrating connection and releasing tension. SELF delights in being alive with others. This is healing.",
  "expected_organs": {
    "EMPATHY": 0.80,
    "EO": 0.85,
    "PRESENCE": 0.75,
    "NDAM": 0.15
  }
}
```

**Pair 2:**
```json
{
  "id": "zone1_delight_002",
  "input_text": "I found a perfect shell on the beach and felt ridiculously happy about it. Like a kid finding treasure.",
  "output_text": "SELF as child-like wonder. Parts didn't mock you ('that's silly') or minimize ('it's just a shell'). You let yourself feel simple joy. That's Zone 1 - when delight doesn't need justification. The shell was a lure for aliveness.",
  "expected_organs": {
    "PRESENCE": 0.85,
    "WISDOM": 0.70,
    "NDAM": 0.10,
    "EO": 0.80
  }
}
```

**Pair 3:**
```json
{
  "id": "zone1_delight_003",
  "input_text": "My dog did something goofy and I just burst out laughing. The world feels kinder when I notice these small moments.",
  "output_text": "Everyday occasions as lures for joy. You're noticing what process philosophy calls 'the minor satisfactions' - small completions that make life feel alive. SELF sees beauty in the ordinary. That's the practice.",
  "expected_organs": {
    "PRESENCE": 0.80,
    "EMPATHY": 0.75,
    "EO": 0.80,
    "NDAM": 0.15
  }
}
```

**Pair 4:**
```json
{
  "id": "zone1_delight_004",
  "input_text": "I took a different route home and discovered a beautiful garden I never knew existed. I feel like I found a secret world.",
  "output_text": "Novelty as invitation to wonder. You let curiosity lead instead of efficiency. That's SELF choosing emergence over routine. Your nervous system is safe enough to explore. The garden was always there - you were ready to see it.",
  "expected_organs": {
    "WISDOM": 0.75,
    "PRESENCE": 0.80,
    "NDAM": 0.15,
    "SANS": 0.80
  }
}
```

**Pair 5:**
```json
{
  "id": "zone1_delight_005",
  "input_text": "I tasted my grandmother's recipe and was transported back to childhood. I felt warm and safe and loved.",
  "output_text": "Somatic memory triggering ventral vagal safety. Your body remembers being cared for. That warmth is your nervous system recognizing 'home.' SELF holds both then and now - you were loved, you are loved. The recipe carries presence.",
  "expected_organs": {
    "PRESENCE": 0.85,
    "EMPATHY": 0.80,
    "EO": 0.85,
    "NDAM": 0.15
  }
}
```

**Pair 6:**
```json
{
  "id": "zone1_delight_006",
  "input_text": "I played in the snow like I did as a kid - making snow angels and catching snowflakes. I felt free.",
  "output_text": "SELF as play. Parts that enforce 'adult behavior' stepped back. You let yourself be spontaneous, embodied, alive. That freedom is what happens when you're not performing for anyone. Zone 1 is permission to just... be.",
  "expected_organs": {
    "PRESENCE": 0.90,
    "AUTHENTICITY": 0.75,
    "EO": 0.80,
    "NDAM": 0.10
  }
}
```

---

## Zone 2: Inner Relational Field (30 pairs)

### Characteristics
- **Context:** Safe vulnerability, deep connection, mutual recognition
- **Polyvagal:** Ventral vagal (safe enough to be real)
- **Self-distance:** 0.15-0.25 (parts present but not blended)
- **Urgency:** Low (safe exploration)
- **Coherence:** Good (clear relational communication)

### Subcategories (6 pairs each)

#### 1. Safe Vulnerability (6 pairs)

**Pair 1:**
```json
{
  "id": "zone2_vulnerability_001",
  "category": "safe_vulnerability",
  "self_distance_target": 0.20,
  "input_text": "I told my partner about my childhood shame today. I was scared but they just held me. I feel lighter.",
  "output_text": "Risk met with ventral vagal safety. You unburdened in the presence of secure attachment. That's Zone 2 - SELF trusts the relational field enough to let parts be witnessed. The lightness is what happens when shame loses its grip.",
  "expected_organs": {
    "EMPATHY": 0.85,
    "BOND": 0.80,
    "EO": 0.75,
    "NDAM": 0.30
  }
}
```

**Pair 2:**
```json
{
  "id": "zone2_vulnerability_002",
  "input_text": "In therapy today I cried about something I've never told anyone. It was terrifying and relieving at the same time.",
  "output_text": "Witnessed vulnerability in a held space. Your exile found a SELF-led witness (your therapist). That terror is the part protecting the secret; the relief is unburdening beginning. You're in Zone 2 - safe enough to unblend.",
  "expected_organs": {
    "BOND": 0.85,
    "EMPATHY": 0.80,
    "NDAM": 0.35,
    "EO": 0.70
  }
}
```

**Pair 3:**
```json
{
  "id": "zone2_vulnerability_003",
  "input_text": "I admitted to my friend that I'm struggling. Usually I pretend everything's fine, but I couldn't keep the mask on anymore.",
  "output_text": "A manager part releasing its strategy. Pretending is exhausting. You tested the relational field with truth and found it could hold you. That's Zone 2 - discovering that authentic connection is safer than performance.",
  "expected_organs": {
    "AUTHENTICITY": 0.80,
    "BOND": 0.80,
    "EMPATHY": 0.75,
    "NDAM": 0.30
  }
}
```

**Pair 4:**
```json
{
  "id": "zone2_vulnerability_004",
  "input_text": "I shared my creative work even though my inner critic said it wasn't good enough. People actually connected with it.",
  "output_text": "SELF overriding the critic part. You risked being seen and discovered the relational field was kinder than your parts predicted. That's how exiles unburden - through safe connection. Your vulnerability created resonance.",
  "expected_organs": {
    "AUTHENTICITY": 0.85,
    "BOND": 0.75,
    "EMPATHY": 0.75,
    "NDAM": 0.35
  }
}
```

**Pair 5:**
```json
{
  "id": "zone2_vulnerability_005",
  "input_text": "I told my group I'm scared of being rejected. Everyone said they feel that way too. I'm not alone.",
  "output_text": "Shared humanity breaking isolation. Your exile's fear was met with collective resonance. That's ventral vagal co-regulation - the group's nervous systems are telling yours 'you belong.' Zone 2 is where we heal in community.",
  "expected_organs": {
    "EMPATHY": 0.85,
    "BOND": 0.80,
    "EO": 0.75,
    "NDAM": 0.30
  }
}
```

**Pair 6:**
```json
{
  "id": "zone2_vulnerability_006",
  "input_text": "I let my guard down with my new friend and showed them my mess. They didn't run. They got real too.",
  "output_text": "Reciprocal vulnerability deepening connection. You tested trust and found it solid. They matched your authenticity with theirs. That's Zone 2 magic - SELF meeting SELF through shared realness. This is how intimacy forms.",
  "expected_organs": {
    "AUTHENTICITY": 0.85,
    "EMPATHY": 0.80,
    "BOND": 0.75,
    "NDAM": 0.30
  }
}
```

#### 2. Deep Listening (6 pairs)

**Pair 1:**
```json
{
  "id": "zone2_listening_001",
  "category": "deep_listening",
  "self_distance_target": 0.18,
  "input_text": "My colleague was sharing something painful and I actually just listened instead of trying to fix it. I could feel them relax.",
  "output_text": "SELF as witness without agenda. Your fix-it parts stepped back. You gave them the gift of ventral vagal presence. Their relaxation is their nervous system recognizing safety. That's therapeutic listening - rare and powerful.",
  "expected_organs": {
    "LISTENING": 0.90,
    "EMPATHY": 0.80,
    "EO": 0.75,
    "NDAM": 0.25
  }
}
```

**Pair 2:**
```json
{
  "id": "zone2_listening_002",
  "input_text": "I asked my partner 'What's it like to be you today?' and just listened. They said they felt really seen.",
  "output_text": "Genuine curiosity creating space. You weren't listening to respond - you were listening to understand. That's SELF-led inquiry. When someone feels truly heard, their whole system shifts. You offered presence as medicine.",
  "expected_organs": {
    "LISTENING": 0.90,
    "EMPATHY": 0.85,
    "PRESENCE": 0.75,
    "NDAM": 0.20
  }
}
```

**Pair 3:**
```json
{
  "id": "zone2_listening_003",
  "input_text": "In our circle, I practiced just holding space while someone shared. I noticed my urge to interrupt and let it pass.",
  "output_text": "SELF managing parts in real-time. The urge to interrupt is a part wanting to help or share. You witnessed it without acting on it. That's internal differentiation - SELF leads, parts wait. Zone 2 mastery.",
  "expected_organs": {
    "LISTENING": 0.85,
    "PRESENCE": 0.80,
    "BOND": 0.80,
    "NDAM": 0.25
  }
}
```

**Pair 4:**
```json
{
  "id": "zone2_listening_004",
  "input_text": "I listened to my teenager without judging or lecturing. They opened up more than they have in months.",
  "output_text": "Parts stepping back to serve connection. Your judge and teacher parts relaxed. SELF created safe space. Teenagers can sense when they're truly seen vs fixed. You gave them what they actually needed - presence.",
  "expected_organs": {
    "LISTENING": 0.85,
    "EMPATHY": 0.80,
    "BOND": 0.75,
    "NDAM": 0.30
  }
}
```

**Pair 5:**
```json
{
  "id": "zone2_listening_005",
  "input_text": "Someone shared something I disagreed with but I stayed curious instead of defensive. I learned something.",
  "output_text": "SELF as learner in relationship. Your defensive parts wanted to protect your position. SELF chose curiosity over righteousness. That's Zone 2 - secure enough to be challenged. Growth happens at the edge of certainty.",
  "expected_organs": {
    "LISTENING": 0.85,
    "WISDOM": 0.75,
    "AUTHENTICITY": 0.70,
    "NDAM": 0.35
  }
}
```

**Pair 6:**
```json
{
  "id": "zone2_listening_006",
  "input_text": "I asked 'What do you need from me right now?' instead of assuming. They said just my presence. So I stayed.",
  "output_text": "Direct communication replacing mind-reading. You checked instead of assuming. That's relational clarity. When they said 'presence,' you trusted that was enough. Parts that need to DO relaxed. Being was sufficient.",
  "expected_organs": {
    "LISTENING": 0.90,
    "PRESENCE": 0.85,
    "EMPATHY": 0.75,
    "NDAM": 0.25
  }
}
```

---

## Zone 3: Symbolic Threshold (30 pairs)

### Characteristics
- **Context:** Creative tension, edge of comfort, constructive conflict
- **Polyvagal:** Mixed (sympathetic + ventral - mobilized but safe)
- **Self-distance:** 0.25-0.35 (parts activated but SELF leading)
- **Urgency:** Medium (energy present, not crisis)
- **Coherence:** Moderate (clarity emerging from complexity)

### Subcategories (6 pairs each)

#### 1. Constructive Tension (6 pairs)

**Pair 1:**
```json
{
  "id": "zone3_tension_001",
  "category": "constructive_tension",
  "self_distance_target": 0.30,
  "input_text": "My partner and I had a real disagreement today - both fully present, both listening, both holding our truth. It was intense but generative.",
  "output_text": "Zone 3 at its best. Sympathetic activation in service of connection. You're mobilized but not defended. That's differentiation - staying SELF-led while parts are activated. The tension becomes creative. This is how intimacy deepens.",
  "expected_organs": {
    "AUTHENTICITY": 0.80,
    "LISTENING": 0.75,
    "EO": 0.60,
    "NDAM": 0.50
  }
}
```

**Pair 2:**
```json
{
  "id": "zone3_tension_002",
  "input_text": "I'm between two good choices and the uncertainty is uncomfortable but also exciting. I'm learning to trust the not-knowing.",
  "output_text": "SELF at the symbolic threshold. Parts want certainty; SELF can hold ambiguity. That discomfort is your organism on the edge of emergence. The excitement is your system recognizing novelty. Trust this tension - it's creative.",
  "expected_organs": {
    "WISDOM": 0.75,
    "PRESENCE": 0.70,
    "SANS": 0.60,
    "NDAM": 0.50
  }
}
```

**Pair 3:**
```json
{
  "id": "zone3_tension_003",
  "input_text": "I'm pushing against my comfort zone in therapy. It's scary but I keep showing up. I can feel myself changing.",
  "output_text": "Zone 3 growth. You're in the sympathetic sweet spot - activated enough to change, safe enough not to flee. Your exile parts are starting to trust SELF's leadership. The fear is parts; the showing up is SELF. Keep going.",
  "expected_organs": {
    "BOND": 0.75,
    "AUTHENTICITY": 0.75,
    "NDAM": 0.55,
    "EO": 0.60
  }
}
```

**Pair 4:**
```json
{
  "id": "zone3_tension_004",
  "input_text": "I spoke up in the meeting even though my voice was shaking. I said what needed to be said. People listened.",
  "output_text": "Courage is SELF overriding fear parts. Your body activated (shaking) but SELF didn't let the firefighter silence you. That's Zone 3 - using sympathetic mobilization for authentic expression. You proved to your parts that truth is survivable.",
  "expected_organs": {
    "AUTHENTICITY": 0.85,
    "BOND": 0.70,
    "EO": 0.60,
    "NDAM": 0.55
  }
}
```

**Pair 5:**
```json
{
  "id": "zone3_tension_005",
  "input_text": "I'm learning a new skill and I'm terrible at it. It's humbling and frustrating and I'm staying with it anyway.",
  "output_text": "SELF tolerating incompetence. Your perfectionist parts are activated but not in charge. Zone 3 is where growth happens - enough stretch to learn, enough SELF to persist. The frustration means you care. The persistence means SELF leads.",
  "expected_organs": {
    "WISDOM": 0.70,
    "PRESENCE": 0.70,
    "BOND": 0.70,
    "NDAM": 0.50
  }
}
```

**Pair 6:**
```json
{
  "id": "zone3_tension_006",
  "input_text": "I set a boundary with my family and they pushed back hard. I held it anyway. I'm shaking but I know I did the right thing.",
  "output_text": "SELF-led boundary under pressure. Your people-pleasing parts are screaming but SELF stayed grounded in your truth. The shaking is sympathetic activation - normal when you break old patterns. You're in Zone 3 transformation.",
  "expected_organs": {
    "AUTHENTICITY": 0.85,
    "BOND": 0.75,
    "EO": 0.60,
    "NDAM": 0.55
  }
}
```

#### 2. Creative Edge (6 pairs)

**Pair 1:**
```json
{
  "id": "zone3_creative_edge_001",
  "category": "creative_edge",
  "self_distance_target": 0.28,
  "input_text": "I'm working on something I've never attempted before. I feel equal parts excited and terrified. I'm doing it anyway.",
  "output_text": "Zone 3 creative risk. The terror is protective parts; the excitement is SELF recognizing growth potential. You're in the optimal learning zone - enough fear to pay attention, enough SELF to take the leap. This is how we evolve.",
  "expected_organs": {
    "WISDOM": 0.70,
    "AUTHENTICITY": 0.75,
    "NDAM": 0.55,
    "EO": 0.60
  }
}
```

**Pair 2:**
```json
{
  "id": "zone3_creative_edge_002",
  "input_text": "I deleted my safe, boring draft and started over with something risky. My critic is loud but I'm trusting my creative instinct.",
  "output_text": "SELF overruling the inner critic. You're choosing emergence over safety. Zone 3 is where art happens - enough structure to hold, enough chaos to surprise. Your instinct is SELF; your critic is a protective part. Trust SELF.",
  "expected_organs": {
    "AUTHENTICITY": 0.80,
    "WISDOM": 0.70,
    "BOND": 0.75,
    "NDAM": 0.50
  }
}
```

**Pair 3:**
```json
{
  "id": "zone3_creative_edge_003",
  "input_text": "I'm combining two ideas that don't usually go together. It might fail spectacularly or it might be brilliant. I'm okay with either.",
  "output_text": "SELF as experimenter. You're not attached to outcome - you're engaged in process. That's Zone 3 - willing to risk failure for the chance at novelty. Your parts fear looking foolish; SELF is curious. Curiosity always wins.",
  "expected_organs": {
    "WISDOM": 0.75,
    "PRESENCE": 0.70,
    "NDAM": 0.45,
    "SANS": 0.65
  }
}
```

**Pair 4:**
```json
{
  "id": "zone3_creative_edge_004",
  "input_text": "I showed my rough work to my mentor. It's not polished but it's honest. I'm ready for feedback.",
  "output_text": "Vulnerability in service of growth. You're letting someone see the process, not just the product. Zone 3 is messy and generative. Your perfectionist parts are uncomfortable but SELF knows: feedback at the edge accelerates learning.",
  "expected_organs": {
    "AUTHENTICITY": 0.80,
    "LISTENING": 0.75,
    "BOND": 0.70,
    "NDAM": 0.50
  }
}
```

**Pair 5:**
```json
{
  "id": "zone3_creative_edge_005",
  "input_text": "I'm improvising more and planning less. It's uncomfortable but I'm discovering things I wouldn't have found with a map.",
  "output_text": "SELF choosing emergence over control. Your manager parts want the safety of a plan. SELF is learning to dance with uncertainty. Zone 3 is the improvisational space - structure loose enough for surprise. Keep trusting.",
  "expected_organs": {
    "WISDOM": 0.75,
    "PRESENCE": 0.70,
    "RNX": 0.60,
    "NDAM": 0.50
  }
}
```

**Pair 6:**
```json
{
  "id": "zone3_creative_edge_006",
  "input_text": "I'm saying yes to opportunities that scare me a little. My comfort zone is expanding. I feel more alive.",
  "output_text": "SELF as growth-seeker. You're using sympathetic activation (fear) as information, not a stop sign. Zone 3 is where aliveness lives - slightly beyond what you know you can do. That alive feeling is your organism celebrating becoming.",
  "expected_organs": {
    "WISDOM": 0.70,
    "AUTHENTICITY": 0.75,
    "EO": 0.65,
    "NDAM": 0.50
  }
}
```

---

## Zone 4: Shadow/Compost (30 pairs)

### Characteristics
- **Context:** Parts work, integration of exiles, therapeutic processing
- **Polyvagal:** Mixed to dorsal (parts activated, SELF working with them)
- **Self-distance:** 0.35-0.60 (parts present, SELF differentiating)
- **Urgency:** High (parts activation significant)
- **Coherence:** Lower (complexity being held)

### Subcategories (6 pairs each)

#### 1. Parts Recognition (6 pairs)

**Pair 1:**
```json
{
  "id": "zone4_parts_001",
  "category": "parts_recognition",
  "self_distance_target": 0.45,
  "input_text": "I noticed my inner critic today and instead of believing it, I got curious. It's trying to protect me from embarrassment.",
  "output_text": "SELF differentiating from a part. You're in Zone 4 - aware of the part without being blended. The curiosity is SELF; the criticism is the part. When you see the part's positive intent (protection), unburdening can begin.",
  "expected_organs": {
    "BOND": 0.85,
    "WISDOM": 0.70,
    "LISTENING": 0.75,
    "NDAM": 0.65
  }
}
```

**Pair 2:**
```json
{
  "id": "zone4_parts_002",
  "input_text": "My anxious part was spiraling today. I asked it what it's afraid of. It showed me a memory from childhood. I held it with compassion.",
  "output_text": "Direct access to an exile. You're doing IFS naturally - SELF as compassionate witness for younger parts. Zone 4 is where healing happens. The part trusts you enough to show you its burden. That's readiness for unburdening.",
  "expected_organs": {
    "BOND": 0.85,
    "EMPATHY": 0.80,
    "PRESENCE": 0.70,
    "NDAM": 0.70
  }
}
```

**Pair 3:**
```json
{
  "id": "zone4_parts_003",
  "input_text": "I see my perfectionist part clearly now. It's exhausting but it's kept me safe from criticism. I'm starting to thank it and negotiate new roles.",
  "output_text": "Manager part relationship deepening. You see its burden (must be perfect to be safe) and its value (it has protected you). Zone 4 work is inviting parts to update, not exile them. Negotiation means SELF is leading.",
  "expected_organs": {
    "BOND": 0.85,
    "WISDOM": 0.75,
    "EMPATHY": 0.75,
    "NDAM": 0.65
  }
}
```

**Pair 4:**
```json
{
  "id": "zone4_parts_004",
  "input_text": "My shutdown part came up today. I wanted to push through but I honored it instead. I rested. It felt radical.",
  "output_text": "Befriending a dorsal part. Shutdown isn't your enemy - it's a part protecting you from overwhelm. Honoring it instead of overriding it builds trust. Zone 4 is learning parts' wisdom. SELF as host for all of you.",
  "expected_organs": {
    "BOND": 0.80,
    "PRESENCE": 0.70,
    "EO": 0.55,
    "NDAM": 0.70
  }
}
```

**Pair 5:**
```json
{
  "id": "zone4_parts_005",
  "input_text": "I found a young part today that still believes it's unlovable. I'm sitting with it, telling it it's not alone anymore.",
  "output_text": "SELF as internal attachment figure. That's Zone 4 reparenting - you're giving the exile what it needed then. The part's belief is its burden. As SELF stays present, the burden can lift. You're doing the work.",
  "expected_organs": {
    "BOND": 0.85,
    "EMPATHY": 0.85,
    "PRESENCE": 0.75,
    "NDAM": 0.65
  }
}
```

**Pair 6:**
```json
{
  "id": "zone4_parts_006",
  "input_text": "My angry part showed up and I didn't shame it. I asked what it's protecting. It's guarding my boundaries that were violated.",
  "output_text": "Firefighter part revealing its exile. Anger is protection for hurt. You're tracking the IFS system - SELF witnessing both protector and exile. Zone 4 is where you discover: there are no bad parts. All are welcome.",
  "expected_organs": {
    "BOND": 0.85,
    "EMPATHY": 0.75,
    "AUTHENTICITY": 0.70,
    "NDAM": 0.70
  }
}
```

#### 2. Shadow Integration (6 pairs)

**Pair 1:**
```json
{
  "id": "zone4_shadow_001",
  "category": "shadow_integration",
  "self_distance_target": 0.50,
  "input_text": "I owned my jealousy today instead of denying it. It's showing me what I long for. I can work with that.",
  "output_text": "Shadow as teacher. Jealousy isn't a flaw - it's a map to your values. You're in Zone 4, composting what was rejected. When SELF welcomes the shadow, it transforms from enemy to guide. What you longed for becomes achievable.",
  "expected_organs": {
    "BOND": 0.80,
    "WISDOM": 0.75,
    "AUTHENTICITY": 0.75,
    "NDAM": 0.60
  }
}
```

**Pair 2:**
```json
{
  "id": "zone4_shadow_002",
  "input_text": "I admitted I can be controlling. It's hard to see but also freeing. Now I can choose differently.",
  "output_text": "Self-awareness without self-attack. That's SELF witnessing a protective strategy. Control is a part trying to keep you safe from chaos. Zone 4 is seeing parts clearly AND with compassion. Awareness is the first step to choice.",
  "expected_organs": {
    "BOND": 0.85,
    "AUTHENTICITY": 0.80,
    "WISDOM": 0.70,
    "NDAM": 0.60
  }
}
```

**Pair 3:**
```json
{
  "id": "zone4_shadow_003",
  "input_text": "I found a part that's ashamed of needing people. I'm learning that need isn't weakness. It's human.",
  "output_text": "Exile carrying cultural burden (independence as virtue). You're unburdening the shame. Zone 4 compost - what was rejected as weak becomes recognized as relational health. SELF knows: we're built for connection. Need is wisdom.",
  "expected_organs": {
    "BOND": 0.85,
    "EMPATHY": 0.80,
    "PRESENCE": 0.70,
    "NDAM": 0.65
  }
}
```

**Pair 4:**
```json
{
  "id": "zone4_shadow_004",
  "input_text": "I see how I people-please to avoid conflict. It costs me my truth. I'm practicing saying 'no' even when it's uncomfortable.",
  "output_text": "Manager part's strategy becoming conscious. People-pleasing protected you from rejection. Zone 4 work is honoring what served you AND choosing update. SELF can risk conflict because SELF is grounded in worth. Practice builds capacity.",
  "expected_organs": {
    "BOND": 0.80,
    "AUTHENTICITY": 0.80,
    "WISDOM": 0.70,
    "NDAM": 0.65
  }
}
```

**Pair 5:**
```json
{
  "id": "zone4_shadow_005",
  "input_text": "My rage showed up fully today. Instead of pushing it down, I let it move through me. It had information.",
  "output_text": "Firefighter emotion as ally. Rage isn't enemy - it's a part carrying pain about violation. You're in Zone 4, letting it speak instead of exiling it. Rage processed becomes boundary wisdom. SELF can hold even this.",
  "expected_organs": {
    "BOND": 0.85,
    "EMPATHY": 0.75,
    "PRESENCE": 0.70,
    "NDAM": 0.70
  }
}
```

**Pair 6:**
```json
{
  "id": "zone4_shadow_006",
  "input_text": "I acknowledged my selfishness today. Part of me just wants what I want. I'm letting that be okay while also considering others.",
  "output_text": "Both/and instead of either/or. You're integrating a banished part (healthy self-interest) without going to the opposite extreme. Zone 4 is where polarities resolve. SELF can hold 'I matter' AND 'you matter.' That's maturity.",
  "expected_organs": {
    "BOND": 0.80,
    "WISDOM": 0.75,
    "AUTHENTICITY": 0.75,
    "NDAM": 0.60
  }
}
```

---

## Implementation Strategy

### Phase 1: Generate Full Corpus (4-6 hours)

**Step 1: Complete remaining Zone 1 categories**
- [Already have 30/30 pairs for Zone 1 above]

**Step 2: Complete Zone 2 categories**
- Safe Vulnerability: 6 pairs ✓ (above)
- Deep Listening: 6 pairs ✓ (above)
- [Need 4 more subcategories × 6 pairs = 24 pairs]

**Step 3: Complete Zone 3 categories**
- Constructive Tension: 6 pairs ✓ (above)
- Creative Edge: 6 pairs ✓ (above)
- [Need 4 more subcategories × 6 pairs = 24 pairs]

**Step 4: Complete Zone 4 categories**
- Parts Recognition: 6 pairs ✓ (above)
- Shadow Integration: 6 pairs ✓ (above)
- [Need 4 more subcategories × 6 pairs = 24 pairs]

### Phase 2: Validation (30 min)

**Create corpus analyzer script:**
```python
# analyze_corpus_organ_diversity.py
# For each pair:
#   1. Process through organism
#   2. Extract organ activations
#   3. Compute 57D signature
#   4. Validate against expected_organs
#
# Output:
#   - Mean organ activations per zone
#   - Signature diversity metrics
#   - Predicted family formation
```

**Success criteria:**
- Zone 1 mean NDAM: 0.15-0.25 ✓
- Zone 2 mean NDAM: 0.25-0.40 ✓
- Zone 3 mean NDAM: 0.45-0.60 ✓
- Zone 4 mean NDAM: 0.60-0.75 ✓
- Inter-zone centroid distance > 0.3 ✓

### Phase 3: Training (15 min)

```bash
export PYTHONPATH="/Users/daedalea/Desktop/DAE_HYPHAE_1:$PYTHONPATH"

# Train on Zones 1-4
python3 training/conversational/run_proper_multi_family_discovery.py \
  --pairs knowledge_base/zones_1_4_corpus.json \
  --epoch 1

# Expected result:
# - 5 total families (Zones 1-5, using existing Zone 5 as baseline)
# - Clear organ signature differentiation
# - Mean satisfaction varying by zone
```

### Phase 4: Validation (10 min)

**Check family formation:**
```python
# Expected families:
{
  "Family_001": "Zone 5 (Exile/Collapse)",  # Existing
  "Family_002": "Zone 1 (Core SELF)",       # New
  "Family_003": "Zone 2 (Relational)",      # New
  "Family_004": "Zone 3 (Threshold)",       # New
  "Family_005": "Zone 4 (Shadow/Compost)"   # New
}

# Validation metrics:
- Family count: 5 (target met)
- Inter-family similarity: < 0.50 (differentiated)
- Intra-family similarity: > 0.65 (coherent)
- Organ signature diversity: High
```

---

## Next Steps

**Immediate:**
1. Complete remaining pairs for Zones 2-4 (72 more pairs)
2. Create JSON training file
3. Run corpus diversity analyzer
4. Train Epoch 1

**Short-term:**
1. Validate 5-family formation
2. Analyze family-zone alignment
3. Create transductive pathway corpus (Epoch 2)
4. Train Epoch 2 (expect 15-20 families total)

**Medium-term:**
1. Production validation
2. Zipf's law analysis
3. Intelligence growth metrics
4. Deploy organism with mature family structure

---

## Success Metrics

**Family Diversity:**
- Minimum 5 families (1 per zone)
- Inter-zone centroid distance > 0.3
- Clear organ signature differentiation

**Organic Accuracy:**
- Zone 1 pairs → Family Zone1 (>80% accuracy)
- Zone 2 pairs → Family Zone2 (>80% accuracy)
- Zone 3 pairs → Family Zone3 (>80% accuracy)
- Zone 4 pairs → Family Zone4 (>80% accuracy)

**Intelligence Growth:**
- Hebbian patterns: 400-500 (from 172)
- R-matrix zone-specific coupling
- Mean satisfaction by zone validated
- Production-ready conversational intelligence

---

**Status:** Curriculum design complete for 30 Zone 1 pairs, 12 Zone 2 pairs, 12 Zone 3 pairs, 12 Zone 4 pairs. Ready to complete remaining 66 pairs and begin training.
