# WEIS

WEIS, Wind Energy with Integrated Servo-control, performs multifidelity co-design of wind turbines. WEIS is a framework that combines multiple NREL-developed tools to enable design optimization of floating offshore wind turbines.

Author: [NREL WISDEM & OpenFAST & Control Teams](mailto:systems.engineering@nrel.gov) 

## Version

This software is a version 0.0.1.

## Documentation

See local documentation in the `docs`-directory or access the online version at <https://weis.readthedocs.io/en/latest/>

## Packages

WEIS integrates in a unique workflow four models:
* [WISDEM](https://github.com/WISDEM/WISDEM) is a set of models for assessing overall wind plant cost of energy (COE).
* [OpenFAST](https://github.com/OpenFAST/openfast) is the community model for wind turbine simulation to be developed and used by research laboratories, academia, and industry.
* [TurbSim](https://www.nrel.gov/docs/fy09osti/46198.pdf) is a stochastic, full-field, turbulent-wind simulator. 
* [ROSCO](https://github.com/NREL/ROSCO) provides an open, modular and fully adaptable baseline wind turbine controller to the scientific community.

In addition, three external libraries are added:
* [ROSCO_Toolbox](https://github.com/NREL/ROSCO_toolbox) is a toolbox designed to ease controller implementation for the wind turbine researcher and tune the ROSCO controller.
* [pCrunch](https://github.com/NREL/pCrunch) is a collection of tools to ease the process of parsing large amounts of OpenFAST output data and conduct loads analysis.
* [pyOptSparse](https://github.com/mdolab/pyoptsparse) is a framework for formulating and efficiently solving nonlinear constrained optimization problems.

The core WEIS modules are:
 * _aeroelasticse_ is a wrapper to call [OpenFAST](https://github.com/OpenFAST/openfast)
 * _control_ contains the routines calling the [ROSCO_Toolbox](https://github.com/NREL/ROSCO_toolbox) and the routines supporting distributed aerodynamic control devices, such trailing edge flaps
 * _gluecode_ contains the scripts glueing together all models and libraries
 * _multifidelity_ contains the codes to run multifidelity design optimizations
 * _optimization_drivers_ contains various optimization drivers
 * _schema_ contains the YAML files and corresponding schemas representing the input files to WEIS

## Installation

Installation with [Anaconda](https://www.anaconda.com) is the recommended approach because of the ability to create self-contained environments suitable for testing and analysis.  WEIS requires [Anaconda 64-bit](https://www.anaconda.com/distribution/).

The installation instructions below use the environment name, "weis-env," but any name is acceptable.

1.  Setup and activate the Anaconda environment from a prompt (Anaconda3 Power Shell on Windows or Terminal.app on Mac)

        conda config --add channels conda-forge
        conda create -y --name weis-env python=3.8
        conda activate weis-env
    
2.  Use conda to install the build dependencies.  Note the differences between Windows and Mac/Linux build systems

        conda install -y cmake cython geopy git jsonschema make matplotlib-base numpy numpydoc openmdao openpyxl pandas pip pytest pyyaml ruamel_yaml scipy setuptools shapely six sympy swig xlrd
        conda install -y petsc4py mpi4py compilers       # (Mac / Linux only)   
        conda install -y m2w64-toolchain libpython       # (Windows only)
        pip install simpy marmot-agents
        git clone https://github.com/WISDEM/WEIS.git
        cd WEIS
        module purge        # (On eagle, or other HPC cluster, only)
        python setup.py develop

**NOTE:** To use WEIS again after installation is complete, you will always need to activate the conda environment first with `conda activate weis-env`

## Git sub-tree

This repo contains copies of other codes created by using the `git subtree` commands.
Below are some details about how to add external codes and update them.

To add an external code, using OpenFAST as an example, type:

```
$ git remote add OpenFAST https://github.com/OpenFAST/openfast
$ git fetch OpenFAST
$ git subtree add -P OpenFAST OpenFAST/dev --squash
```

The `--squash` is important so WEIS doesn't get filled up with commits from the subtree repos.

Once a subtree code exists in this repo, we can update it like this.
This first two lines are needed only if you don't have the remote for the particular subtree yet.
If you already have the remote, only the last line is needed.

```
$ git remote add OpenFAST https://github.com/OpenFAST/openfast
$ git fetch OpenFAST
$ git subtree pull --prefix OpenFAST https://github.com/OpenFAST/openfast dev --squash
```

Changes to these subtree codes **should only be made to their original repos**, *not* to this WEIS repo.
Once those individual repos have been updated, use the previous `git subtree pull` command to pull in those updates to the WEIS repo.

If you run into trouble using `git subtree`, specifically if you see `git: 'subtree' is not a git command.`, try using your system git instead of any conda-installed git.
Specifically, try using `/usr/bin/git subtree` for any subtree commands.
If that doesn't work for you, please open an issue on this repo so we can track it.
This should only be relevant for developers contributing to WEIS, not to users.

## Run Unit Tests

Each package and sub-module of WEIS has its own set of unit tests, some of which are more comprehensive than others.

## Feedback

For software issues please use <https://github.com/WISDEM/WEIS/issues>.  
