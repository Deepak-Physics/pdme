# pdme - the python dipole model evaluator

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-green.svg?style=flat-square)](https://conventionalcommits.org)
[![PyPI](https://img.shields.io/pypi/v/pdme?style=flat-square)](https://pypi.org/project/pdme/)
![Maintenance](https://img.shields.io/maintenance/yes/2024?style=flat-square)

This library includes a variety of utility functions for calculating charge noise in qubits from TLSs for the purposes of Bayesian analysis.
This was a major part of my PhD thesis on characterizing charge noise.
New code here should be mostly low-level numpy calculations or common types that can be shared elsewhere.

## Related libraries

Other libraries us include:
- [deepdog](https://gitea.deepak.science/physics/deepdog): performs Monte Carlo simulations with two underlying algorithm options for direct MC and subset simulation
- [kalpaa](https://gitea.deepak.science/physics/kalpa): high level wrapper for pdme, deepdog and tantri, implementing retry logic, data transformation and summarising. the place to start to actually run analyses
- [tantri](https://gitea.deepak.science/physics/tantri): generates mock telegraph noise and utility functions for binning and transforming measured or simulated power spectral densities (PSDs)
- [dreader](https://gitea.deepak.science/physics/dreader): utility library for parsing output files

## Getting started

`poetry install` to start locally

Commit using [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), and when commits are on master, release with `doo release`.
