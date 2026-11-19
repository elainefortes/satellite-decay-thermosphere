# Input data and reproducibility

The frozen historical solar and geomagnetic index table `indices_maio2024_v8.csv` is provided in this directory.

Three additional inputs are required to reproduce the archived analyses:

- `active_satellites.csv`: orbital data from CelesTrak (https://celestrak.org/).
- `satcat.csv`: satellite catalog data from CelesTrak (https://celestrak.org/).
- `DEN-CO2scaling2000-2500_v2.nc`: WACCM-X dataset from the University of Birmingham (https://doi.org/10.25500/edata.bham.00001075).

These third-party datasets are not redistributed in this repository. Their provenance and archived checksums are documented in the main README and `input_manifest.json`.

For local execution, place the three additional input files in this directory. For Google Colab, the notebook currently requires a locally prepared `satellite_inputs.zip` containing all four inputs. This ZIP is not intended for public redistribution.

Exact numerical reproduction requires the original archived dataset versions. Newly downloaded CelesTrak files may differ from those used in the study.                                                                                 
