"""Unit tests for knowledge graph pipeline."""

import json
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_ROOT))

from models.artifact import ArtifactRecord  # noqa: E402
from pipeline.cleaner import clean_artifact  # noqa: E402
from pipeline.triplet_builder import build_triples, build_triples_batch  # noqa: E402
from models.triple import EntityType, RelationType  # noqa: E402


def test_sample_data_loads():
    sample_path = BACKEND_ROOT / "data" / "sample_artifacts.json"
    data = json.loads(sample_path.read_text(encoding="utf-8"))
    assert len(data["artifacts"]) >= 5


def test_triplet_builder_produces_required_relations():
    sample_path = BACKEND_ROOT / "data" / "sample_artifacts.json"
    data = json.loads(sample_path.read_text(encoding="utf-8"))
    record = ArtifactRecord(**data["artifacts"][0])
    record = clean_artifact(record)
    triples = build_triples(record)
    predicates = {t.predicate for t in triples}
    assert RelationType.COLLECTED_IN in predicates
    assert RelationType.BELONGS_TO_DYNASTY in predicates
    assert RelationType.MATERIAL_IS in predicates
    assert RelationType.TYPE_IS in predicates
    assert RelationType.HAS_NAME in predicates


def test_batch_triples_count():
    sample_path = BACKEND_ROOT / "data" / "sample_artifacts.json"
    data = json.loads(sample_path.read_text(encoding="utf-8"))
    records = [ArtifactRecord(**item) for item in data["artifacts"]]
    triples = build_triples_batch(records)
    assert len(triples) > len(records) * 10


def test_entity_types_present():
    sample_path = BACKEND_ROOT / "data" / "sample_artifacts.json"
    data = json.loads(sample_path.read_text(encoding="utf-8"))
    records = [ArtifactRecord(**item) for item in data["artifacts"]]
    triples = build_triples_batch(records)
    types = {t.subject_type for t in triples} | {t.object_type for t in triples if t.object_type}
    assert EntityType.ARTIFACT in types
    assert EntityType.MUSEUM in types
    assert EntityType.DYNASTY in types
