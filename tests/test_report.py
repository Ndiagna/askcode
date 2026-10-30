
from askcode.report import generate_report


def test_generate_report_returns_file_statistics(tmp_path):
    (tmp_path / "article.php").write_text(
        "<?php\n",
        encoding="utf-8",
    )

    report = generate_report(str(tmp_path))

    assert report["total_files"] == 1
    assert report["files_by_extension"] == {".php": 1}
    assert report["files"] == ["article.php"]


def test_generate_report_includes_python_analysis(tmp_path):
    (tmp_path / "article.py").write_text(
        "def normalize_title(title):\n"
        "    return title.strip()\n",
        encoding="utf-8",
    )

    report = generate_report(str(tmp_path))

    assert len(report["python_analysis"]) == 1
    assert report["python_analysis"][0]["functions"] == [
        {"name": "normalize_title", "line": 1}
    ]


def test_generate_report_includes_php_analysis(tmp_path):
    (tmp_path / "Article.php").write_text(
        "<?php\n"
        "class Article\n"
        "{\n"
        "    public function title(): string\n"
        "    {\n"
        "        return 'Example';\n"
        "    }\n"
        "}\n",
        encoding="utf-8",
    )

    report = generate_report(str(tmp_path))

    assert len(report["php_analysis"]) == 1

    analysis = report["php_analysis"][0]

    assert analysis["language"] == "php"
    assert analysis["classes"][0]["name"] == "Article"
    assert analysis["classes"][0]["methods"][0]["name"] == "title"
