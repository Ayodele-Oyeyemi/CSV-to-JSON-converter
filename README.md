# CSV to JSON Converter

A simple, dependency-free Python CLI tool that converts CSV files into JSON.

No third-party libraries required — just Python's standard library.

## Features

- ✅ Convert a single CSV file to JSON
- ✅ Batch-convert every CSV file in a folder
- ✅ Custom delimiters (comma, semicolon, tab, etc.)
- ✅ Optional type inference — turn `"42"` into `42`, `"true"` into `true`, empty strings into `null`
- ✅ Pretty-printed or compact JSON output
- ✅ Write to a file, or print straight to the terminal

## Requirements

- Python 3.7+
- No external dependencies

## Usage

```bash
python csv_to_json.py <input> [options]
```

### Options

| Flag              | Description                                                        |
|-------------------|---------------------------------------------------------------------|
| `--output`        | Path to write the output JSON file (default: print to stdout)       |
| `--output-dir`    | Directory to write JSON files to when using `--batch`               |
| `--delimiter`     | CSV delimiter character (default: `,`)                              |
| `--infer-types`   | Convert numeric/boolean/empty values into real JSON types           |
| `--compact`       | Output compact JSON instead of pretty-printed                       |
| `--batch`         | Treat `input` as a directory and convert every `.csv` file inside it |

### Examples

**Convert a single CSV, printed to the terminal:**
```bash
python csv_to_json.py data.csv
```

**Convert and save to a file:**
```bash
python csv_to_json.py data.csv --output data.json
```

**Use a semicolon-delimited CSV:**
```bash
python csv_to_json.py data.csv --delimiter ";"
```

**Infer types instead of keeping everything as strings:**
```bash
python csv_to_json.py data.csv --infer-types
```
```
# Input CSV:
name,age,active
Ada,30,true

# Output JSON with --infer-types:
[
  { "name": "Ada", "age": 30, "active": true }
]

# Output JSON without --infer-types (default):
[
  { "name": "Ada", "age": "30", "active": "true" }
]
```

**Compact output:**
```bash
python csv_to_json.py data.csv --compact
```

**Convert every CSV in a folder:**
```bash
python csv_to_json.py ./data_folder --batch --output-dir ./json_output
```

## How it works

Each CSV row becomes one JSON object, using the header row as keys. The whole
file is converted into a single JSON array of these objects.

## Safety notes

- With `--infer-types`, watch out for values you *want* kept as strings that
  look numeric (e.g. zip codes, phone numbers, IDs with leading zeros) —
  they'll be converted to numbers and lose leading zeros. Skip `--infer-types`
  for that kind of data.
- The tool reads CSVs as UTF-8. If your file uses a different encoding,
  convert it to UTF-8 first.

## Running tests

```bash
python -m unittest discover tests
```