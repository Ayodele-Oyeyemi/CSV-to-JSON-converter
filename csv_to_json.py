#!/usr/bin/env python3
"""
csv_to_json.py

A simple CLI tool to convert CSV files into JSON.

Supports:
  - Custom delimiters (comma, semicolon, tab, etc.)
  - Pretty-printed or compact JSON output
  - Optional type inference (numbers/booleans/null instead of plain strings)
  - Batch conversion of every CSV file in a folder
  - Writing to a file or printing to stdout

Usage examples:
  # Convert a single CSV to JSON, printed to the terminal
  python csv_to_json.py data.csv

  # Convert and save to a file
  python csv_to_json.py data.csv --output data.json

  # Use a semicolon-delimited CSV
  python csv_to_json.py data.csv --delimiter ";"

  # Infer types (numbers, booleans, null) instead of keeping everything as strings
  python csv_to_json.py data.csv --infer-types

  # Compact output instead of pretty-printed
  python csv_to_json.py data.csv --compact

  # Convert every .csv file in a folder
  python csv_to_json.py ./data_folder --batch --output-dir ./json_output
"""

import argparse
import csv
import json
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert CSV file(s) to JSON."
    )
    parser.add_argument(
        "input",
        type=str,
        help="Path to a CSV file, or a directory when using --batch",
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Path to write the output JSON file (default: print to stdout)",
    )
    parser.add_argument(
        "--output-dir", type=str, default=None,
        help="Directory to write JSON files to when using --batch (default: same folder as input)",
    )
    parser.add_argument(
        "--delimiter", type=str, default=",",
        help="CSV delimiter character (default: ',')",
    )
    parser.add_argument(
        "--infer-types", action="store_true",
        help="Convert numeric/boolean/null-looking strings into their real JSON types",
    )
    parser.add_argument(
        "--compact", action="store_true",
        help="Output compact JSON instead of pretty-printed (indent=2)",
    )
    parser.add_argument(
        "--batch", action="store_true",
        help="Treat 'input' as a directory and convert every .csv file inside it",
    )
    return parser.parse_args()


def infer_value(value: str):
    """Attempt to convert a CSV string value into a more specific JSON type."""
    if value == "":
        return None

    lowered = value.strip().lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in ("null", "none", "n/a", "na"):
        return None

    # Try integer first, then float
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass

    return value


def csv_to_json_data(csv_path: Path, delimiter: str, infer_types: bool):
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        rows = []
        for row in reader:
            if infer_types:
                row = {key: infer_value(value) for key, value in row.items()}
            rows.append(row)
    return rows


def write_output(data, output_path: Path, compact: bool):
    indent = None if compact else 2
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
        f.write("\n")


def convert_single_file(input_path: Path, args) -> Path:
    if not input_path.is_file():
        print(f"Error: '{input_path}' is not a valid file.")
        sys.exit(1)

    data = csv_to_json_data(input_path, args.delimiter, args.infer_types)

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix(".json")

    return data, output_path


def main():
    args = parse_args()
    input_path = Path(args.input).expanduser().resolve()

    if args.batch:
        if not input_path.is_dir():
            print(f"Error: '{input_path}' is not a valid directory.")
            sys.exit(1)

        csv_files = sorted(input_path.glob("*.csv"))
        if not csv_files:
            print("No .csv files found in the given directory.")
            return

        output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else input_path
        output_dir.mkdir(parents=True, exist_ok=True)

        for csv_file in csv_files:
            data = csv_to_json_data(csv_file, args.delimiter, args.infer_types)
            output_path = output_dir / (csv_file.stem + ".json")
            write_output(data, output_path, args.compact)
            print(f"Converted: {csv_file.name} -> {output_path}")

        print(f"\nDone. {len(csv_files)} file(s) converted.")
        return

    # Single file mode
    if not input_path.is_file():
        print(f"Error: '{input_path}' is not a valid file.")
        sys.exit(1)

    data = csv_to_json_data(input_path, args.delimiter, args.infer_types)

    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        write_output(data, output_path, args.compact)
        print(f"Converted: {input_path.name} -> {output_path}")
    else:
        indent = None if args.compact else 2
        print(json.dumps(data, indent=indent, ensure_ascii=False))


if __name__ == "__main__":
    main()
