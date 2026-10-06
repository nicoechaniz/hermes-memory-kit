#!/usr/bin/env python3
"""Inspect general-memory behavior using disposable fictional data only.

Run from any directory: python3 docs/benchmarks/general-memory-diagnostics.py
Outputs observations, not a passing regression suite. No model or embedding
service is called. Real persistence paths are replaced by temporary fixtures.
"""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def run_script(name: str, *args: str):
    return subprocess.run(
        [sys.executable, str(REPO / "scripts" / name), *args],
        check=True, capture_output=True, text=True, timeout=20,
    )


def inspect(base: Path) -> dict:
    base.mkdir()
    # Import without inspecting the operator's .env or live memory binding.
    with patch.dict(os.environ, {
        "HMK_AGENT_MEMORY_BASE": str(base),
        "HMK_DB_PATH": str(base / "library.db"),
        "HMK_WORKSPACE_ROOT": str(base.parent),
        "HMK_HERMES_HOME": str(base.parent / "fixture-home"),
        "HMK_LIBRARY_CORPUS_PREFIX": "",
        "HERMES_HOME": str(base.parent / "fixture-home"),
    }, clear=True):
        sys.path.insert(0, str(REPO / "scripts"))
        mc = load_module("hmk_general_review", REPO / "scripts/memoryctl.py")
        mc.init_db()
        observations = {}

        query = "Do you remember the name of the person who proposed replay in HarborMesh?"
        observations["lexical_query"] = {
            "query": query, "tokens_used": mc.tokenize_query(query),
            "project_name_retained": "harbormesh" in mc.tokenize_query(query),
            "accented_name_tokens": mc.tokenize_query("Nicolás Echániz"),
        }
        row = {"source_path": "", "shelf": "episodes"}
        observations["domain_prior"] = {
            "empty_prefix_episode": mc.source_domain_prior("Mara encounter", row),
        }
        with patch.object(mc, "BIBLIOTECA_PREFIX", "/fictional/research/"):
            observations["domain_prior"].update({
                "configured_prefix_episode": mc.source_domain_prior("Mara encounter", row),
                "configured_prefix_research": mc.source_domain_prior(
                    "Mara encounter", {"source_path": "/fictional/research/paper.md", "shelf": "evidence"}),
            })

        # Test actual migration backup completeness while committed data is in WAL.
        holder = mc.connect()
        holder.execute("PRAGMA wal_autocheckpoint=0")
        holder.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        old_episode = mc.add_text("episodes", "Imported encounter", "An encounter years ago; exact occurrence date unknown.")
        run_script("migrate-engram.py")
        backup = next(base.glob("library.db.bak.preengram.*"))
        with sqlite3.connect(backup) as con:
            backup_count = con.execute("SELECT COUNT(*) FROM chapters").fetchone()[0]
        observations["migration_backup"] = {
            "committed_chapters_before_migration": 1,
            "chapters_in_backup": backup_count,
        }
        holder.close()
        new_episode = mc.add_text("episodes", "New encounter", "A distinct encounter recorded after migration.")
        with mc.connect() as con:
            old = dict(con.execute("SELECT created_at,event_ts FROM chapters WHERE id=?", (old_episode,)).fetchone())
            new_type = con.execute("SELECT engram_type FROM chapters WHERE id=?", (new_episode,)).fetchone()[0]
        observations["episodic_metadata"] = {
            "unknown_event_time_assigned_recording_time": old["created_at"] == old["event_ts"],
            "new_episodes_shelf_record_type": new_type,
        }

        first = mc.add_text("library", "李青", "firstpersonmarker: a fictional person's separate encounter.")
        mc.add_text("library", "王岚", "secondpersonmarker: another fictional person's separate encounter.")
        observations["unicode_titles"] = {
            "first_slug": mc.slugify("李青"), "second_slug": mc.slugify("王岚"),
            "first_person_still_present": bool(mc.search("firstpersonmarker")),
            "old_id_now_names": mc.expand(first)["title"],
        }

        episode = mc.add_text("episodes", "Queue proposal", "Mara proposed a local replay queue in the relay project.", importance=0.9)
        project = mc.add_text("library", "Relay project", "We maintain the relay scheduler.", importance=0.9)
        mc.add_link(episode, project, "concerns")
        observations["link_traversal"] = {
            "episode_outgoing_neighbors": len(mc.expand(episode)["neighbors"]),
            "project_incoming_relations_returned": len(mc.expand(project)["neighbors"]),
        }
        mc.update_chapter(project, content="We paused relay rollout pending calibration.")
        observations["native_history"] = {
            "old_project_text_searchable_after_update": bool(mc.search("maintain scheduler")),
            "current_project_text": mc.expand(project)["raw"],
        }

        a = mc.add_text("episodes", "HarborMesh shared event with local group about relay Mara", "Mara proposed an offline queue.")
        b = mc.add_text("episodes", "HarborMesh shared event with local group about relay Jo", "Jo taught a mount-listening technique.")
        packed = mc.pack("HarborMesh", threshold=0.0, limit=8)
        observations["distinct_episode_dedup"] = {
            "lexical_candidates": [r["id"] for r in mc.search("HarborMesh")],
            "packed_ids": [r["id"] for r in packed["items"]],
            "both_distinct_events_retained_in_pack": {a, b} <= {r["id"] for r in packed["items"]},
        }
        def unavailable(*args, **kwargs):
            raise mc.EmbeddingBackendError("synthetic embedding outage")
        with patch.object(mc, "semantic_search", unavailable):
            try:
                mc.hybrid_pack("HarborMesh", provider="nvidia", model="fixture")
                observations["hybrid_outage"] = "returned results"
            except mc.EmbeddingBackendError:
                observations["hybrid_outage"] = "raised despite existing lexical candidates"
        weak = {"id": episode, "spr": "Unrelated fixture", "score": 0.001, "shelf": "episodes"}
        with patch.object(mc, "hybrid_pack", return_value={"items": [weak]}):
            fused = mc.engram_pack("unobserved launch", threshold=0.30)
        observations["engram_relevance_gate"] = {
            "mock_input_score": 0.001, "requested_threshold": 0.30,
            "null_retrieval": fused["null_retrieval"], "items_returned": len(fused["items"]),
        }

        # Run the real backfill writer using a printing fixture, never Hermes/model inference.
        fake = base.parent / "fake-hermes"
        Path(os.environ["HMK_HERMES_HOME"]).mkdir()
        fake.write_text(f"#!{sys.executable}\nprint('social | Fictional auditneedle participant helped with a repair.')\n")
        fake.chmod(0o700)
        with patch.dict(os.environ, {"HMK_HERMES_BIN": str(fake)}):
            run_script("backfill-semantic.py", "--shelf-pattern", "episodes", "--limit", "1", "--sleep", "0")
        with mc.connect() as con:
            extracted = con.execute("SELECT COUNT(*) FROM chapters WHERE raw LIKE '%auditneedle%'").fetchone()[0]
        observations["semantic_backfill"] = {
            "extracted_rows_present": extracted,
            "lexical_hits_for_extracted_fact": len(mc.search("auditneedle")),
        }

        workspace = base.parent / "bootstrap-fixture"
        run_script("bootstrap_agent.py", str(workspace), "--name", "fixture")
        learned = workspace / "hermes-home/skills/memory/learned-method/SKILL.md"
        learned.parent.mkdir(parents=True)
        learned.write_text("# Fictional learned method\nPreserve this acquired skill.\n")
        run_script("bootstrap_agent.py", str(workspace), "--upgrade")
        observations["skill_upgrade"] = {"custom_method_preserved": learned.exists()}
        return observations


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="hmk-general-review-") as scratch:
        observations = inspect(Path(scratch) / "memory")
    print(json.dumps({"synthetic_only": True, "model_inference": False, "observations": observations}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
