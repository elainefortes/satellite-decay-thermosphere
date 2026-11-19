# Independent execution verification - 19 November 2026

This report documents the user-run Google Colab execution of the portable
`SatelitesRevisao_GitHub.ipynb` using a locally uploaded `satellite_inputs.zip`.
The notebook did not require a Google Drive mount. The resulting output archive
was independently inspected after execution.

## Audit outcome

- Audit checks: 26 total; 25 OK; 0 FAIL; 1 PENDING.
- Files inventoried by the generated manifest: 44.
- Manifest integrity: all 44 reported file sizes and SHA-256 values verified.
- Original orbit records: 12,810; eligible decay cohort: 12,806.
- Observed cataloged decays within 180 days: 403.
- Held-out Random Forest: 3,202 objects; 101 decay events.
- Average Precision recomputed from the saved predictions: 0.7752287801324917.
- ROC AUC recomputed from the saved predictions: 0.9349299651022825.
- Brier Score recomputed from the saved predictions: 0.0221496337981816.
- NRLMSIS fixed-case density increase at 400 km: 36.761372 percent.
- May 2024 550-km storm median increase: 80.426869 percent.
- WACCM-X SSP2-4.5 2100 density-factor reduction at 550 km: 30.811302 percent.
- WACCM-X SSP5-8.5 2100 remains unavailable; no extrapolation.

## Input identities reported by the audit

- TLE SHA-256: b4b3e88a9ffcfd15e793bd1eda7ec4570fc056b1249ca6c758dc5ce65e303f48
- SATCAT SHA-256: 4a79c9b205c72c699d40db2053b617396499787769ac619c5f2da6ab3bd0c960
- WACCM-X SHA-256: fe7cc40f4fe7fb40f13ba7c509fb53daaa018c18744f3863131ba61090dbe93f

## Outstanding limitations

The SATCAT extraction date (assumed 2026-10-31) remains unverified, and is
recorded as PENDING. The published source package does not contain the four
archived source datasets; readers must obtain the same source snapshots.
The SHA-256 of the *original* frozen May 2024 index CSV has not yet been
independently established; the normalized output CSV must not be misrepresented
as byte-identical to the original input.

The storm median differs from the previous aggregate-only result. This does
not fail the versioned regression check, but it should be acknowledged and
reconciled with any manuscript table using the earlier estimate.

This is computational reproducibility of a fixed archived analysis, not
external validation, time-based prospective validation, or proof of the
physical meaning of cataloged decay labels.

Source: `resultados_execucao_independente.zip`, Colab execution on
2026-11-19; recorded audit timestamp 2026-11-19T05:31:19Z.
The full generated results archive is retained separately, not bundled in
this GitHub source-only release.
