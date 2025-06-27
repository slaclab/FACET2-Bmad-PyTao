# FACET-II S2E Simulation Toolkit

This repository contains utilities, Jupyter notebooks and configuration files used to perform start-to-end (S2E) simulations of the FACET-II electron beam line.  The workflow relies on the [Bmad](https://www.classe.cornell.edu/bmad/) accelerator physics library together with [IMPACT-T](https://github.com/ChristopherMayes/impact) for initial beam generation.

The project grew out of a collection of notebooks and helper scripts.  Everything needed to launch a simulation, modify lattice settings and analyse the beam is included here.

## Installation

1. **Clone with Git LFS**
   ```bash
   git clone https://<your-fork> FACET2-S2E
   cd FACET2-S2E
   git lfs pull
   ```
   Many beam files are tracked with Git LFS.  Without LFS the notebooks will fail to load example beams.

2. **Create the conda environment**
   ```bash
   conda env create -f bmadCondaEnv.yml
   conda activate bmad
   ```
   If this fails you may manually install the key packages:
   ```bash
   conda install jupyter numpy matplotlib pandas
   conda install -c conda-forge bmad pytao openpmd-beamphysics distgen lume-base lume-impact bayesian-optimization
   ```

## Quick start

The notebooks in the repository demonstrate typical workflows:

* **`S3DF demo notebook.ipynb`** – runs a short Bmad simulation from an existing lattice and beam file.  It also introduces the helper functions for adjusting magnet and linac settings.
* **`S3DF demo notebook - with IMPACT.ipynb`** – performs a full S2E run that generates the input beam with IMPACT‑T before tracking it through the lattice.

Launch Jupyter, open one of these notebooks and run all cells to verify the installation.

## Repository layout

```
ARCHIVE/                 Older studies and experimental notebooks
beams/                   Example beams and scripts to generate them
bmad/                    FACET-II lattice descriptions and conversion tools
impact/                  Supplementary IMPACT‑T configuration files
other_configs/           Steering and misalignment configuration JSON files
setLattice_configs/      Default magnet settings in YAML format
UTILITY_*.py             Helper modules used by the notebooks
bmadCondaEnv.yml         Conda environment specification
```

*The `beams/2024-07-01_Impact_TwoBunch` directory contains a small README describing how one of the reference beams was produced with IMPACT‑T.*

The `bmad/conversion` folder documents how to regenerate the Bmad lattice from SLAC MAD optics files.  See `bmad/conversion/README.md` for the full procedure.

## Helper utilities

The main convenience functions live in `UTILITY_quickstart.py` and related modules:

- `initializeTao()` – set up a Bmad/pytao instance, optionally running IMPACT‑T to create a beam.
- `trackBeam()` – track the active beam through a portion of the lattice with optional energy checks and centring.
- `setLattice()` – apply standard magnet and cavity settings from YAML files.
- `finalFocusSolver()` – optimise the final focus quadrupoles to match desired Twiss parameters.

These modules can also be imported directly in your own analysis scripts.

## Notes on large files

Git LFS is required because beam files can be tens of megabytes.  Without LFS you may see errors such as:

```
OSError: Unable to synchronously open file (file signature not found)
```

If you cannot use LFS, manually download the `.h5` beam files from another source and place them in the appropriate directories.

## Further documentation

Most development work happens inside the notebooks.  The notebooks in the `ARCHIVE` folder track previous investigations and may serve as additional examples.  Feel free to explore them once the environment is working.

## Support

This repository is provided as-is without an official support channel.  The notebooks should serve as both documentation and working examples for running FACET-II S2E simulations.
