import json
import sys

from askcode.report import generate_report


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python scripts/demo_report.py <repository_path>")
        raise SystemExit(1)

    report = generate_report(sys.argv[1])
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()