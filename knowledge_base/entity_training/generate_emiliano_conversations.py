"""
Emiliano Entity Corpus Generator

Generates realistic entity-rich conversations for entity-situated training.
Maintains consistent entity graph while varying contexts and emotional tones.

Usage:
    python generate_emiliano_conversations.py --count 90 --output emiliano_entity_corpus.json
"""

import json
import random
from pathlib import Path
from typing import Dict, List


class EmilianoConversationGenerator:
    """
    Generate realistic conversations for Emiliano with consistent entity graph.

    Strategy:
    - Vary phrasing and contexts while maintaining entity consistency
    - Distribute epochs realistically (1-50)
    - Ensure expected organ/polyvagal patterns align with context
    - Create natural variation in entity salience and co-occurrence
    """

    def __init__(self):
        # Load conversation templates
        self.templates = {
            'family_safe': [
                {
                    "template": "{daughter} {action} and it just {feeling}. These are the moments I live for.",
                    "entities": ["daughter"],
                    "organs": {"BOND": 0.85, "EMPATHY": 0.75, "PRESENCE": 0.70},
                    "polyvagal": "ventral",
                    "v0": 0.25,
                    "zone": 1
                },
                {
                    "template": "Watching {daughter} {activity} at the {place} today. Such pure joy on {pronoun} face.",
                    "entities": ["daughter", "place"],
                    "organs": {"BOND": 0.80, "PRESENCE": 0.75, "EMPATHY": 0.70},
                    "polyvagal": "ventral",
                    "v0": 0.28,
                    "zone": 1
                },
                {
                    "template": "{daughter} said the sweetest thing today: '{quote}'. My heart is so full.",
                    "entities": ["daughter"],
                    "organs": {"BOND": 0.88, "EMPATHY": 0.80, "PRESENCE": 0.65},
                    "polyvagal": "ventral",
                    "v0": 0.22,
                    "zone": 1
                },
                {
                    "template": "Morning cuddles with {daughter} before {activity}. These quiet moments together mean everything.",
                    "entities": ["daughter", "home"],
                    "organs": {"BOND": 0.85, "PRESENCE": 0.78, "EMPATHY": 0.72},
                    "polyvagal": "ventral",
                    "v0": 0.26,
                    "zone": 1
                },
                {
                    "template": "{daughter} and {daughter2} playing together {where}. Hearing them laugh together is the best sound.",
                    "entities": ["daughter", "daughter2", "place"],
                    "organs": {"BOND": 0.82, "PRESENCE": 0.75, "EMPATHY": 0.70},
                    "polyvagal": "ventral",
                    "v0": 0.27,
                    "zone": 1
                },
            ],

            'family_worry': [
                {
                    "template": "I'm worried about {daughter} and {concern}. Am I {worry_question}?",
                    "entities": ["daughter"],
                    "organs": {"BOND": 0.80, "WISDOM": 0.65, "PRESENCE": 0.68},
                    "polyvagal": "mixed",
                    "v0": 0.50,
                    "zone": 2,
                    "urgency": 0.4
                },
                {
                    "template": "{daughter} is {struggle} and I don't know how to help. Feeling {emotion}.",
                    "entities": ["daughter"],
                    "organs": {"BOND": 0.78, "AUTHENTICITY": 0.70, "WISDOM": 0.62},
                    "polyvagal": "sympathetic",
                    "v0": 0.58,
                    "zone": 3,
                    "urgency": 0.5,
                    "self_distance": 0.5
                },
                {
                    "template": "Talked to {partner} about {concern} with {daughter}. We're both {feeling} but trying to stay present.",
                    "entities": ["partner", "daughter"],
                    "organs": {"BOND": 0.75, "EMPATHY": 0.72, "WISDOM": 0.65},
                    "polyvagal": "mixed",
                    "v0": 0.48,
                    "zone": 2,
                    "urgency": 0.3
                },
            ],

            'work_stress': [
                {
                    "template": "The {work_stressor} at {place} is {intensity}. I can feel {body_sensation}.",
                    "entities": ["work"],
                    "organs": {"NDAM": 0.85, "AUTHENTICITY": 0.70, "SANS": 0.65},
                    "polyvagal": "sympathetic",
                    "v0": 0.72,
                    "zone": 3,
                    "urgency": 0.8
                },
                {
                    "template": "{colleague} and I {work_event}. The {emotion} is palpable.",
                    "entities": ["colleague", "work"],
                    "organs": {"NDAM": 0.78, "EMPATHY": 0.68, "AUTHENTICITY": 0.72},
                    "polyvagal": "sympathetic",
                    "v0": 0.65,
                    "zone": 3,
                    "urgency": 0.6
                },
                {
                    "template": "Another {work_event} about {work_stressor}. I'm starting to wonder {existential_question}.",
                    "entities": ["work"],
                    "organs": {"NDAM": 0.75, "WISDOM": 0.68, "AUTHENTICITY": 0.72},
                    "polyvagal": "mixed",
                    "v0": 0.58,
                    "zone": 2,
                    "urgency": 0.5
                },
            ],

            'relationship': [
                {
                    "template": "{partner} and I {couple_activity} tonight. {feeling_statement}.",
                    "entities": ["partner", "home"],
                    "organs": {"EMPATHY": 0.75, "PRESENCE": 0.78, "BOND": 0.72},
                    "polyvagal": "ventral",
                    "v0": 0.32,
                    "zone": 1
                },
                {
                    "template": "Tension with {partner} about {issue}. We're both {emotion} and I'm not sure {worry}.",
                    "entities": ["partner"],
                    "organs": {"AUTHENTICITY": 0.75, "EMPATHY": 0.70, "BOND": 0.65},
                    "polyvagal": "sympathetic",
                    "v0": 0.55,
                    "zone": 3,
                    "urgency": 0.4,
                    "self_distance": 0.4
                },
            ],

            'self_care': [
                {
                    "template": "Made time for {activity} at {place} today. {body_awareness}.",
                    "entities": ["place"],
                    "organs": {"PRESENCE": 0.75, "AUTHENTICITY": 0.68, "RNX": 0.70},
                    "polyvagal": "mixed",
                    "v0": 0.42,
                    "zone": 2
                },
                {
                    "template": "Took a {activity} this morning. Just {experience}. I needed that.",
                    "entities": [],
                    "organs": {"PRESENCE": 0.78, "RNX": 0.72, "AUTHENTICITY": 0.65},
                    "polyvagal": "ventral",
                    "v0": 0.35,
                    "zone": 1
                },
            ]
        }

        # Substitution vocabularies
        self.vocab = {
            'daughter': ['Emma', 'Lily'],
            'daughter2': ['Lily', 'Emma'],
            'partner': ['Sofia'],
            'colleague': ['Alex'],
            'place': ['park', 'home'],
            'work': ['work'],

            # Actions and activities
            'action': [
                'smiled at me across the dinner table',
                'took my hand while we were walking',
                'ran to me when I got home',
                'fell asleep on my chest',
                'asked me to read her favorite story again',
                'wanted to help me make breakfast'
            ],
            'activity': [
                'playing on the swings',
                'drawing pictures',
                'building with blocks',
                'splashing in puddles',
                'chasing butterflies',
                'pretending to be a doctor'
            ],
            'feeling': [
                'filled my heart',
                'made everything else fade away',
                'reminded me what matters',
                'made me grateful to be her dad'
            ],

            # Family worry
            'concern': [
                'starting school',
                'making friends',
                'her shyness',
                'separation anxiety',
                'her nightmares',
                'eating habits'
            ],
            'struggle': [
                'having trouble sleeping',
                'acting out at preschool',
                'refusing to share toys',
                'being so clingy lately',
                'having meltdowns'
            ],
            'worry_question': [
                'doing something wrong',
                'being too soft',
                'being too strict',
                'missing something important',
                'equipped for this'
            ],

            # Work stress
            'work_stressor': [
                'deadline pressure',
                'funding uncertainty',
                'team conflict',
                'technical debt',
                'scope creep',
                'leadership expectations'
            ],
            'work_event': [
                'had another tense standup',
                'got pulled into an urgent meeting',
                'stayed late to debug',
                'had to have a difficult conversation',
                'reviewed the roadmap again'
            ],
            'intensity': [
                'relentless',
                'overwhelming',
                'crushing',
                'exhausting',
                'unsustainable'
            ],
            'body_sensation': [
                'my shoulders tensing up',
                'my jaw clenching',
                'my chest tightening',
                'the weight of it all',
                'my energy draining'
            ],

            # Relationship
            'couple_activity': [
                'had a real conversation',
                'watched a movie together',
                'cooked dinner as a team',
                'took a walk',
                'just sat in comfortable silence'
            ],
            'issue': [
                'parenting styles',
                'my work hours',
                'household responsibilities',
                'our lack of couple time',
                'money stress'
            ],

            # Self-care
            'activity': [
                'the gym',
                'a walk',
                'some stretching',
                'meditation',
                'reading'
            ],
            'experience': [
                'being in my body',
                'noticing my breath',
                'feeling the tension release',
                'being present with myself',
                'letting go for a moment'
            ],
            'body_awareness': [
                'Felt my body start to release some tension',
                'Noticed how much I needed to move',
                'My body is grateful',
                'Starting to feel more grounded',
                'Reconnecting with physical sensation'
            ],

            # General
            'emotion': [
                'stressed',
                'overwhelmed',
                'worried',
                'uncertain',
                'anxious',
                'conflicted'
            ],
            'feeling_statement': [
                'It felt good to reconnect',
                'We both needed that',
                'Reminded me why I love her',
                'Simple moments like this matter',
                'Grateful for her partnership'
            ],
            'existential_question': [
                'if this is sustainable',
                'if I should look for something else',
                "what I'm sacrificing for this job",
                'if the stress is worth it'
            ],
            'where': [
                'at home',
                'at the park',
                'in the backyard',
                'before bedtime'
            ],
            'pronoun': ['her', 'his', 'their'],
            'quote': [
                "I love you to the moon and back",
                "You're the best daddy ever",
                "Can we do this again tomorrow?",
                "I feel safe with you"
            ]
        }

    def generate_conversation(
        self,
        conv_id: str,
        category: str,
        template_data: Dict
    ) -> Dict:
        """Generate a single conversation from template"""

        # Fill in template
        text = template_data['template']
        for key in self.vocab:
            if '{' + key + '}' in text:
                text = text.replace('{' + key + '}', random.choice(self.vocab[key]))

        # Build entities list
        entities = []
        entity_map = {
            'Emma': 'Person',
            'Lily': 'Person',
            'Sofia': 'Person',
            'Alex': 'Person',
            'Rich': 'Person',
            'work': 'Place',
            'park': 'Place',
            'home': 'Place',
            'gym': 'Place',
            'kindergarten': 'Place'
        }

        # Extract entities from text
        for entity_name, entity_type in entity_map.items():
            if entity_name in text:
                relationship_map = {
                    'Emma': 'HAS_DAUGHTER',
                    'Lily': 'HAS_DAUGHTER',
                    'Sofia': 'PARTNER',
                    'Alex': 'COLLEAGUE_FRIEND',
                    'Rich': 'FRIEND'
                }
                entity = {
                    'entity_value': entity_name,
                    'entity_type': entity_type,
                    'salience': 0.85 + random.uniform(-0.10, 0.10)
                }
                if entity_name in relationship_map:
                    entity['relationship'] = relationship_map[entity_name]
                entities.append(entity)

        # Generate epoch distribution (5 epochs between 1-50)
        epochs = sorted(random.sample(range(1, 51), 5))

        conversation = {
            'conversation_id': conv_id,
            'category': category,
            'epoch_distribution': epochs,
            'input': text,
            'entities': entities,
            'expected_patterns': template_data.copy()
        }
        # Remove template key from expected_patterns
        del conversation['expected_patterns']['template']
        del conversation['expected_patterns']['entities']

        return conversation

    def generate_corpus(
        self,
        target_counts: Dict[str, int],
        existing_conversations: List[Dict]
    ) -> List[Dict]:
        """Generate full corpus to reach target counts"""

        # Count existing by category
        from collections import Counter
        existing_counts = Counter(c['category'] for c in existing_conversations)

        all_conversations = existing_conversations.copy()
        conv_counter = len(existing_conversations) + 1

        for category, target in target_counts.items():
            current = existing_counts[category]
            needed = target - current

            print(f"Generating {needed} conversations for {category}...")

            for i in range(needed):
                # Pick random template
                template = random.choice(self.templates[category])

                conv_id = f"emiliano_{conv_counter:03d}_{category}"
                conversation = self.generate_conversation(conv_id, category, template)
                all_conversations.append(conversation)
                conv_counter += 1

        return all_conversations


