
from askcode.summary import summarize_analysis


def test_summarize_analysis_counts_classes_methods_and_functions():
    report = {
        "repository": "/project",
        "total_files": 2,
        "files_by_extension": {".php": 1, ".py": 1},
        "python_analysis": [
            {
                "file": "/project/app.py",
                "functions": [{"name": "main", "line": 1}],
                "classes": [],
            }
        ],
        "php_analysis": [
            {
                "file": "/project/Article.php",
                "functions": [],
                "classes": [
                    {
                        "name": "Article",
                        "line": 3,
                        "methods": [
                            {"name": "title", "line": 5}
                        ],
                    }
                ],
            }
        ],
    }

    summary = summarize_analysis(report)

    assert summary["total_files"] == 2
    assert summary["total_classes"] == 1
    assert summary["total_methods"] == 1
    assert summary["total_functions"] == 1
    assert summary["classes"][0]["name"] == "Article"
    assert summary["classes"][0]["file"] == "Article.php"
