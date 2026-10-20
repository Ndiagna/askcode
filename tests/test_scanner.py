
from askcode.scanner import scan_repository


def test_scan_finds_python_and_php_files(tmp_path):
    (tmp_path / "main.py").write_text(
        "print('hello')",
        encoding="utf-8",
    )
    (tmp_path / "Article.php").write_text(
        "<?php",
        encoding="utf-8",
    )
    (tmp_path / "readme.txt").write_text(
        "Documentation",
        encoding="utf-8",
    )

    files = scan_repository(str(tmp_path))

    assert {path.name for path in files} == {
        "main.py",
        "Article.php",
    }


def test_scan_ignores_vendor_directory(tmp_path):
    vendor = tmp_path / "vendor"
    vendor.mkdir()
    (vendor / "dependency.php").write_text(
        "<?php",
        encoding="utf-8",
    )
    (tmp_path / "main.php").write_text(
        "<?php",
        encoding="utf-8",
    )

    files = scan_repository(str(tmp_path))

    assert [path.name for path in files] == ["main.php"]


def test_scan_ignores_cache_directory(tmp_path):
    cache = tmp_path / "cache"
    cache.mkdir()
    (cache / "generated.php").write_text(
        "<?php",
        encoding="utf-8",
    )
    (tmp_path / "main.php").write_text(
        "<?php",
        encoding="utf-8",
    )

    files = scan_repository(str(tmp_path))

    assert [path.name for path in files] == ["main.php"]


def test_scan_ignores_compiled_blade_views(tmp_path):
    compiled_views = (
        tmp_path / "storage" / "framework" / "views"
    )
    compiled_views.mkdir(parents=True)
    (compiled_views / "compiled.php").write_text(
        "<?php",
        encoding="utf-8",
    )

    source_views = tmp_path / "resources" / "views"
    source_views.mkdir(parents=True)
    (source_views / "article.php").write_text(
        "<?php",
        encoding="utf-8",
    )

    files = scan_repository(str(tmp_path))

    relative_paths = {
        path.relative_to(tmp_path).as_posix()
        for path in files
    }

    assert "resources/views/article.php" in relative_paths
    assert "storage/framework/views/compiled.php" not in relative_paths
