import cv2
from cv2 import cv
import time
import numpy as np

cam = cv2.VideoCapture(0)
cam.set(cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 720)
cam.set(cv.CV_CAP_PROP_FPS, 60)

writer  = cv2.VideoWriter()
writer.open('video2.avi', cv.CV_FOURCC('M', 'J', 'P', 'G'), 60, (1280, 720))
print('writer opened: %s' % writer.isOpened())
print('reader opened: %s' % cam.isOpened())
print('format: %s' % cam.get(cv.CV_CAP_PROP_FORMAT))
print('fps: %s' % cam.get(cv.CV_CAP_PROP_FPS))
print('width: %s' % cam.get(cv.CV_CAP_PROP_FRAME_WIDTH))
print('height: %s' % cam.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
print('4cc: %s' % cam.get(cv.CV_CAP_PROP_FOURCC))
print('mode: %s' % cam.get(cv.CV_CAP_PROP_MODE))

start_time = time.time()
frames = 0
# capture_buffer = np.empty(shape=(800, 600, 3), dtype=np.uint8)
_, capture_buffer = cam.read()

while frames <= 180:
  cam.grab()
  rval, capture_buffer = cam.retrieve(capture_buffer)
  #writer.write(capture_buffer)
  # cv2.imshow("webcam",frame)
  
  # wait for any key press
  # if (cv2.waitKey(1) != -1):
  #   break
  frames += 1

fps = frames / (time.time() - start_time)
print('%s fps while recording' % fps)

# start_time = time.time()
# for frame in frame_list:
#   writer.write(frame)
# fps = len(frame_list) / (time.time() - start_time)
# print('%s fps while writing' % fps)

writer.release() 