#!/usr/bin/env python3
"""
Linguistic Ground Truth Corpus Generator
=========================================

Creates a comprehensive corpus of English sentences with full linguistic annotations:
- POS tags (parts of speech)
- Entity types (PERSON, LOCATION, ORG, etc.)
- Dependencies (syntactic relationships)
- Noun chunks (phrases)
- Entity boundaries (multi-word entities)

This corpus establishes the foundational linguistic intelligence needed for
word-occasion learning and felt-to-text propositions in Process Philosophy AI.

Author: DAE_HYPHAE_1 Team + Claude Code
Date: November 19, 2025
Status: Phase 0A Foundation - Linguistic Ground Truth
"""

import json
import spacy
from pathlib import Path
from typing import List, Dict, Any

# Load spaCy English model
print("Loading spaCy model...")
try:
    nlp = spacy.load("en_core_web_sm")
    print("✅ spaCy model loaded successfully")
except OSError:
    print("❌ spaCy model not found. Installing...")
    import subprocess
    subprocess.run(["python3", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")
    print("✅ spaCy model installed and loaded")


def annotate_sentence(text: str, category: str = "general") -> Dict[str, Any]:
    """
    Generate full linguistic ground truth for a sentence.

    Args:
        text: Input sentence
        category: Category label for corpus organization

    Returns:
        Dict with tokens, entities, noun_chunks, dependencies
    """
    doc = nlp(text)

    # Token-level annotations
    tokens = []
    for i, token in enumerate(doc):
        tokens.append({
            "index": i,
            "word": token.text,
            "pos": token.pos_,  # Part of speech (NOUN, VERB, ADJ, etc.)
            "tag": token.tag_,  # Fine-grained POS (NNP, VBZ, etc.)
            "lemma": token.lemma_,  # Base form
            "dep": token.dep_,  # Dependency relation
            "is_entity": token.ent_type_ != "",
            "entity_type": token.ent_type_ if token.ent_type_ else None,
            "entity_iob": token.ent_iob_,  # B-PERSON, I-PERSON, O
            "head_index": token.head.i if token.head != token else i,
            "is_stop": token.is_stop,
            "is_punct": token.is_punct,
            "is_alpha": token.is_alpha,
            "is_digit": token.is_digit
        })

    # Entity-level annotations
    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "start": ent.start,
            "end": ent.end,
            "type": ent.label_,
            "confidence": 1.0  # Ground truth
        })

    # Noun chunk annotations (for multi-word entity learning)
    noun_chunks = []
    for chunk in doc.noun_chunks:
        noun_chunks.append({
            "text": chunk.text,
            "start": chunk.start,
            "end": chunk.end,
            "root": chunk.root.text,
            "root_pos": chunk.root.pos_
        })

    return {
        "text": text,
        "category": category,
        "tokens": tokens,
        "entities": entities,
        "noun_chunks": noun_chunks,
        "sentence_count": len(list(doc.sents))
    }


# ============================================================================
# CORPUS SENTENCES - Organized by Category
# ============================================================================

