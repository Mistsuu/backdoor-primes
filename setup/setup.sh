#!/bin/bash

# Go outside
cd ..

# Clone submodule in case you didn't do it...
git submodule update --init --recursive

# Build curvemul 
cd curvemul
make