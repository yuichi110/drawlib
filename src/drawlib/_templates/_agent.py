# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""AI coding agent instruction synthesizer and exporter for Drawlib."""

from __future__ import annotations

import importlib.resources
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Literal

AgentTriggerMode = Literal["auto", "always"]

MARKER_START: Final[str] = "<!-- drawlib-agent-instruction:start -->"
MARKER_END: Final[str] = "<!-- drawlib-agent-instruction:end -->"

_RULE_DESCRIPTION_AUTO: Final[str] = (
    "Drawlib pure-Python diagrams, charts, SmartArts, technical documentation (HTML/PDF/DOCX), "
    "and 16:9 slide decks (HTML/PDF/PPTX) as code. Load whenever creating, editing, or reviewing "
    "diagrams, charts, slides, or *_src/ documentation projects."
)
_RULE_DESCRIPTION_ALWAYS: Final[str] = (
    "Drawlib pure-Python diagrams, charts, SmartArts, technical documentation, and slides as code."
)
_COPILOT_APPLY_TO_AUTO: Final[str] = "**/*_src/**, **/*.md, **/*.py, **/drawlib.toml"


@dataclass(frozen=True)
class AgentTargetSpec:
    """Specification metadata for a supported AI coding agent instruction target.

    Attributes:
        name: Canonical CLI target identifier (e.g. 'antigravity', 'claude').
        label: Human-readable product name.
        project_rel_path: Default relative path inside a project workspace.
        global_rel_path: Default path relative to user's home directory, or None if unsupported.
        format_summary: Concise description of file format and frontmatter behavior.
        description: Summary of how the target integrates with the AI coding tool.
        merge_project_markers: Whether project file uses shared HTML comment marker blocks.
        merge_global_markers: Whether global file uses shared HTML comment marker blocks.
    """

    name: str
    label: str
    project_rel_path: str
    global_rel_path: str | None
    format_summary: str
    description: str
    merge_project_markers: bool = False
    merge_global_markers: bool = False


AGENT_TARGET_SPECS: Final[dict[str, AgentTargetSpec]] = {
    "antigravity": AgentTargetSpec(
        name="antigravity",
        label="Google Antigravity",
        project_rel_path=".agents/rules/drawlib.md",
        global_rel_path=".gemini/config/rules/drawlib.md",
        format_summary="YAML frontmatter (trigger: model_decision | always_on)",
        description="Modular rule file (.agents/rules/drawlib.md; falls back to .agent/rules/ if .agent/ exists).",
    ),
    "claude": AgentTargetSpec(
        name="claude",
        label="Claude Code",
        project_rel_path=".claude/rules/drawlib.md",
        global_rel_path=".claude/rules/drawlib.md",
        format_summary="Markdown (.claude/rules/)",
        description="Modular Claude Code rule file that coexists safely with root CLAUDE.md.",
    ),
    "cursor": AgentTargetSpec(
        name="cursor",
        label="Cursor",
        project_rel_path=".cursor/rules/drawlib.mdc",
        global_rel_path=None,
        format_summary="MDC frontmatter (description, alwaysApply)",
        description="Cursor MDC rule supporting Agent-Requested (auto) and Always-Apply modes.",
    ),
    "copilot": AgentTargetSpec(
        name="copilot",
        label="GitHub Copilot",
        project_rel_path=".github/instructions/drawlib.instructions.md",
        global_rel_path=None,
        format_summary="YAML frontmatter (description, applyTo)",
        description="Modular GitHub Copilot instructions coexisting with .github/copilot-instructions.md.",
    ),
    "windsurf": AgentTargetSpec(
        name="windsurf",
        label="Windsurf",
        project_rel_path=".windsurf/rules/drawlib.md",
        global_rel_path=".codeium/windsurf/memories/global_rules.md",
        format_summary="YAML frontmatter (trigger: model_decision | always_on)",
        description="Windsurf Cascade workspace rule (< 12,000 chars) or marker-merged global memory.",
        merge_project_markers=False,
        merge_global_markers=True,
    ),
    "cline": AgentTargetSpec(
        name="cline",
        label="Cline",
        project_rel_path=".clinerules/drawlib.md",
        global_rel_path="Documents/Cline/Rules/drawlib.md",
        format_summary="Markdown (.clinerules/ folder)",
        description="Modular Cline rule file toggleable individually in the Cline Rules UI.",
    ),
    "roo": AgentTargetSpec(
        name="roo",
        label="Roo Code",
        project_rel_path=".roo/rules/drawlib.md",
        global_rel_path=".roo/rules/drawlib.md",
        format_summary="Markdown (.roo/rules/)",
        description="Modular Roo Code workspace or user-global rule file.",
    ),
    "codex": AgentTargetSpec(
        name="codex",
        label="OpenAI Codex / AGENTS.md",
        project_rel_path="AGENTS.md",
        global_rel_path=".codex/AGENTS.md",
        format_summary="Shared Markdown (marker-merged block)",
        description="Universal AGENTS.md instruction block merged non-destructively via HTML comment markers.",
        merge_project_markers=True,
        merge_global_markers=True,
    ),
    "gemini": AgentTargetSpec(
        name="gemini",
        label="Gemini CLI / GEMINI.md",
        project_rel_path="GEMINI.md",
        global_rel_path=".gemini/GEMINI.md",
        format_summary="Shared Markdown (marker-merged block)",
        description="Standalone Gemini CLI context block merged non-destructively via HTML comment markers.",
        merge_project_markers=True,
        merge_global_markers=True,
    ),
}

