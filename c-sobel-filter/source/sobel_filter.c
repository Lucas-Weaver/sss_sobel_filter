#include <stdio.h>
#include <omp.h>
#include <math.h>
#include <time.h>
#define STB_IMAGE_IMPLEMENTATION
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image.h"
#include "stb_image_write.h"



void sobel_filter(uint8_t * src_arr,uint8_t * dest_arr,int height, int width,int threshold,int metric)
{	
	/* Variable Declaration */
	register int x_sum, y_sum;

	
	

	/* Parallelizing using OpenMP */
	/* Give an entire row to a single thread to increase cache performance */
	#pragma omp parallel for private(x_sum, y_sum) schedule(static, 1)
	for (register int x = 1; x < height - 1; x++) {
		/* 
		 * Apply the Sobel Filter's kernel convolution
		 * on each pixel of a single row.
		 * Convolution matrices:
		 * X:
		 * -1  0  1
		 * -2  0  2
		 * -1  0  1
		 * Y:
		 * -1 -2 -1
		 *  0  0  0
		 *  1  2  1
		 * Convolve with X to get Gx and with Y to get Gy
		 * The final pixel value is the Eucledian norm of Gx and Gy
		 */
		for (register int y = 1; y < width - 1; y++) {
			x_sum = (
				src_arr[(x + 1)*width + (y + 1)] -
				src_arr[(x + 1)*width + (y - 1)] +
				(src_arr[   (x)*width + (y + 1)] << 1) -
				(src_arr[   (x)*width + (y - 1)] << 1) +
				src_arr[(x - 1)*width + (y + 1)] -
				src_arr[(x - 1)*width + (y - 1)]
			);

			y_sum = (
				src_arr[ (x + 1)*width + (y + 1)] +
				(src_arr[(x + 1)*width + (y)    ] << 1) +
				src_arr[ (x + 1)*width + (y - 1)] -
				src_arr[ (x - 1)*width + (y + 1)] -
				(src_arr[(x - 1)*width + (y)    ] << 1) -
				src_arr[ (x - 1)*width + (y - 1)]
			);

			// Manhatan Distance is used instead of Eucledian to increase performance
			//if metric is 1, use eucliden. otherwise use manhatan
			int distance; //type defines the precision

			if (metric){
				distance =  sqrt(pow((double)x_sum,(double)2) + pow((double)y_sum,(double)2));
			}
			else{
				distance = abs(x_sum)+abs(y_sum);
			}
			if (distance > threshold){
					dest_arr[x * width + y] = 255;
			} else {
					dest_arr[x * width + y] = 0;
			}

		}
	}

}

int main(int argc, char * argv[]){
    
    int width, height, bpp;
    uint8_t* gray_image = stbi_load(argv[1], &width, &height, &bpp, 1);

    uint8_t sobel[width*height];
    clock_t start = clock();
    sobel_filter(gray_image,sobel,height,width,350,1);
    clock_t end = clock();
    double cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    
    stbi_write_png(argv[2],width,height,1,sobel,width);
    
    stbi_image_free(gray_image);
    
    FILE * out = fopen("data/times.txt","a");
    fprintf(out, "%f\n", cpu_time_used);
    fclose(out);
    return 0;
}

