#!/usr/bin/env python3
"""
sync_db.py – Standalone script to refresh all cached data in the NFL Dashboard DB.

Usage:
    python sync_db.py [--teams] [--rosters] [--free-agents] [--draft]

If no flags are provided, all data sources are synced.
"""
import argparse
import logging
import sys
from pathlib import Path

# Ensure the backend package is importable when running from /backend
sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import settings  # noqa: E402
from app.db.session import SessionLocal  # noqa: E402
from app.models import base  # noqa: E402, F401
from app.db.session import engine  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s – %(message)s",
)
logger = logging.getLogger("sync_db")


def main():
    parser = argparse.ArgumentParser(description="Sync NFL Dashboard database")
    parser.add_argument("--teams", action="store_true", help="Sync team data")
    parser.add_argument("--rosters", action="store_true", help="Sync roster data")
    parser.add_argument("--free-agents", action="store_true", help="Sync free agent data")
    parser.add_argument("--draft", action="store_true", help="Sync draft prospect data")
    args = parser.parse_args()

    sync_all = not any([args.teams, args.rosters, args.free_agents, args.draft])

    # Create tables if they don't exist yet
    base.Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if sync_all or args.teams:
            logger.info("Syncing teams …")
            from app.services.teams_service import sync_teams
            n = sync_teams(db)
            logger.info("  → %d teams synced", n)

        if sync_all or args.rosters:
            logger.info("Syncing rosters …")
            from app.services.roster_service import sync_rosters
            n = sync_rosters(db)
            logger.info("  → %d players synced", n)

        if sync_all or args.free_agents:
            logger.info("Syncing free agents …")
            from app.services.free_agents_service import sync_free_agents
            n = sync_free_agents(db)
            logger.info("  → %d free agents synced", n)

        if sync_all or args.draft:
            logger.info("Syncing draft prospects …")
            from app.services.draft_service import sync_draft_prospects
            n = sync_draft_prospects(db)
            logger.info("  → %d prospects synced", n)

    except Exception as exc:
        logger.error("Sync failed: %s", exc, exc_info=True)
        sys.exit(1)
    finally:
        db.close()

    logger.info("All syncs complete ✓")


if __name__ == "__main__":
    main()
