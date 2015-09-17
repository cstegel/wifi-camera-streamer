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



  1. `apt-get install libv4l-dev libjpeg8-dev imagemagick build-essential cmake subversion`
  2. `git clone https://github.com/codewithpassion/mjpg-streamer`
    - verified to work with commit a48d422 (bookmarked as https://github.com/LlazyLlama/mjpg-streamer)
  3. `cd mjpg-streamer-experimental`
  4. `make`
  
# Running the camera stream

Start the camera HTTP stream by doing the following:

`./start_cam_stream.sh <path to mjpg_streamer binary directory>`
    - this folder will also contain the plugins folder 
    - eg: ~/git/mjpg-streamer/mjpg-streamer-experimental
  
# Running the display client

After the camera stream is running, simply run `python py/display_client_test.py` to connect to the HTTP camera stream and display it.
