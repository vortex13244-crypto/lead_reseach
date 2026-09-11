"""Local SQLite database for tracking contacted leads."""

import sqlite3
import threading
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ContactedLead:
    overture_id: str
    name: str
    contacted_at: str


class CRMDatabase:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._local = threading.local()
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        if not hasattr(self._local, "conn"):
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self._local.conn = sqlite3.connect(
                self.db_path,
                check_same_thread=False,
                isolation_level=None,  # autocommit
            )
        return self._local.conn

    def _init_db(self):
        conn = self._get_conn()
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS contacted_leads (
                overture_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                contacted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    def mark_contacted(self, overture_id: str, name: str) -> None:
        """Mark a lead as contacted."""
        if not overture_id:
            return
        conn = self._get_conn()
        conn.execute(
            """
            INSERT INTO contacted_leads (overture_id, name)
            VALUES (?, ?)
            ON CONFLICT(overture_id) DO NOTHING
            """,
            (overture_id, name),
        )

    def is_contacted(self, overture_id: str) -> bool:
        """Check if a lead has been contacted."""
        if not overture_id:
            return False
        conn = self._get_conn()
        cursor = conn.execute(
            "SELECT 1 FROM contacted_leads WHERE overture_id = ?",
            (overture_id,)
        )
        return cursor.fetchone() is not None

    def get_all_contacted_ids(self) -> set[str]:
        """Return a set of all contacted overture_ids for fast filtering."""
        conn = self._get_conn()
        cursor = conn.execute("SELECT overture_id FROM contacted_leads")
        return {row[0] for row in cursor.fetchall()}
