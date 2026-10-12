
from pathlib import Path

from askcode.scanner import scan_repository
from askcode.stats import summarize_files


def generate_report(repository_path: str) -> dict:
    """Generate a basic repository report."""
    files = scan_repository(repository_path)
    counts = summarize_files(files)

    return {
        "repository": str(Path(repository_path).resolve()),
        "total_files": len(files),
        "files_by_extension": counts,
        "files": [
            str(path.relative_to(Path(repository_path).resolve()))
            for path in files
        ],
    }
