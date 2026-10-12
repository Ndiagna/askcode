
from pathlib import Path

from askcode.stats import summarize_files


def test_summarize_files_counts_extensions():
    files = [
        Path("app.py"),
        Path("test.py"),
        Path("Controller.php"),
    ]

    result = summarize_files(files)

    assert result == {
        ".php": 1,
        ".py": 2,
    }


def test_summarize_files_returns_empty_dict_for_no_files():
    assert summarize_files([]) == {}
