#!/bin/bash
# must be run from directory with mjpg_streamer binary
# eg:  ~/git/mjpg-streamer/mjpg-streamer-experimental
if [ $# -ne 2 ]; then
  me=`basename "$0"`
  echo "Usage: $me <directory containing mjpg_streamer binary> </dev/video device # capture from>"
  echo "   ex: $me ~/git/mjpg-streamer-mjpg-streamer 0"
  echo "     - this uses /dev/video0"
  exit 1
fi

export LD_LIBRARY_PATH=$1
$1/mjpg_streamer -i "input_uvc.so --device /dev/video$2 -r 1280x720 --fps 60" -o "output_http.so -p 8090 -w ./www"
