def search_symbols(report: dict, query: str) -> list[dict]:
    """Search for classes, methods and functions."""
    results = []
    query = query.lower()

    analyses = (
        report.get("python_analysis", [])
        + report.get("php_analysis", [])
    )

    for analysis in analyses:
        file_path = analysis["file"]

        for class_info in analysis.get("classes", []):
            class_name = class_info.get("name") or ""

            if query in class_name.lower():
                results.append({
                    "type": "class",
                    "name": class_name,
                    "file": file_path,
                    "line": class_info["line"],
                })

            for method in class_info.get("methods", []):
                if query in method["name"].lower():
                    results.append({
                        "type": "method",
                        "name": method["name"],
                        "class": class_name,
                        "file": file_path,
                        "line": method["line"],
                    })

        for function in analysis.get("functions", []):
            if query in function["name"].lower():
                results.append({
                    "type": "function",
                    "name": function["name"],
                    "file": file_path,
                    "line": function["line"],
                })

    return results