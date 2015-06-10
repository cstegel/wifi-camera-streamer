import cv2

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
  print('opened')
  rval, frame = vc.read()
else:
  print('not opened')
  rval = False

while rval:
  cv2.imshow("preview", frame)
  rval, frame = vc.read()
  key = cv2.waitKey(20)
  if key == 27: # exit on ESC
    break
cv2.destroyWindow("preview")