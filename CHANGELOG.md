# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [1.1.0](https://gitea.deepak.science:2222/physics/pdme/compare/1.0.0...1.1.0) (2024-05-02)


### Features

* adds both electric potential and electric field x sources, makes some fast util tests use the slower explicit versions as double check ([e9e3416](https://gitea.deepak.science:2222/physics/pdme/commit/e9e34162a3b84faad5c18ddeda327c2f7f5ac5aa))

## [1.0.0](https://gitea.deepak.science:2222/physics/pdme/compare/0.9.3...1.0.0) (2024-04-29)


### Bug Fixes

* fixes the broken implementation of the tarucha frequency calculation ([631ba13](https://gitea.deepak.science:2222/physics/pdme/commit/631ba13c791c71ad8922d39a13b780a40eac2391))

### [0.9.3](https://gitea.deepak.science:2222/physics/pdme/compare/0.9.2...0.9.3) (2024-02-26)


### Features

* adds util func for calculating arg using sign instead of complex arithmetic ([3ebe2bb](https://gitea.deepak.science:2222/physics/pdme/commit/3ebe2bb82430d677680383c42a1c269df83d99cd))


### Bug Fixes

* fixes stupid cost shape issue ([ed9dd2c](https://gitea.deepak.science:2222/physics/pdme/commit/ed9dd2c94f88a08c36f581f05b26a87a6b780d5b))

### [0.9.2](https://gitea.deepak.science:2222/physics/pdme/compare/0.9.1...0.9.2) (2023-07-24)


### Bug Fixes

* update tests but for git also don't wrap costs ([50f98ed](https://gitea.deepak.science:2222/physics/pdme/commit/50f98ed89b2a05cd47c41958036dd50bc872e07c))

### [0.9.1](https://gitea.deepak.science:2222/physics/pdme/compare/0.9.0...0.9.1) (2023-07-24)


### Bug Fixes

* fixes some of the shape mangling of our mcmc code ([e01d0e1](https://gitea.deepak.science:2222/physics/pdme/commit/e01d0e14a9bcd6d7e8fe9449ce562dbf1b8fd25c))

## [0.9.0](https://gitea.deepak.science:2222/physics/pdme/compare/0.8.9...0.9.0) (2023-07-24)


### ⚠ BREAKING CHANGES

* separates threshold cost and the seed_cost in mcmc

### Features

* separates threshold cost and the seed_cost in mcmc ([ca710e3](https://gitea.deepak.science:2222/physics/pdme/commit/ca710e359fd0cfbb620a3574a2fa4fab1be2b52a))

### [0.8.9](https://gitea.deepak.science:2222/physics/pdme/compare/0.8.8...0.8.9) (2023-07-23)


### Features

* adds a bunch of mcmc generation code for log spaced models, yay ([f280448](https://gitea.deepak.science:2222/physics/pdme/commit/f280448cfe2fcf5bdc5ac2317ee52b27523bb49d))
* adds utility functions for dealing with markov chain monte carlo ([feb0a5f](https://gitea.deepak.science:2222/physics/pdme/commit/feb0a5f6453dcb5e71a07c7749cd579dab15171c))

### [0.8.8](https://gitea.deepak.science:2222/physics/pdme/compare/0.8.7...0.8.8) (2023-04-09)


### Features

* adds fast calc that allows for variable temp ([36454d5](https://gitea.deepak.science:2222/physics/pdme/commit/36454d5044d93b6b178e016b84dd59a5ebaf15e2))

### [0.8.7](https://gitea.deepak.science:2222/physics/pdme/compare/0.8.6...0.8.7) (2022-09-17)


### Features

* adds xy model for convenience to pdme ([e894c89](https://gitea.deepak.science:2222/physics/pdme/commit/e894c897029c05a1d4754e7930ae9ba2be7a1cfd))
* moves xy model up to model package ([2a1ae3b](https://gitea.deepak.science:2222/physics/pdme/commit/2a1ae3b1a7f7e10469b7fd2930fee0b338f0c03f))


### Bug Fixes

* Correctly generates monte carlo version of xy model dipoles ([5acf0ac](https://gitea.deepak.science:2222/physics/pdme/commit/5acf0ac347382705674bb596440d27cba3730bac))

### [0.8.6](https://gitea.deepak.science:2222/physics/pdme/compare/0.8.5...0.8.6) (2022-06-13)


### Features

* makes library build system poetry-core ([ed0c6e2](https://gitea.deepak.science:2222/physics/pdme/commit/ed0c6e2858f45fec9b9a673d9b5bc98605e73508))


### Bug Fixes

* pyproject build system now core as well ([6277e84](https://gitea.deepak.science:2222/physics/pdme/commit/6277e843d5a7df8eba1878db490d2fae4052af57))

### [0.8.5](https://gitea.deepak.science:2222/physics/pdme/compare/0.8.4...0.8.5) (2022-06-04)


### Features

* adds fixedorientation model ([2cdf46a](https://gitea.deepak.science:2222/physics/pdme/commit/2cdf46afa1492f86b4c403e4c5013cefc89b21d6))

### [0.8.4](https://gitea.deepak.science:2222/physics/pdme/compare/0.8.3...0.8.4) (2022-05-26)


### Bug Fixes

* probability of occupancy fixed ([01f905a](https://gitea.deepak.science:2222/physics/pdme/commit/01f905a237a2423f5637ee6a0f43e0937c55d2ea))

### [0.8.3](https://gitea.deepak.science:2222/physics/pdme/compare/0.8.2...0.8.3) (2022-05-22)


### Features

* Adds log spaced in frequency space model ([7a9fa1b](https://gitea.deepak.science:2222/physics/pdme/commit/7a9fa1ba04a12586ef09c89e35e706817012faab))

### [0.8.2](https://gitea.deepak.science:2222/physics/pdme/compare/0.8.1...0.8.2) (2022-05-07)


### Features

* Adds Random count dipole model with binomial type distribution for dipole number ([27cbb36](https://gitea.deepak.science:2222/physics/pdme/commit/27cbb364a6d9625abca6145dafedf0df5743f816))

### [0.8.1](https://gitea.deepak.science:2222/physics/pdme/compare/0.8.0...0.8.1) (2022-04-30)


### Features

* adds multidipole nonlocal spectrum calculations ([8264ca3](https://gitea.deepak.science:2222/physics/pdme/commit/8264ca3d6edb703422229fde57bbb1d726ce5139))

## [0.8.0](https://gitea.deepak.science:2222/physics/pdme/compare/0.7.0...0.8.0) (2022-04-30)


### ⚠ BREAKING CHANGES

* single dipole still outputs collection now to make interface consistent

### Features

* single dipole still outputs collection now to make interface consistent ([cb3c280](https://gitea.deepak.science:2222/physics/pdme/commit/cb3c280464aa2c4b0ec9320e6a319f4a454a0e9f))

## [0.7.0](https://gitea.deepak.science:2222/physics/pdme/compare/0.6.2...0.7.0) (2022-04-30)


### ⚠ BREAKING CHANGES

* Changes names of classes to make more clear for dipole model and single dipole fixed magnitude model
* reduces model to minimal bayes needed stuff
* Guts the model interface for only the things useful for monte carlo bayes stuff
* Removes unused models to make refactoring a bit easier

### Features

* adds fast method for calculating multiple dipole calculations ([1bad2f7](https://gitea.deepak.science:2222/physics/pdme/commit/1bad2f743af6a95189448d8929c70a036e6c21ab))
* adds multidipole fixed mag model ([0c64ed0](https://gitea.deepak.science:2222/physics/pdme/commit/0c64ed02f0d42cd0957be0511a35dc49153a256f))
* Changes names of classes to make more clear for dipole model and single dipole fixed magnitude model ([7eba331](https://gitea.deepak.science:2222/physics/pdme/commit/7eba3311c7ba90e4404b1a7b7c33df1585a800ba))
* Guts the model interface for only the things useful for monte carlo bayes stuff ([946945d](https://gitea.deepak.science:2222/physics/pdme/commit/946945d791ed763e435afff7a6ae8c2b1c0e1711))
* reduces model to minimal bayes needed stuff ([0d5508a](https://gitea.deepak.science:2222/physics/pdme/commit/0d5508a0b5641d98ee6f3484f58c923440c4c2c1))
* Removes unused models to make refactoring a bit easier ([c04d863](https://gitea.deepak.science:2222/physics/pdme/commit/c04d863d7fa22c98d8542a5f72791b542358ff61))


### Bug Fixes

* makes name of method match interface ([029021e](https://gitea.deepak.science:2222/physics/pdme/commit/029021e39328c7ca7a73afcf23d86ad17516982f))
* makes repr return actual name ([0f78c7c](https://gitea.deepak.science:2222/physics/pdme/commit/0f78c7c2db742d59f2a5ee9da767f35aafa49b78))
* uses rng passed in correctly ([70d95c8](https://gitea.deepak.science:2222/physics/pdme/commit/70d95c8d6d5af10f926d8729a5a0eaed9ad8259d))

### [0.6.2](https://gitea.deepak.science:2222/physics/pdme/compare/0.6.1...0.6.2) (2022-04-18)


### Features

* adds methods for converting pdme objects into flatter numpy arrays ([5c6c4c7](https://gitea.deepak.science:2222/physics/pdme/commit/5c6c4c79d1b55d8d6bf70e2e54226d282d831f66))
* Allows you to pass in rng to generate monte carlo dipoles ([ab244ed](https://gitea.deepak.science:2222/physics/pdme/commit/ab244ed91dede1e3c29fe94ea96089f4c15aa1fb))

### [0.6.1](https://gitea.deepak.science:2222/physics/pdme/compare/0.6.0...0.6.1) (2022-03-28)


### Bug Fixes

* Swaps high and lows for ranges if needed to make negatives behave nicer ([8a60967](https://gitea.deepak.science:2222/physics/pdme/commit/8a60967ddfa18e49460b05edc7ec575f06db868f))

## [0.6.0](https://gitea.deepak.science:2222/physics/pdme/compare/0.5.4...0.6.0) (2022-03-27)


### ⚠ BREAKING CHANGES

* adds pair inputs to array function

### Features

* adds calc for pairs and pair ranges ([e72489f](https://gitea.deepak.science:2222/physics/pdme/commit/e72489f0cb6586756180c2021649f4eb019c77fc))
* adds fast nonlocal noise Sij calculator ([5fbff2a](https://gitea.deepak.science:2222/physics/pdme/commit/5fbff2a5c0f128ffc5b749788c8bdcd6f88de234))
* adds methods for better creation of input lists, including pairs ([852836b](https://gitea.deepak.science:2222/physics/pdme/commit/852836b924c8ffefd6b28a8ea1bc1ca47b77756e))
* adds pair inputs to array function ([a7508b8](https://gitea.deepak.science:2222/physics/pdme/commit/a7508b8906923a579dfa05edc22963d2f0102be9))

### [0.5.4](https://gitea.deepak.science:2222/physics/pdme/compare/0.5.3...0.5.4) (2022-03-06)


### Bug Fixes

* lets you get model from discretisation for fixed magnitude models in type hintable way ([548dcfe](https://gitea.deepak.science:2222/physics/pdme/commit/548dcfebfc7cd6354ad708b3ab0e664881c58de4))

### [0.5.3](https://gitea.deepak.science:2222/physics/pdme/compare/0.5.2...0.5.3) (2022-03-06)


### Features

* Adds between utility function ([a782b49](https://gitea.deepak.science:2222/physics/pdme/commit/a782b4957f2aebfb0bf9a3c7d4166277a5450b76))
* Adds fast calc expressions ([0855911](https://gitea.deepak.science:2222/physics/pdme/commit/08559110be197b7f4a685d5e44e248f914853a3c))
* Adds numpy make more dipoles at once and converters ([c70a971](https://gitea.deepak.science:2222/physics/pdme/commit/c70a971ce09bda236a84cfcff309d9a9cf2092d9))
* Calculates range measurements. ([2d773df](https://gitea.deepak.science:2222/physics/pdme/commit/2d773df7259378ba9285776407b2cb5ae380d809))

### [0.5.2](https://gitea.deepak.science:2222/physics/pdme/compare/0.5.1...0.5.2) (2022-03-06)

### [0.5.1](https://gitea.deepak.science:2222/physics/pdme/compare/0.5.0...0.5.1) (2022-03-05)


### Bug Fixes

* Fixes typo ([31762de](https://gitea.deepak.science:2222/physics/pdme/commit/31762de69785b9c25704605b132c52036ad6dad3))
