# Satellite decay screening and thermospheric density analysis

This research notebook reproduces the archived statistical and physical
experiments in the revised Journal of the Brazilian Computer Society study.
It does not require access to the author's Google Drive.

## Notebook and inputs

Notebook: `SatelitesRevisao_GitHub.ipynb`

Four required inputs (original archived snapshots):

- `active_satellites.csv`
- `satcat.csv`
- `DEN-CO2scaling2000-2500_v2.nc`
- `indices_maio2024_v8.csv`

The inputs are NOT distributed in this repository. To reproduce the archived
results, obtain the identical files; their archived SHA-256 fingerprints are
listed in `input_manifest.json`. The 2024 three-hour geomagnetic index file
must contain 24 rows with UTC date, F107, F107a and seven Ap values. It must
not be replaced by a later download without documenting the new snapshot.

### Option A: Google Colab, without Google Drive

1. Obtain the four archived input files.
2. Create `satellite_inputs.zip` containing those four named files. This is a
   local archive; do not upload it to GitHub without checking redistribution
   permissions and dataset provenance.
3. Open the notebook in Colab and choose Runtime > Run all.
4. When the input cell asks, upload `satellite_inputs.zip`.
5. The notebook reads `/content/data` and writes to `/content/results`.
   These directories are temporary and disappear when the Colab runtime ends.
   Download the results before closing the runtime.

The optional script `tools/create_input_zip.py` prepares the archive from a
local folder containing all four files. If those files currently live in your
personal Drive, you can create the ZIP ONCE in the original Colab session,
download it locally, then use the ZIP in an independent runtime.

### Option B: Local machine

Requires Python 3.13. Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Copy the four source files into `data/` or use `tools/create_input_zip.py`
then extract the resulting ZIP into `data/`.

```bash
python tools/check_release.py
python tools/check_inputs.py --data-dir data
python tools/run_clean.py --data-dir data --timeout 3600
```

To use a different source directory, set `SATELLITE_DATA_DIR` before executing.
To save results elsewhere, set `SATELLITE_RESULTS_DIR`. The notebook never
mounts Google Drive automatically.

## Validation

The portable notebook was executed end to end on 2026-11-19 in Google
Colab using a locally uploaded input ZIP, without mounting Google Drive.
Its generated archive was subsequently checked: 25 audit checks passed,
zero failed, and one SATCAT provenance check remains pending. All 44 files
in the output manifest passed independent size and SHA-256 verification.
The saved held-out RF predictions reproduced AP=0.7752287801,
AUC=0.9349299651 and Brier=0.0221496338.
See `VALIDACAO_EXECUCAO_INDEPENDENTE.md` for evidence and limitations.

The date 2026-10-31 is an assumed SATCAT cutoff used for the archived result.
It is NOT a verified SATCAT extraction date. See `AUDITORIA_CODIGO.md`.

The Random Forest discriminates cataloged decays in a random stratified test
but its probabilities are not well calibrated, and transfer to a different
satellite population is weaker. The test split is not prospective validation.

NRLMSIS 2.0 and WACCM-X density variations are separate analyses, not orbital
propagation or time-to-reentry simulations. The 2024 storm median at 550 km
using the archived 24-time by 15-location sample is 80.426869 percent;
this differs from the previous aggregate-only analysis.

## Project files

- `requirements.txt`: scientific dependencies.
- `input_manifest.json`: archived source identities.
- `tools/check_release.py`: notebook structural and ASCII checks.
- `tools/check_inputs.py`: input SHA-256 and geomagnetic CSV checks.
- `tools/create_input_zip.py`: local source archive preparation.
- `tools/run_clean.py`: notebook execution in a clean kernel.
- `AUDITORIA_CODIGO.md`: scientific and technical limitations.
- `VALIDACAO_EXECUCAO_INDEPENDENTE.md`: successful portable run and checks.
- `data/README.md`: data handling instructions.

No change to an external GitHub repository is performed by these files.
