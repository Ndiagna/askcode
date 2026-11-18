from askcode.php_analyzer import analyze_php_file


def test_analyze_php_file_extracts_class_and_methods(tmp_path):
    php_file = tmp_path / "Article.php"
    php_file.write_text(
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

    result = analyze_php_file(php_file)

    assert result["language"] == "php"
    assert result["classes"][0]["name"] == "Article"
    assert len(result["classes"][0]["methods"]) > 0
