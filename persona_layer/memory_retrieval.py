"""
Memory Retrieval System - Prehensive Recall via Fractal Learning
=================================================================

Retrieves past conversational occasions as "prehensions" (Whitehead) by leveraging
the existing fractal learning infrastructure:
- 57D organ signatures (OrganSignatureExtractor)
- Organic family clustering (OrganicConversationalFamilies)
- Hebbian R-matrix coupling (conversational_hebbian_memory.json)

Key Principles (Process Philosophy):
1. Past occasions are FELT, not merely retrieved (prehension vs query)
2. Memory is multi-modal: signature similarity + family membership + hebbian coupling
3. Recency weighting: temporal gradient (recent occasions more salient)
4. User bundles: persistent identity across conversations

Integration:
- Reuses existing 57D signatures from organic_families.json
- Leverages family centroids for similarity computation
- Hebbian R-matrix for organ coupling bonuses
- Formats top-K results for LLM context enrichment

Date: November 13, 2025
Author: DAE_HYPHAE_1 + Claude (hybrid authorship)
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity

# ✅ NOV 17: Import Config for consistent paths
from config import Config


class MemoryRetrieval:
    """
    Prehensive memory retrieval leveraging fractal learning architecture.

    Retrieves top-K similar past conversational moments using:
    1. 57D organ signature cosine similarity (from OrganSignatureExtractor)
    2. Family-based filtering (prioritize same family members)
    3. Hebbian R-matrix coupling bonus (organs that co-activate)
    4. Recency weighting (temporal decay)

    Returns formatted context for LLM memory-enriched queries.
    """

    def __init__(
        self,
        hebbian_memory_path: str = None,  # ✅ NOV 17: Use Config.HEBBIAN_MEMORY_PATH by default
        organic_families_path: str = None,  # ✅ NOV 17: Use Config.ORGANIC_FAMILIES_PATH by default
        user_bundles_dir: str = "Bundle",
        top_k: int = 5,
        recency_weight: float = 0.2,
        family_bonus: float = 0.15,
        hebbian_bonus_weight: float = 0.1
    ):
        """
        Initialize memory retrieval system.

        Args:
            hebbian_memory_path: Path to 11×11 R-matrix (organ coupling)
            organic_families_path: Path to family clusters (57D signatures)
            user_bundles_dir: Directory for user identity bundles
            top_k: Number of similar past moments to retrieve
            recency_weight: Weight for recency (0.0=ignore time, 1.0=only recent)
            family_bonus: Similarity boost for same-family members
            hebbian_bonus_weight: Weight for R-matrix coupling bonus
        """
        # ✅ NOV 17: Use Config paths if not provided
        if hebbian_memory_path is None:
            hebbian_memory_path = str(Config.HEBBIAN_MEMORY_PATH)
        if organic_families_path is None:
            organic_families_path = str(Config.ORGANIC_FAMILIES_PATH)

        self.hebbian_memory_path = hebbian_memory_path
        self.organic_families_path = organic_families_path
        self.user_bundles_dir = Path(user_bundles_dir)
        self.top_k = top_k
        self.recency_weight = recency_weight
        self.family_bonus = family_bonus
        self.hebbian_bonus_weight = hebbian_bonus_weight

        # Load hebbian R-matrix
        self.r_matrix = self._load_r_matrix()

        # Load organic families (contains 57D signatures + conversation history)
        self.families_data = self._load_families()

        # Extract all past conversations with signatures
        self.past_moments = self._extract_past_moments()

        # Organ names (11 organs)
        self.organs = [
            "LISTENING", "EMPATHY", "WISDOM", "AUTHENTICITY", "PRESENCE",
            "BOND", "SANS", "NDAM", "RNX", "EO", "CARD"
        ]

        print(f"✅ Memory retrieval initialized")
        print(f"   Past conversations available: {len(self.past_moments)}")
        print(f"   Families: {len(self.families_data.get('families', {}))}")

    def _load_r_matrix(self) -> np.ndarray:
        """Load 11×11 hebbian R-matrix (organ coupling)."""
        try:
            with open(self.hebbian_memory_path) as f:
                data = json.load(f)
                r_matrix = np.array(data.get("r_matrix", np.eye(11).tolist()))
            return r_matrix
        except FileNotFoundError:
            # Default: identity matrix (no coupling learned yet)
            return np.eye(11)

    def _load_families(self) -> Dict:
        """Load organic families (contains 57D signatures + conversations)."""
        try:
            with open(self.organic_families_path) as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            return {"families": {}}

    def _extract_past_moments(self) -> List[Dict]:
        """
        Extract all past conversations from families data.

        Each moment contains:
        - conversation_id
        - family_id
        - timestamp
        - organ_signature (57D from OrganSignatureExtractor)
        - input_text (if available)
        - response_text (if available)
        - satisfaction_score
        """
        moments = []
        families = self.families_data.get("families", {})

        for family_id, family_data in families.items():
            conversations = family_data.get("conversations", [])

            for conv in conversations:
                # Extract 57D signature (stored by OrganSignatureExtractor)
                organ_sig = conv.get("organ_signature", {})

                moments.append({
                    "conversation_id": conv.get("conversation_id", "unknown"),
                    "family_id": family_id,
                    "timestamp": conv.get("timestamp", "unknown"),
                    "organ_signature": organ_sig,
                    "input_text": conv.get("input_text", ""),
                    "response_text": conv.get("response_text", ""),
                    "satisfaction_score": conv.get("satisfaction_score", 0.0)
                })

        return moments

    def retrieve_similar_moments(
        self,
        current_organ_signature: Dict,  # 57D signature from OrganSignatureExtractor
        current_family_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> List[Dict]:
        """
        Retrieve top-K similar past conversational moments.

        Args:
            current_organ_signature: 57D signature dict from OrganSignatureExtractor
            current_family_id: Optional family ID (for family bonus)
            user_id: Optional user ID (for user-specific filtering)

        Returns:
            List of top-K similar moments with metadata:
            [
                {
                    "conversation_id": str,
                    "family_id": str,
                    "timestamp": str,
                    "similarity_score": float,
                    "cosine_similarity": float,
                    "hebbian_bonus": float,
                    "recency_score": float,
                    "organ_signature": Dict,
                    "input_text": str,
                    "response_text": str,
                    "satisfaction_score": float
                },
                ...
            ]
        """
        if not self.past_moments:
            return []  # No past conversations yet

        # Convert current signature to 57D vector
        current_vector = self._signature_dict_to_vector(current_organ_signature)

        # Compute similarities
        similarities = []
        for moment in self.past_moments:
            # 1. Cosine similarity (57D organ signature)
            past_vector = self._signature_dict_to_vector(moment["organ_signature"])
            cos_sim = cosine_similarity(
                current_vector.reshape(1, -1),
                past_vector.reshape(1, -1)
            )[0, 0]

            # 2. Hebbian coupling bonus (R-matrix alignment)
            # Extract organ-level activations for coupling check
            current_organ_activations = self._extract_organ_activations(current_organ_signature)
            past_organ_activations = self._extract_organ_activations(moment["organ_signature"])
            hebbian_bonus = self._compute_hebbian_bonus(
                current_organ_activations,
                past_organ_activations
            )

            # 3. Recency score (exponential decay)
            recency_score = self._compute_recency_score(moment["timestamp"])

            # 4. Family bonus (prioritize same family)
            fam_bonus = 0.0
            if current_family_id and moment["family_id"] == current_family_id:
                fam_bonus = self.family_bonus

            # Combined similarity score
            total_similarity = (
                cos_sim * (1 - self.recency_weight) +
                recency_score * self.recency_weight +
                hebbian_bonus * self.hebbian_bonus_weight +
                fam_bonus
            )

            similarities.append({
                **moment,
                "similarity_score": total_similarity,
                "cosine_similarity": cos_sim,
                "hebbian_bonus": hebbian_bonus,
                "recency_score": recency_score,
                "family_bonus": fam_bonus
            })

        # Sort by similarity and return top-K
        similarities.sort(key=lambda x: x["similarity_score"], reverse=True)
        return similarities[:self.top_k]

    def _signature_dict_to_vector(self, signature_dict: Dict) -> np.ndarray:
        """
        Convert 57D signature dict to numpy vector.

        Signature dict format (from OrganSignatureExtractor):
        {
            "LISTENING": {"mean": 0.8, "variance": 0.1, ...},
            "EMPATHY": {"mean": 0.7, ...},
            ...
        }
        """
        if not signature_dict:
            return np.zeros(57)

        vector = []

        # Organ dimension mapping (must match OrganSignatureExtractor)
        organ_dims = {
            'LISTENING': 6,
            'EMPATHY': 7,
            'WISDOM': 7,
            'AUTHENTICITY': 6,
            'PRESENCE': 6,
            'BOND': 5,
            'SANS': 4,
            'NDAM': 4,
            'RNX': 4,
            'EO': 4,
            'CARD': 4
        }

        for organ_name in self.organs:
            organ_data = signature_dict.get(organ_name, {})
            dims_expected = organ_dims.get(organ_name, 4)

            # Extract dimensions (simplified: use mean + variance if available)
            if isinstance(organ_data, dict):
                mean = organ_data.get("mean", 0.0)
                variance = organ_data.get("variance", 0.0)
                # Pad to expected dimensions
                organ_vector = [mean, variance] + [0.0] * (dims_expected - 2)
            else:
                # Fallback: scalar value
                coherence = organ_data if isinstance(organ_data, (int, float)) else 0.0
                organ_vector = [coherence] + [0.0] * (dims_expected - 1)

            vector.extend(organ_vector[:dims_expected])

        # Ensure exactly 57 dimensions
        vector = vector[:57]
        while len(vector) < 57:
            vector.append(0.0)

        return np.array(vector)

    def _extract_organ_activations(self, signature_dict: Dict) -> Dict[str, float]:
        """Extract organ-level activations (mean coherence) for hebbian bonus."""
        activations = {}
        for organ_name in self.organs:
            organ_data = signature_dict.get(organ_name, {})
            if isinstance(organ_data, dict):
                activations[organ_name] = organ_data.get("mean", 0.0)
            else:
                activations[organ_name] = organ_data if isinstance(organ_data, (int, float)) else 0.0
        return activations

    def _compute_hebbian_bonus(
        self,
        current_activations: Dict[str, float],
        past_activations: Dict[str, float]
    ) -> float:
        """
        Compute hebbian coupling bonus using R-matrix.

        Measures how often these organ co-activation patterns occurred in past.
        """
        bonus = 0.0
        count = 0

        for i, organ_i in enumerate(self.organs):
            for j, organ_j in enumerate(self.organs):
                if i >= j:
                    continue  # Only upper triangle (avoid double counting)

                # R-matrix coupling strength
                coupling = self.r_matrix[i, j]

                # Current and past activations
                current_i = current_activations.get(organ_i, 0.0)
                past_j = past_activations.get(organ_j, 0.0)

                # Bonus if both active and strongly coupled
                if current_i > 0.5 and past_j > 0.5:
                    bonus += coupling
                    count += 1

        # Normalize by number of active pairs
        return bonus / max(count, 1)

    def _compute_recency_score(self, timestamp: str) -> float:
        """
        Compute recency score with exponential decay.

        More recent conversations have higher scores.
        """
        try:
            # Try multiple timestamp formats
            formats = [
                "%Y-%m-%d_%H-%M-%S",
                "%Y-%m-%dT%H:%M:%S.%f",
                "%Y-%m-%dT%H:%M:%S"
            ]

            past_time = None
            for fmt in formats:
                try:
                    past_time = datetime.strptime(timestamp, fmt)
                    break
                except ValueError:
                    continue

            if past_time is None:
                return 0.1  # Unknown timestamp, assume old

            now = datetime.now()

            # Time difference in hours
            hours_ago = (now - past_time).total_seconds() / 3600

            # Exponential decay (half-life = 24 hours)
            recency = np.exp(-hours_ago / 24)
            return recency
        except (ValueError, TypeError):
            # If timestamp parsing fails, assume old conversation
            return 0.1

    def format_for_llm_context(
        self,
        similar_moments: List[Dict],
        include_full_text: bool = True,
        max_text_length: int = 150
    ) -> str:
        """
        Format retrieved moments as LLM context string.

        Args:
            similar_moments: List of similar past moments
            include_full_text: Whether to include conversation text
            max_text_length: Maximum characters per text snippet

        Returns:
            Formatted string for LLM prompt context
        """
        if not similar_moments:
            return "No past conversations available yet."

        context_lines = ["=== Past Similar Moments (Prehensive Memory) ==="]
        context_lines.append("")

        for idx, moment in enumerate(similar_moments, 1):
            # Header
            context_lines.append(
                f"{idx}. [{moment['timestamp']}] "
                f"(similarity: {moment['similarity_score']:.3f})"
            )

            # Family membership
            context_lines.append(f"   Family: {moment['family_id']}")

            # Similarity breakdown
            context_lines.append(
                f"   Components: cosine={moment['cosine_similarity']:.2f}, "
                f"hebbian={moment['hebbian_bonus']:.2f}, "
                f"recency={moment['recency_score']:.2f}"
            )

            # Dominant organs
            dominant_organs = self._get_top_organs(moment['organ_signature'], top_n=3)
            if dominant_organs:
                context_lines.append(f"   Dominant organs: {', '.join(dominant_organs)}")

            # Conversation text
            if include_full_text:
                if moment.get('input_text'):
                    input_preview = moment['input_text'][:max_text_length]
                    if len(moment['input_text']) > max_text_length:
                        input_preview += "..."
                    context_lines.append(f"   User: \"{input_preview}\"")

                if moment.get('response_text'):
                    response_preview = moment['response_text'][:max_text_length]
                    if len(moment['response_text']) > max_text_length:
                        response_preview += "..."
                    context_lines.append(f"   DAE: \"{response_preview}\"")

            context_lines.append("")

        return "\n".join(context_lines)

    def _get_top_organs(self, signature: Dict, top_n: int = 3) -> List[str]:
        """Get top-N most active organs from signature."""
        organ_values = []
        for organ_name in self.organs:
            val = signature.get(organ_name, {})
            if isinstance(val, dict):
                coherence = val.get("mean", 0.0)
            else:
                coherence = val if isinstance(val, (int, float)) else 0.0
            organ_values.append((organ_name, coherence))

        # Sort by coherence, descending
        organ_values.sort(key=lambda x: x[1], reverse=True)
        return [name for name, _ in organ_values[:top_n]]

    def load_user_bundle(self, user_id: str) -> Dict:
        """
        Load user-specific identity bundle.

        Contains:
        - total_conversations: int
        - themes: List[str] (recurring patterns)
        - inside_jokes: List[str] (user-specific references)
        - preferences: Dict (response style, length, detail)
        - created_at: str (timestamp)

        Args:
            user_id: User identifier

        Returns:
            User bundle dict
        """
        user_link_file = self.user_bundles_dir / f"user_link_{user_id}" / "user_state.json"

        try:
            with open(user_link_file) as f:
                bundle = json.load(f)
            return bundle
        except FileNotFoundError:
            # New user, return empty bundle
            return {
                "user_id": user_id,
                "total_conversations": 0,
                "themes": [],
                "inside_jokes": [],
                "preferences": {},
                "created_at": datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            }

    def update_user_bundle(
        self,
        user_id: str,
        new_themes: Optional[List[str]] = None,
        new_inside_jokes: Optional[List[str]] = None,
        preferences: Optional[Dict] = None
    ):
        """
        Update user bundle with new information.

        Args:
            user_id: User identifier
            new_themes: New themes to add
            new_inside_jokes: New inside jokes to add
            preferences: Updated preferences
        """
        bundle = self.load_user_bundle(user_id)

        # Update themes
        if new_themes:
            existing_themes = set(bundle.get("themes", []))
            existing_themes.update(new_themes)
            bundle["themes"] = list(existing_themes)

        # Update inside jokes
        if new_inside_jokes:
            existing_jokes = bundle.get("inside_jokes", [])
            existing_jokes.extend(new_inside_jokes)
            bundle["inside_jokes"] = existing_jokes

        # Update preferences
        if preferences:
            bundle["preferences"] = {**bundle.get("preferences", {}), **preferences}

        # Increment conversation count
        bundle["total_conversations"] = bundle.get("total_conversations", 0) + 1

        # Save updated bundle
        user_link_dir = self.user_bundles_dir / f"user_link_{user_id}"
        user_link_dir.mkdir(parents=True, exist_ok=True)

        with open(user_link_dir / "user_state.json", 'w') as f:
            json.dump(bundle, f, indent=2)


# Example usage
if __name__ == "__main__":
    print("Memory Retrieval System - Fractal Learning Integration")
    print("=" * 80)

    # Initialize memory retrieval
    retriever = MemoryRetrieval(top_k=5)

    print()
    print("Example: Retrieve similar moments for current conversation")
    print("-" * 80)

    # Example current signature (would come from OrganSignatureExtractor)
    current_signature = {
        "LISTENING": {"mean": 0.8, "variance": 0.1},
        "EMPATHY": {"mean": 0.7, "variance": 0.05},
        "WISDOM": {"mean": 0.6, "variance": 0.08},
        "NDAM": {"mean": 0.9, "variance": 0.12},  # High urgency
        "EO": {"mean": 0.3, "variance": 0.05},    # Low polyvagal safety
    }

    similar_moments = retriever.retrieve_similar_moments(
        current_organ_signature=current_signature
    )

    print(f"\nFound {len(similar_moments)} similar past moments")
    print()

    # Format for LLM context
    context = retriever.format_for_llm_context(similar_moments)
    print(context)
