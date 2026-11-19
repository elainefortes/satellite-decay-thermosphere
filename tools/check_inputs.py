#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "input_manifest.json").read_text())


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default=str(ROOT / "data"))
    args = parser.parse_args()
    root = Path(args.data_dir).expanduser().resolve()
    failed = False
    for filename, info in MANIFEST["files"].items():
        files = list(root.rglob(filename))
        if len(files) != 1:
            print(f"FAIL: Expected one {filename}; found {len(files)}")
            failed = True
            continue
        actual = sha256(files[0])
        correct = actual == info["sha256"]
        print(f"{'OK' if correct else 'FAIL'}: {filename}: {actual}")
        failed |= not correct
    indices = list(root.rglob("indices_maio2024_v8.csv"))
    if len(indices) != 1:
        print("FAIL: Frozen 2024 space-weather CSV is missing or ambiguous")
        failed = True
    else:
        import csv
        with indices[0].open(newline="") as f:
            rows = list(csv.DictReader(f))
        cols = {"data_utc", "f107", "f107a"} | {f"ap_{i}" for i in range(7)}
        good = len(rows) == 24 and all(cols.issubset(row) for row in rows)
        print(f"{'OK' if good else 'FAIL'}: indices_maio2024_v8.csv: {len(rows)} rows; sha256={sha256(indices[0])}")
        failed |= not good
    print("SATCAT extraction date remains UNVERIFIED until documented separately")
    return int(failed)

if __name__ == "__main__":
    sys.exit(main())
