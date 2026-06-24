"""FastAPI REST service for knowledge graph queries and business data."""

from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config.settings import settings
from models.triple import KG_NAMESPACE, entity_uri, EntityType
from storage.mysql_store import MySQLStore
from storage.neo4j_store import Neo4jStore

app = FastAPI(
    title="Chinese Cultural Relics Knowledge Graph API",
    description="Section 6.3.1 — Knowledge graph construction subsystem",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mysql_store = MySQLStore()
neo4j_store = Neo4jStore()


class ArtifactResponse(BaseModel):
    artifact_id: str
    external_id: str
    name: str
    image_url: str
    local_image_path: Optional[str] = None
    age: Optional[str] = None
    dynasty: Optional[str] = None
    artifact_type: Optional[str] = None
    material: Optional[str] = None
    introduction: Optional[str] = None
    detail_url: str
    museum_name: str
    museum_location: Optional[str] = None
    artist: Optional[str] = None
    culture: Optional[str] = None
    country_of_origin: Optional[str] = None


class StatsResponse(BaseModel):
    mysql_artifacts: int
    neo4j_nodes: int
    neo4j_relationships: int
    kg_namespace: str


class GraphEdgeResponse(BaseModel):
    subject: str
    subject_type: Optional[str] = None
    predicate: str
    object: str
    object_type: Optional[str] = None


@app.on_event("shutdown")
def shutdown_event():
    neo4j_store.close()


@app.get("/")
def root():
    return {
        "service": "Knowledge Graph Construction Subsystem (6.3.1)",
        "museum_target": settings.museum_target,
        "endpoints": [
            "/api/artifacts",
            "/api/artifacts/{artifact_id}",
            "/api/graph/artifact/{artifact_id}",
            "/api/graph/dynasty/{dynasty_name}",
            "/api/stats",
            "/docs",
        ],
    }


@app.get("/api/stats", response_model=StatsResponse)
def get_stats():
    neo4j_stats = neo4j_store.stats()
    return StatsResponse(
        mysql_artifacts=mysql_store.count_artifacts(),
        neo4j_nodes=neo4j_stats["nodes"],
        neo4j_relationships=neo4j_stats["relationships"],
        kg_namespace=KG_NAMESPACE,
    )


@app.get("/api/artifacts", response_model=List[ArtifactResponse])
def list_artifacts(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    dynasty: Optional[str] = None,
    material: Optional[str] = None,
    search: Optional[str] = None,
):
    rows = mysql_store.list_artifacts(
        limit=limit,
        offset=offset,
        dynasty=dynasty,
        material=material,
        search=search,
    )
    return rows


@app.get("/api/artifacts/{artifact_id}", response_model=ArtifactResponse)
def get_artifact(artifact_id: str):
    row = mysql_store.get_artifact(artifact_id)
    if not row:
        raise HTTPException(status_code=404, detail="Artifact not found")
    return row


@app.get("/api/graph/artifact/{artifact_id}", response_model=List[GraphEdgeResponse])
def get_artifact_graph(artifact_id: str, depth: int = Query(2, ge=1, le=3)):
    uri = entity_uri(EntityType.ARTIFACT, artifact_id)
    edges = neo4j_store.get_artifact_graph(uri, depth=depth)
    if not edges:
        raise HTTPException(status_code=404, detail="Artifact graph not found")
    return edges


@app.get("/api/graph/dynasty/{dynasty_name}")
def query_by_dynasty(dynasty_name: str):
    return neo4j_store.sparql_like_query(dynasty_name)


def run_server():
    import uvicorn

    uvicorn.run(
        "api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=False,
    )
