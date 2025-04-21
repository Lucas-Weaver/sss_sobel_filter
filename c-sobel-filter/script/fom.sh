#!/bin/bash
cd ../source
export OMP_NUM_THREADS=16
cd ..
gcc -c -o sobel.o source/sobel_filter.c -fopenmp

