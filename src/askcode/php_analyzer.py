
import json
import subprocess
from pathlib import Path


def analyze_php_file(file_path: Path) -> dict:
    """Analyze a PHP file using PHP-Parser."""
    project_root = Path(__file__).resolve().parents[2]
    php_script = project_root / "php-parser" / "analyze.php"

    result = subprocess.run(
        ["php", str(php_script), str(file_path)],
        capture_output=True,
        text=True,
        check=True,
    )

    return json.loads(result.stdout)
