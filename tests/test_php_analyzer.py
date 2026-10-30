
from pathlib import Path

from askcode.php_analyzer import analyze_php_file


def test_analyze_php_file_extracts_class_and_methods():
    laravel_file = Path(
        r"C:\laragon\www\cross-origin-newspaper\app\Models\Article.php"
    )

    result = analyze_php_file(laravel_file)

    assert result["language"] == "php"
    assert result["classes"][0]["name"] == "Article"
    assert len(result["classes"][0]["methods"]) > 0
