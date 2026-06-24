# SoftwareEnRiad — Chinese Cultural Relics Knowledge Graph

HarmonyOS client + Python backend implementing **Section 6.3.1 Knowledge Graph Construction Subsystem**.

## Architecture

```
Overseas Museum (The Met Open Access API)
        │
        ▼
   Data Crawler ──► Data Cleaning ──► Triplet Builder (SPO)
        │                                      │
        ▼                                      ▼
   MySQL (relational)                    Neo4j (graph)
   • artifact details                    • entities & relations
   • users, crawl jobs                   • graph traversal / SPARQL-like queries
        │                                      │
        └──────────────┬───────────────────────┘
                       ▼
              FastAPI REST API
                       ▼
              HarmonyOS Mobile App
```

## Subsystem Features (6.3.1)

| Module | Description |
|--------|-------------|
| **Data crawling** | Crawls Chinese cultural relics from **The Metropolitan Museum of Art** (overseas museum) via Open Access API |
| **Data modeling** | Converts records to triplets with entities (`Artifact`, `Museum`, `Dynasty`, `Artist`, `Location`, `Material`, `ArtifactType`, `Culture`) and relations (`collected_in`, `created_in`, `belongs_to_dynasty`, `created_by`, `material_is`, `type_is`, …) |
| **Dual storage** | **MySQL** for structured business queries; **Neo4j** for graph traversal and relationship queries; optional **RDF Turtle** export for LOD |

## Quick Start

### 1. Start databases

```bash
docker compose up -d
```

Neo4j Browser: http://localhost:7474 (user: `neo4j`, password: `neo4j_password`)

### 2. Install Python backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env
```

### 3. Load sample data (no live crawl needed)

```bash
python main.py init-db
python main.py demo
```

### 4. Crawl live data from The Met

```bash
python main.py crawl --max 50 --download-images
```

### 5. Start REST API

```bash
python main.py serve
```

API docs: http://localhost:8000/docs

### 6. Export Linked Open Data (optional)

```bash
python main.py export-rdf
# → backend/data/cultural_relics.ttl
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/stats` | Dual-storage statistics |
| `GET /api/artifacts` | List relics (supports `search`, `dynasty`, `material`) |
| `GET /api/artifacts/{id}` | Single relic detail |
| `GET /api/graph/artifact/{id}` | Neo4j neighborhood graph |
| `GET /api/graph/dynasty/{name}` | Query artifacts by dynasty |

## HarmonyOS App

Open the project in **DevEco Studio** and run on a phone emulator or device.

The app displays:
- Knowledge graph statistics (artifacts, nodes, relationships)
- Searchable cultural relic list with images
- Detail view with triplet relationships
- Offline fallback using bundled Met Museum sample data

Configure the API URL in `entry/src/main/ets/services/KnowledgeGraphApi.ets` if needed.

## Project Structure

```
softwareEnRiad/
├── backend/                 # Python KG construction subsystem
│   ├── crawler/             # Met Museum crawler
│   ├── pipeline/            # Cleaning + triplet builder
│   ├── storage/             # MySQL + Neo4j dual layer
│   ├── api/                 # FastAPI REST service
│   ├── schema/              # DB init scripts
│   ├── data/                # Sample & exported data
│   └── main.py              # CLI entry point
├── entry/                   # HarmonyOS mobile app
├── docker-compose.yml       # MySQL + Neo4j
└── README.md
```

## Entity & Relationship Ontology

**Entities:** `Artifact`, `Museum`, `Dynasty`, `Artist`, `Location`, `Material`, `ArtifactType`, `Culture`

**Relations:** `collected_in`, `created_in`, `belongs_to_dynasty`, `created_by`, `material_is`, `type_is`, `belongs_to_culture`, `located_in`, `has_name`, `has_age`, `has_image`, `has_detail_url`, `has_introduction`

## License

Educational project — The Met Open Access API data is subject to The Met's terms of use.
