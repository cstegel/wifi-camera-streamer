# Overview

network_camera is meant as a module to set up video streaming between two devices via WIFI-direct.  It aims to have low latency for transmitting 720p@60fps while being transmitted from a small device such as an Odroid C1.

This is a work-in-progress.  Currently it will only stream locally to the same device.

# Setup

## Dependencies

### OpenCV 3

can be installed with the scripts from https://github.com/jayrambhia/Install-OpenCV
This install script worked as of commit e5ab672 (should be the same as https://github.com/LlazyLlama/Install-OpenCV).  The version used by me was OpenCV 3.0.0

  1. make sure your system is up to date: `sudo apt-get update && sudo apt-get upgrade && sudo apt-get dist-upgrade`
  2. `git clone https://github.com/LlazyLlama/Install-OpenCV`
  3. `cd Ubuntu; ./opencv_latest.sh`
  
  
### mjpg_streamer

Based off of these instructions: http://petrkout.com/electronics/low-latency-0-4-s-video-streaming-from-raspberry-pi-mjpeg-streamer-opencv/



  1. Install dependencies: `apt-get install libv4l-dev libjpeg8-dev imagemagick build-essential cmake subversion`
  2. `git clone https://github.com/codewithpassion/mjpg-streamer`
    - verified to work with commit a48d422 (bookmarked as https://github.com/LlazyLlama/mjpg-streamer)
  3. `cd mjpg-streamer-experimental`
  4. `make`
    - this creates the `mjpg_streamer` binary
  
# Running the camera stream

Start the camera HTTP stream by doing the following:

`./start_cam_stream.sh <path to mjpg_streamer binary directory>`
    
  - this folder will also contain the plugins folder 
  - eg: ~/git/mjpg-streamer/mjpg-streamer-experimental
  
# Running the display client

After the camera stream is running, simply run `python py/display_client_test.py` to connect to the HTTP camera stream and display it.

# Streaming methods

I've investigated a couple different streaming methods for this project and provide a summary below.  The goal is to stream video at 720p@60fps from one device to another on the same LAN.  

The webcam used for testing was a ELP 2.8mm Wide Angle Lens USB 2.0 camera module, capable of 720p@60fps mjpeg video capture.

The laptop this was tested on was an Asus S46CM with Intel i5-3317U  CPU @ 1.7GHz, Nvidia 635M GTX video card, 6 GB of RAM and an SSD hard drive. 

The desktop this was tested on had an Intel i7 860 @ 2.8GHz, Nvidia 560 GTX video card, 8 GB of RAM on a 7200 RPM HDD.

## mjpg-streamer

Most promising solution so far.  Fairly easy to set up as seen by `mjpg-streamer/start_cam_stream.sh` and the local player was able to play the stream somewhere between 20-50fps when a 720p@60fps recording was happening on both my desktop and my laptop.  This lower/varying framerate is likely due to auto-exposure being enabled on the camera since it was around 20fps when aimed at a dark image and 50fps when aimed at a light bulb.  There was also very low latency as observed from the `display_client_test.py` by quickly moving my hand (guess less than 50ms).

## ffmpeg

Various attempts were made to record using ffmpeg and stream directly to a URL as well as ffserver.  ffmpeg always reported that it was recording less than 20fps (usually 6-12fps) even though it was configured at 60fps.  I can't recall if I got it to display at all.  This performance is not good enough.

## PeerStreamer

PeerStreamer was looked into but unfortunately it requires the use of something else like ffmpeg to do a live stream from a webcam (ffmpeg was too slow).
