
#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/imgcodecs.hpp>
#include <chrono>
#include <iostream>
using namespace cv;
using namespace std;
using namespace std::chrono;

extern "C" void sobel_filter(uint8_t * src_arr,uint8_t * dest_arr,int height, int width);

int main() {
    float total_time;
    int total_frames;
    Mat frame;
    
    VideoCapture cap;
    cap.open("test_video_1280p.mp4");
    if (!cap.isOpened()) {
        //cerr << "ERROR! Unable to open camera\n";
        return -1;
    }
    for (;;)
    {
        // wait for a new frame from camera and store it into 'frame'
        cap.read(frame);
        // check if we succeeded
        if (frame.empty()) {
            //cerr << "ERROR! blank frame grabbed\n";
            break;
        }
        Mat grayFrame;
        cvtColor(frame, grayFrame, COLOR_BGR2GRAY);
        
        auto start = high_resolution_clock::now();
        uchar * pixels = grayFrame.data;
        int width = grayFrame.cols;
        int height = grayFrame.rows;
        
        uchar filtered[width*height];
        sobel_filter(pixels,filtered,height,width);
        
        
        
        /*
        Mat grad,grad_x, grad_y;
        Mat abs_grad_x, abs_grad_y;
     
        Sobel(grayFrame, grad_x, CV_8U, 1, 0, 3, 1, 0, BORDER_DEFAULT);
     
        Sobel(grayFrame, grad_y, CV_8U, 0, 1, 3, 1, 0, BORDER_DEFAULT);
     
        // converting back to CV_8U
        convertScaleAbs(grad_x, abs_grad_x);
        convertScaleAbs(grad_y, abs_grad_y);
     
        addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0, grad);
        */
        auto stop = high_resolution_clock::now();
        auto duration = duration_cast<milliseconds>(stop - start);
        
        total_frames++;
        total_time+= duration.count();
        
    
        
        
        // show live and wait for a key with timeout long enough to show images
        imshow("Live", grayFrame);
        if (waitKey(5) >= 0)
            break;
    }
    cout << "average time per frame:"
        << (total_time/total_frames) << "ms" << endl;
        
    cout << "average fps: "
        << (total_frames/(total_time/1000)) << endl;
    return 0;
}