def main():
    """Generate expanded Emiliano corpus"""

    # Load existing corpus
    corpus_path = Path('knowledge_base/entity_training/emiliano_entity_corpus.json')
    with open(corpus_path, 'r') as f:
        corpus = json.load(f)

    # Target counts
    target_counts = {
        'family_safe': 30,
        'family_worry': 20,
        'work_stress': 25,
        'relationship': 15,
        'self_care': 10
    }

    # Generate
    generator = EmilianoConversationGenerator()
    expanded_conversations = generator.generate_corpus(
        target_counts,
        corpus['conversations']
    )

    # Update corpus
    corpus['conversations'] = expanded_conversations
    corpus['corpus_metadata']['total_conversations'] = len(expanded_conversations)
    corpus['corpus_metadata']['generated_date'] = "2025-11-15"

    # Save
    with open(corpus_path, 'w') as f:
        json.dump(corpus, f, indent=2)

    print(f"\n✅ Corpus generated: {len(expanded_conversations)} total conversations")
    print(f"   Saved to: {corpus_path}")

    # Summary by category
    from collections import Counter
    counts = Counter(c['category'] for c in expanded_conversations)
    print(f"\nBreakdown by category:")
    for cat, count in sorted(counts.items()):
        print(f"  {cat}: {count}")


if __name__ == '__main__':
    main()
