import argparse
import json

from askcode.report import generate_report
from askcode.search import search_symbols


def main():
    parser = argparse.ArgumentParser(
        description="AskCode - Understand your codebase"
    )

    parser.add_argument(
        "command",
        choices=["search"],
        help="Command to execute",
    )

    parser.add_argument(
        "repository",
        help="Path to the repository",
    )

    parser.add_argument(
        "query",
        help="Symbol to search for",
    )

    args = parser.parse_args()

    if args.command == "search":
        report = generate_report(args.repository)
        results = search_symbols(report, args.query)

        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()