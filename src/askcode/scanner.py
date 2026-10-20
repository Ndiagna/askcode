from pathlib import Path

SUPPORTED_EXTENSIONS = {".py", ".php"}

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "vendor",
    "node_modules",
    "__pycache__",
    "cache",
}


def scan_repository(repository_path: str) -> list[Path]:
    """Find supported source files in a repository."""
    root = Path(repository_path).resolve()

    if not root.exists():
        raise FileNotFoundError(
            f"Repository does not exist: {root}"
        )

    if not root.is_dir():
        raise NotADirectoryError(
            f"Repository path is not a directory: {root}"
        )

    source_files = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        relative_path = path.relative_to(root)
        parts = relative_path.parts

        if any(
            part in IGNORED_DIRECTORIES
            for part in parts[:-1]
        ):
            continue

        if parts[:3] == ("storage", "framework", "views"):
            continue

        if path.suffix.lower() in SUPPORTED_EXTENSIONS:
            source_files.append(path)

    return sorted(source_files)
