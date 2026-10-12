
from askcode.report import generate_report


def test_generate_report_returns_file_statistics(tmp_path):
    (tmp_path / "app.py").write_text(
        "print('hello')",
        encoding="utf-8",
    )
    (tmp_path / "Controller.php").write_text(
        "<?php",
        encoding="utf-8",
    )

    report = generate_report(str(tmp_path))

    assert report["total_files"] == 2
    assert report["files_by_extension"] == {
        ".php": 1,
        ".py": 1,
    }
    assert "app.py" in report["files"]
    assert "Controller.php" in report["files"]
