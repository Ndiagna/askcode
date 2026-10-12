
from collections import Counter
from pathlib import Path


def summarize_files(files: list[Path]) -> dict[str, int]:
    """Count source files by extension."""
    counts = Counter(
        path.suffix.lower()
        for path in files
    )

    return dict(sorted(counts.items()))
