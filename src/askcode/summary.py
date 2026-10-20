
from pathlib import Path


def summarize_analysis(report: dict) -> dict:
    """Create a compact summary of a repository analysis."""
    analyses = (
        report.get("python_analysis", [])
        + report.get("php_analysis", [])
    )

    classes = []
    total_methods = 0
    total_functions = 0

    for analysis in analyses:
        total_functions += len(analysis.get("functions", []))

        for class_info in analysis.get("classes", []):
            methods = class_info.get("methods", [])
            total_methods += len(methods)

            file_path = Path(analysis["file"])
            repository_path = Path(report["repository"])

            try:
                relative_path = str(
                    file_path.relative_to(repository_path)
                )
            except ValueError:
                relative_path = str(file_path)

            classes.append({
                "name": class_info.get("name") or "(anonymous class)",
                "file": relative_path,
                "line": class_info["line"],
                "methods_count": len(methods),
            })

    return {
        "repository": report["repository"],
        "total_files": report["total_files"],
        "files_by_extension": report["files_by_extension"],
        "total_classes": len(classes),
        "total_methods": total_methods,
        "total_functions": total_functions,
        "classes": classes[:10],
        "additional_classes": max(0, len(classes) - 10),
    }
