"""
Test Felt Language Recorder - Phase 1 Validation
================================================

Validates that:
1. 57D signature extraction works correctly
2. Records are stored and retrieved properly
3. Persistence works (save/load)
4. Statistics computation is accurate
"""

import pytest
import numpy as np
import tempfile
import json
from pathlib import Path

from persona_layer.felt_language_recorder import FeltLanguageRecorder, FeltLanguageRecord


def create_mock_felt_state(
    zone: int = 3,
    polyvagal_state: str = 'ventral',
    v0_energy: float = 0.5,
    epoch: int = 1
) -> dict:
    """Create a mock felt-state for testing."""
    organ_names = [
        'LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
        'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD'
    ]

    return {
        'organ_coherences': {organ: np.random.rand() for organ in organ_names},
        'organ_intensities': {organ: np.random.rand() for organ in organ_names},
        'organ_polarities': {organ: np.random.rand() * 2 - 1 for organ in organ_names},
        'organ_confidences': {organ: 0.5 + np.random.rand() * 0.3 for organ in organ_names},
        'v0_energy': v0_energy,
        'satisfaction': np.random.rand(),
        'zone': zone,
        'polyvagal_state': polyvagal_state,
        'meta_atom_count': np.random.randint(0, 10),
        'nexus_count': np.random.randint(0, 20),
        'field_coherence': np.random.rand(),
        'signal_inflation': np.random.rand(),
        'temporal_collapse': np.random.rand(),
        'safety_gradient': np.random.rand(),
        'epoch': epoch
    }


