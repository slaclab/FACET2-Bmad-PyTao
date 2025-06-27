# FACET-II (start-to-end) S2E Simulation Toolkit

This repository contains utilities, Jupyter notebooks, and configuration files used to perform start-to-end (S2E) simulations of the [FACET-II](https://facet-ii.slac.stanford.edu/) particle accelerator beamline, a US Department of Energy National National User Facility which hosts hundreds of users a year.  The core workflow uses [IMPACT-T](https://github.com/impact-lbl/IMPACT-T) for beam generation and low energy transport, [Bmad, Tao, and PyTao](https://www.classe.cornell.edu/bmad/) for most of the beam transport through the kilometer-long linear accelerator, and, optionally, [QPAD](https://picksc.physics.ucla.edu/qpad.html) for particle-in-cell simulations of the beam in plasma, and [openPMD-beamphysics](https://github.com/ChristopherMayes/openPMD-beamphysics) for handling beam files. It is intended to abstract away unnecessary detail so facility users can quickly and easily run the most common types of simulations including parameter scans, constrained optimization of both Twiss and multi-particle tracking objectives, and jitter sensitivity analysis.


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

## Examples

The notebooks in the repository demonstrate typical workflows:

* **`S3DF demo notebook.ipynb`** – runs a short Bmad simulation with a reference lattice and beam file.  It also introduces the helper functions for adjusting magnet and linac settings.
* **`S3DF demo notebook - with IMPACT.ipynb`** – performs a full S2E run that generates the input beam with IMPACT‑T before tracking it through the lattice.

Launch Jupyter, open one of these notebooks and run all cells to verify the installation.

## Repository layout

```
ARCHIVE/                 Historical studies, optimizations, and experimental notebooks
beams/                   Reference beams and scripts to generate them
bmad/                    Bmad 'golden lattice' (https://github.com/slaclab/facet2-lattice)
impact/                  IMPACT‑T configuration files
other_configs/           Atypical configurations including misalignment and steering solutions
setLattice_configs/      Reference lattices
UTILITY_*.py             Helper functions
bmadCondaEnv.yml         Conda environment specification
```


## Features

Loading `UTILITY_quickstart.py` will import all the utility functions. These functions take many forms

### Core functions

- `initializeTao()` – set up a Bmad/PyTao instance. Optionally run IMPACT‑T to create a beam.
- `setLattice()` – apply lattice configuration to commonly changed knobs using a dictionary or reference file
- `trackBeam()` – track a beam between arbitrary points in the lattice, applying specialized functions like centering or energy correction at checkpoints.

### Other features

- `UTILITY_setLattice` functions to translate between the language and units of the FACET-II EPICS control system and simulation
- `UTILITY_linacPhaseAndAmplitude` which conveniently phase and set the gradients of the linacs
- Plotting tools for displaying both beams and the beamline itself
- Twiss optimizers for the final focus and golden lattice matching
- Infrastructure for dealing with two-bunch operation
- Various options of calculating spot sizes and emittances
- Tools to model laser heater interactions
- Mathematica notebooks which track and analyze optimizer progress
- Mathematica notebooks which visualize beam files, including as 3D animations

## Notes on large files

Git LFS is required because beam files can be tens of megabytes.  Without LFS you may see errors such as:

```
OSError: Unable to synchronously open file (file signature not found)
```

If you cannot use LFS, manually download the `.h5` beam files from another source and place them in the appropriate directories.

## Further documentation

Most development work happens inside the notebooks.  The notebooks in the `ARCHIVE` folder track previous investigations and may serve as additional examples.
