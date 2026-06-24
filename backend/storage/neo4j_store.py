"""Neo4j graph storage for knowledge graph triplets."""

from typing import Any, Dict, List, Optional

from neo4j import GraphDatabase

from config.settings import settings
from models.triple import RelationType, Triple


LITERAL_PROPERTY_MAP = {
    RelationType.HAS_NAME: "name",
    RelationType.HAS_AGE: "age",
    RelationType.HAS_IMAGE: "image_url",
    RelationType.HAS_DETAIL_URL: "detail_url",
    RelationType.HAS_INTRODUCTION: "introduction",
}


class Neo4jStore:
    CONSTRAINTS = [
        "CREATE CONSTRAINT artifact_uri IF NOT EXISTS FOR (n:Artifact) REQUIRE n.uri IS UNIQUE",
        "CREATE CONSTRAINT museum_uri IF NOT EXISTS FOR (n:Museum) REQUIRE n.uri IS UNIQUE",
        "CREATE CONSTRAINT dynasty_uri IF NOT EXISTS FOR (n:Dynasty) REQUIRE n.uri IS UNIQUE",
        "CREATE CONSTRAINT artist_uri IF NOT EXISTS FOR (n:Artist) REQUIRE n.uri IS UNIQUE",
        "CREATE CONSTRAINT location_uri IF NOT EXISTS FOR (n:Location) REQUIRE n.uri IS UNIQUE",
        "CREATE CONSTRAINT material_uri IF NOT EXISTS FOR (n:Material) REQUIRE n.uri IS UNIQUE",
        "CREATE CONSTRAINT artifact_type_uri IF NOT EXISTS FOR (n:ArtifactType) REQUIRE n.uri IS UNIQUE",
        "CREATE CONSTRAINT culture_uri IF NOT EXISTS FOR (n:Culture) REQUIRE n.uri IS UNIQUE",
    ]

    def __init__(
        self,
        uri: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ):
        self.driver = GraphDatabase.driver(
            uri or settings.neo4j_uri,
            auth=(user or settings.neo4j_user, password or settings.neo4j_password),
        )

    def close(self) -> None:
        self.driver.close()

    def init_schema(self) -> None:
        with self.driver.session() as session:
            for statement in self.CONSTRAINTS:
                session.run(statement)

    def upsert_triples(self, triples: List[Triple]) -> int:
        with self.driver.session() as session:
            for triple in triples:
                session.execute_write(self._merge_triple, triple)
        return len(triples)

    @staticmethod
    def _merge_triple(tx, triple: Triple) -> None:
        subject_label = triple.subject_type.value
        tx.run(
            f"MERGE (s:{subject_label} {{uri: $subject_uri}})",
            subject_uri=triple.subject,
        )

        if triple.object_is_literal:
            prop = LITERAL_PROPERTY_MAP.get(triple.predicate, triple.predicate.value)
            tx.run(
                f"""
                MATCH (s:{subject_label} {{uri: $subject_uri}})
                SET s.{prop} = $object_value
                """,
                subject_uri=triple.subject,
                object_value=triple.object,
            )
            return

        object_label = triple.object_type.value if triple.object_type else "Resource"
        rel_type = triple.predicate.value.upper()
        tx.run(
            f"""
            MATCH (s:{subject_label} {{uri: $subject_uri}})
            MERGE (o:{object_label} {{uri: $object_uri}})
            MERGE (s)-[:{rel_type}]->(o)
            """,
            subject_uri=triple.subject,
            object_uri=triple.object,
        )

    def get_artifact_graph(self, artifact_uri: str, depth: int = 2) -> List[Dict[str, Any]]:
        query = """
        MATCH path = (a:Artifact {uri: $uri})-[*1..$depth]-(connected)
        UNWIND relationships(path) AS rel
        RETURN DISTINCT
            startNode(rel).uri AS subject,
            labels(startNode(rel))[0] AS subject_type,
            type(rel) AS predicate,
            endNode(rel).uri AS object,
            labels(endNode(rel))[0] AS object_type
        LIMIT 100
        """
        with self.driver.session() as session:
            result = session.run(query, uri=artifact_uri, depth=depth)
            return [dict(record) for record in result]

    def sparql_like_query(self, dynasty_name: str) -> List[Dict[str, Any]]:
        query = """
        MATCH (a:Artifact)-[:BELONGS_TO_DYNASTY]->(d:Dynasty)
        WHERE toLower(d.name) CONTAINS toLower($dynasty)
           OR toLower(a.age) CONTAINS toLower($dynasty)
        OPTIONAL MATCH (a)-[:MATERIAL_IS]->(m:Material)
        OPTIONAL MATCH (a)-[:TYPE_IS]->(t:ArtifactType)
        OPTIONAL MATCH (a)-[:COLLECTED_IN]->(mu:Museum)
        RETURN a.uri AS artifact_uri,
               a.name AS name,
               a.age AS age,
               d.name AS dynasty,
               m.name AS material,
               t.name AS artifact_type,
               mu.name AS museum
        LIMIT 50
        """
        with self.driver.session() as session:
            result = session.run(query, dynasty=dynasty_name)
            return [dict(record) for record in result]

    def count_nodes(self) -> int:
        with self.driver.session() as session:
            result = session.run("MATCH (n) RETURN count(n) AS count")
            record = result.single()
            return record["count"] if record else 0

    def count_relationships(self) -> int:
        with self.driver.session() as session:
            result = session.run("MATCH ()-[r]->() RETURN count(r) AS count")
            record = result.single()
            return record["count"] if record else 0

    def stats(self) -> Dict[str, int]:
        return {
            "nodes": self.count_nodes(),
            "relationships": self.count_relationships(),
        }
