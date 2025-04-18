#!/bin/bash
export OMP_NUM_THREADS=16
gcc -c -o sobel.o sobel_filter.c -fopenmp
FLAGS="$(pkg-config --cflags --libs opencv4)"
g++ -c test.cpp -o cv $FLAGS
g++ -o final sobel.o cv $FLAGS -fopenmp
./final


