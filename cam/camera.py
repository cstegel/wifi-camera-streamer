import numpy as np
import cv2
import os
import socket
import time
import pickle
from cam import network
from functools import partial

# 
# while(True):
#   # Capture frame-by-frame
#   ret, frame = cap.read()
# 
#   # Our operations on the frame come here
#   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 
#   # Display the resulting frame
#   cv2.imshow('frame',frame)
#   keycode = cv2.waitKey(1)
#   print(keycode)
#   if keycode & 0xFF == ord('q'):
#     break
# 
# # When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()


HOST_IP = '127.0.0.1'
HOST_PORT = 8473

def get_frame(video_capture, ip):
  ret, frame = video_capture.read()
  print('\n'.join(dir(frame)))
  print(frame.dtype)
  print(frame.shape)
  
  return frame.tostring()

def get_msg(ip):
  return 'hello world!'

if __name__ == '__main__':
  is_parent = os.fork()
  
  if is_parent:
    cap = cv2.VideoCapture(0)
    server = network.Server(socket.SOCK_STREAM, 
      partial(get_frame, cap), HOST_IP, HOST_PORT)
    server.serve()
  else:
    time.sleep(0.1)
    while True:
      client = network.Client(socket.SOCK_STREAM)
      data = client.receive(HOST_IP, HOST_PORT)
      frame = np.fromstring(data, 'uint8')
      print(frame.shape)
      frame = frame.reshape(480, 640, 3)
      cv2.imshow('frame', frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.destroyAllWindows()
      