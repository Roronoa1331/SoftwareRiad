#!/usr/bin/env python3
"""
Knowledge Graph Construction Subsystem (Section 6.3.1)

CLI for crawling overseas museum data, building triplets,
and storing in MySQL + Neo4j dual-layer architecture.

Usage:
  python main.py crawl [--max N] [--download-images]
  python main.py init-db
  python main.py import-json [--file path]
  python main.py export-rdf [--file path]
  python main.py serve
  python main.py demo
"""

import argparse
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(BACKEND_ROOT))

from config.settings import settings  # noqa: E402
from crawler.met_museum import get_crawler  # noqa: E402
from pipeline.cleaner import clean_artifact, download_image  # noqa: E402
from pipeline.triplet_builder import build_triples_batch, triples_to_rdf_turtle  # noqa: E402
from storage import DualLayerStore  # noqa: E402


def cmd_crawl(args: argparse.Namespace) -> None:
    crawler = get_crawler(settings.museum_target)
    store = DualLayerStore()
    records = []

    print(f"Crawling Chinese cultural relics from {crawler.museum_name}...")
    for raw in crawler.crawl(max_objects=args.max):
        record = clean_artifact(raw)
        if args.download_images:
            record = download_image(record)
        records.append(record)
        print(f"  [{len(records)}] {record.name}")

    if not records:
        print("No artifacts crawled. Check network connectivity or try again later.")
        return

    json_path = settings.data_dir / "crawled_artifacts.json"
    result = store.save_to_json_fallback(records, json_path)
    print(f"Saved {result['artifacts_saved']} artifacts, {result['triples_saved']} triples to {json_path}")

    try:
        store.init_databases()
        db_result = store.save_artifacts(records)
        store.mysql.record_crawl_job(
            settings.museum_target,
            "completed",
            db_result["artifacts_saved"],
            db_result["triples_saved"],
        )
        print(
            f"MySQL: {db_result['artifacts_saved']} artifacts | "
            f"Neo4j: {db_result['triples_saved']} triples"
        )
    except Exception as exc:
        print(f"Database write skipped ({exc}). JSON fallback data is available.")
    finally:
        store.close()


def cmd_init_db(args: argparse.Namespace) -> None:
    store = DualLayerStore()
    store.init_databases()
    print("MySQL schema and Neo4j constraints initialized.")
    store.close()


def cmd_import_json(args: argparse.Namespace) -> None:
    path = Path(args.file)
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)
    store = DualLayerStore()
    store.init_databases()
    result = store.import_json_to_databases(path)
    print(f"Imported {result['artifacts_saved']} artifacts, {result['triples_saved']} triples.")
    store.close()


def cmd_export_rdf(args: argparse.Namespace) -> None:
    path = Path(args.file)
    store = DualLayerStore()
    records, _ = store.load_from_json(path)
    triples = build_triples_batch(records)
    rdf_path = settings.data_dir / "cultural_relics.ttl"
    rdf_path.write_text(triples_to_rdf_turtle(triples), encoding="utf-8")
    print(f"Exported {len(triples)} triples to {rdf_path} (LOD-ready Turtle format).")
    store.close()


def cmd_serve(args: argparse.Namespace) -> None:
    from api.main import run_server

    print(f"Starting API server at http://{settings.api_host}:{settings.api_port}")
    run_server()


def cmd_demo(args: argparse.Namespace) -> None:
    """Run full pipeline with bundled sample data (no live crawl required)."""
    sample_path = settings.data_dir / "sample_artifacts.json"
    if not sample_path.exists():
        print(f"Sample data missing: {sample_path}")
        sys.exit(1)

    store = DualLayerStore()
    try:
        store.init_databases()
        result = store.import_json_to_databases(sample_path)
        stats = store.get_stats()
        print("Demo pipeline completed successfully.")
        print(f"  Artifacts imported: {result['artifacts_saved']}")
        print(f"  Triples imported:   {result['triples_saved']}")
        print(f"  MySQL total:        {stats['mysql_artifacts']}")
        print(f"  Neo4j nodes:        {stats['neo4j']['nodes']}")
        print(f"  Neo4j relationships:{stats['neo4j']['relationships']}")
    except Exception as exc:
        print(f"Databases unavailable ({exc}). Using JSON-only mode.")
        records, triples = store.load_from_json(sample_path)
        print(f"  Sample artifacts: {len(records)}")
        print(f"  Sample triples:   {len(triples)}")
    finally:
        store.close()


def main():
    parser = argparse.ArgumentParser(
        description="Knowledge Graph Construction Subsystem (6.3.1)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    crawl_p = sub.add_parser("crawl", help="Crawl overseas museum website")
    crawl_p.add_argument("--max", type=int, default=settings.crawl_max_objects)
    crawl_p.add_argument("--download-images", action="store_true")
    crawl_p.set_defaults(func=cmd_crawl)

    init_p = sub.add_parser("init-db", help="Initialize MySQL and Neo4j schemas")
    init_p.set_defaults(func=cmd_init_db)

    import_p = sub.add_parser("import-json", help="Import JSON data into databases")
    import_p.add_argument(
        "--file",
        default=str(settings.data_dir / "crawled_artifacts.json"),
    )
    import_p.set_defaults(func=cmd_import_json)

    export_p = sub.add_parser("export-rdf", help="Export triples as RDF Turtle (LOD)")
    export_p.add_argument(
        "--file",
        default=str(settings.data_dir / "sample_artifacts.json"),
    )
    export_p.set_defaults(func=cmd_export_rdf)

    serve_p = sub.add_parser("serve", help="Start REST API server")
    serve_p.set_defaults(func=cmd_serve)

    demo_p = sub.add_parser("demo", help="Load sample data into dual storage")
    demo_p.set_defaults(func=cmd_demo)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
