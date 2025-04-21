#!/bin/bash

cd /home/atharva/sss_sobel_filter/c-sobel-filter/test/BSDS300/images/test
for filename in *; do
	cd /home/atharva/sss_sobel_filter/c-sobel-filter/
	
	./sobel_filter.o /home/atharva/sss_sobel_filter/c-sobel-filter/test/BSDS300/images/test/$filename /home/atharva/sss_sobel_filter/c-sobel-filter/test/output/${filename/jpg/"png"}
done
	