ALL_MODULAR_AGENTS: Final[tuple[str, ...]] = (
    "antigravity",
    "claude",
    "cursor",
    "copilot",
    "windsurf",
    "cline",
    "roo",
)

_AGENT_ALIASES: Final[dict[str, str]] = {
    "antigravity": "antigravity",
    "jetski": "antigravity",
    "claude": "claude",
    "claude-code": "claude",
    "claudecode": "claude",
    "cursor": "cursor",
    "copilot": "copilot",
    "github-copilot": "copilot",
    "gh-copilot": "copilot",
    "windsurf": "windsurf",
    "cascade": "windsurf",
    "cline": "cline",
    "roo": "roo",
    "roo-code": "roo",
    "roocode": "roo",
    "codex": "codex",
    "agents": "codex",
    "agents-md": "codex",
    "agents.md": "codex",
    "gemini": "gemini",
    "gemini-cli": "gemini",
    "gemini-md": "gemini",
    "gemini.md": "gemini",
}


def _normalize_agent_name(agent: str) -> str:
    """Normalize an agent target name or alias to its canonical key."""
    key = agent.strip().lower().replace("_", "-")
    if key in _AGENT_ALIASES:
        return _AGENT_ALIASES[key]
    available = ", ".join([*AGENT_TARGET_SPECS.keys(), "all"])
    raise ValueError(f"Unknown AI agent target '{agent}'. Available targets: {available}")


def _normalize_mode(mode: str) -> AgentTriggerMode:
    """Validate and normalize trigger mode ('auto' or 'always')."""
    cleaned = mode.strip().lower()
    if cleaned == "auto":
        return "auto"
    if cleaned == "always":
        return "always"
    raise ValueError(f"Invalid mode '{mode}'. Must be 'auto' or 'always'.")


def _load_base_agent_instruction() -> str:
    """Load canonical Drawlib AI agent instruction Markdown body from package resources."""
    res = importlib.resources.files("drawlib._rules").joinpath("agent_instruction.md")
    return res.read_text(encoding="utf-8").strip()


def _build_frontmatter(canonical: str, mode: AgentTriggerMode, global_scope: bool) -> str:
    """Synthesize tool-specific YAML frontmatter header when required."""
    if canonical == "antigravity" or (canonical == "windsurf" and not global_scope):
        if mode == "always":
            return "---\ntrigger: always_on\n---\n\n"
        return f"---\ntrigger: model_decision\ndescription: {_RULE_DESCRIPTION_AUTO}\n---\n\n"

    if canonical == "cursor":
        if mode == "always":
            return f'---\ndescription: "{_RULE_DESCRIPTION_ALWAYS}"\nalwaysApply: true\n---\n\n'
        return f'---\ndescription: "{_RULE_DESCRIPTION_AUTO}"\nalwaysApply: false\n---\n\n'

    if canonical == "copilot":
        apply_to = "**" if mode == "always" else _COPILOT_APPLY_TO_AUTO
        desc = _RULE_DESCRIPTION_ALWAYS if mode == "always" else _RULE_DESCRIPTION_AUTO
        return f'---\ndescription: "{desc}"\napplyTo: "{apply_to}"\n---\n\n'

    return ""


