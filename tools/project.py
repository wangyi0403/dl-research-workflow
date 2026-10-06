"""Initialize and validate a project-local research workflow using only the standard library."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = ("data", "experiments/configs", "experiments/src", "results/data", "results/figures", "results/logs", "results/tables", "paper")
ROOT_FILES = ("AGENTS.md", "AI_START.md", "CLAUDE.md", "README.md", "README_CN.md", "SETUP.md", "SETUP_CN.md", "LICENSE", "NOTICE.md", "VERSION", ".gitignore", ".gitattributes", "skill-manifest.json", "skills-catalog.json")
LICENSE_FILES = ("Orchestra-Research-MIT.txt", "lieflat-less-ai-tone-MIT.txt")

def manifest(root=ROOT):
    return json.loads((root / "skill-manifest.json").read_text(encoding="utf-8"))

def select_skills(spec, profiles, explicit):
    available = {item["name"] for item in spec["skills"]}
    choices = {item["name"]: set(item["skills"]) for item in spec["profiles"]}
    choices["full"] = available
    selected = set(explicit or ())
    for profile in profiles or ():
        if profile not in choices:
            raise ValueError(f"Unknown profile: {profile}")
        selected.update(choices[profile])
    if not selected or selected - available:
        raise ValueError("Select at least one valid bundled profile or skill.")
    return sorted(selected)

def files_under(directory):
    return [p for p in directory.rglob("*") if p.is_file() and not any(x in {"__pycache__", ".pytest_cache", ".ruff_cache"} for x in p.parts) and p.suffix not in {".pyc", ".pyo"}]

def prepare(target, operation, profiles, explicit, agent, dry_run):
    target = target.resolve()
    if target == ROOT or target in ROOT.parents or ROOT in target.parents:
        raise ValueError("Use a separate project directory outside the distribution checkout.")
    spec = manifest()
    selected = select_skills(spec, profiles, explicit)
    for name in selected:
        if not (ROOT / ".agents/skills" / name / "SKILL.md").is_file():
            raise ValueError(f"Source skill is not bundled here: {name}; use the complete distribution checkout.")
    plan = {}
    def include(source, relative):
        destination = target / relative
        if not destination.resolve().is_relative_to(target):
            raise ValueError(f"Destination escapes project: {relative}")
        plan[destination] = source.read_bytes()
    for name in LICENSE_FILES:
        include(ROOT / "licenses" / name, Path("licenses") / name)
    if operation == "init":
        for relative in ROOT_FILES:
            include(ROOT / relative, relative)
        for folder in ("docs", "resources", "experiments", "tools", "licenses"):
            for source in files_under(ROOT / folder):
                include(source, source.relative_to(ROOT))
        for relative in FOLDERS:
            plan[target / relative / ".gitkeep"] = b""
    for name in selected:
        source_root = ROOT / ".agents/skills" / name
        for source in files_under(source_root):
            relative = source.relative_to(source_root)
            include(source, Path(".agents/skills") / name / relative)
            if agent == "claude":
                include(source, Path(".claude/skills") / name / relative)
    if agent == "claude":
        include(ROOT / "CLAUDE.md", "CLAUDE.md")
    for dependency in spec["runtime_dependencies"]:
        if set(dependency["required_by"]) & set(selected):
            for name in dependency["file_patterns"]:
                relative = Path(dependency["destination"]) / name
                include(ROOT / relative, relative)
    conflicts = [str(p.relative_to(target)) for p, data in plan.items() if p.exists() and (not p.is_file() or p.read_bytes() != data)]
    state_path = target / ".agenthub/project.json"
    if state_path.exists():
        previous = json.loads(state_path.read_text(encoding="utf-8"))
        if previous.get("template_version") != spec["template_version"]:
            raise ValueError("Existing deployment uses another version; review its local changes before upgrading.")
        if operation == "init":
            raise ValueError("Project is already initialized; use add for extra profiles.")
    if conflicts:
        raise ValueError("Conflict preflight wrote no files: " + ", ".join(conflicts))
    existing = {p.name for p in (target / ".agents/skills").glob("*") if (p / "SKILL.md").is_file()}
    state = {"template_version": spec["template_version"], "skills": sorted(existing | set(selected)), "agent": agent}
    print(json.dumps({"operation": operation, "agent": agent, "skills": selected, "planned_files": len(plan), "dry_run": dry_run}, indent=2))
    if dry_run:
        return
    # Preflight validates every destination before the first write; existing research is never overwritten.
    created = []
    try:
        for destination, data in plan.items():
            if destination.exists():
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("xb") as stream:
                stream.write(data)
            created.append(destination)
        state_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = state_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        temporary.replace(state_path)
    except Exception:
        for destination in reversed(created):
            if destination.resolve().is_relative_to(target):
                destination.unlink(missing_ok=True)
        raise

def check(target):
    target = target.resolve()
    failures = []
    def require(condition, message):
        if not condition:
            failures.append(message)
    spec = manifest(target)
    declared = {s["name"] for s in spec["skills"]}
    require(len(declared) == 18, "Expected 18 distinct core skill identities.")
    state = target / ".agenthub/project.json"
    if state.exists():
        expected = set(json.loads(state.read_text(encoding="utf-8"))["skills"])
    else:
        expected = declared
    for relative in ROOT_FILES:
        require((target / relative).is_file(), f"Missing {relative}")
    for name in LICENSE_FILES:
        require((target / "licenses" / name).is_file(), f"Missing upstream license: {name}")
    for relative in FOLDERS:
        require((target / relative).is_dir(), f"Missing directory {relative}")
    installed = {p.name for p in (target / ".agents/skills").glob("*") if (p / "SKILL.md").is_file()}
    require(expected <= installed, "Missing selected skills: " + ", ".join(sorted(expected - installed)))
    for name in installed:
        text = (target / ".agents/skills" / name / "SKILL.md").read_text(encoding="utf-8")
        require(text.startswith("---\n"), f"Missing skill frontmatter: {name}")
        require(bool(re.search(r'^name:\s*[\"\']?' + re.escape(name) + r'[\"\']?\s*$', text, re.M)), f"Skill identity mismatch: {name}")
    for dependency in spec["runtime_dependencies"]:
        if set(dependency["required_by"]) & expected:
            for name in dependency["file_patterns"]:
                require((target / dependency["destination"] / name).is_file(), f"Missing runtime support: {name}")
    catalog = json.loads((target / "skills-catalog.json").read_text(encoding="utf-8"))
    require({s["name"] for s in catalog["skills"]} == declared, "Catalog and manifest disagree.")
    with (target / "experiments/registry/experiments.csv").open(encoding="utf-8", newline="") as stream:
        fields = next(csv.reader(stream))
    require({"experiment_id", "status", "claim_id", "config_sha256", "dataset_version", "code_revision", "result_path", "state_path"} <= set(fields), "Missing experiment provenance fields.")
    documents = [target / p for p in ROOT_FILES if p.endswith(".md")]
    documents += list((target / "docs").glob("*.md"))
    for document in documents:
        if not document.is_file():
            continue
        text = document.read_text(encoding="utf-8")
        require(not re.search(r"[A-Za-z]:[/\\]Users[/\\][^\s/\\]+|/Users/[^\s/]+|/home/[^\s/]+", text), f"Personal absolute path in {document.name}")
        for match in re.finditer(r"\[[^\]\n]*\]\(([^)\n]+)\)", text):
            link = match.group(1).split("#", 1)[0].strip("<>")
            if not link or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", link):
                continue
            require((document.parent / link).exists(), f"Broken document link {document.name}: {link}")
    if failures:
        print("\n".join("FAIL: " + item for item in failures))
        return 1
    print(f"PASS: workflow {spec['template_version']}; {len(installed)} installed skills; selected runtime, registry and document links validated.")
    print("This is a structural check; scientific gates and live agent behavior require their own verification.")
    return 0

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    validator = sub.add_parser("check")
    validator.add_argument("project", type=Path, nargs="?", default=ROOT)
    for operation in ("init", "add"):
        action = sub.add_parser(operation)
        action.add_argument("project", type=Path)
        action.add_argument("--profile", nargs="+", default=None)
        action.add_argument("--skill", nargs="+", default=[])
        action.add_argument("--agent", choices=("generic", "codex", "claude", "dsh", "zcode"), default=None)
        action.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "list":
            spec = manifest()
            print(json.dumps({"version": spec["template_version"], "profiles": ["full"] + [p["name"] for p in spec["profiles"]], "skills": [s["name"] for s in spec["skills"]]}, indent=2))
            return 0
        if args.command == "check":
            return check(args.project)
        profiles = args.profile if args.profile is not None else ([] if args.skill else ["full"])
        agent = args.agent
        if agent is None:
            state_path = args.project / ".agenthub/project.json"
            agent = json.loads(state_path.read_text(encoding="utf-8")).get("agent", "generic") if state_path.exists() else "generic"
        prepare(args.project, args.command, profiles, args.skill, agent, args.dry_run)
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
