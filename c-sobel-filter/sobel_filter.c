#include <stdio.h>
#include <omp.h>
#include <math.h>
#define STB_IMAGE_IMPLEMENTATION
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image.h"
#include "stb_image_write.h"



void sobel_filter(uint8_t * src_arr,uint8_t * dest_arr,int height, int width)
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
            if (abs(x_sum) + abs(y_sum) > 255){
			    dest_arr[x * width + y] = 255;
            } else {
			    dest_arr[x * width + y] = abs(x_sum) + abs(y_sum);
            }

		}
	}

}

int main(){
    
    int width, height, bpp;

    uint8_t* gray_image = stbi_load("test.png", &width, &height, &bpp, 1);

    uint8_t sobel[width*height];

    sobel_filter(gray_image,sobel,height,width);

    stbi_write_png("sobel_filter.png",width,height,1,sobel,width);

    
    stbi_image_free(gray_image);
    return 0;
}
