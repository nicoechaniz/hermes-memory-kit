#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

import os as _os
import sys as _sys


def _resolve(keys):
    """v3.0: resolve path from env cascade. Returns None if none set."""
    for k in keys:
        v = _os.environ.get(k)
        if v:
            return Path(v).expanduser()
    return None


def _require(name: str, value):
    if value is None:
        _sys.stderr.write(
            f"ERROR: continuityctl needs {name} resolvable from env.\n"
            "       Load your agent's .env before running. The 'hmk' wrapper\n"
            "       does this automatically. See hermes-memory-kit v3.0 docs.\n"
        )
        _sys.exit(2)
    return value


AGENT_MEMORY_BASE = _resolve(["HMK_AGENT_MEMORY_BASE", "AGENT_MEMORY_BASE", "HMK_BASE_DIR"])

# The module-level constants below are lazy-built from the cascade roots.
# If roots are None, downstream functions will hit _require() and hard-fail.
BASE_DIR = AGENT_MEMORY_BASE
STATE_DIR = (BASE_DIR / "state") if BASE_DIR else None
ACTIVE_CONTEXT_PATH = (STATE_DIR / "ACTIVE-CONTEXT.md") if STATE_DIR else None


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace").strip()


def parse_sections(text: str):
    sections = {}
    current = None
    buf = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = line[3:].strip()
            buf = []
            continue
        buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


def load_active_context():
    text = read_text(ACTIVE_CONTEXT_PATH)
    if not text:
        return {}
    return parse_sections(text)


def render_bullets(items):
    if not items:
        return "- none"
    return "\n".join(f"- {item}" for item in items)


def update_active_context(args):
    sections = load_active_context()

    def set_section(name, values):
        if values is None:
            return
        sections[name] = render_bullets(values)

    set_section("Active Goal", args.goal)
    set_section("Current Focus", args.focus)
    set_section("Open Tasks", args.tasks)
    set_section("Blockers", args.blockers)
    set_section("Next Steps", args.next_steps)
    set_section("Last Topic", args.last_topic)
    set_section("Last User Intent", args.last_user_intent)
    set_section("Last Working Set", args.last_working_set)
    set_section("Resume Hint", args.resume_hint)
    set_section("Relevant Memory", args.memories)
    set_section("Notes", args.notes)

    status_lines = []
    if args.state:
        status_lines.append(f"- state: {args.state}")
    if args.confidence:
        status_lines.append(f"- confidence: {args.confidence}")
    if args.last_updated:
        status_lines.append(f"- last_updated: {args.last_updated}")
    if status_lines:
        sections["Status"] = "\n".join(status_lines)

    ordered = [
        "Status",
        "Active Goal",
        "Current Focus",
        "Open Tasks",
        "Blockers",
        "Next Steps",
        "Last Topic",
        "Last User Intent",
        "Last Working Set",
        "Resume Hint",
        "Relevant Memory",
        "Notes",
    ]
    lines = ["# ACTIVE-CONTEXT", ""]
    for name in ordered:
        value = sections.get(name)
        if value is None:
            continue
        lines.append(f"## {name}")
        lines.append("")
        lines.append(value.strip() if value.strip() else "- none")
        lines.append("")
    ACTIVE_CONTEXT_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return {"ok": True, "path": str(ACTIVE_CONTEXT_PATH)}


def rehydrate(args):
    """Describe native re-entry; never guess a dialogue from shared files."""
    return {
        "mode": "native-first",
        "continuity": {
            "source": "Hermes native session/goal state",
            "restored": False,
            "guidance": (
                "Resume the intended session through Hermes /resume; use session_search "
                "for explicitly selected history and native /goal for the active mission. "
                "This command does not restore a session or infer one from platform, "
                "recency, engineering notes, or a parent ID. Current user direction wins."
            ),
        },
        "meta_context": {},
        "exact_memories": [],
        "query": None,
        "retrieval": None,
    }


def main():
    parser = argparse.ArgumentParser(description="Tactical continuity control for Hermes")
    sub = parser.add_subparsers(dest="command", required=True)

    show = sub.add_parser("show")
    show.add_argument("--json", action="store_true")

    upd = sub.add_parser("update")
    upd.add_argument("--state")
    upd.add_argument("--confidence")
    upd.add_argument("--last-updated")
    upd.add_argument("--goal", nargs="*")
    upd.add_argument("--focus", nargs="*")
    upd.add_argument("--tasks", nargs="*")
    upd.add_argument("--blockers", nargs="*")
    upd.add_argument("--next-steps", nargs="*")
    upd.add_argument("--last-topic", nargs="*")
    upd.add_argument("--last-user-intent", nargs="*")
    upd.add_argument("--last-working-set", nargs="*")
    upd.add_argument("--resume-hint", nargs="*")
    upd.add_argument("--memories", nargs="*")
    upd.add_argument("--notes", nargs="*")

    reh = sub.add_parser(
        "rehydrate", help="Deprecated: native session/goal re-entry guidance only",
        description="No file or database reads. Legacy options are accepted but ignored.",
    )
    reh.add_argument("--budget", type=int, default=700)
    reh.add_argument("--limit", type=int, default=2)
    reh.add_argument("--threshold", type=float, default=0.52)
    reh.add_argument("--max-identity-lines", type=int, default=4)
    reh.add_argument("--max-state-lines", type=int, default=6)
    reh.add_argument("--max-episode-lines", type=int, default=4)
    reh.add_argument("--max-dialogue-lines", type=int, default=6)
    reh.add_argument("--max-memory-lines", type=int, default=5)
    reh.add_argument("--relevant-limit", type=int, default=2)
    reh.add_argument("--skip-retrieval", action="store_true")
    reh.add_argument("--always-retrieve", action="store_true")

    args = parser.parse_args()
    if args.command != "rehydrate":
        _require("HMK_AGENT_MEMORY_BASE", AGENT_MEMORY_BASE)

    if args.command == "show":
        if args.json:
            print(json.dumps(load_active_context(), indent=2, ensure_ascii=False))
        else:
            print(read_text(ACTIVE_CONTEXT_PATH))
        return

    if args.command == "update":
        print(json.dumps(update_active_context(args), indent=2, ensure_ascii=False))
        return

    if args.command == "rehydrate":
        _sys.stderr.write(
            "Deprecated: rehydrate now returns native re-entry guidance only; "
            "legacy retrieval/summary flags have no effect. Use Hermes resume/history "
            "for dialogue, continuityctl show for engineering notes, and "
            "memoryctl hybrid-pack or librarian for explicit durable recall.\n"
        )
        print(json.dumps(rehydrate(args), indent=2, ensure_ascii=False))
        return


if __name__ == "__main__":
    main()
