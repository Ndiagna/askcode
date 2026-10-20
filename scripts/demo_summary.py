
import json
import sys

from askcode.report import generate_report
from askcode.summary import summarize_analysis


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python scripts/demo_summary.py <repository_path>")
        raise SystemExit(1)

    report = generate_report(sys.argv[1])
    summary = summarize_analysis(report)

    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
