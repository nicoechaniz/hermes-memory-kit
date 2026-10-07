"""Verified online SQLite snapshots, including committed WAL pages."""
from __future__ import annotations

import os
from pathlib import Path
import sqlite3
import time


def verified_snapshot(source, destination, *, timeout=30):
    """Create a new private snapshot; never overwrite an existing recovery file.

    SQLite's backup API reads a consistent database, including its journal.
    Failed verification retains the snapshot for inspection and raises before
    the caller changes the source. This does not repair a damaged database.
    """
    source, destination = Path(source), Path(destination)
    fd = os.open(destination, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(fd)
    started = time.monotonic()

    def progress(status, remaining, total):
        if time.monotonic() - started > timeout:
            raise TimeoutError("SQLite snapshot exceeded its time budget")

    src = sqlite3.connect(source.resolve().as_uri() + "?mode=ro", uri=True)
    dst = sqlite3.connect(destination)
    try:
        src.backup(dst, pages=256, progress=progress, sleep=0.05)
        # A recovery snapshot is a standalone file. The source's WAL mode may
        # be copied by backup; normalize the destination before verifying it.
        if dst.execute("PRAGMA journal_mode=DELETE").fetchone()[0] != "delete":
            raise RuntimeError("SQLite snapshot could not become standalone")
        if dst.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
            raise RuntimeError("SQLite snapshot failed integrity verification")
        if dst.execute("PRAGMA foreign_key_check").fetchall():
            raise RuntimeError("SQLite snapshot has foreign-key violations")
    finally:
        dst.close()
        src.close()
    return destination
