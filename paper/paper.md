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

`FACET2-S2E` is a Python package for start-to-end simulations of the Facility for Advanced Accelerator Experimental Tests-II (FACET-II) [@yakimenko:2019], a US Department of Energy National User Facility. A kilometer-long particle accelerator creates, manipulates, and accelerates electron beams to over 10 GeV before focusing and compressing them to the micron-scale. These beams create extreme electric and magnetic fields on the femtosecond timescale, uniquely enabling research into exotic states and advanced accelerator technology, including plasma wakefield acceleration. This software package enables present or prospective facility users to easily run the most common types of simulation pipelines to design experiments and interpret results.


# Statement of need

`FACET2-S2E` is a Python package which contains utilities, analysis notebooks, and configuration files used to perform start-to-end (S2E) simulations of the FACET-II particle accelerator beamline, a facility which hosts hundreds of external users a year. The core workflow uses `IMPACT-T` [@qiang:2006] for beam generation and low energy transport, `Bmad`, `Tao`, and `PyTao` [@Sagan:Bmad2006] for most of the beam transport through the kilometer-long linear accelerator, and, optionally, `QPAD` [@li2021quasi] for particle-in-cell simulations of the beam in plasma, and `openPMD-beamphysics` [@christopher_mayes_2025_15477845] for handling beam files. 

Users can quickly and easily run the most common types of simulations including parameter scans, constrained optimization of both Twiss and multiparticle tracking objectives, and jitter sensitivity analysis. The package seamlessly chains together multiple codes, provides reference configurations, offers convenience functions which mimic real-world feedback systems, and offers templates for common development and optimization tasks, so beam physicists can focus on the physics.

The package translates between the language and units of the underlying codes and the real-world EPICS [@dalesio1991epics] control system. This package is readily integrated into control room tools, both importing real values into simulations and using the simulation optimizers to write new values to the machine. It also abstracts away details (e.g. specific magnet values) instead allowing users to focus on specifying desired higher-level goals (e.g. beam qualities).

Other software packages exist which simulate different parts of a beamline, for example `GPT` [@de1996general] and `IMPACT` [@qiang:2006] for low energy portions; `elegant` [@borland2000elegant] and  `Bmad` [@Sagan:Bmad2006] for higher energy regions; or `HiPACE++` [@diederichs2022hipace] and `QPAD` [@li2021quasi] for particle-in-cell beam-plasma interactions. These are general purpose codes which allow the design of arbitrary beamlines but their learning curves are commensurately steep. Further, they have different domains, requiring handoffs of the beam between codes. In contrast, `FACET2-S2E` is a bespoke package which models, using several underlying codes, a single beamline which is thoughtfully compartmentalized and abstracted, making it as frictionless as possible for members of the FACET-II user community to perform beamline simulations.

While under development, this package has been used to support various experiments including those published as [@PhysRevLett.134.085001] and [@zhang2025]



# Acknowledgements

This work was supported by the U.S. Department of Energy under DOE Contract No. DEAC02-76SF00515. The authors thank M. Ehrlichman and C. Mayes for sharing their Bmad expertise and D. Cesar for his floorplan plotting function.

# References
