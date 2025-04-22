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

scores = []
directory = os.fsencode("/home/atharva/sss_sobel_filter/c-sobel-filter/test/output")
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    output_path = os.path.join(directory, file)
    filename = filename.replace("png","jpg")
    ground_path = "/home/atharva/sss_sobel_filter/c-sobel-filter/test/ground_truth/"+filename
    output_image = Image.open(output_path)
    ground_truth_image = Image.open(ground_path)
    
    output_arr = np.array(output_image)
    ground_truth_arr = np.array(ground_truth_image)
    
    scores.append(fom(output_arr,ground_truth_arr))
    
file = open("/home/atharva/sss_sobel_filter/c-sobel-filter/data/times.txt")
time_sum = 0
line_count = 0
for line in file:
    line = line.replace("\n","")
    time_sum+=float(line)
    line_count+=1
print(f'average time: {time_sum/line_count}')
print(f'average FOM: {sum(scores)/line_count}')

out = open("/home/atharva/sss_sobel_filter/c-sobel-filter/data/euclidean_double_fom.txt","x")

[out.write(f'{i}\n') for i in scores]

out.close()
    
    
'''
test = Image.open(sys.argv[1])
test_arr = np.array(test)
ground = Image.open(sys.argv[2])

ground_truth_arr = np.array(ground)

print(fom(test_arr,ground_truth_arr))
'''



