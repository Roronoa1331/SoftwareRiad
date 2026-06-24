# SoftwareEnRiad

**Chinese Cultural Relics Knowledge Graph** — a HarmonyOS mobile app and Python backend that implements **Section 6.3.1: Knowledge Graph Construction Subsystem**.

The system crawls Chinese cultural relic data from an overseas museum, models it as knowledge-graph triplets, stores it in a dual-layer database architecture (MySQL + Neo4j), and presents it through a searchable mobile interface.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [HarmonyOS App (Quick Start)](#harmonyos-app-quick-start)
- [Python Backend](#python-backend)
- [Knowledge Graph Ontology](#knowledge-graph-ontology)
- [REST API Reference](#rest-api-reference)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

| Layer | Role |
|-------|------|
| **HarmonyOS app** | Browse relics, view graph stats, search, and inspect triplet relationships |
| **Python backend** | Crawl, clean, model, and persist cultural relic data |
| **MySQL** | Relational storage for artifact details, users, and business data |
| **Neo4j** | Graph storage for entities, relationships, and traversal queries |
| **Data source** | [The Metropolitan Museum of Art](https://www.metmuseum.org/) Open Access API (overseas museum) |

### Architecture

```
The Met Open Access API (overseas museum)
              │
              ▼
        Data Crawler
              │
              ▼
        Data Cleaning
              │
              ▼
        Triplet Builder (Subject–Predicate–Object)
              │
      ┌───────┴───────┐
      ▼               ▼
   MySQL           Neo4j
 (relational)     (graph)
      │               │
      └───────┬───────┘
              ▼
        FastAPI REST API
              ▼
      HarmonyOS Mobile App
   (20 offline samples built-in)
```

---

## Features

### 6.3.1 Knowledge Graph Construction Subsystem

| Module | Description |
|--------|-------------|
| **Data crawling** | Crawls Chinese cultural relic information from **The Metropolitan Museum of Art** (New York). Captures name, original image, age, type, material, introduction, and detail page URL. |
| **Data modeling** | Converts cleaned data into triplet form (subject–predicate–object) with defined entity and relationship types. |
| **Dual storage** | **Neo4j** stores all triples for graph queries and relationship traversal. **MySQL** stores detailed relic records, user data, and system business data. Optional **RDF Turtle** export for Linked Open Data (LOD). |

### Mobile App

- Dashboard with **Artifacts**, **Graph Nodes**, and **Relations** counts
- Scrollable list of **20 offline sample relics** (works without backend or internet)
- Search by name, dynasty, material, or artist
- Detail view with full metadata and knowledge-graph triple previews
- Optional live API connection when the Python backend is running

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Mobile app | HarmonyOS, ArkTS, ArkUI |
| Backend | Python 3.11+, FastAPI, SQLAlchemy |
| Graph DB | Neo4j 5.x |
| Relational DB | MySQL 8.x |
| Crawler | Requests + Met Open Access API |
| Infrastructure | Docker Compose |

---

## Project Structure

```
softwareEnRiad/
├── AppScope/                          # App-level HarmonyOS config
├── entry/                             # HarmonyOS entry module
│   └── src/main/ets/
│       ├── pages/Index.ets            # Main UI
│       ├── models/
│       │   ├── Artifact.ets           # Relic model + 20 offline samples
│       │   └── Museum.ts              # Museum model (sample data)
│       └── services/
│           └── KnowledgeGraphApi.ets  # Offline data + optional API client
├── backend/                           # Python KG construction subsystem
│   ├── crawler/                       # Met Museum crawler
│   ├── pipeline/                      # Data cleaning + triplet builder
│   ├── storage/                       # MySQL + Neo4j dual layer
│   ├── api/                           # FastAPI REST service
│   ├── schema/                        # Database init scripts
│   ├── data/                          # Sample JSON, RDF exports
│   ├── tests/                         # Pipeline unit tests
│   ├── main.py                        # CLI entry point
│   └── requirements.txt
├── docker-compose.yml                 # MySQL + Neo4j containers
└── README.md
```

---

## HarmonyOS App (Quick Start)

The app works **out of the box** with 20 bundled offline samples from The Met. No backend setup is required.

### Prerequisites

- [DevEco Studio](https://developer.huawei.com/consumer/en/deveco-studio/) (HarmonyOS SDK **API 6.1.1** or compatible)
- HarmonyOS phone emulator or physical device

### Run the app

1. Open the project folder in **DevEco Studio**
2. Wait for the project to sync and index
3. Select a phone emulator or connected device
4. Click **Run**

### What you should see

| Screen area | Content |
|-------------|---------|
| Stats cards | ~20 Artifacts · ~60+ Graph Nodes · ~160+ Relations |
| Relic list | 20 Chinese cultural relics from The Met |
| Detail view | Dynasty, age, material, introduction, and KG triples |
| Search | Filter by name, dynasty, material, or artist |

### Enable live API (optional)

1. Start the Python backend (see [Python Backend](#python-backend))
2. Open `entry/src/main/ets/services/KnowledgeGraphApi.ets`
3. Set `OFFLINE_ONLY` to `false`
4. Update `API_BASE_URL` if needed:
   - Emulator: `http://10.0.2.2:8000`
   - Physical device on same network: `http://<your-pc-ip>:8000`

---

## Python Backend

### Prerequisites

- Python 3.11+
- Docker Desktop (for MySQL and Neo4j)

### 1. Start databases

```bash
docker compose up -d
```

| Service | URL | Credentials |
|---------|-----|-------------|
| MySQL | `localhost:3306` | user: `kg_user` / password: `kg_password` |
| Neo4j Browser | http://localhost:7474 | user: `neo4j` / password: `neo4j_password` |

### 2. Install dependencies

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env        # Windows
# cp .env.example .env          # macOS / Linux
```

### 3. CLI commands

```bash
# Initialize database schemas
python main.py init-db

# Load bundled sample data into MySQL + Neo4j
python main.py demo

# Crawl live data from The Met (adjust count as needed)
python main.py crawl --max 50
python main.py crawl --max 50 --download-images

# Start REST API server
python main.py serve

# Export triples as RDF Turtle (Linked Open Data)
python main.py export-rdf

# Import a JSON file into both databases
python main.py import-json --file data/sample_artifacts.json
```

API documentation: **http://localhost:8000/docs**

### Run tests

```bash
cd backend
.venv\Scripts\python -c "import sys; sys.path.insert(0,'.'); from tests.test_pipeline import *; test_sample_data_loads(); test_triplet_builder_produces_required_relations(); test_batch_triples_count(); test_entity_types_present(); print('All tests passed')"
```

---

## Knowledge Graph Ontology

### Entity Types

| Entity | Example |
|--------|---------|
| `Artifact` | Ming dynasty porcelain bottle |
| `Museum` | The Metropolitan Museum of Art |
| `Dynasty` | Tang Dynasty |
| `Artist` | Wang Hui |
| `Location` | China, New York |
| `Material` | Bronze, Porcelain |
| `ArtifactType` | Mirror, Hanging scroll |
| `Culture` | China |

### Relationship Types

| Relation | Meaning | Example |
|----------|---------|---------|
| `collected_in` | Artifact → Museum | Bottle collected in The Met |
| `created_in` | Artifact → Location | Vessel created in China |
| `belongs_to_dynasty` | Artifact → Dynasty | Mirror belongs to Tang Dynasty |
| `created_by` | Artifact → Artist | Scroll created by Wang Hui |
| `material_is` | Artifact → Material | Vessel material is Bronze |
| `type_is` | Artifact → ArtifactType | Object type is Mirror |
| `belongs_to_culture` | Artifact → Culture | Artifact belongs to Chinese culture |
| `located_in` | Museum → Location | Museum located in New York |
| `has_name` | Entity → literal | Name property |
| `has_age` | Artifact → literal | Period / date |
| `has_image` | Artifact → literal | Image URL |
| `has_detail_url` | Artifact → literal | Museum detail page |
| `has_introduction` | Artifact → literal | Descriptive text |

---

## REST API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Service info and endpoint list |
| `GET` | `/api/stats` | Dual-storage statistics (MySQL + Neo4j counts) |
| `GET` | `/api/artifacts` | List relics. Query params: `search`, `dynasty`, `material`, `limit`, `offset` |
| `GET` | `/api/artifacts/{artifact_id}` | Single relic detail |
| `GET` | `/api/graph/artifact/{artifact_id}` | Neo4j neighborhood graph for one artifact |
| `GET` | `/api/graph/dynasty/{dynasty_name}` | Query artifacts by dynasty (graph pattern query) |

### Example

```bash
curl http://localhost:8000/api/stats
curl "http://localhost:8000/api/artifacts?search=ming&limit=10"
curl http://localhost:8000/api/graph/dynasty/Ming
```

---

## Configuration

### Backend environment variables

Copy `backend/.env.example` to `backend/.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `MYSQL_HOST` | `localhost` | MySQL host |
| `MYSQL_PORT` | `3306` | MySQL port |
| `MYSQL_USER` | `kg_user` | MySQL username |
| `MYSQL_PASSWORD` | `kg_password` | MySQL password |
| `MYSQL_DATABASE` | `cultural_relics_kg` | Database name |
| `NEO4J_URI` | `bolt://localhost:7687` | Neo4j connection URI |
| `NEO4J_USER` | `neo4j` | Neo4j username |
| `NEO4J_PASSWORD` | `neo4j_password` | Neo4j password |
| `MUSEUM_TARGET` | `met` | Crawler target museum |
| `CRAWL_MAX_OBJECTS` | `100` | Default max objects per crawl |
| `API_PORT` | `8000` | REST API port |

### HarmonyOS app settings

| File | Setting | Description |
|------|---------|-------------|
| `entry/src/main/ets/services/KnowledgeGraphApi.ets` | `OFFLINE_ONLY` | `true` = bundled data only; `false` = try live API |
| `entry/src/main/ets/services/KnowledgeGraphApi.ets` | `API_BASE_URL` | Backend URL for live mode |
| `entry/src/main/ets/models/Artifact.ets` | `SAMPLE_RELICS` | Offline relic dataset (20 items) |

---

## Troubleshooting

### App shows 0 artifacts or blank list

- Rebuild the project in DevEco Studio (**Build → Rebuild Project**)
- Confirm `OFFLINE_ONLY = true` in `KnowledgeGraphApi.ets` for offline use
- Check that `Artifact.ets` (not `.ts`) is present under `entry/src/main/ets/models/`

### App cannot reach the backend API

- Ensure `python main.py serve` is running
- Use `http://10.0.2.2:8000` on the emulator, or your PC's LAN IP on a physical device
- Confirm `ohos.permission.INTERNET` is declared in `entry/src/main/module.json5`

### Backend cannot connect to MySQL / Neo4j

- Run `docker compose up -d` and wait for containers to become healthy
- Verify credentials in `backend/.env` match `docker-compose.yml`
- Run `python main.py init-db` before `demo` or `crawl`

### Crawl returns no artifacts

- Check internet connectivity
- The Met API may rate-limit requests; reduce `--max` or increase `CRAWL_DELAY_SECONDS` in `.env`
- Crawled data is always saved to `backend/data/crawled_artifacts.json` even if databases are offline

### Images not loading in the app

- Relic images load from `images.metmuseum.org` (HTTPS) and require internet on the device
- Text and stats still work offline; only remote images need a network connection

---

## License

Educational project for software engineering coursework.

Data crawled from **The Metropolitan Museum of Art Open Access API** is subject to [The Met's terms of use](https://www.metmuseum.org/about-the-met/policies-and-documents/open-access).
