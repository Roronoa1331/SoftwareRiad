"""Base crawler interface for overseas museum websites."""

from abc import ABC, abstractmethod
from typing import Iterator

from models.artifact import ArtifactRecord


class BaseMuseumCrawler(ABC):
    """Abstract base class for museum artifact crawlers."""

    museum_name: str
    museum_location: str

    @abstractmethod
    def crawl(self, max_objects: int | None = None) -> Iterator[ArtifactRecord]:
        """Yield cleaned artifact records from the target museum."""

    @abstractmethod
    def get_detail_url(self, external_id: str) -> str:
        """Return the museum detail page URL for an object."""
