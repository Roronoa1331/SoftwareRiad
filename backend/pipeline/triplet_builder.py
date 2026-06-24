"""Convert cleaned artifact records into knowledge graph triplets."""

from typing import Iterable, List

from models.artifact import ArtifactRecord
from models.triple import (
    EntityType,
    KG_NAMESPACE,
    RelationType,
    Triple,
    entity_triple,
    literal_triple,
)
from pipeline.cleaner import slugify as make_slug


def _museum_id(name: str) -> str:
    return make_slug(name)


def _location_id(location: str) -> str:
    return make_slug(location)


def build_triples(record: ArtifactRecord) -> List[Triple]:
    """Build SPO triplets for one cultural relic artifact."""
    artifact_id = record.slug_id()
    triples: List[Triple] = []

    triples.append(
        literal_triple(artifact_id, EntityType.ARTIFACT, RelationType.HAS_NAME, record.name)
    )
    if record.age:
        triples.append(
            literal_triple(artifact_id, EntityType.ARTIFACT, RelationType.HAS_AGE, record.age)
        )
    if record.image_url:
        triples.append(
            literal_triple(
                artifact_id, EntityType.ARTIFACT, RelationType.HAS_IMAGE, record.image_url
            )
        )
    if record.introduction:
        triples.append(
            literal_triple(
                artifact_id,
                EntityType.ARTIFACT,
                RelationType.HAS_INTRODUCTION,
                record.introduction,
            )
        )
    triples.append(
        literal_triple(
            artifact_id, EntityType.ARTIFACT, RelationType.HAS_DETAIL_URL, record.detail_url
        )
    )

    museum_id = _museum_id(record.museum_name)
    triples.append(
        entity_triple(
            artifact_id,
            EntityType.ARTIFACT,
            RelationType.COLLECTED_IN,
            museum_id,
            EntityType.MUSEUM,
        )
    )
    triples.append(
        literal_triple(museum_id, EntityType.MUSEUM, RelationType.HAS_NAME, record.museum_name)
    )

    if record.museum_location:
        loc_id = _location_id(record.museum_location)
        triples.append(
            entity_triple(
                museum_id,
                EntityType.MUSEUM,
                RelationType.LOCATED_IN,
                loc_id,
                EntityType.LOCATION,
            )
        )
        triples.append(
            literal_triple(
                loc_id, EntityType.LOCATION, RelationType.HAS_NAME, record.museum_location
            )
        )

    if record.dynasty:
        dynasty_id = make_slug(record.dynasty)
        triples.append(
            entity_triple(
                artifact_id,
                EntityType.ARTIFACT,
                RelationType.BELONGS_TO_DYNASTY,
                dynasty_id,
                EntityType.DYNASTY,
            )
        )
        triples.append(
            literal_triple(
                dynasty_id, EntityType.DYNASTY, RelationType.HAS_NAME, record.dynasty
            )
        )

    if record.country_of_origin:
        origin_id = make_slug(record.country_of_origin)
        triples.append(
            entity_triple(
                artifact_id,
                EntityType.ARTIFACT,
                RelationType.CREATED_IN,
                origin_id,
                EntityType.LOCATION,
            )
        )
        triples.append(
            literal_triple(
                origin_id, EntityType.LOCATION, RelationType.HAS_NAME, record.country_of_origin
            )
        )

    if record.artist and record.artist.lower() not in ("unknown", "anonymous", ""):
        artist_id = make_slug(record.artist)
        triples.append(
            entity_triple(
                artifact_id,
                EntityType.ARTIFACT,
                RelationType.CREATED_BY,
                artist_id,
                EntityType.ARTIST,
            )
        )
        triples.append(
            literal_triple(artist_id, EntityType.ARTIST, RelationType.HAS_NAME, record.artist)
        )

    if record.material:
        material_id = make_slug(record.material)
        triples.append(
            entity_triple(
                artifact_id,
                EntityType.ARTIFACT,
                RelationType.MATERIAL_IS,
                material_id,
                EntityType.MATERIAL,
            )
        )
        triples.append(
            literal_triple(
                material_id, EntityType.MATERIAL, RelationType.HAS_NAME, record.material
            )
        )

    if record.artifact_type:
        type_id = make_slug(record.artifact_type)
        triples.append(
            entity_triple(
                artifact_id,
                EntityType.ARTIFACT,
                RelationType.TYPE_IS,
                type_id,
                EntityType.ARTIFACT_TYPE,
            )
        )
        triples.append(
            literal_triple(
                type_id, EntityType.ARTIFACT_TYPE, RelationType.HAS_NAME, record.artifact_type
            )
        )

    if record.culture:
        culture_id = make_slug(record.culture)
        triples.append(
            entity_triple(
                artifact_id,
                EntityType.ARTIFACT,
                RelationType.BELONGS_TO_CULTURE,
                culture_id,
                EntityType.CULTURE,
            )
        )
        triples.append(
            literal_triple(
                culture_id, EntityType.CULTURE, RelationType.HAS_NAME, record.culture
            )
        )

    return triples


def build_triples_batch(records: Iterable[ArtifactRecord]) -> List[Triple]:
    all_triples: List[Triple] = []
    for record in records:
        all_triples.extend(build_triples(record))
    return all_triples


def triples_to_rdf_turtle(triples: List[Triple]) -> str:
    """Export triples as Turtle for Linked Open Data publishing."""
    lines = [
        f"@prefix kg: <{KG_NAMESPACE}> .",
        "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .",
        "",
    ]
    for triple in triples:
        subj = f"<{triple.subject}>"
        pred = f"kg:{triple.predicate.value}"
        if triple.object_is_literal:
            obj = triple.object.replace('"', '\\"')
            obj_str = f'"{obj}"'
        else:
            obj_str = f"<{triple.object}>"
        lines.append(f"{subj} {pred} {obj_str} .")
    return "\n".join(lines)
