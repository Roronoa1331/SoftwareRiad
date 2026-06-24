"""Application configuration for the knowledge graph construction subsystem."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "kg_user"
    mysql_password: str = "kg_password"
    mysql_database: str = "cultural_relics_kg"

    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "neo4j_password"

    museum_target: str = "met"
    crawl_max_objects: int = 100
    crawl_delay_seconds: float = 0.2
    image_download_dir: str = "./data/images"

    api_host: str = "0.0.0.0"
    api_port: int = 8000

    @property
    def mysql_url(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
            f"?charset=utf8mb4"
        )

    @property
    def backend_root(self) -> Path:
        return Path(__file__).resolve().parent.parent

    @property
    def data_dir(self) -> Path:
        return self.backend_root / "data"

    @property
    def image_dir(self) -> Path:
        path = Path(self.image_download_dir)
        if not path.is_absolute():
            path = self.backend_root / path
        return path


settings = Settings()
