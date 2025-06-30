---
title: 'FACET-S2E: Start-to-end simulations of the FACET-II beamline'
tags:
  - accelerator physics
  - plasma physics
  - python
authors:
  - name: Nathan Majernik
    corresponding: true
    orcid: 0000-0001-9977-0248
    affiliation: 1
  - name: Eric Cropp
    orcid: 0000-0000-0000-0000
    affiliation: 1
  - name: Claudio Emma
    orcid: 0000-0000-0000-0000
    affiliation: 1
  - name: Thamine Dalichaouch
    orcid: 0000-0000-0000-0000
    affiliation: 2             
affiliations:
 - name: SLAC National Accelerator Laboratory, USA
   index: 1
 - name: University of California, Los Angeles, USA
   index: 2
date: 30 June 2025
bibliography: paper.bib
csl: apa.csl
journal: JOSS
---




# Summary

`FACET2-S2E` is a Python package for start-to-end simulations of the Facility for Advanced Accelerator Experimental Tests-II (FACET-II) [cite website and “FACET-II facility for advanced accelerator experimental tests”], a US Department of Energy National User Facility. A kilometer-long particle accelerator creates, manipulates, and accelerates electron beams to over 10 GeV before focusing and compressing them to the micron-scale. These beams create extreme electric and magnetic fields on the femtosecond timescale, uniquely enabling research into exotic states and advanced accelerator technology, including plasma wakefield acceleration. This software package enables present or prospective facility users to quickly and easily run the most common types of simulations to design experiments and interpret results.


# Statement of need

`FACET2-S2E` is a Python package which contains utilities, Jupyter notebooks, and configuration files used to perform start-to-end (S2E) simulations of the FACET-II particle accelerator beamline, a facility which hosts hundreds of external users a year. The core workflow uses IMPACT-T [cite] for beam generation and low energy transport, Bmad, Tao, and PyTao [cite] for most of the beam transport through the kilometer-long linear accelerator, and, optionally, QPAD [cite] for particle-in-cell simulations of the beam in plasma, and openPMD-beamphysics [cite] for handling beam files. 

Present or prospective facility users can quickly and easily run the most common types of simulations including parameter scans, constrained optimization of both Twiss and multiparticle tracking objectives, and jitter sensitivity analysis, since `FACET2-S2E` abstracts away unnecessary detail. The package seamlessly chains together multiple codes, provides reference configurations, and offers templates for common development and optimization tasks, so beam physicists can focus on the physics.

The package translates between the language and units of the underlying codes and the real-world EPICS [cite] control system. This package is readily integrated into control room tools, both importing real values into simulations and using the simulation optimizers to write new values to the machine. It also abstracts away details (e.g. specific magnet values) instead allowing users to focus on specifying desired higher-level goals (e.g. beam qualities).

While under development, this package has been used to support various experiments including those published as [Experimental generation of extreme electron beams for advanced accelerator applications] and [Plasma-Wakefield Accelerator Simultaneously Boosts Electron Beam Energy and Brightness]


# Acknowledgements

This work was supported by the U.S. Department of Energy under DOE Contract No. DEAC02-76SF00515. The authors thank M. Ehrlichman and C. Mayes for sharing their Bmad expertise and D. Cesar for his floorplan plotting function.

# References

