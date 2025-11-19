# Code Examples: New Training Modes Implementation

## 1. LogicalReasoningTrainer Class Template

```python
# persona_layer/logical_reasoning_trainer.py

from arc_inspired_trainer import ArcInspiredTrainer
from typing import Dict, Optional, Tuple
import numpy as np

class LogicalReasoningTrainer(ArcInspiredTrainer):
    """
    Trains logical reasoning through formal structures.
    Inherits from ArcInspiredTrainer - only overrides domain-specific methods.
    """
    
    def __init__(self, organism_wrapper, training_pairs: List[Dict], **kwargs):
        super().__init__(organism_wrapper, training_pairs, **kwargs)
        self.reasoning_types = ['syllogism', 'causal', 'constraint', 'modus_ponens']
        self.assessment_threshold = 0.70  # Higher bar than arc (0.65)
        
    def _select_logical_triplet(self, logic_type: Optional[str] = None
                               ) -> Optional[Tuple[Dict, Dict, Dict]]:
        """Select 3 related logical problems (vs arc triplet)."""
        
        # Filter pairs by type
        if logic_type and logic_type in self.reasoning_types:
            pool = [p for p in self.training_pairs if p.get('type') == logic_type]
        else:
            # Random type
            logic_type = np.random.choice(self.reasoning_types)
            pool = [p for p in self.training_pairs if p.get('type') == logic_type]
        
        if len(pool) < 3:
            return None
        
        indices = np.random.choice(len(pool), 3, replace=False)
        return pool[indices[0]], pool[indices[1]], pool[indices[2]]
    
    def _compute_alignment_score_logical(self, predicted_response: str,
                                        predicted_confidence: float,
                                        predicted_path: str,
                                        predicted_felt_states: Dict,
                                        target_output: str,
                                        target_pair: Dict) -> Dict:
        """
        Assess logical reasoning quality.
        Weights: 50% SANS coherence + 30% formal correctness + 15% clarity + 5% confidence
        """
        
        # 1. Semantic coherence (SANS embedding similarity)
        if self.use_embeddings:
            pred_embedding = self.embedder.encode(predicted_response, convert_to_numpy=True)
            target_embedding = self.embedder.encode(target_output, convert_to_numpy=True)
            pred_norm = pred_embedding / np.linalg.norm(pred_embedding)
            target_norm = target_embedding / np.linalg.norm(target_embedding)
            semantic_similarity = float(np.dot(pred_norm, target_norm))
            semantic_similarity = (semantic_similarity + 1.0) / 2.0
        else:
            semantic_similarity = 0.5
        
        # 2. Formal correctness (check if conclusion is logically valid)
        formal_correctness = self._verify_logical_validity(
            predicted_response, target_pair
        )
        
        # 3. Reasoning clarity (can we follow the logic?)
        reasoning_clarity = self._assess_reasoning_clarity(predicted_response)
        
        # 4. Confidence appropriateness
        confidence_aligned = (
            (semantic_similarity >= 0.7 and predicted_confidence >= 0.6) or
            (semantic_similarity < 0.7 and predicted_confidence < 0.6)
        )
        
        # Weighted score
        overall_score = (
            0.50 * semantic_similarity +
            0.30 * formal_correctness +
            0.15 * reasoning_clarity +
            0.05 * (1.0 if confidence_aligned else 0.0)
        )
        
        # Assessment label
        if overall_score >= 0.85:
            assessment = 'excellent'
        elif overall_score >= self.assessment_threshold:
            assessment = 'good'
        elif overall_score >= 0.40:
            assessment = 'partial'
        else:
            assessment = 'poor'
        
        return {
            'semantic_similarity': float(semantic_similarity),
            'formal_correctness': float(formal_correctness),
            'reasoning_clarity': float(reasoning_clarity),
            'confidence_aligned': bool(confidence_aligned),
            'overall_score': float(overall_score),
            'assessment': assessment,
            'prediction_confidence': float(predicted_confidence),
            'prediction_path': predicted_path
        }
    
    def _verify_logical_validity(self, prediction: str, target_pair: Dict) -> float:
        """
        Check if predicted conclusion is logically valid.
        Returns 0.0-1.0 confidence in validity.
        
        For syllogisms: Check against Barbara/Celarent/Darii/Ferio forms
        For causal: Check if chain is maintained
        For constraint: Check consistency
        """
        # Simplified: Check for keywords that indicate valid reasoning
        validity_keywords = {
            'must', 'therefore', 'thus', 'implies', 'follows',
            'conclusion', 'because', 'since', 'as a result'
        }
        
        prediction_lower = prediction.lower()
        keyword_score = sum(
            1 for keyword in validity_keywords
            if keyword in prediction_lower
        ) / len(validity_keywords)
        
        # Check length (valid reasoning typically medium-length)
        prediction_length = len(prediction.split())
        target_length = len(target_pair.get('conclusion_target', '').split())
        length_match = 1.0 - min(abs(prediction_length - target_length) / max(target_length, 1), 1.0)
        
        return (keyword_score * 0.6) + (length_match * 0.4)
    
    def _assess_reasoning_clarity(self, prediction: str) -> float:
        """Assess how clearly the reasoning is presented."""
        # Look for structural clarity
        sentences = prediction.split('. ')
        
        # Multi-step reasoning is clearer
        clarity_score = min(len(sentences) / 3.0, 1.0)  # Target: 3+ sentences
        
        # Look for logical connectors
        connectors = ['if', 'then', 'therefore', 'because', 'so', 'thus']
        connector_count = sum(
            1 for connector in connectors
            if connector in prediction.lower()
        )
        connector_score = min(connector_count / 2.0, 1.0)  # Target: 2+ connectors
        
        return (clarity_score * 0.5) + (connector_score * 0.5)
    
    def train_logical_epoch(self, num_arcs: int = 30,
                           logic_type: Optional[str] = None,
                           verbose: bool = False) -> Dict:
        """Train epoch of logical reasoning."""
        print(f"\n🧠 Logical Reasoning Epoch ({num_arcs} problems, type={logic_type})")
        print("="*60)
        
        epoch_start = self.total_arcs_processed
        epoch_successes = 0
        
        for i in range(num_arcs):
            # Select logical triplet
            triplet = self._select_logical_triplet(logic_type)
            if triplet is None:
                continue
            
            example1, example2, target = triplet
            logic_type_used = target.get('type', 'unknown')
            
            # 1. Pattern exposure (same as Arc)
            example1_result = self.organism.process_text(
                self._get_input(example1),
                context={'arc_id': f'logic_{i:04d}', 'role': 'example1'},
                enable_tsk_recording=False
            )
            
            example2_result = self.organism.process_text(
                self._get_input(example2),
                context={'arc_id': f'logic_{i:04d}', 'role': 'example2'},
                enable_tsk_recording=False
            )
            
            # 2. Prediction
            prediction_result = self.organism.process_text(
                self._get_input(target),
                context={'arc_id': f'logic_{i:04d}', 'role': 'prediction'},
                enable_tsk_recording=False
            )
            
            # 3. Assessment (logical-specific)
            target_output = self._get_output(target)
            alignment = self._compute_alignment_score_logical(
                prediction_result.get('emission_text', ''),
                prediction_result.get('emission_confidence', 0.0),
                prediction_result.get('emission_path', ''),
                prediction_result.get('felt_states', {}),
                target_output,
                target
            )
            
            # 4. Learning (same as Arc)
            if self.enable_learning and alignment['overall_score'] >= self.assessment_threshold:
                self._apply_phase5_learning(example1_result, example2_result,
                                           prediction_result, target_output, i)
                epoch_successes += 1
            
            # Progress
            if (i + 1) % 10 == 0:
                print(f"   [{i+1}/{num_arcs}] Success rate: {epoch_successes/(i+1):.1%}")
        
        print(f"\n✅ Logical Reasoning Epoch Complete")
        print(f"   Success rate: {epoch_successes}/{num_arcs}")
        
        return {
            'training_mode': 'logical_reasoning',
            'arcs_processed': num_arcs,
            'success_rate': epoch_successes / num_arcs if num_arcs > 0 else 0.0,
            'logic_type_distribution': {logic_type: num_arcs}
        }
```

