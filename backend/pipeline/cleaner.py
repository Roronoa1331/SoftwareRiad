"""Data cleaning and normalization pipeline."""

import re
from pathlib import Path
from typing import Optional

import requests

from config.settings import settings
from models.artifact import ArtifactRecord


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def normalize_material(material: str) -> str:
    material = normalize_whitespace(material)
    if not material:
        return "Unknown"
    return material[0].upper() + material[1:]


def normalize_artifact_type(artifact_type: str) -> str:
    artifact_type = normalize_whitespace(artifact_type)
    return artifact_type or "Artifact"


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^\w\s-]", "", value)
    return re.sub(r"[\s_-]+", "_", value)


def clean_artifact(record: ArtifactRecord) -> ArtifactRecord:
    """Normalize fields on a crawled artifact record."""
    data = record.model_dump()
    data["name"] = normalize_whitespace(data["name"])
    data["age"] = normalize_whitespace(data["age"])
    data["material"] = normalize_material(data["material"])
    data["artifact_type"] = normalize_artifact_type(data["artifact_type"])
    data["introduction"] = normalize_whitespace(data["introduction"])
    if data.get("artist"):
        data["artist"] = normalize_whitespace(data["artist"])
    if data.get("dynasty"):
        data["dynasty"] = normalize_whitespace(data["dynasty"])
    return ArtifactRecord(**data)


def download_image(record: ArtifactRecord, session: Optional[requests.Session] = None) -> ArtifactRecord:
    """Download the original artifact image to local storage."""
    if not record.image_url:
        return record

    image_dir = settings.image_dir
    image_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(record.image_url.split("?")[0]).suffix or ".jpg"
    filename = f"{record.slug_id()}{ext}"
    local_path = image_dir / filename

    if local_path.exists():
        return record.model_copy(update={"local_image_path": str(local_path)})

    http = session or requests.Session()
    try:
        response = http.get(record.image_url, timeout=60)
        response.raise_for_status()
        local_path.write_bytes(response.content)
        return record.model_copy(update={"local_image_path": str(local_path)})
    except requests.RequestException:
        return record
