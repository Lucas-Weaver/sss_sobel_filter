from PIL import Image, ImageFilter
import numpy as np
import math
import cv2 as cv
#from matplotlib import plot
#from matplotlib.image import imread

#method 1, high productivity

x_kernel = (1,0,-1,2,0,-2,1,0,-1)
y_kernel = (1,2,1,0,0,0,-1,-2,-1)

def high_productivity(im):
    
    im_x_gradient = im.filter(filter = ImageFilter.Kernel((3,3),x_kernel,1,0))
    im_y_gradient = im.filter(filter = ImageFilter.Kernel((3,3),y_kernel,1,0))
    
    x_arr = np.asarray(im_x_gradient)
    y_arr = np.asarray(im_y_gradient)
    final = np.zeros((len(x_arr),len(x_arr[0])),dtype=np.float64)
    for r in range(len(x_arr)):
        for c in range(len(x_arr[0])):
            final[r][c] = math.sqrt( (x_arr[r][c]**2)+(y_arr[r][c]**2))*3
    final_uint8 = np.clip(final, 0, 255).astype(np.uint8)
    return final_uint8
    #sobel = Image.fromarray(final_uint8,mode="L")





 
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
 
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    pil_im = Image.fromarray(gray)
    edges = high_productivity(pil_im)
    # Display the resulting frame
    cv.imshow('frame', edges)
    if cv.waitKey(1) == ord('q'):
        break
 
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