CORPUS_SENTENCES = {

    # Category 1: Basic Syntax (100 sentences)
    # Learn: sentence structure, basic POS patterns
    "basic_syntax": [
        # Simple sentences (SVO)
        "Emma walks.",
        "She talks.",
        "Dogs bark.",
        "Birds fly.",
        "Children play.",

        # Compound sentences
        "Emma walks and talks.",
        "She runs and jumps.",
        "Dogs bark and cats meow.",
        "Birds fly and fish swim.",
        "Children play and learn.",

        # Complex sentences
        "Emma, who is my daughter, walks to school.",
        "She talks when she is happy.",
        "Dogs bark because they hear noises.",
        "Birds fly where they find food.",
        "Children play after they finish homework.",

        # Questions
        "Who is Emma?",
        "What does she do?",
        "Where do dogs live?",
        "When do birds fly?",
        "Why do children play?",

        # Negations
        "Emma does not walk.",
        "She is not talking.",
        "Dogs do not always bark.",
        "Birds cannot swim.",
        "Children should not run.",

        # Modal verbs
        "Emma can walk.",
        "She should talk.",
        "Dogs might bark.",
        "Birds will fly.",
        "Children must learn.",

        # Progressive tenses
        "Emma is walking.",
        "She was talking.",
        "Dogs are barking.",
        "Birds were flying.",
        "Children will be playing.",

        # Perfect tenses
        "Emma has walked.",
        "She had talked.",
        "Dogs have barked.",
        "Birds had flown.",
        "Children will have played.",

        # Passive voice
        "The book was read by Emma.",
        "The song is sung by her.",
        "The ball was thrown by dogs.",
        "The nest is built by birds.",
        "The game is won by children.",
    ],

    # Category 2: Entity Types (200 sentences)
    # Learn: PERSON, LOCATION, ORG, TIME, etc.
    "entity_types": [
        # PERSON entities
        "Emma is my daughter.",
        "Dr. Smith is a physician.",
        "President Biden spoke today.",
        "My friend Sarah called.",
        "The CEO John Anderson resigned.",
        "Emma Smith lives in New York.",
        "Dr. Jane Doe works at the hospital.",
        "Mayor Johnson announced the plan.",
        "Professor Williams teaches biology.",
        "Coach Martinez trains the team.",

        # LOCATION entities
        "I live in New York.",
        "She moved to California.",
        "They visited Paris last year.",
        "The office is in Manhattan.",
        "We went to Central Park.",
        "The hospital is on Fifth Avenue.",
        "She works at Mount Sinai Hospital.",
        "The conference is in San Francisco.",
        "He traveled to Tokyo.",
        "The restaurant is in Brooklyn.",

        # ORGANIZATION entities
        "Google announced new products.",
        "Apple released the iPhone.",
        "Microsoft is based in Seattle.",
        "The United Nations met today.",
        "Harvard University offers scholarships.",
        "The World Health Organization warned.",
        "Amazon expanded its services.",
        "The Federal Reserve raised rates.",
        "NASA launched a mission.",
        "Tesla produces electric vehicles.",

        # TIME entities
        "I saw her yesterday.",
        "The meeting is tomorrow.",
        "We met last week.",
        "The event is next month.",
        "She arrived in November.",
        "The deadline is Friday.",
        "We start at 9 AM.",
        "The concert is tonight.",
        "I called her this morning.",
        "They left last year.",

        # MONEY entities
        "The cost is 100 dollars.",
        "She earned $50,000 last year.",
        "The price increased by 20 percent.",
        "He paid fifty euros.",
        "The budget is $2 million.",

        # QUANTITY entities
        "I bought three apples.",
        "She has two cats.",
        "There are fifty students.",
        "We need five volunteers.",
        "The box weighs ten pounds.",

        # Mixed entity types
        "Emma Smith works at Google in New York.",
        "Dr. Jones joined Harvard University last month.",
        "The CEO visited the Paris office yesterday.",
        "President Biden spoke at the United Nations.",
        "Sarah moved to California for Apple.",
    ],

    # Category 3: Pronouns & Coreference (100 sentences)
    # Learn: pronoun resolution, entity continuity
    "pronouns_coreference": [
        # Subject pronouns
        "Emma is worried. She called me.",
        "My daughter is sick. She has a fever.",
        "The doctor is busy. He is seeing patients.",
        "The nurses are tired. They worked all night.",
        "John and I are friends. We meet often.",

        # Object pronouns
        "I saw Emma. I told her the news.",
        "The boss called John. She wants to see him.",
        "My parents are visiting. I will meet them.",
        "Sarah found the keys. She gave them to me.",
        "The teacher graded the tests. She returned them.",

        # Possessive pronouns
        "Emma lost her phone.",
        "John forgot his wallet.",
        "The company changed its policy.",
        "My parents sold their house.",
        "The dog wagged its tail.",

        # Reflexive pronouns
        "Emma taught herself to code.",
        "I made myself breakfast.",
        "They organized themselves.",
        "She prepared herself for the test.",
        "We introduced ourselves.",

        # Demonstrative pronouns
        "This is my daughter Emma.",
        "That is her office.",
        "These are the documents.",
        "Those are my colleagues.",
        "This is important.",

        # Relative pronouns
        "Emma, who is my daughter, called.",
        "The doctor whom I trust recommended this.",
        "The book that I read was great.",
        "The person whose car broke down called.",
        "The place where we met was beautiful.",

        # Multi-sentence coreference
        "My daughter Emma is anxious. She has been struggling lately. I want to help her.",
        "Dr. Smith is excellent. He has 20 years of experience. I trust him completely.",
        "The hospital is nearby. It has good facilities. We chose it for that reason.",
    ],

    # Category 4: Multi-word Entities (100 sentences)
    # Learn: entity boundary detection, phrase coherence
    "multi_word_entities": [
        # Multi-word PERSON names
        "Emma Smith is my daughter.",
        "Dr. Jane Doe works here.",
        "President Joe Biden spoke.",
        "Mayor Eric Adams announced.",
        "Professor Sarah Williams teaches.",
        "Coach Mike Martinez trains.",
        "Senator Elizabeth Warren voted.",
        "CEO Tim Cook presented.",
        "Director James Cameron filmed.",
        "Author J.K. Rowling wrote.",

        # Multi-word LOCATION names
        "We live in New York City.",
        "She moved to Los Angeles.",
        "They visited San Francisco.",
        "The office is in Silicon Valley.",
        "We went to Central Park.",
        "The hospital is on Fifth Avenue.",
        "She works in Times Square.",
        "He traveled to Hong Kong.",
        "The meeting is in Washington D.C.",
        "We stayed at the Grand Canyon.",

        # Multi-word ORGANIZATION names
        "Google LLC announced products.",
        "Apple Inc. released earnings.",
        "Microsoft Corporation is growing.",
        "The United Nations met today.",
        "Harvard Medical School offers programs.",
        "The World Health Organization warned.",
        "Amazon Web Services expanded.",
        "The Federal Reserve Bank decided.",
        "NASA Jet Propulsion Laboratory built it.",
        "Tesla Motors produces vehicles.",

        # Multi-word TIME expressions
        "I saw her last week.",
        "The meeting is next Monday.",
        "We met two years ago.",
        "The event is this coming Friday.",
        "She arrived last November.",
        "The deadline is end of month.",
        "We start early next year.",
        "The concert is tomorrow night.",
        "I called her this past weekend.",
        "They left three days ago.",

        # Complex multi-word phrases
        "The Chief Executive Officer of Apple Inc. presented.",
        "Mount Sinai Hospital in New York City is excellent.",
        "The United States of America voted.",
        "New York University School of Medicine trains doctors.",
        "The Supreme Court of the United States ruled.",
    ],

    # Category 5: Relationships & Context (100 sentences)
    # Learn: relational context, entity roles
    "relationships_context": [
        # Family relationships
        "My daughter Emma is worried.",
        "Her son John is sick.",
        "Our mother called yesterday.",
        "His father works at Google.",
        "Their sister lives in California.",
        "My parents are visiting.",
        "Her brother is a doctor.",
        "Our grandmother is 90 years old.",
        "His uncle owns a restaurant.",
        "Their cousin moved to Texas.",

        # Professional relationships
        "My boss Sarah is demanding.",
        "Her colleague John is helpful.",
        "Our manager announced changes.",
        "His coworker is on vacation.",
        "Their supervisor approved it.",
        "My professor teaches well.",
        "Her mentor is supportive.",
        "Our director made decisions.",
        "His assistant is efficient.",
        "Their team leader organized.",

        # Social relationships
        "My friend Emma called.",
        "Her neighbor is friendly.",
        "Our roommate is messy.",
        "His partner is understanding.",
        "Their classmate is smart.",
        "My colleague is helpful.",
        "Her best friend moved.",
        "Our mutual friend connected us.",
        "His old friend visited.",
        "Their childhood friend wrote.",

        # Possessive relationships
        "Emma's mother is concerned.",
        "John's car broke down.",
        "The company's CEO resigned.",
        "Sarah's apartment is spacious.",
        "The dog's owner called.",
        "The hospital's director spoke.",
        "Google's products are innovative.",
        "The team's performance improved.",
        "The city's mayor announced.",
        "The university's president decided.",

        # Complex relational contexts
        "My daughter Emma, who works at Google, called from New York.",
        "Dr. Smith, our family physician, recommended the specialist.",
        "The CEO of Apple, Tim Cook, presented the quarterly results.",
        "My colleague Sarah, who is from California, moved to Texas.",
        "Professor Williams, the department chair, approved the proposal.",
    ],

    # Category 6: Sentiment & Emotion (50 sentences)
    # Learn: affective states, polyvagal cues
    "sentiment_emotion": [
        # Positive emotions
        "Emma is happy.",
        "She feels joyful.",
        "I am excited.",
        "They are grateful.",
        "We feel content.",

        # Negative emotions
        "Emma is worried.",
        "She feels anxious.",
        "I am sad.",
        "They are frustrated.",
        "We feel disappointed.",

        # Emotional intensity
        "Emma is very happy.",
        "She is extremely worried.",
        "I am somewhat concerned.",
        "They are quite pleased.",
        "We are deeply moved.",

        # Emotional transitions
        "Emma was worried but now she is calm.",
        "I felt anxious until the results came.",
        "She seemed sad when I saw her.",
        "They appeared happy at the event.",
        "We became concerned after hearing the news.",
    ],

    # ============================================================================
    # Phase 0A.5: CONVERSATIONAL VOCABULARY EXPANSION (450 sentences)
    # Added: November 19, 2025
    # Purpose: Fill critical gaps identified in Phase 0A coverage analysis
    # ============================================================================

    # Category 7: Emotional Expression (100 sentences)
    # Learn: feeling, stressed, anxious, nervous, calm, relieved, overwhelmed
    "emotional_expression": [
        # Core emotional vocabulary
        "I'm feeling stressed about work today.",
        "She's feeling anxious about the test results.",
        "We're feeling overwhelmed by all the changes.",
        "He's feeling calm after the meditation.",
        "They're feeling nervous before the presentation.",
        "I'm feeling relieved now that it's over.",
        "She's feeling excited about the new opportunity.",
        "We're feeling hopeful about the future.",

        # Emotional states with causes
        "I feel stressed when I have too much work.",
        "She feels anxious before important meetings.",
        "He feels overwhelmed when things pile up.",
        "They feel calm in nature.",
        "We feel nervous about big decisions.",
        "I feel relieved after talking to someone.",
        "She feels excited when planning trips.",
        "He feels hopeful despite the challenges.",

        # Gradations of feeling
        "I'm feeling a bit stressed lately.",
        "She's feeling quite anxious these days.",
        "We're feeling very overwhelmed right now.",
        "He's feeling much calmer than before.",
        "They're feeling slightly nervous still.",
        "I'm feeling extremely relieved.",
        "She's feeling incredibly excited.",
        "We're feeling cautiously hopeful.",

        # Feeling + temporal markers
        "I was feeling stressed yesterday.",
        "She's been feeling anxious all week.",
        "We've been feeling overwhelmed lately.",
        "He started feeling calm this morning.",
        "They'll be feeling nervous tomorrow.",
        "I stopped feeling relieved too soon.",
        "She keeps feeling excited about it.",
        "We continue feeling hopeful.",

        # Feeling + about/with/from
        "I'm feeling stressed about my daughter Emma.",
        "She's feeling anxious about her health.",
        "We're feeling overwhelmed with everything.",
        "He's feeling calm about the decision.",
        "They're feeling nervous about the outcome.",
        "I'm feeling relieved from the news.",
        "She's feeling excited about seeing her family.",
        "We're feeling hopeful for better times.",

        # Combinations with other emotions
        "I'm feeling both stressed and excited.",
        "She's feeling anxious but hopeful.",
        "We're feeling overwhelmed yet determined.",
        "He's feeling calm and confident.",
        "They're feeling nervous and curious.",
        "I'm feeling relieved and grateful.",
        "She's feeling excited and scared.",
        "We're feeling hopeful and realistic.",

        # Physical manifestations of feelings
        "I feel stressed in my shoulders.",
        "She feels anxious in her stomach.",
        "We feel overwhelmed and exhausted.",
        "He feels calm and relaxed.",
        "They feel nervous energy building.",
        "I feel relieved physically.",
        "She feels excited tingles.",
        "We feel hopeful lightness.",

        # Comparative feelings
        "I'm feeling more stressed than usual.",
        "She's feeling less anxious than yesterday.",
        "We're feeling as overwhelmed as before.",
        "He's feeling calmer than he expected.",
        "They're feeling more nervous now.",
        "I'm feeling much more relieved.",
        "She's feeling equally excited.",
        "We're feeling just as hopeful.",

        # Feeling in context
        "I'm feeling stressed at work but calm at home.",
        "She's feeling anxious about Emma's health.",
        "We're feeling overwhelmed by the medical bills.",
        "He's feeling calm after yoga class.",
        "They're feeling nervous before the surgery.",
        "I'm feeling relieved the tests came back normal.",
        "She's feeling excited for the weekend.",
        "We're feeling hopeful things will improve.",

        # Questions about feelings
        "Are you feeling stressed?",
        "Is she feeling anxious?",
        "How are you feeling now?",
        "When did you start feeling overwhelmed?",
        "Why is he feeling calm?",
        "Has anyone been feeling nervous?",
        "Do you feel relieved?",
        "Can you describe what you're feeling?",

        # Feeling + person
        "My daughter is feeling anxious.",
        "Emma is feeling stressed about school.",
        "My friend is feeling overwhelmed.",
        "The doctor says I'm feeling normal stress.",
        "My family is feeling hopeful.",
        "My coworker is feeling nervous.",
        "My therapist says feeling anxious is okay.",
        "Everyone is feeling somewhat stressed.",

        # Negations
        "I'm not feeling stressed anymore.",
        "She isn't feeling anxious today.",
        "We're no longer feeling overwhelmed.",
        "He's never felt this calm before.",
        "They don't feel nervous at all.",
        "I wasn't feeling relieved initially.",
        "She's hardly feeling excited.",
        "We can't keep feeling hopeless.",

        # Feeling progression
        "I started feeling stressed last month.",
        "She gradually began feeling less anxious.",
        "We suddenly felt completely overwhelmed.",
        "He slowly became calmer.",
        "They immediately felt nervous.",
        "I eventually felt relieved.",
        "She quickly grew excited.",
        "We're starting to feel more hopeful.",
    ],

    # Category 8: Temporal Continuity (80 sentences)
    # Learn: yesterday, tomorrow, morning, evening, afternoon, tonight, later
    "temporal_continuity": [
        # Yesterday
        "Yesterday I talked to my doctor about Emma.",
        "She went to work yesterday morning.",
        "We visited the hospital yesterday afternoon.",
        "He felt better yesterday evening.",
        "They arrived yesterday at noon.",
        "I saw Emma yesterday after school.",
        "She called me yesterday night.",
        "We discussed this yesterday.",

        # Tomorrow
        "Tomorrow I have an appointment with my therapist.",
        "She's meeting Emma tomorrow morning.",
        "We're going to the clinic tomorrow afternoon.",
        "He'll feel better by tomorrow evening.",
        "They're arriving tomorrow at six.",
        "I'll see the doctor tomorrow.",
        "She'll call tomorrow night.",
        "We'll talk about it tomorrow.",

        # Morning
        "This morning I woke up feeling worried.",
        "She goes to work every morning.",
        "We have coffee in the morning.",
        "He exercises each morning.",
        "They meditate every morning.",
        "I saw Emma this morning.",
        "She felt anxious this morning.",
        "We'll meet tomorrow morning.",

        # Evening
        "This evening we're having dinner together.",
        "She comes home every evening at seven.",
        "We relax in the evening.",
        "He reads each evening.",
        "They talk every evening after work.",
        "I felt better this evening.",
        "She'll arrive this evening.",
        "We spoke yesterday evening.",

        # Afternoon
        "This afternoon I'm meeting my friend.",
        "She naps every afternoon.",
        "We work in the afternoon.",
        "He has therapy each afternoon.",
        "They play cards every afternoon.",
        "I saw the doctor this afternoon.",
        "She felt tired this afternoon.",
        "We'll finish by late afternoon.",

        # Tonight
        "Tonight I'm staying home to rest.",
        "She's coming over tonight.",
        "We're having a family dinner tonight.",
        "He's working late tonight.",
        "They're sleeping early tonight.",
        "I'll call Emma tonight.",
        "She feels nervous about tonight.",
        "We'll decide tonight.",

        # Later
        "I'll call you back later today.",
        "She said she'd come by later.",
        "We can discuss this later.",
        "He'll feel better later on.",
        "They're meeting up later tonight.",
        "I'll finish this later.",
        "She mentioned it earlier, I'll check later.",
        "We'll see what happens later.",

        # Combined temporal references
        "Yesterday morning I felt anxious, but this evening I'm calm.",
        "Tomorrow afternoon we're meeting, then dinner later that evening.",
        "She works mornings and I work evenings.",
        "He called yesterday, I'll call him back tomorrow.",
        "They arrived this morning and leave tomorrow night.",
        "I saw Emma yesterday, I'll see her again tomorrow.",
        "She felt stressed yesterday evening but better this morning.",
        "We talked this afternoon about meeting tomorrow morning.",

        # With feeling vocabulary
        "I felt stressed yesterday but I'm calm today.",
        "She's been anxious since yesterday morning.",
        "We'll feel better tomorrow after the appointment.",
        "He was overwhelmed yesterday evening.",
        "They're feeling nervous about tomorrow.",
        "I'm relieved this evening is finally here.",
        "She'll be excited tomorrow morning.",
        "We felt hopeful yesterday afternoon.",
    ],

    # Category 9: Spatial Context (80 sentences)
    # Learn: work, home, hospital, office, school, park, downtown
    "spatial_context": [
        # At work
        "I'm at work right now with my colleague.",
        "She goes to work every morning.",
        "We're stressed about work lately.",
        "He's leaving work early today.",
        "They work at the hospital downtown.",
        "I feel anxious at work sometimes.",
        "She called from work this afternoon.",
        "We talked about work yesterday evening.",

        # At home
        "She's at home resting after the surgery.",
        "I feel calm when I'm at home.",
        "We're staying home tonight.",
        "He works from home now.",
        "They came home late yesterday.",
        "I left my phone at home.",
        "She feels safe at home.",
        "We'll be home by evening.",

        # At hospital
        "We met at the hospital near downtown.",
        "I'm going to the hospital tomorrow morning.",
        "She works at the hospital.",
        "He's been in the hospital since yesterday.",
        "They visited me at the hospital.",
        "I felt anxious at the hospital.",
        "She's leaving the hospital today.",
        "We'll meet at the hospital entrance.",

        # At office
        "I'll be at the office until late tonight.",
        "She has an office downtown.",
        "We're meeting at my office tomorrow.",
        "He called from his office this morning.",
        "They're renovating the office.",
        "I feel stressed at the office lately.",
        "She left the office early yesterday.",
        "We'll discuss this at the office.",

        # At school
        "Emma goes to school every morning.",
        "I pick her up from school each afternoon.",
        "She teaches at the school downtown.",
        "He's doing well at school now.",
        "They're meeting at the school tonight.",
        "I feel nervous about school events.",
        "She called from school yesterday.",
        "We visited the school last week.",

        # At park
        "We walk in the park every evening.",
        "I saw them at the park yesterday.",
        "She feels calm at the park.",
        "He runs in the park each morning.",
        "They're meeting at the park tomorrow.",
        "I'll be at the park this afternoon.",
        "She goes to the park with Emma.",
        "We talked at the park yesterday evening.",

        # Downtown
        "I work downtown near the hospital.",
        "She lives downtown now.",
        "We're meeting downtown tomorrow afternoon.",
        "He goes downtown every day for work.",
        "They moved downtown last year.",
        "I feel overwhelmed by downtown traffic.",
        "She has an office downtown.",
        "We'll eat downtown tonight.",

        # Combinations
        "I go from home to work every morning.",
        "She's at the hospital but she'll be home tonight.",
        "We work downtown and live near the park.",
        "He leaves school and goes to the park.",
        "They meet at the office then go downtown.",
        "I'll be at work tomorrow and home tomorrow evening.",
        "She went from the hospital to home yesterday.",
        "We're going from home to the park this afternoon.",

        # With emotional context
        "I feel stressed at work but calm at home.",
        "She felt anxious at the hospital yesterday.",
        "We feel hopeful since leaving the hospital.",
        "He feels overwhelmed at the office lately.",
        "They're feeling nervous about going to the hospital tomorrow.",
        "I felt relieved leaving work yesterday evening.",
        "She feels excited going downtown tonight.",
        "We feel peaceful at the park.",
    ],

    # Category 10: Evaluative Expressions (70 sentences)
    # Learn: better, worse, like, prefer, good, bad, fine, okay
    "evaluative_expressions": [
        # Better
        "I'm feeling better than yesterday.",
        "She's getting better every day.",
        "We're doing better now.",
        "He feels much better this morning.",
        "Things are better than before.",
        "I hope she gets better soon.",
        "She's better at this than me.",
        "We'll feel better tomorrow.",

        # Worse
        "I'm feeling worse than yesterday.",
        "She's getting worse despite treatment.",
        "We're doing worse financially.",
        "He feels worse in the evening.",
        "Things are worse than we thought.",
        "I'm worried she'll get worse.",
        "She's handling it worse than before.",
        "We felt worse last week.",

        # Like
        "I like spending time with Emma.",
        "She likes going to the park.",
        "We like our new doctor.",
        "He doesn't like hospitals.",
        "They like working from home.",
        "I'd like to feel better.",
        "She likes how calm she feels.",
        "We like this new approach.",

        # Prefer
        "I prefer morning appointments.",
        "She prefers working from home.",
        "We prefer to talk about it tomorrow.",
        "He prefers the hospital downtown.",
        "They prefer meeting at the park.",
        "I'd prefer feeling less anxious.",
        "She prefers evenings for relaxing.",
        "We prefer discussing this later.",

        # Good
        "I feel good about this decision.",
        "She's doing really good now.",
        "We had a good talk yesterday.",
        "He got good news this morning.",
        "Things look good for tomorrow.",
        "I'm in good hands at the hospital.",
        "She feels good about going home.",
        "We're making good progress.",

        # Bad
        "I feel bad about missing work.",
        "She had a bad day yesterday.",
        "We got bad news this morning.",
        "He's having a bad reaction.",
        "Things don't look too bad.",
        "I felt bad for her.",
        "She doesn't feel that bad anymore.",
        "We're through the worst of it, it's not bad now.",

        # Fine
        "I'm fine now, thank you.",
        "She's doing fine after the surgery.",
        "We'll be fine by tomorrow.",
        "He says he's fine but I'm worried.",
        "Things are fine at work.",
        "I feel fine about going home.",
        "She looks fine this morning.",
        "We're fine with that plan.",

        # Okay
        "I'm okay with waiting until tomorrow.",
        "She's okay, just tired.",
        "We're doing okay considering everything.",
        "He said it's okay to feel anxious.",
        "Things will be okay eventually.",
        "I don't feel okay about this.",
        "She's okay with the new schedule.",
        "We'll be okay, we always are.",

        # Combinations
        "I'm feeling better but not good yet.",
        "She prefers home but she's okay at work.",
        "We like the doctor, she's really good.",
        "He's doing fine, better than yesterday but not completely good.",
        "Things are okay now but they were worse before.",
        "I'd prefer to feel better but I'm okay for now.",
    ],

    # Category 11: Mental States (60 sentences)
    # Learn: think, want, need, understand, know, believe, mean
    "mental_states": [
        # Think
        "I think Emma is worried about her exam.",
        "She thinks we should wait until tomorrow.",
        "We think the doctor is right.",
        "He thinks it's getting better.",
        "They think I'm doing well.",
        "I think I need more rest.",
        "She thinks about it every day.",
        "We think things will improve.",

        # Want
        "I want to feel better soon.",
        "She wants to go home.",
        "We want to talk about Emma.",
        "He wants to try a different approach.",
        "They want us to come tomorrow.",
        "I want my daughter to be happy.",
        "She wants to understand what's happening.",
        "We want to know the results.",

        # Need
        "I need to rest this afternoon.",
        "She needs to see the doctor.",
        "We need to talk about this.",
        "He needs more time to recover.",
        "They need to know by tomorrow.",
        "I need my family right now.",
        "She needs to feel less anxious.",
        "We need better options.",

        # Understand
        "I understand how you feel.",
        "She understands the situation.",
        "We understand it takes time.",
        "He doesn't understand why.",
        "They understand our concerns.",
        "I need you to understand this.",
        "She's trying to understand.",
        "We understand each other better now.",

        # Know
        "I know Emma is stressed.",
        "She knows how I feel.",
        "We know it's not easy.",
        "He knows the doctor well.",
        "They know what we're going through.",
        "I want to know the truth.",
        "She knows better than anyone.",
        "We know things will get better.",

        # Believe
        "I believe she'll get better.",
        "She believes in positive thinking.",
        "We believe the treatment is working.",
        "He believes I'm making progress.",
        "They believe we can handle this.",
        "I believe in taking time to heal.",
        "She believes Emma will be fine.",
        "We believe things happen for a reason.",

        # Mean
        "I mean what I said yesterday.",
        "She means well, I know.",
        "We mean to help, not hurt.",
        "What do you mean by that?",
        "He didn't mean to worry us.",
        "They mean a lot to me.",
        "I know what you mean.",
        "She means we should wait until tomorrow.",
    ],

    # Category 12: Multi-word Phrases (60 sentences)
    # Learn: looking forward to, dealing with, talking about, worried about, at home, at work, by myself
    "multi_word_phrases": [
        # Looking forward to
        "I'm looking forward to seeing my family.",
        "She's looking forward to going home.",
        "We're looking forward to better days.",
        "He's looking forward to the weekend.",
        "They're looking forward to the results.",
        "I'm looking forward to feeling better.",
        "She's looking forward to tomorrow evening.",
        "We're not looking forward to the appointment.",

        # Dealing with
        "I'm dealing with a lot right now.",
        "She's dealing with Emma's anxiety.",
        "We're dealing with this together.",
        "He's dealing with work stress.",
        "They're dealing with health issues.",
        "I'm learning to deal with uncertainty.",
        "She's been dealing with this for weeks.",
        "We dealt with worse before.",

        # Talking about
        "I'm talking about my feelings more now.",
        "She's talking about seeing a therapist.",
        "We're talking about moving closer to the hospital.",
        "He's talking about changing jobs.",
        "They're talking about us.",
        "I want to talk about Emma.",
        "She's been talking about this for days.",
        "We talked about it yesterday evening.",

        # Worried about
        "I'm worried about my daughter Emma.",
        "She's worried about the test results.",
        "We're worried about money.",
        "He's worried about work.",
        "They're worried about me.",
        "I'm not worried about tomorrow.",
        "She's always worried about something.",
        "We were worried about you.",

        # At home / At work
        "I feel better at home than at work.",
        "She works at home now.",
        "We're at home this evening.",
        "He's at work until late tonight.",
        "They're comfortable at home.",
        "I left it at home this morning.",
        "She feels stressed at work lately.",
        "We'll talk when you get home.",

        # By myself / With others
        "I need some time by myself.",
        "She's doing this by herself.",
        "We can't do this by ourselves.",
        "He prefers being by himself.",
        "They're not by themselves, we're here.",
        "I'm not alone, I'm with my family.",
        "She's with Emma at the park.",
        "We're going together, not by ourselves.",

        # Combined multi-word phrases
        "I'm looking forward to being at home by myself tomorrow.",
        "She's dealing with feeling worried about work.",
        "We're talking about what we're looking forward to.",
        "He's worried about dealing with this by himself.",
        "They're at home talking about tomorrow.",
    ],
}


