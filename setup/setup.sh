#!/bin/bash

# Go outside
cd ..

# Unzip phi_files
cd phi_files
cat phi_j.tar.* | tar xzvf -
cd ..

# Clone submodule in case you didn't do it...
git submodule update --init --recursive

# Build curvemul 
cd curvemul 
make
cd ..