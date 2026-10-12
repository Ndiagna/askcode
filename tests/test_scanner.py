
from askcode.scanner import scan_repository


def test_scan_finds_python_and_php_files(tmp_path):
    (tmp_path / "main.py").write_text(
        "print('hello')",
        encoding="utf-8",
    )
    (tmp_path / "Controller.php").write_text(
        "<?php",
        encoding="utf-8",
    )
    (tmp_path / "notes.txt").write_text(
        "Not source code",
        encoding="utf-8",
    )

    files = scan_repository(str(tmp_path))

    assert [path.name for path in files] == [
        "Controller.php",
        "main.py",
    ]


def test_scan_ignores_vendor_directory(tmp_path):
    vendor = tmp_path / "vendor"
    vendor.mkdir()
    (vendor / "dependency.php").write_text(
        "<?php",
        encoding="utf-8",
    )
    (tmp_path / "app.php").write_text(
        "<?php",
        encoding="utf-8",
    )

    files = scan_repository(str(tmp_path))

    assert [path.name for path in files] == ["app.php"]

def test_scan_ignores_cache_directory(tmp_path):
    cache = tmp_path / "bootstrap" / "cache"
    cache.mkdir(parents=True)

    (cache / "generated.php").write_text(
        "<?php",
        encoding="utf-8",
    )
    (tmp_path / "app.php").write_text(
        "<?php",
        encoding="utf-8",
    )

    files = scan_repository(str(tmp_path))

    assert [path.name for path in files] == ["app.php"]