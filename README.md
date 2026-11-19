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

The four required inputs consist of three third-party datasets and one frozen historical space-weather index table. The file `data/indices_maio2024_v8.csv` is publicly available in this repository.

The original CelesTrak orbital data and SATCAT snapshots are not redistributed here. The WACCM-X thermospheric density scaling dataset can be obtained from the University of Birmingham (DOI: 10.25500/edata.bham.00001075).

The archived input checksums are documented in `input_manifest.json`. Current CelesTrak downloads may differ from the historical snapshots used in the study, and therefore may not reproduce the exact numerical results.

To reproduce the archived results, obtain the identical files; their archived
SHA-256 fingerprints are listed in `input_manifest.json`. The 2024 three-hour
geomagnetic index file
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

The author confirmed a CelesTrak download/access date of 2025-10-21 from
local download history. This is consistent with the orbital epochs in
`active_satellites.csv` (September to early October 2025), but it cannot be
the extraction date of the current `satcat.csv` archive: that file includes
launches and decays dated through 2026-10-30. The date 2026-10-31 is a
provisional SATCAT cutoff assumed in the study, NOT a verified extraction
date. See `AUDITORIA_CODIGO.md`.

The Random Forest discriminates cataloged decays in a random stratified test
but its probabilities are not well calibrated, and transfer to a different
satellite population is weaker. The test split is not prospective validation.

NRLMSIS 2.0 and WACCM-X density variations are separate analyses, not orbital
propagation or time-to-reentry simulations. The 2024 storm median at 550 km
using the archived 24-time by 15-location sample is 80.426869 percent;
this differs from the previous aggregate-only analysis.

## Data availability and provenance

The four archived input files used for the independent run on 2026-11-19
are not publicly redistributed in this repository. A frozen input archive
(`satellite_inputs.zip`, approximately 3.4 MB) is retained separately for
potential confidential peer review, subject to editorial arrangements and
applicable third-party redistribution conditions. No personal Google Drive
access is required to execute the notebook once the input archive is obtained.

- **`active_satellites.csv`**: Orbital element snapshot obtained from
  [CelesTrak](https://celestrak.org/). The author confirmed an access/download
  date of **2025-10-21** using local browser download history. The archived
  orbital epochs range from 2025-09-11 to 2025-10-04; the epoch of an orbital
  element set is not necessarily its download date.
- **`satcat.csv`**: Satellite Catalog (SATCAT) snapshot obtained from
  [CelesTrak](https://celestrak.org/). The archived file contains launches
  and decays dated through **2026-10-30**, so it cannot be the same
  2025-10-21 snapshot. Its exact download date remains unverified. The
  **2026-10-31** SATCAT cutoff in the computational archive is provisional,
  not documented as the actual acquisition date. A current CelesTrak download
  is not an identical substitute for this frozen file.
- **`DEN-CO2scaling2000-2500_v2.nc`**: Thermospheric density scaling factors
  from the WACCM-X research dataset published via the University of
  Birmingham's research data archive
  ([DOI: 10.25500/edata.bham.00001075](https://doi.org/10.25500/edata.bham.00001075)).
  The archived SHA-256 is recorded in `input_manifest.json`. The source
  record provides open download access but does not specify a redistribution
  license; permission to republish this dataset is being clarified.
- **`indices_maio2024_v8.csv`**: A study-specific, frozen 24-record table of
  historical solar F10.7/F10.7a and geomagnetic Ap inputs used for the
  May 10-12, 2024 NRLMSIS 2.0 analysis. The exact primary-source attribution
  and preparation history still require documentation. This file is not
  currently included in the public repository. Archived SHA-256:
  `31860b6ea963f7d57c7d7cecd27771899c23491cc1afff4b49af8f113c926605`.

To reproduce the *archived* numerical results, use the same four snapshots
and verify their checksums. For local execution, place them in `data/` as
specified above. In Google Colab, supply a ZIP containing the four files
when prompted by the notebook. Downloading up-to-date CelesTrak files
will not reproduce an identical historical snapshot.

A software license has not yet been assigned in this repository. Any
future license for the original software will not extend to third-party
input datasets.

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