class TestFeltLanguageRecorder:
    """Test suite for FeltLanguageRecorder."""

    def test_initialization(self):
        """Test recorder initialization with temporary storage."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            storage_path = f.name

        try:
            recorder = FeltLanguageRecorder(storage_path=storage_path)
            assert recorder.storage_path == storage_path
            assert len(recorder.memory) == 0
            assert len(recorder.ORGAN_NAMES) == 11
        finally:
            Path(storage_path).unlink(missing_ok=True)

    def test_57d_signature_extraction(self):
        """Test that 57D signature is extracted correctly."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            storage_path = f.name

        try:
            recorder = FeltLanguageRecorder(storage_path=storage_path)
            felt_state = create_mock_felt_state()

            signature = recorder._compute_57d_signature(felt_state)

            # Validate shape
            assert signature.shape == (57,), f"Expected 57D, got {signature.shape}"

            # Validate range (most values should be 0-1)
            assert np.all(signature >= -1.0), "Some values below -1"
            assert np.all(signature <= 2.0), "Some values above 2"

            # Validate first 44 dimensions (organs × 4)
            # Every 4th dimension starting at index 2 is polarity (-1 to 1)
            for i in range(11):
                polarity_idx = i * 4 + 2
                assert -1.0 <= signature[polarity_idx] <= 1.0, \
                    f"Organ {i} polarity out of range: {signature[polarity_idx]}"

        finally:
            Path(storage_path).unlink(missing_ok=True)

    def test_polyvagal_one_hot_encoding(self):
        """Test polyvagal state one-hot encoding."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            storage_path = f.name

        try:
            recorder = FeltLanguageRecorder(storage_path=storage_path)

            # Test ventral
            onehot = recorder._one_hot_polyvagal('ventral')
            assert onehot == [1.0, 0.0, 0.0]

            # Test sympathetic
            onehot = recorder._one_hot_polyvagal('sympathetic')
            assert onehot == [0.0, 1.0, 0.0]

            # Test dorsal
            onehot = recorder._one_hot_polyvagal('dorsal')
            assert onehot == [0.0, 0.0, 1.0]

            # Test unknown
            onehot = recorder._one_hot_polyvagal('unknown')
            assert onehot == [0.0, 0.0, 0.0]

        finally:
            Path(storage_path).unlink(missing_ok=True)

    def test_record_llm_emission(self):
        """Test recording a single LLM emission."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            storage_path = f.name

        try:
            recorder = FeltLanguageRecorder(storage_path=storage_path)
            felt_state = create_mock_felt_state(zone=3, epoch=1)

            record = recorder.record_llm_emission(
                felt_state=felt_state,
                llm_output="What's present for you right now?",
                success_metrics={
                    'confidence': 0.75,
                    'satisfaction': 0.80,
                    'coherence': 0.70
                },
                conversation_id="test_conv_1",
                turn_number=1
            )

            # Validate record fields
            assert isinstance(record, FeltLanguageRecord)
            assert record.epoch == 1
            assert record.conversation_id == "test_conv_1"
            assert record.turn_number == 1
            assert record.language_output == "What's present for you right now?"
            assert len(record.felt_signature) == 57
            assert record.success_metrics['confidence'] == 0.75

            # Validate metadata
            assert record.metadata['zone'] == 3
            assert 'polyvagal_state' in record.metadata

            # Validate memory
            assert len(recorder.memory) == 1

        finally:
            Path(storage_path).unlink(missing_ok=True)

    def test_persistence_save_load(self):
        """Test that records are saved and loaded correctly."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            storage_path = f.name

        try:
            # Create recorder and add records
            recorder1 = FeltLanguageRecorder(storage_path=storage_path)

            for i in range(5):
                felt_state = create_mock_felt_state(epoch=i+1)
                recorder1.record_llm_emission(
                    felt_state=felt_state,
                    llm_output=f"Response {i+1}",
                    success_metrics={'confidence': 0.5 + i*0.1},
                    conversation_id="test_conv",
                    turn_number=i
                )

            # Force save
            recorder1._save_memory()

            # Create new recorder instance (should load from disk)
            recorder2 = FeltLanguageRecorder(storage_path=storage_path)

            # Validate loaded data
            assert len(recorder2.memory) == 5
            assert recorder2.memory[0].language_output == "Response 1"
            assert recorder2.memory[4].language_output == "Response 5"
            assert recorder2.memory[0].epoch == 1
            assert recorder2.memory[4].epoch == 5

        finally:
            Path(storage_path).unlink(missing_ok=True)

    def test_statistics_computation(self):
        """Test statistics computation."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            storage_path = f.name

        try:
            recorder = FeltLanguageRecorder(storage_path=storage_path)

            # Add records from different epochs
            for epoch in [1, 1, 2, 2, 2, 3]:
                felt_state = create_mock_felt_state(epoch=epoch)
                recorder.record_llm_emission(
                    felt_state=felt_state,
                    llm_output=f"Response epoch {epoch}",
                    success_metrics={'confidence': 0.7},
                    conversation_id=f"conv_{epoch}",
                    turn_number=0
                )

            stats = recorder.get_statistics()

            # Validate statistics
            assert stats['total_records'] == 6
            assert stats['epochs_covered'] == [1, 2, 3]
            assert stats['unique_conversations'] == 3
            assert stats['records_per_epoch'][1] == 2
            assert stats['records_per_epoch'][2] == 3
            assert stats['records_per_epoch'][3] == 1
            assert stats['mean_signature_norm'] > 0

        finally:
            Path(storage_path).unlink(missing_ok=True)

    def test_get_records_by_epoch(self):
        """Test filtering records by epoch."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            storage_path = f.name

        try:
            recorder = FeltLanguageRecorder(storage_path=storage_path)

            # Add records from epochs 1, 2, 3
            for epoch in [1, 2, 2, 3, 3, 3]:
                felt_state = create_mock_felt_state(epoch=epoch)
                recorder.record_llm_emission(
                    felt_state=felt_state,
                    llm_output=f"Epoch {epoch}",
                    success_metrics={'confidence': 0.7},
                    conversation_id="test",
                    turn_number=0
                )

            # Filter by epoch
            epoch1_records = recorder.get_records_by_epoch(1)
            epoch2_records = recorder.get_records_by_epoch(2)
            epoch3_records = recorder.get_records_by_epoch(3)

            assert len(epoch1_records) == 1
            assert len(epoch2_records) == 2
            assert len(epoch3_records) == 3

        finally:
            Path(storage_path).unlink(missing_ok=True)

    def test_get_records_by_zone(self):
        """Test filtering records by zone."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            storage_path = f.name

        try:
            recorder = FeltLanguageRecorder(storage_path=storage_path)

            # Add records from different zones
            for zone in [1, 2, 3, 3, 4, 5]:
                felt_state = create_mock_felt_state(zone=zone)
                recorder.record_llm_emission(
                    felt_state=felt_state,
                    llm_output=f"Zone {zone}",
                    success_metrics={'confidence': 0.7},
                    conversation_id="test",
                    turn_number=0
                )

            # Filter by zone
            zone3_records = recorder.get_records_by_zone(3)
            zone5_records = recorder.get_records_by_zone(5)

            assert len(zone3_records) == 2
            assert len(zone5_records) == 1

        finally:
            Path(storage_path).unlink(missing_ok=True)

    def test_auto_save_every_10_records(self):
        """Test that memory is auto-saved every 10 records."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            storage_path = f.name

        try:
            recorder = FeltLanguageRecorder(storage_path=storage_path)

            # Add 15 records (should trigger auto-save at 10)
            for i in range(15):
                felt_state = create_mock_felt_state()
                recorder.record_llm_emission(
                    felt_state=felt_state,
                    llm_output=f"Response {i}",
                    success_metrics={'confidence': 0.7},
                    conversation_id="test",
                    turn_number=i
                )

            # Verify file was created and contains data
            assert Path(storage_path).exists()

            with open(storage_path, 'r') as f:
                data = json.load(f)
                # After 10 and 15, should have 15 records
                # (auto-save at 10, then continue to 15)
                assert len(data['records']) >= 10

        finally:
            Path(storage_path).unlink(missing_ok=True)


def run_tests():
    """Run all tests."""
    pytest.main([__file__, '-v'])


if __name__ == '__main__':
    run_tests()
