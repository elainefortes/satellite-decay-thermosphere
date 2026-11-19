# Satellite decay screening and thermospheric density analysis

Research code for the revised Journal of the Brazilian Computer Society manuscript.
The notebook contains observational decay screening, a perigee baseline, Random
Forest evaluation, K-Means, Isolation Forest, NRLMSIS 2.0 and WACCM-X experiments.

## Status

This is a cleaned, source-checked publication candidate. The dependency setup
was corrected after the missing-pymsis error observed in a fresh Colab runtime.
A full clean-run test
has not been performed on this package. The original notebook was run previously
in Colab with 21 passing numerical checks, but that does not validate the exact
exported version. Do not describe the release as independently reproduced yet.

## Files

- `SatelitesRevisao_GitHub.ipynb`: source notebook with outputs cleared.
- `requirements.txt`: versions recorded for the scientific components.
- `input_manifest.json`: expected SHA-256 fingerprints of input sources.
- `tools/check_release.py`: static syntax, encoding and metadata checks.
- `tools/check_inputs.py`: source fingerprint and frozen Ap-index checks.
- `AUDITORIA_CODIGO.md`: audit findings and remaining limitations.
- `.gitignore`: prevents accidental publication of large inputs and outputs.

## Environment

The prior Colab run used Python 3.13.18. Create a fresh Python 3.13 environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python tools/check_release.py
```

On Google Colab, the first code cell installs missing or mismatched scientific
packages, including `pymsis==0.12.0`, without requiring `requirements.txt` to
be uploaded separately. Execute the notebook from the top. If a library was
already loaded and needs replacement, restart the runtime, then run all cells.
Do not skip the environment-setup cell. The bootstrap is also suitable for a
standalone notebook uploaded to Colab. In a local environment, installing
`requirements.txt` before running is still recommended. When a different
version of Colab is used, record the full resolved environment
(`python -m pip freeze > installed-versions.txt`) after validation.
Do not commit `installed-versions.txt` without reviewing it.

## Required input files

The source datasets were not bundled. The following must exist:

- `data/active_satellites.csv`: archived TLE snapshot, 12,810 objects.
- `data/satcat.csv`: archived SATCAT snapshot.
- `data/DEN-CO2scaling2000-2500_v2.nc`: WACCM-X factors, version 2.
- `data/indices_maio2024_v8.csv`: frozen space-weather indices for May 2024,
  24 rows with UTC date, F107, F107a and seven Ap components.

The first three data files are checked against SHA-256 fingerprints in the
notebook and `input_manifest.json`. The Ap indices must be copied from the
archived Colab audit (`revisao_jbcs_2026/auditoria_v8/indices_maio2024_v8.csv`).
They are mandatory in the release. There is no silent new CelesTrak download.

To run locally, place all four inputs inside `data/` then run:

```bash
python tools/check_inputs.py --data-dir data
python tools/run_clean.py --data-dir data --timeout 3600
```

The clean-run tool executes a fresh notebook kernel, writes the executed
notebook into `results/` and returns an error code if any cell fails. Results
are not committed by default. The static check does not replace a clean run.

To run in Colab, copy the data into `/content/drive/MyDrive/Aeroespacial/`,
including `indices_maio2024_v8.csv`, or set `SATELLITE_DATA_DIR` to the folder
holding the input files. With a custom directory set, mounting Drive is skipped.
The WACCM-X file can also be stored in a subdirectory of the selected input root.

The notebook writes results to a separate `revisao_jbcs_2026/reexecucao_publica`
folder under the input directory, not to the original `auditoria_v8` folder.
Input datasets may be subject to redistribution requirements. Verify relevant
terms and attribution before making them public.

## Observation window

A SATCAT snapshot cutoff of 2026-10-31 is used only to reproduce the archived
calculation. This is not a documented extraction date. Until the provenance of
the original SATCAT file is established, the 180-day non-event assignments are
conditional and the notebook reports a PENDING provenance check. The date must
not be presented as independently verified. `SATCAT_CUTOFF_DATE` changes the
assumed cutoff, and any resulting changes in the sample must be documented.

## Physical and statistical interpretation

- The outcome is cataloged decay, not necessarily uncontrolled atmospheric
  reentry or predicted ground impact.
- A random stratified holdout is not temporal validation. The calibrated
  probability interpretation is not supported by the present Random Forest.
- Cross-population transfer shows degraded generalization.
- K=4 is retained for interpretability, not maximal silhouette.
- Isolation Forest score percentiles are not observed anomaly prevalence.
- NRLMSIS compares atmospheric densities; WACCM-X supplies future relative
  density factors. Neither model is coupled to an orbital propagator here.
- The May 2024 median at 550 km from the frozen 24 x 15 x 6 design was
  80.426869 percent in the archived run. The prior aggregate-only table
  yielded a different median. The cause of this discrepancy remains open.

## Reproducibility and GitHub

Before publication, execute the notebook from the first cell in a new runtime,
check the output audit and figure files, retain the exact four input sources,
and review the README and data license. This code generates three atmospheric
figures; the other manuscript figures are not regenerated by this notebook.

The package does not push, modify, or connect to any GitHub repository.