def list_agent_targets() -> list[dict[str, str]]:
    """Return metadata for all supported AI coding agent instruction targets.

    Returns:
        list[dict[str, str]]: List of target metadata dictionaries with keys
            'name', 'label', 'project_path', 'global_path', 'format', and 'description'.
    """
    results: list[dict[str, str]] = []
    for spec in AGENT_TARGET_SPECS.values():
        global_display = f"~/{spec.global_rel_path}" if spec.global_rel_path is not None else "-"
        results.append(
            {
                "name": spec.name,
                "label": spec.label,
                "project_path": spec.project_rel_path,
                "global_path": global_display,
                "format": spec.format_summary,
                "description": spec.description,
            }
        )
    return results


def detect_agent_targets(destination: str | Path = ".") -> list[str]:
    """Detect AI coding agents configured in the given workspace directory.

    Inspects the workspace root for existing tool configuration directories or instruction
    files (such as ``.agents/``, ``.agent/``, ``.claude/``, ``.cursor/``,
    ``.github/instructions/``, ``.windsurf/``, ``.clinerules/``, ``.roo/``,
    ``AGENTS.md``, and ``GEMINI.md``).

    Args:
        destination: Workspace root directory to inspect (defaults to current directory).

    Returns:
        list[str]: Canonical names of detected AI coding agents in deterministic order.
    """
    root = Path(destination).expanduser().resolve()
    detected: list[str] = []

    if (root / ".agents").is_dir() or (root / ".agent").is_dir():
        detected.append("antigravity")
    if (root / ".claude").is_dir() or (root / "CLAUDE.md").is_file() or (root / "CLAUDE.local.md").is_file():
        detected.append("claude")
    if (root / ".cursor").is_dir() or (root / ".cursorrules").is_file():
        detected.append("cursor")
    if (root / ".github" / "instructions").is_dir() or (root / ".github" / "copilot-instructions.md").is_file():
        detected.append("copilot")
    if (root / ".windsurf").is_dir() or (root / ".windsurfrules").is_file():
        detected.append("windsurf")
    if (root / ".clinerules").is_dir():
        detected.append("cline")
    if (root / ".roo").is_dir() or (root / ".roorules").is_file():
        detected.append("roo")
    if (root / ".codex").is_dir() or (root / "AGENTS.md").is_file():
        detected.append("codex")
    if (root / "GEMINI.md").is_file():
        detected.append("gemini")

    return detected


def get_agent_instruction(
    agent: str,
    mode: AgentTriggerMode = "auto",
    global_scope: bool = False,
) -> str:
    """Render the complete instruction file content for a specific AI coding agent.

    Args:
        agent: Agent target name or alias (e.g. 'antigravity', 'claude', 'cursor', 'copilot').
        mode: Activation mode for frontmatter-capable agents ('auto' or 'always').
        global_scope: Whether formatting is for the global user configuration target.

    Returns:
        str: Formatted Markdown or MDC content including any required YAML frontmatter.

    Raises:
        ValueError: If agent name or mode is invalid.
    """
    canonical = _normalize_agent_name(agent)
    validated_mode = _normalize_mode(mode)
    body = _load_base_agent_instruction()
    frontmatter = _build_frontmatter(canonical=canonical, mode=validated_mode, global_scope=global_scope)
    return f"{frontmatter}{body}\n"


def _expand_agent_targets(agent: str | Sequence[str]) -> list[str]:
    """Parse, expand 'all' and comma-separated items, and deduplicate agent targets."""
    raw_items: list[str] = [agent] if isinstance(agent, str) else list(agent)
    tokens: list[str] = []
    for raw in raw_items:
        for part in raw.split(","):
            stripped = part.strip()
            if stripped:
                tokens.append(stripped)

    if not tokens:
        raise ValueError("At least one AI agent target must be specified.")

    expanded: list[str] = []
    for token in tokens:
        if token.lower() == "all":
            for mod_name in ALL_MODULAR_AGENTS:
                if mod_name not in expanded:
                    expanded.append(mod_name)
        else:
            canonical = _normalize_agent_name(token)
            if canonical not in expanded:
                expanded.append(canonical)
    return expanded


