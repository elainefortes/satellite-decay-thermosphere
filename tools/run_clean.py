#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description="Run the archived satellite analysis.")
    parser.add_argument("--data-dir", default=str(ROOT / "data"))
    parser.add_argument("--timeout", type=int, default=3600)
    args = parser.parse_args()
    data_dir = Path(args.data_dir).expanduser().resolve()

    validation = subprocess.run([
        sys.executable,
        str(ROOT / "tools" / "check_inputs.py"),
        "--data-dir",
        str(data_dir)
    ], check=False)
    if validation.returncode != 0:
        print("Input verification failed. Notebook was not executed.")
        return 1

    import nbformat
    from nbclient import NotebookClient

    source = ROOT / "SatelitesRevisao_GitHub.ipynb"
    output_dir = ROOT / "results"
    output_dir.mkdir(exist_ok=True)
    output = output_dir / "SatelitesRevisao_executado.ipynb"
    notebook = nbformat.read(source, as_version=4)
    os.environ["SATELLITE_DATA_DIR"] = str(data_dir)
    client = NotebookClient(
        notebook,
        timeout=args.timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(ROOT)}}
    )

    try:
        client.execute()
    except Exception as exc:
        nbformat.write(notebook, output)
        print(f"Execution failed; partial run saved to {output}")
        print(type(exc).__name__, exc)
        return 1

    nbformat.write(notebook, output)
    print(f"Execution completed: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
