#!/bin/bash
cd BSDS300/images/train
for filename in *; do
	cd /home/atharva/sss_sobel_filter/c-sobel-filter/test/ground_truth
	curl https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/BSDS300/html/images/human/normal/outline/gray/union/$filename > $filename
	echo $filename
done