---

## 2. PoeticCreationTrainer Class Template

```python
# persona_layer/poetic_creation_trainer.py

from arc_inspired_trainer import ArcInspiredTrainer
from typing import Dict, Optional, Tuple
import numpy as np

class PoeticCreationTrainer(ArcInspiredTrainer):
    """
    Trains poetic expression through resonant language.
    Inherits from ArcInspiredTrainer.
    """
    
    def __init__(self, organism_wrapper, training_pairs: List[Dict], **kwargs):
        super().__init__(organism_wrapper, training_pairs, **kwargs)
        self.poetry_types = ['metaphor', 'image_grounding', 'rhythm', 'resonance', 'narrative']
        self.assessment_threshold = 0.55  # LOWER bar (poetic harder to assess)
        
    def _select_poetic_triplet(self, poetry_type: Optional[str] = None
                              ) -> Optional[Tuple[Dict, Dict, Dict]]:
        """Select 3 related poetic prompts."""
        
        if poetry_type and poetry_type in self.poetry_types:
            pool = [p for p in self.training_pairs if p.get('type') == poetry_type]
        else:
            poetry_type = np.random.choice(self.poetry_types)
            pool = [p for p in self.training_pairs if p.get('type') == poetry_type]
        
        if len(pool) < 3:
            return None
        
        indices = np.random.choice(len(pool), 3, replace=False)
        return pool[indices[0]], pool[indices[1]], pool[indices[2]]
    
    def _compute_alignment_score_poetic(self, predicted_response: str,
                                       predicted_confidence: float,
                                       predicted_path: str,
                                       predicted_felt_states: Dict,
                                       target_output: str,
                                       target_pair: Dict) -> Dict:
        """
        Assess poetic quality.
        Weights: 40% emotional_resonance (EMPATHY) + 25% authenticity + 20% imagery + 15% depth
        """
        
        # 1. Semantic similarity (basic)
        if self.use_embeddings:
            pred_embedding = self.embedder.encode(predicted_response, convert_to_numpy=True)
            target_embedding = self.embedder.encode(target_output, convert_to_numpy=True)
            pred_norm = pred_embedding / np.linalg.norm(pred_embedding)
            target_norm = target_embedding / np.linalg.norm(target_embedding)
            semantic_similarity = (np.dot(pred_norm, target_norm) + 1.0) / 2.0
        else:
            semantic_similarity = 0.5
        
        # 2. Emotional resonance (EMPATHY organ coherence from felt_states)
        felt_states = predicted_felt_states.get('organ_coherences', {})
        empathy_coherence = felt_states.get('EMPATHY', 0.0)
        emotional_resonance = empathy_coherence  # 0.0-1.0
        
        # 3. Authenticity score (AUTHENTICITY organ coherence)
        authenticity_coherence = felt_states.get('AUTHENTICITY', 0.0)
        
        # 4. Imagery vividness (check for sensory language)
        imagery_score = self._assess_imagery_vividness(predicted_response)
        
        # 5. Vulnerability depth
        vulnerability_score = self._assess_vulnerability_depth(predicted_response)
        
        # Weighted score
        overall_score = (
            0.40 * emotional_resonance +
            0.25 * authenticity_coherence +
            0.20 * imagery_score +
            0.15 * vulnerability_score
        )
        
        # Assessment
        if overall_score >= 0.85:
            assessment = 'excellent'
        elif overall_score >= self.assessment_threshold:
            assessment = 'good'
        elif overall_score >= 0.35:
            assessment = 'partial'
        else:
            assessment = 'poor'
        
        return {
            'semantic_similarity': float(semantic_similarity),
            'emotional_resonance': float(emotional_resonance),
            'authenticity': float(authenticity_coherence),
            'imagery_vividness': float(imagery_score),
            'vulnerability_depth': float(vulnerability_score),
            'overall_score': float(overall_score),
            'assessment': assessment,
            'prediction_confidence': float(predicted_confidence),
            'prediction_path': predicted_path
        }
    
    def _assess_imagery_vividness(self, text: str) -> float:
        """Assess sensory/concrete language."""
        sensory_words = {
            'see', 'sight', 'look', 'watch', 'gaze',
            'feel', 'touch', 'sensation', 'body', 'skin',
            'hear', 'sound', 'voice', 'whisper', 'silence',
            'taste', 'smell', 'scent', 'aroma',
            'cold', 'warm', 'soft', 'hard', 'sharp', 'smooth',
            'light', 'dark', 'shadow', 'glow', 'bright',
            'water', 'stone', 'earth', 'fire', 'wind', 'rain'
        }
        
        text_lower = text.lower()
        sensory_count = sum(
            1 for word in sensory_words
            if word in text_lower
        )
        
        # Normalize by text length (words)
        text_length = len(text.split())
        vividness = min(sensory_count / max(text_length / 10, 1), 1.0)
        
        return vividness
    
    def _assess_vulnerability_depth(self, text: str) -> float:
        """Assess emotional exposure/vulnerability markers."""
        vulnerability_words = {
            'scared', 'afraid', 'vulnerable', 'exposed', 'raw',
            'broken', 'fragile', 'wounded', 'ache', 'pain',
            'lonely', 'alone', 'lost', 'scared', 'desperate',
            'hope', 'wish', 'long', 'yearn',
            'truth', 'real', 'honestly', 'truly',
            'heart', 'soul', 'spirit'
        }
        
        text_lower = text.lower()
        vulnerability_count = sum(
            1 for word in vulnerability_words
            if word in text_lower
        )
        
        text_length = len(text.split())
        vulnerability = min(vulnerability_count / max(text_length / 12, 1), 1.0)
        
        return vulnerability
    
    def train_poetic_epoch(self, num_arcs: int = 30,
                          poetry_type: Optional[str] = None,
                          verbose: bool = False) -> Dict:
        """Train epoch of poetic creation."""
        print(f"\n🎭 Poetic Creation Epoch ({num_arcs} problems, type={poetry_type})")
        print("="*60)
        
        epoch_start = self.total_arcs_processed
        epoch_successes = 0
        
        for i in range(num_arcs):
            triplet = self._select_poetic_triplet(poetry_type)
            if triplet is None:
                continue
            
            example1, example2, target = triplet
            
            # Same pattern as Arc (pattern exposure → prediction → assessment → learning)
            example1_result = self.organism.process_text(
                self._get_input(example1),
                context={'arc_id': f'poetic_{i:04d}', 'role': 'example1'},
                enable_tsk_recording=False
            )
            
            example2_result = self.organism.process_text(
                self._get_input(example2),
                context={'arc_id': f'poetic_{i:04d}', 'role': 'example2'},
                enable_tsk_recording=False
            )
            
            prediction_result = self.organism.process_text(
                self._get_input(target),
                context={'arc_id': f'poetic_{i:04d}', 'role': 'prediction'},
                enable_tsk_recording=False
            )
            
            target_output = self._get_output(target)
            alignment = self._compute_alignment_score_poetic(
                prediction_result.get('emission_text', ''),
                prediction_result.get('emission_confidence', 0.0),
                prediction_result.get('emission_path', ''),
                prediction_result.get('felt_states', {}),
                target_output,
                target
            )
            
            if self.enable_learning and alignment['overall_score'] >= self.assessment_threshold:
                self._apply_phase5_learning(example1_result, example2_result,
                                           prediction_result, target_output, i)
                epoch_successes += 1
            
            if (i + 1) % 10 == 0:
                print(f"   [{i+1}/{num_arcs}] Success rate: {epoch_successes/(i+1):.1%}")
        
        return {
            'training_mode': 'poetic_creation',
            'arcs_processed': num_arcs,
            'success_rate': epoch_successes / num_arcs if num_arcs > 0 else 0.0
        }
```

