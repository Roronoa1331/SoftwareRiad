"""Knowledge graph triplet and ontology definitions."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EntityType(str, Enum):
    ARTIFACT = "Artifact"
    MUSEUM = "Museum"
    DYNASTY = "Dynasty"
    ARTIST = "Artist"
    LOCATION = "Location"
    MATERIAL = "Material"
    ARTIFACT_TYPE = "ArtifactType"
    CULTURE = "Culture"


class RelationType(str, Enum):
    COLLECTED_IN = "collected_in"
    CREATED_IN = "created_in"
    BELONGS_TO_DYNASTY = "belongs_to_dynasty"
    CREATED_BY = "created_by"
    MATERIAL_IS = "material_is"
    TYPE_IS = "type_is"
    HAS_NAME = "has_name"
    HAS_AGE = "has_age"
    HAS_IMAGE = "has_image"
    HAS_DETAIL_URL = "has_detail_url"
    HAS_INTRODUCTION = "has_introduction"
    BELONGS_TO_CULTURE = "belongs_to_culture"
    LOCATED_IN = "located_in"


class Triple(BaseModel):
    """Subject-predicate-object knowledge graph triple."""

    subject: str = Field(description="Subject entity URI or ID")
    subject_type: EntityType
    predicate: RelationType
    object: str = Field(description="Object entity URI, ID, or literal value")
    object_type: Optional[EntityType] = None
    object_is_literal: bool = False

    def to_dict(self) -> dict:
        return {
            "subject": self.subject,
            "subject_type": self.subject_type.value,
            "predicate": self.predicate.value,
            "object": self.object,
            "object_type": self.object_type.value if self.object_type else None,
            "object_is_literal": self.object_is_literal,
        }


# RDF namespace for Linked Open Data publishing
KG_NAMESPACE = "http://softwareenriad.org/kg/"
RDF_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"


def entity_uri(entity_type: EntityType, entity_id: str) -> str:
    return f"{KG_NAMESPACE}{entity_type.value}/{entity_id}"


def literal_triple(
    subject_id: str,
    subject_type: EntityType,
    predicate: RelationType,
    value: str,
) -> Triple:
    return Triple(
        subject=entity_uri(subject_type, subject_id),
        subject_type=subject_type,
        predicate=predicate,
        object=value,
        object_is_literal=True,
    )


def entity_triple(
    subject_id: str,
    subject_type: EntityType,
    predicate: RelationType,
    object_id: str,
    object_type: EntityType,
) -> Triple:
    return Triple(
        subject=entity_uri(subject_type, subject_id),
        subject_type=subject_type,
        predicate=predicate,
        object=entity_uri(object_type, object_id),
        object_type=object_type,
    )
