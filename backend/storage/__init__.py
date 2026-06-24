"""Dual-layer storage orchestrator: MySQL + Neo4j."""

import json
from pathlib import Path
from typing import List, Optional

from config.settings import settings
from models.artifact import ArtifactRecord
from models.triple import Triple
from pipeline.triplet_builder import build_triples_batch
from storage.mysql_store import MySQLStore
from storage.neo4j_store import Neo4jStore


class DualLayerStore:
    """Coordinates relational (MySQL) and graph (Neo4j) persistence."""

    def __init__(
        self,
        mysql: Optional[MySQLStore] = None,
        neo4j: Optional[Neo4jStore] = None,
    ):
        self.mysql = mysql or MySQLStore()
        self.neo4j = neo4j or Neo4jStore()

    def init_databases(self) -> None:
        self.mysql.init_schema()
        self.neo4j.init_schema()

    def save_artifacts(self, records: List[ArtifactRecord]) -> dict:
        artifact_count = self.mysql.upsert_artifacts(records)
        triples = build_triples_batch(records)
        triple_count = self.neo4j.upsert_triples(triples)
        return {
            "artifacts_saved": artifact_count,
            "triples_saved": triple_count,
        }

    def save_to_json_fallback(self, records: List[ArtifactRecord], path: Path) -> dict:
        """Persist to JSON when databases are unavailable (demo/offline mode)."""
        triples = build_triples_batch(records)
        payload = {
            "artifacts": [r.model_dump(mode="json") for r in records],
            "triples": [t.to_dict() for t in triples],
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        return {
            "artifacts_saved": len(records),
            "triples_saved": len(triples),
            "json_path": str(path),
        }

    def load_from_json(self, path: Path) -> tuple[List[ArtifactRecord], List[Triple]]:
        data = json.loads(path.read_text(encoding="utf-8"))
        records = [ArtifactRecord(**item) for item in data.get("artifacts", [])]
        triples = [Triple(**item) for item in data.get("triples", [])]
        return records, triples

    def import_json_to_databases(self, path: Path) -> dict:
        records, triples = self.load_from_json(path)
        artifact_count = self.mysql.upsert_artifacts(records)
        triple_count = self.neo4j.upsert_triples(triples)
        return {
            "artifacts_saved": artifact_count,
            "triples_saved": triple_count,
        }

    def get_stats(self) -> dict:
        return {
            "mysql_artifacts": self.mysql.count_artifacts(),
            "neo4j": self.neo4j.stats(),
        }

    def close(self) -> None:
        self.neo4j.close()
