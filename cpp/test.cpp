#include "opencv2/opencv.hpp"
#include <iostream>
#include <iomanip>
#include <sys/time.h>

using namespace cv;

// TODO: put this in a header...
long get_time();

int main(int, char**)
{
    VideoCapture cap(0); // open the default camera
    if(!cap.isOpened())  // check if we succeeded
        return -1;
    cap.set(CAP_PROP_FRAME_WIDTH, 1280);
    cap.set(CAP_PROP_FRAME_HEIGHT, 720);
    cap.set(CAP_PROP_FPS, 60);

    int height = cap.get(CAP_PROP_FRAME_HEIGHT);
    int width = cap.get(CAP_PROP_FRAME_WIDTH);
    int fps = cap.get(CAP_PROP_FPS);

    std::printf("helo %d", 1);
    std::cout << "res: " << width << "x" << height << std::endl;
    std::cout << fps << "fps at start" << std::endl;

    Mat edges;
    namedWindow("edges",1);
    int frame_count = 0;
    long start_time = get_time();

    for(;;)
    {
        Mat frame;
        cap.read(frame); // get a new frame from camera
        // cvtColor(frame, edges, COLOR_BGR2GRAY);
        // GaussianBlur(edges, edges, Size(7,7), 1.5, 1.5);
        // Canny(edges, edges, 0, 30, 3);
        // imshow("edges", edges);
        imshow("edges", frame);
        if(waitKey(1) >= 0) break;

        frame_count += 1;
        if (frame_count >= 30) {
          long end_time = get_time();
          std::cout << std::setw(6) << (float(frame_count) / (float(end_time - start_time)/1000)) << "fps" << std::endl;
          start_time = end_time;
          frame_count = 0;
        }
    }
    // the camera will be deinitialized automatically in VideoCapture destructor
    return 0;
}

long get_time() {
  timeval time;
  gettimeofday(&time, NULL);
  return (time.tv_sec * 1000) + (time.tv_usec / 1000);
}
