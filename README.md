# Typical installation 

Start by setting up a Conda environment using bmadCondaEnv.yml (https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

Try executing "S3DF demo notebook.ipynb"; this should, using only a few lines, perform and plot an output from a Bmad simulation from a pre-generated lattice and beam file. It will also demonstrate some of the helper functions for changing magnet and linac settings.

"S3DF demo notebook - with IMPACT.ipynb" will demonstrate a start-to-end simulation which uses IMPACT-T for the beam generation

# Additional notes

## Git LFS

This repo uses Git LFS. Strongly recommend installing it: https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage

Alternative is to manually download the requisite large files (namely .h5 beam files). Otherwise you'll get errors like

```
/opt/conda/lib/python3.12/site-packages/pmd_beamphysics/particles.py:681: SyntaxWarning: invalid escape sequence '\l'
  """
---------------------------------------------------------------------------
OSError                                   Traceback (most recent call last)
Cell In[2], line 1
----> 1 tao = initializeTao(
      2     inputBeamFilePathSuffix = '/beams/nmmToL0AFEND_2bunch_2024-02-16Clean/2024-02-16_2bunch_1e5Downsample_nudgeWeights_driverOnly_2023-05-16InjectorMatch.h5'
      3 )

...

File h5py/h5f.pyx:102, in h5py.h5f.open()

OSError: Unable to synchronously open file (file signature not found)
```

## Other Conda hints

If the Conda environment files don't work, try:

`conda install jupyter numpy matplotlib pandas`

`conda install -c conda-forge bmad pytao openpmd-beamphysics distgen lume-base lume-impact bayesian-optimization`

But from here, you'll just need to try running things and seeing if you can play whack-a-mole with the errors
