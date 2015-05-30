import socket
import cv2
import sys

MSG = 'hello world!'


class Server(object):
  SERVER_HOST = ''
  SERVER_PORT = 1436
  
  def __init__(self, sock_type, get_msg, host_ip=None, host_port=None):
    self.host_ip = host_ip or self.SERVER_HOST
    self.host_port = host_port or self.SERVER_PORT
    self.sock = socket.socket(socket.AF_INET, sock_type)
    self.get_msg = get_msg
    
  def serve(self):
    self.sock.bind((self.host_ip, self.host_port))
    self.sock.listen(1)
    
    while True:
      (client, addr) = self.sock.accept()
      total_sent_bytes = 0
      msg = self.get_msg(addr)
      
      while total_sent_bytes < len(msg):
        sent_bytes = client.send(msg[total_sent_bytes:])
        if sent_bytes == 0:
          print('socket connection broken (server)')  # TODO: raise/log?
        total_sent_bytes += sent_bytes
      client.close()
    self.sock.close()
    
def start_server():
  # create a UDP server socket    # SOCK_DGRAM
  server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_sock.bind((SERVER_HOST, SERVER_PORT))
  server_sock.listen(1)

  sent_bytes = 0
  # accept a connection
  (client_sock, address) = server_sock.accept()
  print('accepted (server)')
  while sent_bytes < len(MSG):
    # write stuff to the socket
    sent = client_sock.send(MSG[sent_bytes:])
    if sent == 0:
      raise RuntimeError('socket connection broken (server)')
    sent_bytes += sent
    
  client_sock.close()
  server_sock.close()
     
def create_client():
  client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_sock.connect((SERVER_HOST, SERVER_PORT))
  print('connected (client)')
  chunks = []
  bytes_recd = 0
  while bytes_recd < len(MSG):
    chunk = client_sock.recv(min(len(MSG) - bytes_recd, 2048))
    if chunk == '':
      raise RuntimeError('socket conenction broken (client)')
    chunks.append(chunk)
    bytes_recd += len(chunk)
  msg = ''.join(chunks)
  client_sock.close()
  print(msg)
  
if __name__ == '__main__':
  if sys.argv[1] == 'client':
    create_client()
  elif sys.argv[1] == 'server':
    start_server()
  else:
    print 'only client or server'
