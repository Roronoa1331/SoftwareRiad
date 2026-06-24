"""MySQL relational storage for cultural relic business data."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Text,
    create_engine,
    func,
)
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from config.settings import settings
from models.artifact import ArtifactRecord

Base = declarative_base()


class ArtifactORM(Base):
    __tablename__ = "artifacts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    artifact_id = Column(String(128), unique=True, nullable=False, index=True)
    external_id = Column(String(64), nullable=False)
    name = Column(String(512), nullable=False, index=True)
    image_url = Column(Text, nullable=False)
    local_image_path = Column(Text)
    age = Column(String(256))
    dynasty = Column(String(128), index=True)
    artifact_type = Column(String(256), index=True)
    material = Column(String(512), index=True)
    introduction = Column(Text)
    detail_url = Column(Text, nullable=False)
    museum_name = Column(String(256), nullable=False, index=True)
    museum_location = Column(String(256))
    artist = Column(String(256))
    culture = Column(String(256))
    country_of_origin = Column(String(128))
    department = Column(String(256))
    crawled_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserORM(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    role = Column(String(32), default="viewer")
    created_at = Column(DateTime, default=datetime.utcnow)


class CrawlJobORM(Base):
    __tablename__ = "crawl_jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    museum_target = Column(String(64), nullable=False)
    status = Column(String(32), default="pending")
    artifacts_count = Column(Integer, default=0)
    triples_count = Column(Integer, default=0)
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime)


class MySQLStore:
    def __init__(self, url: Optional[str] = None):
        self.engine = create_engine(url or settings.mysql_url, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def init_schema(self) -> None:
        Base.metadata.create_all(self.engine)

    def upsert_artifact(self, record: ArtifactRecord) -> str:
        artifact_id = record.slug_id()
        with self.SessionLocal() as session:
            existing = (
                session.query(ArtifactORM)
                .filter(ArtifactORM.artifact_id == artifact_id)
                .first()
            )
            if existing:
                for key, value in self._record_to_row(record, artifact_id).items():
                    if key != "artifact_id":
                        setattr(existing, key, value)
                existing.updated_at = datetime.utcnow()
            else:
                session.add(ArtifactORM(**self._record_to_row(record, artifact_id)))
            session.commit()
        return artifact_id

    def upsert_artifacts(self, records: List[ArtifactRecord]) -> int:
        count = 0
        for record in records:
            self.upsert_artifact(record)
            count += 1
        return count

    def list_artifacts(
        self,
        limit: int = 50,
        offset: int = 0,
        dynasty: Optional[str] = None,
        material: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[dict]:
        with self.SessionLocal() as session:
            query = session.query(ArtifactORM)
            if dynasty:
                query = query.filter(ArtifactORM.dynasty.ilike(f"%{dynasty}%"))
            if material:
                query = query.filter(ArtifactORM.material.ilike(f"%{material}%"))
            if search:
                like = f"%{search}%"
                query = query.filter(
                    (ArtifactORM.name.ilike(like))
                    | (ArtifactORM.introduction.ilike(like))
                )
            rows = (
                query.order_by(ArtifactORM.id.desc())
                .offset(offset)
                .limit(limit)
                .all()
            )
            return [self._row_to_dict(row) for row in rows]

    def get_artifact(self, artifact_id: str) -> Optional[dict]:
        with self.SessionLocal() as session:
            row = (
                session.query(ArtifactORM)
                .filter(ArtifactORM.artifact_id == artifact_id)
                .first()
            )
            return self._row_to_dict(row) if row else None

    def count_artifacts(self) -> int:
        with self.SessionLocal() as session:
            return session.query(func.count(ArtifactORM.id)).scalar() or 0

    def record_crawl_job(
        self,
        museum_target: str,
        status: str,
        artifacts_count: int = 0,
        triples_count: int = 0,
    ) -> int:
        with self.SessionLocal() as session:
            job = CrawlJobORM(
                museum_target=museum_target,
                status=status,
                artifacts_count=artifacts_count,
                triples_count=triples_count,
                finished_at=datetime.utcnow() if status in ("completed", "failed") else None,
            )
            session.add(job)
            session.commit()
            return job.id

    @staticmethod
    def _record_to_row(record: ArtifactRecord, artifact_id: str) -> dict:
        return {
            "artifact_id": artifact_id,
            "external_id": record.external_id,
            "name": record.name,
            "image_url": record.image_url,
            "local_image_path": record.local_image_path,
            "age": record.age,
            "dynasty": record.dynasty,
            "artifact_type": record.artifact_type,
            "material": record.material,
            "introduction": record.introduction,
            "detail_url": record.detail_url,
            "museum_name": record.museum_name,
            "museum_location": record.museum_location,
            "artist": record.artist,
            "culture": record.culture,
            "country_of_origin": record.country_of_origin,
            "department": record.department,
            "crawled_at": record.crawled_at,
        }

    @staticmethod
    def _row_to_dict(row: ArtifactORM) -> dict:
        return {
            "artifact_id": row.artifact_id,
            "external_id": row.external_id,
            "name": row.name,
            "image_url": row.image_url,
            "local_image_path": row.local_image_path,
            "age": row.age,
            "dynasty": row.dynasty,
            "artifact_type": row.artifact_type,
            "material": row.material,
            "introduction": row.introduction,
            "detail_url": row.detail_url,
            "museum_name": row.museum_name,
            "museum_location": row.museum_location,
            "artist": row.artist,
            "culture": row.culture,
            "country_of_origin": row.country_of_origin,
            "department": row.department,
            "crawled_at": row.crawled_at.isoformat() if row.crawled_at else None,
        }