def generate_corpus(output_path: str = "knowledge_base/linguistic_ground_truth_corpus.json"):
    """
    Generate the complete linguistic ground truth corpus.

    Args:
        output_path: Path to save the corpus JSON file
    """
    print("=" * 80)
    print("🧠 LINGUISTIC GROUND TRUTH CORPUS GENERATOR")
    print("=" * 80)
    print()

    corpus = {
        "metadata": {
            "version": "1.0",
            "created": "2025-11-19",
            "purpose": "Phase 0A linguistic foundation for Process Philosophy AI",
            "total_sentences": 0,
            "categories": list(CORPUS_SENTENCES.keys())
        },
        "training_pairs": []
    }

    pair_id = 0

    for category, sentences in CORPUS_SENTENCES.items():
        print(f"📝 Processing category: {category} ({len(sentences)} sentences)")

        for i, sentence in enumerate(sentences):
            pair_id += 1

            # Annotate sentence with spaCy
            ground_truth = annotate_sentence(sentence, category)

            # Create training pair
            training_pair = {
                "pair_id": f"{category}_{i:03d}",
                "global_id": pair_id,
                "input": sentence,
                "category": category,
                "ground_truth": ground_truth
            }

            corpus["training_pairs"].append(training_pair)

            # Progress indicator
            if (i + 1) % 10 == 0:
                print(f"   Processed {i + 1}/{len(sentences)} sentences...")

        print(f"   ✅ Category '{category}' complete\n")

    corpus["metadata"]["total_sentences"] = len(corpus["training_pairs"])

    # Save corpus
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(corpus, f, indent=2)

    print("=" * 80)
    print("✅ CORPUS GENERATION COMPLETE")
    print("=" * 80)
    print(f"\n📊 Statistics:")
    print(f"   Total sentences: {corpus['metadata']['total_sentences']}")
    print(f"   Categories: {len(corpus['metadata']['categories'])}")
    print(f"   Output file: {output_path}")
    print(f"   File size: {output_file.stat().st_size / 1024:.1f} KB")
    print()

    # Sample statistics
    total_tokens = sum(len(pair["ground_truth"]["tokens"]) for pair in corpus["training_pairs"])
    total_entities = sum(len(pair["ground_truth"]["entities"]) for pair in corpus["training_pairs"])

    print(f"📈 Content Statistics:")
    print(f"   Total tokens: {total_tokens}")
    print(f"   Total entities: {total_entities}")
    print(f"   Avg tokens/sentence: {total_tokens / len(corpus['training_pairs']):.1f}")
    print(f"   Avg entities/sentence: {total_entities / len(corpus['training_pairs']):.2f}")
    print()

    return corpus


if __name__ == "__main__":
    corpus = generate_corpus()
    print("🌀 Linguistic ground truth corpus ready for Phase 0A training!")
