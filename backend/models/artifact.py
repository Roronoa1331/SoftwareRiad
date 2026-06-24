"""Domain models for cultural relic artifacts."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ArtifactRecord(BaseModel):
    """Cleaned cultural relic record from an overseas museum."""

    external_id: str = Field(description="Museum-specific object identifier")
    name: str
    image_url: str = Field(description="Original image URL from the museum")
    local_image_path: Optional[str] = None
    age: str = Field(default="", description="Period or date of creation")
    dynasty: Optional[str] = None
    artifact_type: str = Field(default="", description="Object classification")
    material: str = Field(default="")
    introduction: str = Field(default="", description="Descriptive text")
    detail_url: str
    museum_name: str
    museum_location: str = ""
    artist: Optional[str] = None
    culture: Optional[str] = None
    country_of_origin: Optional[str] = None
    department: Optional[str] = None
    crawled_at: datetime = Field(default_factory=datetime.utcnow)

    def slug_id(self) -> str:
        museum_prefix = self.museum_name.lower().replace(" ", "_")[:10]
        return f"{museum_prefix}_{self.external_id}"
