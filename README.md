# FACET-II start-to-end (S2E) simulation toolkit

This repository contains utilities, Jupyter notebooks, and configuration files used to perform start-to-end (S2E) simulations of the [FACET-II](https://facet-ii.slac.stanford.edu/) particle accelerator beamline, a US Department of Energy National National User Facility which hosts hundreds of users a year.  The core workflow uses [IMPACT-T](https://github.com/impact-lbl/IMPACT-T) for beam generation and low energy transport, [Bmad, Tao, and PyTao](https://www.classe.cornell.edu/bmad/) for most of the beam transport through the kilometer-long linear accelerator, and, optionally, [QPAD](https://picksc.physics.ucla.edu/qpad.html) for particle-in-cell simulations of the beam in plasma, and [openPMD-beamphysics](https://github.com/ChristopherMayes/openPMD-beamphysics) for handling beam files. It is intended to abstract away unnecessary detail so present or prospective facility users can quickly and easily run the most common types of simulations including parameter scans, constrained optimization of both Twiss and multiparticle tracking objectives, and jitter sensitivity analysis.


## Installation


1. **Clone with Git LFS**
   ```bash
   git clone https://github.com/slaclab/FACET2-S2E.git
   cd FACET2-S2E
   git lfs pull
   ```
   Many beam files are tracked with Git LFS.  Without LFS the notebooks will fail to load example beams.

2. **Create the conda environment**
   ```bash
   conda env create -f bmadCondaEnv.yml
   conda activate bmad
   ```
   Alternatively, directly install key packages:
   ```bash
   conda install jupyter numpy matplotlib pandas
   conda install -c conda-forge bmad pytao openpmd-beamphysics distgen lume-base lume-impact bayesian-optimization
   ```

## Examples

The notebooks in the repository demonstrate typical workflows:

* **`Example - Basic introduction.ipynb`** – runs Bmad simulations with a reference lattice and beam file.  It also introduces some basic functionality like reading and setting magnets using control system units, phasing linacs, etc.
* **`Example - IMPACT-T beam generation.ipynb`** – performs a full S2E run that generates the input beam with IMPACT‑T before tracking it through the lattice to the end of the beamline
* **`Example - Final focus tuning.ipynb`** – demonstrates the final focus optics optimizer to pick magnet settings to achieve desired Twiss
* **`Example - Multiparticle tracking optimization.ipynb`** – demonstrates optimization constrained by real-world hardware limits of a multiparticle tracked beam
* **`Example - Solution postprocessing and analysis.ipynb`** – postprocessing and analysis of the beam throughout the lattice
* **`Example - Beam visualization.nb`** – Mathematica notebook for advanced beam visualization and analysis, including 3D animation generation
* **`Example - Optimization progress dashboard.nb`** – Mathematica companion notebook which visualizes optimization progress, e.g. parameter sensitivities and convergence
* **`Example - Jitter study.py`** – Parallel computation of many simulations with parameters subject to jitter, informed by real-world measurements
* 

### Tests

When run, "Example" notebooks should reproduce the figures and results of the notebooks in the repo, up to random error resulting from RNG subsampling

## Repository layout

```
ARCHIVE/                 Historical studies, optimizations, and experimental notebooks
beams/                   Reference beams and scripts to generate them
bmad/                    Bmad 'golden lattice' (https://github.com/slaclab/facet2-lattice)
impact/                  IMPACT‑T configuration files
other_configs/           Atypical configurations including misalignment and steering solutions
setLattice_configs/      Reference configurations
UTILITY_*.py             Utility functions
bmadCondaEnv.yml         Conda environment specification
```


## Features

Loading `UTILITY_quickstart.py` will import all the utility functions. These functions take many forms

### Core functions

- `initializeTao()` – set up a Bmad/PyTao instance. Optionally run IMPACT‑T to create a beam or import a reference beam
- `setLattice()` – apply lattice configuration to commonly changed knobs using a dictionary or reference file
- `trackBeam()` – track a beam between arbitrary points in the lattice, applying specialized functions like centering or energy correction at checkpoints

### Other features

- `UTILITY_setLattice` functions to translate between the language and units of the FACET-II EPICS control system and simulation
- `UTILITY_linacPhaseAndAmplitude` which conveniently phases and sets the gradients of the linacs
- Plotting tools for displaying beams and the beamline itself
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

Most development work happens inside the notebooks.  The notebooks in the `ARCHIVE` folder are previous investigations and may serve as additional examples.


## Support

For support, contact @majernik-slac-stanford-edu
