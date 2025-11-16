#!/usr/bin/env python3
"""
Conversational TSK Recorder - Transductive Summary Kernel Infrastructure
=========================================================================

Records complete transductive summaries for epoch learning.
Captures INITIAL → FINAL felt-state transformations per conversation.

Architecture (DAE 3.0 Inspired):
1. INITIAL STATE: Organism state before processing user input
2. PROCESSING: V0 convergence, organ activation, nexus formation
3. FINAL STATE: Organism state after response generation
4. TSK: Summary of transformation (what changed, how it changed)

This enables proper epoch learning via transformation signatures,
not snapshot clustering.

Date: November 16, 2025
Status: Core infrastructure for epoch learning
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import numpy as np
from pathlib import Path


@dataclass
class TransductiveSummaryKernel:
    """
    Complete summary of one conversational transformation.

    This is what DAE 3.0 calls "INPUT/OUTPUT TSK pair" adapted
    for conversational context.

    The KEY INSIGHT: We capture TRANSFORMATION patterns, not states.
    """
    # Metadata
    conversation_id: str
    timestamp: str
    user_input: str
    response_text: str

    # INITIAL STATE (before processing user input)
    initial_v0_energy: float = 1.0
    initial_organ_coherences: Dict[str, float] = field(default_factory=dict)
    initial_polyvagal_state: str = "ventral_vagal"
    initial_zone: int = 1
    initial_urgency: float = 0.0
    initial_satisfaction: float = 0.5
    initial_self_distance: float = 0.5

    # FINAL STATE (after response generation)
    final_v0_energy: float = 0.5
    final_organ_coherences: Dict[str, float] = field(default_factory=dict)
    final_polyvagal_state: str = "ventral_vagal"
    final_zone: int = 1
    final_urgency: float = 0.0
    final_satisfaction: float = 0.5
    final_self_distance: float = 0.5

    # TRANSFORMATION METRICS (the HOW)
    v0_energy_descent: float = 0.5
    convergence_cycles: int = 3
    kairos_detected: bool = False
    kairos_cycle_index: Optional[int] = None

    # Nexus type transitions (multi-cycle)
    nexus_type_initial: str = "Relational"
    nexus_type_final: str = "Relational"
    nexus_domain_initial: str = "PSYCHE"
    nexus_domain_final: str = "PSYCHE"

    # Transductive vocabulary (averaged across cycles)
    signal_inflation: float = 0.0
    salience_drift: float = 0.0
    prehensive_overload: float = 0.0
    coherence_leakage: float = 0.0

    # RNX/TSK metrics
    rnx_activation: float = 0.0
    rnx_kairos: float = 0.0
    transition_mechanism: str = "maintain"
    trajectory_coherence: float = 1.0

    # Constraint evolution (how organs changed during cycles)
    bond_constraint_delta: float = 0.0  # BOND: protection shift
    ndam_constraint_delta: float = 0.0  # NDAM: urgency shift
    sans_constraint_delta: float = 0.0  # SANS: coherence shift
    eo_constraint_delta: float = 0.0    # EO: rhythm shift

    # Response characteristics
    emission_path: str = "fusion"  # direct/fusion/kairos/hebbian
    emission_confidence: float = 0.5
    nexus_count: int = 5

    # Learning outcome (set after family assignment)
    family_id: Optional[str] = None
    family_similarity: float = 0.0
    is_new_family: bool = False

    # 57D signature (computed from transformation)
    transformation_signature: List[float] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert to JSON-serializable dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'TransductiveSummaryKernel':
        """Create from dictionary."""
        return cls(**data)

    def compute_organ_coherence_shifts(self) -> Dict[str, float]:
        """
        Compute how each organ's coherence changed.
        This is the KEY differentiation metric for families.

        Returns dict: {organ_name: shift_value}
        Positive = organ strengthened, Negative = organ weakened
        """
        shifts = {}
        organ_names = [
            'LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
            'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD', 'NEXUS'
        ]

        for organ in organ_names:
            initial_coh = self.initial_organ_coherences.get(organ, 0.5)
            final_coh = self.final_organ_coherences.get(organ, 0.5)
            shifts[organ] = final_coh - initial_coh

        return shifts

    def compute_satisfaction_improvement(self) -> float:
        """How much satisfaction improved."""
        return self.final_satisfaction - self.initial_satisfaction

    def compute_polyvagal_transition(self) -> str:
        """Describe polyvagal state transition."""
        return f"{self.initial_polyvagal_state}→{self.final_polyvagal_state}"

    def compute_zone_movement(self) -> int:
        """How many zones moved (positive = toward collapse, negative = toward SELF)."""
        return self.final_zone - self.initial_zone


class ConversationalTSKRecorder:
    """
    Records TSK summaries for conversational transformations.

    Integrates with existing wrapper by:
    1. Capturing initial state before processing
    2. Capturing final state after processing
    3. Building complete TSK for epoch learning

    Does NOT break dae_interactive.py - optional layer on top.
    """

    def __init__(self, storage_dir: str = "persona_layer/tsk_logs"):
        """Initialize TSK recorder."""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # In-memory storage for current session
        self.current_session_tsks: List[TransductiveSummaryKernel] = []

        # Persistent index
        self.index_path = self.storage_dir / "tsk_index.json"
        self.index = self._load_index()

        print(f"✅ ConversationalTSKRecorder initialized")
        print(f"   Storage: {self.storage_dir}")
        print(f"   Total TSKs: {len(self.index.get('tsk_ids', []))}")

    def _load_index(self) -> Dict:
        """Load TSK index from disk."""
        if self.index_path.exists():
            with open(self.index_path, 'r') as f:
                return json.load(f)
        else:
            return {
                'tsk_ids': [],
                'total_count': 0,
                'families_observed': {},
                'last_updated': datetime.now().isoformat()
            }

    def _save_index(self):
        """Save TSK index to disk."""
        self.index['last_updated'] = datetime.now().isoformat()
        with open(self.index_path, 'w') as f:
            json.dump(self.index, f, indent=2)

    def create_initial_state(self) -> Dict:
        """
        Create default initial felt state.

        Called BEFORE processing user input.
        Sets neutral baselines for all organs.

        Returns dict that can be passed to process_text()
        """
        initial_state = {
            'v0_energy': 1.0,  # High energy, not yet engaged
            'organ_coherences': {
                'LISTENING': 0.5,
                'EMPATHY': 0.5,
                'WISDOM': 0.5,
                'AUTHENTICITY': 0.5,
                'PRESENCE': 0.5,
                'BOND': 0.5,
                'SANS': 0.5,
                'NDAM': 0.5,
                'RNX': 0.5,
                'EO': 0.5,
                'CARD': 0.5,
                'NEXUS': 0.5
            },
            'polyvagal_state': 'ventral_vagal',
            'zone': 1,
            'urgency': 0.0,
            'satisfaction': 0.5,
            'self_distance': 0.5,
            'timestamp': datetime.now().isoformat()
        }
        return initial_state

    def create_tsk_from_processing(
        self,
        conversation_id: str,
        user_input: str,
        initial_state: Dict,
        final_felt_states: Dict,
        transduction_trajectory: List[Dict],
        response_text: str
    ) -> TransductiveSummaryKernel:
        """
        Create TSK from processing results.

        Called AFTER organism processes user input.

        Args:
            conversation_id: Unique conversation identifier
            user_input: User's text input
            initial_state: State before processing (from create_initial_state)
            final_felt_states: felt_states dict from process_text()
            transduction_trajectory: List of per-cycle transduction states
            response_text: Generated response

        Returns:
            Complete TSK for epoch learning
        """
        # Extract final organ coherences
        final_organ_coherences = final_felt_states.get('organ_coherences', {})

        # Extract transductive vocabulary (average across trajectory)
        signal_inflation = 0.0
        salience_drift = 0.0
        prehensive_overload = 0.0
        coherence_leakage = 0.0

        if transduction_trajectory:
            signal_inflations = [t.get('signal_inflation', 0.0) for t in transduction_trajectory]
            salience_drifts = [t.get('salience_drift', 0.0) for t in transduction_trajectory]
            prehensive_overloads = [t.get('prehensive_overload', 0.0) for t in transduction_trajectory]
            coherence_leakages = [t.get('coherence_leakage', 0.0) for t in transduction_trajectory]

            signal_inflation = np.mean(signal_inflations) if signal_inflations else 0.0
            salience_drift = np.mean(salience_drifts) if salience_drifts else 0.0
            prehensive_overload = np.mean(prehensive_overloads) if prehensive_overloads else 0.0
            coherence_leakage = np.mean(coherence_leakages) if coherence_leakages else 0.0

        # Extract nexus type transitions
        nexus_type_initial = "Relational"
        nexus_type_final = "Relational"
        nexus_domain_initial = "PSYCHE"
        nexus_domain_final = "PSYCHE"

        if transduction_trajectory:
            first_trans = transduction_trajectory[0]
            last_trans = transduction_trajectory[-1]

            nexus_type_initial = first_trans.get('current_type', 'Relational')
            nexus_type_final = last_trans.get('current_type', 'Relational')
            nexus_domain_initial = first_trans.get('current_category', 'PSYCHE')
            nexus_domain_final = last_trans.get('current_category', 'PSYCHE')

        # Compute constraint deltas (how organs evolved during multi-cycle)
        # Since organs process same text, these reflect V0 energy modulation effects
        bond_delta = 0.0
        ndam_delta = 0.0
        sans_delta = 0.0
        eo_delta = 0.0

        if len(transduction_trajectory) > 1:
            first_trans = transduction_trajectory[0]
            last_trans = transduction_trajectory[-1]

            bond_delta = last_trans.get('bond_self_distance', 0.5) - first_trans.get('bond_self_distance', 0.5)
            ndam_delta = last_trans.get('ndam_urgency_level', 0.0) - first_trans.get('ndam_urgency_level', 0.0)
            eo_delta = last_trans.get('rhythm_coherence', 0.5) - first_trans.get('rhythm_coherence', 0.5)
            # SANS coherence computed from field resonance change
            sans_delta = last_trans.get('field_resonance', 0.5) - first_trans.get('field_resonance', 0.5)

        # Build TSK
        tsk = TransductiveSummaryKernel(
            conversation_id=conversation_id,
            timestamp=datetime.now().isoformat(),
            user_input=user_input,
            response_text=response_text[:500],  # Truncate for storage

            # Initial state
            initial_v0_energy=initial_state.get('v0_energy', 1.0),
            initial_organ_coherences=initial_state.get('organ_coherences', {}),
            initial_polyvagal_state=initial_state.get('polyvagal_state', 'ventral_vagal'),
            initial_zone=initial_state.get('zone', 1),
            initial_urgency=initial_state.get('urgency', 0.0),
            initial_satisfaction=initial_state.get('satisfaction', 0.5),
            initial_self_distance=initial_state.get('self_distance', 0.5),

            # Final state
            final_v0_energy=final_felt_states.get('v0_energy_final', 0.5),
            final_organ_coherences=final_organ_coherences,
            final_polyvagal_state=final_felt_states.get('eo_polyvagal_state', 'ventral_vagal'),
            final_zone=final_felt_states.get('zone', 1),
            final_urgency=final_felt_states.get('NDAM_urgency_level', 0.0),
            final_satisfaction=final_felt_states.get('satisfaction_final', 0.5),
            final_self_distance=final_felt_states.get('bond_self_distance', 0.5),

            # Transformation metrics
            v0_energy_descent=1.0 - final_felt_states.get('v0_energy_final', 0.5),
            convergence_cycles=final_felt_states.get('convergence_cycles', 3),
            kairos_detected=final_felt_states.get('kairos_detected', False),
            kairos_cycle_index=final_felt_states.get('kairos_cycle_index', None),

            # Nexus transitions
            nexus_type_initial=nexus_type_initial,
            nexus_type_final=nexus_type_final,
            nexus_domain_initial=nexus_domain_initial,
            nexus_domain_final=nexus_domain_final,

            # Transductive vocabulary
            signal_inflation=signal_inflation,
            salience_drift=salience_drift,
            prehensive_overload=prehensive_overload,
            coherence_leakage=coherence_leakage,

            # RNX metrics (computed from trajectory)
            rnx_activation=self._compute_rnx_activation(transduction_trajectory),
            rnx_kairos=self._compute_rnx_kairos(transduction_trajectory, final_felt_states),
            transition_mechanism=last_trans.get('transition_mechanism', 'maintain') if transduction_trajectory else 'maintain',
            trajectory_coherence=self._compute_trajectory_coherence(transduction_trajectory),

            # Constraint deltas
            bond_constraint_delta=bond_delta,
            ndam_constraint_delta=ndam_delta,
            sans_constraint_delta=sans_delta,
            eo_constraint_delta=eo_delta,

            # Response characteristics
            emission_path=final_felt_states.get('emission_path', 'fusion'),
            emission_confidence=final_felt_states.get('emission_confidence', 0.5),
            nexus_count=final_felt_states.get('nexus_count', 5)
        )

        # Compute 57D transformation signature
        tsk.transformation_signature = self._compute_transformation_signature(tsk)

        return tsk

    def _compute_rnx_activation(self, trajectory: List[Dict]) -> float:
        """Compute RNX activation score from trajectory."""
        if not trajectory:
            return 0.0

        # RNX activation = variance in V0 energy across cycles
        v0_energies = [t.get('v0_energy', 0.5) for t in trajectory]
        if len(v0_energies) > 1:
            return float(np.var(v0_energies))
        return 0.0

    def _compute_rnx_kairos(self, trajectory: List[Dict], felt_states: Dict) -> float:
        """Compute RNX Kairos score (bifurcation intensity)."""
        rnx_activation = self._compute_rnx_activation(trajectory)
        kairos_factor = 1.5 if felt_states.get('kairos_detected', False) else 1.0
        return rnx_activation * kairos_factor

    def _compute_trajectory_coherence(self, trajectory: List[Dict]) -> float:
        """Compute how coherent the nexus type trajectory was."""
        if len(trajectory) <= 1:
            return 1.0

        # Count nexus type changes
        changes = 0
        for i in range(len(trajectory) - 1):
            if trajectory[i].get('current_type') != trajectory[i+1].get('current_type'):
                changes += 1

        return 1.0 - (changes / len(trajectory))

    def _compute_transformation_signature(self, tsk: TransductiveSummaryKernel) -> List[float]:
        """
        Compute 57D transformation signature from TSK.

        This is the key metric for family clustering.
        Captures HOW the organism transformed, not WHAT it is.

        Architecture:
        [0-5]:   V0 Energy Transformation (6D)
        [6-16]:  Organ Coherence SHIFTS (11D)
        [17-19]: Polyvagal Transformation (3D)
        [20-22]: Zone Transformation (3D)
        [23-28]: Satisfaction Evolution (6D)
        [29-32]: Convergence Characteristics (4D)
        [33-34]: Urgency Shift (2D)
        [35-37]: Emission Path (3D one-hot)
        [38-39]: Reserved (2D)
        [40-56]: RNX/TSK Dimensions (17D)
        """
        signature = np.zeros(57)

        # === V0 Energy Transformation (dims 0-5) ===
        signature[0] = tsk.initial_v0_energy
        signature[1] = tsk.final_v0_energy
        signature[2] = tsk.v0_energy_descent
        signature[3] = abs(tsk.v0_energy_descent) / max(tsk.initial_v0_energy, 1e-6)
        signature[4] = (tsk.convergence_cycles - 3.0) / 2.0  # Normalize around 3 cycles
        signature[5] = 1.0 if tsk.kairos_detected else 0.0

        # === Organ Coherence SHIFTS (dims 6-16) ===
        organ_names = ['LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
                       'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD']

        for i, organ in enumerate(organ_names):
            initial_coh = tsk.initial_organ_coherences.get(organ, 0.5)
            final_coh = tsk.final_organ_coherences.get(organ, 0.5)
            signature[6 + i] = final_coh - initial_coh  # SHIFT: positive = strengthened

        # === Polyvagal Transformation (dims 17-19) ===
        polyvagal_map = {'ventral_vagal': 0, 'sympathetic': 1, 'dorsal_vagal': 2, 'mixed_state': 1.5}
        initial_poly = polyvagal_map.get(tsk.initial_polyvagal_state, 0)
        final_poly = polyvagal_map.get(tsk.final_polyvagal_state, 0)

        signature[17] = initial_poly / 2.0
        signature[18] = final_poly / 2.0
        signature[19] = (final_poly - initial_poly) / 2.0

        # === Zone Transformation (dims 20-22) ===
        signature[20] = (tsk.initial_zone - 1) / 4.0
        signature[21] = (tsk.final_zone - 1) / 4.0
        signature[22] = (tsk.final_zone - tsk.initial_zone) / 4.0

        # === Satisfaction Evolution (dims 23-28) ===
        signature[23] = tsk.initial_satisfaction
        signature[24] = tsk.final_satisfaction
        signature[25] = tsk.final_satisfaction - tsk.initial_satisfaction
        signature[26] = abs(signature[25])
        signature[27] = 1.0 if signature[25] > 0.05 else 0.0
        signature[28] = 0.0  # Reserved for satisfaction variance

        # === Convergence Characteristics (dims 29-32) ===
        signature[29] = (tsk.convergence_cycles - 1.0) / 4.0
        signature[30] = 1.0 if tsk.kairos_detected else 0.0
        signature[31] = tsk.v0_energy_descent
        signature[32] = tsk.nexus_count / 15.0

        # === Urgency Shift (dims 33-34) ===
        signature[33] = tsk.initial_urgency
        signature[34] = tsk.final_urgency

        # === Emission Path (dims 35-37) - one-hot ===
        if tsk.emission_path == 'direct':
            signature[35:38] = [1.0, 0.0, 0.0]
        elif tsk.emission_path == 'fusion':
            signature[35:38] = [0.0, 1.0, 0.0]
        elif tsk.emission_path == 'kairos':
            signature[35:38] = [0.0, 0.0, 1.0]
        else:  # hebbian fallback
            signature[35:38] = [0.0, 0.0, 0.0]

        # === Reserved (dims 38-39) ===
        signature[38] = 0.0
        signature[39] = 0.0

        # === RNX/TSK Dimensions (dims 40-56) ===
        # Nexus type (40-42)
        nexus_type_map = {
            'Innate': 0.0, 'Relational': 0.2, 'Protective': 0.4, 'Urgency': 0.6,
            'Paradox': 0.7, 'Dissociative': 0.8, 'Recursive': 0.85, 'Looped': 0.9,
            'Disruptive': 0.95, 'Absorbed': 1.0
        }
        signature[40] = nexus_type_map.get(tsk.nexus_type_initial, 0.2)
        signature[41] = nexus_type_map.get(tsk.nexus_type_final, 0.2)

        domain_map = {'GUT': 0.0, 'PSYCHE': 0.5, 'SOCIAL_CONTEXT': 1.0}
        initial_domain = domain_map.get(tsk.nexus_domain_initial, 0.5)
        final_domain = domain_map.get(tsk.nexus_domain_final, 0.5)
        signature[42] = final_domain - initial_domain

        # Constraint deltas (43-46)
        signature[43] = tsk.bond_constraint_delta
        signature[44] = tsk.ndam_constraint_delta
        signature[45] = tsk.sans_constraint_delta
        signature[46] = tsk.eo_constraint_delta

        # Transductive vocabulary (47-50)
        signature[47] = tsk.signal_inflation
        signature[48] = tsk.salience_drift
        signature[49] = tsk.prehensive_overload
        signature[50] = tsk.coherence_leakage

        # Crisis/healing scores (51-52)
        crisis_types = {'Paradox', 'Dissociative', 'Disruptive', 'Recursive', 'Looped', 'Urgency'}
        crisis_score = 1.0 if tsk.nexus_type_final in crisis_types else 0.0
        healing_score = max(0.0, signature[25])  # Satisfaction improvement
        signature[51] = crisis_score
        signature[52] = min(1.0, healing_score)

        # RNX metrics (53-56)
        signature[53] = tsk.rnx_activation
        signature[54] = tsk.rnx_kairos
        mechanism_map = {'maintain': 0.0, 'amplify': 0.3, 'dampen': 0.6, 'transform': 1.0}
        signature[55] = mechanism_map.get(tsk.transition_mechanism, 0.0)
        signature[56] = tsk.trajectory_coherence

        # L2 normalize to unit sphere
        norm = np.linalg.norm(signature)
        if norm > 1e-6:
            signature = signature / norm

        return signature.tolist()

    def __len__(self) -> int:
        """Return total number of TSKs stored."""
        return self.index.get('total_count', 0)

    def store_tsk(self, tsk: TransductiveSummaryKernel, epoch_id: Optional[int] = None) -> str:
        """
        Store TSK to disk and update index.

        Args:
            tsk: Transductive Summary Kernel to store
            epoch_id: Optional epoch number (for organizing)

        Returns path to stored file.
        """
        # Create filename (with optional epoch prefix)
        if epoch_id is not None:
            filename = f"epoch{epoch_id}_{tsk.conversation_id}_{tsk.timestamp.replace(':', '-')}.json"
        else:
            filename = f"{tsk.conversation_id}_{tsk.timestamp.replace(':', '-')}.json"
        filepath = self.storage_dir / filename

        # Store TSK
        with open(filepath, 'w') as f:
            json.dump(tsk.to_dict(), f, indent=2)

        # Update session storage
        self.current_session_tsks.append(tsk)

        # Update index
        self.index['tsk_ids'].append(tsk.conversation_id)
        self.index['total_count'] += 1

        if tsk.family_id:
            if tsk.family_id not in self.index['families_observed']:
                self.index['families_observed'][tsk.family_id] = 0
            self.index['families_observed'][tsk.family_id] += 1

        self._save_index()

        return str(filepath)

    def load_tsk(self, filepath: str) -> TransductiveSummaryKernel:
        """Load TSK from disk."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return TransductiveSummaryKernel.from_dict(data)

    def get_session_tsks(self) -> List[TransductiveSummaryKernel]:
        """Get all TSKs from current session."""
        return self.current_session_tsks

    def get_transformation_signatures(self) -> List[np.ndarray]:
        """Get all transformation signatures from current session."""
        return [np.array(tsk.transformation_signature) for tsk in self.current_session_tsks]

    def clear_session(self):
        """Clear current session storage (for new epoch)."""
        self.current_session_tsks = []