---

## 3. Training Mode Coordinator

```python
# persona_layer/training_mode_coordinator.py

from arc_inspired_trainer import ArcInspiredTrainer
from logical_reasoning_trainer import LogicalReasoningTrainer
from poetic_creation_trainer import PoeticCreationTrainer
from dialectical_reasoning_trainer import DialecticalReasoningTrainer

class TrainingModeCoordinator:
    """Orchestrates multi-mode epoch training with family maturity tracking."""
    
    def __init__(self, organism_wrapper, training_data: Dict[str, List[Dict]]):
        """
        Initialize with training data organized by mode.
        
        Args:
            organism_wrapper: ConversationalOrganismWrapper
            training_data: {
                'arc_pattern_completion': [pairs],
                'logical_reasoning': [pairs],
                'poetic_creation': [pairs],
                'dialectical_reasoning': [pairs]
            }
        """
        self.wrapper = organism_wrapper
        
        self.trainers = {
            'arc': ArcInspiredTrainer(
                organism_wrapper,
                training_data['arc_pattern_completion']
            ),
            'logical': LogicalReasoningTrainer(
                organism_wrapper,
                training_data['logical_reasoning']
            ),
            'poetic': PoeticCreationTrainer(
                organism_wrapper,
                training_data['poetic_creation']
            ),
            'dialectical': DialecticalReasoningTrainer(
                organism_wrapper,
                training_data['dialectical_reasoning']
            )
        }
        
        self.family_maturity = {}
        self.training_history = []
    
    def run_comprehensive_training(self, num_epochs: int = 100,
                                  schedule: Optional[Dict] = None) -> Dict:
        """
        Run multi-mode training with round-robin or custom schedule.
        
        Args:
            num_epochs: Total epochs to run
            schedule: Optional {'mode': proportion} dict
                Default: round-robin across all modes
        
        Returns:
            Training summary with family metrics
        """
        
        if schedule is None:
            # Round-robin: distribute epochs evenly
            schedule = {
                'arc': 0.40,
                'logical': 0.25,
                'poetic': 0.20,
                'dialectical': 0.15
            }
        
        print("\n" + "="*70)
        print("🧬 COMPREHENSIVE MULTI-MODE TRAINING")
        print("="*70)
        print(f"Total epochs: {num_epochs}")
        print(f"Schedule: {schedule}")
        
        overall_success = 0
        overall_count = 0
        
        for epoch_idx in range(num_epochs):
            # Select mode based on schedule
            mode = np.random.choice(
                list(schedule.keys()),
                p=list(schedule.values())
            )
            
            trainer = self.trainers[mode]
            
            # Run epoch
            result = trainer.train_epoch(num_arcs=30, verbose=False)
            
            # Track success
            overall_success += result.get('success_rate', 0) * 30
            overall_count += 30
            
            # Update family maturity
            self._update_family_maturity(mode, result)
            
            # Report progress
            if (epoch_idx + 1) % 10 == 0:
                family_count = len(self.family_maturity)
                print(f"   Epoch {epoch_idx+1}/{num_epochs} (mode={mode})")
                print(f"      Families formed: {family_count}")
                print(f"      Overall success: {overall_success/overall_count:.1%}")
        
        print(f"\n✅ Comprehensive training complete!")
        
        return {
            'total_epochs': num_epochs,
            'overall_success_rate': overall_success / overall_count,
            'families_formed': len(self.family_maturity),
            'family_maturity': self.family_maturity
        }
    
    def _update_family_maturity(self, mode: str, epoch_result: Dict):
        """Track family maturity progress."""
        # Query Phase 5 learning for current family count
        if self.wrapper.phase5_learning:
            stats = self.wrapper.phase5_learning.get_statistics()
            self.family_maturity = {
                'total': stats.get('total_families', 0),
                'by_mode': self.family_maturity.get('by_mode', {})
            }
            self.family_maturity['by_mode'][mode] = \
                self.family_maturity['by_mode'].get(mode, 0) + 1
```

