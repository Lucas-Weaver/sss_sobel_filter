import numpy as np
from PIL import Image
import sys, os
#from canny import canny
from scipy.ndimage import distance_transform_edt

DEFAULT_ALPHA = 1.0 / 9

def fom(img, img_gold_std, alpha = DEFAULT_ALPHA):
    """
    Computes Pratt's Figure of Merit for the given image img, using a gold
    standard image as source of the ideal edge pixels.
    """
    #img has to be array_like
    # To avoid oversmoothing, we apply canny edge detection with very low
    # standard deviation of the Gaussian kernel (sigma = 0.1).
    #img = canny(img, 0.1, 20, 50)
    #edges_gold = canny(img_gold_std, 0.1, 20, 50)
    
    # Compute the distance transform for the gold standard image.
    dist = distance_transform_edt(np.invert(img_gold_std))

    fom = 1.0 / np.maximum(
        np.count_nonzero(img),
        np.count_nonzero(img_gold_std))

    N, M = img.shape

    for i in range(0, N):
        for j in range(0, M):
            if img[i, j]:
                fom += 1.0 / ( 1.0 + dist[i, j] * dist[i, j] * alpha)

    fom /= np.maximum(
        np.count_nonzero(img),
        np.count_nonzero(img_gold_std))    

    return fom
def make_grey(name_of_dir):
    for filename in os.listdir(name_of_dir):
        img = Image.open(os.path.join(name_of_dir,filename)).convert('L')
        img.save(os.path.join(name_of_dir,filename))
        
'''
test = Image.open(sys.argv[1])
test_arr = np.array(test)
ground = Image.open(sys.argv[2])

ground_truth_arr = np.array(ground)

print(fom(test_arr,ground_truth_arr))
'''

make_grey("/home/atharva/sss_sobel_filter/c-sobel-filter/test/BSDS300/images/train")

