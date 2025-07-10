# Multi-dimensional Analysis of Real-time Edge Detection on an Embedded System​

## Overview
This was a semester research project done with the Synergy lab at Virginia Tech. I implemented and tested the Sobel filter for edge detection and measured runtime, power, and accuracy. my results are all contained in the data folder, and if you would like to test the code yourself you can find all of the test images I used at https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/grouping/resources.html. I would like to give a huge thanks to my advisors Dr. Wu Feng and Atharva Gondhalekar ​for helping me along the way. The below abstract and the poster in the repo were submitted to the Virginia Tech Undergraduate Rsearch in Computer Science Spring Symposium.

## Abstract

Image processing on edge devices has become prominent in the past few years with the global focus on self-driving cars by leading companies such as Tesla, Waymo and Cruise. The need for real-time edge detection is especially important as Tesla abandoned its close-range RADAR detectors in favor of a full computer-vision approach in 2021 and removed all ultrasonic sensors by 2023. We consider the Sobel operator with different parameters for this task as it is easily parallelizable and takes a relatively low amount of computation compared to other edge-detection strategies. We test different implementations of the sobel filter by varying its precision and distance metric to find optimal parameters for runtime, power, and accuracy as measured by the Pratt Figure of Merit (FOM). For ground truth images we use the Berkeley Segmentation Dataset and Benchmark (BSDS300). As expected we find that higher precision results in higher runtimes and higher accuracy, however, we find that using the euclidean metric is significantly less accurate than the Manhattan metric while taking 2-3x the runtime per frame. We also find that single precision floats take the least amount of power. Thus, we recommend the Sobel filter with both manhattan distance metric and float precision for the best balance between accuracy, runtime, and power consumption.


compile code in c-sobel-filter with 'gcc -g *.c -lm'


 
