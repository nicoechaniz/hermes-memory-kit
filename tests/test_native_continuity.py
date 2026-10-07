"""Native continuity must not be reconstructed from unscoped HMK state."""
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def run_rehydrate(tmp_path, *args):
    home = tmp_path / "hermes-home"
    base = tmp_path / "agent-memory"
    (home / "memories").mkdir(parents=True, exist_ok=True)
    (base / "state").mkdir(parents=True, exist_ok=True)
    # Directories in place of files make any accidental legacy read fail,
    # even if the content would subsequently be filtered out of the result.
    for path in (home / "memories" / "MEMORY.md", home / "memories" / "USER.md",
                 base / "state" / "DIALOGUE-HANDOFF.md",
                 base / "state" / "ACTIVE-CONTEXT.md", base / "state" / "NOW.md"):
        path.mkdir(exist_ok=True)
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("HMK_", "HERMES_", "AGENT_MEMORY_"))}
    env.update(HMK_HERMES_HOME=str(home), HMK_AGENT_MEMORY_BASE=str(base))
    return subprocess.run([sys.executable, str(ROOT / "scripts/continuityctl.py"),
                           "rehydrate", *args], env=env, text=True, capture_output=True)


def test_default_rehydrate_does_not_read_legacy_state_or_retrieve(tmp_path):
    result = run_rehydrate(tmp_path)
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["mode"] == "native-first"
    assert data["continuity"]["source"] == "Hermes native session/goal state"
    assert data["continuity"]["restored"] is False
    assert data["retrieval"] is None
    assert data["exact_memories"] == []
    assert data["meta_context"] == {}
    assert "dialogue_handoff" not in data
    assert "episode_handoff" not in data
    assert "user" not in data.get("identity", {})
    assert "memory" not in data.get("identity", {})
    assert not (tmp_path / "agent-memory/library.db").exists()


def test_native_reentry_guidance_needs_no_hmk_roots(tmp_path):
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("HMK_", "HERMES_", "AGENT_MEMORY_"))}
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/continuityctl.py"), "rehydrate",
         "--always-retrieve", "--max-dialogue-lines", "99"],
        env=env, text=True, capture_output=True, cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["retrieval"] is None
    assert "deprecated" in result.stderr.lower()


def test_ownership_policy_uses_native_state_not_shared_handoff():
    policy = json.loads((ROOT / "policies/memory-ownership.v1.json").read_text())
    continuity = next(item for item in policy["artifact_classes"]
                      if item["id"] == "dialogue-continuity")
    paths = continuity["selector"]["path_globs"]
    assert "${HERMES_HOME}/state.db" in paths
    assert not any("DIALOGUE-HANDOFF" in path for path in paths)
