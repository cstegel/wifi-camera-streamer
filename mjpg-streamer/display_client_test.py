import time
import cv2
import sys

import argparse


def start_vid_player(host, port):
  # Script to test if OpenCV is working by streaming video from a
  # camera device.  Intended for OpenCV 3, incompatible with OpenCV 2

  cv2.namedWindow("preview")
  vc = cv2.VideoCapture("http://localhost:8090/?action=stream")

  # vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
  # vc.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

  # print('res: %sx%s, FPS: %s' % (vc.get(cv2.CAP_PROP_FRAME_WIDTH),
  #   vc.get(cv2.CAP_PROP_FRAME_HEIGHT), vc.get(cv2.CAP_PROP_FPS)))

  if not vc.isOpened():
    print('failed to open VideoCapture, exiting')
    sys.exit(1)

  frame_count = 0
  start_time = time.time()

  # read once to initialize the "frame" container
  rval, frame = vc.read()

  while True:
    rval, frame = vc.read(frame)

    if not rval:
      break
      
    cv2.imshow("preview", frame)
    # opencv interprets the incoming RGB as BGR, need to convert it???
    # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # display the image, exit if ESC was pressed
    key = cv2.waitKey(1)
    if key == 27:
      break

    # output fps
    frame_count += 1
    if frame_count >= 30:
      end_time = time.time()
      print('%ffps' % (frame_count / (end_time - start_time)))
      frame_count = 0
      start_time = end_time

  cv2.destroyWindow("preview")

def main():
  parser = argparse.ArgumentParser(description='Connect to and play an mjpg-streamer video stream')
  parser.add_argument('-H', '--host', type=str, default='localhost',
                      help='host to connect to that is serving the video stream')
  parser.add_argument('-p', '--port', type=int, default='8090',
                      help='port for the host that is serving the video stream')
  args = parser.parse_args()
  
  start_vid_player(args.host, args.port)

if __name__ == '__main__':
  main()