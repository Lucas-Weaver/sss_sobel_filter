#!/bin/bash

cd input 
curl https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/BSDS300/html/images/plain/normal/gray/$1.jpg > $1.jpg
cd ../ground_truth
curl https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/BSDS300/html/images/human/normal/outline/gray/union/$1.jpg > $1.jpg
