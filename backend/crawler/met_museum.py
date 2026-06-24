"""Metropolitan Museum of Art crawler for Chinese cultural relics.

Uses the Met Open Access Collection API (department 6 = Asian Art)
to retrieve Chinese and East Asian artifacts held by this overseas museum.
"""

import re
import time
from typing import Iterator, Optional
from urllib.parse import urljoin

import requests

from config.settings import settings
from crawler.base import BaseMuseumCrawler
from models.artifact import ArtifactRecord

MET_API_BASE = "https://collectionapi.metmuseum.org/public/collection/v1"
MET_WEB_BASE = "https://www.metmuseum.org"
ASIAN_ART_DEPARTMENT_ID = 6

CHINA_KEYWORDS = (
    "china",
    "chinese",
    "ming",
    "qing",
    "tang",
    "song",
    "yuan",
    "han",
    "shang",
    "zhou",
    "jin",
    "wei",
    "sui",
    "liao",
    "jin dynasty",
    "porcelain",
    "jade",
    "bronze",
    "celadon",
    "calligraphy",
    "scroll",
)

DYNASTY_PATTERNS = [
    (r"\b(shang|zhou|qin|han|three kingdoms|jin|northern wei|sui|tang|"
     r"five dynasties|liao|song|yuan|ming|qing)\b", None),
    (r"\b(\d{1,4})\s*(?:century|th century|st century|nd century|rd century)\b", None),
]


class MetMuseumCrawler(BaseMuseumCrawler):
    museum_name = "The Metropolitan Museum of Art"
    museum_location = "New York, USA"

    def __init__(self, session: Optional[requests.Session] = None):
        self.session = session or requests.Session()
        self.session.headers.update({"User-Agent": "SoftwareEnRiad-KG-Crawler/1.0"})

    def get_detail_url(self, external_id: str) -> str:
        return f"{MET_WEB_BASE}/art/collection/search/{external_id}"

    def _search_object_ids(self) -> list[int]:
        ids: set[int] = set()
        for keyword in CHINA_KEYWORDS:
            response = self.session.get(
                f"{MET_API_BASE}/search",
                params={
                    "q": keyword,
                    "departmentId": ASIAN_ART_DEPARTMENT_ID,
                    "hasImages": "true",
                },
                timeout=30,
            )
            response.raise_for_status()
            payload = response.json()
            for obj_id in payload.get("objectIDs") or []:
                ids.add(int(obj_id))
            time.sleep(settings.crawl_delay_seconds)
        return sorted(ids)

    def _fetch_object(self, object_id: int) -> Optional[dict]:
        response = self.session.get(
            f"{MET_API_BASE}/objects/{object_id}",
            timeout=30,
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def _extract_dynasty(self, age: str, culture: str) -> Optional[str]:
        combined = f"{age} {culture}".lower()
        dynasty_names = [
            "shang", "zhou", "qin", "han", "jin", "wei", "sui", "tang",
            "song", "yuan", "ming", "qing", "liao", "five dynasties",
        ]
        for name in dynasty_names:
            if name in combined:
                return name.title() + (" Dynasty" if name not in ("jin", "wei") else " Dynasty")
        century_match = re.search(r"(\d{1,2})(?:th|st|nd|rd)?\s*century", combined)
        if century_match:
            return f"{century_match.group(1)}th century"
        return None

    def _is_chinese_artifact(self, obj: dict) -> bool:
        culture = (obj.get("culture") or "").lower()
        country = (obj.get("country") or "").lower()
        title = (obj.get("title") or "").lower()
        period = (obj.get("period") or "").lower()
        combined = " ".join([culture, country, title, period])
        china_markers = ("china", "chinese", "ming", "qing", "tang", "song", "yuan")
        return any(marker in combined for marker in china_markers)

    def _map_object(self, obj: dict) -> ArtifactRecord:
        external_id = str(obj["objectID"])
        age_parts = [
            obj.get("objectDate") or "",
            obj.get("period") or "",
        ]
        age = " — ".join(part.strip() for part in age_parts if part and part.strip())
        culture = obj.get("culture") or ""
        image_url = obj.get("primaryImage") or obj.get("primaryImageSmall") or ""
        introduction_parts = [
            obj.get("objectDescription") or "",
            f"Culture: {culture}" if culture else "",
            f"Credit line: {obj.get('creditLine')}" if obj.get("creditLine") else "",
        ]
        introduction = "\n".join(p for p in introduction_parts if p).strip()

        return ArtifactRecord(
            external_id=external_id,
            name=(obj.get("title") or "Untitled").strip(),
            image_url=image_url,
            age=age,
            dynasty=self._extract_dynasty(age, culture),
            artifact_type=(obj.get("classification") or obj.get("objectName") or "Artifact").strip(),
            material=(obj.get("medium") or "").strip(),
            introduction=introduction,
            detail_url=obj.get("objectURL") or self.get_detail_url(external_id),
            museum_name=self.museum_name,
            museum_location=self.museum_location,
            artist=(obj.get("artistDisplayName") or None),
            culture=culture or None,
            country_of_origin=obj.get("country") or None,
            department=obj.get("department") or None,
        )

    def crawl(self, max_objects: int | None = None) -> Iterator[ArtifactRecord]:
        limit = max_objects or settings.crawl_max_objects
        object_ids = self._search_object_ids()
        yielded = 0

        for object_id in object_ids:
            if yielded >= limit:
                break
            try:
                obj = self._fetch_object(object_id)
            except requests.RequestException:
                continue
            finally:
                time.sleep(settings.crawl_delay_seconds)

            if not obj or not self._is_chinese_artifact(obj):
                continue
            if not obj.get("primaryImage") and not obj.get("primaryImageSmall"):
                continue

            yield self._map_object(obj)
            yielded += 1


def get_crawler(name: str) -> BaseMuseumCrawler:
    crawlers = {"met": MetMuseumCrawler}
    if name not in crawlers:
        raise ValueError(f"Unknown museum target: {name}. Available: {list(crawlers)}")
    return crawlers[name]()
