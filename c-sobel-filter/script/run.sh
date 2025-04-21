#!/bin/bash
#clear times.txt
cd /home/atharva/sss_sobel_filter/c-sobel-filter/data
rm -f times.txt
#re-compile c files to reflect recent changes
cd /home/atharva/sss_sobel_filter/c-sobel-filter
export OMP_NUM_THREADS=16
gcc -g -o sobel_filter.o source/sobel_filter.c -fopenmp -lm
#run sobel filter on all the test images
cd /home/atharva/sss_sobel_filter/c-sobel-filter/test/BSDS300/images/test
for filename in *; do
	cd /home/atharva/sss_sobel_filter/c-sobel-filter/
	
	./sobel_filter.o /home/atharva/sss_sobel_filter/c-sobel-filter/test/BSDS300/images/test/$filename /home/atharva/sss_sobel_filter/c-sobel-filter/test/output/${filename/jpg/"png"}
done

cd /home/atharva/sss_sobel_filter/c-sobel-filter/test/BSDS300/images/train
for filename in *; do
	cd /home/atharva/sss_sobel_filter/c-sobel-filter/
	
	./sobel_filter.o /home/atharva/sss_sobel_filter/c-sobel-filter/test/BSDS300/images/train/$filename /home/atharva/sss_sobel_filter/c-sobel-filter/test/output/${filename/jpg/"png"}
done
#run FOM metric on all images
cd /home/atharva/sss_sobel_filter/c-sobel-filter
python3 source/fom.py

