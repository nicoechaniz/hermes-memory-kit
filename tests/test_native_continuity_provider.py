"""HMK remains independent of dialogue configuration, using real temp SQL.

Only embedding computation is replaced by a deterministic vector. No provider
inference, live credentials, or live library are involved. Set
HMK_TEST_MEMORYCTL_PATH to test an older deployed artifact copied into a temp dir.
"""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
MEMORYCTL = Path(os.environ.get("HMK_TEST_MEMORYCTL_PATH", ROOT / "scripts/memoryctl.py"))


@pytest.mark.parametrize("dialogue_enabled", [False, True])
def test_real_hmk_retrieval_and_librarian_ignore_dialogue(
    tmp_path, monkeypatch, provider_module, dialogue_enabled,
):
    # Clear ALL inherited HMK/embedding paths before import-time resolution.
    for key in tuple(os.environ):
        if key.startswith(("HMK_", "HERMES_", "AGENT_MEMORY_")):
            monkeypatch.delenv(key)
    home = tmp_path / "hermes-home"
    base = tmp_path / "custom-memory-base"
    home.mkdir()
    base.mkdir()
    config = {
        "memory": {"provider": "hmk-memory", "memory_enabled": False,
                   "user_profile_enabled": False},
        "plugins": {"enabled": ["hmk-memory"] + (["dialogue-handoff"] if dialogue_enabled else []),
                    "disabled": [] if dialogue_enabled else ["dialogue-handoff"]},
    }
    config_path = home / "config.yaml"
    config_path.write_text(yaml.safe_dump(config))
    config_before = config_path.read_bytes()
    monkeypatch.setenv("HMK_AGENT_MEMORY_BASE", str(base))
    monkeypatch.setenv("HMK_HERMES_HOME", str(home))
    monkeypatch.setenv("HMK_ENV_FILE", str(home / "absent.env"))
    monkeypatch.setenv("HMK_MEMORYCTL_PATH", str(MEMORYCTL))
    monkeypatch.setenv("HERMES_EMBED_PROVIDER", "local")
    monkeypatch.setenv("HERMES_RERANK_PROVIDER", "none")
    spec = importlib.util.spec_from_file_location("isolated_memoryctl", MEMORYCTL)
    assert spec is not None and spec.loader is not None
    mc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mc)
    mc.init_db()
    chapter = mc.add_text("library", "amber", "amber continuity fixture", tags=["fixture"])
    provider = provider_module.HMKMemoryProvider()
    assert provider.is_available()
    provider.initialize(session_id="selected-session", hermes_home=str(home))
    loaded = provider._get_memoryctl()
    assert loaded.DB_PATH == base / "library.db"
    assert loaded.HERMES_ENV_PATH == home / "absent.env"
    embedding_queries = []

    def embedding_fixture(_provider, texts, **kwargs):
        embedding_queries.extend(texts)
        return [[1.0, 0.0] for _ in texts]

    monkeypatch.setattr(loaded, "embed_texts", embedding_fixture)
    assert provider.prefetch("   ") == ""
    assert not embedding_queries
    assert f"[mem:{chapter}]" in provider.prefetch("amber")
    assert embedding_queries == ["amber"]
    assert any(s["name"] == "librarian" for s in provider.get_tool_schemas())
    expanded = json.loads(provider.handle_tool_call("librarian", {"action": "expand", "chapter_id": chapter}))
    assert expanded["success"] is True
    assert expanded["chapter"]["raw"] == "amber continuity fixture"
    null = json.loads(provider.handle_tool_call("librarian", {"action": "query", "query": "absentword"}))
    assert null["null_retrieval"] is True
    assert null["items"] == []
    # Re-entry cannot trigger an import, access counters, embedding work, or
    # schema work, even alongside the legacy memoryctl artifact.
    db_before = (base / "library.db").read_bytes()
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/continuityctl.py"), "rehydrate"],
        text=True, capture_output=True, check=True,
    )
    assert json.loads(result.stdout)["continuity"]["restored"] is False
    assert (base / "library.db").read_bytes() == db_before
    assert config_path.read_bytes() == config_before
    assert not (home / "memories").exists()
    assert not (base / "state/DIALOGUE-HANDOFF.md").exists()
    # A failed embedding backend means absent recall, not stale handoff/native
    # store substitution. Runtime scheduling/loader behavior is tested by Hermes.
    def unavailable(*args, **kwargs):
        raise SystemExit("fixture backend unavailable")
    monkeypatch.setattr(loaded, "embed_texts", unavailable)
    assert provider.prefetch("amber") == ""
    assert config_path.read_bytes() == config_before
