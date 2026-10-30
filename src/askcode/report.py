
from pathlib import Path

from askcode.analyzer import analyze_python_file
from askcode.php_analyzer import analyze_php_file
from askcode.scanner import scan_repository
from askcode.stats import summarize_files


def generate_report(repository_path: str) -> dict:
    """Generate a repository report with source code analysis."""
    root = Path(repository_path).resolve()

    files = scan_repository(repository_path)
    counts = summarize_files(files)

    python_analysis = []
    php_analysis = []

    for path in files:
        if path.suffix.lower() == ".py":
            python_analysis.append(analyze_python_file(path))
        elif path.suffix.lower() == ".php":
            php_analysis.append(analyze_php_file(path))

    return {
        "repository": str(root),
        "total_files": len(files),
        "files_by_extension": counts,
        "files": [
            str(path.relative_to(root))
            for path in files
        ],
        "python_analysis": python_analysis,
        "php_analysis": php_analysis,
    }