def _resolve_agent_output_path(
    spec: AgentTargetSpec,
    dest_dir: Path,
    global_scope: bool,
    output_path: str | Path | None,
) -> Path:
    """Resolve destination filesystem path for a single agent instruction target."""
    if output_path is not None:
        return Path(output_path).expanduser().resolve()

    if global_scope:
        if spec.global_rel_path is None:
            raise ValueError(
                f"Global instruction file is not supported for '{spec.name}' "
                f"(managed via {spec.label} IDE/account settings). Omit --global or pass -o <path>."
            )
        return (Path.home() / spec.global_rel_path).resolve()

    if spec.name == "antigravity":
        if (dest_dir / ".agents").exists():
            return dest_dir / ".agents" / "rules" / "drawlib.md"
        if (dest_dir / ".agent").exists():
            return dest_dir / ".agent" / "rules" / "drawlib.md"
        return dest_dir / ".agents" / "rules" / "drawlib.md"

    return dest_dir / spec.project_rel_path


def _ensure_parent_directory(target_file: Path) -> None:
    """Ensure parent directory can be created without colliding with an existing regular file."""
    for ancestor in (target_file.parent, *target_file.parent.parents):
        if ancestor.exists() and not ancestor.is_dir():
            raise FileExistsError(
                f"Cannot create directory '{target_file.parent}' because '{ancestor}' already exists as a file."
            )
    target_file.parent.mkdir(parents=True, exist_ok=True)


def _write_marker_merged_file(target_file: Path, body_content: str, force: bool) -> None:
    """Write or non-destructively merge Drawlib instructions inside HTML comment markers."""
    wrapped_block = f"{MARKER_START}\n{body_content.strip()}\n{MARKER_END}"

    if not target_file.exists():
        _ensure_parent_directory(target_file)
        target_file.write_text(f"{wrapped_block}\n", encoding="utf-8")
        return

    if target_file.is_dir():
        raise IsADirectoryError(f"Target path '{target_file}' is a directory, not a file.")

    existing = target_file.read_text(encoding="utf-8")
    has_start = MARKER_START in existing
    has_end = MARKER_END in existing

    if has_start != has_end:
        raise ValueError(
            f"Malformed Drawlib instruction markers found in '{target_file}'. "
            "Remove the partial marker comment and retry."
        )

    if has_start and has_end:
        start_idx = existing.index(MARKER_START)
        end_idx = existing.index(MARKER_END)
        if end_idx < start_idx:
            raise ValueError(f"Reversed Drawlib instruction markers found in '{target_file}'.")
        if not force:
            raise FileExistsError(
                f"Drawlib agent instructions already exist in '{target_file}'. Pass --force (-f) to update."
            )
        updated = existing[:start_idx] + wrapped_block + existing[end_idx + len(MARKER_END) :]
        if not updated.endswith("\n"):
            updated += "\n"
        target_file.write_text(updated, encoding="utf-8")
        return

    if not existing.strip():
        target_file.write_text(f"{wrapped_block}\n", encoding="utf-8")
        return

    merged = f"{existing.rstrip()}\n\n{wrapped_block}\n"
    target_file.write_text(merged, encoding="utf-8")


def _write_dedicated_file(target_file: Path, rendered_content: str, force: bool) -> None:
    """Write a dedicated Drawlib rule file, guarding against accidental overwrite."""
    if target_file.exists():
        if target_file.is_dir():
            raise IsADirectoryError(f"Target path '{target_file}' is a directory, not a file.")
        if not force:
            raise FileExistsError(
                f"Agent instruction file '{target_file}' already exists. Pass --force (-f) to overwrite."
            )

    _ensure_parent_directory(target_file)
    content = rendered_content if rendered_content.endswith("\n") else f"{rendered_content}\n"
    target_file.write_text(content, encoding="utf-8")


