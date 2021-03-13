#!/usr/bin/env bash

brew install icu4c
brew link icu4c --force
ver=$(icu-config --version)
export ICU_VERSION="${ver}"
export PYICU_INCLUDES="/usr/local/Cellar/icu4c/${ver}/include"
export PYICU_LFLAGS=-L"/usr/local/Cellar/icu4c/${ver}/lib"
