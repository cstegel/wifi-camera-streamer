import numpy as np
import cv2
import os
import socket
import time
import pickle
import sys
from cam import network
from functools import partial


HOST_IP = '127.0.0.1'
HOST_PORT = 8479

def get_frame(video_capture, ip):
  ret, frame = video_capture.read()
  #print('\n'.join(dir(frame)))
  #print(frame.dtype)
  #print(frame.shape)
  
  return frame.tostring()

def get_msg(ip):
  return 'hello world!'
  
def got_msg(msg):
  frame = np.fromstring(msg, 'uint8')
  #print(frame.shape)
  try:
    frame = frame.reshape(480, 640, 3)
  except ValueError:
    print('failed to reshape message')
    return
  cv2.imshow('frame', frame)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    print('PRESSED Q')
    sys.exit(0)

if __name__ == '__main__':
  port = sys.argv[2] or HOST_PORT
  ip = sys.argv[3] or HOST_IP
  
  if sys.argv[1] == 'sender':
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
      print('\n'.join(dir(cap)))
      print('Could not connect to video camera')
      sys.exit(1)
    sender = network.UdpSender(partial(get_frame, cap), ip, port)
    sender.send_forever()
    
  elif sys.argv[1] == 'receiver':
    client = network.UdpReceiver(ip, port, got_msg)
    client.receive_forever()
    cv2.destroyAllWindows()
    
  else: 
    print('Usage: <script> sender|receiver port ip')
      