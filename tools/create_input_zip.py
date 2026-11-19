#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAMES = (
    "active_satellites.csv",
    "satcat.csv",
    "DEN-CO2scaling2000-2500_v2.nc",
    "indices_maio2024_v8.csv"
)


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default=str(ROOT / "data"))
    parser.add_argument("--output", default="satellite_inputs.zip")
    args = parser.parse_args()
    base = Path(args.data_dir).expanduser().resolve()
    manifest = json.loads((ROOT / "input_manifest.json").read_text("ascii"))
    for filename in NAMES:
        path = base / filename
        if not path.is_file():
            parser.error("Missing input: " + str(path))
        metadata = manifest["files"].get(filename)
        if metadata and sha256(path) != metadata["sha256"]:
            parser.error("Input SHA-256 mismatch: " + filename)
    output = Path(args.output).expanduser().resolve()
    if output.is_relative_to(base):
        parser.error("Keep the input archive outside the data directory.")
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for filename in NAMES:
            z.write(base / filename, arcname=filename)
    print("Source archive:", output)
    print("Size (MB):", round(output.stat().st_size / 1024**2, 2))
    print("Do not upload this archive to a public repository without review.")

if __name__ == "__main__":
    main()
