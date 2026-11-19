#!/usr/bin/env python3
import ast
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "SatelitesRevisao_GitHub.ipynb"

def main():
    problems = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix not in {".py", ".ipynb", ".md", ".txt", ".json"} and path.name not in {".gitignore", ".gitattributes", ".python-version"}:
            continue
        raw = path.read_bytes()
        if any(byte > 127 for byte in raw):
            problems.append(f"Non-ASCII bytes: {path.relative_to(ROOT)}")
        if b"\r" in raw or b"\x00" in raw:
            problems.append(f"CR or NUL bytes: {path.relative_to(ROOT)}")
        try:
            raw.decode("ascii")
        except UnicodeDecodeError:
            problems.append(f"Not ASCII text: {path.relative_to(ROOT)}")
    nb = json.loads(NOTEBOOK.read_text(encoding="ascii"))
    if nb.get("nbformat") != 4:
        problems.append("Unexpected notebook format")
    if any(k not in {"language_info", "kernelspec"} for k in nb.get("metadata", {})):
        problems.append("Unexpected notebook metadata")
    code_count = 0
    for i, cell in enumerate(nb["cells"], 1):
        if cell.get("metadata"):
            problems.append(f"Cell {i}: extra metadata")
        if cell["cell_type"] == "code":
            code_count += 1
            if cell.get("execution_count") is not None or cell.get("outputs"):
                problems.append(f"Cell {i}: stored execution data")
            try:
                ast.parse("".join(cell["source"]))
            except SyntaxError as exc:
                problems.append(f"Cell {i}: syntax error: {exc}")
    first_code = next(("".join(c["source"]) for c in nb["cells"]
                       if c["cell_type"] == "code"), "")
    if '"pymsis": "0.12.0"' not in first_code or 'subprocess.check_call' not in first_code:
        problems.append("Missing dependency installation cell")
    code_cells = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
    if len(code_cells) < 2 or "Upload satellite_inputs.zip" not in code_cells[1]:
        problems.append("Missing portable input setup")
    if any("drive.mount(" in src or "/content/drive" in src for src in code_cells):
        problems.append("Notebook contains a Google Drive dependency")
    if code_count != 25:
        problems.append(f"Unexpected number of code cells: {code_count}")
    try:
        import nbformat
        nbformat.validate(nbformat.read(str(NOTEBOOK), as_version=4))
    except ImportError:
        print("nbformat not installed; JSON and Python syntax still checked")
    except Exception as exc:
        problems.append(f"Notebook schema validation: {exc}")
    if problems:
        print("STATIC AUDIT FAILED")
        for item in problems:
            print(item)
        return 1
    print(f"STATIC AUDIT OK: {code_count} Python cells; ASCII only; no stored outputs")
    return 0

if __name__ == "__main__":
    sys.exit(main())
