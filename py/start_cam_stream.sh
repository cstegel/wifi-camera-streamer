#!/bin/bash
# must be run from directory with mjpg_streamer binary
# eg:  ~/git/mjpg-streamer/mjpg-streamer-experimental
if [ $# -ne 1 ]; then
  me=`basename "$0"`
  echo "Usage: $me <path to mjpg_streamer binary folder (that contains the plugins folder as well)>"
  exit 1
fi

export LD_LIBRARY_PATH=$1
$1/mjpg_streamer -i "input_uvc.so --device /dev/video0 -r 1280x720 --fps 60" -o "output_http.so -p 8090 -w ./www"
