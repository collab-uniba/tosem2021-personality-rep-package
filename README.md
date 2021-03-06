## tosem2021-personality-rep-package [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4720988.svg)](https://doi.org/10.5281/zenodo.4720988)
Replication package for the manuscript F. Calefato and F. Lanubile (2021) "Using Personality Detection Tools for Software Engineering Research: How Far Can
We Go?" *ACM TOSEM*, DOI: 10.1145/3491.039.

### Requirements
Ensure that your box fulfills the following requirements:
* Python 3.8.3+
* R 4.0.4+
* Java 1.8+
* python3-venv
* pandoc
* LaTeX
* homebrew (macOS-only)

On macOS, you can install LaTeX and pandoc by executing `brew install mactex pandoc`.

On Ubuntu, run `sudo apt install texlive-latex-extra pandoc`.

Finally, after installing Java, ensure that the environment variable `$JAVA_HOME` is properly set.

### Cloning
The repository uses git submodules. To clone the code and its submodules, run `git clone --recursive <repo-url.git>`

### Setup
Setup instructions are contained in the file `setup.sh` and must be run only once. The script has been tested on macOS Big Sur and Ubuntu 20.04 LTS.
To complete the setup, simply run `bash setup.sh`. Please, note that the installation of the R packages will prompt you to enter the your password via `sudo`. 

If you have `anaconda` installed, ensure that the `conda base` environment is not active during setup.

### Reproducible pipeline

To reproduce the pipeline, run `bash repro.sh`:
```text
Usage: repro.sh [-h] [-v] -s all|phase1|phase2 -d test|full
Available options:
-h, --help      Print this help and exit
-v, --verbose   Print script debug info
-s, --stage     Pipeline stage. Accepted values: all, phase1, phase2
-d, --dataset   Dataset size. Accepted values: test, full
```

You can choose to reproduce the full pipeline by passing the argument `-s|--stage all`.
Otherwise, you can reproduce individually the two phases of the experiment by passing instead
the arguments `phase1` or `phase2`. Also, to reduce the computational time, you can chose between running the script
on the `full` dataset or on a random `test` subsample.

#### Notes

1. *Phase Two* is quite time-consuming---it can take hours, in not days, depending on your box specs. For test 
   purposes, you can supply the argument `test` to work with a very small, random subsample of the original dataset and 
   keep the computational time within minutes.

2. The script `ph1_0-goldstandard_creation.sh` is intentionally not part of the reproducible pipeline. It is meant to be
   executed only once, to create the anonymized gold standard in which email addresses have been replaced
   with hashed ids and all the sensitive content from emails (e.g., names, urls) have been scrubbed. This is intended to prevent others 
   from tracking down the participants by searching for matching text into the public email archives of the Apache Software Foundation.