def _validate_marker_state(target_file: Path, existing: str, force: bool) -> None:
    """Validate marker-comment state inside an existing shared instruction file."""
    has_start = MARKER_START in existing
    has_end = MARKER_END in existing
    if has_start != has_end:
        raise ValueError(
            f"Malformed Drawlib instruction markers found in '{target_file}'. "
            "Remove the partial marker comment and retry."
        )
    if has_start and has_end:
        if existing.index(MARKER_END) < existing.index(MARKER_START):
            raise ValueError(f"Reversed Drawlib instruction markers found in '{target_file}'.")
        if not force:
            raise FileExistsError(
                f"Drawlib agent instructions already exist in '{target_file}'. Pass --force (-f) to update."
            )


def _validate_target_file_plan(target_file: Path, use_markers: bool, force: bool) -> None:
    """Dry-check filesystem collisions and overwrite guards before writing any files."""
    if target_file.exists() and target_file.is_dir():
        raise IsADirectoryError(f"Target path '{target_file}' is a directory, not a file.")

    for ancestor in (target_file.parent, *target_file.parent.parents):
        if ancestor.exists() and not ancestor.is_dir():
            raise FileExistsError(
                f"Cannot create directory '{target_file.parent}' because '{ancestor}' already exists as a file."
            )

    if not use_markers and target_file.exists() and not force:
        raise FileExistsError(
            f"Agent instruction file '{target_file}' already exists. Pass --force (-f) to overwrite."
        )

    if use_markers and target_file.is_file():
        _validate_marker_state(target_file, target_file.read_text(encoding="utf-8"), force=force)


def init_agent_instruction(
    agent: str | Sequence[str],
    destination: str | Path = ".",
    mode: AgentTriggerMode = "auto",
    global_scope: bool = False,
    output_path: str | Path | None = None,
    force: bool = False,
) -> list[Path]:
    """Generate AI coding agent instruction file(s) for one or more targets.

    Creates tool-idiomatic rule files (with YAML/MDC frontmatter where required) for
    dedicated modular directories (``.agents/rules/``, ``.claude/rules/``,
    ``.cursor/rules/``, ``.github/instructions/``, ``.windsurf/rules/``,
    ``.clinerules/``, ``.roo/rules/``), or non-destructively merges a marker-delimited
    section into shared files (``AGENTS.md``, ``GEMINI.md``).

    Args:
        agent: Target agent name, comma-separated names, sequence of names, or 'all'.
        destination: Workspace root directory for project-scoped output (defaults to '.').
        mode: Trigger mode for frontmatter-capable agents ('auto' [default] or 'always').
        global_scope: If True, write to user's home global agent rules path instead of workspace.
        output_path: Explicit output file path override (valid only for a single agent target).
        force: If True, overwrite existing dedicated files or update existing marker blocks.

    Returns:
        list[Path]: Resolved paths of created or updated instruction files.

    Raises:
        ValueError: If agent target, mode, global_scope, or multi-target output_path is invalid.
        FileExistsError: If target file (or marker block) already exists and force is False.
    """
    validated_mode = _normalize_mode(mode)
    targets = _expand_agent_targets(agent)

    if output_path is not None and len(targets) > 1:
        raise ValueError("Cannot specify --output (-o) when initializing multiple AI agent targets.")

    dest_dir = Path(destination).expanduser().resolve()

    plan: list[tuple[Path, str, bool]] = []
    for canonical in targets:
        spec = AGENT_TARGET_SPECS[canonical]
        target_file = _resolve_agent_output_path(
            spec=spec,
            dest_dir=dest_dir,
            global_scope=global_scope,
            output_path=output_path,
        )
        use_markers = spec.merge_global_markers if global_scope else spec.merge_project_markers
        rendered = get_agent_instruction(canonical, mode=validated_mode, global_scope=global_scope)
        _validate_target_file_plan(target_file=target_file, use_markers=use_markers, force=force)
        plan.append((target_file, rendered, use_markers))

    written_paths: list[Path] = []
    for target_file, rendered, use_markers in plan:
        if use_markers:
            _write_marker_merged_file(target_file=target_file, body_content=rendered, force=force)
        else:
            _write_dedicated_file(target_file=target_file, rendered_content=rendered, force=force)
        written_paths.append(target_file)

    return written_paths
