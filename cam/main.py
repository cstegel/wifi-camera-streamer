
import sys
print('\n'.join(sys.path))
import cam
import socket

def create_string(*args):
  return '123456789' * 1000 
  
if __name__ == '__main__':
  port = 3413
  if sys.argv[1] == 'client':
    while True:
      client = cam.network.Client(socket.SOCK_STREAM)
      print("received: %s" % client.receive('127.0.0.1', port))
  elif sys.argv[1] == 'server':
    server = cam.network.Server(socket.SOCK_STREAM, create_string, '127.0.0.1', port)
    server.serve()
  else:
    print 'only client or server'
