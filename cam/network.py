import socket

class Server(object):
  SERVER_HOST = ''
  SERVER_PORT = 1436
  
  def __init__(self, sock_type, get_msg, host_ip=None, host_port=None):
    self.host_ip = host_ip or self.SERVER_HOST
    self.host_port = int(host_port) or self.SERVER_PORT
    self.sock = socket.socket(socket.AF_INET, sock_type)
    self.get_msg = get_msg
    
  def serve(self):
    self.sock.bind((self.host_ip, self.host_port))
    print('connected @ %s:%s' % (self.host_ip, self.host_port))
    self.sock.listen(1)
    
    while True:
      (client, addr) = self.sock.accept()
      print('client: %s' % str(addr))
      total_sent_bytes = 0
      msg = self.get_msg(addr)
      
      while total_sent_bytes < len(msg):
        sent_bytes = client.send(msg[total_sent_bytes:])
        if sent_bytes == 0:
          print('socket connection broken (server)')  # TODO: raise/log?
        total_sent_bytes += sent_bytes
      client.shutdown(socket.SHUT_RDWR)
      client.close()
    self.sock.shutdown(socket.SHUT_RDWR)
    self.sock.close()
    
  def __del__(self):
    self.sock.shutdown(socket.SHUT_RDWR)
    self.sock.close()
    
class Client(object):
  
  def __init__(self, sock_type):
    self.sock = socket.socket(socket.AF_INET, sock_type)
    
  def receive(self, ip, port):
    self.sock.connect((ip, int(port)))
    chunks = []
    bytes_recd = 0
    while True:
      chunk = self.sock.recv(2048)
      if chunk == '':
        break
      chunks.append(chunk)
      bytes_recd += len(chunk)
    self.sock.shutdown(socket.SHUT_RDWR)
    self.sock.close()
    return ''.join(chunks)
    
  
