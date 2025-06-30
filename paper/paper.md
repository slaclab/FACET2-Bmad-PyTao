---
# Example from https://joss.readthedocs.io/en/latest/submitting.html
title: 'ConFluxPro: A toolkit for soil gas analysis'
tags:
  - R
  - soil gas
  - flux-gradient method
  - flux
authors:
  - name: Valentin Gartiser
    orcid: 0000-0001-5320-374X
    affiliation: "1, 2" # (Multiple affiliations must be quoted)
  - name: Verena Lang
    orcid: 0000-0002-5316-2746
    affiliation: 1
  - name: Martin Maier
    orcid: 0000-0002-7959-0108
    affiliation: 2
affiliations:
 - name: Forest Research Institute, Freiburg, Germany
   index: 1
 - name: Soil Physics, Department of Crop Sciences, Göttingen, Germany
   index: 2
citation_author: Gartiser et al.
date: 05 November 2024
year: 2024
bibliography: paper.bib
output: rticles::joss_article
csl: apa.csl
journal: JOSS
---



# Summary
``ConFluxPro`` is an R-package to model soil gas fluxes with the flux-gradient method (FGM).
The FGM is a cost-effective way to measure fluxes and production rates of gases in soils [@Maier2014].
It relies on the principle that gas exchange in soils is driven by molecular diffusion and can therefore be described by Fick's first law of diffusion.
In situ, it requires measuring vertical concentration profiles of soil gases and parameters to estimate the diffusivity of the soil.
Flux rates can then be modeled by deriving concentration gradients and diffusion coefficients of soil gases.

We developed ``ConFluxPro`` to assist along the entire modeling process, from data handling and preparation to flux modeling and beyond.
The package (I) provides object classes for the preparation, combination and modification of soil gas and physical data, (II) implements different common FGM models, (III) introduces an inverse modeling approach, (IV) provides functions for post-hoc calibration and (V) uncertainty estimation of the model results.
All this functionality was built to be modular and user-friendly on the outside with robust internals handling more complex data manipulations.
This makes it easy to implement an individual approach to the FGM, while improving the reproducibility of the analysis.

# Statement of need

The FGM is conceptually simple and has been applied in numerous studies.
However, codes or evaluation files have often not been shared publicly and there are differences between individual implementations.
For example, concentration gradients may be calculated using a linear regression [@Tang2003], simple differences between depths [@Jong1972] or by fitting exponential functions [@Davidson2006].
While there may be valid reasons to favour one approach over another within any study, this makes it hard to compare results between studies. 
Furthermore, the uncertainty of the approach due to soil heterogeneity and measurement uncertainty is often not considered.
Still, the FGM is uniquely equipped to address questions on subsurface processes and for long-term measurement [@Maier2020].
The goal of ``ConFluxPro`` was to make the FGM easy to implement, flexible and reproducible.

A first challenge in applying the FGM is to combine the various input parameters needed for the flux calculation.
These may be from different sources (online measurement or soil samples), be of different types (volumetric or point measurements) and have different spatial and temporal resolutions. 
For this reason, ``ConFluxPro`` first implements different functions and object classes to shape the data into a predictable frame.
Once the data is unified in this way, all subsequent operations can be mostly handled internally.
This limits the need for user intervention, both making it easier to implement and reducing an important source of error in the analysis.

Apart from the commonly used approaches, ``ConFluxPro`` also comes with an inverse model to estimate profiles of gas production rates similar to @SchackKirchner2011.
Instead of deriving concentration gradients from the measurements, the model calculates a concentration profile form assumed production (or consumption) rates.
This profile is then fit to the measurements by algorithmically optimizing the production rates. 
The advantage of the inverse model is that the entire profile is consistently described by functions derived from physical laws.
While this approach is conceptually more advanced, it is as easy to use within the package.

Soil heterogeneity and measurement error introduces uncertainty in FGM models.
This is addressed in ``ConFluxPro`` in two ways.
First, we implemented a calibration approach to reduce the differences between modeled and reference flux rates (e.g. from chamber measurements).
Second, a bootstrapping approach gives an estimate of the model uncertainty introduced from the variability of the input parameters.

``ConFluxPro`` is a versatile toolkit to model soil gas fluxes with the FGM.
During development, we have already used it in multiple studies [@Maier2020; @Jochheim2022]. 
The scientific background of the methods is described in @Gartiser2025.
By sharing this package we hope to make it easier to implement the FGM in future studies, furthering our knowledge of important soil processes.

# Related software

To our knowledge, there is currently no other comprehensive implementation of the FGM.
An approach in `Python` is described in @Bittelli2015.
The package [``neonSoilFlux``](https://github.com/jmzobitz/neonSoilFlux) [@Zobitz2024] implements the FGM specificly to the National Ecological Observatory Network (NEON).
There are multiple R-packages to help with the analysis of chamber measurement data, 
[``gasfluxes``](https://git-dmz.thuenen.de/fuss/gasfluxes) [@Fuss2016], [``goFlux``](https://github.com/Qepanna/goFlux) [@Rheault2024] and [``FluxCalR``](https://github.com/junbinzhao/FluxCalR) [@Zhao2019].

# Funding

This work was funded in part by the WKF (Waldklimafond/Forest Climate Fund) and the FNR (Fachagentur Nachwachsende Rohstoffe e.V.), jointly managed by the Federal Ministry for the Environment (BMU) and the Federal Ministry of Food and Agriculture (BMEL)—grant number 2218WK58X4.

# References

