
from askcode.analyzer import analyze_python_file


def test_analyze_python_file_extracts_structure(tmp_path):
    source = """\
class ArticleService:
    def find_all(self):
        pass

    async def create(self):
        pass


def normalize_title(title):
    return title.strip()
"""

    file_path = tmp_path / "article_service.py"
    file_path.write_text(source, encoding="utf-8")

    result = analyze_python_file(file_path)

    assert result["language"] == "python"
    assert result["classes"][0]["name"] == "ArticleService"
    assert result["classes"][0]["methods"] == [
        {"name": "find_all", "line": 2},
        {"name": "create", "line": 5},
    ]
    assert result["functions"] == [
        {"name": "normalize_title", "line": 9}
    ]


def test_analyze_empty_python_file(tmp_path):
    file_path = tmp_path / "empty.py"
    file_path.write_text("", encoding="utf-8")

    result = analyze_python_file(file_path)

    assert result["classes"] == []
    assert result["functions"] == []
