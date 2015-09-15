import time
import cv2

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
vc.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

print('res: %sx%s, FPS: %s' % (vc.get(cv2.CAP_PROP_FRAME_WIDTH),
  vc.get(cv2.CAP_PROP_FRAME_HEIGHT), vc.get(cv2.CAP_PROP_FPS)))

if vc.isOpened(): # try to get the first frame
  print('opened')
  rval, frame = vc.read()
else:
  print('not opened')
  rval = False

frame_count = 0
start_time = time.time()

while rval:
  cv2.imshow("preview", frame)
  rval, frame = vc.read(frame)
  key = cv2.waitKey(1)
  if key == 27: # exit on ESC
    break

  frame_count += 1
  if frame_count >= 30:
    end_time = time.time()
    print('%ffps' % (frame_count / (end_time - start_time)))
    frame_count = 0
    start_time = end_time

cv2.destroyWindow("preview")
