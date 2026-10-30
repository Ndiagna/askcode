
import ast
from pathlib import Path


def analyze_python_file(file_path: Path) -> dict:
    """Extract classes, methods and top-level functions."""
    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(file_path))

    classes = []

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            methods = [
                {
                    "name": child.name,
                    "line": child.lineno,
                }
                for child in node.body
                if isinstance(
                    child,
                    (ast.FunctionDef, ast.AsyncFunctionDef),
                )
            ]

            classes.append({
                "name": node.name,
                "line": node.lineno,
                "methods": methods,
            })

    functions = [
        {
            "name": node.name,
            "line": node.lineno,
        }
        for node in tree.body
        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        )
    ]

    return {
        "file": str(file_path),
        "language": "python",
        "classes": classes,
        "functions": functions,
    }