---

## 4. Training Data Format Examples

```python
# Example training pairs for each mode

# LOGICAL REASONING
logical_pair_syllogism = {
    "type": "syllogism",
    "input_text": "All humans are mortal. Socrates is human. What is true about Socrates?",
    "output_text": "Socrates is mortal.",
    "logical_form": "Barbara (AAA-1)",
    "difficulty": "easy",
    "metadata": {
        "category": "logical_reasoning",
        "logic_type": "syllogism"
    }
}

logical_pair_causal = {
    "type": "causal_chain",
    "input_text": "Sleep deprivation impairs cognitive function. Impaired cognition reduces work quality. What happens with sleep deprivation?",
    "output_text": "Sleep deprivation reduces work quality.",
    "chain_depth": 2,
    "difficulty": "medium",
    "metadata": {
        "category": "logical_reasoning",
        "logic_type": "causal_chain"
    }
}

# POETIC CREATION
poetic_pair_metaphor = {
    "type": "metaphor_completion",
    "input_text": "The wound of betrayal is...",
    "output_text": "...a mirror that shows you pieces you didn't know were broken.",
    "emotional_core": "fragmentation, sudden self-awareness",
    "difficulty": "medium",
    "metadata": {
        "category": "poetic_creation",
        "poetry_type": "metaphor"
    }
}

poetic_pair_resonance = {
    "type": "emotional_resonance",
    "input_text": "I feel so alone even in crowded rooms",
    "output_text": "To be surrounded and still untouched. To speak and not be heard. That's a specific kind of lonely.",
    "resonance_depth": "mirror_and_witness",
    "difficulty": "medium",
    "metadata": {
        "category": "poetic_creation",
        "poetry_type": "resonance"
    }
}

# DIALECTICAL REASONING
dialectical_pair = {
    "type": "simple_dialectic",
    "input_text": "Thesis: Urgency is necessary for success. Antithesis: Rest is necessary for sustainability. Synthesis?",
    "output_text": "Success requires both urgency (when truly needed) and sustainability (as the baseline). Confusing them is the error.",
    "values_in_tension": ["productivity", "wellbeing"],
    "difficulty": "medium",
    "metadata": {
        "category": "dialectical_reasoning",
        "dialect_type": "simple"
    }
}
```

