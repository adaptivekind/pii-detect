#!/usr/bin/env python3
"""
PII Detection CLI using Microsoft Presidio
Detects personally identifiable information in text files or directories
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from detector import PIIDetector


def print_results(results: List[Dict[str, Any]], output_format: str = "text"):
    """Print results in specified format"""
    if output_format == "json":
        print(json.dumps(results, indent=2))
        return

    # Text format
    total_files = len(results)
    files_with_pii = sum(1 for r in results if r.get("pii_found", False))
    total_pii_entities = sum(r.get("pii_count", 0) for r in results)

    print("\n=== PII Detection Results ===")
    print(f"Files analyzed: {total_files}")
    print(f"Files with PII: {files_with_pii}")
    print(f"Total PII entities found: {total_pii_entities}")
    print("=" * 30)

    for result in results:
        if result.get("error"):
            print(f"\n❌ ERROR in {result['file']}: {result['error']}")
            continue

        if result.get("pii_found", False):
            print(f"\n🔍 {result['file']} - {result['pii_count']} PII entities found: ")
            for entity in result["entities"]:
                print(
                    f"  • {entity['entity_type']}: '{entity['text']}' "
                    f"(confidence: {entity['score']: .2f})"
                )
        else:
            print(f"\n✅ {result['file']} - No PII detected")


def main():
    parser = argparse.ArgumentParser(
        description="Detect PII in text files using Microsoft Presidio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s file.txt                    # Analyze single file
  %(prog)s /path/to/directory          # Analyze all text files in directory
  %(prog)s -f json file.txt            # Output results as JSON
  %(prog)s -e .py -e .js directory/    # Only analyze .py and .js files
        """,
    )

    parser.add_argument("path", help="Path to file or directory to analyze")

    parser.add_argument(
        "-f",
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    parser.add_argument(
        "-e",
        "--extensions",
        action="append",
        help="File extensions to analyze (can be used multiple times)",
    )

    args = parser.parse_args()

    # Validate path
    path = Path(args.path)
    if not path.exists():
        print(f"Error: Path '{args.path}' does not exist")
        sys.exit(1)

    # Initialize detector
    detector = PIIDetector()

    # Analyze based on path type
    if path.is_file():
        result = detector.analyze_file(path)
        results = [result]
    elif path.is_dir():
        results = detector.analyze_directory(path, args.extensions)
    else:
        print(f"Error: '{args.path}' is not a file or directory")
        sys.exit(1)

    # Print results
    print_results(results, args.format)


if __name__ == "__main__":
    main()
