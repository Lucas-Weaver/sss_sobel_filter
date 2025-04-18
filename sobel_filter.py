from PIL import Image, ImageFilter
import numpy as np
import math,time
import cv2 as cv
from scipy import ndimage, datasets

#method 1, high productivity

x_kernel = (1,0,-1,2,0,-2,1,0,-1)
y_kernel = (1,2,1,0,0,0,-1,-2,-1)

total_time = 0
frames = 0
def filter(arr,scale,offset):
    sobel_h = ndimage.sobel(arr, 0)  # horizontal gradient
    sobel_v = ndimage.sobel(arr, 1)  # vertical gradient
    magnitude = np.sqrt(sobel_h**2 + sobel_v**2)
    magnitude *= scale
    magnitude += offset
    return magnitude.astype(np.uint8)



    
def high_productivity(im):
    global total_time
    global frames
    start = time.time()
    im_x_gradient = im.filter(filter = ImageFilter.Kernel((3,3),x_kernel,1,0))
    im_y_gradient = im.filter(filter = ImageFilter.Kernel((3,3),y_kernel,1,0))

    x_arr = np.asarray(im_x_gradient)
    y_arr = np.asarray(im_y_gradient)
    final = np.zeros((len(x_arr),len(x_arr[0])),dtype=np.uint8)
    for r in range(len(x_arr)):
        for c in range(len(x_arr[0])):
            #final[r][c] = math.sqrt( (x_arr[r][c]**2)+(y_arr[r][c]**2))*3
            final[r][c] = abs(x_arr[r][c])+abs(y_arr[r][c])
    #final_uint8 = np.clip(final, 0, 255).astype(np.uint8)
    end = time.time()
    total_time+=(end-start)
    frames+=1
    return final
def convolution(im_arr,kernel):
    final = np.zeros((len(im_arr),len(im_arr[0]),1))
    im_arr = im_arr.astype(int)
    for row in range(1,len(im_arr)-1):
        for col in range(1,len(im_arr[0])-1):
            a = 0
            for k_row in range(len(kernel)):
                for k_col in range(len(kernel[k_row])):
                    #print(kernel[k_row][k_col])
                    #print(im_arr[row+k_row-1][col+k_col-1][0])
                    a+=(kernel[k_row][k_col])*(im_arr[row+k_row-1][col+k_col-1][0])
            a = a if a>0 and a<255 else (0 if a<0 else 255)
            
            final[row][col] = [a]

    return final

def mid_productivity(im):
    global total_time
    global frames
    start = time.time()
    x_arr = convolution(
        convolution(np.asarray(im),((),(1,0,-1),()))
        ,[[1],[2],[1]]
        )
    y_arr = convolution(convolution(np.asarray(im),((),(1,2,-1),())),[[1],[2],[1]])
    final = np.zeros((len(x_arr),len(x_arr[0])),dtype=np.uint8)
    for r in range(len(x_arr)):
        for c in range(len(x_arr[0])):
            final[r][c] = abs(x_arr[r][c][0])+abs(y_arr[r][c][0])
    end = time.time()
    total_time+=(end-start)
    frames+=1
    return final
'''
arr = mid_productivity(Image.open('test.png'))
sobel = Image.fromarray(arr)
sobel.show()

'''

cap = cv.VideoCapture('test_video_1280p.mp4')

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
    start = time.time()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    final = filter(np.asarray(gray),3,20)
    end = time.time()
    frames+=1
    total_time+=end-start
    # Display the resulting frame
    cv.imshow('frame', final)
    if cv.waitKey(1) == ord('q'):
        break
 
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
print(total_time/frames)

